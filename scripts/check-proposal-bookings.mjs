/**
 * check-proposal-bookings.mjs
 *
 * Runs on a schedule via audit-scheduler.yml. Queries HubSpot for deals that
 * were moved to the "Proposal Scheduled" stage (34633618) within the last
 * LOOKBACK_DAYS days, fetches the primary contact and their Fathom discovery
 * call transcript, and writes a trigger JSON to triggers/audit-research/ so
 * the audit-pipeline.yml workflow fires.
 *
 * Required secrets:
 *   HUBSPOT_TOKEN   — HubSpot private app token (Settings → Integrations → Private Apps)
 *   FATHOM_API_KEY  — Fathom API key (fathom.video → Settings → API)
 *
 * Optional:
 *   LOOKBACK_DAYS   — How many days back to look for stage changes (default: 2)
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';

const HUBSPOT_TOKEN  = process.env.HUBSPOT_TOKEN;
const FATHOM_API_KEY = process.env.FATHOM_API_KEY;
const LOOKBACK_DAYS  = parseInt(process.env.LOOKBACK_DAYS || '2', 10);

// Deal stage IDs that indicate a proposal should be generated.
// 34633617 (40%) = "Proposal Scheduled"
// 34633618 (50%) = next stage — reps sometimes land here directly
const PROPOSAL_STAGES = ['34633617', '34633618'];

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
 * Find deals that have been moved to a proposal stage within the last
 * LOOKBACK_DAYS days. Uses OR logic across both proposal stage IDs so deals
 * landing in either stage are captured.
 */
async function findProposalBookings() {
  const nowMs      = Date.now();
  const lookbackMs = nowMs - LOOKBACK_DAYS * 24 * 60 * 60 * 1000;

  // One filterGroup per stage (OR logic between groups), each ANDed with the time window
  const body = {
    filterGroups: PROPOSAL_STAGES.map(stageId => ({
      filters: [
        { propertyName: 'dealstage',           operator: 'EQ',  value: stageId },
        { propertyName: 'hs_lastmodifieddate',  operator: 'GTE', value: String(lookbackMs) },
      ],
    })),
    properties: [
      'dealname', 'dealstage', 'pipeline', 'hubspot_owner_id',
      'hs_lastmodifieddate', 'hs_v2_date_entered_current_stage',
    ],
    sorts: [{ propertyName: 'hs_lastmodifieddate', propertyOrder: 'ASCENDING' }],
    limit: 50,
  };

  const res = await fetch('https://api.hubapi.com/crm/v3/objects/deals/search', {
    method:  'POST',
    headers: {
      'Authorization': `Bearer ${HUBSPOT_TOKEN}`,
      'Content-Type':  'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    throw new Error(`HubSpot deals/search failed: ${res.status} ${await res.text()}`);
  }

  const data = await res.json();
  return data.results || [];
}

/**
 * Return the primary contact associated with a deal, or null if none.
 * Picks the first contact in the associations list.
 */
async function getPrimaryContact(dealId) {
  const res = await fetch(
    `https://api.hubapi.com/crm/v3/objects/deals/${dealId}/associations/contacts`,
    { headers: { 'Authorization': `Bearer ${HUBSPOT_TOKEN}` } }
  );
  if (!res.ok) return null;

  const data    = await res.json();
  const results = data.results || [];
  if (!results.length) return null;

  const contactId = results[0].id;
  const cRes = await fetch(
    `https://api.hubapi.com/crm/v3/objects/contacts/${contactId}?properties=firstname,lastname,email,company,website`,
    { headers: { 'Authorization': `Bearer ${HUBSPOT_TOKEN}` } }
  );
  if (!cRes.ok) return null;
  const contact = await cRes.json();
  return { id: contactId, ...contact.properties };
}

/** Resolve a HubSpot owner ID to { name, email }. */
async function getOwnerDetails(ownerId) {
  if (!ownerId) return { name: 'Sales Rep', email: '' };
  const res = await fetch(`https://api.hubapi.com/crm/v3/owners/${ownerId}`, {
    headers: { 'Authorization': `Bearer ${HUBSPOT_TOKEN}` },
  });
  if (!res.ok) return { name: 'Sales Rep', email: '' };
  const data = await res.json();
  return {
    name:  `${data.firstName || ''} ${data.lastName || ''}`.trim() || 'Sales Rep',
    email: data.email || '',
  };
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

  const latest     = calls[0];
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
  return text.slice(0, 8000);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  console.log(`\n=== Audit Scheduler: deals moved to Proposal Scheduled stages in last ${LOOKBACK_DAYS} days ===\n`);

  const deals = await findProposalBookings();
  console.log(`HubSpot returned ${deals.length} deal(s) in Proposal Scheduled stage.\n`);

  if (!deals.length) {
    console.log('No recently-moved Proposal Scheduled deals found. Exiting.');
    return;
  }

  mkdirSync('triggers/audit-research', { recursive: true });

  const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  let triggered = 0;

  for (const deal of deals) {
    const p         = deal.properties;
    const dealName  = p.dealname || '';

    // Get associated contact for firm name, email, and website
    const contact   = await getPrimaryContact(deal.id);
    const firmName  = contact?.company || dealName.replace(/\s*\(.*?\)\s*$/, '').replace(/\s*-\s*New Deal\s*$/i, '').trim() || dealName;
    const friendlyName = toFriendlyName(firmName);
    const triggerPath  = `triggers/audit-research/${friendlyName}.json`;

    const stageEnteredDate = p.hs_v2_date_entered_current_stage
      ? new Date(p.hs_v2_date_entered_current_stage).toISOString().slice(0, 10)
      : today;

    console.log(`Processing deal: ${dealName} (stage entered: ${stageEnteredDate})`);

    // Skip if already triggered today — avoids re-firing on every scheduler run
    if (existsSync(triggerPath)) {
      try {
        const existing = JSON.parse(readFileSync(triggerPath, 'utf8'));
        if (existing._triggered_date === today) {
          console.log(`  Already triggered today — skipping.\n`);
          continue;
        }
      } catch (_) { /* malformed file — overwrite */ }
    }

    const dealOwner  = await getOwnerDetails(p.hubspot_owner_id);
    const contactEmail = contact?.email || '';
    const contactName  = contact
      ? `${contact.firstname || ''} ${contact.lastname || ''}`.trim()
      : firmName;
    const transcript = await getFathomTranscript(contactEmail, contactName);
    const auditDate  = formatDate(new Date());

    const triggerData = {
      firm_name:          firmName,
      friendly_name:      friendlyName,
      url:                contact?.website || '',
      sales_rep:          dealOwner.name,
      sales_rep_email:    dealOwner.email,
      date:               auditDate,
      hubspot_contact_id: contact?.id || null,
      contact_email:      contactEmail,
      deal_id:            deal.id,
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
