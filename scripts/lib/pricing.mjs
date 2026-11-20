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
 *   - `addOn: true` products (Growth Academy) have one price and only sell
 *     with another core package. They DO count toward a bundle (Stephanie,
 *     Nov 2026: marketing + Growth Academy gets marketing's package price).
 *
 * Field meaning in package_decision.json: `*_price_bundled` is the price the
 * client is CHARGED (bundled or stand-alone, per the rule), `*_price_retail`
 * is the stand-alone price. Savings = retail − charged.
 */

// ─── Catalog ──────────────────────────────────────────────────────────────────

// One-time setup fees (2026 pricing sheet). Charged once, shown on the
// investment slide and counted in the year-one total. `waivable` follows the
// sheet's rule "Set-Up Fees Can Be Waived for All Packages EXCEPT Bookkeeping";
// a waiver is the seller's call (package_decision.json `setup_fee_waived`).
const BOOTCAMP = { amount: 497, label: 'Video Ads Express Bootcamp', waivable: true };
const AVATAR = { amount: 1850, label: 'AI Avatar setup', waivable: true };
const books = amount => ({ amount, label: 'Bookkeeping setup', waivable: false });
// Managed Financials setup fees can't be waived either (Jaime, Nov 2026).
const fcfoSetup = amount => ({ amount, label: 'Managed Financials setup', waivable: false });
const adsSetup = tier => (tier === 'Essentials' ? BOOTCAMP : AVATAR);

const fsm = (tier, bundled, standalone) => ({ name: `Full Service Marketing — ${tier}`, category: 'marketing', tier, bundled, standalone, setup: adsSetup(tier) });
const ads = (tier, bundled, standalone) => ({ name: `Paid Ads ${tier}`, category: 'marketing', tier: `Paid Ads ${tier}`, bundled, standalone, setup: adsSetup(tier) });
const web = (tier, bundled, standalone) => ({ name: `Web + SEO ${tier}`, category: 'marketing', tier: `Web + SEO ${tier}`, bundled, standalone });
export const managedOps = tier => `Managed Operations Tier ${tier}`;
const mo = (tier, bundled, standalone, minRev, minTeam) => ({ name: managedOps(tier), category: 'coaching', family: 'Managed Operations', moTier: tier, bundled, standalone, minRev, minTeam });
const retiredTo = (name, tier) => ({ name, category: 'coaching', retired: true, replacement: managedOps(tier) });

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

  // Managed Operations (Managed Operations tab, 2026 sheet — Nov 2026 GTM).
  // One packaged product that replaces Elite Coach, Elite Coach Plus,
  // Master's Circle, Coach Essentials and FCOO. Every tier includes Growth
  // Academy (Tier 3: Master's Circle Growth Academy), quarterly planning and
  // projects, and monthly working sessions. The tab lists no setup fee.
  mo(1, 3297, 3497,   250_000, null),
  mo(2, 5497, 5997,   500_000, 5),
  mo(3, 7497, 7997, 1_000_000, 10),
  // Growth Academy add-ons: one price, "ONLY SOLD w/OTHER CORE PACKAGES" —
  // never on their own, but they count as a service for the bundle rule.
  { name: 'Growth Academy',                  category: 'coaching', addOn: true, price: 1497 },
  { name: "Growth Academy Master's Circle",  category: 'coaching', addOn: true, price: 2497 },

  // Managed Financials (Managed Financials tab). Fractional CFO keeps its
  // Advisor / Director / Partner names (= the tab's Level 1 / 2 / 3; the deck's
  // ProfitOS slides key off them). Above $4M is a custom agreement. Setup
  // fees can never be waived.
  { name: 'FCFO Advisor',          category: 'coaching', bundled: 3497, standalone: 3997,  minRev: 500_000,   setup: fcfoSetup(1000) },
  { name: 'FCFO Director',         category: 'coaching', bundled: 5497, standalone: 5997,  minRev: 1_000_000, setup: fcfoSetup(1500) },
  { name: 'FCFO Partner',          category: 'coaching', bundled: 9997, standalone: 10997, minRev: 2_000_000, setup: fcfoSetup(2000) },
  // Bookkeeping. Sold on the coaching line. Setup fees can never be waived.
  // Level 4 ($4M+) is custom-scoped — never priced here.
  { name: 'Bookkeeping Level 1',   category: 'coaching', bundled: 1997, standalone: 2997, setup: books(2000) },
  { name: 'Bookkeeping Level 2',   category: 'coaching', bundled: 2997, standalone: 3997, minRev: 1_000_000, setup: books(3500) },
  { name: 'Bookkeeping Level 3',   category: 'coaching', bundled: 3997, standalone: 4997, minRev: 2_000_000, setup: books(5000) },
  { name: 'Bookkeeping Level 4',   category: 'coaching', custom: true, minRev: 4_000_000 },

  // Retired by Managed Operations (Nov 2026). Old decks, Slack replies and
  // research notes still name them, so they resolve to the closest tier.
  // "Master's Circle" on its own is NOT retired — it means the Growth Academy
  // Master's Circle add-on (or Tier 3, which includes it; Lynne, Nov 2026) —
  // see the alias below.
  retiredTo('Coach Essentials', 1), retiredTo('Coach Essentials Plus', 1),
  retiredTo('Elite Coach', 1), retiredTo('Elite Coach Plus', 1),
  retiredTo('FCOO Advisor', 1), retiredTo('FCOO Director', 2), retiredTo('FCOO Partner', 3),
  retiredTo('Elite Coach + FCOO Advisor', 1), retiredTo('Elite Coach + FCOO Director', 2), retiredTo('Elite Coach + FCOO Partner', 3),
  retiredTo("Master's Circle + FCOO Advisor", 3), retiredTo("Master's Circle + FCOO Director", 3), retiredTo("Master's Circle + FCOO Partner", 3),

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
  [/^(?:managed operations|managed ops|mo) (?:tier|level|t|l) ?([1-3])$/, m => managedOps(m[1])],
  [/^(?:growth academy (?:master's circle|mc)|(?:master's circle|mc) growth academy)$/, "Growth Academy Master's Circle"],
  [/^(?:fcoo|fractional coo) (advisor|director|partner)$/, m => `FCOO ${cap(m[1])}`],
  [/^(?:fcfo|fractional cfo) (advisor|director|partner)$/, m => `FCFO ${cap(m[1])}`],
  [/^(?:fcfo|fractional cfo|managed financials|financial strategy) (?:level|l) ?([1-3])$/, m => `FCFO ${['Advisor', 'Director', 'Partner'][m[1] - 1]}`],
  [/^ecp$/, 'Elite Coach Plus'],
  [/^(?:bookkeeping|bk) (?:level|l) ?([1-4])$/, m => `Bookkeeping Level ${m[1]}`],
  [/^master'?s circle$|^mc$/, "Growth Academy Master's Circle"],
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
 * catalog entry stays whole.
 * Returns [{ raw, product, seats }].
 */
export function resolveName(rawName) {
  if (!rawName) return [];
  const whole = resolveOne(rawName);
  if (whole.product) return [{ raw: rawName, ...whole }];
  return rawName.split(/\s\+\s(?![^()]*\))/).map(part => ({ raw: part.trim(), ...resolveOne(part.trim()) }));
}

/**
 * Retired coaching names map to Managed Operations, so "Elite Coach + FCOO
 * Director" can arrive as two tiers. A package has one Managed Operations
 * tier: keep the highest.
 */
function collapseManagedOps(parts, notes) {
  const mo = parts.filter(p => p.product?.family === 'Managed Operations');
  if (mo.length < 2) return parts;
  const keep = mo.reduce((a, b) => (b.product.moTier > a.product.moTier ? b : a));
  notes.push(`${mo.map(p => p.raw).join(' + ')} → one Managed Operations package: ${keep.product.name}.`);
  return parts.filter(p => p.product?.family !== 'Managed Operations' || p === keep);
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
    resolved[key] = { line, parts: collapseManagedOps(parts, notes) };
  }

  // A Growth Academy add-on the Managed Operations tier already includes is
  // dropped (every tier includes Growth Academy; Tier 3 includes Master's
  // Circle Growth Academy, so "Tier 3 + Master's Circle" is just Tier 3).
  const moTier = Object.values(resolved).flatMap(r => r?.parts ?? []).find(p => p.product?.family === 'Managed Operations')?.product.moTier;
  if (moTier) {
    for (const r of Object.values(resolved)) {
      if (!r) continue;
      r.parts = r.parts.filter(p => {
        const included = p.product?.addOn && (p.product.name === 'Growth Academy' || moTier === 3);
        if (included) notes.push(`${p.raw} is already included in Managed Operations Tier ${moTier} — not charged separately.`);
        return !included;
      });
    }
    for (const key of Object.keys(resolved)) if (resolved[key] && !resolved[key].parts.length) resolved[key] = null;
  }

  // Growth Academy add-ons only sell with another core package.
  const all = Object.values(resolved).flatMap(r => r?.parts ?? []);
  const hasCore = all.some(p => !p.product || !p.product.addOn);

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
      if (p.custom) {
        ok = false;
        unpriced.push(p.name);
        notes.push(`${p.name} is custom-priced — it must be scoped by Sales before it can be quoted.`);
        continue;
      }
      if (p.addOn) {
        if (!hasCore) {
          ok = false;
          unpriced.push(p.name);
          notes.push(p.name === "Growth Academy Master's Circle"
            ? `Master's Circle can't be sold on its own — ask the rep: Managed Operations Tier 3 (includes Master's Circle Growth Academy), or the Growth Academy Master's Circle add-on with another service.`
            : `${p.name} is only sold with another core package (Managed Operations, Managed Financials, marketing or AI) — add one or choose Managed Operations instead.`);
          continue;
        }
        charged += p.price; retail += p.price; // one price, bundled or not
        continue;
      }
      if (p.fixed) {
        const a = aiwpPrice(p, part.seats);
        charged += a.price; seats = a.seats;
        retailKnown = false; // AI Workforce Pro has no stand-alone price
        continue;
      }
      if (mode === 'bundled') {
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

  // One-time setup fees, one per catalog product.
  const setupFees = [];
  for (const [key, r] of Object.entries(resolved)) {
    for (const part of r?.parts ?? []) {
      const f = part.product?.setup;
      if (f?.amount > 0) setupFees.push({ line: key, product: part.product.name, label: f.label, amount: f.amount, waivable: f.waivable !== false });
      // OmniSocial AI isn't in the catalog (priced by hand from audit-write.md) but every package carries the $1,850 setup fee.
      else if (!part.product && /^omnisocial/i.test(part.raw)) setupFees.push({ line: key, product: part.raw, label: 'OmniSocial AI setup', amount: 1850, waivable: true });
    }
  }

  const totalSavings = Object.values(out).reduce((s, l) => s + (l?.savings ?? 0), 0);

  if (mode === 'standalone' && eligibleCount === 1) {
    notes.push('Only one bundle-eligible product in this package — stand-alone pricing applied, no bundle savings.');
  }
  if (Object.values(resolved).some(r => r?.parts.some(p => p.product?.bundleEligible === false && !p.product.addOn))) {
    notes.push('AI Workforce Pro – Starter does not count toward bundle pricing.');
  }
  if (!unpriced.length && total > 0 && total < MIN_MRR) {
    notes.push(`Total $${total.toLocaleString()}/mo is under the $${MIN_MRR.toLocaleString()}/mo minimum — review with sales rep.`);
  }

  return { lines: out, mode, eligibleCount, total, totalSavings, setupFees, unpriced, notes };
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

  // Setup fees. The seller can waive a waivable fee through the Slack review
  // by listing the product in `setup_fee_waived`; the fee then stays on the
  // slide marked waived and counts $0. Bookkeeping fees can't be waived.
  const waived = new Set((decision.setup_fee_waived ?? []).map(n => resolveOne(n).product?.name ?? n));
  decision.setup_fees = r.setupFees.map(f => {
    const isWaived = f.waivable && waived.has(f.product);
    if (!f.waivable && waived.has(f.product)) r.notes.push(`${f.label} for ${f.product} can't be waived — still charged.`);
    return { ...f, waived: isWaived, charged: isWaived ? 0 : f.amount };
  });
  decision.setup_total = decision.setup_fees.reduce((s, f) => s + f.charged, 0);
  return r.notes;
}
