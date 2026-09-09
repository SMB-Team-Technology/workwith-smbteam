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
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { getFathomTranscript, shouldSkipFathomOverwrite } from '../lib/fathom.mjs';

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
  const out = await getFathomTranscript('jane@examplefirm.com', 'Jane', 'k');
  assert.match(out, /No Fathom transcript available \(API returned 401/);
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
  const out = await getFathomTranscript('jane@examplefirm.com', 'Jane', 'k');
  assert.match(out, /lookup error: ECONNRESET/);
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

test('hitting the pagination cap warns that the scan is incomplete', async () => {
  const warnings = [];
  const realWarn = console.warn;
  console.warn = (...a) => warnings.push(a.join(' '));
  try {
    stubFetch(() => jsonResponse({ items: [], next_cursor: 'more' }));
    const out = await getFathomTranscript('jane@examplefirm.com', 'Jane', 'k');
    assert.equal(calls.length, 5, 'stops at MAX_PAGES');
    assert.ok(warnings.some(w => /pagination cap hit/i.test(w)), 'must warn the scan was incomplete');
    assert.match(out, /No Fathom transcript found/);
  } finally {
    console.warn = realWarn;
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
    assert.equal(spawnSync(process.execPath, [script, realFile]).status, 0);
    assert.equal(spawnSync(process.execPath, [script, missFile]).status, 1);
    assert.equal(spawnSync(process.execPath, [script, noteFile]).status, 0);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
