/**
 * Investment math for the proposal deck — ad spend range, return projection,
 * monthly and year-one totals. Deterministic: the same package_decision.json
 * and the same research-notes inputs always give the same numbers.
 *
 * The rules are the AD SPEND CALCULATION and ROI PROJECTIONS sections of
 * .claude/commands/audit-write.md (detail in Design Files/Scoping_and_Ad_Spend_Guide.md
 * Steps 3–4 and 8). Where those documents are silent or conflict, the choice
 * made here is written next to the code as "DECISION:" — keep audit-write.md's
 * "How the code applies these rules" list in sync.
 *
 * Used by scripts/select-package.mjs (Phase 1) and scripts/reprice.mjs (every
 * package change and before every deck build), which write the result to
 * package_decision.json → `investment`. The deck's investment slide reads it
 * from there; nobody retypes a number.
 */

// ─── Tables (audit-write.md / Scoping guide Step 4) ──────────────────────────

/** Monthly channel minimums by practice area (Scoping guide Step 4 table). */
export const CHANNEL_MINIMUMS = {
  'MVA':              { ppc: 10_000, lsa: 2_000, metaRetargeting: 1_500, metaLeadGen: 6_000 },
  'Accident/Injury':  { ppc:  6_000, lsa: 2_000, metaRetargeting: 1_200, metaLeadGen: 5_500 },
  'Criminal Defense': { ppc:  5_500, lsa: 2_000, metaRetargeting: 1_200, metaLeadGen: 4_500 },
  'Bankruptcy':       { ppc:  4_500, lsa: 2_000, metaRetargeting: 1_200, metaLeadGen: 3_500 },
  'Family Law':       { ppc:  3_500, lsa: 2_000, metaRetargeting: 1_200, metaLeadGen: 3_500 },
  'Estate Planning':  { ppc:  3_500, lsa: 2_000, metaRetargeting: 1_200, metaLeadGen: 3_500 },
  'Business Law':     { ppc:  3_500, lsa: 2_000, metaRetargeting: 1_200, metaLeadGen: 3_500 },
  'Immigration':      { ppc:  3_000, lsa: 2_000, metaRetargeting: 1_200, metaLeadGen: 3_000 },
  'Other':            { ppc:  3_000, lsa: 2_000, metaRetargeting: 1_200, metaLeadGen: 3_000 },
};
export const PRACTICE_AREAS = Object.keys(CHANNEL_MINIMUMS);

/** Client-facing CPL ranges (audit-write.md ROI PROJECTIONS). */
const CPL_RANGES = {
  'Accident/Injury':  { ppc: [630, 780], lsa: [210, 260], metaRetargeting: [80, 100] },
  'Criminal Defense': { ppc: [155, 205], lsa: [140, 180], metaRetargeting: [50, 70] },
  'Family Law':       { ppc: [90, 110],  lsa: [70, 90],   metaRetargeting: [50, 65] },
  'Estate Planning':  { ppc: [120, 150], lsa: [55, 75],   metaRetargeting: [45, 60] },
  'Immigration':      { ppc: [85, 110],  lsa: [55, 75],   metaRetargeting: [50, 65] },
  'Bankruptcy':       { ppc: [80, 100],  lsa: [90, 120],  metaRetargeting: [60, 80] },
  'Business Law':     { ppc: [100, 120], lsa: [110, 140], metaRetargeting: [60, 80] },
};
// DECISION: the CPL table has no MVA row; MVA uses "Accident & Injury".
// "Other" has no row at all — the benchmark projection is skipped for it.
const CPL_ROW = { 'MVA': 'Accident/Injury' };

/** Practice-area default case values (audit-write.md) — [low, high]. */
const DEFAULT_CASE_VALUE = {
  'MVA': [5_000, 10_000], 'Accident/Injury': [5_000, 8_000], 'Criminal Defense': [3_000, 5_000],
  'Family Law': [3_000, 5_000], 'Estate Planning': [1_500, 3_000], 'Immigration': [3_000, 6_000],
  'Bankruptcy': [1_500, 3_000], 'Business Law': [3_000, 7_000],
};

const GEO_MULTIPLIER = { 1: 1.5, 2: 1.3, 3: 1.15, 4: 1.0, 5: 0.85 };

/** Ad spend managed per marketing product (audit-write.md + Scoping guide Step 3H). */
const AD_CAPS = {
  'Full Service Marketing — Essentials': 7_500,  'Full Service Marketing — Starter': 25_000,
  'Full Service Marketing — Growth':    50_000,  'Full Service Marketing — Dominate': 100_000,
  'Full Service Marketing — Platinum': 150_000,
  'Paid Ads Essentials': 7_500, 'Paid Ads Starter': 20_000, 'Paid Ads Growth': 50_000,
  'Paid Ads Dominate': 100_000, 'Paid Ads Platinum': 150_000,
};

// DECISION: the channels "being recommended" are never defined per package.
// Full Service and Paid Ads packages are costed on the Scoping guide's three
// primary channels — Google PPC, LSA and Meta retargeting (its worked example
// and its "all 3 primary channels" line). Meta lead gen and PMax are add-on
// channels the aggressive budget can fund; they're not part of the floor.
const CHANNELS = [
  { key: 'ppc', label: 'Google Search' },
  { key: 'lsa', label: 'Local Services Ads' },
  { key: 'metaRetargeting', label: 'Meta retargeting' },
];

const ABSOLUTE_MIN = 3_000;
const DEFAULT_CLOSE_RATE = 0.15;
const CONSERVATIVE_CPL_CUSHION = 1.2;
const OVERAGE_FEE = 0.10;                 // audit-write.md: "note 10% overage fee"
const SCOPING_AD_SPEND = 25_000;          // escalation flag threshold

// ─── Research-notes inputs ───────────────────────────────────────────────────

function field(text, label) {
  const m = String(text || '').match(new RegExp(`^\\s*-?\\s*${label}\\s*:\\s*(.+)$`, 'im'));
  if (!m) return null;
  const v = m[1].trim();
  return v && !v.startsWith('[') ? v : null;
}

const NOT_STATED = /^\s*["']?\s*(?:not stated|not given|unknown|n\/a|not recorded|not observed)/i;

/** First explicit dollar amount ("$25,000", "$4.5K", "$1.2M"). Null if none or "not stated". */
export function parseDollars(value) {
  if (value == null || NOT_STATED.test(value)) return null;
  const m = String(value).match(/\$\s*(\d[\d,]*(?:\.\d+)?)\s*(k|thousand|m|million)?\b/i);
  if (!m) return null;
  let n = parseFloat(m[1].replace(/,/g, ''));
  const u = (m[2] || '').toLowerCase();
  if (u === 'k' || u === 'thousand') n *= 1_000;
  if (u === 'm' || u === 'million') n *= 1_000_000;
  return n > 0 ? Math.round(n) : null;
}

/** Spend: "$0", "none" or "no paid ads" → 0; a dollar amount → that; else null. */
function parseSpend(value) {
  if (value == null || NOT_STATED.test(value)) return null;
  if (/^\s*["']?\s*(?:none|no paid|\$?\s*0\b|zero)/i.test(value)) return 0;
  return parseDollars(value);
}

function parsePercent(value) {
  if (value == null || NOT_STATED.test(value)) return null;
  const m = String(value).match(/(\d+(?:\.\d+)?)\s*%/);
  return m ? parseFloat(m[1]) / 100 : null;
}

function parsePracticeArea(value) {
  if (!value) return null;
  const v = value.toLowerCase();
  return PRACTICE_AREAS.find(p => v.startsWith(p.toLowerCase())) ?? null;
}

/** Practice area from free-text practice areas, when the machine-read line is missing. */
export function practiceAreaFromText(areas = []) {
  const t = areas.join(' | ').toLowerCase();
  const rules = [
    ['MVA', /mva|motor vehicle|car accident|auto accident|truck/],
    ['Accident/Injury', /personal injury|accident|wrongful death/],
    ['Criminal Defense', /criminal|dui|dwi/],
    ['Family Law', /family|divorce|custody/],
    ['Estate Planning', /estate|wills|trusts|probate|elder/],
    ['Immigration', /immigration/],
    ['Bankruptcy', /bankruptcy/],
    ['Business Law', /business|corporate/],
  ];
  return rules.find(([, re]) => re.test(t))?.[0] ?? null;
}

/**
 * The "Investment inputs" block of the research notes (audit-research.md
 * STEP 9). Every value is what was said on the call, or "not stated".
 */
export function parseInvestmentInputs(text) {
  const tier = field(text, 'geo market tier')?.match(/\b([1-5])\b/);
  const comp = field(text, 'market competitiveness')?.match(/\b(low|medium|high)\b/i);
  const spanish = field(text, 'spanish campaign needed');
  return {
    practiceArea: parsePracticeArea(field(text, 'ad spend practice area')),
    geoTier: tier ? parseInt(tier[1], 10) : null,
    competitiveness: comp ? comp[1][0].toUpperCase() + comp[1].slice(1).toLowerCase() : null,
    spanish: spanish ? /^\s*yes/i.test(spanish) : null,
    currentAdSpend: parseSpend(field(text, 'current monthly ad spend \\(stated\\)')),
    currentCostPerCase: parseDollars(field(text, 'current cost per signed case \\(stated\\)')),
    currentCostPerLead: parseDollars(field(text, 'current cost per lead \\(stated\\)')),
    caseValue: parseDollars(field(text, 'average case value \\(stated, one figure\\)')),
    closeRate: parsePercent(field(text, 'close rate \\(stated\\)')),
    revenueGoal: parseDollars(field(text, 'revenue goal \\(annual, one figure\\)')),
    maxAdBudget: parseDollars(field(text, 'maximum monthly ad budget \\(stated\\)')),
  };
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

const money = n => `$${Math.round(n).toLocaleString('en-US')}`;
const round100 = n => Math.round(n / 100) * 100;
const round500 = n => Math.round(n / 500) * 500;
const one = n => Math.round(n * 10) / 10;

/** The package's product lines, from the priced decision. */
function productLines(d) {
  const lines = [];
  const add = (category, name, charged, standalone, extra = '') => {
    if (name) lines.push({ category, name: name + extra, charged, standalone });
  };
  add('marketing', d.marketing_name, d.marketing_price_bundled, d.marketing_price_retail);
  add('coaching', d.coaching_name, d.coaching_price_bundled, d.coaching_price_retail);
  const seats = d.law_seats && /AI Workforce Pro/.test(d.law_name || '') ? ` (${d.law_seats} seat${d.law_seats === 1 ? '' : 's'})` : '';
  add('law', d.law_name, d.law_price_bundled, d.law_price_retail, seats);
  return lines;
}

function weightedCpl(pa) {
  const row = CPL_RANGES[CPL_ROW[pa] ?? pa];
  if (!row) return null;
  const mins = CHANNEL_MINIMUMS[pa];
  // DECISION: "weight by channel spend proportion" — no split is defined, so
  // the weights are the channel minimums of the three recommended channels.
  let spend = 0, cost = 0;
  for (const { key } of CHANNELS) {
    const mid = (row[key][0] + row[key][1]) / 2;
    spend += mins[key];
    cost += mins[key] / mid;          // leads bought at that channel's CPL
  }
  return spend / cost;                // blended $ per lead
}

// ─── Main ────────────────────────────────────────────────────────────────────

/**
 * @param d       priced package_decision.json (applyPricing already run)
 * @param inputs  parseInvestmentInputs(research notes), or {}
 * @returns the `investment` block
 */
export function computeInvestment(d, inputs = {}) {
  const flags = [];          // internal — BUILD NOTES only, never on a slide
  const products = productLines(d);
  const monthly = d.total_bundled || products.reduce((s, p) => s + (p.charged || 0), 0);

  const investment = {
    version: 1,
    products,
    monthly_total: monthly,
    total_savings: d.total_savings || 0,
    pricing_mode: d.pricing_mode ?? null,
    // DECISION: no setup fee is listed for Full Service Marketing, Paid Ads,
    // Web + SEO, coaching or fractional products in the pricing tables
    // (Fractional CTO is $0), so year one is 12 × the monthly fees.
    year_one_total: monthly * 12,
    year_one_basis: `12 × ${money(monthly)}/mo in fees. Ad spend is paid separately to Google and Meta.`,
    ad_spend: null,
    return: null,
    inputs: {},
    flags,
  };

  const mkt = d.marketing_name || '';
  const runsAds = /^(Full Service Marketing|Paid Ads)/.test(mkt);
  if (!runsAds) return investment;

  // ── Inputs, each with its source ──────────────────────────────────────────
  let pa = inputs.practiceArea ?? null;
  let paSource = 'research notes';
  if (!pa) {
    pa = practiceAreaFromText(d.practice_areas_detected || []) ?? 'Other';
    paSource = 'inferred from practice areas';
    flags.push(`Ad spend practice area not recorded in research — using ${pa} (${paSource}).`);
  }
  const tier = inputs.geoTier ?? 4;
  if (inputs.geoTier == null) flags.push('Geo market tier not recorded in research — using Tier 4 (1.0×).');
  const isPI = pa === 'MVA' || pa === 'Accident/Injury';
  const competitiveness = inputs.competitiveness ?? 'Medium';
  if (inputs.competitiveness == null && (isPI || pa === 'Criminal Defense')) {
    flags.push('Market competitiveness not recorded in research — using Medium for the ad spend floor.');
  }
  const spanish = !!inputs.spanish;
  const revenue = d.revenue_effective || 0;
  const goal = inputs.revenueGoal ?? revenue * 2;
  const goalSource = inputs.revenueGoal ? 'stated on the call' : 'not stated — 2× current revenue (audit-write.md)';
  const caseValueStated = inputs.caseValue != null;
  const caseValue = inputs.caseValue ?? DEFAULT_CASE_VALUE[pa]?.[0] ?? null;
  // DECISION: the default case values are ranges; the low end is used.
  const closeStated = inputs.closeRate != null;
  const closeRate = inputs.closeRate ?? DEFAULT_CLOSE_RATE;
  const fee = d.marketing_price_bundled || 0;
  const cap = AD_CAPS[mkt.replace(/\s*\(.*\)$/, '')] ?? null;
  if (cap == null) flags.push(`No ad spend cap on file for "${mkt}" — cap not applied.`);

  investment.inputs = {
    practice_area: { value: pa, source: paSource },
    geo_tier: { value: tier, multiplier: GEO_MULTIPLIER[tier], source: inputs.geoTier ? 'research notes' : 'default' },
    competitiveness: { value: competitiveness, source: inputs.competitiveness ? 'research notes' : 'default' },
    spanish_campaign: spanish,
    revenue_effective: revenue,
    revenue_goal: { value: goal, source: goalSource },
    case_value: { value: caseValue, source: caseValueStated ? 'stated on the call' : 'practice-area default (low end)' },
    close_rate: { value: closeRate, source: closeStated ? 'stated on the call' : 'default 15%' },
    current_ad_spend: inputs.currentAdSpend ?? null,
    current_cost_per_case: inputs.currentCostPerCase ?? null,
    current_cost_per_lead: inputs.currentCostPerLead ?? null,
    max_ad_budget: inputs.maxAdBudget ?? null,
    management_fee: fee,
    ad_spend_cap: cap,
  };

  // ── Conservative: channel minimums, practice floors, and today's spend ────
  const mins = CHANNEL_MINIMUMS[pa];
  const channels = CHANNELS.map(c => ({ channel: c.label, minimum: mins[c.key] }));
  const channelSum = channels.reduce((s, c) => s + c.minimum, 0);
  let floor = Math.max(channelSum, ABSOLUTE_MIN);
  const floorNotes = [`channel minimums ${channels.map(c => money(c.minimum)).join(' + ')} = ${money(channelSum)}`];
  if (isPI) {
    const piFloor = { Low: 5_500, Medium: 7_500, High: 10_000 }[competitiveness];
    if (piFloor > floor) { floor = piFloor; floorNotes.push(`personal injury ${competitiveness.toLowerCase()}-competition floor ${money(piFloor)}`); }
  }
  if (pa === 'Criminal Defense' && competitiveness === 'High' && 5_000 > floor) {
    floor = 5_000; floorNotes.push('criminal defense high-competition floor $5,000');
  }
  // DECISION: never recommend less than the client already spends. Today's
  // stated spend is held as the low end ("held in place at launch").
  const current = inputs.currentAdSpend;
  let conservative = floor;
  let conservativeBasis = floorNotes.join('; ');
  if (current != null && current > floor) {
    conservative = current;
    conservativeBasis = `current spend stated on the call (${money(current)}/mo) held at launch — above the ${money(floor)} channel floor`;
  }

  // ── Aggressive: 20% rule vs reverse math, then floors and caps ────────────
  const geo = GEO_MULTIPLIER[tier] ?? 1;
  const spanishMult = spanish ? (isPI ? 1.5 : 1.33) : 1;
  const budget20 = goal * 0.20 / 12 * geo * spanishMult - fee;
  const benchCpl = weightedCpl(pa);
  let reverse = null, reverseBasis = null;
  if (caseValue) {
    const targetCases = goal / 12 / caseValue;
    if (inputs.currentCostPerCase) {
      reverse = targetCases * inputs.currentCostPerCase;
      reverseBasis = `${one(targetCases)} cases/mo × ${money(inputs.currentCostPerCase)} cost per case (stated)`;
    } else if (inputs.currentCostPerLead) {
      reverse = targetCases / closeRate * inputs.currentCostPerLead;
      reverseBasis = `${one(targetCases)} cases/mo ÷ ${Math.round(closeRate * 100)}% close × ${money(inputs.currentCostPerLead)} cost per lead (stated)`;
    } else if (benchCpl) {
      reverse = targetCases / closeRate * benchCpl;
      reverseBasis = `${one(targetCases)} cases/mo ÷ ${Math.round(closeRate * 100)}% close × ${money(benchCpl)} benchmark blended CPL`;
    }
  }
  let aggressive = Math.max(budget20, reverse ?? 0, conservative);
  const aggressiveSteps = [
    `20% rule: ${money(goal)} goal × 20% ÷ 12 × ${geo} geo${spanish ? ` × ${spanishMult} Spanish` : ''} − ${money(fee)} fee = ${money(budget20)}`,
    reverse != null ? `reverse math: ${reverseBasis} = ${money(reverse)}` : 'reverse math: not possible (no case value)',
  ];
  if (reverse != null && reverse > budget20 * 1.5) {
    flags.push(`Reverse math (${money(reverse)}) is well above the 20% rule (${money(budget20)}) — the goal may be aggressive for the budget (paid ads team review).`);
  }
  if (inputs.maxAdBudget != null && aggressive > inputs.maxAdBudget) {
    // DECISION: a monthly ceiling the client named on the call caps the high
    // end (not in the tables — follows the budget-reality override).
    aggressive = Math.max(inputs.maxAdBudget, conservative);
    aggressiveSteps.push(`capped at the ${money(inputs.maxAdBudget)}/mo the client said they can spend`);
  }
  let overage = null;
  if (cap != null && aggressive > cap) {
    // DECISION: product selection is never changed here, so instead of the
    // tier upgrade the boundary rule allows, the high end stops at the cap
    // and the seller is told.
    flags.push(`Goal-based ad spend (${money(aggressive)}) is above the ${money(cap)} cap for ${mkt} — capped. Higher spend means a tier upgrade or the ${OVERAGE_FEE * 100}% overage fee (seller decision).`);
    aggressive = Math.max(cap, conservative);
    aggressiveSteps.push(`capped at the ${money(cap)} the package manages`);
  }
  if (cap != null && conservative > cap) {
    overage = { above_cap: conservative - cap, fee_rate: OVERAGE_FEE };
    flags.push(`Current spend (${money(conservative)}) is above the ${money(cap)} cap for ${mkt} — the ${OVERAGE_FEE * 100}% overage fee applies above the cap.`);
  }
  conservative = round100(conservative);
  aggressive = Math.max(round500(aggressive), conservative);

  if (aggressive > SCOPING_AD_SPEND) flags.push('Ad spend over $25K — scoping approval required.');

  investment.ad_spend = {
    channels,
    conservative,
    aggressive,
    current_stated: current ?? null,
    cap,
    overage,
    conservative_basis: conservativeBasis,
    aggressive_steps: aggressiveSteps,
    year_one_range: [conservative * 12, aggressive * 12],
  };

  // ── Return on ad spend ────────────────────────────────────────────────────
  if (!caseValue) {
    flags.push('No case value (stated or default) — return projection left out.');
    return investment;
  }
  let method, basis;
  const spends = [...new Set([conservative, aggressive])];
  const scenarios = spends.map((spend, i) => {
    let leads = null, cases;
    if (inputs.currentCostPerCase) {
      cases = spend / inputs.currentCostPerCase;
    } else if (inputs.currentCostPerLead) {
      leads = spend / inputs.currentCostPerLead;
      cases = leads * closeRate;
    } else if (benchCpl) {
      const cpl = benchCpl * (i === 0 && spends.length > 1 ? CONSERVATIVE_CPL_CUSHION : 1);
      leads = spend / cpl;
      cases = leads * closeRate;
    } else {
      return null;
    }
    const revenueOut = cases * caseValue;
    return {
      label: i === 0 ? (spends.length > 1 ? 'Conservative' : 'Recommended') : 'Aggressive',
      ad_spend: spend,
      leads: leads != null ? one(leads) : null,
      cases: one(cases),
      revenue: round100(revenueOut),
      return_multiple: one(revenueOut / spend),
    };
  }).filter(Boolean);
  if (!scenarios.length) {
    flags.push(`No cost data for ${pa} (no stated cost per case or lead, no CPL benchmark) — return projection left out.`);
    return investment;
  }
  const cvText = `${money(caseValue)} ${caseValueStated ? 'average case (said on the call)' : 'case value (assumed default)'}`;
  if (inputs.currentCostPerCase) {
    method = 'stated_cost_per_case';
    basis = `At today's ${money(inputs.currentCostPerCase)} cost per signed case and a ${cvText}, with no improvement assumed.`;
  } else if (inputs.currentCostPerLead) {
    method = 'stated_cost_per_lead';
    basis = `At today's ${money(inputs.currentCostPerLead)} cost per lead, a ${Math.round(closeRate * 100)}% close rate${closeStated ? ' (said on the call)' : ' (assumed)'} and a ${cvText}.`;
  } else {
    method = 'benchmark_cpl';
    basis = `SMB Team ${/^[A-Z]+$/.test(pa) ? pa : pa.toLowerCase()} cost-per-lead benchmarks (${money(benchCpl)} blended${spends.length > 1 ? ', +20% on the low end' : ''}), ${Math.round(closeRate * 100)}% close rate${closeStated ? ' (said on the call)' : ' (assumed)'} and a ${cvText}.`;
  }
  if (!caseValueStated) flags.push(`Case value assumed (${money(caseValue)}, low end of the ${pa} default) — confirm the real fee per case.`);
  if (scenarios[0].return_multiple < 1) flags.push(`Low-end return is under 1× (${scenarios[0].return_multiple}×) — review before presenting.`);

  investment.return = {
    method,
    basis,
    case_value: caseValue,
    case_value_stated: caseValueStated,
    cost_per_case: inputs.currentCostPerCase ?? null,
    share_of_case_value: inputs.currentCostPerCase ? Math.round(inputs.currentCostPerCase / caseValue * 100) : null,
    close_rate: closeRate,
    blended_cpl: benchCpl ? Math.round(benchCpl) : null,
    scenarios,
    disclaimer: 'Illustrative arithmetic, not a forecast.',
  };
  return investment;
}

/** Copy the headline numbers onto the legacy top-level fields the Slack post reads. */
export function applyInvestment(decision, inputs) {
  const inv = computeInvestment(decision, inputs);
  decision.investment = inv;
  decision.ad_spend_conservative = inv.ad_spend?.conservative ?? null;
  decision.ad_spend_aggressive = inv.ad_spend?.aggressive ?? null;
  decision.ad_spend_rationale = inv.ad_spend
    ? { conservative_basis: inv.ad_spend.conservative_basis, aggressive_basis: inv.ad_spend.aggressive_steps.join(' → ') }
    : null;
  return inv;
}
