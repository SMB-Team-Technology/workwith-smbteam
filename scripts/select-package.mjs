/**
 * select-package.mjs — Pass 1.5: Deterministic package selection
 *
 * Runs after Pass 1 (research notes committed) and before Pass 2 (report write).
 * Outputs [friendly-name]/package_decision.json so Pass 2 reads hard values
 * instead of re-deriving tier from noisy data in a long prompt.
 *
 * Revenue hierarchy (highest to lowest confidence):
 *   1. Research notes: explicit "Annual revenue: $X" line from transcript
 *   2. Research notes: inline $ mentions near "revenue" keyword
 *   3. HubSpot contact: annual_law_firm_revenue (text range, e.g. "$961K - $3M")
 *   4. HubSpot contact: how_much_revenue_is_your_law_firm_currently_generating_per_month (× 12)
 *   5. HubSpot contact: n2024_annual_revenue, total_annual_revenue_last_year
 *   6. Estimate from team size
 *
 * Usage:
 *   node scripts/select-package.mjs <friendly-name>
 *
 * Env:
 *   HUBSPOT_TOKEN  — HubSpot private app token (used for revenue fallback lookup)
 *
 * Exits 0 always (failures are warnings, not blockers — Pass 2 falls back to PACKAGE_HINT).
 */

import { readFileSync, writeFileSync, existsSync, readdirSync } from 'fs';
import path from 'path';

// ---------------------------------------------------------------------------
// Args + env
// ---------------------------------------------------------------------------

const FRIENDLY_NAME  = process.argv[2];
const HUBSPOT_TOKEN  = process.env.HUBSPOT_TOKEN;

if (!FRIENDLY_NAME) {
  console.error('Usage: node scripts/select-package.mjs <friendly-name>');
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Pricing tables (from audit-write.md — never deviate)
// ---------------------------------------------------------------------------

const MARKETING = {
  Essentials: { bundled: 3397,  retail: null,  adSpendMin: 5000,  adSpendMax: 10000 },
  Starter:    { bundled: 4847,  retail: 5697,  adSpendMin: 10000, adSpendMax: 25000 },
  Growth:     { bundled: 7397,  retail: 8997,  adSpendMin: 25000, adSpendMax: 50000 },
  Dominate:   { bundled: 10497, retail: 12497, adSpendMin: 50000, adSpendMax: 75000 },
  Platinum:   { bundled: 15997, retail: 18997, adSpendMin: 75000, adSpendMax: 150000 },
};

const COACHING = {
  'Elite Coach':                          { bundled: 2600, retail: 3497 },
  'Elite Coach Plus':                     { bundled: 3200, retail: 3497 },
  'Elite Coach Plus + FCOO Advisor':      { bundled: 5694, retail: null },
  'FCOO Advisor':                         { bundled: 3297, retail: 3797 },
  'Master\'s Circle':                     { bundled: 4600, retail: 4997 },
  'Master\'s Circle + FCOO Advisor':      { bundled: 6694, retail: null },
  'Master\'s Circle + FCOO Director':     { bundled: 8394, retail: null },
  'Master\'s Circle + FCOO Partner':      { bundled: 12394, retail: null },
};

// ---------------------------------------------------------------------------
// Revenue parsing utilities
// ---------------------------------------------------------------------------

/**
 * Parse a dollar-amount string with optional K/M suffix into a number.
 * Examples: "1.5M" → 1500000, "680K" → 680000, "500,000" → 500000
 */
function parseDollarAmount(numStr, suffix) {
  let n = parseFloat((numStr || '').replace(/,/g, ''));
  if (isNaN(n)) return null;
  const s = (suffix || '').toUpperCase();
  if (s === 'K') n *= 1000;
  if (s === 'M') n *= 1_000_000;
  if (s === 'B') n *= 1_000_000_000;
  return n;
}

/**
 * Parse a HubSpot text revenue range into { min, max, mid }.
 * Handles formats like "$961K - $3M", "$180K - $960K", "$81K-$250K"
 * Returns null if unparseable.
 */
function parseRevenueRange(text) {
  if (!text || typeof text !== 'string') return null;
  const cleaned = text.trim();

  // Find all dollar amounts in the string
  const re = /\$([0-9,]+(?:\.[0-9]+)?)\s*(K|M|B|k|m|b)?/gi;
  const amounts = [];
  let m;
  while ((m = re.exec(cleaned)) !== null) {
    const v = parseDollarAmount(m[1], m[2]);
    if (v !== null) amounts.push(v);
  }

  if (amounts.length === 0) return null;
  const min = Math.min(...amounts);
  const max = Math.max(...amounts);
  return { min, max, mid: (min + max) / 2 };
}

/**
 * Extract an annual revenue estimate from raw research notes text.
 * Returns { value, source, confidence } or null.
 *
 * Hierarchy within research notes:
 *   1. "Annual revenue: [TRANSCRIPT — exact] — $X" — highest confidence
 *   2. "Annual revenue: $X (stated directly on call)" — high
 *   3. Inline "$X in revenue" / "$X revenue" / "revenue of $X" — medium
 *   4. Monthly revenue × 12 from inline mentions — medium-low
 */
function extractRevenueFromNotes(text) {
  if (!text) return null;

  // Pattern 1 & 2: dedicated "Annual revenue:" line
  const annualLine = text.match(
    /annual revenue[:\s]+(?:\[.*?\]\s*[—-]\s*)?\$([0-9,]+(?:\.[0-9]+)?)\s*(K|M|k|m)?/i
  );
  if (annualLine) {
    const value = parseDollarAmount(annualLine[1], annualLine[2]);
    if (value) return { value, source: 'transcript_annual_line', confidence: 'high' };
  }

  // Pattern 3: revenue N million / N.N million near "revenue"
  const millionPattern = text.match(
    /revenue[^$\n]{0,60}\$([0-9,]+(?:\.[0-9]+)?)\s*(M|million|m)\b/i
  ) || text.match(
    /\$([0-9,]+(?:\.[0-9]+)?)\s*(M|million|m)\b[^$\n]{0,40}revenue/i
  );
  if (millionPattern) {
    const value = parseDollarAmount(millionPattern[1], millionPattern[2]);
    if (value) return { value, source: 'transcript_inline', confidence: 'medium' };
  }

  // Pattern 4: "$X,XXX,XXX" near "revenue" (6+ digit amounts)
  const largeAmountPattern = text.match(
    /\$([1-9][0-9]{5,}(?:,[0-9]{3})*)[^0-9][^\n]{0,60}(?:revenue|annually|per year)/i
  ) || text.match(
    /(?:revenue|annually|per year)[^\n]{0,60}\$([1-9][0-9]{5,}(?:,[0-9]{3})*)/i
  );
  if (largeAmountPattern) {
    const value = parseDollarAmount(largeAmountPattern[1]);
    if (value) return { value, source: 'transcript_inline', confidence: 'medium' };
  }

  // Pattern 5: monthly revenue mentioned explicitly — annualize
  const monthlyLine = text.match(
    /monthly revenue[:\s]+.*?\$([0-9,]+(?:\.[0-9]+)?)\s*(K|k)?/i
  ) || text.match(
    /\$([0-9,]+(?:\.[0-9]+)?)\s*(K|k)?\s*(?:per month|\/month|monthly|\/mo)\b[^$\n]{0,60}revenue/i
  );
  if (monthlyLine) {
    const monthly = parseDollarAmount(monthlyLine[1], monthlyLine[2]);
    if (monthly) {
      return { value: monthly * 12, source: 'transcript_monthly_annualized', confidence: 'medium' };
    }
  }

  return null;
}

// ---------------------------------------------------------------------------
// HubSpot revenue lookup
// ---------------------------------------------------------------------------

const HUBSPOT_REVENUE_FIELDS = [
  'annual_law_firm_revenue',
  'how_much_revenue_is_your_law_firm_currently_generating_per_month',
  'n2024_annual_revenue',
  'total_annual_revenue_last_year',
  'annual_revenue_',
  'what_is_your_firms_annual_revenue',
  'what_was_your_firm_s_revenue_last_year_',
];

async function fetchHubSpotRevenue(contactId) {
  if (!HUBSPOT_TOKEN || !contactId) return null;

  const fields = HUBSPOT_REVENUE_FIELDS.join(',');
  let res;
  try {
    res = await fetch(
      `https://api.hubapi.com/crm/v3/objects/contacts/${contactId}?properties=${fields}`,
      {
        headers: {
          'Authorization': `Bearer ${HUBSPOT_TOKEN}`,
          'Content-Type': 'application/json',
        },
      }
    );
  } catch (err) {
    console.warn(`  HubSpot revenue lookup failed (network): ${err.message}`);
    return null;
  }

  if (!res.ok) {
    console.warn(`  HubSpot revenue lookup returned ${res.status} for contact ${contactId}`);
    return null;
  }

  const data = await res.json();
  const props = data.properties || {};

  // Try each field in priority order
  const annualRaw = props.annual_law_firm_revenue;
  if (annualRaw) {
    const range = parseRevenueRange(annualRaw);
    if (range) {
      return {
        value: range.mid,
        min: range.min,
        max: range.max,
        source: 'hubspot_annual_law_firm_revenue',
        confidence: range.max / range.min > 5 ? 'low' : 'medium',
        rawLabel: annualRaw,
      };
    }
  }

  // Monthly field → annualize
  const monthlyRaw = props.how_much_revenue_is_your_law_firm_currently_generating_per_month;
  if (monthlyRaw) {
    const range = parseRevenueRange(monthlyRaw);
    if (range) {
      return {
        value: range.mid * 12,
        min: range.min * 12,
        max: range.max * 12,
        source: 'hubspot_monthly_annualized',
        confidence: 'medium',
        rawLabel: `${monthlyRaw} (×12 annualized)`,
      };
    }
  }

  // 2024 annual revenue
  const rev2024 = props.n2024_annual_revenue;
  if (rev2024) {
    const range = parseRevenueRange(rev2024);
    if (range) {
      return {
        value: range.mid,
        min: range.min,
        max: range.max,
        source: 'hubspot_2024_annual_revenue',
        confidence: 'medium',
        rawLabel: rev2024,
      };
    }
  }

  // Total annual revenue last year
  const lastYear = props.total_annual_revenue_last_year;
  if (lastYear) {
    const range = parseRevenueRange(lastYear);
    if (range) {
      return {
        value: range.mid,
        min: range.min,
        max: range.max,
        source: 'hubspot_total_annual_revenue_last_year',
        confidence: 'medium',
        rawLabel: lastYear,
      };
    }
  }

  // Generic annual revenue field
  const annualGeneric = props.annual_revenue_ || props.what_is_your_firms_annual_revenue || props.what_was_your_firm_s_revenue_last_year_;
  if (annualGeneric) {
    const range = parseRevenueRange(annualGeneric);
    if (range) {
      return {
        value: range.mid,
        min: range.min,
        max: range.max,
        source: 'hubspot_annual_revenue_field',
        confidence: 'low',
        rawLabel: annualGeneric,
      };
    }
  }

  console.log(`  HubSpot: no parseable revenue fields for contact ${contactId}`);
  return null;
}

// ---------------------------------------------------------------------------
// Team size + practice area parsing from research notes
// ---------------------------------------------------------------------------

function parseTeamSize(text) {
  if (!text) return null;
  const patterns = [
    /team\s+(?:of\s+)?(\d+)\b/i,
    /(\d+)\s+(?:full[- ]time\s+)?(?:attorneys?|employees?|staff|people|members?|person team)/i,
    /(\d+)-person\s+(?:firm|team|office)/i,
    /(?:total|entire|whole)\s+team[^.]{0,40}?(\d+)\b/i,
  ];
  for (const re of patterns) {
    const m = text.match(re);
    if (m) {
      const n = parseInt(m[1], 10);
      if (n > 0 && n < 1000) return n;
    }
  }
  return null;
}

function hasDedicatedOps(text) {
  if (!text) return false;
  return /dedicated\s+(?:ops|operations|marketing|intake)\s+(?:team|member|staff|manager)/i.test(text) ||
    /(?:ops|operations|marketing)\s+manager/i.test(text) ||
    /office\s+manager/i.test(text);
}

function detectPracticeAreas(text) {
  if (!text) return [];
  const areas = [];
  if (/personal\s+injury|PI\b|slip.and.fall/i.test(text)) areas.push('pi');
  if (/criminal\s+(?:defense|law)/i.test(text)) areas.push('criminal');
  if (/family\s+law|divorce|custody/i.test(text)) areas.push('family');
  if (/immigration/i.test(text)) areas.push('immigration');
  if (/estate\s+plan|probate|trust/i.test(text)) areas.push('estate');
  if (/employment\s+law|labor\s+law/i.test(text)) areas.push('employment');
  if (/real\s+estate\s+law/i.test(text)) areas.push('real_estate');
  if (/business\s+law|corporate\s+law|commercial/i.test(text)) areas.push('business');
  if (/bankruptcy/i.test(text)) areas.push('bankruptcy');
  return areas;
}

function estimateRevenueFromTeamSize(teamSize) {
  if (!teamSize || teamSize < 1) return null;
  // Very rough: $150K per team member (conservative for law firms)
  return { value: teamSize * 150_000, source: 'team_size_estimate', confidence: 'low' };
}

// ---------------------------------------------------------------------------
// Package selection (eligibility rules from audit-write.md)
// ---------------------------------------------------------------------------

function selectMarketingTier(revenue, practiceAreas, isAggressive = false) {
  const r = revenue || 0;
  const isPI = practiceAreas.includes('pi');
  const isCriminal = practiceAreas.includes('criminal');

  if (r >= 3_000_000) {
    return { tier: 'Platinum', reason: 'Revenue $3M+' };
  }
  if (r >= 2_000_000 && isAggressive) {
    return { tier: 'Dominate', reason: 'Revenue $2M+ with aggressive goals' };
  }
  if (r >= 1_000_000) {
    // Over $1M → hide Essentials
    if (isAggressive) {
      return { tier: 'Dominate', reason: 'Revenue $1M+ with aggressive goals' };
    }
    return { tier: 'Growth', reason: 'Revenue $1M–$3M' };
  }
  if (r >= 400_000) {
    // PI minimum is Starter
    return { tier: 'Starter', reason: `Revenue $400K–$1M${isPI ? ' (PI minimum Starter)' : ''}` };
  }
  if (r >= 250_000) {
    if (isPI || isCriminal) {
      return { tier: 'Starter', reason: 'PI/Criminal Defense — Essentials hidden, minimum Starter' };
    }
    return { tier: 'Essentials', reason: 'Revenue $250K–$400K' };
  }
  // Under $250K — too early, default to Essentials if we're recommending at all
  if (isPI || isCriminal) {
    return { tier: 'Starter', reason: 'PI/Criminal Defense — minimum Starter regardless of revenue' };
  }
  return { tier: 'Essentials', reason: 'Revenue under $250K — verify client can cover 4 months of services' };
}

function selectCoachingTier(revenue, teamSize, hasOps) {
  const r = revenue || 0;
  const t = teamSize || 0;

  // Under $500K — no FCOO/FCFO products
  if (r < 500_000) {
    if (r < 400_000) {
      return { tier: 'Elite Coach', reason: 'Revenue under $400K' };
    }
    return { tier: 'Elite Coach Plus', reason: 'Revenue $400K–$1M' };
  }

  // Under $1M — no Master's Circle
  if (r < 1_000_000) {
    if (hasOps) {
      return { tier: 'Elite Coach Plus + FCOO Advisor', reason: 'Revenue $400K–$1M, growing team with ops focus' };
    }
    return { tier: 'Elite Coach Plus', reason: 'Revenue $400K–$1M' };
  }

  // $1M+ range
  if (r >= 3_000_000 && t >= 10) {
    return { tier: "Master's Circle + FCOO Partner", reason: 'Revenue $3M+, large team' };
  }
  if (r >= 2_000_000 && t >= 5) {
    return { tier: "Master's Circle + FCOO Director", reason: 'Revenue $2M+, 5+ dedicated staff' };
  }
  if (t >= 5) {
    if (hasOps) {
      return { tier: "Master's Circle + FCOO Advisor", reason: 'Revenue $1M+, 5+ staff with dedicated ops' };
    }
    return { tier: "Master's Circle", reason: 'Revenue $1M+, 5+ dedicated staff' };
  }

  // Under 5 people at $1M+
  if (hasOps) {
    return { tier: 'FCOO Advisor', reason: 'Revenue $1M+, under 5 team, operational focus' };
  }
  return { tier: 'Elite Coach Plus', reason: 'Revenue $1M+, under 5 team members' };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  console.log(`\n=== Pass 1.5: Package Selection — ${FRIENDLY_NAME} ===\n`);

  // -- Load trigger JSON --
  const triggerPath = `triggers/audit-research/${FRIENDLY_NAME}.json`;
  if (!existsSync(triggerPath)) {
    console.warn(`  Trigger file not found: ${triggerPath} — skipping.`);
    process.exit(0);
  }
  const trigger = JSON.parse(readFileSync(triggerPath, 'utf8'));

  // -- Respect manual package override --
  if (trigger.package) {
    console.log(`  Trigger has explicit "package" field — deferring to PACKAGE_HINT, skipping selection.`);
    console.log(`  Package hint: ${trigger.package}`);
    process.exit(0);
  }

  const contactId = trigger.hubspot_contact_id;

  // -- Find research notes --
  let researchText = '';
  if (existsSync(FRIENDLY_NAME)) {
    const files = readdirSync(FRIENDLY_NAME);
    const notesFile = files.find(f => f.toLowerCase().includes('research') && f.endsWith('.txt'));
    if (notesFile) {
      researchText = readFileSync(path.join(FRIENDLY_NAME, notesFile), 'utf8');
      console.log(`  Loaded research notes: ${notesFile} (${researchText.length} chars)`);
    } else {
      console.warn(`  No research notes TXT found in ${FRIENDLY_NAME}/`);
    }
  } else {
    console.warn(`  Firm folder ${FRIENDLY_NAME}/ does not exist yet.`);
  }

  // ---------------------------------------------------------------------------
  // REVENUE HIERARCHY
  // ---------------------------------------------------------------------------
  let revenueResult = null;

  // Level 1 & 2: Research notes (transcript is ground truth)
  const notesRevenue = extractRevenueFromNotes(researchText);
  if (notesRevenue) {
    revenueResult = notesRevenue;
    console.log(`  Revenue source: ${notesRevenue.source} → $${notesRevenue.value.toLocaleString()} (${notesRevenue.confidence} confidence)`);
  } else {
    console.log(`  No revenue found in research notes — checking HubSpot...`);
  }

  // Level 3–6: HubSpot fallback
  if (!revenueResult || revenueResult.confidence === 'low') {
    const hsRevenue = await fetchHubSpotRevenue(contactId);
    if (hsRevenue) {
      if (!revenueResult || revenueResult.confidence === 'low') {
        // HubSpot medium > research notes low
        revenueResult = hsRevenue;
        console.log(`  Revenue source: ${hsRevenue.source} → $${hsRevenue.value.toLocaleString()} (${hsRevenue.confidence} confidence) [label: "${hsRevenue.rawLabel}"]`);
      }
    } else if (!revenueResult) {
      console.warn(`  No HubSpot revenue data available.`);
    }
  }

  // Level 7: Team size estimate
  const teamSize = parseTeamSize(researchText);
  if (!revenueResult && teamSize) {
    revenueResult = estimateRevenueFromTeamSize(teamSize);
    console.log(`  Revenue source: team size estimate (${teamSize} members) → $${revenueResult.value.toLocaleString()} (low confidence)`);
  }

  if (!revenueResult) {
    console.warn(`  Could not determine revenue — cannot produce package_decision.json.`);
    console.warn(`  Set "package" field in trigger JSON to use PACKAGE_HINT fallback.`);
    process.exit(0);
  }

  // ---------------------------------------------------------------------------
  // ELIGIBILITY + SELECTION
  // ---------------------------------------------------------------------------
  const revenue      = revenueResult.value;
  const practiceAreas = detectPracticeAreas(researchText);
  const teamSizeFinal = teamSize || null;
  const dedicatedOps  = hasDedicatedOps(researchText);

  console.log(`  Revenue estimate: $${revenue.toLocaleString()}`);
  console.log(`  Practice areas: ${practiceAreas.join(', ') || '(unknown)'}`);
  console.log(`  Team size: ${teamSizeFinal ?? '(unknown)'}`);
  console.log(`  Dedicated ops: ${dedicatedOps}`);

  const marketingResult = selectMarketingTier(revenue, practiceAreas);
  const coachingResult  = selectCoachingTier(revenue, teamSizeFinal, dedicatedOps);

  const mTier = marketingResult.tier;
  const cTier = coachingResult.tier;
  const mPrices = MARKETING[mTier];
  const cPrices = COACHING[cTier];

  const total = (mPrices?.bundled || 0) + (cPrices?.bundled || 0);

  // Confidence: overall is min of revenue confidence + data availability
  const overallConfidence = revenueResult.confidence === 'high' ? 'high'
    : revenueResult.confidence === 'medium' && teamSizeFinal ? 'medium'
    : 'low';

  const eligibilityNotes = [
    `Revenue: $${revenue.toLocaleString()} (${revenueResult.source})`,
    `Marketing: ${mTier} — ${marketingResult.reason}`,
    `Coaching: ${cTier} — ${coachingResult.reason}`,
    revenue < 500_000 ? 'FCOO/FCFO hidden (revenue under $500K)' : null,
    revenue < 1_000_000 ? "Master's Circle hidden (revenue under $1M)" : null,
    revenue > 1_000_000 ? 'Essentials hidden (revenue over $1M)' : null,
    practiceAreas.includes('pi') ? 'PI firm: Essentials hidden, minimum Starter' : null,
    teamSizeFinal !== null && teamSizeFinal < 5 ? "Master's Circle hidden (team under 5)" : null,
    revenueResult.rawLabel ? `HubSpot label: "${revenueResult.rawLabel}"` : null,
  ].filter(Boolean).join('; ');

  const decision = {
    marketing_tier:          mTier,
    marketing_bundled:       mPrices?.bundled   ?? null,
    marketing_retail:        mPrices?.retail    ?? null,
    coaching_tier:           cTier,
    coaching_bundled:        cPrices?.bundled   ?? null,
    coaching_retail:         cPrices?.retail    ?? null,
    total_bundled:           total,
    ad_spend_min:            mPrices?.adSpendMin ?? null,
    ad_spend_max:            mPrices?.adSpendMax ?? null,
    revenue_estimate:        revenue,
    revenue_source:          revenueResult.source,
    revenue_label:           revenueResult.rawLabel || `$${revenue.toLocaleString()}`,
    confidence:              overallConfidence,
    eligibility_notes:       eligibilityNotes,
    generated_at:            new Date().toISOString(),
  };

  const outPath = path.join(FRIENDLY_NAME, 'package_decision.json');
  writeFileSync(outPath, JSON.stringify(decision, null, 2));

  console.log(`\n  ✓ package_decision.json written to ${outPath}`);
  console.log(`    Marketing: ${mTier} ($${mPrices?.bundled?.toLocaleString()}/mo bundled)`);
  console.log(`    Coaching:  ${cTier} ($${cPrices?.bundled?.toLocaleString()}/mo bundled)`);
  console.log(`    Total:     $${total.toLocaleString()}/mo`);
  console.log(`    Confidence: ${overallConfidence}`);
}

main().catch(err => {
  console.error(`  select-package.mjs error: ${err.message}`);
  // Exit 0 so pipeline continues to Pass 2 (which falls back to PACKAGE_HINT)
  process.exit(0);
});
