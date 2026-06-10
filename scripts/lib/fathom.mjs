/**
 * fathom.mjs — shared Fathom transcript lookup utility
 *
 * Lookup hierarchy:
 *   1. Direct call ID — if a fathom_url or fathom_call_id is provided, fetch
 *      that specific call directly. Most reliable; bypasses all search issues.
 *   2. List + filter — list recent calls from GET /api/v1/calls and match
 *      client-side by email/name. Fallback when no direct ID is available.
 *      NOTE: The Fathom REST API list endpoint behavior is not fully documented;
 *      if it returns 404 the lookup is skipped gracefully.
 */

const FATHOM_BASE = 'https://fathom.video/api/v1';
const LOOKBACK_DAYS = 90;
const MAX_SUMMARY_CHARS = 8000;

/**
 * Extract a numeric call ID from a Fathom URL.
 * Handles https://fathom.video/calls/704816497 → "704816497"
 */
function extractCallId(url) {
  if (!url) return null;
  const m = String(url).match(/\/calls\/(\d+)/);
  return m ? m[1] : null;
}

/**
 * Fetch the summary text for a single call by its ID. Returns null on failure.
 */
async function fetchCallSummary(callId, headers) {
  const res = await fetch(`${FATHOM_BASE}/calls/${callId}/summary`, { headers });
  if (!res.ok) {
    console.warn(`  Fathom summary fetch failed for call ${callId}: ${res.status}`);
    return null;
  }
  const data = await res.json();
  return data.summary || data.text || data.content || null;
}

/**
 * Returns true if a call's metadata matches the given contact email or name.
 */
function callMatchesContact(call, emailLower, nameParts) {
  const inviteeFields = [
    call.attendees,
    call.invitees,
    call.calendar_invitees,
    call.participants,
  ].filter(Boolean);

  for (const field of inviteeFields) {
    const items = Array.isArray(field) ? field : [field];
    for (const item of items) {
      if (!item) continue;
      const str = typeof item === 'string' ? item : JSON.stringify(item);
      const lower = str.toLowerCase();
      if (lower.includes(emailLower)) return true;
      if (nameParts.some(p => lower.includes(p))) return true;
    }
  }

  // Check call title for contact name
  const title = (call.title || '').toLowerCase();
  if (nameParts.some(p => title.includes(p))) return true;

  return false;
}

/**
 * Look up a Fathom transcript for a contact.
 *
 * @param {string} email         - contact's email address
 * @param {string} contactName   - contact's full name
 * @param {string} apiKey        - Fathom API key
 * @param {string} [fathomUrl]   - optional: direct Fathom call URL from trigger file
 *                                 e.g. "https://fathom.video/calls/704816497"
 *                                 When provided, skips search and fetches directly.
 * @returns {Promise<string>}
 */
export async function getFathomTranscript(email, contactName, apiKey, fathomUrl) {
  if (!apiKey) {
    console.warn('  FATHOM_API_KEY not set — skipping transcript lookup.');
    return 'No transcript available. FATHOM_API_KEY secret is not configured.';
  }

  const headers = {
    'Authorization': `Bearer ${apiKey}`,
    'Accept': 'application/json',
  };

  // ── Strategy 1: Direct call ID lookup ──────────────────────────────────────
  // Most reliable. Use when a fathom_url is stored in the trigger file.
  const directCallId = extractCallId(fathomUrl);
  if (directCallId) {
    console.log(`  Fathom: direct lookup for call ID ${directCallId}`);
    const summaryText = await fetchCallSummary(directCallId, headers);
    if (summaryText) {
      console.log(`  Fathom: found summary via direct call ID ${directCallId}`);
      return summaryText.slice(0, MAX_SUMMARY_CHARS);
    }
    console.warn(`  Fathom: direct lookup failed for call ${directCallId}, falling back to search`);
  }

  // ── Strategy 2: List recent calls + client-side filter ─────────────────────
  // The Fathom REST API list endpoint does not support filtering by invitee email.
  // We fetch recent calls and match by email/name in metadata and title.
  const emailLower = (email || '').toLowerCase().trim();
  const nameParts = (contactName || '')
    .toLowerCase()
    .split(/\s+/)
    .filter(p => p.length > 2);

  const since = new Date(Date.now() - LOOKBACK_DAYS * 24 * 60 * 60 * 1000)
    .toISOString()
    .split('T')[0];

  let allCalls = [];
  let page = 1;
  let keepPaging = true;

  while (keepPaging && page <= 5) {
    const url = `${FATHOM_BASE}/calls?per_page=100&page=${page}&sort=created_at:desc&created_after=${since}`;
    let res;
    try {
      res = await fetch(url, { headers });
    } catch (err) {
      console.warn(`  Fathom network error on page ${page}: ${err.message}`);
      break;
    }

    if (!res.ok) {
      if (res.status === 404 && page === 1) {
        // Try without date filter
        const fallbackRes = await fetch(`${FATHOM_BASE}/calls?per_page=100&sort=created_at:desc`, { headers });
        if (!fallbackRes.ok) {
          console.warn(`  Fathom list API unavailable: ${fallbackRes.status}`);
          return `No Fathom transcript available (list API returned ${fallbackRes.status}).`;
        }
        const fallbackData = await fallbackRes.json();
        allCalls = fallbackData.calls || fallbackData.data || fallbackData.results || [];
        keepPaging = false;
        break;
      }
      console.warn(`  Fathom API error on page ${page}: ${res.status}`);
      break;
    }

    const data = await res.json();
    const pageCalls = data.calls || data.data || data.results || [];
    allCalls = allCalls.concat(pageCalls);

    if (pageCalls.length < 100 || !data.next_page) {
      keepPaging = false;
    } else {
      page++;
    }
  }

  if (!allCalls.length) {
    console.log(`  Fathom: no calls returned from list API.`);
    return `No Fathom transcript found for ${contactName} (${email}).`;
  }

  console.log(`  Fathom: scanning ${allCalls.length} call(s) for "${contactName}" / ${email}`);

  const matched = allCalls.filter(call => callMatchesContact(call, emailLower, nameParts));

  if (!matched.length) {
    return `No Fathom transcript found for ${contactName} (${email}).`;
  }

  const latest = matched[0];
  const callLabel = latest.title || latest.id;
  console.log(`  Fathom: matched "${callLabel}" (${latest.created_at || ''})`);

  const summaryText = await fetchCallSummary(latest.id, headers);
  if (!summaryText) {
    return `Fathom recording found ("${callLabel}") but summary is unavailable.`;
  }

  return summaryText.slice(0, MAX_SUMMARY_CHARS);
}
