/**
 * fetch-pass1-transcript.test.mjs — unit tests for scripts/fetch-pass1-transcript.mjs
 *
 * Run: node --test scripts/tests/fetch-pass1-transcript.test.mjs
 *
 * Pins the Pass 1 Fetch contract: the real Fathom API (api.fathom.ai,
 * X-Api-Key) is ALWAYS attempted — including for Slack-created triggers whose
 * transcript field is empty — and HubSpot internal notes are a fallback only
 * after the API failed to return outcome "found" from source "fathom_api".
 * fathom.video is never called.
 *
 * Network is stubbed (global.fetch) or bypassed entirely by injecting deps.
 */

import { test, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, writeFileSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { runFetchPass1Transcript } from '../fetch-pass1-transcript.mjs';

const SCRIPT = join(dirname(fileURLToPath(import.meta.url)), '..', 'fetch-pass1-transcript.mjs');
const SPEAKER_TRANSCRIPT = 'Libby Martin (0:12): We get maybe 30 leads a month.\nRep (0:31): And how many of those sign?';
const HUBSPOT_NOTES = 'Meeting Purpose\nDiscovery call with Indiana Immigration.\n\nKey Takeaways\n- 30 leads/month, no intake follow-up.';

const realFetch = global.fetch;
const realKey = process.env.FATHOM_API_KEY;
let dir;

beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), 'pass1-fetch-'));
  process.env.FATHOM_API_KEY = 'test-key';
});

afterEach(() => {
  rmSync(dir, { recursive: true, force: true });
  global.fetch = realFetch;
  if (realKey === undefined) delete process.env.FATHOM_API_KEY;
  else process.env.FATHOM_API_KEY = realKey;
});

function writeTrigger(trigger, name = 'indiana-immigration.json') {
  const file = join(dir, name);
  writeFileSync(file, JSON.stringify(trigger, null, 2));
  return file;
}

/** Trigger as the Slack /trigger command writes it: no transcript key at all. */
function slackTrigger(extra = {}) {
  return {
    firm_name: 'Indiana Immigration',
    friendly_name: 'indiana-immigration',
    url: 'https://indianaimmigration.com',
    sales_rep: 'Dan',
    date: '2026-09-16',
    contact_email: 'libby@indianaimmigration.com',
    contact_name: 'Libby Martin',
    hubspot_contact_id: '4455',
    ...extra,
  };
}

function foundResult(text = SPEAKER_TRANSCRIPT) {
  return {
    text,
    status: {
      outcome: 'found',
      custody: 'machine',
      source: 'fathom_api',
      reason: 'matched',
      checked_at: '2026-09-16T12:00:00.000Z',
    },
  };
}

function absentResult() {
  return {
    text: 'No Fathom transcript found for Libby Martin (libby@indianaimmigration.com).',
    status: { outcome: 'absent', custody: 'machine', source: 'fathom_api', reason: 'exhausted' },
  };
}

function unknownResult() {
  return {
    text: 'Fathom lookup incomplete for Libby Martin (libby@indianaimmigration.com) — HTTP 500 on page 1. This is not a confirmed absence.',
    status: { outcome: 'unknown', custody: 'machine', source: 'fathom_api', reason: 'http_error' },
  };
}

/** Recording stubs so each test can assert exactly who was called with what. */
function spies({ transcript = foundResult(), notes = '' } = {}) {
  const transcriptCalls = [];
  const notesCalls = [];
  return {
    transcriptCalls,
    notesCalls,
    deps: {
      getTranscript: async (...args) => {
        transcriptCalls.push(args);
        return typeof transcript === 'function' ? transcript(...args) : transcript;
      },
      getHubSpotNotes: async (...args) => {
        notesCalls.push(args);
        return typeof notes === 'function' ? notes(...args) : notes;
      },
    },
  };
}

test('Slack-created trigger with no transcript key still calls the Fathom API and writes the transcript', async () => {
  const file = writeTrigger(slackTrigger());
  const { deps, transcriptCalls, notesCalls } = spies();

  const res = await runFetchPass1Transcript(file, deps);

  assert.equal(res.exitCode, 0);
  assert.equal(transcriptCalls.length, 1, 'Fathom API must be attempted for empty Slack triggers');
  assert.deepEqual(
    transcriptCalls[0].slice(0, 3),
    ['libby@indianaimmigration.com', 'Libby Martin', 'test-key'],
  );

  const after = JSON.parse(readFileSync(file, 'utf8'));
  assert.equal(after.transcript, SPEAKER_TRANSCRIPT);
  assert.equal(after.transcript_status.outcome, 'found');
  assert.equal(after.transcript_status.source, 'fathom_api');
  assert.equal(after.firm_name, 'Indiana Immigration', 'other trigger fields survive the merge');
  assert.equal(notesCalls.length, 0, 'HubSpot fallback must not run after an API hit');
});

test('email and name fall back to the legacy keys', async () => {
  const file = writeTrigger({
    firm_name: 'Angel Law',
    friendly_name: 'angel-law',
    email: 'rick@angel-law.com',
  });
  const { deps, transcriptCalls } = spies();

  await runFetchPass1Transcript(file, deps);

  assert.deepEqual(transcriptCalls[0].slice(0, 3), ['rick@angel-law.com', 'Angel Law', 'test-key']);
});

test('API found — HubSpot notes are never fetched', async () => {
  const file = writeTrigger(slackTrigger());
  const { deps, notesCalls } = spies({ notes: HUBSPOT_NOTES });

  const res = await runFetchPass1Transcript(file, deps);

  assert.equal(res.exitCode, 0);
  assert.equal(notesCalls.length, 0);
  assert.equal(JSON.parse(readFileSync(file, 'utf8')).transcript, SPEAKER_TRANSCRIPT);
});

test('API absent + HubSpot notes present — falls back to the HubSpot summary', async () => {
  const file = writeTrigger(slackTrigger());
  const { deps, notesCalls } = spies({ transcript: absentResult(), notes: HUBSPOT_NOTES });

  const res = await runFetchPass1Transcript(file, deps);

  assert.equal(res.exitCode, 0);
  assert.deepEqual(notesCalls[0], ['4455']);

  const after = JSON.parse(readFileSync(file, 'utf8'));
  assert.ok(
    after.transcript.startsWith('SOURCE: Fathom (via HubSpot internal notes)\n\n'),
    `unexpected transcript: ${after.transcript.slice(0, 80)}`,
  );
  assert.ok(after.transcript.includes('30 leads/month, no intake follow-up.'));
  assert.equal(after.transcript_status.outcome, 'found');
  assert.equal(after.transcript_status.source, 'hubspot_notes');
  assert.equal(after.transcript_status.custody, 'machine');
});

test('API unknown + HubSpot notes present — falls back to the HubSpot summary', async () => {
  const file = writeTrigger(slackTrigger());
  const { deps } = spies({ transcript: unknownResult(), notes: HUBSPOT_NOTES });

  const res = await runFetchPass1Transcript(file, deps);

  assert.equal(res.exitCode, 0);
  const after = JSON.parse(readFileSync(file, 'utf8'));
  assert.equal(after.transcript_status.source, 'hubspot_notes');
  assert.ok(after.transcript.includes('Discovery call with Indiana Immigration.'));
});

test('lookup miss with no HubSpot notes exits 0 and never fails the job', async () => {
  const file = writeTrigger(slackTrigger());
  const { deps, notesCalls } = spies({ transcript: absentResult(), notes: '   ' });

  const res = await runFetchPass1Transcript(file, deps);

  assert.equal(res.exitCode, 0);
  assert.equal(notesCalls.length, 1);
  const after = JSON.parse(readFileSync(file, 'utf8'));
  assert.equal(after.transcript_status.outcome, 'absent');
  assert.match(after.transcript, /^No Fathom transcript found for/);
});

test('lookup miss with no hubspot_contact_id exits 0 without touching HubSpot', async () => {
  const file = writeTrigger(slackTrigger({ hubspot_contact_id: '' }));
  const { deps, notesCalls } = spies({ transcript: absentResult(), notes: HUBSPOT_NOTES });

  const res = await runFetchPass1Transcript(file, deps);

  assert.equal(res.exitCode, 0);
  assert.equal(notesCalls.length, 0);
});

test('existing outcome found from fathom_api — no lookup, no HubSpot, file untouched', async () => {
  const trigger = slackTrigger({
    transcript: SPEAKER_TRANSCRIPT,
    transcript_status: { outcome: 'found', custody: 'machine', source: 'fathom_api' },
  });
  const file = writeTrigger(trigger);
  const before = readFileSync(file, 'utf8');
  const { deps, transcriptCalls, notesCalls } = spies();

  const res = await runFetchPass1Transcript(file, deps);

  assert.equal(res.exitCode, 0);
  assert.equal(transcriptCalls.length, 0);
  assert.equal(notesCalls.length, 0);
  assert.equal(readFileSync(file, 'utf8'), before);
});

test('existing HubSpot summary is upgraded by a later API transcript', async () => {
  const file = writeTrigger(slackTrigger({
    transcript: `SOURCE: Fathom (via HubSpot internal notes)\n\n${HUBSPOT_NOTES}`,
    transcript_status: { outcome: 'found', custody: 'machine', source: 'hubspot_notes' },
  }));
  const { deps, transcriptCalls, notesCalls } = spies();

  const res = await runFetchPass1Transcript(file, deps);

  assert.equal(transcriptCalls.length, 1, 'a HubSpot summary must not block the API upgrade path');
  assert.equal(res.exitCode, 0);

  const after = JSON.parse(readFileSync(file, 'utf8'));
  assert.equal(after.transcript, SPEAKER_TRANSCRIPT);
  assert.equal(after.transcript_status.source, 'fathom_api');
  assert.equal(notesCalls.length, 0);
});

test('human custody — no lookup, file untouched', async () => {
  const file = writeTrigger(slackTrigger({
    transcript: 'Call the rep before writing anything.',
    transcript_status: { outcome: 'unknown', custody: 'human' },
  }));
  const before = readFileSync(file, 'utf8');
  const { deps, transcriptCalls, notesCalls } = spies();

  const res = await runFetchPass1Transcript(file, deps);

  assert.equal(res.exitCode, 0);
  assert.equal(transcriptCalls.length, 0);
  assert.equal(notesCalls.length, 0);
  assert.equal(readFileSync(file, 'utf8'), before);
});

test('SALES REP NOTE in the transcript — no lookup, file untouched', async () => {
  const file = writeTrigger(slackTrigger({
    transcript: 'No Fathom transcript available.\n\nSALES REP NOTE: they only want the intake section.',
  }));
  const before = readFileSync(file, 'utf8');
  const { deps, transcriptCalls, notesCalls } = spies();

  const res = await runFetchPass1Transcript(file, deps);

  assert.equal(res.exitCode, 0);
  assert.equal(transcriptCalls.length, 0);
  assert.equal(notesCalls.length, 0);
  assert.equal(readFileSync(file, 'utf8'), before);
});

test('default getTranscript hits api.fathom.ai with X-Api-Key and never fathom.video', async () => {
  const file = writeTrigger(slackTrigger());
  const fetches = [];
  global.fetch = async (url, opts) => {
    fetches.push({ url: String(url), opts });
    return {
      ok: true,
      status: 200,
      json: async () => ({
        items: [{
          recording_id: 'rec1',
          title: 'Discovery Call',
          created_at: '2026-09-10T15:00:00Z',
          calendar_invitees: [{ email: 'libby@indianaimmigration.com' }],
          transcript: [{ speaker: { display_name: 'Libby Martin' }, text: 'We get maybe 30 leads a month.', timestamp: '0:12' }],
        }],
        next_cursor: null,
      }),
      text: async () => '',
    };
  };

  const res = await runFetchPass1Transcript(file, { getHubSpotNotes: async () => '' });

  assert.equal(res.exitCode, 0);
  assert.equal(fetches.length, 1);
  assert.ok(fetches[0].url.startsWith('https://api.fathom.ai/external/v1/meetings?'), fetches[0].url);
  assert.ok(fetches[0].url.includes('include_transcript=true'), fetches[0].url);
  assert.equal(fetches[0].opts.headers['X-Api-Key'], 'test-key');
  assert.equal(fetches[0].opts.headers.Authorization, undefined, 'the API uses X-Api-Key, not Bearer');
  assert.ok(!fetches.some(f => f.url.includes('fathom.video')), 'fathom.video must never be called');

  const after = JSON.parse(readFileSync(file, 'utf8'));
  assert.equal(after.transcript, 'Libby Martin (0:12): We get maybe 30 leads a month.');
  assert.equal(after.transcript_status.source, 'fathom_api');
});

test('CLI with a relative script path still runs (GHA invokes it that way)', () => {
  const file = writeTrigger(slackTrigger());
  const repoRoot = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
  const res = spawnSync(process.execPath, ['scripts/fetch-pass1-transcript.mjs', file], {
    cwd: repoRoot,
    encoding: 'utf8',
    env: { ...process.env, FATHOM_API_KEY: '' },
  });
  assert.equal(res.status, 0, res.stderr);
  const after = JSON.parse(readFileSync(file, 'utf8'));
  assert.match(
    after.transcript || '',
    /FATHOM_API_KEY secret is not configured/,
    'relative-path CLI must actually run, not load-and-exit',
  );
});

test('CLI exits 2 when the trigger path is missing', () => {
  const res = spawnSync(process.execPath, [SCRIPT], { encoding: 'utf8' });
  assert.equal(res.status, 2);
  assert.match(res.stderr, /trigger/i);
});

test('CLI exits 2 when the trigger file does not exist', () => {
  const res = spawnSync(process.execPath, [SCRIPT, join(dir, 'nope.json')], { encoding: 'utf8' });
  assert.equal(res.status, 2);
});

test('unparseable trigger exits 2 and writes nothing', async () => {
  const file = join(dir, 'broken.json');
  writeFileSync(file, '{ not json');
  const { deps, transcriptCalls } = spies();

  const res = await runFetchPass1Transcript(file, deps);

  assert.equal(res.exitCode, 2);
  assert.equal(transcriptCalls.length, 0);
  assert.equal(readFileSync(file, 'utf8'), '{ not json');
});

test('HubSpot notes helper crash exits 2 after the API miss is already persisted', async () => {
  const file = writeTrigger(slackTrigger());
  const res = await runFetchPass1Transcript(file, {
    getTranscript: async () => absentResult(),
    getHubSpotNotes: async () => { throw new Error('hs down'); },
  });
  assert.equal(res.exitCode, 2);
  const after = JSON.parse(readFileSync(file, 'utf8'));
  assert.equal(after.transcript_status.outcome, 'absent');
  assert.match(after.transcript, /^No Fathom transcript found for/);
});

test('a crashing lookup helper exits 2 rather than writing a bogus miss', async () => {
  const file = writeTrigger(slackTrigger());
  const before = readFileSync(file, 'utf8');

  const res = await runFetchPass1Transcript(file, {
    getTranscript: async () => { throw new Error('boom'); },
    getHubSpotNotes: async () => '',
  });

  assert.equal(res.exitCode, 2);
  assert.equal(readFileSync(file, 'utf8'), before);
});
