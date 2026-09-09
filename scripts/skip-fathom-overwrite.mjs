#!/usr/bin/env node
/**
 * Exit 0 if trigger.transcript should be left alone (real transcript or
 * existing HubSpot summary). Exit 1 if GHA may run the HubSpot/summary fallback.
 *
 * Usage: node scripts/skip-fathom-overwrite.mjs <trigger.json>
 */
import { readFileSync } from 'fs';
import { shouldSkipFathomOverwrite } from './lib/fathom.mjs';

const file = process.argv[2];
if (!file) process.exit(1);

let transcript;
try {
  transcript = JSON.parse(readFileSync(file, 'utf8')).transcript;
} catch {
  process.exit(1);
}

process.exit(shouldSkipFathomOverwrite(transcript) ? 0 : 1);
