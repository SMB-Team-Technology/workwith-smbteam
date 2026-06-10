#!/usr/bin/env node
/**
 * fetch-hubspot-fathom-notes.mjs
 *
 * Extracts the Fathom AI meeting summary from HubSpot's hs_internal_meeting_notes
 * field. Fathom's "Log Meetings and Fathom Call Summaries in HubSpot" integration
 * writes the full AI summary to this field on the associated Meeting engagement.
 *
 * This is used when resolve-fathom-url.mjs returns a share URL (not a direct
 * /calls/:id URL), since the Fathom REST API requires a numeric call ID.
 *
 * Usage:   node scripts/fetch-hubspot-fathom-notes.mjs <hubspot_contact_id>
 * Output:  Plain text summary to stdout, nothing if not found.
 * Env:     HUBSPOT_TOKEN
 */

const [, , contactId] = process.argv;
const HUBSPOT_TOKEN = process.env.HUBSPOT_TOKEN;

if (!HUBSPOT_TOKEN || !contactId || contactId === 'undefined' || contactId === '') {
  process.exit(0);
}

const HEADERS = {
  Authorization: `Bearer ${HUBSPOT_TOKEN}`,
  'Content-Type': 'application/json',
};

function stripHtml(html) {
  return html
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/p>/gi, '\n\n')
    .replace(/<\/li>/gi, '\n')
    .replace(/<\/h[1-6]>/gi, '\n\n')
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&#[0-9]+;/g, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

(async () => {
  try {
    const assocRes = await fetch(
      `https://api.hubapi.com/crm/v3/objects/contacts/${contactId}/associations/meetings`,
      { headers: HEADERS }
    );
    if (!assocRes.ok) {
      console.error(`HubSpot meetings associations: ${assocRes.status}`);
      process.exit(0);
    }

    const ids = ((await assocRes.json()).results || []).map(r => r.id);
    if (!ids.length) {
      console.error('No meetings associated with contact.');
      process.exit(0);
    }

    const batchRes = await fetch(
      'https://api.hubapi.com/crm/v3/objects/meetings/batch/read',
      {
        method: 'POST',
        headers: HEADERS,
        body: JSON.stringify({
          properties: ['hs_internal_meeting_notes', 'hs_timestamp'],
          inputs: ids.map(id => ({ id })),
        }),
      }
    );
    if (!batchRes.ok) {
      console.error(`HubSpot meetings batch read: ${batchRes.status}`);
      process.exit(0);
    }

    const items = (await batchRes.json()).results || [];

    // Sort most-recent first
    items.sort((a, b) => {
      const ta = new Date(a.properties?.hs_timestamp || 0).getTime();
      const tb = new Date(b.properties?.hs_timestamp || 0).getTime();
      return tb - ta;
    });

    for (const item of items) {
      const notes = item.properties?.hs_internal_meeting_notes || '';
      if (notes.includes('fathom.video')) {
        console.error(`Found Fathom notes in meeting ${item.id}`);
        const plain = stripHtml(notes);
        process.stdout.write(plain.slice(0, 8000));
        process.exit(0);
      }
    }

    console.error('No Fathom content found in HubSpot internal meeting notes.');
    process.exit(0);
  } catch (err) {
    console.error(`fetch-hubspot-fathom-notes error: ${err.message}`);
    process.exit(0);
  }
})();
