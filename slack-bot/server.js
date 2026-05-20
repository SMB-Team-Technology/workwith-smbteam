'use strict';
const crypto  = require('crypto');
const express = require('express');

const app  = express();
const PORT = process.env.PORT || 8080;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function verifySlackSignature(secret, rawBody, timestamp, slackSig) {
  if (!timestamp || !slackSig) return false;
  if (Math.abs(Date.now() / 1000 - Number(timestamp)) > 300) return false;
  const computed = 'v0=' + crypto
    .createHmac('sha256', secret)
    .update(`v0:${timestamp}:${rawBody}`)
    .digest('hex');
  try {
    return crypto.timingSafeEqual(Buffer.from(computed), Buffer.from(slackSig));
  } catch {
    return false;
  }
}

async function slackPost(token, channel, text, thread_ts) {
  await fetch('https://slack.com/api/chat.postMessage', {
    method:  'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body:    JSON.stringify({ channel, text, ...(thread_ts ? { thread_ts } : {}) }),
  });
}

async function githubDispatch(pat, repo, instruction, slackChannel, slackTs) {
  const res = await fetch(`https://api.github.com/repos/${repo}/dispatches`, {
    method:  'POST',
    headers: {
      Authorization:  `Bearer ${pat}`,
      Accept:         'application/vnd.github.v3+json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      event_type:     'slack-change-request',
      client_payload: { instruction, slack_channel: slackChannel, slack_thread_ts: slackTs },
    }),
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`GitHub dispatch failed ${res.status}: ${body}`);
  }
}

// ---------------------------------------------------------------------------
// Routes
// ---------------------------------------------------------------------------

// express.raw() gives us the unmodified body Buffer — required for Slack
// signature verification (any JSON parsing would mutate the raw bytes).
app.post('/api/slack', express.raw({ type: '*/*' }), async (req, res) => {
  // Ignore Slack retries — the first delivery already dispatched the workflow
  if (req.headers['x-slack-retry-num']) return res.status(200).json({ ok: true });

  const rawBody = req.body.toString();

  if (!verifySlackSignature(
    process.env.SLACK_SIGNING_SECRET,
    rawBody,
    req.headers['x-slack-request-timestamp'],
    req.headers['x-slack-signature'],
  )) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  const payload = JSON.parse(rawBody);

  // Slack URL verification handshake (one-time, when you save the Event URL)
  if (payload.type === 'url_verification') {
    return res.status(200).json({ challenge: payload.challenge });
  }

  const event = payload.event;

  // Only handle plain user messages in the designated channel
  if (
    !event ||
    event.type    !== 'message' ||
    event.subtype ||              // ignore edits, joins, bot_message subtypes
    event.bot_id  ||              // ignore messages posted by bots (including ourselves)
    event.channel !== process.env.SLACK_CHANNEL_ID
  ) {
    return res.status(200).json({ ok: true });
  }

  const token = process.env.SLACK_BOT_TOKEN;
  const pat   = process.env.GITHUB_PAT;
  const repo  = process.env.GITHUB_REPO || 'SMB-Team-Technology/workwith-smbteam';

  // Acknowledge in-thread before dispatching so the user sees an immediate reply
  await slackPost(token, event.channel, `Got it — making that change now. I'll reply here when it's done.`, event.ts);
  await githubDispatch(pat, repo, event.text, event.channel, event.ts);

  return res.status(200).json({ ok: true });
});

// Health check — Cloud Run probes this to confirm the container is up
app.get('/health', (_req, res) => res.status(200).send('ok'));

app.listen(PORT, () => console.log(`SMB Audit Slack Bot listening on port ${PORT}`));
