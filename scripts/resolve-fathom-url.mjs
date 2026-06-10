#!/usr/bin/env node
/**
 * resolve-fathom-url.mjs
 *
 * Resolves the Fathom recording URL for a HubSpot contact.
 *
 * The Fathom → HubSpot integration ("Log Meetings and Fathom Call Summaries
 * in HubSpot") logs each recording as a HubSpot Note engagement on the
 * matching contact. The note body contains the call summary and a link to
 * the Fathom recording.
 *
 * Strategy:
 *   1. Use fathom_url from trigger JSON if present.
 *   2. Search HubSpot notes associated with the contact for a fathom.video URL.
 *   3. Fallback: search HubSpot calls (in case object type varies by setup).
 *
 * Usage:   node scripts/resolve-fathom-url.mjs <hubspot_contact_id> [fathom_url_hint]
 * Output:  Fathom URL printed to stdout, nothing if not found.
 * Env:     HUBSPOT_TOKEN
 */

const [, , contactId, fathomUrlHint] = process.argv;

// Matches both direct call URLs and share URLs logged by Fathom's HubSpot integration
const FATHOM_URL_RE = /https:\/\/fathom\.video\/(calls\/\d+|share\/[A-Za-z0-9_-]+)/;

if (fathomUrlHint && FATHOM_URL_RE.test(fathomUrlHint)) {
  process.stdout.write(fathomUrlHint.match(FATHOM_URL_RE)[0]);
  process.exit(0);
}

const HUBSPOT_TOKEN = process.env.HUBSPOT_TOKEN;
if (!HUBSPOT_TOKEN || !contactId || contactId === 'undefined' || contactId === '') {
  process.exit(0);
}

const HEADERS = {
  Authorization: `Bearer ${HUBSPOT_TOKEN}`,
  'Content-Type': 'application/json',
};

/**
 * Get all HubSpot object IDs of a given type associated with this contact,
 * then batch-read their body/text fields and return any that contain a Fathom URL.
 * bodyFields: string or array of property names to search.
 * Call URLs (/calls/\d+) take priority over share URLs (/share/...).
 * Returns the most recent Fathom URL found, or null.
 */
async function searchEngagementType(objectType, bodyFields) {
  const fields = Array.isArray(bodyFields) ? bodyFields : [bodyFields];

  const assocRes = await fetch(
    `https://api.hubapi.com/crm/v3/objects/contacts/${contactId}/associations/${objectType}`,
    { headers: HEADERS }
  );
  if (!assocRes.ok) {
    console.error(`HubSpot ${objectType} associations: ${assocRes.status}`);
    return null;
  }

  const ids = ((await assocRes.json()).results || []).map(r => r.id);
  if (!ids.length) return null;

  const batchRes = await fetch(
    `https://api.hubapi.com/crm/v3/objects/${objectType}/batch/read`,
    {
      method: 'POST',
      headers: HEADERS,
      body: JSON.stringify({
        properties: [...fields, 'hs_timestamp', 'hs_lastmodifieddate'],
        inputs: ids.map(id => ({ id })),
      }),
    }
  );
  if (!batchRes.ok) {
    console.error(`HubSpot ${objectType} batch read: ${batchRes.status}`);
    return null;
  }

  const items = (await batchRes.json()).results || [];

  // Sort most-recent first
  items.sort((a, b) => {
    const ta = new Date(a.properties?.hs_timestamp || a.properties?.hs_lastmodifieddate || 0).getTime();
    const tb = new Date(b.properties?.hs_timestamp || b.properties?.hs_lastmodifieddate || 0).getTime();
    return tb - ta;
  });

  let shareUrlFallback = null;

  for (const item of items) {
    for (const field of fields) {
      const body = item.properties?.[field] || '';
      const m = body.match(FATHOM_URL_RE);
      if (m) {
        const url = 'https://fathom.video/' + m[1];
        if (m[1].startsWith('calls/')) {
          console.error(`Found Fathom call URL in HubSpot ${objectType}.${field} (id ${item.id})`);
          return url;
        }
        if (!shareUrlFallback) {
          console.error(`Found Fathom share URL in HubSpot ${objectType}.${field} (id ${item.id})`);
          shareUrlFallback = url;
        }
      }
    }
  }

  if (shareUrlFallback) return shareUrlFallback;

  console.error(`Scanned ${items.length} HubSpot ${objectType} — no Fathom URL found.`);
  return null;
}

(async () => {
  try {
    // Fathom's HubSpot integration logs summaries to hs_internal_meeting_notes on Meeting engagements
    const fromMeetings = await searchEngagementType('meetings', ['hs_meeting_body', 'hs_internal_meeting_notes']);
    if (fromMeetings) {
      process.stdout.write(fromMeetings);
      process.exit(0);
    }

    // Fallback: notes
    const fromNotes = await searchEngagementType('notes', 'hs_note_body');
    if (fromNotes) {
      process.stdout.write(fromNotes);
      process.exit(0);
    }

    // Fallback: calls
    const fromCalls = await searchEngagementType('calls', 'hs_call_body');
    if (fromCalls) {
      process.stdout.write(fromCalls);
      process.exit(0);
    }

    console.error('No Fathom URL found in HubSpot meetings, notes, or calls for this contact.');
    process.exit(0);
  } catch (err) {
    console.error(`resolve-fathom-url error: ${err.message}`);
    process.exit(0);
  }
})();
