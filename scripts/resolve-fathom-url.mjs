#!/usr/bin/env node
/**
 * resolve-fathom-url.mjs
 *
 * Resolves the Fathom recording URL for a HubSpot contact.
 *
 * Strategy:
 *   1. If fathom_url_hint is a valid Fathom call URL, use it directly.
 *   2. Query HubSpot calls associated with the contact, parse hs_call_body
 *      for a fathom.video URL. Requires Fathom → HubSpot sync to be enabled
 *      in Fathom account settings (Integrations → HubSpot).
 *
 * Usage:   node scripts/resolve-fathom-url.mjs <hubspot_contact_id> [fathom_url_hint]
 * Output:  Fathom URL printed to stdout, nothing if not found.
 * Env:     HUBSPOT_TOKEN
 */

const [, , contactId, fathomUrlHint] = process.argv;

const FATHOM_URL_RE = /https:\/\/fathom\.video\/calls\/\d+/;

if (fathomUrlHint && FATHOM_URL_RE.test(fathomUrlHint)) {
  process.stdout.write(fathomUrlHint.match(FATHOM_URL_RE)[0]);
  process.exit(0);
}

const HUBSPOT_TOKEN = process.env.HUBSPOT_TOKEN;
if (!HUBSPOT_TOKEN || !contactId || contactId === 'undefined' || contactId === '') {
  process.exit(0);
}

(async () => {
  try {
    // Step 1: get call IDs associated with this contact
    const assocRes = await fetch(
      `https://api.hubapi.com/crm/v3/objects/contacts/${contactId}/associations/calls`,
      { headers: { Authorization: `Bearer ${HUBSPOT_TOKEN}` } }
    );
    if (!assocRes.ok) {
      console.error(`HubSpot associations lookup returned ${assocRes.status}`);
      process.exit(0);
    }

    const callIds = ((await assocRes.json()).results || []).map(r => r.id);
    if (!callIds.length) {
      console.error('No HubSpot calls associated with this contact.');
      process.exit(0);
    }

    // Step 2: batch-read call bodies
    const batchRes = await fetch(
      'https://api.hubapi.com/crm/v3/objects/calls/batch/read',
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${HUBSPOT_TOKEN}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          properties: ['hs_call_body', 'hs_call_title', 'hs_timestamp', 'hs_call_source'],
          inputs: callIds.map(id => ({ id })),
        }),
      }
    );
    if (!batchRes.ok) {
      console.error(`HubSpot batch read returned ${batchRes.status}`);
      process.exit(0);
    }

    const calls = (await batchRes.json()).results || [];

    // Sort most-recent first
    calls.sort((a, b) => {
      const ta = new Date(a.properties?.hs_timestamp || 0).getTime();
      const tb = new Date(b.properties?.hs_timestamp || 0).getTime();
      return tb - ta;
    });

    for (const call of calls) {
      const body = call.properties?.hs_call_body || '';
      const m = body.match(FATHOM_URL_RE);
      if (m) {
        process.stdout.write(m[0]);
        process.exit(0);
      }
    }

    console.error(`Scanned ${calls.length} HubSpot calls — no Fathom URL found. Enable Fathom → HubSpot sync in Fathom account settings.`);
    process.exit(0);
  } catch (err) {
    console.error(`resolve-fathom-url error: ${err.message}`);
    process.exit(0);
  }
})();
