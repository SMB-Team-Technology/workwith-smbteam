# SMB Team — Audit Write (Pass 2): Build the Proposal Deck

Build the 5-slide proposal PowerPoint for a firm and commit it. Run this after `/audit-research` completes. This pass used to build the "Growth, Profit & Freedom Roadmap" website and the Sales Companion PDF; both are retired. The deck is now the only output, and it is built from the same inputs the website was.

## How to invoke

```
/audit-write
Firm Name: [Full legal name of the firm]
Friendly Name: [same value used in /audit-research, e.g. angel-law]
Sales Rep: [rep's full name]
Date: [same date used in /audit-research — Month DD, YYYY]
```

(`--with-pptx` is still accepted for old trigger files but does nothing — the deck is always built.)

---

## BEFORE STARTING

Read these files. They are the only inputs — no new research:
1. `[friendly-name]/[FirmName]_[Date]_Research_Notes.txt` — all firm data comes from here: the web research, the transcript extraction (STEP 9), the KPI AND DIAGNOSIS block (STEP 9B — the source for every number on slides 1–3) and the `Key prospect quotes` list. Trust it. Older notes have no STEP 9B: then use only figures STEP 9 records as said on the call, and if none fits the recommendation, build slide 1 as a qualitative pain point with a seller note (audit-pptx.md DATA RULES).
2. `[friendly-name]/package_decision.json` — the package, prices, ad-spend starting points and seller overrides (see STEP 1). It may be absent (see STEP 1).
3. `.claude/commands/audit-pptx.md` — what each slide field holds and the rules for filling it.

If the research notes file does not exist, stop and tell the user to run `/audit-research` first.

Do not read anything under `[friendly-name]/sections/`, `[friendly-name]/index.html`, or any earlier `*_Proposal.py` / `*_Sales_Companion.py` in the firm folder. Older firms still have those files from the retired website; a new build must come from the inputs above only.

**Transcript-first principle:** The research notes contain data extracted from the transcript. Those values are ground truth. Never search for data that's already in the notes. This pass never has the transcript file itself — only what the research notes captured.

---

## CRITICAL RULES — NEVER BREAK THESE

- Direct transcript quotes (`PROSPECT_QUOTES` on slide 1) come only from the research notes' STEP 9 fields and `Key prospect quotes` list. If the notes say quotes come from an AI summary rather than a full transcript, there are no usable quotes: set `PROSPECT_QUOTES = []` and never present summary text as the client's exact words.
- Never say "you are not running ads" — only "does not appear to be running" or "not observed."
- Never mention live chat as an SMB Team service.
- Never mention CRM setup as an SMB Team deliverable.
- Never state profitability facts by practice area unless the prospect explicitly said so on the call.
- Escalation flags are internal only — they go in the BUILD NOTES block (STEP 2), never in a slide field and never in `SELLER_NOTES`. The deck's speaker notes are always empty; `SELLER_NOTES` (call prep and deal context, keyed by slide name) goes to the seller prep file the pipeline emails and posts in Slack (see audit-pptx.md).
- Every number on the story slides (everything before the investment slide) was said on the call (client or seller) or measured in research, copied exactly — never invented or estimated, and every target rests on call data or is left `None` (DATA RULES in `audit-pptx.md`).
- **Never print a review count or star rating (firm or competitor) tagged `UNCONFIRMED` in the research notes as a specific fact.** Use qualitative framing instead (e.g., "far fewer reviews than several competitors in this market" rather than an exact number), and add "Review counts unconfirmed — verify live before the call" to the escalation flags in the BUILD NOTES. Only a number tagged `[confirmed via Google]` in the research notes may appear as a specific figure in the deck.

---

## TRAFFIC LIGHT CRITERIA

Rate each pillar red / amber / green from the transcript and research notes. These ratings are not shown on any slide — use them to rank the What You Told Us items and to sanity-check that the slide 2 diagnosis covers the reddest pillar the recommendation addresses:

**Lead Generation** — Red: referrals only, no system, inconsistent flow. Amber: some paid ads or SEO, inconsistent results. Green: multiple reliable systems running.

**Intake** — Red: attorney personally handles intake, no process, slow follow-up. Amber: some delegation but gaps, no after-hours coverage. Green: trained team, defined process, fast follow-up.

**Team** — Red: owner cannot step away, no accountability, no org structure. Amber: small team but owner manages everything closely. Green: managers exist, team runs without constant owner involvement. Never reference "Stage 6" — describe specifically what a self-managing firm looks like.

**Profit** — Red: no financial visibility, expenses out of control. Amber: revenue growing but margins unclear. Green: knows numbers, profit planned not discovered.

---

## DOMINANT BUYING MOTIVE (DBM)

The DBM is the personal reason behind growth — what success will allow the owner to do. Not "more money" — what the money enables. Use exact transcript words if available. If not stated, infer: most owners want (1) a firm that runs itself so they have time, (2) grow and sell, or (3) scale and dominate. Anchor every slide to the DBM.

---

## STEP 1 — PACKAGE AND PRICES

Apply all package eligibility and calculation logic in this step and the tables below before filling any slide field.

**TRANSCRIPT-STATED NEED OVERRIDE — APPLY THIS BEFORE ANYTHING ELSE**

`package_decision.json` is a deterministic revenue/team-size lookup. It cannot read the transcript and does not know what the call was actually about. Its `confidence` field reflects how sure the pipeline is about the *revenue number* — it says nothing about whether a marketing+coaching bundle is the right recommendation at all. Before touching the decision file or the eligibility tables, read the research notes' transcript extraction and DBM section and check for these four overrides. Any one of them supersedes `package_decision.json` and the eligibility tables below, regardless of `confidence` level, and regardless of whether a `PACKAGE INSTRUCTION` block is present:

1. **Call-purpose override.** If the transcript or research notes state the discovery call's actual subject was something other than standard marketing/intake growth (e.g., explicitly framed as a Fractional CTO / AI automation engagement, an operations/coaching engagement, etc.), lead the recommendation with that stated category. Do not default to Full Service Marketing just because revenue qualifies for a tier — the firm did not ask about marketing. Check the LAW package table and the non-marketing package table first; only add a marketing package if the transcript shows an actual marketing/lead-gen gap alongside the stated need.
2. **Existing-vendor override.** If the transcript states the firm has recently signed with, or is already paying, another marketing/SEO/ad/AEO vendor (an active or recent contract), exclude Full Service Marketing — every tier and every sub-package — from the recommendation entirely. A firm that just committed to a marketing engagement does not have a marketing gap; recommending one anyway ignores the client's actual, stated situation. Recommend the package(s) that match what the transcript says the firm still needs instead (coaching, ops, AI/FCTO, etc.).
3. **Budget-reality override.** If the transcript or notes state, or strongly imply, that the client cannot afford or is not positioned to spend at the tier the revenue table implies (budget concerns, an explicit statement of financial limits, a stated preference for a smaller engagement), do not present the revenue-implied tier. Lead with the lowest-cost package that still addresses the transcript's stated need, and document the gap between the revenue table's suggestion and what you actually recommended in the BUILD NOTES (STEP 2) so sales can see the override was intentional.
4. **Effective-revenue override.** If the research notes state a net/take-home/collected revenue figure distinct from a gross/case-value figure (common for contingency-fee practices — e.g. "$1.5–2M gross / ~$500k net"), tier and calculate against the **net** figure, not gross, regardless of what `revenue_effective` in `package_decision.json` says. `select-package.mjs` applies this automatically when both figures are parseable (check `net_revenue_stated` and `is_contingency_practice` in the decision file), but if the notes state a net figure the script's regex missed, run `node scripts/reprice.mjs [friendly-name] --revenue <net annual figure>` (it recomputes the ad spend range and return) and document the correction — including the 35%-cap check — in the BUILD NOTES (STEP 2).

None of these four checks are about recomputing a price in isolation — they are about whether the *category* and *scale* of product being proposed matches what actually happened on the call. Do this check even when `package_decision.json` says `confidence: "high"`.

**PACKAGE DECISION FILE — CHECK THIS FIRST**

Before any eligibility logic, check whether `[friendly-name]/package_decision.json` exists.

- **If it exists:** Read it and extract `marketing_tier`, `marketing_price_bundled`, `marketing_price_retail`, `coaching_name`, `coaching_price_bundled`, `coaching_price_retail`, `total_bundled`, `ad_spend_conservative`, `ad_spend_aggressive`, `net_revenue_stated`, `is_contingency_practice`, `confidence`, `call_focus`, and the LAW fields (`law_tier`, `law_name`, `law_price_bundled`, `law_price_retail`, `law_seats`). A `null` marketing field means no marketing package is part of the recommendation. When `call_focus.primary_engagement` is set, `select-package.mjs` has already applied the call-purpose override (marketing left out on a coaching/ops- or AI-led call with no lead-gen need; AI products named on the call included as the LAW package) — still run the override check below as a backstop, but don't re-add marketing it removed unless the research notes show a lead-gen need. After applying the Transcript-Stated Need Override above:
  - **Prices in the file are already correct — copy them, never recompute.** `*_price_bundled` is the price the client is CHARGED and `*_price_retail` is the stand-alone price. `scripts/lib/pricing.mjs` applies the bundle rule: when `pricing_mode` is `"standalone"` (fewer than 2 bundle-eligible products — AI Workforce Pro – Starter never counts), the charged price IS the stand-alone price and there are no bundle savings. If you change which products are in the package for any reason, edit only the product name fields and then run `node scripts/reprice.mjs [friendly-name]` to get the prices.
  - **Seller always wins.** If `package_source` is `"trigger_override"` or any `selection_notes` entry starts with "Seller override", the seller chose this package in Slack. Use it as-is — the four Transcript-Stated Need overrides above do not apply to it. Note any rule it breaks in the BUILD NOTES (STEP 2), but build it.
  - If `needs_revenue_confirmation` is `true`, the seller locked it in without confirming revenue. Build it, and add "Revenue unverified (draft based on <revenue_source>)" to the BUILD NOTES (STEP 2) — never mention this in the deck.
  - If `needs_seller_input` is `true`, no package was chosen (call focus unknown) and the seller never set one. Do not fall back to a revenue-based marketing + coaching package. Stop and report that the seller must set the package in the Phase 1 Slack thread first.
  - If none of the three overrides apply and `confidence` is `"high"`, use the tier names and prices exactly — do not re-run eligibility logic.
  - If none of the three overrides apply but `confidence` is `"medium"` or `"low"`, use the decision file as a starting point, cross-check the selected tiers against the research notes, and document any correction in the BUILD NOTES (STEP 2).
  - If any override applies, the decision file's marketing/coaching selection is not usable as-is — apply the full eligibility rules below instead (pulling in the LAW / non-marketing tables as the override directs) and document in the BUILD NOTES (STEP 2) which override triggered the departure from the decision file.
- **If it does not exist (interactive session or fallback):** Apply the full eligibility rules and MANDATORY PRICE LOOKUP below.

Apply all package eligibility and calculation logic (below) BEFORE starting STEP 2.

If the pipeline injected a `PACKAGE INSTRUCTION` block in your system prompt, treat it as input to the override check above, not as something that bypasses it — a `PACKAGE INSTRUCTION` cannot make a marketing package correct for a firm that just told you it doesn't need one.

**MANDATORY PRICE LOOKUP — COMPLETE THIS BEFORE STEP 2**

Do not rely on memory for any price. If using package_decision.json, copy the prices from that file. Otherwise, scroll to the SELECT MARKETING PACKAGE and SELECT NON-MARKETING PACKAGE tables in this command file and read the exact dollar amounts. Then write them out explicitly in this format before proceeding:

- Marketing package selected: [name]
  - Bundled price (from table): $X,XXX/mo
  - Stand-alone price (from table): $X,XXX/mo
  - Savings (stand-alone minus bundled): $X,XXX/mo
- Non-marketing package selected: [name]
  - Bundled price (from table): $X,XXX/mo
  - Stand-alone price (from table): $X,XXX/mo
  - Savings (stand-alone minus bundled): $X,XXX/mo
- Legal AI Workforce (LAW) package selected (if applicable): [name or "none"]
  - Bundled price (from table): $X,XXX/mo
  - Stand-alone price (from table): $X,XXX/mo
  - Savings (stand-alone minus bundled): $X,XXX/mo
- AI Avatar / Video Growth add-on selected (if applicable): [name or "none"]
  - Price (from table): $X,XXX one-time or $X,XXX/mo + $X,XXX setup
- Total monthly investment (sum of all bundled/recurring prices): $X,XXX/mo
- Total savings (sum of all savings): $X,XXX/mo

**Bundle rule:** bundled prices apply only when the package has 2 or more bundle-eligible products. AI Workforce Pro – Starter does not count toward a bundle. With fewer than 2, every product is charged its stand-alone price and savings are $0. A product with no stand-alone price (Paid Ads Essentials, Web + SEO Essentials, Coach Essentials) cannot be sold on its own — if it ends up alone, stop and report it instead of building.

If any price you are about to write is not an exact match to a value in those tables, stop. Go back to the table and find the correct number. Do not round, interpolate, or estimate. Do not proceed to STEP 2 until these lookups are confirmed character-by-character against the tables in this file.

---

## STEP 2 — WORKINGS (inside the deck build)

Do the calculations that used to go in the retired `section_11_workings.txt` here. Do not write a separate workings file. Instead, copy `Design Files/audit_pptx_template.py` to `[friendly-name]/[FirmName]_[Date]_Proposal.py` (see audit-pptx.md) and record the workings as a comment block directly under the `# FILL — Replace every placeholder` banner, above the first slide field:

```python
# ── BUILD NOTES (internal — never shown on a slide) ──────────────
# Marketing package: <name> — bundled $X,XXX/mo, stand-alone $X,XXX/mo, savings $X,XXX/mo
# Non-marketing package(s): ...
# LAW package: ... (or "none")
# Total monthly investment: $X,XXX/mo · total savings: $X,XXX/mo · pricing_mode: bundled|standalone
# Year one: $X (from package_decision.json → investment.year_one_total)
# Ad spend (copied from investment.ad_spend — computed in code, never by hand):
#   $X,XXX–$XX,XXX/mo · low end: <conservative_basis> · high end: <aggressive_steps joined>
# Return (copied from investment.return): <method> · <basis> · scenarios: $X → N cases → $X → X.X× …
# Investment inputs used: <investment.inputs, with each source> · flags: <investment.flags>
# Why this range: <the client-facing sentence>
# Pillar review: Lead Gen <red|amber|green> — <biggest gap> · Intake … · Team … · Profit …
# KPI (slide 1): <label> — "<figure exactly as said>" — <client|seller>, <timestamp> (STEP 9B) — or "none usable: qualitative"
# Diagnosis (slide 2): 1. <cause> — <evidence> — <source> · 2. … (STEP 9B)
# Targets (slides 2–3): <metric> — <target> — basis: <call data> · or "none — seller note"
# Client's why / cost of inaction (slide 1): "<verbatim>" — <Full Name (client), timestamp> (STEP 9B) · or "none on the call"
# Closing quote (slide 5): "<verbatim>" — <Full Name (client), timestamp> · or "none — no unused verbatim line"
# Legacy Staircase slide: <included — current N / goal N, as discussed (STEP 9B) | left out — not walked through on the call>
# Plan (slide 3): each action — <action> — tied to: "<client line or STEP 9B plan input>"
# What You Told Us (slide 1 quotes and tie lines):
#   1. <label> — transcript line: "<verbatim line from the research notes>" — supports: <package>
#   2. ...
#   3. ...
# Overrides applied: <which Transcript-Stated Need Override, or seller override, and why>
# Escalation flags: <each flag that applies, or "none">
```

Contents — the same items the old workings file held:
- Selected marketing package name, bundled price, stand-alone price, savings
- Selected non-marketing package(s) name, bundled price, stand-alone price, savings
- Total monthly investment (sum of bundled prices) and total savings
- Year-one total, ad spend range and return projection — copied from `package_decision.json` → `investment`, which `scripts/reprice.mjs` computes in code from the AD SPEND CALCULATION and ROI PROJECTIONS rules below and the research notes' investment inputs. Never recalculate, round or adjust them. If `investment` is missing, run `node scripts/reprice.mjs [friendly-name]`. Copy `investment.flags` into the escalation flags.
- If a paid-ads package is part of the recommendation: the one plain-English "why this range" sentence (rules under AD SPEND CALCULATION). It feeds `AD_SPEND_WHY`.
- DBM statement
- Pillar review — replaces the website's Sections 5–9: for each of Lead Generation, Intake, Team and Profit, the traffic-light rating and the single biggest gap the research notes show, one line each.
- KPI, diagnosis and targets for slides 1–3, each with its STEP 9B source line (or research step), so every number on those slides can be traced
- What You Told Us: the slide 1 quotes selected (rules under WHAT YOU TOLD US below), each with the verbatim line from the research notes it comes from and the package/deliverable it supports
- Which override (if any) changed the decision file's package, any "Revenue unverified (draft based on <revenue_source>)" note, and every escalation flag that applies

These notes stay in the `.py` as the record of what went into the deck. They are comments above the layout engine, so the layout diff check is unaffected. The repo is public: keep transcript lines short, exactly as they already appear in the research notes, and never add anything from outside the research notes.

## STEP 3 — BUILD THE DECK

Follow `.claude/commands/audit-pptx.md` to fill every slide field from the research notes, `package_decision.json` and your STEP 2 workings, then run the script and check its output. The investment slide (slide 5) reads every price, total, ad spend and return figure from `package_decision.json` itself, and every number on slides 1–3 must match its STEP 9B source.

---

## PRICE INTEGRITY — CRITICAL

The prices in the tables below are the ONLY approved prices. Do not estimate, round, interpolate, or use any number not listed here. Every dollar figure in the deck must come from one of the approved pricing tables below (Marketing, Non-Marketing, Legal AI Workforce, AI Avatar, Bookkeeping, General Add-Ons, OmniSocial AI, or Attorney Assistant). The example numbers in template comments are illustrative only — do not use them as actual prices.

---

## PACKAGE ELIGIBILITY AND CALCULATIONS

Complete this entire section before starting STEP 2.

### ELIGIBILITY FILTERS — apply first, hide anything that fails

**Practice Area:**
- Personal Injury → hide ALL Essentials marketing packages AND the LSA-only add-on. Minimum tier is Starter.
- Criminal Defense + High competitiveness → hide ALL Essentials marketing packages. LSA-only still allowed.
- Essentials marketing tier requires a single location AND a single practice area → hide Essentials for any firm with multiple locations or multiple practice areas, regardless of revenue.

**Revenue:**
- Under $250K → confirm client has funds to cover 4 months of services before proceeding.
- Under $500K → hide all Fractional CFO and Fractional COO products and all bundles containing them.
- Under $1M → hide Master's Circle and all bundles.
- Under $2M → hide Dominate and Platinum marketing tiers.
- Under $3M → hide Platinum marketing tier.
- Over $750K → hide all Essentials marketing products.

**Team:**
- Fewer than 5 team members → hide all Master's Circle options.
- No dedicated ops, marketing, or intake team member → hide all Master's Circle options.

**General:**
- Minimum MRR: $2,497/month — never recommend below this.
- Default to recommending both a marketing package and a non-marketing package. A single-product recommendation is acceptable only when the transcript clearly shows the firm's needs are best served by one service category — do not force a second product that does not fit.
- Total SMB spend (management fees + ad spend) must not exceed 35% of monthly revenue. Legal AI Workforce (LAW) recurring monthly fees count toward this cap alongside marketing and coaching packages.

---

### SELECT MARKETING PACKAGE

Default to Full Service Marketing at the appropriate tier unless there is a specific reason to use a sub-package. Sub-packages (ads-only, web+SEO only) must be paired with a coaching package.

**Marketing Tiers — Full Service Bundled Prices:**

| Revenue | Tier | Bundled Price | Ad Spend Cap |
|---|---|---|---|
| Under $750K, single location + single practice area | Essentials | $3,497/mo | $7,500 |
| $500K–$1M (or under $750K with multiple locations/practice areas) | Starter | $4,997/mo | $25,000 |
| $1M–$2M | Growth | $7,497/mo | $50,000 |
| $2M–$3M | Dominate | $10,497/mo | $100,000 |
| $3M+ | Platinum | $15,997/mo | $150,000 |

Note: the Paid-Ads-only sub-package for Starter has a lower cap of $20,000 — $25,000 applies only to the Full Service Marketing Starter bundle above.

**Sub-packages — Paid Ads and Web + SEO** (from the Sub-Package tables in `Design Files/Scoping_and_Ad_Spend_Guide.md`; also in `scripts/lib/pricing.mjs`):

| Package | Bundled | Stand-alone |
|---|---|---|
| Paid Ads Essentials | $1,997/mo | none — can't be sold on its own (awaiting a price from Sales) |
| Paid Ads Starter | $2,497/mo | $3,497/mo |
| Paid Ads Growth | $4,497/mo | $5,497/mo |
| Paid Ads Dominate | $6,997/mo | $7,997/mo |
| Paid Ads Platinum | $8,997/mo | $9,997/mo |
| Web + SEO Essentials | $1,997/mo | none — can't be sold on its own |
| Web + SEO Starter | $3,497/mo | $3,997/mo |
| Web + SEO Growth | $4,897/mo | $5,897/mo |
| Web + SEO Dominate | $6,997/mo | $7,997/mo |
| Web + SEO Platinum | $9,597/mo | $11,497/mo |

**Stand-alone prices (for the savings calculation on slide 5):**
Essentials $3,797 | Starter $5,697 | Growth $8,997 | Dominate $12,497 | Platinum $18,997

**Boundary rule:** If the firm's calculated ad spend exceeds the tier's cap, move to the higher tier. Aggressive goals alone no longer bypass the Dominate/Platinum revenue floors — a firm must meet the revenue threshold to be eligible.

**Website rebuild needed if:** PageSpeed mobile below 50, design 5+ years old, not mobile responsive, no practice area pages, no attorney bios. If rebuild needed, must use Full Service (not ads-only).

---

### SELECT NON-MARKETING PACKAGE

Non-marketing packages are the default recommendation alongside marketing. Recommend one when it genuinely fits the firm's stage and needs.

| Revenue | Team | Recommended | Bundled Price |
|---|---|---|---|
| $250K–$400K, tight budget | Any | Coach Essentials | $1,000/mo |
| $250K–$400K, tight budget, wants 1:1 support | Any | Coach Essentials Plus | $1,997/mo |
| $250K–$400K | Any | Elite Coach | $2,600/mo |
| $400K–$1M | Any | Elite Coach Plus | $3,200/mo |
| $400K–$1M | Growing | Elite Coach + FCOO Advisor | $5,694/mo |
| $400K–$1M | Growing, larger ops need | Elite Coach + FCOO Director | $7,394/mo |
| $1M+ | Under 5 | Elite Coach Plus | $3,200/mo |
| $1M+ | Under 5 operational focus | FCOO Advisor | $3,297/mo |
| $1M+ | Under 5, established leaders, operational focus | FCOO Director | $4,997/mo |
| $1M+ | 5+ with dedicated staff | Master's Circle | $4,600/mo |
| $1M+ | 5+ with dedicated staff + ops | Master's Circle + FCOO Advisor | $6,694/mo |
| $2M+ | 5+ with dedicated staff | Master's Circle + FCOO Director | $8,394/mo |
| $3M+ | Large team, operational focus | FCOO Director | $4,997/mo |
| $3M+ | Large team | Master's Circle + FCOO Director | $8,394/mo |

**FCOO Partner is retired (Oct 2026) — never recommend it or any package containing it (Elite Coach + FCOO Partner, Master's Circle + FCOO Partner). Use FCOO Director.**

**Add Fractional CFO** if: owner mentions profit problems, revenue growing but not taking home more, no financial visibility, doesn't know acquisition cost. FCFO Advisor $3,297/mo bundled (min revenue $400K); FCFO Director $4,997/mo bundled (min revenue $1M); FCFO Partner $8,997/mo bundled (min revenue $3M).

**Note on Coach Essentials / Coach Essentials Plus:** Coach Essentials is group coaching only and cannot be sold standalone. Coach Essentials Plus adds a monthly 1:1 coaching call and can be sold standalone at $2,497/mo. Both are lower-cost alternatives to Elite Coach in the same $250K–$400K revenue band — use them only when the transcript indicates a tighter budget (e.g. via the Budget-Reality Override), not as the default recommendation for that revenue band.

**Stand-alone prices:** Coach Essentials Plus $2,497 (Coach Essentials has no stand-alone price) | Elite Coach $3,497 | Elite Coach Plus $3,497 | Master's Circle $4,997 | FCOO Advisor $3,797 | FCOO Director $5,797 | FCFO Advisor $3,797 | FCFO Director $5,797 | FCFO Partner $9,997

**Fractional packages (FCOO and FCFO) now include Elite Coach group deliverables.** When recommending any fractional package, its deliverables must include weekly group coaching sessions, practice area masterminds, virtual access to quarterly workshops, and one annual in-person workshop — reflect this in that package card's services line on slide 5 (condensed to fit) and in its slide 4 deliverables. These are included in the fractional price — do not list them as a separate charge.

---

### SELECT LEGAL AI WORKFORCE (LAW) PACKAGE

Legal AI Workforce (LAW) provides managed AI implementation for law firms — Claude Enterprise workspace, pre-built Law Firm AI Skills, and optional Fractional CTO leadership. Recommend alongside a marketing or coaching package when the firm shows AI readiness. LAW recurring fees count against the 35% cap.

Source of truth for every price and requirement below: the AI Services tab of the 2026 SMB Team Pricing, Products & Packages sheet. Keep this section, `LAW_TIERS` in `scripts/select-package.mjs`, and the Slack bot prompts in `.github/workflows/slack-*.yml` in sync with it.

**Do NOT recommend LAW if:**
- Revenue is under the tier's requirement (Fractional CTO tiers only; AI Workforce Pro and the Foundation Sprint have no revenue requirement — they're limited by user count / any size)
- Firm is solo with no support staff (minimum 1–2 staff needed to engage with implementation)
- Owner shows no openness to staff training or technology adoption

**LAW Tiers:**

| Product | Bundled Price | Standalone Price | Requirements |
|---|---|---|---|
| AI Workforce Pro – Starter | $350/user/mo | — | 1–4 users |
| AI Workforce Pro | $1,597/mo (5 users) + $120/mo per employee over 5 | — | 5+ users |
| Fractional CTO Level 1 | $3,297/mo | $3,797/mo | $400K+ annual revenue |
| Fractional CTO Level 2 | $4,997/mo | $5,797/mo | $1M+ annual revenue |
| Fractional CTO Level 3 | $8,997/mo | $9,997/mo | $3M+ annual revenue |

Fractional CTO setup fee: $0 at every level.

**AI Workforce Pro terms:**
- AI Workforce Pro – Starter: month-to-month contract, 1M AI credits per user, overages $150/mo. Includes access to AI Workforce Pro and a weekly AI Implementation Session.
- AI Workforce Pro: yearly contract, 10M usage credits + 10M bonus credits (20M total), $120/mo per employee over 5, overages $150/mo. Includes access to AI Workforce Pro and a weekly AI Implementation Session.
- There is no standalone price for either AI Workforce Pro tier — do not quote one in the deck.

**Fractional CTO deliverables (per month):**

| | Level 1 | Level 2 | Level 3 |
|---|---|---|---|
| 1:1 sessions with the fCTO | One monthly | Two monthly | Weekly |
| Additional 1-hour sessions (optional) | Up to 2 | Up to 4 | Up to 4 |
| Skills deployed from the skills library (clients keep access; this is set-up help) | Up to 2 | Up to 4 | Up to 4 |
| Custom automations | Up to 1 | Up to 2 | Up to 3 |
| Training videos on skills and automations (as needed) | ✓ | ✓ | ✓ |
| Automation report on skills and automations | ✓ | ✓ | ✓ |
| Law Firm AI Foundation Sprint | — | — | Included |

**Law Firm AI Foundation Sprint (one-time):** includes an AI Readiness Assessment. Any firm size.
- Standalone: $19,997
- Packaged with any other service: $14,997
- Packaged with Fractional CTO Level 1: $8,403
- Packaged with Fractional CTO Level 2: $5,003
- Packaged with Fractional CTO Level 3: $0 (included)

**When to recommend each tier:**
- **AI Workforce Pro – Starter ($350/user/mo, 1–4 users):** Small team wants to adopt AI at the lowest entry cost; the team does the implementation work with the weekly implementation session for support.
- **AI Workforce Pro ($1,597/mo for 5 users):** Same model as Starter for firms with 5+ users — more cost-effective per seat than Starter once a firm has 5+ users.
- **Fractional CTO Level 1 ($3,297/mo):** Revenue $400K+. Owner doesn't have time to run the AI rollout and wants a dedicated Fractional CTO leading it. Prefer this over AI Workforce Pro when the owner says they don't have bandwidth to manage it themselves.
- **Fractional CTO Level 2 ($4,997/mo):** Revenue $1M+. Firm wants a faster rollout — two monthly fCTO sessions, up to 4 skills and up to 2 custom automations a month.
- **Fractional CTO Level 3 ($8,997/mo):** Revenue $3M+. Firm wants weekly fCTO sessions, up to 3 custom automations a month, and the Foundation Sprint included at kickoff.

---

### SELECT AI AVATAR / VIDEO GROWTH ADD-ON

AI Avatar products pair with any active marketing package to drive social and video content using AI-generated avatar footage. Recommend when the firm is already investing in digital marketing and the owner expresses interest in video, social presence, or brand building.

**Escalation: All AI Avatar / Virtual Video Growth packages require Alexis approval before including in a proposal.** Flag in the research notes.

**AI Avatar Pricing:**

| Product | Price | Contract |
|---|---|---|
| One-Time AI Avatar (kickoff + 5 videos) | $1,850 one-time | None |
| Add-On: Virtual Video Growth Using AI Avatar | $1,950/mo + $2,997 setup fee | 12-month, auto-renewal |
| Standalone: Virtual Video Growth Using AI Avatar (Qualified Firms Only) | $3,000/mo + $6,000 setup fee | 12-month, auto-renewal |

**Add-On and Standalone recurring deliverables:** 1 long-form video/mo, 30 short-form videos/mo, YouTube optimization, 5 social media scripts/quarter, quarterly strategy meetings.

**Standalone tier: firm must meet ALL of the following to qualify:**
- $1M+ annual revenue
- Established marketing budget
- Running paid ads (paid social included)
- Established organic social media presence
- Studio setup with proper recording equipment
- Strong intake system in place

Note: Standalone setup fee ($6,000) may be waived if firm demonstrates a legitimate studio setup already in place.

**When to recommend:**
- **One-Time ($1,850):** Firm wants to test AI video content with no recurring commitment. Good for brand-aware firms not yet ready for ongoing video investment.
- **Add-On recurring ($1,950/mo):** Firm is already on a marketing package and wants to accelerate social/video presence. Must have an active SMB marketing relationship.
- **Standalone recurring ($3,000/mo):** Only for qualified firms meeting ALL six criteria above. Requires Alexis approval.

---

### SELECT BOOKKEEPING PACKAGE

Bookkeeping pairs with any active package as a standalone recurring engagement. Recommend when the firm has no dedicated bookkeeper or financials are disorganized — typically a Phase 3 (Optimize) roadmap addition, not a Phase 1 recommendation, unless financials are in immediate crisis.

**Bookkeeping Tiers:**

| Revenue | Level | Bundled Price | Stand-Alone Price | Setup Fee (non-waivable) |
|---|---|---|---|---|
| Under $1M | Level 1 | $1,697/mo | $1,997/mo | $1,500 |
| $1M–$2.9M | Level 2 | $2,197/mo | $2,597/mo | $2,000 |
| $3M–$3.9M | Level 3 | $3,497/mo | $4,597/mo | $2,500 |
| $4M+ | Level 4 | Custom | Custom | Custom |

Each tier includes 2 hours/month of Controller Services in addition to monthly bookkeeping. The setup fee covers one quarter's worth of clean-up and reconciliation; additional cleanup time bills at $75/hr. Bookkeeping is the only product line where the setup fee can never be waived.

**AR/AP/Payroll Add-On** (requires an active Bookkeeping engagement at the matching level):

| Add-On Level | Requires | Additional Hours/mo | Revenue Band |
|---|---|---|---|
| Level 1 | Bookkeeping Level 1 | +12 hrs/mo | Under $1M |
| Level 2 | Bookkeeping Level 2 | +25 hrs/mo | $1.5M–$2.9M |
| Level 3 | Bookkeeping Level 3 | +45 hrs/mo | $3M–$3.9M |

Add-on pricing is custom-scoped — never quote a dollar figure for it in the deck. Flag "AR/AP/Payroll add-on interest — requires custom scoping" in research notes instead.

**When to recommend:** Firm has no bookkeeper, financials are disorganized, or the owner has no visibility into cash position. Add AR/AP/Payroll only if the firm explicitly needs help with receivables, payables, or running payroll beyond standard bookkeeping.

---

### GENERAL ADD-ONS

Standalone add-on line items available from the catalog. Most are one-time or per-unit purchases rather than recurring packages — quote them individually, never bundle their cost into a package's bundled price.

**Marketing add-ons:**

| Add-On | Price |
|---|---|
| Website Hosting & Maintenance | $500/mo |
| Content creation | $0.22/word |
| Content transfer over allotted package amount (incl. multi-site merges) | $300 per 50 pages |
| Premium Backlink | $950/each |
| GBP Set-Up | $500/each |
| Brand Video | $4,997/each |
| Social/Landing Page Videos (6) | $3,997/each |
| Social/Landing Page Videos (12) | $7,497/each |
| Photoshoot | $3,997/each |
| Landing Page (1) | $1,497/each |
| EBook, up to 1.5K words | $1,997/each |
| EBook, up to 3K words | $2,997/each |
| EBook, up to 5K words | $4,997/each |
| Integrations (per platform, up to 5 landing pages, common CRMs only, requires approval) | $500 for approved partners / $150/hr for others (must be scoped) |
| Essentials On-Going SEO (Local + Organic SEO + 10K words/year content) | $900/mo — add-on only, requires an existing Essentials Web/SEO or FSM Essentials client (including hosting-only clients) |
| Ongoing GBP Management (Local SEO, quarterly optimizations) | $500/mo |
| AI Video Avatar Expansion Pack (add-on to an active AI Avatar/Virtual Video Growth package) | $1,800 for an initial batch of 10 additional short-form (<2 min) videos + avatar, $600 per additional batch of 10 |
| At-Home Film Equipment Option (camera + microphone kit, for clients who cannot attend a workshop) | $300 |
| Done-For-You Review Generation, Level 1 (up to 250 Google review requests sent per month; law firm must supply the list) | $500/mo — included at no charge for Growth tier and above |

**Coaching add-ons:**

| Add-On | Price |
|---|---|
| Bookkeeping Hourly Rate | $50/hr |
| Course Bundle (8 courses) | $9,997 |

**In-Person Workshop Ticket** (tiered by the client's existing package):

| Client Type | Price |
|---|---|
| Elite Coach & Master's Circle clients | $697 |
| FCOO & FCFO clients | $997 |
| Coach Essentials / Coach Essentials Plus clients | $1,497 |
| Non-coaching clients | $1,997 |

---

### SELECT OMNISOCIAL AI ADD-ON

OmniSocial AI covers paid and organic social/video content, separate from the Full Service Marketing package. Most tiers are upgrade-only for existing marketing clients — only the 360 bundle can be sold standalone to a new client. Requires a 12-month minimum term. Minimum revenue $500K+ (flexible if the firm is profitable).

**Escalation: every OmniSocial AI proposal requires sales-ops approval with a 72-hour turnaround.** Do not promise same-day terms — flag in research notes.

**OmniSocial AI Pricing** (all tiers carry a $1,850 one-time setup fee):

| Package | Price | Notes |
|---|---|---|
| Content – Standard | $2,297/mo | Organic video presence. Existing-client upgrade only |
| Content – Pro | $3,697/mo | High-volume organic video (2x volume + avatar refreshes). Existing-client upgrade only |
| Ads – Starter | $1,297/mo | Up to $5K ad spend. Existing-client upgrade only |
| Ads – Growth | $1,797/mo | $5K–$10K ad spend. Existing-client upgrade only |
| Ads – Dominate | $2,497/mo | $10K–$25K ad spend. Existing-client upgrade only |
| Ads – Platinum | $3,997/mo | $25K–$50K ad spend. Existing-client upgrade only |
| OmniSocial AI 360 (Content + Ads bundle) | Combined tier price minus $350/mo bundle discount | Sellable standalone to new clients |
| "Omni Total Ads" | Concept — TBD/custom | Not yet a sellable product; do not offer |

**When to recommend:** Firm is already an active SMB marketing client and wants a dedicated paid/organic social presence beyond what their Full Service Marketing package includes. For net-new prospects, only the 360 bundle is available — never offer a single Content or Ads tier standalone to a new client.

---

### SELECT ATTORNEY ASSISTANT (AI INTAKE AGENT) ADD-ON

Attorney Assistant is a volume-priced AI intake agent (IA) product — priced per seat, not a flat fee. Recommend when the firm's intake volume or after-hours coverage is a clear bottleneck.

**Attorney Assistant Pricing (per IA, USD/month):**

| # of IAs | Starting Price/IA | After Day 60 Price/IA (applies to all IAs) |
|---|---|---|
| 1–4 | $2,145 | $2,000 |
| 5–9 | $2,145 | $1,975 |
| 10–19 | $2,000 (for IAs 10+) | $1,950 |
| 20–49 | $1,900 (for IAs 20+) | $1,875 |
| 50+ | Custom | Custom |

**Contract terms:** Technically a 12-month agreement, but includes a 60-day no-questions-asked opt-out. After day 60, cancellation requires 30 days' notice — functions as month-to-month after the first 60 days. This is the one product line where "Clients Can Pivot, But Cannot Cancel" does not strictly apply after day 60.

**When to recommend:** Firm has intake volume or after-hours gaps that a human team can't cover cost-effectively. No documented revenue floor for this product — if fit is unclear, flag "Attorney Assistant fit — confirm qualification with sales rep" rather than guessing.

---

### AD SPEND CALCULATION — CONSERVATIVE AND AGGRESSIVE

**These rules are implemented in code — `scripts/lib/investment.mjs`, run by `select-package.mjs` and `reprice.mjs` — so the same inputs always give the same numbers. Never calculate ad spend or the return by hand; copy `package_decision.json` → `investment`. Keep this section and the code in sync.** Inputs come from the research notes' "Investment inputs" lines (audit-research.md STEP 9): figures the client stated on the call win over every default below.

How the code applies these rules where they are silent or conflict:
1. **Channels costed:** Full Service and Paid Ads packages are costed on Google PPC + LSA + Meta retargeting (the Scoping guide's worked example and "3 primary channels"). Web + SEO packages have no ad spend.
2. **Today's spend:** when the client stated what they spend now, the low end is never below it ("held at launch"). The high end is never below the low end.
3. **Stated budget ceiling:** when the client named the most they can spend a month, the high end stops there (not below the low end).
4. **Tier cap:** product selection is never changed here. When the goal math exceeds the package's cap, the high end stops at the cap and the seller is flagged (tier upgrade or the 10% overage fee is the seller's call). When today's spend is already above the cap, the overage is flagged.
5. **Reverse math:** uses the client's stated cost per signed case, else their stated cost per lead, else the CPL benchmarks below — whichever is most specific to the firm.
6. **Defaults:** case value = the low end of the practice-area default range; close rate 15%; geo Tier 4; competitiveness Medium — each flagged when used. MVA uses the Accident & Injury CPL row; "Other" practice areas have no CPL benchmark, so the return projection is left out unless a cost was stated.
7. **Rounding:** low end to the nearest $100, high end to the nearest $500.
8. **Year one:** 12 × the monthly fees. The pricing tables list no setup fee for marketing, coaching or fractional products, so none is added. Ad spend is shown separately.

Always present ad spend as a range: **Conservative (low end) to Aggressive (high end).**

**Conservative = Sum of channel minimums** for the recommended channels:

| Practice Area | Google PPC Min | LSA Min | Meta Retargeting Min | Meta Lead Gen Min |
|---|---|---|---|---|
| MVA / Car Accidents | $10,000 | $2,000 | $1,500 | $6,000 |
| Accident/Injury (General) | $6,000 | $2,000 | $1,200 | $5,500 |
| Criminal Defense | $5,500 | $2,000 | $1,200 | $4,500 |
| Bankruptcy | $4,500 | $2,000 | $1,200 | $3,500 |
| Family Law | $3,500 | $2,000 | $1,200 | $3,500 |
| Estate Planning | $3,500 | $2,000 | $1,200 | $3,500 |
| Immigration | $3,000 | $2,000 | $1,200 | $3,000 |
| Business Law | $3,500 | $2,000 | $1,200 | $3,500 |

**PI hard floors:** Low competitiveness $5,500 | Medium $7,500 | High $10,000 minimum.
**Criminal Defense + High:** $5,000 minimum.
**Absolute minimum for any paid ads: $3,000/month.**

**Aggressive = 20% rule calculation:**
1. Revenue GOAL × 20% ÷ 12 = Monthly marketing budget (if no goal stated, use 2× current revenue)
2. × Geographic market multiplier (Tier 1 mega markets 1.5× | Tier 2 primary high-density 1.3× | Tier 3 strategic growth 1.15× | Tier 4 significant regional 1.0× | Tier 5 sub-regional 0.85×)
3. If Spanish campaign needed: × 1.50 for PI/MVA or × 1.33 for all other
4. − Marketing package management fee = Available ad spend
5. Run reverse math validation: (Revenue Goal ÷ 12) ÷ Average Case Value = Target cases/month → ÷ Close rate = Required leads → × Blended CPL = Required spend. Use whichever of 20% rule or reverse math is higher.
6. Check against tier cap. If above cap, recommend tier upgrade or note 10% overage fee.

**Common geo tiers:** NYC/LA/Chicago/Houston/Dallas/Atlanta/Philly/DC = Tier 1. Miami/Boston/Phoenix/Seattle/Detroit/SF/Tampa/Minneapolis/Denver/San Diego/Orlando = Tier 2. Charlotte/Austin/Portland/Nashville/Indianapolis/Columbus/Cleveland/Raleigh = Tier 3. Most mid-size cities = Tier 4. Rural/small markets = Tier 5.

**Client-facing "why this range" sentence:** once both numbers are calculated, write one sentence for the BUILD NOTES (its payoff clause becomes `AD_SPEND_WHY` on slide 5) that sells the *payoff*, not the math — what this spend converts or captures for this firm specifically. Ground it in a real specific from the audit: their practice area ("to convert high-intent personal injury searches into signed cases"), a named competitor gap from the research notes ("before [Competitor] captures them first"), or their stated goal/DBM. Do not name the conservative/aggressive calculation basis (channel minimums, the 20% rule, geo-tier multipliers, CPL benchmarks) in this sentence — that level of detail stays in the BUILD NOTES only. This only applies when a marketing/ads package is part of the recommendation.

---

### ROI PROJECTIONS (slide 5 "What that ad spend buys" table)

Computed in code (see AD SPEND CALCULATION). When the client stated their cost per signed case, the projection uses it (cases = ad spend ÷ that cost, no improvement assumed) instead of the CPL benchmarks — a benchmark that contradicts the client's own number is never shown. Next best is a stated cost per lead; the benchmarks below are the fallback.

Calculate separately for conservative and aggressive ad spend amounts.

**Client-facing CPL ranges** (use these — not internal averages):

| Practice Area | Google Search | LSA | Meta Retargeting | Meta Cold |
|---|---|---|---|---|
| Accident & Injury | $630–$780 | $210–$260 | $80–$100 | $150–$190 |
| Criminal Defense | $155–$205 | $140–$180 | $50–$70 | $80–$100 |
| Family Law | $90–$110 | $70–$90 | $50–$65 | $75–$95 |
| Estate Planning | $120–$150 | $55–$75 | $45–$60 | $45–$65 |
| Immigration | $85–$110 | $55–$75 | $50–$65 | $65–$85 |
| Bankruptcy | $80–$100 | $90–$120 | $60–$80 | $70–$90 |
| Business Law | $100–$120 | $110–$140 | $60–$80 | $70–$90 |

**Blended CPL:** Weight by channel spend proportion, use CPL midpoints. For conservative: add 20% cushion. For aggressive: no cushion.

**For each scenario:**
- Leads = Ad Spend ÷ Blended CPL
- Cases = Leads × Close Rate (from transcript, or default 15%)
- Revenue = Cases × Average Case Value (from transcript, or practice area default)
- Return = Revenue ÷ Ad Spend

**Practice area default case values** (use only if not stated in transcript): MVA $5K–$10K | Accident/Injury $5K–$8K | Criminal Defense $3K–$5K | Family Law $3K–$5K | Estate Planning $1.5K–$3K | Immigration $3K–$6K | Bankruptcy $1.5K–$3K | Business Law $3K–$7K. Always disclose when using defaults.

---

### ESCALATION FLAGS (internal — never appear in the deck)

Note these in the BUILD NOTES block (STEP 2) for the sales team. Never put them in a slide field:
- Revenue under $300K → scoping approval required
- Marketing MRR over $10K → scoping approval required
- Ad spend over $25K → scoping approval required
- Criminal Defense in top 10 metro → approval required
- Family Law in top 10 metro → approval required
- Personal Injury in top 40 metro → approval required
- Ad spend below practice area minimums → paid ads team review
- Revenue goal exceeds projected ad revenue → paid ads team review
- Any AI Virtual Video Growth / AI Avatar package → Alexis approval required
- Any Legal AI Workforce (LAW) package → confirm with sales rep that LAW delivery has launched and capacity is available before including in proposal
- Any OmniSocial AI package → sales-ops approval required, 72-hour turnaround
- AR/AP/Payroll Bookkeeping add-on → custom scoping required, never price in the deck
- Attorney Assistant fit unclear → confirm qualification with sales rep before including in proposal

---
### WHAT YOU TOLD US (slide 1 quotes)

This was Block 5 of the retired website. It now picks the client lines for
`PROSPECT_QUOTES` on slide 1 — the client's own words, each with a tie line
saying how the recommendation answers it. (The slide 6 "How this plan
addresses it" panel is gone; slide 1 covers it.)

Content:
- Up to 3 items. Each item = one thing the owner (or another attendee from
  the firm) raised on the discovery call, in their words, plus how the
  recommended package addresses it.
- Pick the ones that most directly support the recommended package — cover
  each package where possible, most central package first (tie to the
  reddest pillar, the DBM, or the largest bundled price). Don't repeat the
  slide 1 KPI headline quote.

Sourcing (non-negotiable):
- Every item must come from the transcript, as captured in the research
  notes (STEP 9B "KPI quotes", STEP 9 fields and `Key prospect quotes`).
  Record the verbatim line for each in the BUILD NOTES (STEP 2). If you
  cannot point to a line, do not use it.
- Quote rules for slide 1 are in audit-pptx.md (verbatim only; never
  strengthen, exaggerate, or combine what they said).
- Problems found only in research (website, reviews, ads) are not eligible —
  those belong on the diagnosis slide (slide 2).

No verbatim transcript: no quotes (`PROSPECT_QUOTES = []`). Never word a
research finding as if the owner said it ("you told us", "you mentioned",
"you said").

Never include (the deck is forwarded to partners and staff):
- Named employees, or criticism of an identifiable staff member
- Personal, health, or family matters
- Partner or co-owner disputes
- Specific financial-distress figures (debt, missed payroll, overdrafts)
If one of these is the strongest item, generalize it (e.g. "the firm
depends on you for every decision") or pick a different one.

Language rules:
- Tie lines say how the recommendation addresses it — never promise outcomes,
  launch dates, timelines, lead or click counts, or deliverables outside
  the signed agreement.
- Never use the phrase "pain points" (or other internal closer language)
  in client-facing copy.
- Every "addresses it" clause must connect to something SMB Team actually
  delivers. Never mention live chat. Never mention CRM setup.

---

## FINAL CHECK

Run these with bash — do not re-read the whole `.py`:

```bash
PY=$(ls "[friendly-name]"/*_Proposal.py | head -1)
grep -nE "[\"'][^\"']*FILL[^\"']*[\"']" "$PY" || true               # no FILL placeholder left in a string value
grep -n "UNCONFIRMED" "$PY" | grep -vE '^[0-9]+:\s*#' || true    # no unverified figure outside the BUILD NOTES comments
grep -c "BUILD NOTES" "$PY"                                   # workings recorded (expect 1)
jq -e '.investment.products | length > 0' "[friendly-name]/package_decision.json"   # computed investment present (expect true)
diff <(sed -n '/LAYOUT ENGINE/,$p' "Design Files/audit_pptx_template.py") <(sed -n '/LAYOUT ENGINE/,$p' "$PY")
wc -c "[friendly-name]"/*_Proposal.pptx
```

The first two must print nothing, the diff must print nothing, the `jq` check must print `true` (if not, run `node scripts/reprice.mjs [friendly-name]` and rebuild), and the `.pptx` must not be empty. Fix anything flagged, re-run the script, then commit.

---

## COMMIT AND PUSH

Commit to the branch you are on — in the pipeline that is `main` (production) or an `audit-test/**` branch (test mode). Never switch branches.

```bash
git add "[friendly-name]/"*_Proposal.py "[friendly-name]/"*_Proposal.pptx "[friendly-name]/smb_team_logo.png"
git add "[friendly-name]/package_decision.json" 2>/dev/null || true
git commit -m "Add proposal deck: [Firm Name] ([Date])"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
git pull --rebase origin "$BRANCH" && GIT_TERMINAL_PROMPT=0 git push origin "HEAD:$BRANCH"
git log -1 --format="%H %s"
```

Report the commit hash.

---

IMPORTANT NOTE:

Git vs. GitHub MCP — when to use which (Claude Code on the Web)

Sessions running on Claude Code on the Web have two distinct GitHub paths and should use both, not just one:

Local git CLI for git-shaped operations: git pull, git fetch, git add, git commit, git push, git diff, etc. The session's harness sets up local clones at /home/user/<repo>/ with the origin remote pointing at a local HTTP proxy (http://local_proxy@127.0.0.1:<port>/git/...). That proxy is authenticated, sanctioned, and identical to what the MCP server is using under the hood. You can git push normally. This is the right path for any change that involves committing files — especially large ones, where the GitHub MCP write tools (create_or_update_file, push_files) hit a stream-idle timeout above ~14–25 KB of inline file content per call.

GitHub MCP tools (prefixed mcp__github__) for GitHub-platform operations that aren't a git command: opening / commenting on / reviewing PRs, reading issues, querying CI status, browsing repo metadata, etc. These are the only path for those operations since you don't have gh / hub / direct REST access.

Anti-pattern to avoid: routing every file edit through mcp__github__create_or_update_file because the system prompt says "use the GitHub MCP server tools for ALL GitHub interactions." That phrasing was written to differentiate from forbidden tools likeghCLI, and it's been causing sessions to stall on stream timeouts when committing modest-sized files. Read it as: use MCP for GitHub-the-platform operations (PRs, issues, comments, CI), not for git-the-tool operations (commits, pushes, pulls). The session's own setup already points you at how to commit — see the "Git Operations" block in your system prompt for the canonical git push -u origin <branch> recipe.

Quick check at start of session:

ls /home/user/                        # see what repos are cloned
cd /home/user/<repo> && git remote -v # see the proxy URL
git fetch origin                       # confirm push/pull plumbing is live
If git fetch works, git push will work too — use it for commits.
