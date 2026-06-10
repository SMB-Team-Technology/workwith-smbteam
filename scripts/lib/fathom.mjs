/**
 * fathom.mjs — shared Fathom transcript lookup utility
 *
 * The Fathom REST API only supports direct call lookup by ID.
 * GET /api/v1/calls (list) returns HTTP 404 — that endpoint does not exist.
 * Call discovery must happen via the Fathom MCP in interactive Claude Code
 * sessions (see .claude/commands/trigger.md) before the pipeline runs.
 */

const FATHOM_BASE = 'https://fathom.video/api/v1';
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
 * Look up a Fathom transcript for a contact.
 *
 * @param {string} email         - contact's email address (unused, kept for API compat)
 * @param {string} contactName   - contact's full name (unused, kept for API compat)
 * @param {string} apiKey        - Fathom API key
 * @param {string} [fathomUrl]   - direct Fathom call URL from trigger file
 *                                 e.g. "https://fathom.video/calls/704816497"
 *                                 Must be present — the Fathom REST API has no list endpoint.
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

  const directCallId = extractCallId(fathomUrl);
  if (!directCallId) {
    console.warn('  Fathom: no fathom_url in trigger file. The Fathom REST API has no list endpoint — call discovery requires running /trigger in Claude Code to find and record the URL first.');
    return `No Fathom transcript available — fathom_url not set. Use the /trigger command to create trigger files with automatic Fathom call lookup.`;
  }

  console.log(`  Fathom: direct lookup for call ID ${directCallId}`);
  const summaryText = await fetchCallSummary(directCallId, headers);
  if (summaryText) {
    console.log(`  Fathom: found summary via call ID ${directCallId}`);
    return summaryText.slice(0, MAX_SUMMARY_CHARS);
  }

  return `Fathom call ${directCallId} found but summary is unavailable.`;
}
