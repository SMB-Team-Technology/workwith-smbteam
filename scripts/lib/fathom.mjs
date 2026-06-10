/**
 * fathom.mjs — shared Fathom transcript lookup utility
 *
 * The Fathom REST API v1 does NOT support filtering by invitee email via query
 * parameter (returns 404). Instead we fetch recent calls and filter client-side
 * by matching the contact's email or name against call metadata.
 */

const FATHOM_BASE = 'https://fathom.video/api/v1';
const LOOKBACK_DAYS = 90;
const MAX_SUMMARY_CHARS = 8000;

/**
 * Returns true if a call's metadata matches the given contact email or name.
 */
function callMatchesContact(call, emailLower, nameParts) {
  // Collect all attendee/invitee identifiers from possible field names
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

  // Also check the call title for the contact name
  const title = (call.title || '').toLowerCase();
  if (nameParts.some(p => title.includes(p))) return true;

  return false;
}

/**
 * Fetch the summary text for a single call. Returns null on failure.
 */
async function fetchCallSummary(callId, headers) {
  const res = await fetch(`${FATHOM_BASE}/calls/${callId}/summary`, { headers });
  if (!res.ok) return null;
  const data = await res.json();
  return data.summary || data.text || data.content || null;
}

/**
 * Look up a Fathom call transcript for a contact, identified by email and name.
 *
 * Strategy:
 *  1. List recent calls (last LOOKBACK_DAYS days) via GET /api/v1/calls
 *  2. Filter client-side by matching email or name in invitee/attendee fields or title
 *  3. Fetch the summary for the most recent matched call
 *
 * @param {string} email - contact's email address
 * @param {string} contactName - contact's full name (used for name-based matching)
 * @param {string} apiKey - Fathom API key
 * @returns {Promise<string>} transcript/summary text, or a descriptive fallback message
 */
export async function getFathomTranscript(email, contactName, apiKey) {
  if (!apiKey) {
    console.warn('  FATHOM_API_KEY not set — skipping transcript lookup.');
    return 'No transcript available. FATHOM_API_KEY secret is not configured.';
  }

  const headers = {
    'Authorization': `Bearer ${apiKey}`,
    'Accept': 'application/json',
  };

  const emailLower = (email || '').toLowerCase().trim();
  const nameParts = (contactName || '')
    .toLowerCase()
    .split(/\s+/)
    .filter(p => p.length > 2);

  // Fetch recent calls without an email filter (that filter returns 404)
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
        // Try without date filter — some API versions don't support created_after
        const fallbackUrl = `${FATHOM_BASE}/calls?per_page=100&sort=created_at:desc`;
        const fallbackRes = await fetch(fallbackUrl, { headers });
        if (!fallbackRes.ok) {
          console.warn(`  Fathom list API unavailable: ${fallbackRes.status}`);
          return `No Fathom transcript available (API returned ${fallbackRes.status}).`;
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

    // Stop paging if this page was short (last page) or no next cursor
    if (pageCalls.length < 100 || !data.next_page) {
      keepPaging = false;
    } else {
      page++;
    }
  }

  if (!allCalls.length) {
    console.log(`  No Fathom calls returned from API.`);
    return `No Fathom transcript found for ${contactName} (${email}).`;
  }

  console.log(`  Fathom: scanning ${allCalls.length} recent call(s) for "${contactName}" / ${email}`);

  const matched = allCalls.filter(call => callMatchesContact(call, emailLower, nameParts));

  if (!matched.length) {
    console.log(`  No matching Fathom recording found for ${contactName} (${email}).`);
    return `No Fathom transcript found for ${contactName} (${email}).`;
  }

  const latest = matched[0];
  const callLabel = latest.title || latest.id;
  console.log(`  Matched Fathom recording: "${callLabel}" (${latest.created_at || ''})`);

  const summaryText = await fetchCallSummary(latest.id, headers);
  if (!summaryText) {
    return `Fathom recording found ("${callLabel}") but summary is unavailable.`;
  }

  return summaryText.slice(0, MAX_SUMMARY_CHARS);
}
