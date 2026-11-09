/**
 * investment.test.mjs — scripts/lib/investment.mjs (ad spend range, return
 * projection, year-one total).
 *
 * Run: node --test scripts/tests/investment.test.mjs
 *
 * The two firm cases use the figures said on real discovery calls:
 * RCG Law Group (Ryan Gregerson, Oct 14 2026) and O'Brien Law Group (Oct 26 2026).
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { computeInvestment, parseInvestmentInputs, parseDollars, applyInvestment } from '../lib/investment.mjs';

const growthPlusElite = {
  marketing_name: 'Full Service Marketing — Growth', marketing_price_bundled: 7497, marketing_price_retail: 8997,
  coaching_name: 'Elite Coach', coaching_price_bundled: 2600, coaching_price_retail: 3497,
  total_bundled: 10097, total_savings: 2397, pricing_mode: 'bundled', revenue_effective: 5_000_000,
};
const ryanInputs = {
  practiceArea: 'Family Law', geoTier: 4, competitiveness: 'High', spanish: false,
  currentAdSpend: 25_000, currentCostPerCase: 4_500, caseValue: 9_100, closeRate: 0.21,
};

test('RCG: holds today\'s $25K spend, caps at the Growth $50K, projects at the stated cost per case', () => {
  const inv = computeInvestment(growthPlusElite, ryanInputs);
  assert.equal(inv.monthly_total, 10097);
  assert.equal(inv.year_one_total, 121164);
  assert.equal(inv.ad_spend.conservative, 25_000);
  assert.equal(inv.ad_spend.aggressive, 50_000);
  assert.equal(inv.return.method, 'stated_cost_per_case');
  assert.equal(inv.return.share_of_case_value, 49);
  assert.deepEqual(inv.return.scenarios.map(s => [s.ad_spend, s.cases, s.return_multiple]),
    [[25_000, 5.6, 2], [50_000, 11.1, 2]]);
  assert.ok(inv.flags.some(f => /above the \$50,000 cap/.test(f)));
});

test('same inputs → same numbers', () => {
  const a = JSON.stringify(computeInvestment(growthPlusElite, ryanInputs));
  const b = JSON.stringify(computeInvestment(structuredClone(growthPlusElite), { ...ryanInputs }));
  assert.equal(a, b);
});

test('never recommends less than the client already spends', () => {
  const inv = computeInvestment(growthPlusElite, { ...ryanInputs, currentAdSpend: 40_000 });
  assert.equal(inv.ad_spend.conservative, 40_000);
  assert.ok(inv.ad_spend.aggressive >= 40_000);
});

test('O\'Brien: MVA channel floor, capped at the $30K the client said he can spend, benchmark return', () => {
  const d = {
    marketing_name: 'Full Service Marketing — Growth', marketing_price_bundled: 8997, marketing_price_retail: 8997,
    total_bundled: 8997, pricing_mode: 'standalone', revenue_effective: 1_900_000,
  };
  const inv = computeInvestment(d, { practiceArea: 'MVA', geoTier: 1, competitiveness: 'High', spanish: true, currentAdSpend: 0, maxAdBudget: 30_000 });
  assert.equal(inv.ad_spend.conservative, 13_500);   // $10,000 + $2,000 + $1,500
  assert.equal(inv.ad_spend.aggressive, 30_000);
  assert.equal(inv.return.method, 'benchmark_cpl');
  assert.equal(inv.return.case_value_stated, false);
  assert.ok(inv.flags.some(f => /Case value assumed/.test(f)));
});

test('a current spend above the tier cap flags the overage', () => {
  const inv = computeInvestment(growthPlusElite, { ...ryanInputs, currentAdSpend: 60_000 });
  assert.equal(inv.ad_spend.conservative, 60_000);
  assert.equal(inv.ad_spend.overage.above_cap, 10_000);
});

test('no paid-ads product → no ad spend or return, still a year-one total', () => {
  const inv = computeInvestment({ coaching_name: 'Elite Coach Plus', coaching_price_bundled: 3497, total_bundled: 3497, revenue_effective: 900_000 }, {});
  assert.equal(inv.ad_spend, null);
  assert.equal(inv.return, null);
  assert.equal(inv.year_one_total, 3497 * 12);
  const web = computeInvestment({ marketing_name: 'Web + SEO Starter', marketing_price_bundled: 3997, total_bundled: 3997, revenue_effective: 900_000 }, {});
  assert.equal(web.ad_spend, null);
});

test('missing research inputs fall back to documented defaults and say so', () => {
  const inv = computeInvestment({ ...growthPlusElite, practice_areas_detected: ['family law / divorce'] }, {});
  assert.equal(inv.inputs.practice_area.value, 'Family Law');
  assert.equal(inv.ad_spend.conservative, 6_700);    // $3,500 + $2,000 + $1,200
  assert.ok(inv.flags.some(f => /Geo market tier not recorded/.test(f)));
});

test('parseInvestmentInputs reads the machine-read lines', () => {
  const notes = `
- Ad spend practice area: Family Law
- Geo market tier: Tier 4 (Salt Lake City metro)
- Market competitiveness: High — several large family firms nearby
- Spanish campaign needed: no
- Current monthly ad spend (stated): $25,000 (client, 00:08:39 — "last month we did 25")
- Current cost per signed case (stated): $4,500 (Google Ads + LSA, client, 00:07:10)
- Current cost per lead (stated): not stated
- Average case value (stated, one figure): $9,100 (client, 00:07:18)
- Close rate (stated): 21% (client, 00:17:23)
- Revenue goal (annual, one figure): not stated
- Maximum monthly ad budget (stated): not stated`;
  assert.deepEqual(parseInvestmentInputs(notes), {
    practiceArea: 'Family Law', geoTier: 4, competitiveness: 'High', spanish: false,
    currentAdSpend: 25_000, currentCostPerCase: 4_500, currentCostPerLead: null,
    caseValue: 9_100, closeRate: 0.21, revenueGoal: null, maxAdBudget: null,
  });
  assert.equal(parseInvestmentInputs('- Current monthly ad spend (stated): none — has never run paid ads').currentAdSpend, 0);
});

test('parseDollars needs an explicit dollar figure', () => {
  assert.equal(parseDollars('$4.5K'), 4_500);
  assert.equal(parseDollars('$1.2M'), 1_200_000);
  assert.equal(parseDollars('25 (read as thousands)'), null);
  assert.equal(parseDollars('not stated'), null);
});

test('applyInvestment keeps the legacy Slack fields in step', () => {
  const d = structuredClone(growthPlusElite);
  applyInvestment(d, ryanInputs);
  assert.equal(d.ad_spend_conservative, 25_000);
  assert.equal(d.ad_spend_aggressive, 50_000);
  assert.equal(d.investment.ad_spend.aggressive, 50_000);
});
