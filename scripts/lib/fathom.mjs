/**
 * fathom.mjs — shared Fathom transcript fetch.
 *
 * Uses the documented Fathom external API (https://developers.fathom.ai):
 *   GET https://api.fathom.ai/external/v1/meetings
 *   Header: X-Api-Key
 *   include_transcript=true → transcript: [{ speaker: { display_name }, text, timestamp }]
 *
 * The API filters by company domain (calendar_invitees_domains[]), not by
 * individual invitee email — we filter by the contact's email domain when it's
 * a custom domain, then match the exact invitee client-side. Free-mail
 * contacts (gmail etc.) fall back to a recent-meetings scan + client match.
 *
 * Call signature matches the schedulers on main:
 *   getFathomTranscript(email, contactName, apiKey, fathomUrl?)
 * fathomUrl is accepted for compat and ignored — discovery is by invitee email,
 * not by the fathom.video URL. The previous implementation called
 * fathom.video/api/v1/calls (list and /summary) — that host is not the API.
 *
 * Lookup status lives on trigger.transcript_status (outcome × custody).
 * getFathomTranscript() returns only .text for older call sites.
 * mergeTrigger() is the scheduler persist rule: never wholesale-replace.
 *
 * shouldSkipFathomOverwrite() is the GHA guard: if the trigger already has a
 * real transcript (or an existing HubSpot summary), the workflow must not
 * overwrite it with an 8k fathom.video summary.
 */

import { writeFileSync, renameSync, unlinkSync } from 'fs';

const FREE_MAIL = new Set(['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'aol.com', 'icloud.com', 'me.com', 'msn.com', 'live.com', 'protonmail.com']);
const FATHOM_LOOKBACK_DAYS = 90;
const TRANSCRIPT_MAX_CHARS = 300_000; // ~60-90 min call with headroom; keeps trigger JSONs sane
const MAX_PAGES = 5;
const FETCH_TIMEOUT_MS = 15_000; // a hung connection must not hang the scheduled run

// Leading generated-miss sentences (no $). Leftover after a match is protected
// content (sales-rep notes). Unmatched miss-family strings (legacy "No Fathom
// transcript available.") still allow HubSpot fallback.
const GENERATED_MISS_HEAD = [
  /^No transcript available\. FATHOM_API_KEY secret is not configured\./,
  /^No Fathom transcript lookup possible — contact has no email on file\./,
  /^No Fathom transcript available \(API returned \d+ for [^)]+\)\./,
  /^No Fathom transcript available \(lookup error: [^)]+\)\./,
  /^No Fathom transcript found for .+? \([^)]+\)\./,
  /^Fathom meeting found \("[^"]*"\) but transcript was empty — flag for the rep\./,
  /^No Fathom transcript available — fathom_url not set\. Use the \/trigger command\./,
  /^Fathom call \d+ found but summary is unavailable\./,
  /^Fathom lookup incomplete for .+? \([^)]+\) — .+\. This is not a confirmed absence\./,
];
const MISS_FAMILY = /^(No transcript available|No Fathom transcript|Fathom meeting found \(|Fathom call \d+ found but|Fathom lookup incomplete for)/;
// Bare openers used in older triggers: "No Fathom transcript available." plus notes.
const BARE_MISS_HEAD = /^(No Fathom transcript available|No transcript available(?: yet)?)\./;

function sniffSkip(transcript) {
  if (typeof transcript !== 'string') return false;
  const t = transcript.trim();
  if (!t) return false;
  for (const re of GENERATED_MISS_HEAD) {
    const m = t.match(re);
    if (m && m.index === 0) {
      const rest = t.slice(m[0].length).trim();
      if (!rest) return false;
      if (/\bSALES REP NOTE\b/i.test(rest)) return true;
      if (MISS_FAMILY.test(rest) || /^No recordings found\b/i.test(rest)) return false;
      return true;
    }
  }
  const bare = t.match(BARE_MISS_HEAD);
  if (bare && bare.index === 0) {
    const rest = t.slice(bare[0].length).trim();
    if (!rest) return false;
    if (/\bSALES REP NOTE\b/i.test(rest)) return true;
    if (MISS_FAMILY.test(rest) || /^No recordings found\b/i.test(rest)) return false;
    return true;
  }
  // Em-dash miss heads ("available — proposal call scheduled") fall through
  // GENERATED/BARE. A closer note on that string must still be protected.
  if (MISS_FAMILY.test(t) && /\bSALES REP NOTE\b/i.test(t)) return true;
  if (MISS_FAMILY.test(t)) return false;
  return true;
}

/**
 * True when GHA should leave trigger.transcript alone.
 * Accepts the transcript string (legacy) or the parsed trigger object.
 * When transcript_status is present: human custody, outcome found, or a
 * miss/incomplete string with leftover closer notes → skip. Unknown/absent
 * miss-only still allows HubSpot. Unrecognized prose with unknown status
 * does not skip (that would block fallback).
 */
export function shouldSkipFathomOverwrite(transcriptOrTrigger) {
  if (transcriptOrTrigger && typeof transcriptOrTrigger === 'object' && !Array.isArray(transcriptOrTrigger)) {
    const st = transcriptOrTrigger.transcript_status;
    if (st && typeof st === 'object') {
      if (isHumanTrigger(transcriptOrTrigger)) return true;
      if (st.outcome === 'found') return true;
      const t = transcriptOrTrigger.transcript;
      if (typeof t === 'string' && MISS_FAMILY.test(t.trim()) && sniffSkip(t)) return true;
      return false;
    }
    return sniffSkip(transcriptOrTrigger.transcript);
  }
  return sniffSkip(transcriptOrTrigger);
}

function lookupStatus(partial) {
  return {
    custody: 'machine',
    source: 'fathom_api',
    checked_at: new Date().toISOString(),
    pages_fetched: 0,
    pages_remaining: false,
    ...partial,
  };
}

function incompleteText(contactName, email, detail) {
  return `Fathom lookup incomplete for ${contactName} (${email}) — ${detail}. This is not a confirmed absence.`;
}

function isHumanTrigger(existing) {
  if (existing?.transcript_status?.custody === 'human') return true;
  return typeof existing?.transcript === 'string' && /\bSALES REP NOTE\b/i.test(existing.transcript);
}

function isFoundPayload(existing) {
  if (existing?.transcript_status?.outcome === 'found') return true;
  const t = existing?.transcript;
  if (typeof t !== 'string') return false;
  const trimmed = t.trim();
  if (!trimmed) return false;
  if (MISS_FAMILY.test(trimmed)) return false;
  return sniffSkip(trimmed);
}

/**
 * Read-merge-write contract for trigger JSON.
 * freshFields must not include transcript / transcript_status — those come
 * from lookupResult. Existing found payloads and human notes are kept.
 */
export function mergeTrigger(existing, freshFields, lookupResult) {
  const text = lookupResult?.text ?? '';
  const status = { ...(lookupResult?.status || {}) };
  if (!status.checked_at) status.checked_at = new Date().toISOString();
  const fields = freshFields && typeof freshFields === 'object' ? freshFields : {};

  if (!existing || typeof existing !== 'object') {
    return {
      ...fields,
      transcript: text,
      transcript_status: { ...status, custody: 'machine' },
    };
  }

  const merged = { ...existing, ...fields };
  const human = isHumanTrigger(existing);
  const found = isFoundPayload(existing);

  const sniffProtected = typeof existing.transcript === 'string' && sniffSkip(existing.transcript);
  if (human || (sniffProtected && !found)) {
    merged.transcript = existing.transcript;
    const prior = existing.transcript_status && typeof existing.transcript_status === 'object'
      ? existing.transcript_status
      : {};
    const keptOutcome = (prior.outcome === 'absent' || prior.outcome === 'unknown' || prior.outcome === 'found_empty')
      ? prior.outcome
      : 'unknown';
    merged.transcript_status = {
      ...prior,
      outcome: keptOutcome,
      custody: 'human',
      last_attempt_at: status.checked_at,
      last_attempt_outcome: status.outcome,
    };
    return merged;
  }

  if (found) {
    const looksLikeSummary = typeof existing.transcript === 'string'
      && existing.transcript.startsWith('SOURCE: Fathom');
    const canUpgrade = status.outcome === 'found'
      && status.source === 'fathom_api'
      && looksLikeSummary;
    if (canUpgrade) {
      merged.transcript = text;
      merged.transcript_status = { ...status, custody: 'machine' };
      return merged;
    }
    merged.transcript = existing.transcript;
    const prior = existing.transcript_status && typeof existing.transcript_status === 'object'
      ? existing.transcript_status
      : { outcome: 'found', source: 'fathom_api' };
    merged.transcript_status = {
      ...prior,
      outcome: 'found',
      custody: prior.custody || 'machine',
      last_attempt_at: status.checked_at,
      last_attempt_outcome: status.outcome,
    };
    return merged;
  }

  merged.transcript = text;
  merged.transcript_status = { ...status, custody: 'machine' };
  return merged;
}

export function writeTriggerAtomic(filePath, data) {
  const tmp = `${filePath}.tmp`;
  try {
    writeFileSync(tmp, JSON.stringify(data, null, 2));
    renameSync(tmp, filePath);
  } catch (err) {
    try { unlinkSync(tmp); } catch (_) { /* tmp may not exist */ }
    throw err;
  }
}

export async function getFathomTranscriptResult(email, contactName, apiKey, _fathomUrl) {
  if (!apiKey) {
    console.warn('  FATHOM_API_KEY not set — skipping transcript lookup.');
    return {
      text: 'No transcript available. FATHOM_API_KEY secret is not configured.',
      status: lookupStatus({ outcome: 'unknown', reason: 'not_started', detail: 'missing_api_key' }),
    };
  }
  if (!email) {
    return {
      text: 'No Fathom transcript lookup possible — contact has no email on file.',
      status: lookupStatus({ outcome: 'unknown', reason: 'not_started', detail: 'missing_email' }),
    };
  }

  const domain = email.split('@')[1]?.toLowerCase() || '';
  const createdAfter = new Date(Date.now() - FATHOM_LOOKBACK_DAYS * 24 * 60 * 60 * 1000).toISOString();

  const params = new URLSearchParams({ include_transcript: 'true', created_after: createdAfter });
  if (domain && !FREE_MAIL.has(domain)) params.append('calendar_invitees_domains[]', domain);

  const meetings = [];
  let cursor = null;
  let aborted = false;
  let abortReason = null;
  let abortDetail = null;
  let pagesFetched = 0;
  try {
    for (let page = 0; page < MAX_PAGES; page++) {
      const url = `https://api.fathom.ai/external/v1/meetings?${params}${cursor ? `&cursor=${encodeURIComponent(cursor)}` : ''}`;
      const res = await fetch(url, {
        headers: { 'X-Api-Key': apiKey, 'Accept': 'application/json' },
        signal: AbortSignal.timeout(FETCH_TIMEOUT_MS),
      });
      if (!res.ok) {
        console.warn(`  Fathom lookup failed (${res.status}) for ${email}: ${(await res.text()).slice(0, 200)}`);
        if (meetings.length > 0) {
          aborted = true;
          abortReason = 'http_error';
          abortDetail = `${res.status} on page ${page + 1}`;
          break;
        }
        const detail = `HTTP ${res.status} on page ${page + 1}`;
        return {
          text: incompleteText(contactName, email, detail),
          status: lookupStatus({
            outcome: 'unknown',
            reason: 'http_error',
            detail,
            http_status: res.status,
            pages_fetched: page + 1,
          }),
        };
      }
      const data = await res.json();
      if (!Array.isArray(data.items)) {
        if (meetings.length > 0) {
          aborted = true;
          abortReason = 'protocol_error';
          abortDetail = 'malformed items on a later page';
          break;
        }
        return {
          text: incompleteText(contactName, email, 'malformed list response'),
          status: lookupStatus({
            outcome: 'unknown',
            reason: 'protocol_error',
            detail: 'items is not an array',
            pages_fetched: page + 1,
          }),
        };
      }
      meetings.push(...data.items);
      cursor = data.next_cursor || null;
      pagesFetched = page + 1;
      if (!cursor) break;
    }
  } catch (err) {
    console.warn(`  Fathom lookup error for ${email}: ${err.message}`);
    if (meetings.length === 0) {
      const detail = `lookup error: ${err.message}`;
      return {
        text: incompleteText(contactName, email, detail),
        status: lookupStatus({
          outcome: 'unknown',
          reason: 'network_error',
          detail,
          pages_fetched: pagesFetched,
        }),
      };
    }
    aborted = true;
    abortReason = 'network_error';
    abortDetail = err.message;
  }

  const capHit = !!(cursor && !aborted);

  const mine = meetings
    .filter(m => (m.calendar_invitees || []).some(i =>
      (i.email || i.email_address || '').toLowerCase() === email.toLowerCase()))
    .sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));

  if (!mine.length) {
    if (aborted || capHit) {
      const why = aborted ? (abortDetail || abortReason) : `pagination cap hit (${MAX_PAGES} pages)`;
      console.warn(`  Fathom scan incomplete (${why}) for ${email} — a no-transcript result is not a confirmed absence.`);
      const detail = capHit
        ? `pagination cap after ${pagesFetched} pages`
        : (abortDetail || 'scan stopped early');
      return {
        text: incompleteText(contactName, email, detail),
        status: lookupStatus({
          outcome: 'unknown',
          reason: capHit ? 'page_cap' : (abortReason || 'incomplete'),
          detail,
          pages_fetched: pagesFetched,
          pages_remaining: !!cursor,
        }),
      };
    }
    if (meetings.length > 0) {
      const detail = `no exact invitee match after ${pagesFetched} page(s)`;
      console.warn(`  Fathom listed ${meetings.length} meeting(s) for ${email} but none matched the invitee — not a confirmed absence.`);
      return {
        text: incompleteText(contactName, email, detail),
        status: lookupStatus({
          outcome: 'unknown',
          reason: 'no_invitee_match',
          detail,
          pages_fetched: pagesFetched,
          pages_remaining: false,
        }),
      };
    }
    console.log(`  No Fathom meetings found for ${email} in last ${FATHOM_LOOKBACK_DAYS} days.`);
    return {
      text: `No Fathom transcript found for ${contactName} (${email}).`,
      status: lookupStatus({
        outcome: 'absent',
        reason: 'exhausted',
        pages_fetched: pagesFetched,
        pages_remaining: false,
      }),
    };
  }

  const latest = mine[0];
  const lines = (latest.transcript || []).map(seg => {
    const speaker = seg.speaker?.display_name || 'Speaker';
    const ts = seg.timestamp ? ` (${seg.timestamp})` : '';
    return `${speaker}${ts}: ${seg.text || ''}`;
  });

  if (!lines.length) {
    console.warn(`  Fathom meeting "${latest.title || latest.recording_id}" found but transcript empty.`);
    return {
      text: `Fathom meeting found ("${latest.title || 'untitled'}") but transcript was empty — flag for the rep.`,
      status: lookupStatus({
        outcome: 'found_empty',
        reason: 'empty_transcript',
        pages_fetched: pagesFetched,
        pages_remaining: !!cursor,
      }),
    };
  }

  const transcript = lines.join('\n');
  console.log(`  Found Fathom transcript: "${latest.title || latest.recording_id}" (${latest.created_at || ''}) — ${lines.length} segments, ${transcript.length} chars.`);
  const text = transcript.length > TRANSCRIPT_MAX_CHARS
    ? transcript.slice(0, TRANSCRIPT_MAX_CHARS) + '\n[TRANSCRIPT TRUNCATED AT 300K CHARS]'
    : transcript;
  return {
    text,
    status: lookupStatus({
      outcome: 'found',
      reason: aborted ? (abortReason || 'matched') : (capHit ? 'page_cap' : 'matched'),
      pages_fetched: pagesFetched,
      pages_remaining: !!cursor,
    }),
  };
}

export async function getFathomTranscript(email, contactName, apiKey, _fathomUrl) {
  const result = await getFathomTranscriptResult(email, contactName, apiKey, _fathomUrl);
  return result.text;
}
