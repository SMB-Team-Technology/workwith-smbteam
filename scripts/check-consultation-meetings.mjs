/**
 * check-consultation-meetings.mjs
 *
 * Runs on a schedule via audit-scheduler.yml. Queries HubSpot for Meeting objects
 * with title "First Mover Growth Consultation" or "Partnership Activation Meeting"
 * that have already started (start time <= now) within the last 7 days, fetches
 * the Fathom discovery call transcript for each associated contact, and writes a
 * trigger JSON to triggers/audit-research/ so the audit-pipeline.yml workflow fires.
 *
 * Trigger files include suppress_pricing: true so the pipeline strips pricing
 * sections from the assembled report.
 *
 * Required secrets:
 *   HUBSPOT_TOKEN   — HubSpot private app token (Settings → Integrations → Private Apps)
 *   FATHOM_API_KEY  — Fathom API key (fathom.video → Settings → API)
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';

const HUBSPOT_TOKEN  = process.env.HUBSPOT_TOKEN;
const FATHOM_API_KEY = process.env.FATHOM_API_KEY;
const LOOKBACK_DAYS  = 7;

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
 * Search HubSpot Meeting objects for meetings with the specified titles that
 * have already started (hs_meeting_start_time <= now) within the last LOOKBACK_DAYS days.
 * Uses filterGroups OR logic — one filterGroup per meeting title.
 */
async function findConsultationMeetings() {
  const nowMs      = Date.now();
  const lookbackMs = nowMs - LOOKBACK_DAYS * 24 * 60 * 60 * 1000;

  const MEETING_TITLES = [
    'First Mover Growth Consultation',
    'Partnership Activation Meeting',
  ];

  // One filterGroup per title (OR logic between groups), each with the time range filters
  const filterGroups = MEETING_TITLES.map(title => ({
    filters: [
      { propertyName: 'hs_meeting_title',      operator: 'EQ',  value: title },
      { propertyName: 'hs_meeting_start_time', operator: 'GTE', value: String(lookbackMs) },
      { propertyName: 'hs_meeting_start_time', operator: 'LTE', value: String(nowMs) },
    ],
  }));

  const body = {
    filterGroups,
    properties: [
      'hs_meeting_title',
      'hs_meeting_start_time',
      'hubspot_owner_id',
    ],
    sorts: [{ propertyName: 'hs_meeting_start_time', propertyOrder: 'DESCENDING' }],
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
    throw new Error(`HubSpot meetings/search failed: ${res.status} ${await res.text()}`);
  }

  const data = await res.json();
  return data.results || [];
}

/**
 * Get the first associated contact ID for a meeting object.
 * Returns null if no contact is associated.
 */
async function getMeetingContactId(meetingId) {
  const res = await fetch(
    `https://api.hubapi.com/crm/v3/objects/meetings/${meetingId}/associations/contacts`,
    { headers: { 'Authorization': `Bearer ${HUBSPOT_TOKEN}` } }
  );
  if (!res.ok) return null;
  const data = await res.json();
  const results = data.results || [];
  return results.length ? results[0].id : null;
}

/**
 * Fetch contact details for a given contact ID.
 */
async function getContactDetails(contactId) {
  const props = 'firstname,lastname,email,company,website,hubspot_owner_id';
  const res = await fetch(
    `https://api.hubapi.com/crm/v3/objects/contacts/${contactId}?properties=${props}`,
    { headers: { 'Authorization': `Bearer ${HUBSPOT_TOKEN}` } }
  );
  if (!res.ok) return null;
  return res.json();
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

/**
 * Find the newest deal associated with a contact and return its owner's
 * details. Falls back to { name: 'Sales Rep', email: '' } if no deal exists.
 */
async function getNewestDealOwner(contactId) {
  const res = await fetch(
    `https://api.hubapi.com/crm/v3/objects/contacts/${contactId}/associations/deals`,
    { headers: { 'Authorization': `Bearer ${HUBSPOT_TOKEN}` } }
  );
  if (!res.ok) return { name: 'Sales Rep', email: '' };

  const data    = res.ok ? await res.json() : {};
  const results = data.results || [];
  if (!results.length) return { name: 'Sales Rep', email: '' };

  // Fetch all associated deals to find the newest by createdate
  const dealsRes = await fetch(
    `https://api.hubapi.com/crm/v3/objects/deals/batch/read`,
    {
      method:  'POST',
      headers: {
        'Authorization': `Bearer ${HUBSPOT_TOKEN}`,
        'Content-Type':  'application/json',
      },
      body: JSON.stringify({
        inputs:     results.map(r => ({ id: r.id })),
        properties: ['hubspot_owner_id', 'createdate'],
      }),
    }
  );
  if (!dealsRes.ok) return { name: 'Sales Rep', email: '' };

  const dealsData = await dealsRes.json();
  const deals     = dealsData.results || [];
  deals.sort((a, b) =>
    new Date(b.properties.createdate) - new Date(a.properties.createdate)
  );

  const newestOwnerId = deals[0]?.properties?.hubspot_owner_id;
  return getOwnerDetails(newestOwnerId);
}

// ---------------------------------------------------------------------------
// Fathom
// ---------------------------------------------------------------------------

/**
 * Look up Fathom recordings for a contact by email, then return the summary
 * of the most recent discovery/analysis call as a transcript string.
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
  console.log(`\n=== Audit Scheduler: consultation meetings in the last ${LOOKBACK_DAYS} days ===\n`);

  const meetings = await findConsultationMeetings();
  console.log(`HubSpot returned ${meetings.length} meeting(s).\n`);

  if (!meetings.length) {
    console.log('No recent consultation meetings found. Exiting.');
    return;
  }

  mkdirSync('triggers/audit-research', { recursive: true });

  let triggered = 0;
  let skipped   = 0;

  for (const meeting of meetings) {
    const p            = meeting.properties;
    const meetingTitle = p.hs_meeting_title || 'Consultation Meeting';
    const meetingId    = meeting.id;

    console.log(`Processing meeting: "${meetingTitle}" (ID: ${meetingId}, start: ${p.hs_meeting_start_time})`);

    // Get associated contact
    const contactId = await getMeetingContactId(meetingId);
    if (!contactId) {
      console.log(`  No associated contact found — skipping.\n`);
      skipped++;
      continue;
    }

    const contact = await getContactDetails(contactId);
    if (!contact) {
      console.log(`  Could not fetch contact ${contactId} — skipping.\n`);
      skipped++;
      continue;
    }

    const cp           = contact.properties;
    const contactName  = `${cp.firstname || ''} ${cp.lastname || ''}`.trim();
    const firmName     = cp.company || contactName;
    const friendlyName = toFriendlyName(firmName);
    const triggerPath  = `triggers/audit-research/${friendlyName}-consult.json`;

    console.log(`  Contact: ${contactName} — ${firmName}`);

    // Deduplication: skip if already triggered for this exact meeting ID
    if (existsSync(triggerPath)) {
      try {
        const existing = JSON.parse(readFileSync(triggerPath, 'utf8'));
        if (existing._triggered_meeting_id === meetingId) {
          console.log(`  Already triggered for meeting ID ${meetingId} — skipping.\n`);
          skipped++;
          continue;
        }
      } catch (_) { /* malformed file — overwrite */ }
    }

    // Sales rep: try newest deal owner, fall back to contact owner
    let dealOwner = await getNewestDealOwner(contactId);
    if (!dealOwner.name || dealOwner.name === 'Sales Rep') {
      dealOwner = await getOwnerDetails(cp.hubspot_owner_id);
    }

    const transcript = await getFathomTranscript(cp.email, contactName);
    const auditDate  = formatDate(new Date());

    const triggerData = {
      firm_name:              firmName,
      friendly_name:          friendlyName,
      url:                    cp.website || '',
      sales_rep:              dealOwner.name,
      sales_rep_email:        dealOwner.email,
      date:                   auditDate,
      hubspot_contact_id:     contactId,
      contact_email:          cp.email,
      meeting_title:          meetingTitle,
      suppress_pricing:       true,
      _triggered_meeting_id:  meetingId,
      transcript,
    };

    writeFileSync(triggerPath, JSON.stringify(triggerData, null, 2));
    console.log(`  Wrote trigger: ${triggerPath}\n`);
    triggered++;
  }

  console.log(`=== Done: triggered ${triggered} new audit(s), skipped ${skipped}. ===`);
}

main().catch(err => {
  console.error('Script error:', err);
  process.exit(1);
});
