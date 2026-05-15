/**
 * check-proposal-bookings.mjs
 *
 * Runs daily via audit-scheduler.yml. Queries HubSpot for contacts where a
 * closer recently booked a Proposal Call, fetches the Fathom discovery call
 * transcript for each, and writes a trigger JSON to triggers/audit-research/
 * so the audit-pipeline.yml workflow fires automatically.
 *
 * Required secrets:
 *   HUBSPOT_TOKEN   — HubSpot private app token (Settings → Integrations → Private Apps)
 *   FATHOM_API_KEY  — Fathom API key (fathom.video → Settings → API)
 *
 * Optional:
 *   LOOKBACK_HOURS  — How far back to look for new bookings (default: 48)
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';

const HUBSPOT_TOKEN  = process.env.HUBSPOT_TOKEN;
const FATHOM_API_KEY = process.env.FATHOM_API_KEY;
const LOOKBACK_HOURS = parseInt(process.env.LOOKBACK_HOURS || '48', 10);

if (!HUBSPOT_TOKEN) {
  console.error('ERROR: HUBSPOT_TOKEN secret is not set.');
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Utilities
// ---------------------------------------------------------------------------

/** Convert "Conroy Scott LLP" → "conroy-scott" */
function toFriendlyName(firmName) {
  return firmName
    .toLowerCase()
    .replace(/\b(llp|llc|pc|pllc|ltd|inc|co\.?|law\s+group|law\s+firm|attorneys?|counselors?)\b/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '')
    .trim();
}

/** Format a Date as "May 15, 2026" */
function formatDate(date) {
  return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
}

// ---------------------------------------------------------------------------
// HubSpot
// ---------------------------------------------------------------------------

/**
 * Find contacts where a proposal call was recently booked.
 *
 * Detection logic: contacts modified in the last LOOKBACK_HOURS that have an
 * upcoming `notes_next_activity_date`. This catches the "closer just booked a
 * proposal call" event without needing a custom HubSpot property.
 *
 * IMPROVEMENT OPTION: Create a HubSpot workflow that sets a custom property
 * `proposal_call_booked_at` (datetime) when a "Law Firm Proposal Review"
 * meeting is booked. Then filter on that property here instead. That removes
 * false positives from other types of activity.
 */
async function findProposalBookings() {
  const since = new Date(Date.now() - LOOKBACK_HOURS * 60 * 60 * 1000).toISOString();
  const now   = new Date().toISOString();

  const body = {
    filterGroups: [{
      filters: [
        { propertyName: 'lastmodifieddate',       operator: 'GTE', value: since },
        { propertyName: 'notes_next_activity_date', operator: 'GTE', value: now  },
      ]
    }],
    properties: [
      'firstname', 'lastname', 'email', 'phone', 'company', 'website',
      'city', 'state', 'country', 'hubspot_owner_id',
      'notes_next_activity_date', 'lifecyclestage', 'hs_lead_status',
    ],
    sorts: [{ propertyName: 'lastmodifieddate', propertyOrder: 'DESCENDING' }],
    limit: 50,
  };

  const res = await fetch('https://api.hubapi.com/crm/v3/objects/contacts/search', {
    method:  'POST',
    headers: {
      'Authorization': `Bearer ${HUBSPOT_TOKEN}`,
      'Content-Type':  'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    throw new Error(`HubSpot contacts/search failed: ${res.status} ${await res.text()}`);
  }

  const data = await res.json();
  return data.results || [];
}

/** Resolve a HubSpot owner ID to a display name. */
async function getOwnerName(ownerId) {
  if (!ownerId) return 'Sales Rep';
  const res = await fetch(`https://api.hubapi.com/crm/v3/owners/${ownerId}`, {
    headers: { 'Authorization': `Bearer ${HUBSPOT_TOKEN}` },
  });
  if (!res.ok) return 'Sales Rep';
  const data = await res.json();
  return `${data.firstName || ''} ${data.lastName || ''}`.trim() || 'Sales Rep';
}

// ---------------------------------------------------------------------------
// Fathom
// ---------------------------------------------------------------------------

/**
 * Look up Fathom recordings for a contact by email, then return the summary
 * of the most recent discovery/analysis call as a transcript string.
 *
 * NOTE: The Fathom REST API endpoint below is based on documented v1 API
 * structure. Verify against https://developers.fathom.video if endpoints change.
 */
async function getFathomTranscript(email, contactName) {
  if (!FATHOM_API_KEY) {
    console.warn('  FATHOM_API_KEY not set — skipping transcript lookup.');
    return `No transcript available. FATHOM_API_KEY secret is not configured.`;
  }

  // Search recordings where this person was an invitee
  const searchUrl = `https://fathom.video/api/v1/calls?invitee_email=${encodeURIComponent(email)}&per_page=10&sort=created_at:desc`;
  const res = await fetch(searchUrl, {
    headers: {
      'Authorization': `Bearer ${FATHOM_API_KEY}`,
      'Accept':        'application/json',
    },
  });

  if (!res.ok) {
    console.warn(`  Fathom lookup failed for ${email}: ${res.status}`);
    return `No Fathom transcript available (API returned ${res.status} for ${email}).`;
  }

  const data  = await res.json();
  const calls = data.calls || data.data || data.results || [];

  if (!calls.length) {
    console.log(`  No Fathom recordings found for ${email}.`);
    return `No Fathom transcript found for ${contactName} (${email}).`;
  }

  // Use the most recent call's summary
  const latest    = calls[0];
  const summaryRes = await fetch(`https://fathom.video/api/v1/calls/${latest.id}/summary`, {
    headers: {
      'Authorization': `Bearer ${FATHOM_API_KEY}`,
      'Accept':        'application/json',
    },
  });

  if (!summaryRes.ok) {
    return `Fathom recording found (${latest.title || latest.id}) but summary unavailable.`;
  }

  const summary = await summaryRes.json();
  const text    = summary.summary || summary.text || summary.content || JSON.stringify(summary);
  console.log(`  Found Fathom transcript: "${latest.title || latest.id}" (${latest.created_at || ''})`);
  return text.slice(0, 8000); // cap at ~8k chars — the full summary is what matters
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  console.log(`\n=== Audit Scheduler: checking last ${LOOKBACK_HOURS}h for proposal bookings ===\n`);

  const contacts = await findProposalBookings();
  console.log(`HubSpot returned ${contacts.length} contact(s) with upcoming activity.\n`);

  if (!contacts.length) {
    console.log('No new proposal bookings. Exiting.');
    return;
  }

  mkdirSync('triggers/audit-research', { recursive: true });

  const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  let triggered = 0;

  for (const contact of contacts) {
    const p           = contact.properties;
    const contactName = `${p.firstname || ''} ${p.lastname || ''}`.trim();
    const firmName    = p.company || contactName;
    const friendlyName = toFriendlyName(firmName);
    const triggerPath = `triggers/audit-research/${friendlyName}.json`;

    console.log(`Processing: ${contactName} — ${firmName}`);

    // Skip if already triggered today for this firm
    if (existsSync(triggerPath)) {
      try {
        const existing = JSON.parse(readFileSync(triggerPath, 'utf8'));
        if (existing._triggered_date === today) {
          console.log(`  Already triggered today — skipping.\n`);
          continue;
        }
      } catch (_) { /* file exists but is malformed — overwrite */ }
    }

    const salesRep   = await getOwnerName(p.hubspot_owner_id);
    const transcript = await getFathomTranscript(p.email, contactName);
    const auditDate  = formatDate(new Date());

    const triggerData = {
      firm_name:          firmName,
      friendly_name:      friendlyName,
      url:                p.website || `https://${firmName.toLowerCase().replace(/\s+/g, '')}.com`,
      sales_rep:          salesRep,
      date:               auditDate,
      hubspot_contact_id: contact.id,
      contact_email:      p.email,
      proposal_call_date: p.notes_next_activity_date || null,
      _triggered_date:    today,
      transcript,
    };

    writeFileSync(triggerPath, JSON.stringify(triggerData, null, 2));
    console.log(`  Wrote trigger: ${triggerPath}\n`);
    triggered++;
  }

  console.log(`=== Done: triggered ${triggered} new audit(s). ===`);
}

main().catch(err => {
  console.error('Script error:', err);
  process.exit(1);
});
