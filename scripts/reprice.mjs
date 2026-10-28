#!/usr/bin/env node
/**
 * Re-price a firm's package_decision.json after its products change.
 *
 * The Slack seller-reply bots choose WHICH products go in the package (they
 * edit the *_name / law_seats fields); this script sets every price, savings
 * figure and total from scripts/lib/pricing.mjs, applying the bundle rule
 * (stand-alone prices when fewer than 2 bundle-eligible products remain).
 * audit-write.yml also runs it before Pass 2 builds the deck.
 *
 * Usage:
 *   node scripts/reprice.mjs <friendly-name>                   re-price only
 *   node scripts/reprice.mjs <friendly-name> --revenue 300000  also record seller-confirmed revenue
 *
 * Prints a JSON summary on stdout (for the bots to quote in Slack).
 * Exit codes: 0 ok, 1 missing file / bad args.
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';
import { applyPricing } from './lib/pricing.mjs';

const args = process.argv.slice(2);
const friendlyName = args.find(a => !a.startsWith('--'));
const revIdx = args.indexOf('--revenue');
const confirmedRevenue = revIdx >= 0 ? Number(String(args[revIdx + 1]).replace(/[$,]/g, '')) : null;

if (!friendlyName) {
  console.error('Usage: node scripts/reprice.mjs <friendly-name> [--revenue <annual dollars>]');
  process.exit(1);
}
const path = join(friendlyName, 'package_decision.json');
if (!existsSync(path)) {
  console.error(`ERROR: ${path} not found`);
  process.exit(1);
}
if (revIdx >= 0 && !(confirmedRevenue > 0)) {
  console.error('ERROR: --revenue needs a positive dollar amount, e.g. --revenue 300000');
  process.exit(1);
}

const decision = JSON.parse(readFileSync(path, 'utf8'));
decision.selection_notes ??= [];

if (confirmedRevenue) {
  decision.revenue_effective = confirmedRevenue;
  decision.revenue_source = 'seller_confirmed';
  decision.revenue_verified = true;
  decision.needs_revenue_confirmation = false;
  decision.selection_notes.push(`Revenue confirmed by seller: $${confirmedRevenue.toLocaleString()}.`);
}

const anyProduct = decision.marketing_name || decision.coaching_name || decision.law_name;
if (anyProduct) {
  // Products are set, so the package no longer waits on the seller for that —
  // unless a product can't be priced on its own (applyPricing sets it again).
  decision.needs_seller_input = false;
  for (const note of applyPricing(decision)) {
    if (!decision.selection_notes.includes(note)) decision.selection_notes.push(note);
  }
}

writeFileSync(path, JSON.stringify(decision, null, 2));

console.log(JSON.stringify({
  marketing: decision.marketing_name ? { name: decision.marketing_name, price: decision.marketing_price_bundled } : null,
  coaching: decision.coaching_name ? { name: decision.coaching_name, price: decision.coaching_price_bundled } : null,
  ai: decision.law_name ? { name: decision.law_name, seats: decision.law_seats, price: decision.law_price_bundled } : null,
  pricing_mode: decision.pricing_mode,
  total: decision.total_bundled,
  savings: decision.total_savings,
  unpriced_products: decision.unpriced_products ?? [],
  needs_revenue_confirmation: !!decision.needs_revenue_confirmation,
}, null, 2));
