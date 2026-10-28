/**
 * SMB Team product catalog + the bundle pricing rule.
 *
 * Single source of truth for prices used by code (select-package.mjs,
 * reprice.mjs). Keep in sync with the pricing tables in
 * .claude/commands/audit-write.md and Design Files/Scoping_and_Ad_Spend_Guide.md.
 *
 * Bundle rule (decided by Sales/Greta, Oct 2026):
 *   - A package gets bundled (discounted) prices when it has 2 or more
 *     bundle-eligible products. Otherwise every product is charged its
 *     stand-alone price and savings are $0.
 *   - Products with `bundleEligible: false` never count toward a bundle
 *     (AI Workforce Pro – Starter). To add another exception, set the flag.
 *   - `standalone: null` + no `fixed` price means the product can't be sold
 *     on its own yet (e.g. Paid Ads Essentials — awaiting a price from Sales).
 *   - `retired: true` products are never priced; they resolve to `replacement`.
 *
 * Field meaning in package_decision.json: `*_price_bundled` is the price the
 * client is CHARGED (bundled or stand-alone, per the rule), `*_price_retail`
 * is the stand-alone price. Savings = retail − charged.
 */

// ─── Catalog ──────────────────────────────────────────────────────────────────

const fsm = (tier, bundled, standalone) => ({ name: `Full Service Marketing — ${tier}`, category: 'marketing', tier, bundled, standalone });
const ads = (tier, bundled, standalone) => ({ name: `Paid Ads ${tier}`, category: 'marketing', tier: `Paid Ads ${tier}`, bundled, standalone });
const web = (tier, bundled, standalone) => ({ name: `Web + SEO ${tier}`, category: 'marketing', tier: `Web + SEO ${tier}`, bundled, standalone });

export const CATALOG = [
  // Marketing — Full Service
  fsm('Essentials', 3497, 3797),
  fsm('Starter',    4997, 5697),
  fsm('Growth',     7497, 8997),
  fsm('Dominate',  10497, 12497),
  fsm('Platinum',  15997, 18997),
  // Marketing — sub-packages (Scoping_and_Ad_Spend_Guide.md "Sub-Package" tables)
  ads('Essentials', 1997, null),
  ads('Starter',    2497, 3497),
  ads('Growth',     4497, 5497),
  ads('Dominate',   6997, 7997),
  ads('Platinum',   8997, 9997),
  web('Essentials', 1997, null),
  web('Starter',    3497, 3997),
  web('Growth',     4897, 5897),
  web('Dominate',   6997, 7997),
  web('Platinum',   9597, 11497),

  // Coaching / advisory
  { name: 'Coach Essentials',      category: 'coaching', bundled: 1000, standalone: null },
  { name: 'Coach Essentials Plus', category: 'coaching', bundled: 1997, standalone: 2497 },
  { name: 'Elite Coach',           category: 'coaching', bundled: 2600, standalone: 3497 },
  { name: 'Elite Coach Plus',      category: 'coaching', bundled: 3200, standalone: 3497 },
  { name: "Master's Circle",       category: 'coaching', bundled: 4600, standalone: 4997 },
  { name: 'FCOO Advisor',          category: 'coaching', bundled: 3297, standalone: 3797, minRev: 500_000 },
  { name: 'FCOO Director',         category: 'coaching', bundled: 4997, standalone: 5797, minRev: 1_000_000 },
  { name: 'FCOO Partner',          category: 'coaching', retired: true, replacement: 'FCOO Director' },
  { name: 'FCFO Advisor',          category: 'coaching', bundled: 3297, standalone: 3797, minRev: 400_000 },
  { name: 'FCFO Director',         category: 'coaching', bundled: 4997, standalone: 5797, minRev: 1_000_000 },
  { name: 'FCFO Partner',          category: 'coaching', bundled: 8997, standalone: 9997, minRev: 3_000_000 },
  // Coaching packages Sales prices as a pair (audit-write.md non-marketing table).
  // `parts` = how many products they count as toward the bundle rule.
  { name: 'Elite Coach + FCOO Advisor',      category: 'coaching', bundled: 5694, standalone: null, parts: 2, packaged: true },
  { name: 'Elite Coach + FCOO Director',     category: 'coaching', bundled: 7394, standalone: null, parts: 2, packaged: true },
  { name: 'Elite Coach + FCOO Partner',      category: 'coaching', retired: true, replacement: 'Elite Coach + FCOO Director' },
  { name: "Master's Circle + FCOO Advisor",  category: 'coaching', bundled: 6694, standalone: null, parts: 2, packaged: true },
  { name: "Master's Circle + FCOO Director", category: 'coaching', bundled: 8394, standalone: null, parts: 2, packaged: true },
  { name: "Master's Circle + FCOO Partner",  category: 'coaching', retired: true, replacement: "Master's Circle + FCOO Director" },

  // Legal AI Workforce. AI Workforce Pro is priced by seat and has one price
  // whether bundled or not (`fixed`), so it never shows savings.
  { name: 'AI Workforce Pro – Starter', category: 'law', fixed: true, perUser: 350, maxUsers: 4, bundleEligible: false },
  { name: 'AI Workforce Pro',           category: 'law', fixed: true, base: 1597, baseUsers: 5, perExtraUser: 120 },
  { name: 'Fractional CTO Level 1',     category: 'law', bundled: 3297, standalone: 3797, minRev: 400_000 },
  { name: 'Fractional CTO Level 2',     category: 'law', bundled: 4997, standalone: 5797, minRev: 1_000_000 },
  { name: 'Fractional CTO Level 3',     category: 'law', bundled: 8997, standalone: 9997, minRev: 3_000_000 },
];

const BY_NAME = new Map(CATALOG.map(p => [p.name, p]));
export const getProduct = name => BY_NAME.get(name) ?? null;

export const MIN_MRR = 2497;

// ─── Name resolution ──────────────────────────────────────────────────────────
// Names in package_decision.json are often typed by the AI ("Paid Ads — Starter
// (stand-alone)", "AI Essentials — Starter", "Fractional CTO Level 1 + AI
// Workforce Pro (15 seats)"), so normalize before looking up.

function normalize(s) {
  return s
    .toLowerCase()
    .replace(/\((?:stand[- ]?alone|standalone|bundled?)\)/g, ' ')
    .replace(/\bpackage\b/g, ' ')
    .replace(/[–—]/g, '-')
    .replace(/\s*-\s*/g, ' ')
    .replace(/[’']/g, "'")
    .replace(/\s+/g, ' ')
    .trim();
}

// Legacy / shorthand names → catalog name. Checked against the normalized string.
const ALIASES = [
  [/^(?:ai essentials )?(?:starter )?ai workforce pro starter$|^aiwp starter$|^ai essentials starter$|^starter$/, 'AI Workforce Pro – Starter'],
  [/^(?:ai essentials )?(?:base )?ai workforce pro(?: base)?$|^aiwp(?: base)?$|^ai essentials(?: base)?$/, 'AI Workforce Pro'],
  [/^(?:ai accelerator l1 )?(?:fractional cto|fcto) (?:level|l) ?1$|^ai accelerator l1$/, 'Fractional CTO Level 1'],
  [/^(?:ai accelerator l2 )?(?:fractional cto|fcto) (?:level|l) ?2$|^ai accelerator l2$/, 'Fractional CTO Level 2'],
  [/^(?:ai enterprise )?(?:fractional cto|fcto) (?:level|l) ?3$|^ai enterprise$/, 'Fractional CTO Level 3'],
  [/^full service marketing (essentials|starter|growth|dominate|platinum)$/, m => `Full Service Marketing — ${cap(m[1])}`],
  [/^(?:fsm )(essentials|starter|growth|dominate|platinum)$/, m => `Full Service Marketing — ${cap(m[1])}`],
  [/^paid ads (essentials|starter|growth|dominate|platinum)$/, m => `Paid Ads ${cap(m[1])}`],
  [/^web \+ seo (essentials|starter|growth|dominate|platinum)$/, m => `Web + SEO ${cap(m[1])}`],
  [/^(?:fcoo|fractional coo) (advisor|director|partner)$/, m => `FCOO ${cap(m[1])}`],
  [/^(?:fcfo|fractional cfo) (advisor|director|partner)$/, m => `FCFO ${cap(m[1])}`],
  [/^ecp$/, 'Elite Coach Plus'],
  [/^masters circle$|^mc$/, "Master's Circle"],
];
const cap = s => s[0].toUpperCase() + s.slice(1);

const NORMALIZED = new Map(CATALOG.map(p => [normalize(p.name), p.name]));

/**
 * Resolve one product name (no " + ") to a catalog entry.
 * Returns { product, seats } or { product: null } when unknown.
 * Seat counts written inline, e.g. "AI Workforce Pro (15 seats)", are returned as `seats`.
 */
export function resolveOne(rawName) {
  if (!rawName) return { product: null };
  const seatMatch = rawName.match(/\((\d+)\s*(?:seats?|users?)\)/i);
  const seats = seatMatch ? parseInt(seatMatch[1], 10) : null;
  const n = normalize(rawName.replace(/\((\d+)\s*(?:seats?|users?)\)/i, ' '));
  if (NORMALIZED.has(n)) return { product: BY_NAME.get(NORMALIZED.get(n)), seats };
  for (const [re, target] of ALIASES) {
    const m = n.match(re);
    if (m) return { product: BY_NAME.get(typeof target === 'function' ? target(m) : target), seats };
  }
  return { product: null, seats };
}

/**
 * Split a package-field name into catalog products. A name that is itself a
 * catalog package (e.g. "Elite Coach + FCOO Advisor") stays whole.
 * Returns [{ raw, product, seats }].
 */
export function resolveName(rawName) {
  if (!rawName) return [];
  const whole = resolveOne(rawName);
  if (whole.product) return [{ raw: rawName, ...whole }];
  return rawName.split(/\s\+\s(?![^()]*\))/).map(part => ({ raw: part.trim(), ...resolveOne(part.trim()) }));
}

/** Follow `retired` → `replacement`. Returns { product, retiredFrom }. */
export function unretire(product) {
  if (!product?.retired) return { product, retiredFrom: null };
  return { product: getProduct(product.replacement), retiredFrom: product.name };
}

// ─── Pricing ──────────────────────────────────────────────────────────────────

function aiwpPrice(p, seats) {
  if (p.perUser) {
    const s = Math.min(Math.max(seats ?? 1, 1), p.maxUsers);
    return { price: p.perUser * s, seats: s };
  }
  const s = Math.max(seats ?? p.baseUsers, p.baseUsers);
  return { price: p.base + p.perExtraUser * (s - p.baseUsers), seats: s };
}

/**
 * Price a whole package.
 *
 * @param lines  { marketing, coaching, law } — each { name, seats?, price? } or null.
 *               `price` is only used for products the catalog doesn't know.
 * @returns {
 *   lines: { marketing, coaching, law } each { name, charged, retail, savings, seats } or null,
 *   mode: 'bundled' | 'standalone', eligibleCount, total, totalSavings,
 *   unpriced: [names that can't be sold alone], notes: [strings]
 * }
 */
export function pricePackage(lines) {
  const notes = [];
  const unpriced = [];

  // Resolve every line into catalog parts (retired → replacement).
  const resolved = {};
  for (const key of ['marketing', 'coaching', 'law']) {
    const line = lines[key];
    if (!line?.name) { resolved[key] = null; continue; }
    const parts = resolveName(line.name).map(part => {
      const { product, retiredFrom } = unretire(part.product);
      if (retiredFrom) notes.push(`${retiredFrom} is retired — using ${product.name} instead.`);
      return { ...part, product, seats: part.seats ?? line.seats ?? null };
    });
    resolved[key] = { line, parts };
  }

  // Count bundle-eligible products.
  let eligibleCount = 0;
  for (const r of Object.values(resolved)) {
    if (!r) continue;
    for (const part of r.parts) {
      if (!part.product) { eligibleCount += 1; continue; }
      if (part.product.bundleEligible === false) continue;
      eligibleCount += part.product.parts ?? 1;
    }
  }
  const mode = eligibleCount >= 2 ? 'bundled' : 'standalone';

  const out = {};
  for (const [key, r] of Object.entries(resolved)) {
    if (!r) { out[key] = null; continue; }
    // savings is summed per product, so one product without a stand-alone price
    // (AI Workforce Pro) doesn't hide the savings on the others.
    let charged = 0, retail = 0, retailKnown = true, savings = 0, seats = null, ok = true;
    const names = [];
    for (const part of r.parts) {
      const p = part.product;
      if (!p) {
        // Unknown to the catalog — keep whatever price was given, don't guess.
        const given = r.parts.length === 1 ? r.line.price : null;
        notes.push(`"${part.raw}" isn't in the pricing catalog — price not checked automatically${given != null ? ` (kept $${given.toLocaleString()}/mo)` : ''}.`);
        names.push(part.raw);
        if (given == null) { ok = false; continue; }
        charged += given; retailKnown = false;
        continue;
      }
      names.push(p.name);
      if (p.fixed) {
        const a = aiwpPrice(p, part.seats);
        charged += a.price; seats = a.seats;
        retailKnown = false; // AI Workforce Pro has no stand-alone price
        continue;
      }
      if (mode === 'bundled' || p.packaged) {
        charged += p.bundled;
        if (p.standalone != null) { retail += p.standalone; savings += p.standalone - p.bundled; } else retailKnown = false;
      } else if (p.standalone != null) {
        charged += p.standalone; retail += p.standalone;
      } else {
        ok = false;
        unpriced.push(p.name);
        notes.push(`${p.name} has no stand-alone price and can't be sold on its own yet — pair it with another product or choose a different tier (stand-alone price awaiting Sales).`);
      }
    }
    out[key] = {
      name: names.join(' + '),
      charged: ok ? charged : null,
      retail: ok && retailKnown ? retail : null,
      savings: ok && savings > 0 ? savings : (ok && retailKnown ? 0 : null),
      seats,
    };
  }

  const total = Object.values(out).reduce((s, l) => s + (l?.charged ?? 0), 0);
  const totalSavings = Object.values(out).reduce((s, l) => s + (l?.savings ?? 0), 0);

  if (mode === 'standalone' && eligibleCount === 1) {
    notes.push('Only one bundle-eligible product in this package — stand-alone pricing applied, no bundle savings.');
  }
  if (Object.values(resolved).some(r => r?.parts.some(p => p.product?.bundleEligible === false))) {
    notes.push('AI Workforce Pro – Starter does not count toward bundle pricing.');
  }
  if (!unpriced.length && total > 0 && total < MIN_MRR) {
    notes.push(`Total $${total.toLocaleString()}/mo is under the $${MIN_MRR.toLocaleString()}/mo minimum — review with sales rep.`);
  }

  return { lines: out, mode, eligibleCount, total, totalSavings, unpriced, notes };
}

/**
 * Apply pricePackage() to a package_decision object in place: rewrites the
 * marketing/coaching/law name + price fields and the totals.
 * Returns the pricing notes (callers decide where to put them).
 */
export function applyPricing(decision) {
  const lineFrom = prefix => decision[`${prefix}_name`]
    ? { name: decision[`${prefix}_name`], seats: decision[`${prefix}_seats`] ?? null, price: decision[`${prefix}_price_bundled`] ?? null }
    : null;
  const r = pricePackage({ marketing: lineFrom('marketing'), coaching: lineFrom('coaching'), law: lineFrom('law') });

  for (const key of ['marketing', 'coaching', 'law']) {
    const l = r.lines[key];
    if (!l) continue;
    decision[`${key}_name`] = l.name;
    decision[`${key}_price_bundled`] = l.charged;
    decision[`${key}_price_retail`] = l.retail;
    if (key !== 'law') decision[`${key}_savings`] = l.savings;
    if (key === 'law' && l.seats != null) decision.law_seats = l.seats;
  }
  if (r.lines.law) {
    const parts = resolveName(r.lines.law.name);
    decision.law_tier = parts.map(p => p.product?.name ?? p.raw).join(' + ');
  }
  if (r.lines.marketing) {
    const p = resolveName(r.lines.marketing.name)[0]?.product;
    if (p?.tier) decision.marketing_tier = p.tier;
  }

  decision.pricing_mode = r.mode;
  decision.bundle_eligible_count = r.eligibleCount;
  decision.total_bundled = r.total;
  decision.total_savings = r.totalSavings > 0 ? r.totalSavings : null;
  decision.unpriced_products = r.unpriced;
  if (r.unpriced.length) decision.needs_seller_input = true;
  return r.notes;
}
