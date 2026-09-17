#!/usr/bin/env node
/**
 * fetch-pass1-transcript.mjs — the single Fathom call in Pass 1.
 *
 * Used by the "Fetch Fathom transcript" step in audit-pipeline.yml and
 * rerun-research.yml. It ALWAYS attempts the documented Fathom external API
 * (api.fathom.ai, X-Api-Key) via getFathomTranscriptResult — including for
 * Slack-created triggers, whose transcript field starts out empty and which
 * previously skipped the lookup entirely because no fathom.video URL resolved.
 *
 * HubSpot's Fathom AI meeting notes are a fallback only: they run after the API
 * failed to return outcome "found" from source "fathom_api". A HubSpot summary
 * already on the trigger does not block the lookup — mergeTrigger upgrades it
 * when a later API result is found.
 *
 * Usage: node scripts/fetch-pass1-transcript.mjs <trigger.json>
 * Env:   FATHOM_API_KEY, HUBSPOT_TOKEN (optional, fallback only)
 *
 * Exit 0 — transcript written, or nothing to do (skip / lookup miss). A missed
 *          transcript must never fail the pipeline.
 * Exit 2 — could not evaluate: missing path, unreadable/unparseable trigger,
 *          failed write, or a helper crash.
 */

import { readFileSync } from 'fs';
import { spawnSync } from 'child_process';
import { dirname, join, resolve } from 'path';
import { fileURLToPath, pathToFileURL } from 'url';
import {
  getFathomTranscriptResult,
  mergeTrigger,
  writeTriggerAtomic,
} from './lib/fathom.mjs';

const HUBSPOT_NOTES_SCRIPT = join(dirname(fileURLToPath(import.meta.url)), 'fetch-hubspot-fathom-notes.mjs');
const HUBSPOT_PREFIX = 'SOURCE: Fathom (via HubSpot internal notes)\n\n';

/** Same rule as fathom.mjs: explicit human custody, or rep notes in the field. */
function isHumanCustody(trigger) {
  if (trigger?.transcript_status?.custody === 'human') return true;
  return typeof trigger?.transcript === 'string' && /\bSALES REP NOTE\b/i.test(trigger.transcript);
}

function isApiFound(trigger) {
  const st = trigger?.transcript_status;
  return st?.outcome === 'found' && st?.source === 'fathom_api';
}

function defaultGetHubSpotNotes(contactId) {
  const res = spawnSync(process.execPath, [HUBSPOT_NOTES_SCRIPT, String(contactId)], {
    encoding: 'utf8',
    maxBuffer: 10 * 1024 * 1024,
  });
  if (res.error) throw res.error;
  if (res.stderr) process.stderr.write(res.stderr);
  // The notes script exits 0 for "queried, nothing found". Any other
  // status is a spawn/runtime failure, not a content miss.
  if (res.status !== 0) {
    throw new Error(`fetch-hubspot-fathom-notes.mjs exited ${res.status}`);
  }
  return (res.stdout || '').trim();
}

/**
 * @returns {Promise<{exitCode: number, action: string}>}
 */
export async function runFetchPass1Transcript(triggerPath, deps = {}) {
  const getTranscript = deps.getTranscript || getFathomTranscriptResult;
  const getHubSpotNotes = deps.getHubSpotNotes || defaultGetHubSpotNotes;

  if (!triggerPath) {
    console.error('fetch-pass1-transcript: missing trigger path');
    return { exitCode: 2, action: 'error' };
  }

  let trigger;
  try {
    trigger = JSON.parse(readFileSync(triggerPath, 'utf8'));
  } catch (err) {
    console.error(`fetch-pass1-transcript: cannot read trigger ${triggerPath}: ${err.message}`);
    return { exitCode: 2, action: 'error' };
  }

  if (isHumanCustody(trigger)) {
    console.log('Trigger is under human custody (rep notes) — leaving transcript unchanged.');
    return { exitCode: 0, action: 'skip_human' };
  }

  if (isApiFound(trigger)) {
    console.log('Trigger already carries a Fathom API transcript — nothing to fetch.');
    return { exitCode: 0, action: 'skip_api_found' };
  }

  const email = trigger.contact_email || trigger.email || '';
  const contactName = trigger.contact_name || trigger.firm_name || 'contact';

  let lookup;
  try {
    lookup = await getTranscript(email, contactName, process.env.FATHOM_API_KEY);
  } catch (err) {
    console.error(`fetch-pass1-transcript: Fathom lookup crashed: ${err.message}`);
    return { exitCode: 2, action: 'error' };
  }

  let merged;
  try {
    merged = mergeTrigger(trigger, {}, lookup);
    writeTriggerAtomic(triggerPath, merged);
  } catch (err) {
    console.error(`fetch-pass1-transcript: cannot write trigger ${triggerPath}: ${err.message}`);
    return { exitCode: 2, action: 'error' };
  }

  if (isApiFound(merged)) {
    console.log(`Fathom API transcript written to ${triggerPath} (${(merged.transcript || '').length} chars).`);
    return { exitCode: 0, action: 'api_found' };
  }

  const contactId = trigger.hubspot_contact_id;
  if (!contactId) {
    console.log(`No Fathom API transcript (outcome ${merged.transcript_status?.outcome}) and no hubspot_contact_id — nothing more to try.`);
    return { exitCode: 0, action: 'lookup_miss' };
  }

  let notes;
  try {
    notes = await getHubSpotNotes(String(contactId));
  } catch (err) {
    console.error(`fetch-pass1-transcript: HubSpot notes lookup crashed: ${err.message}`);
    return { exitCode: 2, action: 'error' };
  }

  if (!notes || !notes.trim()) {
    console.log(`No Fathom content in HubSpot internal notes for contact ${contactId} — leaving the lookup result in place.`);
    return { exitCode: 0, action: 'lookup_miss' };
  }

  try {
    const withNotes = mergeTrigger(merged, {}, {
      text: HUBSPOT_PREFIX + notes,
      status: { outcome: 'found', custody: 'machine', source: 'hubspot_notes' },
    });
    writeTriggerAtomic(triggerPath, withNotes);
    console.log(`HubSpot Fathom notes written to ${triggerPath} (${notes.length} chars).`);
  } catch (err) {
    console.error(`fetch-pass1-transcript: cannot write HubSpot fallback to ${triggerPath}: ${err.message}`);
    return { exitCode: 2, action: 'error' };
  }

  return { exitCode: 0, action: 'hubspot_notes' };
}

// GHA runs `node scripts/fetch-pass1-transcript.mjs` (relative). argv[1] may
// be relative or absolute depending on the Node; compare resolved file URLs.
function invokedAsCli() {
  if (!process.argv[1]) return false;
  return import.meta.url === pathToFileURL(resolve(process.argv[1])).href;
}

if (invokedAsCli()) {
  const { exitCode } = await runFetchPass1Transcript(process.argv[2]);
  process.exit(exitCode);
}
