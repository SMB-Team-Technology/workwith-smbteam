#!/usr/bin/env node
/**
 * resolve-slack-mention.mjs
 *
 * Resolves a real Slack @-mention (`<@USERID>`) for a sales rep, so proposal
 * review messages actually notify the seller instead of posting a literal
 * "@Name" string that Slack won't render as a tag.
 *
 * Resolution order:
 *   1. Live Slack users.lookupByEmail, if an email is given.
 *   2. scripts/slack-user-map.json fallback — by_email, then by_name.
 *   3. Unresolved: print the plain name with a visible warning flag, so a
 *      broken lookup is obvious in the posted message instead of silently
 *      looking like a working tag (which is what caused this to go
 *      unnoticed for so long — see git history on this file).
 *
 * Known non-person placeholders (unassigned-rep rows in trigger data) are
 * passed through as plain text with no warning — that's a data-quality gap
 * elsewhere, not a mention-resolution failure.
 *
 * Usage:  node scripts/resolve-slack-mention.mjs <sales_rep> [sales_rep_email]
 * Output: resolved mention text printed to stdout.
 * Env:    SLACK_BOT_TOKEN
 */

import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const MAP_PATH = join(__dirname, 'slack-user-map.json');

const PLACEHOLDER_NAMES = new Set([
  'sales rep',
  'fishing pond (new)',
  'smb team scheduling',
]);

const [, , salesRepArg, salesRepEmailArg] = process.argv;
const salesRep = (salesRepArg || '').trim();
const salesRepEmail = (salesRepEmailArg || '').trim();

function loadMap() {
  if (!existsSync(MAP_PATH)) return { by_email: {}, by_name: {} };
  try {
    const parsed = JSON.parse(readFileSync(MAP_PATH, 'utf8'));
    return { by_email: parsed.by_email || {}, by_name: parsed.by_name || {} };
  } catch (err) {
    console.error(`slack-user-map.json unreadable (${err.message}) — ignoring fallback map.`);
    return { by_email: {}, by_name: {} };
  }
}

async function lookupByEmail(email) {
  const token = process.env.SLACK_BOT_TOKEN;
  if (!token || !email) return null;
  try {
    const res = await fetch(
      `https://slack.com/api/users.lookupByEmail?email=${encodeURIComponent(email)}`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    const body = await res.json();
    if (body.ok) return body.user.id;
    console.error(`users.lookupByEmail failed (${body.error}) — falling back to cached map.`);
    return null;
  } catch (err) {
    console.error(`users.lookupByEmail request failed (${err.message}) — falling back to cached map.`);
    return null;
  }
}

(async () => {
  if (!salesRep) {
    process.stdout.write('');
    process.exit(0);
  }

  if (PLACEHOLDER_NAMES.has(salesRep.toLowerCase())) {
    process.stdout.write(salesRep);
    process.exit(0);
  }

  const map = loadMap();

  let userId = await lookupByEmail(salesRepEmail);

  if (!userId && salesRepEmail) {
    userId = map.by_email[salesRepEmail.toLowerCase()] || null;
    if (userId) console.error(`Resolved ${salesRepEmail} via slack-user-map.json (by_email).`);
  }

  if (!userId) {
    userId = map.by_name[salesRep] || null;
    if (userId) console.error(`Resolved "${salesRep}" via slack-user-map.json (by_name).`);
  }

  if (userId) {
    process.stdout.write(`<@${userId}>`);
    process.exit(0);
  }

  console.error(`Could not resolve a Slack ID for "${salesRep}" <${salesRepEmail || 'no email'}> — posting a visibly-flagged plain-text mention.`);
  process.stdout.write(`*${salesRep}* (⚠️ Slack tag unresolved — check sales_rep_email)`);
  process.exit(0);
})();
