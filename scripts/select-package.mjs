#!/usr/bin/env node
/**
 * Pass 1.5 — Deterministic package selection
 *
 * Reads research notes from a completed Pass 1, applies the SMB Team eligibility
 * rules in code, and writes package_decision.json to the firm folder.
 *
 * Usage: node scripts/select-package.mjs <friendly-name>
 * Output: <friendly-name>/package_decision.json
 *
 * Pass 2 reads this file and uses the tier/price values directly, removing AI
 * judgment from the pricing decision.
 *
 * Exit codes:
 *   0 — decision written (or skipped because trigger has explicit override)
 *   1 — fatal error (no research notes, bad args)
 */

import { readFileSync, writeFileSync, readdirSync, existsSync } from 'fs';
import { join } from 'path';

// ─── Approved pricing tables ─────────────────────────────────────────────────
// Keep in sync with Design Files/audit-write.md and SMB_Team_Audit_Agent_System_Prompt.txt

const MARKETING_TIERS = [
  { tier: 'Essentials', name: 'Full Service Marketing — Essentials', bundled: 3497,  retail: 3797,  adCap: 5_000,   minRev: 0,         maxRev: 749_999 },
  { tier: 'Starter',    name: 'Full Service Marketing — Starter',    bundled: 4997,  retail: 5697,  adCap: 20_000,  minRev: 500_000,   maxRev: 999_999 },
  { tier: 'Growth',     name: 'Full Service Marketing — Growth',     bundled: 7497,  retail: 8997,  adCap: 50_000,  minRev: 1_000_000, maxRev: 1_999_999 },
  { tier: 'Dominate',   name: 'Full Service Marketing — Dominate',   bundled: 10497, retail: 12497, adCap: 100_000, minRev: 2_000_000, maxRev: 2_999_999 },
  { tier: 'Platinum',   name: 'Full Service Marketing — Platinum',   bundled: 15997, retail: 18997, adCap: 150_000, minRev: 3_000_000, maxRev: Infinity },
];
const TIER_BY_NAME = Object.fromEntries(MARKETING_TIERS.map(t => [t.tier.toLowerCase(), t]));

// Coaching (non-marketing) stand-alone prices for savings calculation
const COACHING_RETAIL = {
  'Elite Coach':     3497,
  'Elite Coach Plus': 3497,
  "Master's Circle": 4997,
  'FCOO Advisor':    3797,
  'FCOO Director':   5797,
};

// Conservative ad spend floors by practice area keyword ($/mo)
const AD_SPEND_FLOORS = [
  { keywords: ['mva', 'motor vehicle', 'car accident', 'auto accident'],             floor: 10_000 },
  { keywords: ['personal injury', 'accident & injury', 'wrongful death', 'truck'],   floor: 7_500  },
  { keywords: ['criminal defense', 'criminal law', 'dui', 'dwi'],                    floor: 5_500  },
  { keywords: ['family law', 'divorce', 'custody'],                                  floor: 3_500  },
  { keywords: ['estate planning', 'wills', 'trusts', 'elder law', 'probate'],        floor: 3_500  },
  { keywords: ['immigration'],                                                        floor: 3_000  },
  { keywords: ['business law', 'business litigation', 'corporate'],                  floor: 3_500  },
  { keywords: ['bankruptcy'],                                                         floor: 4_500  },
];

// ─── HubSpot revenue lookup ───────────────────────────────────────────────────

/**
 * Parse a HubSpot text revenue range (e.g. "$961K - $3M", "$81K-$250K") into
 * { min, max, mid }. Returns null if unparseable.
 */
function parseRevenueRange(text) {
  if (!text || typeof text !== 'string') return null;
  const re = /\$([0-9,]+(?:\.[0-9]+)?)\s*(K|M|B|k|m|b)?/gi;
  const amounts = [];
  let m;
  while ((m = re.exec(text)) !== null) {
    let n = parseFloat(m[1].replace(/,/g, ''));
    const s = (m[2] || '').toUpperCase();
    if (s === 'K') n *= 1_000;
    if (s === 'M') n *= 1_000_000;
    if (s === 'B') n *= 1_000_000_000;
    if (!isNaN(n) && n > 0) amounts.push(n);
  }
  if (!amounts.length) return null;
  const min = Math.min(...amounts);
  const max = Math.max(...amounts);
  return { min, max, mid: (min + max) / 2 };
}

/**
 * Query HubSpot for revenue-related contact fields.
 * Returns { value, source, confidence, rawLabel } or null.
 *
 * Field priority:
 *   1. annual_law_firm_revenue — e.g. "$961K - $3M"
 *   2. how_much_revenue_is_your_law_firm_currently_generating_per_month × 12
 *   3. n2024_annual_revenue
 *   4. total_annual_revenue_last_year
 */
async function fetchHubSpotRevenue(contactId) {
  const HUBSPOT_TOKEN = process.env.HUBSPOT_TOKEN;
  if (!HUBSPOT_TOKEN || !contactId) return null;

  const fields = [
    'annual_law_firm_revenue',
    'how_much_revenue_is_your_law_firm_currently_generating_per_month',
    'n2024_annual_revenue',
    'total_annual_revenue_last_year',
  ].join(',');

  let res;
  try {
    res = await fetch(
      `https://api.hubapi.com/crm/v3/objects/contacts/${contactId}?properties=${fields}`,
      { headers: { 'Authorization': `Bearer ${HUBSPOT_TOKEN}`, 'Content-Type': 'application/json' } }
    );
  } catch (err) {
    console.warn(`  HubSpot revenue lookup failed: ${err.message}`);
    return null;
  }
  if (!res.ok) {
    console.warn(`  HubSpot revenue lookup returned ${res.status} for contact ${contactId}`);
    return null;
  }

  const props = (await res.json()).properties || {};

  const annual = parseRevenueRange(props.annual_law_firm_revenue);
  if (annual) return { value: annual.mid, source: 'hubspot_annual_law_firm_revenue', confidence: annual.max / annual.min > 5 ? 'low' : 'medium', rawLabel: props.annual_law_firm_revenue };

  const monthly = parseRevenueRange(props.how_much_revenue_is_your_law_firm_currently_generating_per_month);
  if (monthly) return { value: monthly.mid * 12, source: 'hubspot_monthly_annualized', confidence: 'medium', rawLabel: `${props.how_much_revenue_is_your_law_firm_currently_generating_per_month} (×12)` };

  const rev2024 = parseRevenueRange(props.n2024_annual_revenue);
  if (rev2024) return { value: rev2024.mid, source: 'hubspot_2024_annual_revenue', confidence: 'medium', rawLabel: props.n2024_annual_revenue };

  const lastYear = parseRevenueRange(props.total_annual_revenue_last_year);
  if (lastYear) return { value: lastYear.mid, source: 'hubspot_total_revenue_last_year', confidence: 'medium', rawLabel: props.total_annual_revenue_last_year };

  console.log(`  HubSpot: no parseable revenue fields for contact ${contactId}`);
  return null;
}

// ─── Parsing helpers ──────────────────────────────────────────────────────────

function parseRevenue(text) {
  const patterns = [
    /annual revenue[:\s]+\$?([\d,\.]+)\s*(million|M)\b/i,
    /annual revenue[:\s]+\$?([\d,\.]+)\s*([Kk])\b/i,
    /annual revenue[:\s]+\$?([\d,\.]+)/i,
    /revenue[:\s]+approximately\s+\$?([\d,\.]+)\s*(million|M|K)?\b/i,
    /current revenue[:\s]+\$?([\d,\.]+)\s*(million|M)\b/i,
    /current revenue[:\s]+\$?([\d,\.]+)/i,
    /gross revenue[:\s]+\$?([\d,\.]+)\s*(million|M)\b/i,
    /gross revenue[:\s]+\$?([\d,\.]+)/i,
    /revenue[:\s]+\$?([\d,\.]+)\s*(million|M)\b/i,
  ];
  for (const pattern of patterns) {
    const m = text.match(pattern);
    if (!m) continue;
    const raw = parseFloat(m[1].replace(/,/g, ''));
    if (isNaN(raw) || raw <= 0) continue;
    const suffix = (m[2] || '').toLowerCase();
    if (suffix === 'million' || suffix === 'm') return raw * 1_000_000;
    if (suffix === 'k') return raw * 1_000;
    // Bare number: if it looks like a thousands-shortened form (e.g. "800") skip;
    // only trust bare numbers with >= 6 digits or explicit dollar signs nearby
    if (raw >= 100_000) return raw;
  }
  return null;
}

function parsePracticeAreas(text) {
  const areas = new Set();
  // "Practice areas confirmed: X, Y, Z"
  const confirmedMatch = text.match(/practice areas?\s+confirmed[:\s]+([^\n\r]{3,120})/i);
  if (confirmedMatch) {
    confirmedMatch[1].split(/[,;\/]/).forEach(s => areas.add(s.trim().toLowerCase()));
  }
  // "PRACTICE AREA N: ..."
  for (const m of text.matchAll(/PRACTICE AREA \d+[:\s]+([^\n\r]+)/gi)) {
    areas.add(m[1].trim().toLowerCase());
  }
  // "Practice areas listed: ..."
  const listedMatch = text.match(/practice areas?\s+listed[:\s]+([^\n\r]{3,120})/i);
  if (listedMatch) {
    listedMatch[1].split(/[,;\/]/).forEach(s => areas.add(s.trim().toLowerCase()));
  }
  return [...areas].filter(Boolean);
}

function parseTeamSize(text) {
  if (/team size[:\s]+(solo practitioner|sole practitioner)/i.test(text)) return 1;
  const patterns = [
    /team size[:\s]+(\d+)\s*(employee|attorney|staff|team member|people)/i,
    /(\d+)\s*(employees|staff members|team members|attorneys)\s+confirmed/i,
    /total\s+(employees|staff|team)[:\s]+(\d+)/i,
  ];
  for (const p of patterns) {
    const m = text.match(p);
    if (m) {
      const n = parseInt(m[1] === undefined ? m[2] : m[1]);
      if (!isNaN(n) && n > 0) return n;
    }
  }
  return null;
}

function hasDedicatedOps(text) {
  return /intake coordinator|office manager|operations manager|marketing (manager|director|coordinator)|dedicated (ops|operations|intake|marketing)\s+(staff|team)/i.test(text);
}

function detectPI(practiceAreas) {
  return practiceAreas.some(a => /personal injury|car accident|auto accident|mva|motor vehicle|truck accident|wrongful death|catastrophic injury|brain injury|tbi|slip and fall|premise|dog bite/i.test(a));
}

function detectCriminalDefense(practiceAreas) {
  return practiceAreas.some(a => /criminal defense|criminal law|dui|dwi|drug offense|felony|misdemeanor/i.test(a));
}

function detectHighCompetitiveness(text) {
  const highMetroPattern = /\b(new york city|los angeles|chicago|houston|dallas|atlanta|philadelphia|washington dc|miami|boston|phoenix|seattle|detroit|san francisco|tampa|minneapolis|denver|san diego|orlando)\b/i;
  return highMetroPattern.test(text) && /high.{0,30}competi|competi.{0,30}high/i.test(text);
}

// ─── Package selection ────────────────────────────────────────────────────────

function selectMarketingTier(revenue, effectiveRevenue, practiceAreas, text, notes) {
  const piDetected = detectPI(practiceAreas);
  const cdDetected = detectCriminalDefense(practiceAreas);
  const cdHighComp  = cdDetected && detectHighCompetitiveness(text);
  const multiPracticeArea = practiceAreas.length > 1;

  let tier;

  if (effectiveRevenue >= 3_000_000) {
    tier = TIER_BY_NAME['platinum'];
    notes.push('Revenue $3M+: Platinum tier.');
  } else if (effectiveRevenue >= 2_000_000) {
    tier = TIER_BY_NAME['dominate'];
    notes.push('Revenue $2M–$3M: Dominate tier.');
  } else if (effectiveRevenue >= 1_000_000) {
    tier = TIER_BY_NAME['growth'];
    notes.push('Revenue $1M–$2M: Growth tier.');
  } else if (effectiveRevenue < 750_000 && !multiPracticeArea) {
    tier = TIER_BY_NAME['essentials'];
    notes.push('Revenue under $750K, single practice area detected: Essentials tier. Essentials also requires a single location — confirm with sales rep before finalizing.');
  } else {
    tier = TIER_BY_NAME['starter'];
    notes.push(effectiveRevenue < 750_000
      ? 'Revenue under $750K but multiple practice areas detected: Essentials hidden (requires single practice area) — Starter tier.'
      : 'Revenue $500K–$1M: Starter tier.');
  }

  // Eligibility overrides
  if (piDetected && tier.tier === 'Essentials') {
    tier = TIER_BY_NAME['starter'];
    notes.push('PI practice: Essentials hidden — upgraded to Starter.');
  }
  if (cdHighComp && tier.tier === 'Essentials') {
    tier = TIER_BY_NAME['starter'];
    notes.push('Criminal Defense in high-competition market: Essentials hidden — upgraded to Starter.');
  }

  return tier;
}

function selectCoachingTier(revenue, effectiveRevenue, teamSize, effectiveTeam, text, notes) {
  const fcooEligible = effectiveRevenue >= 500_000;
  const masterCircleEligible = effectiveRevenue >= 1_000_000 && effectiveTeam >= 5;
  const hasOps = hasDedicatedOps(text);

  if (effectiveRevenue < 250_000) {
    notes.push('Revenue under $250K: Elite Coach selected, scoping approval required.');
    return { name: 'Elite Coach', bundled: 2600, retail: COACHING_RETAIL['Elite Coach'] };
  }

  if (effectiveRevenue < 400_000) {
    notes.push('Revenue $250K–$400K: Elite Coach selected.');
    return { name: 'Elite Coach', bundled: 2600, retail: COACHING_RETAIL['Elite Coach'] };
  }

  if (effectiveRevenue < 1_000_000) {
    if (fcooEligible && effectiveTeam >= 3 && hasOps) {
      notes.push('Revenue $500K–$1M with growing team and dedicated ops: Elite Coach Plus + FCOO Advisor considered. Defaulting to Elite Coach Plus — confirm with sales rep if FCOO is appropriate.');
    }
    notes.push('Revenue $400K–$1M: Elite Coach Plus selected.');
    return { name: 'Elite Coach Plus', bundled: 3200, retail: COACHING_RETAIL['Elite Coach Plus'] };
  }

  // $1M+
  if (masterCircleEligible && hasOps) {
    if (effectiveRevenue >= 3_000_000) {
      notes.push(`Revenue $3M+, team ${effectiveTeam}+: Master's Circle + FCOO Partner selected.`);
      return { name: "Master's Circle + FCOO Partner", bundled: 12394, retail: null };
    }
    if (effectiveRevenue >= 2_000_000) {
      notes.push(`Revenue $2M+, team ${effectiveTeam}+, dedicated ops: Master's Circle + FCOO Director selected.`);
      return { name: "Master's Circle + FCOO Director", bundled: 8394, retail: null };
    }
    notes.push(`Revenue $1M+, team ${effectiveTeam}+, dedicated ops: Master's Circle selected.`);
    return { name: "Master's Circle", bundled: 4600, retail: COACHING_RETAIL["Master's Circle"] };
  }

  if (masterCircleEligible && !hasOps) {
    notes.push(`Revenue $1M+, team ${effectiveTeam}+ but no dedicated ops detected: Master's Circle selected. Verify ops capacity with sales rep.`);
    return { name: "Master's Circle", bundled: 4600, retail: COACHING_RETAIL["Master's Circle"] };
  }

  if (effectiveRevenue >= 1_000_000 && effectiveTeam < 5) {
    notes.push(`Revenue $1M+, team under 5: Elite Coach Plus selected (Master's Circle requires 5+ team).`);
    return { name: 'Elite Coach Plus', bundled: 3200, retail: COACHING_RETAIL['Elite Coach Plus'] };
  }

  notes.push('Fallback: Elite Coach Plus selected.');
  return { name: 'Elite Coach Plus', bundled: 3200, retail: COACHING_RETAIL['Elite Coach Plus'] };
}

function estimateAdSpend(practiceAreas, marketingTier) {
  let floor = 3_000;
  for (const area of practiceAreas) {
    for (const entry of AD_SPEND_FLOORS) {
      if (entry.keywords.some(k => area.includes(k))) {
        floor = Math.max(floor, entry.floor);
      }
    }
  }
  const ceiling = Math.min(marketingTier.adCap, floor * 4);
  return { conservative: floor, aggressive: ceiling };
}

// ─── Revenue estimation when not stated ──────────────────────────────────────

function estimateRevenueFromTeamSize(teamSize, notes) {
  // Rough heuristic: $100K–$150K per attorney/staff member in a typical law firm
  if (teamSize === 1) {
    notes.push('Revenue not stated. Solo practitioner — estimating ~$300K (medium-low confidence).');
    return { estimate: 300_000, confidence: 'low' };
  }
  if (teamSize <= 3) {
    notes.push(`Revenue not stated. ${teamSize}-person team — estimating ~$600K (low confidence).`);
    return { estimate: 600_000, confidence: 'low' };
  }
  if (teamSize <= 6) {
    notes.push(`Revenue not stated. ${teamSize}-person team — estimating ~$900K (low confidence).`);
    return { estimate: 900_000, confidence: 'low' };
  }
  if (teamSize <= 12) {
    notes.push(`Revenue not stated. ${teamSize}-person team — estimating ~$1.5M (low confidence).`);
    return { estimate: 1_500_000, confidence: 'low' };
  }
  notes.push(`Revenue not stated. ${teamSize}+ person team — estimating ~$2.5M (low confidence).`);
  return { estimate: 2_500_000, confidence: 'low' };
}

// ─── Main ─────────────────────────────────────────────────────────────────────
// Top-level async wrapper so we can await HubSpot fetch

(async () => {
const friendlyName = process.argv[2];
if (!friendlyName) {
  console.error('Usage: node scripts/select-package.mjs <friendly-name>');
  process.exit(1);
}

if (!existsSync(friendlyName)) {
  console.error(`ERROR: Firm directory not found: ${friendlyName}/`);
  process.exit(1);
}

// If trigger file has an explicit package override, skip — PACKAGE_HINT handles it
const triggerPath = `triggers/audit-research/${friendlyName}.json`;
let hubspotContactId = null;
if (existsSync(triggerPath)) {
  try {
    const trigger = JSON.parse(readFileSync(triggerPath, 'utf8'));
    if (trigger.package && trigger.package.trim()) {
      console.log(`Trigger file has explicit package override: "${trigger.package}"`);
      console.log('Skipping deterministic selection — PACKAGE_HINT will be used in Pass 2.');
      process.exit(0);
    }
    hubspotContactId = trigger.hubspot_contact_id || null;
  } catch { /* non-fatal */ }
}

// Find research notes
const researchFiles = readdirSync(friendlyName).filter(f => f.endsWith('_Research_Notes.txt'));
if (researchFiles.length === 0) {
  console.error(`ERROR: No *_Research_Notes.txt found in ${friendlyName}/ — Pass 1 may not have completed.`);
  process.exit(1);
}
const notesPath = join(friendlyName, researchFiles[0]);
const text = readFileSync(notesPath, 'utf8');
console.log(`Reading: ${notesPath}`);

const notes = [];

// Parse signals
const revenueStated  = parseRevenue(text);
const practiceAreas  = parsePracticeAreas(text);
const teamSizeStated = parseTeamSize(text);

console.log(`  Revenue stated:  ${revenueStated != null ? '$' + revenueStated.toLocaleString() : 'NOT STATED'}`);
console.log(`  Team size:       ${teamSizeStated ?? 'NOT STATED'}`);
console.log(`  Practice areas:  ${practiceAreas.join(' | ') || 'none detected'}`);

// Determine effective values (stated or estimated)
// Revenue hierarchy: research notes → HubSpot contact fields → team size estimate
let confidence = 'high';
let effectiveRevenue = revenueStated;
let revenueSource = revenueStated != null ? 'research_notes' : null;
let revenueLabel  = null;
let effectiveTeam = teamSizeStated ?? 3;

if (revenueStated === null) {
  // Fallback 1: HubSpot contact revenue fields
  const hsRevenue = await fetchHubSpotRevenue(hubspotContactId);
  if (hsRevenue) {
    effectiveRevenue = hsRevenue.value;
    revenueSource    = hsRevenue.source;
    revenueLabel     = hsRevenue.rawLabel;
    confidence       = hsRevenue.confidence;
    notes.push(`Revenue not in research notes — sourced from HubSpot (${hsRevenue.source}): "${hsRevenue.rawLabel}" → $${hsRevenue.value.toLocaleString()}`);
    console.log(`  HubSpot revenue: ${hsRevenue.rawLabel} → $${hsRevenue.value.toLocaleString()} (${hsRevenue.confidence})`);
  } else if (teamSizeStated !== null) {
    // Fallback 2: team size estimate
    const est = estimateRevenueFromTeamSize(teamSizeStated, notes);
    effectiveRevenue = est.estimate;
    revenueSource    = 'team_size_estimate';
    confidence       = 'medium';
  } else {
    notes.push('Revenue and team size both unknown — using conservative defaults. Review with sales rep.');
    effectiveRevenue = 500_000;
    revenueSource    = 'default';
    confidence       = 'low';
  }
}

if (teamSizeStated === null) {
  notes.push('Team size not stated in research notes — defaulting to 3. Review for coaching tier accuracy.');
}

// Select packages
const marketing = selectMarketingTier(revenueStated, effectiveRevenue, practiceAreas, text, notes);
const coaching  = selectCoachingTier(revenueStated, effectiveRevenue, teamSizeStated, effectiveTeam, text, notes);
const adSpend   = estimateAdSpend(practiceAreas, marketing);

// Calculate totals and savings
const totalBundled = marketing.bundled + coaching.bundled;
const mktSavings   = marketing.retail != null ? marketing.retail - marketing.bundled : null;
const cchSavings   = coaching.retail  != null ? coaching.retail  - coaching.bundled  : null;
const totalSavings = (mktSavings ?? 0) + (cchSavings ?? 0);

const decision = {
  confidence,
  revenue_stated:          revenueStated,
  revenue_effective:       effectiveRevenue,
  revenue_source:          revenueSource,
  revenue_label:           revenueLabel,
  team_size_stated:        teamSizeStated,
  team_size_effective:     effectiveTeam,
  practice_areas_detected: practiceAreas,

  marketing_tier:          marketing.tier,
  marketing_name:          marketing.name,
  marketing_price_bundled: marketing.bundled,
  marketing_price_retail:  marketing.retail,
  marketing_savings:       mktSavings,

  coaching_name:           coaching.name,
  coaching_price_bundled:  coaching.bundled,
  coaching_price_retail:   coaching.retail,
  coaching_savings:        cchSavings,

  law_tier:                null,

  total_bundled:           totalBundled,
  total_savings:           totalSavings > 0 ? totalSavings : null,

  ad_spend_conservative:   adSpend.conservative,
  ad_spend_aggressive:     adSpend.aggressive,

  selection_notes: notes,
};

const outputPath = join(friendlyName, 'package_decision.json');
writeFileSync(outputPath, JSON.stringify(decision, null, 2));

console.log(`\nPackage decision → ${outputPath}`);
console.log(`  Marketing:  ${marketing.name} — $${marketing.bundled.toLocaleString()}/mo`);
console.log(`  Coaching:   ${coaching.name} — $${coaching.bundled.toLocaleString()}/mo`);
console.log(`  Total:      $${totalBundled.toLocaleString()}/mo`);
console.log(`  Ad spend:   $${adSpend.conservative.toLocaleString()}–$${adSpend.aggressive.toLocaleString()}/mo`);
console.log(`  Confidence: ${confidence}`);
if (notes.length) {
  console.log(`  Notes:`);
  notes.forEach(n => console.log(`    - ${n}`));
}
})().catch(err => {
  console.error(`select-package.mjs error: ${err.message}`);
  process.exit(0); // non-fatal — Pass 2 falls back to PACKAGE_HINT
});
