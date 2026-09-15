#!/usr/bin/env node
/**
 * Exit 0 — leave trigger.transcript alone (found payload, human custody, or notes).
 * Exit 1 — fallback-eligible (absent / unknown / found_empty / legacy miss).
 * Exit 2 — helper could not evaluate (missing path, import, I/O, parse);
 *          GHA must leave the field unchanged, not treat this as a miss.
 * Prefers trigger.transcript_status when present; otherwise sniffs .transcript.
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

let trigger;
try {
  trigger = JSON.parse(readFileSync(file, 'utf8'));
} catch (err) {
  console.error(`skip-fathom-overwrite: ${err.message}`);
  process.exit(2);
}

try {
  process.exit(shouldSkipFathomOverwrite(trigger) ? 0 : 1);
} catch (err) {
  console.error(`skip-fathom-overwrite: ${err.message}`);
  process.exit(2);
}
