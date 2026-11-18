#!/usr/bin/env node
/**
 * resolve-marketing-mention.mjs
 *
 * Resolves the Slack @-mention (`<@USERID>`) for the marketing reviewer
 * (Leif), who is tagged in the proposals channel whenever a proposal
 * includes a marketing product (Full Service Marketing, Paid Ads, Web + SEO).
 * The callers decide whether marketing is in the package; this only resolves
 * the tag.
 *
 * Config: scripts/marketing-reviewer.json — { name, email, slack_id }.
 *
 * Resolution order:
 *   1. slack_id from the config, if set.
 *   2. Live Slack users.lookupByEmail on the config email, if set.
 *   3. scripts/slack-user-map.json — by_email (config email), then by_name.
 *   4. Live Slack users.list: the one active, non-bot member whose first name
 *      (or real/display name) matches the config name. Skipped if there is
 *      more than one match, so the wrong person is never tagged.
 *   5. Unresolved: the plain name with a visible warning flag.
 *
 * Usage:  node scripts/resolve-marketing-mention.mjs
 * Output: mention text on stdout.
 * Env:    SLACK_BOT_TOKEN
 */

import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CONFIG_PATH = join(__dirname, 'marketing-reviewer.json');
const MAP_PATH = join(__dirname, 'slack-user-map.json');

function readJson(path, fallback) {
  if (!existsSync(path)) return fallback;
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch (err) {
    console.error(`${path} unreadable (${err.message}) — ignoring.`);
    return fallback;
  }
}

async function slackGet(method, params) {
  const token = process.env.SLACK_BOT_TOKEN;
  if (!token) return null;
  const url = new URL(`https://slack.com/api/${method}`);
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
  try {
    const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
    const body = await res.json();
    if (!body.ok) console.error(`${method} failed (${body.error}).`);
    return body.ok ? body : null;
  } catch (err) {
    console.error(`${method} request failed (${err.message}).`);
    return null;
  }
}

async function lookupByName(name) {
  const want = name.trim().toLowerCase();
  const matches = new Set();
  let cursor = '';
  do {
    const body = await slackGet('users.list', cursor ? { limit: '200', cursor } : { limit: '200' });
    if (!body) return null;
    for (const m of body.members || []) {
      if (m.deleted || m.is_bot || m.id === 'USLACKBOT') continue;
      const p = m.profile || {};
      const names = [p.first_name, p.real_name, p.display_name, m.real_name, m.name]
        .filter(Boolean).map(s => s.trim().toLowerCase());
      if (names.some(n => n === want || n.split(/\s+/)[0] === want)) matches.add(m.id);
    }
    cursor = body.response_metadata?.next_cursor || '';
  } while (cursor);
  if (matches.size === 1) return [...matches][0];
  if (matches.size > 1) console.error(`${matches.size} Slack members match "${name}" — set slack_id in marketing-reviewer.json.`);
  return null;
}

(async () => {
  const cfg = readJson(CONFIG_PATH, {});
  const name = (cfg.name || 'Leif').trim();
  const email = (cfg.email || '').trim().toLowerCase();
  const map = readJson(MAP_PATH, {});

  let id = (cfg.slack_id || '').trim() || null;
  if (!id && email) id = (await slackGet('users.lookupByEmail', { email }))?.user?.id || null;
  if (!id && email) id = map.by_email?.[email] || null;
  if (!id) id = map.by_name?.[name] || null;
  if (!id) id = await lookupByName(name);

  if (id) {
    process.stdout.write(`<@${id}>`);
  } else {
    console.error(`Could not resolve a Slack ID for marketing reviewer "${name}".`);
    process.stdout.write(`*${name}* (⚠️ Slack tag unresolved — set slack_id in scripts/marketing-reviewer.json)`);
  }
})();
