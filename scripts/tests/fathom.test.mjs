/**
 * fathom.test.mjs — unit tests for scripts/lib/fathom.mjs
 *
 * Run: node --test scripts/tests/fathom.test.mjs
 *
 * Network is stubbed by replacing global.fetch per test. Pins the contract
 * for the real Fathom external API (api.fathom.ai, X-Api-Key, full transcript)
 * plus shouldSkipFathomOverwrite — the GHA HubSpot/summary step must not
 * clobber a real transcript.
 *
 * Call signature matches current main schedulers:
 *   getFathomTranscript(email, contactName, apiKey, fathomUrl?)
 */

import { test, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, writeFileSync, rmSync, readFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  getFathomTranscript,
  getFathomTranscriptResult,
  shouldSkipFathomOverwrite,
  mergeTrigger,
  writeTriggerAtomic,
} from '../lib/fathom.mjs';

const realFetch = global.fetch;
let calls;

function stubFetch(handler) {
  global.fetch = async (url, opts) => {
    calls.push({ url: String(url), opts });
    return handler(String(url), opts);
  };
}

function jsonResponse(body, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
    text: async () => JSON.stringify(body),
  };
}

function meeting({ email = 'libby@indianaimmigration.com', title = 'Discovery Call', created = '2026-06-01T00:00:00Z', transcript = null, id = 'rec1' } = {}) {
  return {
    recording_id: id,
    title,
    created_at: created,
    calendar_invitees: [{ email }],
    transcript,
  };
}

beforeEach(() => { calls = []; });
afterEach(() => { global.fetch = realFetch; });

test('calls the documented endpoint with X-Api-Key and include_transcript=true', async () => {
  stubFetch(() => jsonResponse({ items: [] }));
  await getFathomTranscript('jane@examplefirm.com', 'Jane', 'key-123');
  assert.equal(calls.length, 1);
  assert.match(calls[0].url, /^https:\/\/api\.fathom\.ai\/external\/v1\/meetings\?/);
  assert.match(calls[0].url, /include_transcript=true/);
  assert.equal(calls[0].opts.headers['X-Api-Key'], 'key-123');
  assert.equal(calls[0].opts.headers['Authorization'], undefined);
});

test('does not call fathom.video even when a fathomUrl is passed', async () => {
  stubFetch(() => jsonResponse({ items: [] }));
  await getFathomTranscript(
    'jane@examplefirm.com',
    'Jane',
    'key-123',
    'https://fathom.video/calls/704816497',
  );
  assert.ok(calls.length >= 1);
  for (const c of calls) {
    assert.doesNotMatch(c.url, /fathom\.video/);
  }
});

test('filters by the contact email domain when it is a custom domain', async () => {
  stubFetch(() => jsonResponse({ items: [] }));
  await getFathomTranscript('jane@examplefirm.com', 'Jane', 'k');
  assert.match(decodeURIComponent(calls[0].url), /calendar_invitees_domains\[\]=examplefirm\.com/);
});

test('does NOT filter by domain for free-mail addresses', async () => {
  stubFetch(() => jsonResponse({ items: [] }));
  await getFathomTranscript('jane@gmail.com', 'Jane', 'k');
  assert.doesNotMatch(decodeURIComponent(calls[0].url), /calendar_invitees_domains/);
});

test('returns the full speaker-attributed transcript for the exact invitee', async () => {
  const tx = [
    { speaker: { display_name: 'Libby' }, text: 'We keep our marketing in-house.', timestamp: '00:01' },
    { speaker: { display_name: 'Rep' }, text: 'Understood.', timestamp: '00:02' },
  ];
  stubFetch(() => jsonResponse({ items: [
    meeting({ email: 'other@elsewhere.com', transcript: [{ speaker: { display_name: 'X' }, text: 'wrong call' }] }),
    meeting({ transcript: tx }),
  ] }));
  const out = await getFathomTranscript('libby@indianaimmigration.com', 'Libby', 'k');
  assert.match(out, /Libby \(00:01\): We keep our marketing in-house\./);
  assert.match(out, /Rep \(00:02\): Understood\./);
  assert.doesNotMatch(out, /wrong call/);
});

test('picks the most recent matching meeting', async () => {
  stubFetch(() => jsonResponse({ items: [
    meeting({ created: '2026-05-01T00:00:00Z', transcript: [{ speaker: { display_name: 'A' }, text: 'older call' }] }),
    meeting({ created: '2026-06-05T00:00:00Z', transcript: [{ speaker: { display_name: 'A' }, text: 'newer call' }] }),
  ] }));
  const out = await getFathomTranscript('libby@indianaimmigration.com', 'Libby', 'k');
  assert.match(out, /newer call/);
  assert.doesNotMatch(out, /older call/);
});

test('truncates transcripts above the max-chars cap with an explicit marker', async () => {
  const seg = { speaker: { display_name: 'A' }, text: 'x'.repeat(10_000) };
  stubFetch(() => jsonResponse({ items: [meeting({ transcript: Array(40).fill(seg) })] }));
  const out = await getFathomTranscript('libby@indianaimmigration.com', 'Libby', 'k');
  assert.ok(out.length <= 300_000 + 100);
  assert.match(out, /TRANSCRIPT TRUNCATED/);
});

test('follows pagination cursors', async () => {
  let page = 0;
  stubFetch(() => {
    page++;
    if (page === 1) return jsonResponse({ items: [], next_cursor: 'abc' });
    return jsonResponse({ items: [meeting({ transcript: [{ speaker: { display_name: 'A' }, text: 'page two' }] })] });
  });
  const out = await getFathomTranscript('libby@indianaimmigration.com', 'Libby', 'k');
  assert.equal(calls.length, 2);
  assert.match(calls[1].url, /cursor=abc/);
  assert.match(out, /page two/);
});

test('API error returns a descriptive no-transcript message, never throws', async () => {
  stubFetch(() => jsonResponse({ error: 'nope' }, 401));
  const r = await getFathomTranscriptResult('jane@examplefirm.com', 'Jane', 'k');
  assert.equal(r.status.outcome, 'unknown');
  assert.equal(r.status.reason, 'http_error');
  assert.match(r.text, /^Fathom lookup incomplete for Jane \(jane@examplefirm.com\)/);
  assert.doesNotMatch(r.text, /^No Fathom transcript found for/);
});

test('later-page HTTP error keeps meetings already fetched', async () => {
  let page = 0;
  stubFetch(() => {
    page++;
    if (page === 1) {
      return jsonResponse({
        items: [meeting({ transcript: [{ speaker: { display_name: 'A' }, text: 'page one hit' }] })],
        next_cursor: 'more',
      });
    }
    return jsonResponse({ error: 'nope' }, 429);
  });
  const out = await getFathomTranscript('libby@indianaimmigration.com', 'Libby', 'k');
  assert.match(out, /page one hit/);
  assert.doesNotMatch(out, /No Fathom transcript available \(API returned/);
});

test('later-page throw keeps meetings already fetched', async () => {
  let page = 0;
  stubFetch(() => {
    page++;
    if (page === 1) {
      return jsonResponse({
        items: [meeting({ transcript: [{ speaker: { display_name: 'A' }, text: 'before hang' }] })],
        next_cursor: 'more',
      });
    }
    throw new Error('ECONNRESET');
  });
  const out = await getFathomTranscript('libby@indianaimmigration.com', 'Libby', 'k');
  assert.match(out, /before hang/);
  assert.doesNotMatch(out, /lookup error: ECONNRESET/);
});

test('network failure returns a descriptive message, never throws', async () => {
  global.fetch = async () => { throw new Error('ECONNRESET'); };
  const r = await getFathomTranscriptResult('jane@examplefirm.com', 'Jane', 'k');
  assert.equal(r.status.outcome, 'unknown');
  assert.equal(r.status.reason, 'network_error');
  assert.match(r.text, /^Fathom lookup incomplete for Jane \(jane@examplefirm.com\)/);
  assert.match(r.text, /lookup error: ECONNRESET/);
});

test('missing API key and missing email are handled without a network call', async () => {
  stubFetch(() => { throw new Error('should not be called'); });
  const noKey = await getFathomTranscript('jane@examplefirm.com', 'Jane', '');
  assert.match(noKey, /FATHOM_API_KEY secret is not configured/);
  const noEmail = await getFathomTranscript('', 'Jane', 'k');
  assert.match(noEmail, /no email on file/);
  assert.equal(calls.length, 0);
});

test('meeting found but empty transcript flags for the rep', async () => {
  stubFetch(() => jsonResponse({ items: [meeting({ transcript: [] })] }));
  const out = await getFathomTranscript('libby@indianaimmigration.com', 'Libby', 'k');
  assert.match(out, /transcript was empty — flag for the rep/);
});

test('every request carries an abort signal so a hung connection cannot hang the scheduler', async () => {
  stubFetch(() => jsonResponse({ items: [] }));
  await getFathomTranscript('jane@examplefirm.com', 'Jane', 'k');
  assert.ok(calls[0].opts.signal instanceof AbortSignal, 'fetch options must include an AbortSignal timeout');
});

test('hitting the pagination cap is an incomplete scan, not a confirmed miss', async () => {
  const warnings = [];
  const realWarn = console.warn;
  console.warn = (...a) => warnings.push(a.join(' '));
  try {
    stubFetch(() => jsonResponse({ items: [], next_cursor: 'more' }));
    const r = await getFathomTranscriptResult('jane@examplefirm.com', 'Jane', 'k');
    assert.equal(calls.length, 5, 'stops at MAX_PAGES');
    assert.ok(warnings.some(w => /incomplete/i.test(w)), 'must warn the scan was incomplete');
    assert.equal(r.status.outcome, 'unknown');
    assert.equal(r.status.reason, 'page_cap');
    assert.equal(r.status.pages_fetched, 5);
    assert.match(r.text, /^Fathom lookup incomplete for/);
    assert.doesNotMatch(r.text, /^No Fathom transcript found for/);
  } finally {
    console.warn = realWarn;
  }
});

test('live getFathomTranscript miss strings allow GHA overwrite', async () => {
  stubFetch(() => jsonResponse({ error: 'nope' }, 401));
  const produced = [
    await getFathomTranscript('jane@examplefirm.com', 'Jane', ''),
    await getFathomTranscript('', 'Jane', 'k'),
    await getFathomTranscript('jane@examplefirm.com', 'Jane', 'k'),
  ];
  global.fetch = async () => { throw new Error('ECONNRESET'); };
  produced.push(await getFathomTranscript('jane@examplefirm.com', 'Jane', 'k'));
  stubFetch(() => jsonResponse({ items: [] }));
  produced.push(await getFathomTranscript('jane@examplefirm.com', 'Jane', 'k'));
  stubFetch(() => jsonResponse({ items: [meeting({ transcript: [] })] }));
  produced.push(await getFathomTranscript('libby@indianaimmigration.com', 'Libby', 'k'));
  for (const out of produced) {
    assert.equal(shouldSkipFathomOverwrite(out), false, out);
  }
});

test('shouldSkipFathomOverwrite is false for empty / miss placeholders (GHA fallback may run)', () => {
  assert.equal(shouldSkipFathomOverwrite(undefined), false);
  assert.equal(shouldSkipFathomOverwrite(null), false);
  assert.equal(shouldSkipFathomOverwrite(''), false);
  assert.equal(shouldSkipFathomOverwrite('   '), false);
  assert.equal(shouldSkipFathomOverwrite('No transcript available. FATHOM_API_KEY secret is not configured.'), false);
  assert.equal(shouldSkipFathomOverwrite('No Fathom transcript lookup possible — contact has no email on file.'), false);
  assert.equal(shouldSkipFathomOverwrite('No Fathom transcript available (API returned 404 for a@b.com).'), false);
  assert.equal(shouldSkipFathomOverwrite('No Fathom transcript available (lookup error: ECONNRESET).'), false);
  assert.equal(shouldSkipFathomOverwrite('No Fathom transcript found for Jane (jane@examplefirm.com).'), false);
  assert.equal(shouldSkipFathomOverwrite('Fathom meeting found ("untitled") but transcript was empty — flag for the rep.'), false);
  assert.equal(shouldSkipFathomOverwrite('No Fathom transcript available — fathom_url not set. Use the /trigger command.'), false);
  assert.equal(shouldSkipFathomOverwrite('Fathom call 704816497 found but summary is unavailable.'), false);
  assert.equal(shouldSkipFathomOverwrite('No Fathom transcript available.'), false);
  assert.equal(shouldSkipFathomOverwrite('No Fathom transcript available — proposal call scheduled for 2026-09-09.'), false);
  assert.equal(shouldSkipFathomOverwrite('No transcript available yet.'), false);
  assert.equal(
    shouldSkipFathomOverwrite('No Fathom transcript available. No recordings found for karla@santiagolegalgroup.com.'),
    false,
  );
  assert.equal(
    shouldSkipFathomOverwrite('No Fathom transcript available (API returned 404 for a@b.com). No recordings found for a@b.com.'),
    false,
  );
  assert.equal(
    shouldSkipFathomOverwrite('Fathom lookup incomplete for Jane (jane@examplefirm.com) — 429 on page 2. This is not a confirmed absence.'),
    false,
  );
});

test('shouldSkipFathomOverwrite is true for a real speaker transcript and for an existing HubSpot summary', () => {
  const real = 'Libby (00:01): We keep marketing in-house.\nRep (00:02): Understood.';
  assert.equal(shouldSkipFathomOverwrite(real), true);
  const hubspot = 'SOURCE: Fathom (via HubSpot internal notes) — https://fathom.video/share/abc\n\nAI Meeting Summary';
  assert.equal(shouldSkipFathomOverwrite(hubspot), true);
  const directSummary = 'SOURCE: Fathom (direct) — https://fathom.video/calls/1\n\nSome summary';
  assert.equal(shouldSkipFathomOverwrite(directSummary), true);
});

test('shouldSkipFathomOverwrite is true when a miss prefix is followed by sales-rep notes', () => {
  const withNote = 'No Fathom transcript available (API returned 404 for mymzheng@gmail.com). SALES REP NOTE: Recommend FCOO Advisor only — no marketing package.';
  assert.equal(shouldSkipFathomOverwrite(withNote), true);
  assert.equal(
    shouldSkipFathomOverwrite('No Fathom transcript found for Jane (a@b.com).\nSALES REP NOTE: keep this'),
    true,
  );
  assert.equal(
    shouldSkipFathomOverwrite('No Fathom transcript found for Jane (a@b.com). SALES REP NOTE: push FCOO advisor (not marketing).'),
    true,
  );
  assert.equal(
    shouldSkipFathomOverwrite('No Fathom transcript available. SALES REP NOTE: Phase 1 recommendation is Full Service Marketing Starter only. Do not recommend a coaching or non-marketing package at this stage.'),
    true,
  );
  assert.equal(
    shouldSkipFathomOverwrite('No Fathom transcript available — proposal call scheduled for 2026-09-09. SALES REP NOTE: FCOO only.'),
    true,
  );
});

test('skip-fathom-overwrite.mjs exits 0 for a real transcript and 1 for a miss', () => {
  const dir = mkdtempSync(join(tmpdir(), 'fathom-skip-'));
  const realFile = join(dir, 'real.json');
  const missFile = join(dir, 'miss.json');
  writeFileSync(realFile, JSON.stringify({ transcript: 'Libby (00:01): hello' }));
  writeFileSync(missFile, JSON.stringify({ transcript: 'No Fathom transcript found for Jane (a@b.com).' }));
  const script = fileURLToPath(new URL('../skip-fathom-overwrite.mjs', import.meta.url));
  try {
    const noteFile = join(dir, 'note.json');
    writeFileSync(noteFile, JSON.stringify({
      transcript: 'No Fathom transcript available (API returned 404 for a@b.com). SALES REP NOTE: keep this',
    }));
    const bareNoteFile = join(dir, 'bare-note.json');
    writeFileSync(bareNoteFile, JSON.stringify({
      transcript: 'No Fathom transcript available. SALES REP NOTE: Phase 1 recommendation is Full Service Marketing Starter only.',
    }));
    const badJson = join(dir, 'bad.json');
    writeFileSync(badJson, '{not json');
    const missing = join(dir, 'no-such.json');
    assert.equal(spawnSync(process.execPath, [script, realFile]).status, 0);
    assert.equal(spawnSync(process.execPath, [script, missFile]).status, 1);
    assert.equal(spawnSync(process.execPath, [script, noteFile]).status, 0);
    assert.equal(spawnSync(process.execPath, [script, bareNoteFile]).status, 0);
    assert.equal(spawnSync(process.execPath, [script]).status, 2);
    assert.equal(spawnSync(process.execPath, [script, missing]).status, 2);
    assert.equal(spawnSync(process.execPath, [script, badJson]).status, 2);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

// The skip rules and the leave-unchanged-on-error behaviour that used to live
// in the fetch steps' bash now belong to fetch-pass1-transcript.mjs (see
// fetch-pass1-transcript.test.mjs). What the workflows must still guarantee:
// the step always runs — an empty Slack trigger has no fathom_url and no
// transcript — and it goes through the API script, never fathom.video.
test('GHA fetch steps always run and delegate to fetch-pass1-transcript.mjs', () => {
  const root = fileURLToPath(new URL('../..', import.meta.url));
  for (const rel of [
    '.github/workflows/audit-pipeline.yml',
    '.github/workflows/rerun-research.yml',
  ]) {
    const yml = readFileSync(join(root, rel), 'utf8');
    const step = yml.split(/\n {6}- name: /).find(s => s.startsWith('Fetch Fathom transcript'));
    assert.ok(step, `${rel}: no "Fetch Fathom transcript" step`);
    assert.doesNotMatch(step, /^ {8}if:/m, `${rel}: the fetch step must not be conditional`);
    assert.match(step, /node scripts\/fetch-pass1-transcript\.mjs/, rel);
    assert.match(step, /FATHOM_API_KEY: \$\{\{ secrets\.FATHOM_API_KEY \}\}/, rel);
    assert.match(step, /HUBSPOT_TOKEN: \$\{\{ secrets\.HUBSPOT_TOKEN \}\}/, rel);
    assert.doesNotMatch(step, /fathom\.video/, `${rel}: fathom.video is not the API`);
    assert.doesNotMatch(step, /Authorization: Bearer \$FATHOM_API_KEY/, rel);
    assert.doesNotMatch(step, /SKIP_RC/, `${rel}: the script owns the skip rules`);
    assert.doesNotMatch(step, /\.transcript = \$t \| \.transcript_status/, rel);
  }
});

test('page 1 unrelated meetings plus page 2 HTTP error is unknown, not absent', async () => {
  let page = 0;
  stubFetch(() => {
    page++;
    if (page === 1) {
      return jsonResponse({
        items: [meeting({ email: 'someone.else@gmail.com', transcript: [{ speaker: { display_name: 'X' }, text: 'other call' }] })],
        next_cursor: 'more',
      });
    }
    return jsonResponse({ error: 'rate' }, 429);
  });
  const r = await getFathomTranscriptResult('teddy@gmail.com', 'Teddy', 'k');
  assert.equal(r.status.outcome, 'unknown');
  assert.equal(r.status.reason, 'http_error');
  assert.match(r.text, /^Fathom lookup incomplete for Teddy \(teddy@gmail.com\)/);
  assert.doesNotMatch(r.text, /^No Fathom transcript found for/);
  assert.equal(shouldSkipFathomOverwrite({ transcript: r.text, transcript_status: r.status }), false);
});

test('page 1 unrelated meetings plus page 2 throw is unknown', async () => {
  let page = 0;
  stubFetch(() => {
    page++;
    if (page === 1) {
      return jsonResponse({
        items: [meeting({ email: 'other@gmail.com' })],
        next_cursor: 'more',
      });
    }
    throw new Error('ECONNRESET');
  });
  const r = await getFathomTranscriptResult('teddy@gmail.com', 'Teddy', 'k');
  assert.equal(r.status.outcome, 'unknown');
  assert.equal(r.status.reason, 'network_error');
  assert.match(r.text, /^Fathom lookup incomplete for/);
});

test('natural exhaustion with no invitee is absent and uses the confirmed-miss sentence', async () => {
  stubFetch(() => jsonResponse({ items: [] }));
  const r = await getFathomTranscriptResult('jane@examplefirm.com', 'Jane', 'k');
  assert.equal(r.status.outcome, 'absent');
  assert.equal(r.status.reason, 'exhausted');
  assert.match(r.text, /^No Fathom transcript found for Jane \(jane@examplefirm.com\)\./);
  assert.notEqual(r.status.outcome, 'unknown');
});

test('domain meetings with no exact invitee match are unknown, not absent', async () => {
  stubFetch(() => jsonResponse({
    items: [meeting({ email: 'partner@examplefirm.com', transcript: [{ speaker: { display_name: 'P' }, text: 'the call' }] })],
  }));
  const r = await getFathomTranscriptResult('jane@examplefirm.com', 'Jane', 'k');
  assert.equal(r.status.outcome, 'unknown');
  assert.equal(r.status.reason, 'no_invitee_match');
  assert.doesNotMatch(r.text, /^No Fathom transcript found for/);
  assert.match(r.text, /^Fathom lookup incomplete for/);
});

test('absent and unknown produce different leading sentences', async () => {
  stubFetch(() => jsonResponse({ items: [] }));
  const absent = await getFathomTranscriptResult('jane@examplefirm.com', 'Jane', 'k');
  let page = 0;
  stubFetch(() => {
    page++;
    if (page === 1) return jsonResponse({ items: [meeting({ email: 'other@gmail.com' })], next_cursor: 'c' });
    return jsonResponse({ error: 'nope' }, 429);
  });
  const unknown = await getFathomTranscriptResult('teddy@gmail.com', 'Teddy', 'k');
  assert.equal(absent.status.outcome, 'absent');
  assert.equal(unknown.status.outcome, 'unknown');
  assert.match(absent.text, /^No Fathom transcript found for/);
  assert.match(unknown.text, /^Fathom lookup incomplete for/);
});

test('exact hit before a later-page failure still returns found content', async () => {
  let page = 0;
  stubFetch(() => {
    page++;
    if (page === 1) {
      return jsonResponse({
        items: [meeting({ transcript: [{ speaker: { display_name: 'A' }, text: 'page one hit' }] })],
        next_cursor: 'more',
      });
    }
    return jsonResponse({ error: 'nope' }, 429);
  });
  const r = await getFathomTranscriptResult('libby@indianaimmigration.com', 'Libby', 'k');
  assert.equal(r.status.outcome, 'found');
  assert.match(r.text, /page one hit/);
});

test('empty matched transcript is found_empty', async () => {
  stubFetch(() => jsonResponse({ items: [meeting({ transcript: [] })] }));
  const r = await getFathomTranscriptResult('libby@indianaimmigration.com', 'Libby', 'k');
  assert.equal(r.status.outcome, 'found_empty');
  assert.equal(shouldSkipFathomOverwrite({ transcript: r.text, transcript_status: r.status }), false);
});

test('missing key and missing email are unknown not_started', async () => {
  const noKey = await getFathomTranscriptResult('jane@examplefirm.com', 'Jane', '');
  assert.equal(noKey.status.outcome, 'unknown');
  assert.equal(noKey.status.reason, 'not_started');
  const noEmail = await getFathomTranscriptResult('', 'Jane', 'k');
  assert.equal(noEmail.status.outcome, 'unknown');
  assert.equal(noEmail.status.reason, 'not_started');
});

test('malformed items array is unknown protocol_error', async () => {
  stubFetch(() => jsonResponse({ items: { nope: true } }));
  const r = await getFathomTranscriptResult('jane@examplefirm.com', 'Jane', 'k');
  assert.equal(r.status.outcome, 'unknown');
  assert.equal(r.status.reason, 'protocol_error');
  assert.match(r.text, /^Fathom lookup incomplete for/);
});

test('shouldSkipFathomOverwrite prefers transcript_status when present', () => {
  assert.equal(shouldSkipFathomOverwrite({ transcript: 'whatever', transcript_status: { custody: 'human' } }), true);
  assert.equal(shouldSkipFathomOverwrite({
    transcript: 'Libby (00:01): hi',
    transcript_status: { outcome: 'found', custody: 'machine' },
  }), true);
  assert.equal(shouldSkipFathomOverwrite({
    transcript: 'Fathom lookup incomplete for Jane (a@b.com) — 429 on page 2. This is not a confirmed absence.',
    transcript_status: { outcome: 'unknown', custody: 'machine' },
  }), false);
  assert.equal(shouldSkipFathomOverwrite({
    transcript: 'No Fathom transcript found for Jane (a@b.com).',
    transcript_status: { outcome: 'absent', custody: 'machine' },
  }), false);
  assert.equal(shouldSkipFathomOverwrite({
    transcript: 'Fathom lookup timed out.',
    transcript_status: { outcome: 'unknown', custody: 'machine' },
  }), false);
  assert.equal(shouldSkipFathomOverwrite({
    transcript: 'No Fathom transcript found for Jane (a@b.com). SALES REP NOTE: FCOO only',
    transcript_status: { outcome: 'absent', custody: 'machine' },
  }), true);
  const leftover = 'No Fathom transcript available (API returned 404 for a@b.com). Do not recommend coaching.';
  assert.equal(shouldSkipFathomOverwrite({
    transcript: leftover,
    transcript_status: { outcome: 'unknown', custody: 'machine' },
  }), true);
  assert.equal(shouldSkipFathomOverwrite({
    transcript: leftover,
    transcript_status: { outcome: 'absent', custody: 'machine' },
  }), true);
});

test('skip-fathom-overwrite.mjs honors transcript_status on the trigger object', () => {
  const dir = mkdtempSync(join(tmpdir(), 'fathom-status-'));
  const script = fileURLToPath(new URL('../skip-fathom-overwrite.mjs', import.meta.url));
  try {
    const human = join(dir, 'human.json');
    const found = join(dir, 'found.json');
    const unknown = join(dir, 'unknown.json');
    const leftover = join(dir, 'leftover.json');
    writeFileSync(human, JSON.stringify({ transcript: 'x', transcript_status: { custody: 'human' } }));
    writeFileSync(found, JSON.stringify({
      transcript: 'Libby (00:01): hi',
      transcript_status: { outcome: 'found', custody: 'machine' },
    }));
    writeFileSync(unknown, JSON.stringify({
      transcript: 'Fathom lookup incomplete for Jane (a@b.com) — 429 on page 2. This is not a confirmed absence.',
      transcript_status: { outcome: 'unknown', custody: 'machine' },
    }));
    writeFileSync(leftover, JSON.stringify({
      transcript: 'No Fathom transcript available (API returned 404 for a@b.com). Do not recommend coaching.',
      transcript_status: { outcome: 'unknown', custody: 'machine' },
    }));
    assert.equal(spawnSync(process.execPath, [script, human]).status, 0);
    assert.equal(spawnSync(process.execPath, [script, found]).status, 0);
    assert.equal(spawnSync(process.execPath, [script, unknown]).status, 1);
    assert.equal(spawnSync(process.execPath, [script, leftover]).status, 0);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('live note files stay skip=true', () => {
  const root = fileURLToPath(new URL('../..', import.meta.url));
  for (const f of ['hoyer-law.json', 'maiden-law-firm.json', 'lasser-law-group.json']) {
    const trigger = JSON.parse(readFileSync(join(root, 'triggers/audit-research', f), 'utf8'));
    assert.equal(shouldSkipFathomOverwrite(trigger), true, f);
  }
});

test('mergeTrigger keeps an existing real transcript when the new lookup is absent', () => {
  const existing = {
    transcript: 'x'.repeat(4000),
    package: 'FCOO',
    _run: 3,
    extra: 'keep',
  };
  const lookup = {
    text: 'No Fathom transcript found for Jane (a@b.com).',
    status: { outcome: 'absent', reason: 'exhausted', custody: 'machine', source: 'fathom_api', checked_at: '2026-09-11T00:00:00Z' },
  };
  const out = mergeTrigger(existing, { date: 'September 11, 2026', firm_name: 'X' }, lookup);
  assert.equal(out.transcript, existing.transcript);
  assert.equal(out.package, 'FCOO');
  assert.equal(out._run, 3);
  assert.equal(out.extra, 'keep');
  assert.equal(out.transcript_status.outcome, 'found');
  assert.equal(out.firm_name, 'X');
});

test('mergeTrigger preserves SALES REP NOTE through an unknown lookup', () => {
  const note = 'No Fathom transcript available. SALES REP NOTE: Starter only';
  const out = mergeTrigger(
    { transcript: note },
    { date: 'x' },
    {
      text: 'Fathom lookup incomplete for Jane (a@b.com) — 429 on page 2. This is not a confirmed absence.',
      status: { outcome: 'unknown', reason: 'http_error', custody: 'machine' },
    },
  );
  assert.equal(out.transcript, note);
  assert.equal(out.transcript_status.custody, 'human');
});

test('mergeTrigger does not label a kept note as outcome found', () => {
  const note = 'No Fathom transcript available (API returned 404 for a@b.com). SALES REP NOTE: FCOO only';
  const out = mergeTrigger(
    { transcript: note },
    { date: 'x' },
    { text: 'Libby (00:01): hi', status: { outcome: 'found', custody: 'machine', source: 'fathom_api', checked_at: '2026-09-11T00:00:00Z' } },
  );
  assert.equal(out.transcript, note);
  assert.equal(out.transcript_status.custody, 'human');
  assert.equal(out.transcript_status.outcome, 'unknown');
  assert.equal(out.transcript_status.last_attempt_outcome, 'found');
});

test('mergeTrigger keeps leftover closer notes that omit SALES REP NOTE', () => {
  const leftover = 'No Fathom transcript available (API returned 404 for a@b.com). Do not recommend coaching.';
  const out = mergeTrigger(
    { transcript: leftover },
    { date: 'x' },
    {
      text: 'No Fathom transcript found for Jane (a@b.com).',
      status: { outcome: 'absent', reason: 'exhausted', custody: 'machine' },
    },
  );
  assert.equal(out.transcript, leftover);
  assert.equal(out.transcript_status.custody, 'human');
  assert.notEqual(out.transcript_status.outcome, 'found');
  assert.equal(shouldSkipFathomOverwrite(out), true);
});

test('mergeTrigger does not label a notes-only transcript as found', () => {
  const note = 'SALES REP NOTE: recommend FCOO only.';
  const out = mergeTrigger(
    { transcript: note },
    { date: 'x' },
    { text: 'Libby (00:01): hi', status: { outcome: 'found', custody: 'machine', source: 'fathom_api' } },
  );
  assert.equal(out.transcript, note);
  assert.equal(out.transcript_status.custody, 'human');
  assert.notEqual(out.transcript_status.outcome, 'found');
});

test('mergeTrigger upgrades a HubSpot summary to a full fathom_api transcript', () => {
  const summary = 'SOURCE: Fathom (via HubSpot internal notes) — https://fathom.video/share/abc\n\nAI Meeting Summary';
  const full = 'Libby (00:01): We keep marketing in-house.';
  const out = mergeTrigger(
    { transcript: summary, transcript_status: { outcome: 'found', custody: 'machine', source: 'hubspot_notes' } },
    { date: 'x' },
    { text: full, status: { outcome: 'found', custody: 'machine', source: 'fathom_api' } },
  );
  assert.equal(out.transcript, full);
  assert.equal(out.transcript_status.source, 'fathom_api');
});

test('mergeTrigger replaces a machine miss with a found transcript', () => {
  const out = mergeTrigger(
    { transcript: 'No Fathom transcript found for Jane (a@b.com).' },
    { date: 'x' },
    { text: 'Libby (00:01): hi', status: { outcome: 'found', custody: 'machine', source: 'fathom_api' } },
  );
  assert.equal(out.transcript, 'Libby (00:01): hi');
  assert.equal(out.transcript_status.outcome, 'found');
});

test('mergeTrigger on a new file writes incomplete text with machine custody', () => {
  const text = 'Fathom lookup incomplete for Jane (a@b.com) — 429 on page 2. This is not a confirmed absence.';
  const out = mergeTrigger(null, { firm_name: 'Y' }, {
    text,
    status: { outcome: 'unknown', reason: 'http_error' },
  });
  assert.equal(out.firm_name, 'Y');
  assert.equal(out.transcript, text);
  assert.equal(out.transcript_status.outcome, 'unknown');
  assert.equal(out.transcript_status.custody, 'machine');
});

test('mergeTrigger does not replace an existing found transcript with a newer found', () => {
  const first = 'Libby (00:01): original';
  const out = mergeTrigger(
    { transcript: first, transcript_status: { outcome: 'found', custody: 'machine' } },
    {},
    { text: 'newer', status: { outcome: 'found', custody: 'machine' } },
  );
  assert.equal(out.transcript, first);
  assert.equal(out.transcript_status.outcome, 'found');
});

test('writeTriggerAtomic replaces the target via a temp file', () => {
  const dir = mkdtempSync(join(tmpdir(), 'fathom-atomic-'));
  const dest = join(dir, 't.json');
  try {
    writeTriggerAtomic(dest, { ok: true });
    assert.equal(existsSync(dest), true);
    assert.equal(existsSync(`${dest}.tmp`), false);
    assert.equal(JSON.parse(readFileSync(dest, 'utf8')).ok, true);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test('schedulers merge instead of wholesale transcript replace', () => {
  const root = fileURLToPath(new URL('../..', import.meta.url));
  for (const rel of [
    'scripts/check-proposal-bookings.mjs',
    'scripts/check-consultation-meetings.mjs',
  ]) {
    const src = readFileSync(join(root, rel), 'utf8');
    assert.match(src, /mergeTrigger\(/, rel);
    assert.match(src, /writeTriggerAtomic\(/, rel);
    assert.match(src, /getFathomTranscriptResult/, rel);
    assert.doesNotMatch(src, /writeFileSync\(triggerPath/, rel);
  }
});
