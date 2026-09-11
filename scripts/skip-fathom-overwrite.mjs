#!/usr/bin/env node
/**
 * Exit 0 — leave trigger.transcript alone (real transcript or notes).
 * Exit 1 — confirmed miss placeholder; GHA may run HubSpot/summary fallback.
 * Exit 2 — helper could not evaluate (missing path, import, I/O, parse);
 *          GHA must leave the field unchanged, not treat this as a miss.
 *
 * Usage: node scripts/skip-fathom-overwrite.mjs <trigger.json>
 */
import { readFileSync } from 'fs';

const file = process.argv[2];
if (!file) {
  console.error('skip-fathom-overwrite: missing trigger path');
  process.exit(2);
}

let shouldSkipFathomOverwrite;
try {
  ({ shouldSkipFathomOverwrite } = await import('./lib/fathom.mjs'));
} catch (err) {
  console.error(`skip-fathom-overwrite: ${err.message}`);
  process.exit(2);
}

let transcript;
try {
  transcript = JSON.parse(readFileSync(file, 'utf8')).transcript;
} catch (err) {
  console.error(`skip-fathom-overwrite: ${err.message}`);
  process.exit(2);
}

process.exit(shouldSkipFathomOverwrite(transcript) ? 0 : 1);
