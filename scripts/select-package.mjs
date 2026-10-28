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
 * judgment from the pricing decision. Prices and the bundle rule live in
 * scripts/lib/pricing.mjs.
 *
 * Exit codes:
 *   0 — decision written (or skipped because the trigger's package override
 *       names a product the catalog doesn't know — Pass 2 uses the override text)
 *   1 — fatal error (no research notes, bad args)
 */

import { readFileSync, writeFileSync, readdirSync, existsSync, statSync } from 'fs';
import { join } from 'path';
import { execFileSync } from 'child_process';
import { pathToFileURL } from 'url';
import { getProduct, resolveName, unretire, pricePackage, applyPricing } from './lib/pricing.mjs';

// ─── Selection tables ────────────────────────────────────────────────────────
// Revenue bands and ad-spend caps per marketing tier. Prices come from
// scripts/lib/pricing.mjs. Caps match audit-write.md (Essentials $7,500,
// Full Service Starter $25,000).

const MARKETING_TIERS = [
  { tier: 'Essentials', adCap: 7_500,   minRev: 0,         maxRev: 749_999 },
  { tier: 'Starter',    adCap: 25_000,  minRev: 500_000,   maxRev: 999_999 },
  { tier: 'Growth',     adCap: 50_000,  minRev: 1_000_000, maxRev: 1_999_999 },
  { tier: 'Dominate',   adCap: 100_000, minRev: 2_000_000, maxRev: 2_999_999 },
  { tier: 'Platinum',   adCap: 150_000, minRev: 3_000_000, maxRev: Infinity },
].map(t => ({ ...t, name: `Full Service Marketing — ${t.tier}` }));
const TIER_BY_NAME = Object.fromEntries(MARKETING_TIERS.map(t => [t.tier.toLowerCase(), t]));

// Shorthand reps use on calls → catalog name. Keep in sync with the
// "Products discussed on call" alias table in .claude/commands/audit-research.md
// and the change-bot prompts in .github/workflows/slack-*.yml.
// Order matters: more specific names first, so "AI Workforce Pro – Starter"
// is matched before plain "AI Workforce Pro", and "FCOO Director" before "FCOO".
// A tier followed by "/" ("FCOO Advisor / Director / Partner") is a list of
// options, not a choice, so it falls through to the generic name.
const AIWP_UNSPECIFIED = 'AI Workforce Pro (tier not specified)';
const NOT_A_LIST = '(?!\\s*\\/)';
const PRODUCT_ALIASES = [
  { name: 'AI Workforce Pro – Starter', pattern: /ai workforce pro\s*[–—-]\s*starter|aiwp\s*starter|ai essentials\s*[–—-]?\s*starter/i },
  // Bare "AIWP" / "AI Workforce Pro" doesn't say which tier — resolved by team size in selectLawTier.
  { name: 'AI Workforce Pro',           pattern: /ai workforce pro\s*[–—(-]?\s*base\)?|aiwp\s*base|ai essentials\s*[–—-]?\s*base/i },
  { name: AIWP_UNSPECIFIED,             pattern: /ai workforce pro|\baiwp\b/i },
  { name: 'Fractional CTO Level 3',     pattern: /(fractional cto|fcto)\s*(level|l)\s*3|ai enterprise/i },
  { name: 'Fractional CTO Level 2',     pattern: /(fractional cto|fcto)\s*(level|l)\s*2|ai accelerator\s*l2/i },
  { name: 'Fractional CTO Level 1',     pattern: /(fractional cto|fcto)\s*(level|l)\s*1|ai accelerator\s*l1/i },
  { name: 'Elite Coach Plus',           pattern: /elite coach plus/i },
  { name: 'Elite Coach',                pattern: /elite coach(?!\s*plus)/i },
  { name: 'Coach Essentials Plus',      pattern: /coach essentials plus/i },
  { name: 'Coach Essentials',           pattern: /coach essentials(?!\s*plus)/i },
  { name: "Master's Circle",            pattern: /master'?s circle|\bmc\b/i },
  { name: 'FCOO Advisor',               pattern: new RegExp(`(?:\\bfcoo|fractional coo)\\s*advisor${NOT_A_LIST}`, 'i') },
  { name: 'FCOO Director',              pattern: new RegExp(`(?:\\bfcoo|fractional coo)\\s*director${NOT_A_LIST}`, 'i') },
  { name: 'FCOO Partner',               pattern: new RegExp(`(?:\\bfcoo|fractional coo)\\s*partner${NOT_A_LIST}`, 'i') },
  { name: 'FCOO',                       pattern: /\bfcoo\b|fractional coo/i },
  { name: 'FCFO Advisor',               pattern: new RegExp(`(?:\\bfcfo|fractional cfo)\\s*advisor${NOT_A_LIST}`, 'i') },
  { name: 'FCFO Director',              pattern: new RegExp(`(?:\\bfcfo|fractional cfo)\\s*director${NOT_A_LIST}`, 'i') },
  { name: 'FCFO Partner',               pattern: new RegExp(`(?:\\bfcfo|fractional cfo)\\s*partner${NOT_A_LIST}`, 'i') },
  { name: 'FCFO',                       pattern: /\bfcfo\b|fractional cfo/i },
  { name: 'Full Service Marketing',     pattern: /full service marketing/i },
];
const COACHING_PRODUCTS = new Set([
  'Elite Coach', 'Elite Coach Plus', 'Coach Essentials', 'Coach Essentials Plus', "Master's Circle",
  'FCOO', 'FCOO Advisor', 'FCOO Director', 'FCOO Partner', 'FCFO', 'FCFO Advisor', 'FCFO Director', 'FCFO Partner',
]);
const LAW_PRODUCTS = new Set(['AI Workforce Pro – Starter', 'AI Workforce Pro', 'Fractional CTO Level 1', 'Fractional CTO Level 2', 'Fractional CTO Level 3']);

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

// ─── HubSpot lookups ──────────────────────────────────────────────────────────

/**
 * Parse a HubSpot text revenue range (e.g. "$961K - $3M", "$81K-$250K") into
 * { min, max, mid }. Returns null if unparseable.
 */
export function parseRevenueRange(text) {
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

async function hubspotGet(path) {
  const HUBSPOT_TOKEN = process.env.HUBSPOT_TOKEN;
  if (!HUBSPOT_TOKEN) return null;
  try {
    const res = await fetch(`https://api.hubapi.com${path}`, {
      headers: { 'Authorization': `Bearer ${HUBSPOT_TOKEN}`, 'Content-Type': 'application/json' },
    });
    if (!res.ok) {
      console.warn(`  HubSpot ${path} returned ${res.status}`);
      return null;
    }
    return await res.json();
  } catch (err) {
    console.warn(`  HubSpot ${path} failed: ${err.message}`);
    return null;
  }
}

/**
 * Query HubSpot for revenue-related contact fields.
 * Returns { value, source, confidence, rawLabel, isRange } or null.
 * A range ("$180K - $960K") is a bracket the prospect ticked on a form, not
 * their revenue — the midpoint is used for the draft only and is flagged
 * for the seller to confirm (`isRange`).
 *
 * Field priority:
 *   1. annual_law_firm_revenue — e.g. "$961K - $3M"
 *   2. how_much_revenue_is_your_law_firm_currently_generating_per_month × 12
 *   3. n2024_annual_revenue
 *   4. total_annual_revenue_last_year
 */
export async function fetchHubSpotRevenue(contactId) {
  if (!contactId) return null;
  const fields = [
    'annual_law_firm_revenue',
    'how_much_revenue_is_your_law_firm_currently_generating_per_month',
    'n2024_annual_revenue',
    'total_annual_revenue_last_year',
  ].join(',');
  const json = await hubspotGet(`/crm/v3/objects/contacts/${contactId}?properties=${fields}`);
  if (!json) return null;
  const props = json.properties || {};

  const pick = (range, source, rawLabel, scale = 1) => ({
    value: range.mid * scale,
    source,
    confidence: range.max / range.min > 5 ? 'low' : 'medium',
    rawLabel,
    isRange: range.max > range.min,
  });

  const annual = parseRevenueRange(props.annual_law_firm_revenue);
  if (annual) return pick(annual, 'hubspot_annual_law_firm_revenue', props.annual_law_firm_revenue);

  const monthly = parseRevenueRange(props.how_much_revenue_is_your_law_firm_currently_generating_per_month);
  if (monthly) return pick(monthly, 'hubspot_monthly_annualized', `${props.how_much_revenue_is_your_law_firm_currently_generating_per_month} (×12)`, 12);

  const rev2024 = parseRevenueRange(props.n2024_annual_revenue);
  if (rev2024) return pick(rev2024, 'hubspot_2024_annual_revenue', props.n2024_annual_revenue);

  const lastYear = parseRevenueRange(props.total_annual_revenue_last_year);
  if (lastYear) return pick(lastYear, 'hubspot_total_revenue_last_year', props.total_annual_revenue_last_year);

  console.log(`  HubSpot: no parseable revenue fields for contact ${contactId}`);
  return null;
}

/**
 * The HubSpot company associated with a contact: { id, name, domain, employees }.
 * Used as a team-size fallback and recorded so the Slack post can show the
 * company record's name.
 */
export async function fetchHubSpotCompany(contactId) {
  if (!contactId) return null;
  const assoc = await hubspotGet(`/crm/v4/objects/contacts/${contactId}/associations/companies`);
  const companyId = assoc?.results?.[0]?.toObjectId;
  if (!companyId) return null;
  const json = await hubspotGet(`/crm/v3/objects/companies/${companyId}?properties=name,domain,numberofemployees`);
  if (!json) return null;
  const p = json.properties || {};
  const employees = parseInt(p.numberofemployees, 10);
  return { id: String(companyId), name: p.name || null, domain: p.domain || null, employees: employees > 0 ? employees : null };
}

// ─── Parsing helpers ──────────────────────────────────────────────────────────

// Tolerates a parenthetical qualifier between the label and the colon (e.g.
// "Annual revenue (gross / case value): ...") and stray quote/tilde
// punctuation between the colon and the value (e.g. `: "~$800k"`) — both
// common in the current research-notes template but not matched by a plain
// `label[:\s]+` prefix.
const QUALIFIER = '(?:\\s*\\([^)]*\\))?';
// Also skips a leading year label (e.g. "Annual revenue: 2023 revenue $400k"),
// which would otherwise be read as the amount and rejected as too small.
const PUNCT = '[\\s"‘’\'~]*(?:(?:19|20)\\d\\d\\s+(?:revenue\\s+)?(?:was\\s+|of\\s+)?)?';

// A minority of research notes state the label's figure as a monthly run-rate
// (e.g. "Annual revenue (gross / case value): ~$30K/month...") with the true
// annual figure only appearing later in the sentence. Rather than guess at
// annualizing, treat a number immediately followed by a "/mo"-style marker as
// unusable here and let the caller fall back to other sources — reporting a
// monthly figure as the annual one would be worse than not parsing it at all.
function isMonthlyFigure(text, matchEndIndex) {
  return /^\s*\/?\s*(mo\b|month|monthly)/i.test(text.slice(matchEndIndex, matchEndIndex + 20));
}

// Value of a "- Label: value" line in the research notes. By default includes
// wrapped continuation lines (indented, not starting a new "- " item); pass
// { firstLineOnly: true } to stop at the end of the first line. Null if
// absent or still holding the template's [placeholder].
export function readNoteField(text, label, { firstLineOnly = false } = {}) {
  const re = firstLineOnly
    ? new RegExp(`^\\s*-?\\s*${label}[:\\s]+(.+)`, 'im')
    : new RegExp(`^\\s*-?\\s*${label}[:\\s]+(.+(?:\\n(?!\\s*-\\s)(?!\\s*$)\\s+.+)*)`, 'im');
  const m = text.match(re);
  if (!m) return null;
  const value = m[1].replace(/\s+/g, ' ').trim();
  return value && !value.startsWith('[') ? value : null;
}

const NOT_STATED = /^(?:not stated|not available|unknown|n\/a|none|not given|not disclosed|number not stated)/i;

/**
 * First dollar amount in a free-text revenue value, e.g.
 *   '"north of $300,000" (William, 00:07:15 …'        → 300000
 *   'about $1.2 million [transcript unclear …]'        → 1200000
 *   '"… this year I'm on track to make about 250."'    → 250000
 *   '"1.2" (00:36:20) in answer to …'                  → 1200000
 * Unit-less numbers are read in context: under 50 → millions, 50–999 →
 * thousands (how people say revenue out loud). Timestamps, years and
 * percentages are ignored. Returns null when the value says it wasn't stated.
 */
export function parseMoneyText(value) {
  if (!value || NOT_STATED.test(value.replace(/^["'\s]+/, ''))) return null;
  const cleaned = value
    .replace(/\b\d{1,2}:\d{2}(?::\d{2})?\b/g, ' ')             // timestamps
    .replace(/\b\d+(?:\.\d+)?\s*%/g, ' ')                      // percentages
    .replace(/(?<!\$)\b(?:19|20)\d\d\b(?!\s*(?:k|m|million)\b)/gi, ' '); // years
  // The number must end at a word boundary ("about 250." is fine, "250k" is a unit).
  const re = /(\$\s*)?(\d[\d,]*(?:\.\d+)?)\s*(million|mil|mm|m|k|thousand|billion|b)?(?!\w|\.\d)/gi;
  let m;
  while ((m = re.exec(cleaned)) !== null) {
    const hasDollar = !!m[1];
    const n = parseFloat(m[2].replace(/,/g, ''));
    if (isNaN(n) || n <= 0) continue;
    const unit = (m[3] || '').toLowerCase();
    if (unit === 'million' || unit === 'mil' || unit === 'mm' || unit === 'm') return n * 1_000_000;
    if (unit === 'billion' || unit === 'b') return n * 1_000_000_000;
    if (unit === 'k' || unit === 'thousand') return n * 1_000;
    if (n >= 10_000) return n;
    if (hasDollar && n >= 1_000) return n;
    if (!hasDollar && n < 50) return n * 1_000_000;
    if (!hasDollar && n < 1_000) return n * 1_000;
  }
  if (/\b(?:a|one) million\b/i.test(cleaned)) return 1_000_000;
  return null;
}

export function parseRevenue(text) {
  // Range forms first (e.g. "Annual revenue: $1.5-2M gross", "$1.5–2M"), since a
  // bare-number pattern below would otherwise only catch the first number in the range.
  const rangePatterns = [
    new RegExp(`annual revenue${QUALIFIER}[:\\s]+${PUNCT}\\$?([\\d,\\.]+)\\s*[-–—to]+\\s*\\$?([\\d,\\.]+)\\s*(million|M|[Kk])\\b`, 'i'),
    new RegExp(`revenue${QUALIFIER}[:\\s]+${PUNCT}\\$?([\\d,\\.]+)\\s*[-–—to]+\\s*\\$?([\\d,\\.]+)\\s*(million|M|[Kk])\\b`, 'i'),
  ];
  for (const pattern of rangePatterns) {
    const m = text.match(pattern);
    if (!m) continue;
    if (isMonthlyFigure(text, m.index + m[0].length)) continue;
    const lo = parseFloat(m[1].replace(/,/g, ''));
    const hi = parseFloat(m[2].replace(/,/g, ''));
    if (isNaN(lo) || isNaN(hi) || lo <= 0 || hi <= 0) continue;
    const suffix = m[3].toLowerCase();
    const mult = (suffix === 'million' || suffix === 'm') ? 1_000_000 : 1_000;
    return ((lo + hi) / 2) * mult;
  }

  const patterns = [
    new RegExp(`annual revenue${QUALIFIER}[:\\s]+${PUNCT}\\$?([\\d,\\.]+)\\s*(million|M)\\b`, 'i'),
    new RegExp(`annual revenue${QUALIFIER}[:\\s]+${PUNCT}\\$?([\\d,\\.]+)\\s*([Kk])\\b`, 'i'),
    new RegExp(`annual revenue${QUALIFIER}[:\\s]+${PUNCT}\\$?([\\d,\\.]+)`, 'i'),
    /revenue[:\s]+approximately\s+\$?([\d,\.]+)\s*(million|M|K)?\b/i,
    new RegExp(`current revenue${QUALIFIER}[:\\s]+${PUNCT}\\$?([\\d,\\.]+)\\s*(million|M)\\b`, 'i'),
    new RegExp(`current revenue${QUALIFIER}[:\\s]+${PUNCT}\\$?([\\d,\\.]+)`, 'i'),
    new RegExp(`gross revenue${QUALIFIER}[:\\s]+${PUNCT}\\$?([\\d,\\.]+)\\s*(million|M)\\b`, 'i'),
    new RegExp(`gross revenue${QUALIFIER}[:\\s]+${PUNCT}\\$?([\\d,\\.]+)`, 'i'),
    new RegExp(`revenue${QUALIFIER}[:\\s]+${PUNCT}\\$?([\\d,\\.]+)\\s*(million|M)\\b`, 'i'),
  ];
  for (const pattern of patterns) {
    const m = text.match(pattern);
    if (!m) continue;
    if (isMonthlyFigure(text, m.index + m[0].length)) continue;
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

/**
 * Revenue from the research notes, best source first:
 *   1. "Revenue (annual, best estimate): $NNN" — the machine-read line
 *   2. the fixed-format patterns in parseRevenue()
 *   3. the first amount in the "Annual revenue (gross …)" / "Revenue" line,
 *      read as free text ("north of $300,000", "about $1.2 million")
 * Returns { value, source } or null.
 */
export function parseRevenueFromNotes(text) {
  const structured = readNoteField(text, 'revenue \\(annual, best estimate\\)', { firstLineOnly: true });
  if (structured) {
    const v = parseMoneyText(structured);
    if (v != null) return { value: v, source: 'research_notes' };
  }
  const fixed = parseRevenue(text);
  if (fixed != null) return { value: fixed, source: 'research_notes' };
  // Each label swallows its "(gross / case value)"-style qualifier so the value
  // starts at the actual text ("not stated …" must be seen as not stated).
  for (const label of [`annual revenue(?!\\s*\\(net)${QUALIFIER}`, `current revenue${QUALIFIER}`, `revenue(?!\\s*goal)${QUALIFIER}`]) {
    const v = parseMoneyText(readNoteField(text, label));
    if (v != null && v >= 50_000) return { value: v, source: 'research_notes_text' };
  }
  return null;
}

export function parsePracticeAreas(text) {
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

const NUMBER_WORDS = { one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10, eleven: 11, twelve: 12, thirteen: 13, fourteen: 14, fifteen: 15, sixteen: 16, seventeen: 17, eighteen: 18, nineteen: 19, twenty: 20 };

/**
 * Total headcount from the "Team size:" line value, e.g.
 *   "15 total, 2 lawyers"                    → 15
 *   "3 — Dan (attorney/owner), Shane …"      → 3
 *   "~18 employees" / "13-person firm"       → 18 / 13
 *   "Solo — Andrew Ferrell"                  → 1
 *   "Three people plus outside vendors"      → 3
 *   "per site, 7 attorneys + 9 support staff" → 16
 *   "not stated by the prospect … Website: 7 attorneys" → 7
 */
export function parseTeamSizeValue(value) {
  if (!value) return null;
  const v = value.replace(/^["'\s]+/, '');
  if (/^(?:solo|sole|just me|effectively 1\b)/i.test(v)) return 1;

  const sumPair = s => {
    const m = s.match(/(\d+)\s+[a-z][\w\s-]{0,25}?\+\s*(\d+)/i);
    return m ? parseInt(m[1], 10) + parseInt(m[2], 10) : null;
  };

  if (!NOT_STATED.test(v)) {
    const lead = v.match(/^~?\s*(\d+)(?!\s*[:%])(?:\s*[-–]\s*\d+)?\b/);
    if (lead) {
      // "7 attorneys + 9 support staff" at the start → both groups
      const pair = sumPair(v.slice(0, 60));
      return pair ?? parseInt(lead[1], 10);
    }
    const word = v.match(/^(\w+)\s+(?:people|employees|staff|total|person|team members)\b/i);
    if (word && NUMBER_WORDS[word[1].toLowerCase()]) return NUMBER_WORDS[word[1].toLowerCase()];
    const person = v.match(/\b(\d+)[-\s]person\b/i);
    if (person) return parseInt(person[1], 10);
    const counted = v.match(/^(?:about|approximately|roughly|around)\s+(\d+)\b/i);
    if (counted) return parseInt(counted[1], 10);
  }

  // Not stated by the prospect: fall back to a website count in the same line.
  const site = v.match(/(?:per (?:the )?(?:web)?site|website(?: lists| shows)?)[,:]?\s*([^.;]{0,80})/i);
  if (site) {
    const pair = sumPair(site[1]);
    if (pair) return pair;
    const n = site[1].match(/(\d+)\s+(?:attorneys|lawyers|employees|staff|people)/i);
    if (n) return parseInt(n[1], 10);
  }
  return null;
}

export function parseTeamSize(text) {
  const structured = readNoteField(text, 'team size \\(total headcount\\)', { firstLineOnly: true });
  if (structured) {
    const n = parseTeamSizeValue(structured);
    if (n != null) return n;
  }
  const fromLine = parseTeamSizeValue(readNoteField(text, 'team size', { firstLineOnly: true }));
  if (fromLine != null) return fromLine;

  if (/team size[:\s]+(solo|sole)\s+(practitioner|attorney)/i.test(text)) return 1;
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

/**
 * Read the structured call-focus fields from the research notes
 * (see STEP 9 in .claude/commands/audit-research.md). Each value is null when
 * the notes predate those fields or leave them blank.
 *
 * "Products discussed on call" is read from its first line only — wrapped
 * lines are explanation ("$3,797 is also the FCOO Advisor … price"), and
 * reading them made products appear that nobody discussed.
 */
export function parseCallFocus(text) {
  const engagementRaw = readNoteField(text, 'primary engagement');
  let engagement = null;
  if (engagementRaw) {
    const e = engagementRaw.toLowerCase();
    if (/^mixed/.test(e)) engagement = 'mixed';
    else if (/^(coaching|ops|operations)/.test(e)) engagement = 'coaching/ops';
    else if (/^ai\b/.test(e)) engagement = 'AI';
    else if (/^marketing/.test(e)) engagement = 'marketing';
  }

  const productsRaw = readNoteField(text, 'products discussed on call', { firstLineOnly: true });
  let products = null;
  if (productsRaw) {
    products = [];
    if (!/^none\b/i.test(productsRaw)) {
      // Parenthetical asides on the same line are explanation, not products.
      let rest = productsRaw.replace(/\([^)]*\)/g, ' ');
      for (const { name, pattern } of PRODUCT_ALIASES) {
        const g = new RegExp(pattern.source, 'gi');
        if (g.test(rest)) {
          if (!products.includes(name)) products.push(name);
          rest = rest.replace(g, ' ');
        }
      }
    }
  }

  const gapRaw = readNoteField(text, 'lead-gen gap stated');
  const leadGenGap = gapRaw == null ? null : /^yes\b/i.test(gapRaw) ? true : /^no\b/i.test(gapRaw) ? false : null;

  return { engagement, products, productsRaw, leadGenGap };
}

/**
 * The AI line: at most one Fractional CTO level and one AI Workforce Pro tier.
 * Returns { name, seats } (name may be "Fractional CTO Level 1 + AI Workforce Pro – Starter") or null.
 */
export function selectLawTier(products, effectiveRevenue, teamSizeStated, notes) {
  // "AIWP" alone: Starter for 1–4 users (or unknown team size), base for 5+.
  const resolved = [...new Set((products || []).filter(p => LAW_PRODUCTS.has(p) || p === AIWP_UNSPECIFIED).map(p => {
    if (p !== AIWP_UNSPECIFIED) return p;
    const tier = teamSizeStated != null && teamSizeStated >= 5 ? 'AI Workforce Pro' : 'AI Workforce Pro – Starter';
    notes.push(`"AI Workforce Pro" named without a tier — using ${tier} (${teamSizeStated == null ? 'team size not stated' : `team of ${teamSizeStated}`}).`);
    return tier;
  }))];
  if (!resolved.length) return null;

  const parts = [];

  // Fractional CTO: if several levels were named, take the highest one the firm qualifies for.
  const fcto = resolved.filter(p => p.startsWith('Fractional CTO')).sort().reverse();
  if (fcto.length) {
    const eligible = fcto.filter(p => effectiveRevenue >= getProduct(p).minRev);
    if (eligible.length) {
      parts.push(eligible[0]);
      if (fcto.length > 1) notes.push(`Several Fractional CTO levels discussed (${fcto.join(', ')}) — using ${eligible[0]}, the highest the firm's revenue qualifies for; confirm with sales rep.`);
    } else {
      const lowest = fcto[fcto.length - 1];
      notes.push(`${lowest} discussed on call but revenue ($${effectiveRevenue.toLocaleString()}) is under its $${getProduct(lowest).minRev.toLocaleString()} floor — not included. Confirm with sales rep.`);
    }
  }

  const aiwp = resolved.filter(p => p.startsWith('AI Workforce Pro'));
  let seats = null;
  if (aiwp.length) {
    if (aiwp.length > 1) notes.push(`Both AI Workforce Pro tiers discussed — using ${aiwp[0]}; confirm with sales rep.`);
    const p = getProduct(aiwp[0]);
    parts.push(p.name);
    if (p.perUser) {
      seats = Math.min(Math.max(teamSizeStated ?? 1, 1), p.maxUsers);
      notes.push(`${p.name} discussed on call: ${seats} seat${seats > 1 ? 's' : ''} × $${p.perUser}/mo` +
        (teamSizeStated == null ? ' (team size not stated — 1 seat assumed; confirm seat count).' : '.'));
      if (teamSizeStated != null && teamSizeStated > p.maxUsers) {
        notes.push(`Team of ${teamSizeStated} is over Starter's ${p.maxUsers}-user limit — consider AI Workforce Pro (5+ users).`);
      }
    } else {
      seats = Math.max(teamSizeStated ?? p.baseUsers, p.baseUsers);
      notes.push(`${p.name} discussed on call: $${p.base.toLocaleString()}/mo for ${p.baseUsers} users` +
        (seats > p.baseUsers ? ` + ${seats - p.baseUsers} extra × $${p.perExtraUser}.` : '.'));
    }
  }

  return parts.length ? { name: parts.join(' + '), seats } : null;
}

function hasDedicatedOps(text) {
  return /intake coordinator|office manager|operations manager|marketing (manager|director|coordinator)|dedicated (ops|operations|intake|marketing)\s+(staff|team)/i.test(text);
}

function detectPI(practiceAreas) {
  return practiceAreas.some(a => /personal injury|car accident|auto accident|mva|motor vehicle|truck accident|wrongful death|catastrophic injury|brain injury|tbi|slip and fall|premise|dog bite/i.test(a));
}

// Practices commonly billed on contingency, where "revenue" in a research note
// is often the gross case value rather than the fee actually collected.
function detectContingencyPractice(practiceAreas) {
  return practiceAreas.some(a => /personal injury|car accident|auto accident|mva|motor vehicle|truck accident|wrongful death|catastrophic injury|brain injury|tbi|slip and fall|premise|dog bite|mass tort|workers[' ]?comp|medical malpractice|product liability/i.test(a));
}

/**
 * Parse a net/collected/take-home revenue figure, distinct from gross revenue.
 * Contingency-fee practices frequently state both in the same breath
 * (e.g. "$1.5-2M gross / ~$500k net") — the net figure is what the firm
 * actually collects and is the correct basis for package tiering.
 */
function parseNetRevenue(text) {
  const patterns = [
    /\$?([\d,\.]+)\s*(million|M|k|K)?\s*net\b/i,
    /net\s+revenue[:\s]+\$?([\d,\.]+)\s*(million|M|k|K)?/i,
    /take[- ]home[:\s]+\$?([\d,\.]+)\s*(million|M|k|K)?/i,
    /collected(?:\s+revenue)?[:\s]+\$?([\d,\.]+)\s*(million|M|k|K)?/i,
    /net of contingency[:\s]+\$?([\d,\.]+)\s*(million|M|k|K)?/i,
  ];
  for (const pattern of patterns) {
    const m = text.match(pattern);
    if (!m) continue;
    const raw = parseFloat(m[1].replace(/,/g, ''));
    if (isNaN(raw) || raw <= 0) continue;
    const suffix = (m[2] || '').toLowerCase();
    if (suffix === 'million' || suffix === 'm') return raw * 1_000_000;
    if (suffix === 'k') return raw * 1_000;
    if (raw >= 100_000) return raw;
  }
  return null;
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

/** Coaching by revenue and team size alone. Returns { name }. */
function selectCoachingByRevenue(effectiveRevenue, effectiveTeam, text, notes) {
  const fcooEligible = effectiveRevenue >= 500_000;
  const masterCircleEligible = effectiveRevenue >= 1_000_000 && effectiveTeam >= 5;
  const hasOps = hasDedicatedOps(text);

  if (effectiveRevenue < 250_000) {
    notes.push('Revenue under $250K: Elite Coach selected, scoping approval required.');
    return { name: 'Elite Coach' };
  }

  if (effectiveRevenue < 400_000) {
    notes.push('Revenue $250K–$400K: Elite Coach selected.');
    return { name: 'Elite Coach' };
  }

  if (effectiveRevenue < 1_000_000) {
    if (fcooEligible && effectiveTeam >= 3 && hasOps) {
      notes.push('Revenue $500K–$1M with growing team and dedicated ops: Elite Coach Plus + FCOO Advisor considered. Defaulting to Elite Coach Plus — confirm with sales rep if FCOO is appropriate.');
    }
    notes.push('Revenue $400K–$1M: Elite Coach Plus selected.');
    return { name: 'Elite Coach Plus' };
  }

  // $1M+ (FCOO Partner is retired, so $3M+ firms get the Director pairing)
  if (masterCircleEligible && hasOps) {
    if (effectiveRevenue >= 2_000_000) {
      notes.push(`Revenue $2M+, team ${effectiveTeam}+, dedicated ops: Master's Circle + FCOO Director selected.`);
      return { name: "Master's Circle + FCOO Director" };
    }
    notes.push(`Revenue $1M+, team ${effectiveTeam}+, dedicated ops: Master's Circle selected.`);
    return { name: "Master's Circle" };
  }

  if (masterCircleEligible && !hasOps) {
    notes.push(`Revenue $1M+, team ${effectiveTeam}+ but no dedicated ops detected: Master's Circle selected. Verify ops capacity with sales rep.`);
    return { name: "Master's Circle" };
  }

  if (effectiveRevenue >= 1_000_000 && effectiveTeam < 5) {
    notes.push(`Revenue $1M+, team under 5: Elite Coach Plus selected (Master's Circle requires 5+ team).`);
    return { name: 'Elite Coach Plus' };
  }

  notes.push('Fallback: Elite Coach Plus selected.');
  return { name: 'Elite Coach Plus' };
}

/**
 * Coaching named on the call. What was discussed wins over the revenue rule
 * (Vanessa, Oct 2026: "Prioritize the product explicitly discussed on the call
 * and flag it for rep confirmation"). FCOO/FCFO named without a tier: Advisor
 * under $2M, Director at $2M+. Returns { name } or null when none was named.
 */
export function selectDiscussedCoaching(products, effectiveRevenue, notes) {
  const discussed = (products || []).filter(p => COACHING_PRODUCTS.has(p));
  if (!discussed.length) return null;

  const tierFor = family => {
    const named = discussed.find(p => p.startsWith(`${family} `));
    if (named) {
      const { product, retiredFrom } = unretire(getProduct(named));
      if (retiredFrom) notes.push(`${retiredFrom} is retired — using ${product.name}.`);
      return product.name;
    }
    return effectiveRevenue >= 2_000_000 ? `${family} Director` : `${family} Advisor`;
  };

  const picks = [];
  const has = name => discussed.includes(name);
  const hasFamily = family => discussed.some(p => p === family || p.startsWith(`${family} `));
  const coach = ["Master's Circle", 'Elite Coach Plus', 'Elite Coach', 'Coach Essentials Plus', 'Coach Essentials'].find(has);
  const fcoo = hasFamily('FCOO') ? tierFor('FCOO') : null;
  const fcfo = hasFamily('FCFO') ? tierFor('FCFO') : null;

  // Sales prices some coaching + FCOO pairs as one package.
  if (coach && fcoo && getProduct(`${coach} + ${fcoo}`)) picks.push(`${coach} + ${fcoo}`);
  else picks.push(...[coach, fcoo].filter(Boolean));
  if (fcfo) picks.push(fcfo);

  const name = picks.join(' + ');
  for (const p of picks.flatMap(x => x.split(' + '))) {
    const min = getProduct(p)?.minRev;
    if (min && effectiveRevenue < min) notes.push(`${p} usually needs $${min.toLocaleString()}+ revenue (using $${effectiveRevenue.toLocaleString()}) — included because it was discussed on the call.`);
  }
  return { name };
}

function estimateAdSpend(practiceAreas, marketingTier) {
  let floor = 3_000;
  let floorBasis = 'no practice area matched a channel-minimum table — default floor';
  for (const area of practiceAreas) {
    for (const entry of AD_SPEND_FLOORS) {
      if (entry.keywords.some(k => area.includes(k)) && entry.floor > floor) {
        floor = entry.floor;
        floorBasis = area;
      }
    }
  }
  const uncappedCeiling = floor * 4;
  const ceiling = Math.min(marketingTier.adCap, uncappedCeiling);
  const aggressiveBasis = ceiling < uncappedCeiling
    ? `capped by ${marketingTier.tier} tier's ad cap`
    : 'scaled 4x off the conservative channel-minimum floor';
  return {
    conservative: floor,
    aggressive: ceiling,
    rationale: { conservative_basis: floorBasis, aggressive_basis: aggressiveBasis },
  };
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

// ─── Research notes file ─────────────────────────────────────────────────────

/**
 * The most recent research notes file in a firm folder. A re-run can leave two
 * (ppd-law, the-fusselman); use the one last committed, falling back to file
 * modification time outside a git checkout.
 */
export function newestResearchNotes(dir) {
  const files = readdirSync(dir).filter(f => f.endsWith('_Research_Notes.txt'));
  if (files.length <= 1) return files[0] ?? null;
  const when = f => {
    try {
      const t = execFileSync('git', ['log', '-1', '--format=%ct', '--', join(dir, f)], { encoding: 'utf8' }).trim();
      if (t) return parseInt(t, 10) * 1000;
    } catch { /* not a git checkout */ }
    return statSync(join(dir, f)).mtimeMs;
  };
  return files.map(f => ({ f, t: when(f) })).sort((a, b) => b.t - a.t || b.f.localeCompare(a.f))[0].f;
}

// ─── Package from a trigger-file override ────────────────────────────────────

/**
 * Turn a seller's package text ("Elite Coach Plus + AI Workforce Pro – Starter")
 * into package lines. Returns null unless every product is in the catalog —
 * free-text overrides ("FSM Starter (opt 1) + FSM Essentials (opt 2)") are left
 * to Pass 2, which reads the override text itself.
 */
export function linesFromOverride(text, teamSizeStated) {
  const lines = { marketing: [], coaching: [], law: [] };
  let seats = null;
  // "AI Workforce Pro – Starter (1 user, $350/mo) only — no marketing, …":
  // instructions after " — " / ". " and asides in parentheses aren't products.
  // Product names contain dashes too ("Full Service Marketing — Starter"), so
  // only cut where a dash starts an instruction.
  const head = text
    .split(/\s[—–-]\s+(?=(?:no|do|don't|with|without|this|use|section)\b)|\.\s|;\s/i)[0]
    .replace(/\bonly\b/gi, ' ');
  for (const part of head.split(/\s\+\s(?![^()]*\))/).map(s => s.trim()).filter(Boolean)) {
    const seatMatch = part.match(/\((\d+)\s*(?:users?|seats?)\b/i);
    const clean = part.replace(/\([^)]*\)/g, ' ').trim();
    const resolved = resolveName(clean);
    if (resolved.length !== 1 || !resolved[0].product) return null;
    const { product } = unretire(resolved[0].product);
    lines[product.category].push(product.name);
    if (seatMatch) seats = parseInt(seatMatch[1], 10);
  }
  if (lines.marketing.length > 1) return null;
  const join = arr => arr.length ? arr.join(' + ') : null;
  return {
    marketing: join(lines.marketing),
    coaching: join(lines.coaching),
    law: join(lines.law),
    seats: seats ?? (lines.law.some(n => n.startsWith('AI Workforce Pro')) ? teamSizeStated : null),
  };
}

// ─── Main ─────────────────────────────────────────────────────────────────────

export async function selectPackage(friendlyName) {
  // Trigger-file override and HubSpot contact
  const triggerPath = `triggers/audit-research/${friendlyName}.json`;
  let hubspotContactId = null;
  let packageOverride = null;
  if (existsSync(triggerPath)) {
    try {
      const trigger = JSON.parse(readFileSync(triggerPath, 'utf8'));
      if (trigger.package && trigger.package.trim()) packageOverride = trigger.package.trim();
      hubspotContactId = trigger.hubspot_contact_id || null;
    } catch { /* non-fatal */ }
  }

  // Find research notes
  const notesFile = newestResearchNotes(friendlyName);
  if (!notesFile) {
    console.error(`ERROR: No *_Research_Notes.txt found in ${friendlyName}/ — Pass 1 may not have completed.`);
    process.exit(1);
  }
  const notesPath = join(friendlyName, notesFile);
  const text = readFileSync(notesPath, 'utf8');
  console.log(`Reading: ${notesPath}`);

  const notes = [];

  // Parse signals
  const revenueParsed   = parseRevenueFromNotes(text);
  const revenueStated   = revenueParsed?.value ?? null;
  const netRevenueStated = parseNetRevenue(text);
  const practiceAreas   = parsePracticeAreas(text);
  let teamSizeStated    = parseTeamSize(text);
  let teamSizeSource    = teamSizeStated != null ? 'research_notes' : null;
  const isContingencyPractice = detectContingencyPractice(practiceAreas);

  console.log(`  Revenue stated:  ${revenueStated != null ? '$' + revenueStated.toLocaleString() : 'NOT STATED'}`);
  console.log(`  Net revenue:     ${netRevenueStated != null ? '$' + netRevenueStated.toLocaleString() : 'NOT STATED'}`);
  console.log(`  Team size:       ${teamSizeStated ?? 'NOT STATED'}`);
  console.log(`  Practice areas:  ${practiceAreas.join(' | ') || 'none detected'}`);

  const company = await fetchHubSpotCompany(hubspotContactId);
  if (teamSizeStated == null && company?.employees) {
    teamSizeStated = company.employees;
    teamSizeSource = 'hubspot_company';
    notes.push(`Team size not in research notes — using ${company.employees} employees from the HubSpot company record.`);
  }

  // Determine effective values (stated or estimated)
  // Revenue hierarchy: research notes → HubSpot contact fields → team size estimate
  let confidence = revenueParsed?.source === 'research_notes_text' ? 'medium' : 'high';
  let effectiveRevenue = revenueStated;
  let revenueSource = revenueParsed?.source ?? null;
  let revenueLabel  = null;
  let revenueVerified = revenueStated != null;
  const effectiveTeam = teamSizeStated ?? 3;

  // Contingency-fee practices: tier on collected/net revenue, not gross case value,
  // when the research notes state a net/collected figure.
  if (isContingencyPractice && netRevenueStated !== null) {
    effectiveRevenue = netRevenueStated;
    revenueSource = 'research_notes_net';
    revenueVerified = true;
    notes.push(revenueStated !== null
      ? `Contingency-fee practice with both gross ($${revenueStated.toLocaleString()}) and net/collected ($${netRevenueStated.toLocaleString()}) revenue stated — tiering on net per contingency-revenue rule.`
      : `Contingency-fee practice with net/collected revenue stated ($${netRevenueStated.toLocaleString()}) — tiering on net per contingency-revenue rule.`);
  } else if (isContingencyPractice && revenueStated !== null && netRevenueStated === null) {
    notes.push(`Contingency-fee practice with only gross revenue stated ($${revenueStated.toLocaleString()}) — no net/collected figure found. Using gross as fallback, but confidence downgraded: confirm actual collected revenue with sales rep before finalizing tier.`);
    confidence = 'low';
  }

  if (effectiveRevenue === null) {
    // Fallback 1: HubSpot contact revenue fields
    const hsRevenue = await fetchHubSpotRevenue(hubspotContactId);
    if (hsRevenue) {
      effectiveRevenue = hsRevenue.value;
      revenueSource    = hsRevenue.source;
      revenueLabel     = hsRevenue.rawLabel;
      confidence       = hsRevenue.confidence;
      revenueVerified  = !hsRevenue.isRange;
      notes.push(hsRevenue.isRange
        ? `Revenue not stated on the call — HubSpot only has the range "${hsRevenue.rawLabel}". Using the midpoint ($${hsRevenue.value.toLocaleString()}) for this draft only; confirm actual revenue with the prospect before locking in.`
        : `Revenue not in research notes — sourced from HubSpot (${hsRevenue.source}): "${hsRevenue.rawLabel}" → $${hsRevenue.value.toLocaleString()}`);
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
    notes.push('Team size not stated in research notes or HubSpot — assumed 3. Please confirm headcount.');
  }

  // Call focus — what the discovery call was actually about. Applied here so the
  // seller-facing Phase 1 package already reflects it (Pass 2's call-purpose
  // override in audit-write.md stays as a backstop). Its notes go first so they
  // show in the Slack summary.
  const callFocus = parseCallFocus(text);
  const focusNotes = [];
  console.log(`  Call focus:      ${callFocus.engagement ?? 'NOT STATED'} | products: ${callFocus.products?.join(', ') || 'none'} | lead-gen gap: ${callFocus.leadGenGap ?? 'NOT STATED'}`);

  // Unknown call focus (usually no discovery call found): recommend nothing and
  // ask the seller what the call was about. A revenue-only marketing + coaching
  // bundle is computed below only as a reference option the seller can pick.
  const needsSellerInput = callFocus.engagement === null && !packageOverride;
  let includeMarketing = true;
  if (needsSellerInput) {
    focusNotes.push('Call focus unknown (no discovery call found, or Primary engagement not recorded) — no package recommended. Seller must say what the call was about before this can be locked in.');
  } else if (callFocus.engagement === 'coaching/ops' || callFocus.engagement === 'AI') {
    if (callFocus.leadGenGap === true) {
      focusNotes.push(`${callFocus.engagement === 'AI' ? 'AI' : 'Coaching/ops'}-led call, but prospect stated a lead-gen need — marketing included.`);
    } else if (callFocus.leadGenGap === false) {
      includeMarketing = false;
      focusNotes.push(`${callFocus.engagement === 'AI' ? 'AI' : 'Coaching/ops'}-led call with no lead-gen need stated — marketing left out (call-purpose rule).`);
    } else {
      focusNotes.push(`${callFocus.engagement === 'AI' ? 'AI' : 'Coaching/ops'}-led call but lead-gen gap not recorded — marketing kept; confirm with sales rep whether it belongs.`);
    }
  }

  // Select packages
  const revenueMarketing = includeMarketing ? selectMarketingTier(revenueStated, effectiveRevenue, practiceAreas, text, notes) : null;
  // The revenue rule's reasoning is only shown if its pick is the one used.
  const coachingRuleNotes = [];
  const revenueCoaching  = selectCoachingByRevenue(effectiveRevenue, effectiveTeam, text, coachingRuleNotes);
  const revenueAdSpend   = revenueMarketing ? estimateAdSpend(practiceAreas, revenueMarketing) : null;

  // Coaching named on the call wins over the revenue rule. On an AI-led call
  // where no coaching was named, leave coaching out rather than adding the
  // revenue default nobody asked for.
  const discussedCoaching = selectDiscussedCoaching(callFocus.products, effectiveRevenue, focusNotes);
  let coaching = revenueCoaching;
  if (discussedCoaching) {
    coaching = discussedCoaching;
    if (discussedCoaching.name !== revenueCoaching.name) {
      focusNotes.push(`${discussedCoaching.name} selected because it was discussed on the call (revenue rule would pick ${revenueCoaching.name}) — confirm tier with sales rep.`);
    }
  } else if (callFocus.engagement === 'AI') {
    coaching = null;
    focusNotes.push(`AI-led call with no coaching discussed — coaching left out (revenue rule would add ${revenueCoaching.name}; add it back if the seller wants it).`);
  }
  if (coaching === revenueCoaching || needsSellerInput) notes.push(...coachingRuleNotes);

  const law = selectLawTier(callFocus.products, effectiveRevenue, teamSizeStated, focusNotes);

  if (callFocus.engagement === 'AI' && !(callFocus.products || []).some(p => LAW_PRODUCTS.has(p) || p === AIWP_UNSPECIFIED)) {
    focusNotes.push('AI-led call but no AI product in "Products discussed on call" — review whether an AI Workforce Pro / Fractional CTO tier belongs in the package.');
  }

  // Reference option for an unknown-focus package: what the revenue rules alone
  // would pick. Not a recommendation — the seller can choose it in Slack.
  let revenueOnlyOption = null;
  if (needsSellerInput) {
    const ref = pricePackage({
      marketing: revenueMarketing ? { name: revenueMarketing.name } : null,
      coaching: { name: revenueCoaching.name },
    });
    revenueOnlyOption = {
      marketing_tier:          revenueMarketing?.tier ?? null,
      marketing_name:          revenueMarketing?.name ?? null,
      marketing_price_bundled: ref.lines.marketing?.charged ?? null,
      marketing_price_retail:  ref.lines.marketing?.retail ?? null,
      coaching_name:           revenueCoaching.name,
      coaching_price_bundled:  ref.lines.coaching?.charged ?? null,
      coaching_price_retail:   ref.lines.coaching?.retail ?? null,
      ad_spend_conservative:   revenueAdSpend?.conservative ?? null,
      ad_spend_aggressive:     revenueAdSpend?.aggressive ?? null,
      ad_spend_rationale:      revenueAdSpend?.rationale ?? null,
      total_bundled:           ref.total,
    };
  }

  let marketing = needsSellerInput ? null : revenueMarketing;
  if (needsSellerInput) coaching = null;
  let adSpend = needsSellerInput ? null : revenueAdSpend;
  let lawLine = law;

  // A seller-set package in the trigger file replaces the selection, as long
  // as every product in it is one the catalog can price.
  let packageSource = 'rules';
  if (packageOverride) {
    const o = linesFromOverride(packageOverride, teamSizeStated);
    if (!o) {
      console.log(`Trigger file has a package override the catalog can't fully parse: "${packageOverride}"`);
      console.log('Skipping deterministic selection — Pass 2 uses the override text.');
      return null;
    }
    packageSource = 'trigger_override';
    focusNotes.unshift(`Package set by the seller: "${packageOverride}".`);
    marketing = o.marketing ? (MARKETING_TIERS.find(t => t.name === o.marketing) ?? { name: o.marketing, adCap: 20_000 }) : null;
    adSpend = marketing ? estimateAdSpend(practiceAreas, marketing) : null;
    coaching = o.coaching ? { name: o.coaching } : null;
    lawLine = o.law ? { name: o.law, seats: o.seats } : null;
  }

  notes.unshift(...focusNotes);

  const decision = {
    confidence,
    revenue_stated:          revenueStated,
    net_revenue_stated:      netRevenueStated,
    is_contingency_practice: isContingencyPractice,
    revenue_effective:       effectiveRevenue,
    revenue_source:          revenueSource,
    revenue_label:           revenueLabel,
    revenue_verified:        revenueVerified,
    needs_revenue_confirmation: !revenueVerified,
    team_size_stated:        teamSizeStated,
    team_size_source:        teamSizeSource,
    team_size_effective:     effectiveTeam,
    practice_areas_detected: practiceAreas,
    hubspot_company:         company,
    // "MISMATCH — trigger says X; website says Y" from the research notes;
    // the Phase 1 Slack post asks the seller to confirm the firm name.
    firm_identity_check:     readNoteField(text, 'firm identity check', { firstLineOnly: true }),

    package_source:          packageSource,
    package_override:        packageOverride,
    needs_seller_input:      needsSellerInput,
    revenue_only_option:     revenueOnlyOption,

    call_focus: {
      primary_engagement:  callFocus.engagement,
      products_discussed:  callFocus.products,
      lead_gen_gap:        callFocus.leadGenGap,
    },

    marketing_tier:          marketing?.tier ?? null,
    marketing_name:          marketing?.name ?? null,
    marketing_price_bundled: null,
    marketing_price_retail:  null,
    marketing_savings:       null,

    coaching_name:           coaching?.name ?? null,
    coaching_price_bundled:  null,
    coaching_price_retail:   null,
    coaching_savings:        null,

    law_tier:                null,
    law_name:                lawLine?.name ?? null,
    law_price_bundled:       null,
    law_price_retail:        null,
    law_seats:               lawLine?.seats ?? null,

    total_bundled:           0,
    total_savings:           null,

    ad_spend_conservative:   adSpend?.conservative ?? null,
    ad_spend_aggressive:     adSpend?.aggressive ?? null,
    ad_spend_rationale:      adSpend?.rationale ?? null,

    selection_notes: notes,
  };

  // Prices, bundle rule and totals (scripts/lib/pricing.mjs).
  notes.push(...applyPricing(decision));
  if (!revenueVerified) decision.confidence = 'low';

  // 35% cap: management fees + ad spend must not exceed 35% of monthly revenue.
  const monthlyCap = Math.round(effectiveRevenue / 12 * 0.35);
  const spendAtFloor = decision.total_bundled + (adSpend?.conservative ?? 0);
  if (spendAtFloor > monthlyCap) {
    notes.push(`Total at conservative ad spend ($${spendAtFloor.toLocaleString()}/mo) is over the 35% cap ($${monthlyCap.toLocaleString()}/mo on $${effectiveRevenue.toLocaleString()} revenue) — review with sales rep.`);
  }

  return decision;
}

/** Last-resort decision when selection itself crashes, so Slack never shows an empty package. */
function fallbackDecision(err) {
  return {
    confidence: 'low',
    needs_seller_input: true,
    selection_error: err.message,
    package_source: 'error',
    marketing_name: null, coaching_name: null, law_name: null,
    total_bundled: 0, total_savings: null,
    selection_notes: [`Automatic package selection failed (${err.message}). Tell the bot which products to propose in this thread.`],
  };
}

function printSummary(decision, outputPath) {
  const money = n => (n == null ? 'price TBD' : `$${n.toLocaleString()}/mo`);
  console.log(`\nPackage decision → ${outputPath}`);
  if (decision.needs_seller_input) console.log('  NEEDS SELLER INPUT');
  if (decision.revenue_only_option) {
    const r = decision.revenue_only_option;
    console.log(`  Revenue-only reference: ${r.marketing_name ?? 'no marketing'} + ${r.coaching_name} — ${money(r.total_bundled)}`);
  }
  console.log(`  Marketing:  ${decision.marketing_name ? `${decision.marketing_name} — ${money(decision.marketing_price_bundled)}` : 'none'}`);
  console.log(`  Coaching:   ${decision.coaching_name ? `${decision.coaching_name} — ${money(decision.coaching_price_bundled)}` : 'none'}`);
  if (decision.law_name) console.log(`  AI:         ${decision.law_name} — ${money(decision.law_price_bundled)}`);
  console.log(`  Total:      ${money(decision.total_bundled)} (${decision.pricing_mode ?? 'n/a'} pricing)`);
  if (decision.ad_spend_conservative != null) console.log(`  Ad spend:   $${decision.ad_spend_conservative.toLocaleString()}–$${decision.ad_spend_aggressive.toLocaleString()}/mo`);
  console.log(`  Confidence: ${decision.confidence}`);
  (decision.selection_notes || []).forEach(n => console.log(`    - ${n}`));
}

async function main() {
  const friendlyName = process.argv[2];
  if (!friendlyName) {
    console.error('Usage: node scripts/select-package.mjs <friendly-name>');
    process.exit(1);
  }
  if (!existsSync(friendlyName)) {
    console.error(`ERROR: Firm directory not found: ${friendlyName}/`);
    process.exit(1);
  }
  const outputPath = join(friendlyName, 'package_decision.json');
  let decision;
  try {
    decision = await selectPackage(friendlyName);
  } catch (err) {
    console.error(`select-package.mjs error: ${err.stack || err.message}`);
    decision = fallbackDecision(err);
  }
  if (!decision) return; // override left to Pass 2
  writeFileSync(outputPath, JSON.stringify(decision, null, 2));
  printSummary(decision, outputPath);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch(err => {
    console.error(`select-package.mjs error: ${err.message}`);
    process.exit(0); // non-fatal — Pass 2 falls back to its own rules
  });
}
