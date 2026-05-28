/**
 * check-proposal-bookings.mjs
 *
 * Runs on a schedule via audit-scheduler.yml. Detects proposal-ready contacts
 * via two complementary signals and writes trigger JSONs to
 * triggers/audit-research/ so the audit-pipeline.yml workflow fires.
 *
 * Signal 1 — Deal stage: deals moved to "Proposal Scheduled" stages
 *   (34633617 or 34633618) within the last LOOKBACK_DAYS days.
 *
 * Signal 2 — Meeting booking: HubSpot Meeting objects titled
 *   "Law Firm Proposal Review" that started within the last LOOKBACK_DAYS days.
 *   This catches closers who book directly via calendar without moving the
 *   deal stage first (e.g. Randy Haas, Kate Lawrence pattern).
 *
 * Required secrets:
 *   HUBSPOT_TOKEN   — HubSpot private app token (Settings → Integrations → Private Apps)
 *   FATHOM_API_KEY  — Fathom API key (fathom.video → Settings → API)
 *
 * Optional:
 *   LOOKBACK_DAYS   — How many days back to look for signals (default: 2)
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
// HubSpot Meetings (Signal 2)
// ---------------------------------------------------------------------------

/**
 * Find HubSpot Meeting objects titled "Law Firm Proposal Review" that started
 * within the last LOOKBACK_DAYS days. Returns an array of { meeting, contact }
 * objects so callers can build trigger files without extra lookups.
 */
async function findProposalMeetings() {
  const nowMs      = Date.now();
  const lookbackMs = nowMs - LOOKBACK_DAYS * 24 * 60 * 60 * 1000;

  const body = {
    filterGroups: [{
      filters: [
        { propertyName: 'hs_meeting_title',      operator: 'EQ',  value: 'Law Firm Proposal Review' },
        { propertyName: 'hs_meeting_start_time', operator: 'GTE', value: String(lookbackMs) },
      ],
    }],
    properties: [
      'hs_meeting_title', 'hs_meeting_start_time', 'hubspot_owner_id',
      'hs_timestamp', 'hs_lastmodifieddate',
    ],
    sorts: [{ propertyName: 'hs_meeting_start_time', propertyOrder: 'ASCENDING' }],
    limit: 50,
  };

  const res = await fetch('https://api.hubapi.com/crm/v3/objects/meetings/search', {
    method:  'POST',
    headers: {
      'Authorization': `Bearer ${HUBSPOT_TOKEN}`,
      'Content-Type':  'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    console.warn(`HubSpot meetings/search failed: ${res.status} ${await res.text()} — skipping meeting signal.`);
    return [];
  }

  const data     = await res.json();
  const meetings = data.results || [];
  console.log(`HubSpot returned ${meetings.length} "Law Firm Proposal Review" meeting(s) in last ${LOOKBACK_DAYS} days.\n`);
  return meetings;
}

/**
 * Return the primary contact associated with a meeting, or null if none.
 */
async function getContactFromMeeting(meetingId) {
  const res = await fetch(
    `https://api.hubapi.com/crm/v3/objects/meetings/${meetingId}/associations/contacts`,
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

/**
 * Return the primary deal associated with a contact, or null if none.
 * Used to get deal_id and hubspot_owner_id for meeting-triggered firms.
 */
async function getDealFromContact(contactId) {
  const res = await fetch(
    `https://api.hubapi.com/crm/v3/objects/contacts/${contactId}/associations/deals`,
    { headers: { 'Authorization': `Bearer ${HUBSPOT_TOKEN}` } }
  );
  if (!res.ok) return null;

  const data    = await res.json();
  const results = data.results || [];
  if (!results.length) return null;

  const dealId = results[0].id;
  const dRes = await fetch(
    `https://api.hubapi.com/crm/v3/objects/deals/${dealId}?properties=dealname,hubspot_owner_id,hs_lastmodifieddate`,
    { headers: { 'Authorization': `Bearer ${HUBSPOT_TOKEN}` } }
  );
  if (!dRes.ok) return null;
  const deal = await dRes.json();
  return { id: dealId, ...deal.properties };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  console.log(`\n=== Audit Scheduler: deals moved to Proposal Scheduled stages in last ${LOOKBACK_DAYS} days ===\n`);

  const deals = await findProposalBookings();
  console.log(`HubSpot returned ${deals.length} deal(s) in Proposal Scheduled stage.\n`);

  mkdirSync('triggers/audit-research', { recursive: true });

  const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  let triggered = 0;

  // Track friendly names written in this run to deduplicate against meeting signal
  const writtenThisRun = new Set();

  // --- Signal 1: Deal stage ---
  for (const deal of deals) {
    const p         = deal.properties;
    const dealName  = p.dealname || '';

    const contact   = await getPrimaryContact(deal.id);
    const firmName  = contact?.company || dealName.replace(/\s*\(.*?\)\s*$/, '').replace(/\s*-\s*New Deal\s*$/i, '').trim() || dealName;
    const friendlyName = toFriendlyName(firmName);
    const triggerPath  = `triggers/audit-research/${friendlyName}.json`;

    const stageEnteredDate = p.hs_v2_date_entered_current_stage
      ? new Date(p.hs_v2_date_entered_current_stage).toISOString().slice(0, 10)
      : today;

    console.log(`Processing deal: ${dealName} (stage entered: ${stageEnteredDate})`);

    if (existsSync(triggerPath)) {
      try {
        const existing = JSON.parse(readFileSync(triggerPath, 'utf8'));
        if (existing._triggered_date === today) {
          console.log(`  Already triggered today — skipping.\n`);
          writtenThisRun.add(friendlyName);
          continue;
        }
      } catch (_) { /* malformed file — overwrite */ }
    }

    const dealOwner    = await getOwnerDetails(p.hubspot_owner_id);
    const contactEmail = contact?.email || '';
    const contactName  = contact
      ? `${contact.firstname || ''} ${contact.lastname || ''}`.trim()
      : firmName;
    const transcript   = await getFathomTranscript(contactEmail, contactName);
    const auditDate    = formatDate(new Date());

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
    writtenThisRun.add(friendlyName);
    triggered++;
  }

  // --- Signal 2: "Law Firm Proposal Review" meeting bookings ---
  console.log('\n=== Checking for "Law Firm Proposal Review" meeting bookings ===\n');
  const meetings = await findProposalMeetings();

  for (const meeting of meetings) {
    const mp = meeting.properties;

    const contact = await getContactFromMeeting(meeting.id);
    if (!contact) {
      console.log(`  Meeting ${meeting.id}: no associated contact — skipping.\n`);
      continue;
    }

    const firmName     = contact.company || `${contact.firstname || ''} ${contact.lastname || ''}`.trim() || `Meeting ${meeting.id}`;
    const friendlyName = toFriendlyName(firmName);
    const triggerPath  = `triggers/audit-research/${friendlyName}.json`;

    const meetingStart = mp.hs_meeting_start_time
      ? new Date(mp.hs_meeting_start_time).toISOString()
      : null;

    console.log(`Processing meeting: ${mp.hs_meeting_title} → ${firmName} (starts: ${meetingStart || 'unknown'})`);

    // Skip if already handled by deal-stage signal this run
    if (writtenThisRun.has(friendlyName)) {
      console.log(`  Already triggered via deal stage this run — skipping.\n`);
      continue;
    }

    if (existsSync(triggerPath)) {
      try {
        const existing = JSON.parse(readFileSync(triggerPath, 'utf8'));
        if (existing._triggered_date === today) {
          console.log(`  Already triggered today — skipping.\n`);
          writtenThisRun.add(friendlyName);
          continue;
        }
      } catch (_) { /* malformed file — overwrite */ }
    }

    // Try to get deal and owner from the contact
    const deal       = await getDealFromContact(contact.id);
    const ownerId    = deal?.hubspot_owner_id || mp.hubspot_owner_id || null;
    const dealOwner  = await getOwnerDetails(ownerId);

    const contactEmail = contact.email || '';
    const contactName  = `${contact.firstname || ''} ${contact.lastname || ''}`.trim() || firmName;
    const transcript   = await getFathomTranscript(contactEmail, contactName);
    const auditDate    = formatDate(new Date());

    const triggerData = {
      firm_name:          firmName,
      friendly_name:      friendlyName,
      url:                contact.website || '',
      sales_rep:          dealOwner.name,
      sales_rep_email:    dealOwner.email,
      date:               auditDate,
      hubspot_contact_id: contact.id || null,
      contact_email:      contactEmail,
      deal_id:            deal?.id || null,
      proposal_call_date: meetingStart,
      _triggered_date:    today,
      transcript,
    };

    writeFileSync(triggerPath, JSON.stringify(triggerData, null, 2));
    console.log(`  Wrote trigger: ${triggerPath}\n`);
    writtenThisRun.add(friendlyName);
    triggered++;
  }

  if (!triggered && !writtenThisRun.size) {
    console.log('No new proposal bookings found.');
  }
  console.log(`\n=== Done: triggered ${triggered} new audit(s). ===`);
}

main().catch(err => {
  console.error('Script error:', err);
  process.exit(1);
});
