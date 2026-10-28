/**
 * select-package.test.mjs — unit tests for scripts/lib/pricing.mjs,
 * scripts/select-package.mjs and scripts/reprice.mjs
 *
 * Run: node --test scripts/tests/select-package.test.mjs
 *
 * Each case is a real example from Vanessa O'Donnell's proposal-tool feedback
 * (email "Proposal Opportunities: Week of 10/19", Oct 23 2026) or from the
 * research notes it came from. HubSpot is never called (HUBSPOT_TOKEN unset).
 */

import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { pricePackage, resolveName } from '../lib/pricing.mjs';
import {
  parseMoneyText,
  parseRevenueFromNotes,
  parseTeamSizeValue,
  parseTeamSize,
  parseCallFocus,
  selectDiscussedCoaching,
  selectLawTier,
  linesFromOverride,
  selectPackage,
} from '../select-package.mjs';

delete process.env.HUBSPOT_TOKEN;
const SCRIPTS = fileURLToPath(new URL('..', import.meta.url));

// ─── Pricing: bundle rule (issue 1) ───────────────────────────────────────────

test('one product left → stand-alone price, no savings (Chase, Harold Rosbottom, Mirabella, Riggs)', () => {
  const cases = [
    ['Paid Ads — Starter (stand-alone)', 3497],
    ['Paid Ads Platinum', 9997],
    ['Full Service Marketing — Essentials', 3797],
  ];
  for (const [name, price] of cases) {
    const r = pricePackage({ marketing: { name } });
    assert.equal(r.mode, 'standalone');
    assert.equal(r.total, price, name);
    assert.equal(r.totalSavings, 0, name);
  }
  assert.equal(pricePackage({ coaching: { name: 'Coach Essentials Plus' } }).total, 2497);
});

test('two products → bundled prices and savings', () => {
  const r = pricePackage({ marketing: { name: 'Full Service Marketing — Starter' }, coaching: { name: 'Elite Coach Plus' } });
  assert.equal(r.mode, 'bundled');
  assert.equal(r.total, 4997 + 3200);
  assert.equal(r.totalSavings, (5697 - 4997) + (3497 - 3200));
});

test('AI Workforce Pro – Starter does not make a bundle (Johnson Law Group, Allied Defense)', () => {
  const johnson = pricePackage({ marketing: { name: 'Full Service Marketing — Essentials' }, law: { name: 'AI Workforce Pro – Starter', seats: 3 } });
  assert.equal(johnson.mode, 'standalone');
  assert.equal(johnson.lines.marketing.charged, 3797);
  assert.equal(johnson.total, 3797 + 3 * 350);

  const allied = pricePackage({ law: { name: 'Fractional CTO Level 1 + AI Workforce Pro – Starter (1 seat)' } });
  assert.equal(allied.mode, 'standalone');
  assert.equal(allied.total, 3797 + 350);
});

test('full AI Workforce Pro still counts toward a bundle, and keeps FCTO savings visible', () => {
  const r = pricePackage({ law: { name: 'Fractional CTO Level 1 + AI Workforce Pro (15 seats)' } });
  assert.equal(r.mode, 'bundled');
  assert.equal(r.total, 3297 + 1597 + 10 * 120);
  assert.equal(r.totalSavings, 500);
});

test('Paid Ads Essentials alone has no price — flagged, not invented (Jason Breit)', () => {
  const r = pricePackage({ marketing: { name: 'Paid Ads Essentials' } });
  assert.deepEqual(r.unpriced, ['Paid Ads Essentials']);
  assert.equal(r.lines.marketing.charged, null);
  // …but it can be sold bundled
  const bundled = pricePackage({ marketing: { name: 'Paid Ads Essentials' }, coaching: { name: 'Elite Coach' } });
  assert.equal(bundled.lines.marketing.charged, 1997);
});

test('FCOO Partner is retired → priced as FCOO Director (Glen Larson)', () => {
  const r = pricePackage({ coaching: { name: 'FCOO Partner' }, law: { name: 'Fractional CTO Level 1' } });
  assert.equal(r.lines.coaching.name, 'FCOO Director');
  assert.ok(r.notes.some(n => /FCOO Partner is retired/.test(n)));
  assert.equal(resolveName("Master's Circle + FCOO Partner")[0].product.retired, true);
});

test('names the AI typed by hand still resolve', () => {
  for (const [raw, name] of [
    ['AI Essentials — Starter — AI Workforce Pro – Starter (1 seat)', 'AI Workforce Pro – Starter'],
    ['AI Accelerator L2 — Fractional CTO Level 2', 'Fractional CTO Level 2'],
    ['Full Service Marketing Essentials', 'Full Service Marketing — Essentials'],
    ['Web + SEO Growth (standalone)', 'Web + SEO Growth'],
    ['Paid Ads Starter (stand-alone)', 'Paid Ads Starter'],
  ]) assert.equal(resolveName(raw)[0].product?.name, name, raw);
});

test('unknown products keep their given price and are flagged', () => {
  const r = pricePackage({ marketing: { name: 'OmniSocial AI 360 (Content – Standard + Ads – Growth bundle)', price: 3000 }, coaching: { name: 'Elite Coach' } });
  assert.equal(r.lines.marketing.charged, 3000);
  assert.ok(r.notes.some(n => /isn't in the pricing catalog/.test(n)));
});

// ─── Revenue (issue 2) ────────────────────────────────────────────────────────

test('revenue stated in free text is read, not replaced by the HubSpot midpoint', () => {
  assert.equal(parseMoneyText('"north of $300,000" (William, 00:07:15, "I don\'t have it in front of me"'), 300_000);
  assert.equal(parseMoneyText('about $1.2 million [transcript unclear — "1.2" read as $1.2M]'), 1_200_000);
  assert.equal(parseMoneyText('"my first year I made about a hundred, and this year I\'m on track to make about 250." (00:07:27)'), 250_000);
  assert.equal(parseMoneyText('2026 YTD $2.57M at time of call; target $3.14M'), 2_570_000);
  assert.equal(parseMoneyText('about $10M projected for 2026'), 10_000_000);
  assert.equal(parseMoneyText('"1.2" (00:36:20) in answer to "what\'s the revenue currently"'), 1_200_000);
});

test('"not stated" revenue stays unknown (Mason Law, Dan Mayer)', () => {
  assert.equal(parseMoneyText('not stated for the firm. Only firm-level figure:'), null);
  const notes = '- Annual revenue (gross / case value): not stated as a figure. Closest: "we\'re not at the $700,000 mark"\n';
  assert.equal(parseRevenueFromNotes(notes), null);
});

test('the machine-read revenue line wins', () => {
  const notes = '- Revenue (annual, best estimate): $300,000\n- Annual revenue (gross / case value): $1.5M gross\n';
  assert.deepEqual(parseRevenueFromNotes(notes), { value: 300_000, source: 'research_notes' });
});

// ─── Team size (issue 4) ──────────────────────────────────────────────────────

test('team size in the wording research notes actually use', () => {
  for (const [value, n] of [
    ['15 total, 2 lawyers ("Myself and one other one")', 15],
    ['3 — Dan (attorney/owner), Shane (legal assistant)', 3],
    ['~18 employees', 18],
    ['13-person firm', 13],
    ['Solo — Andrew Ferrell', 1],
    ['Three people plus outside vendors', 3],
    ['per site, 7 attorneys + 9 support staff (incl. in-house marketing coordinator)', 16],
    ['not stated by the prospect. Rep said "I think you guys have 30 employees". Website: 7 attorneys.', 7],
    ['number not stated. Roles named: Paul (founder/owner)', null],
    ['Two owners / senior attorneys (Jacqueline Radebaugh and Jason)', null],
  ]) assert.equal(parseTeamSizeValue(value), n, value);
});

test('the machine-read team size line wins', () => {
  assert.equal(parseTeamSize('- Team size (total headcount): 15\n- Team size: 2 lawyers\n'), 15);
});

// ─── Products discussed (issues 3, 8) ─────────────────────────────────────────

test('explanation on wrapped lines is not read as products (Sweeney, Dan Mayer)', () => {
  const sweeney = '- Products discussed on call: Fractional CTO Level 1\n    (Basis: $3,797 is also the FCOO Advisor and Full Service Marketing Essentials retail price)\n';
  assert.deepEqual(parseCallFocus(sweeney).products, ['Fractional CTO Level 1']);
  const dan = '- Products discussed on call: AI Workforce Pro – Starter, Fractional CTO Level 1\n    (prospect called AI Workforce Pro "$3.50 a month")\n';
  assert.deepEqual(parseCallFocus(dan).products, ['AI Workforce Pro – Starter', 'Fractional CTO Level 1']);
});

test('"FCOO Advisor / Director / Partner" is the generic FCOO, not Partner (Glen Larson)', () => {
  const p = parseCallFocus('- Products discussed on call: FCOO Advisor / Director / Partner\n').products;
  assert.deepEqual(p, ['FCOO']);
});

test('coaching discussed on the call wins over the revenue default (KHK, Mason, Glen Larson)', () => {
  const notes = [];
  assert.equal(selectDiscussedCoaching(['FCFO Advisor', 'Full Service Marketing'], 700_000, notes).name, 'FCFO Advisor');
  assert.equal(selectDiscussedCoaching(["Master's Circle"], 500_000, notes).name, "Master's Circle");
  assert.equal(selectDiscussedCoaching(['FCOO'], 2_570_000, notes).name, 'FCOO Director');
  assert.equal(selectDiscussedCoaching(['FCOO'], 800_000, notes).name, 'FCOO Advisor');
  assert.equal(selectDiscussedCoaching(['FCOO Partner'], 3_200_000, notes).name, 'FCOO Director');
  assert.equal(selectDiscussedCoaching(['Elite Coach', 'FCOO Advisor'], 600_000, notes).name, 'Elite Coach + FCOO Advisor');
  assert.equal(selectDiscussedCoaching(['Fractional CTO Level 1'], 600_000, notes), null);
});

test('AI line: one FCTO level + one AIWP tier, no duplicates (Dan Mayer, Current Shift)', () => {
  const notes = [];
  const dan = selectLawTier(['AI Workforce Pro – Starter', 'AI Workforce Pro (tier not specified)', 'Fractional CTO Level 1'], 600_000, 3, notes);
  assert.equal(dan.name, 'Fractional CTO Level 1 + AI Workforce Pro – Starter');
  const cs = selectLawTier(['Fractional CTO Level 3', 'Fractional CTO Level 2', 'Fractional CTO Level 1'], 1_200_000, null, notes);
  assert.equal(cs.name, 'Fractional CTO Level 2');
});

// ─── Seller package overrides (issue 9) ───────────────────────────────────────

test('seller package text becomes package lines when every product is known', () => {
  assert.deepEqual(linesFromOverride('Elite Coach Plus + AI Workforce Pro – Starter (1 user, team size unknown)', 3),
    { marketing: null, coaching: 'Elite Coach Plus', law: 'AI Workforce Pro – Starter', seats: 1 });
  assert.equal(linesFromOverride('AI Workforce Pro – Starter (1 user, $350/mo) only — no marketing, coaching, or Fractional CTO', 3).law, 'AI Workforce Pro – Starter');
  assert.equal(linesFromOverride('FSM Starter (opt 1) + FSM Essentials (opt 2) stand-alone, $5K ad spend', 3), null);
});

// ─── End to end ───────────────────────────────────────────────────────────────

let tmp, cwd;
before(() => {
  cwd = process.cwd();
  tmp = mkdtempSync(join(tmpdir(), 'select-package-'));
  mkdirSync(join(tmp, 'triggers/audit-research'), { recursive: true });
});
after(() => {
  process.chdir(cwd);
  rmSync(tmp, { recursive: true, force: true });
});

function firm(name, notes, trigger = {}) {
  mkdirSync(join(tmp, name), { recursive: true });
  writeFileSync(join(tmp, name, `${name}_October 1, 2026_Research_Notes.txt`), notes);
  writeFileSync(join(tmp, 'triggers/audit-research', `${name}.json`), JSON.stringify(trigger));
}

test('Glen Larson end to end: team of 15, FCOO Director stand-alone, no FCOO Partner', async () => {
  firm('glen', [
    '- Team size: 15 total, 2 lawyers ("Myself and one other one").',
    '- Annual revenue (gross / case value): 2026 YTD $2.57M at time of call; projected $3.27M',
    '- Primary engagement: coaching/ops',
    '- Products discussed on call: FCOO Advisor / Director / Partner',
    '- Lead-gen gap stated: no — "I feel pretty confident about our systems"',
  ].join('\n'));
  process.chdir(tmp);
  const d = await selectPackage('glen');
  assert.equal(d.team_size_stated, 15);
  assert.equal(d.revenue_effective, 2_570_000);
  assert.equal(d.coaching_name, 'FCOO Director');
  assert.equal(d.marketing_name, null);
  assert.equal(d.pricing_mode, 'standalone');
  assert.equal(d.total_bundled, 5797);
  assert.ok(!JSON.stringify(d).includes('FCOO Partner"'));
});

test('unknown revenue is flagged for the seller to confirm', async () => {
  firm('mason', [
    '- Team size: number not stated. Roles named: Paul (founder/owner)',
    '- Annual revenue (gross / case value): not stated for the firm.',
    '- Primary engagement: coaching/ops',
    "- Products discussed on call: Master's Circle",
    '- Lead-gen gap stated: no',
  ].join('\n'));
  process.chdir(tmp);
  const d = await selectPackage('mason');
  assert.equal(d.needs_revenue_confirmation, true);
  assert.equal(d.coaching_name, "Master's Circle");
  assert.ok(d.selection_notes.some(n => /assumed 3/.test(n)));
});

test('a seller override in the trigger is written as the package (PPD Law), not left empty', async () => {
  firm('ppd', [
    '- Team size: 4 total — Premmal (owner/lawyer) + 3 support staff.',
    '- Annual revenue (gross / case value): ~$500k/year',
    '- Primary engagement: coaching/ops',
    '- Products discussed on call: none',
    '- Lead-gen gap stated: no',
  ].join('\n'), { package: 'Elite Coach Plus + AI Workforce Pro – Starter (1 user, team size unknown)' });
  process.chdir(tmp);
  const d = await selectPackage('ppd');
  assert.equal(d.package_source, 'trigger_override');
  assert.equal(d.coaching_name, 'Elite Coach Plus');
  assert.equal(d.law_name, 'AI Workforce Pro – Starter');
  assert.equal(d.total_bundled, 3497 + 350);
});

test('reprice.mjs re-prices a seller-edited package and records confirmed revenue', () => {
  mkdirSync(join(tmp, 'johnson'), { recursive: true });
  writeFileSync(join(tmp, 'johnson/package_decision.json'), JSON.stringify({
    marketing_name: 'Full Service Marketing — Essentials', marketing_price_bundled: 3497, marketing_price_retail: 3797,
    coaching_name: null, law_name: 'AI Workforce Pro – Starter', law_seats: 3, law_price_bundled: 1050,
    total_bundled: 4547, total_savings: 300, needs_revenue_confirmation: true, selection_notes: [],
  }));
  const r = spawnSync(process.execPath, [join(SCRIPTS, 'reprice.mjs'), 'johnson', '--revenue', '300000'], { cwd: tmp, encoding: 'utf8' });
  assert.equal(r.status, 0, r.stderr);
  const d = JSON.parse(readFileSync(join(tmp, 'johnson/package_decision.json'), 'utf8'));
  assert.equal(d.total_bundled, 3797 + 1050);
  assert.equal(d.total_savings, null);
  assert.equal(d.revenue_effective, 300_000);
  assert.equal(d.needs_revenue_confirmation, false);
});
