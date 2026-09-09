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
 * shouldSkipFathomOverwrite() is the GHA guard: if the trigger already has a
 * real transcript (or an existing HubSpot summary), the workflow must not
 * overwrite it with an 8k fathom.video summary.
 */

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
];
const MISS_FAMILY = /^(No transcript available|No Fathom transcript|Fathom meeting found \(|Fathom call \d+ found but)/;
// Bare openers used in older triggers: "No Fathom transcript available." plus notes.
const BARE_MISS_HEAD = /^(No Fathom transcript available|No transcript available(?: yet)?)\./;

/**
 * True when GHA should leave trigger.transcript alone.
 * False (run HubSpot/summary fallback) for empty values, exact generated
 * misses, and legacy miss-only lines. A miss sentence plus leftover notes
 * is treated as real content, including "No Fathom transcript available.
 * SALES REP NOTE: ...".
 */
export function shouldSkipFathomOverwrite(transcript) {
  if (typeof transcript !== 'string') return false;
  const t = transcript.trim();
  if (!t) return false;
  for (const re of GENERATED_MISS_HEAD) {
    const m = t.match(re);
    if (m && m.index === 0) return t.slice(m[0].length).trim().length > 0;
  }
  const bare = t.match(BARE_MISS_HEAD);
  if (bare && bare.index === 0) {
    const rest = t.slice(bare[0].length).trim();
    if (!rest) return false;
    if (/\bSALES REP NOTE\b/i.test(rest)) return true;
    if (MISS_FAMILY.test(rest) || /^No recordings found\b/i.test(rest)) return false;
    return true;
  }
  if (MISS_FAMILY.test(t)) return false;
  return true;
}

export async function getFathomTranscript(email, contactName, apiKey, _fathomUrl) {
  if (!apiKey) {
    console.warn('  FATHOM_API_KEY not set — skipping transcript lookup.');
    return 'No transcript available. FATHOM_API_KEY secret is not configured.';
  }
  if (!email) {
    return 'No Fathom transcript lookup possible — contact has no email on file.';
  }

  const domain = email.split('@')[1]?.toLowerCase() || '';
  const createdAfter = new Date(Date.now() - FATHOM_LOOKBACK_DAYS * 24 * 60 * 60 * 1000).toISOString();

  const params = new URLSearchParams({ include_transcript: 'true', created_after: createdAfter });
  if (domain && !FREE_MAIL.has(domain)) params.append('calendar_invitees_domains[]', domain);

  const meetings = [];
  let cursor = null;
  let aborted = false;
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
          break;
        }
        return `No Fathom transcript available (API returned ${res.status} for ${email}).`;
      }
      const data = await res.json();
      meetings.push(...(data.items || []));
      cursor = data.next_cursor || null;
      if (!cursor) break;
    }
  } catch (err) {
    console.warn(`  Fathom lookup error for ${email}: ${err.message}`);
    if (meetings.length === 0) {
      return `No Fathom transcript available (lookup error: ${err.message}).`;
    }
    aborted = true;
  }
  if (cursor && !aborted) {
    console.warn(`  Fathom pagination cap hit (${MAX_PAGES} pages) for ${email} — scan incomplete; a no-transcript result may be a false negative.`);
  }

  const mine = meetings
    .filter(m => (m.calendar_invitees || []).some(i =>
      (i.email || i.email_address || '').toLowerCase() === email.toLowerCase()))
    .sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));

  if (!mine.length) {
    console.log(`  No Fathom meetings found for ${email} in last ${FATHOM_LOOKBACK_DAYS} days.`);
    return `No Fathom transcript found for ${contactName} (${email}).`;
  }

  const latest = mine[0];
  const lines = (latest.transcript || []).map(seg => {
    const speaker = seg.speaker?.display_name || 'Speaker';
    const ts = seg.timestamp ? ` (${seg.timestamp})` : '';
    return `${speaker}${ts}: ${seg.text || ''}`;
  });

  if (!lines.length) {
    console.warn(`  Fathom meeting "${latest.title || latest.recording_id}" found but transcript empty.`);
    return `Fathom meeting found ("${latest.title || 'untitled'}") but transcript was empty — flag for the rep.`;
  }

  const transcript = lines.join('\n');
  console.log(`  Found Fathom transcript: "${latest.title || latest.recording_id}" (${latest.created_at || ''}) — ${lines.length} segments, ${transcript.length} chars.`);
  return transcript.length > TRANSCRIPT_MAX_CHARS
    ? transcript.slice(0, TRANSCRIPT_MAX_CHARS) + '\n[TRANSCRIPT TRUNCATED AT 300K CHARS]'
    : transcript;
}
