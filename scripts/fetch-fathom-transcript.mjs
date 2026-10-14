#!/usr/bin/env node
/**
 * fetch-fathom-transcript.mjs
 *
 * Downloads the full verbatim transcript for the Fathom call HubSpot links to
 * and writes it to <out_file>, which must be OUTSIDE the repo (the workflows
 * use $RUNNER_TEMP). This repo and its Actions logs are public, so the
 * transcript is never written to a trigger JSON and never printed: only
 * status, match method and character count go to stderr.
 *
 * Usage:   node scripts/fetch-fathom-transcript.mjs <out_file> <fathom_url> <contact_email> [rep_email]
 * Output:  stdout "found" or "not_found"; transcript in <out_file> when found.
 * Env:     FATHOM_API_KEY
 * Exit:    always 0 — a missing transcript must not fail the pipeline; the
 *          summary in the trigger file remains the fallback.
 */
import { writeFileSync } from 'fs';
import { getFullTranscriptForCall } from './lib/fathom.mjs';

const [, , outFile, fathomUrl = '', contactEmail = '', repEmail = ''] = process.argv;
const log = msg => console.error(`fetch-fathom-transcript: ${msg}`);

if (!outFile) {
  log('missing out_file argument');
  process.stdout.write('not_found');
  process.exit(0);
}

try {
  const result = await getFullTranscriptForCall({
    fathomUrl,
    contactEmail,
    repEmail,
    apiKey: process.env.FATHOM_API_KEY,
    log,
  });
  if (result.found) {
    writeFileSync(outFile, result.text, { mode: 0o600 });
    log(`found recording ${result.recording_id} (matched by ${result.matched_by}), ${result.chars} chars`);
    process.stdout.write('found');
  } else {
    log(`no full transcript (${result.reason})`);
    process.stdout.write('not_found');
  }
} catch (err) {
  log(`error: ${err.message}`);
  process.stdout.write('not_found');
}
process.exit(0);
