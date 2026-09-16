#!/usr/bin/env node
/**
 * build-slack-user-map.mjs
 *
 * One-time (and re-runnable) bootstrap for scripts/slack-user-map.json, the
 * fallback rep -> Slack user ID map used by resolve-slack-mention.mjs when a
 * live users.lookupByEmail call can't resolve someone (blank/wrong
 * sales_rep_email in trigger data, a transient API issue, etc). This is a
 * fallback, not a live sync — re-run it by hand whenever a new sales rep
 * joins, or add a one-off scripts/slack-user-map.json entry directly.
 *
 * Requires the Slack bot token to carry both users:read and
 * users:read.email (the same scopes users.lookupByEmail needs).
 *
 * Run manually, not from a workflow:
 *   SLACK_BOT_TOKEN=xoxb-... node scripts/build-slack-user-map.mjs
 *
 * Writes scripts/slack-user-map.json: by_email is populated automatically
 * from every non-bot, non-deleted @smbteam.com workspace member. by_name
 * entries (for a rep whose company email convention doesn't match their
 * real Slack account email) are preserved across re-runs — add those by
 * hand.
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const MAP_PATH = join(__dirname, 'slack-user-map.json');

const token = process.env.SLACK_BOT_TOKEN;
if (!token) {
  console.error('SLACK_BOT_TOKEN is required.');
  process.exit(1);
}

async function fetchAllMembers() {
  const members = [];
  let cursor = '';
  do {
    const url = new URL('https://slack.com/api/users.list');
    url.searchParams.set('limit', '200');
    if (cursor) url.searchParams.set('cursor', cursor);
    const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
    const body = await res.json();
    if (!body.ok) {
      throw new Error(`users.list failed: ${body.error}`);
    }
    members.push(...body.members);
    cursor = body.response_metadata?.next_cursor || '';
  } while (cursor);
  return members;
}

(async () => {
  const existing = existsSync(MAP_PATH)
    ? JSON.parse(readFileSync(MAP_PATH, 'utf8'))
    : { by_email: {}, by_name: {} };

  const members = await fetchAllMembers();

  const by_email = {};
  for (const member of members) {
    if (member.deleted || member.is_bot || member.id === 'USLACKBOT') continue;
    const email = member.profile?.email;
    if (email && email.toLowerCase().endsWith('@smbteam.com')) {
      by_email[email.toLowerCase()] = member.id;
    }
  }

  const map = { by_email, by_name: existing.by_name || {} };
  writeFileSync(MAP_PATH, JSON.stringify(map, null, 2) + '\n');
  console.error(`Wrote ${Object.keys(by_email).length} by_email entries (kept ${Object.keys(map.by_name).length} existing by_name entries) to ${MAP_PATH}.`);
})().catch(err => {
  console.error(`build-slack-user-map error: ${err.message}`);
  process.exit(1);
});
