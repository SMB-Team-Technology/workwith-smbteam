# SMB Team — Scoping & Ad Spend Calculation Guide
## Referenced by the Audit Agent System Prompt for Package Selection, Ad Spend, and ROI Projections

---

## TABLE OF CONTENTS

1. [Purpose and When to Use This Guide](#1-purpose)
2. [Step 1 — Extract Discovery Call Data](#2-extract-data)
3. [Step 2 — Determine Market Tier and Geographic Multiplier](#3-market-tier)
4. [Step 3 — Calculate Ad Spend Using the 20% Rule](#4-ad-spend-calc)
5. [Step 4 — Validate Against Practice Area Minimums](#5-validate-minimums)
6. [Step 5 — Select the Marketing Package](#6-marketing-package)
7. [Step 6 — Select the Non-Marketing Package](#7-non-marketing-package)
8. [Step 7 — Validate Total Investment Against 35% Cap](#8-validate-cap)
9. [Step 8 — Calculate ROI Projections](#9-roi-projections)
10. [Step 9 — Scope Website and SEO Requirements](#10-seo-scoping)
11. [Step 10 — Check Escalation Flags](#11-escalation)
12. [Step 11 — Handle Missing Data and Edge Cases](#12-edge-cases)
13. [Reference Tables](#13-reference-tables)

---

<a id="1-purpose"></a>
## 1. PURPOSE AND WHEN TO USE THIS GUIDE

This guide replaces the manual scoping process previously done by the internal team. When the audit agent reaches Part Three (Package Recommendation Logic) of the system prompt, it must follow every step in this guide sequentially to produce an accurate, data-driven recommendation.

The output of this guide feeds directly into:
- **Block 2** of section_11_next_steps.html — package blocks with deliverables
- **Block 3** — investment rows with retail and bundled prices
- **Block 4** — ad spend amount, estimated case value, estimated cases, estimated revenue
- **Block 5** — first 90 days action bullets
- **Block 6** — three phase cards with milestone triggers

**Non-negotiable principles:**
- This is a prescription, not a menu. The client gets told what they need, not asked what they want.
- Use ranges, not absolutes, for all projections. Better to under-promise and over-deliver.
- Every number must be traceable to a formula or benchmark in this guide.
- The 35% cap on total monthly spend (management fees + ad spend) relative to monthly revenue is a hard constraint.
- Minimum MRR is $3,497/month. Never recommend below this.

---

<a id="2-extract-data"></a>
## 2. STEP 1 — EXTRACT DISCOVERY CALL DATA

Before any calculations begin, extract the following data points from the discovery call transcript. These map to what the sales team is supposed to gather per the Discovery Call Question Guide and the Scoping Request Form.

### Required Data Points (must find or infer):

| Data Point | Source | Default If Missing |
|---|---|---|
| Firm name | Provided with audit inputs | — |
| Website URL | Provided with audit inputs | — |
| Primary location / most aggressive geo | Transcript or provided | — |
| Practice areas | Transcript | CANNOT DEFAULT — flag for follow-up |
| Case types they want to grow | Transcript | Use practice areas as proxy |
| Average case value (most desirable cases) | Transcript | See Practice Area Defaults table below |
| Current annual revenue | Transcript | CANNOT DEFAULT — flag for follow-up |
| Revenue goal (12-24 months) | Transcript | If not stated, use 2x current revenue |
| Current close rate (lead to signed client) | Transcript | 15% (industry mid-range) |
| Team size and roles | Transcript | Assume under 5 if not mentioned |
| Number of locations | Transcript or research | 1 if not mentioned |
| Current ad budget (PPC, LSA, Social) | Transcript | $0 if not mentioned |
| Current non-ads spending (website, SEO) | Transcript | $0 if not mentioned |
| Has a GBP | Research (Pass 1) | Check during audit |
| Interested in keeping current website | Transcript | Assume no if site scores poorly |
| Spanish translation needed | Transcript | No if not mentioned |
| Multiple websites | Transcript or research | No if not mentioned |
| CRM in use | Transcript | Not applicable (SMB doesn't manage CRM) |
| Dominant Buying Motive | Transcript (already extracted in Part Two) | — |

### Practice Area Default Case Values (use ONLY when not provided):

| Practice Area | Default Average Case Value | Notes |
|---|---|---|
| Personal Injury (general) | $5,000–$8,000 | Highly variable — settlement-based |
| Car Accidents / MVA | $5,000–$10,000 | Depends on severity |
| Truck Accidents | $15,000–$50,000 | Higher severity cases |
| Criminal Defense | $3,000–$5,000 | Per case, retainer-based |
| Family Law | $3,000–$5,000 | Per case, retainer-based |
| Estate Planning | $1,500–$3,000 | Per engagement |
| Immigration | $3,000–$6,000 | Per case type varies widely |
| Bankruptcy | $1,500–$3,000 | Per filing |
| Business Law | $3,000–$7,000 | Per engagement |
| Disability | $2,000–$5,000 | Contingency-based |

**IMPORTANT:** If using defaults, always disclose in the audit: "Based on industry benchmarks for [practice area] firms. If your actual case values differ, projected revenue will scale accordingly."

---

<a id="3-market-tier"></a>
## 3. STEP 2 — DETERMINE MARKET TIER AND GEOGRAPHIC MULTIPLIER

Using the firm's primary location, classify them into one of the following market tiers. Use DMA (Designated Market Area) population, not city population.

### Tier 1 — Mega Markets (5M+ DMA population) → 1.5x multiplier

| Market | Approximate DMA Population |
|---|---|
| New York | ~19M |
| Los Angeles | ~12M |
| Chicago | ~9M |
| Houston | ~7M |
| Dallas–Fort Worth | ~7M |
| Atlanta | ~6.3M |
| Philadelphia | ~6M |
| Washington DC | ~5.6M |

### Tier 2 — Primary High-Density (2.5M–5M DMA) → 1.3x multiplier

| Market | Approximate DMA Population |
|---|---|
| Miami–Fort Lauderdale | ~4.5M |
| Boston | ~4.4M |
| Phoenix | ~3.5M |
| Seattle–Tacoma | ~3.4M |
| Detroit | ~3.3M |
| San Francisco Bay Area | ~3.3M |
| Tampa–St. Petersburg | ~3.1M |
| Minneapolis–St. Paul | ~3M |
| Denver | ~3M |
| San Diego | ~3M |
| Orlando | ~2.6M |
| Sacramento | ~2.5M |

### Tier 3 — Strategic Growth (1.5M–2.5M DMA) → 1.15x multiplier

| Market | Approximate DMA Population |
|---|---|
| Charlotte | ~2.4M |
| Baltimore | ~2.3M |
| Austin | ~2.2M |
| Portland | ~2.2M |
| San Antonio | ~2.1M |
| Indianapolis | ~2M |
| Nashville | ~2M |
| Salt Lake City | ~1.9M |
| Columbus | ~1.8M |
| Cincinnati | ~1.8M |
| Kansas City | ~1.7M |
| Cleveland | ~1.7M |
| Raleigh-Durham | ~1.6M |

### Tier 4 — Significant Regional (600K–1.5M DMA) → 1.0x multiplier (base rate)

| Market | Approximate DMA Population |
|---|---|
| Milwaukee | ~1.4M |
| Las Vegas | ~1.3M |
| Oklahoma City | ~1M |
| Memphis | ~1M |
| Albuquerque | ~980K |
| Louisville | ~950K |
| Tulsa | ~800K |
| Fresno | ~750K |
| Tucson | ~700K |
| El Paso | ~650K |

### Tier 5 — Sub-Regional / Rural (Under 600K DMA) → 0.85x multiplier

All markets not listed above with DMA population under 600K.

**NOTE:** If a firm targets multiple locations spanning different tiers, use the multiplier of the most competitive market they are targeting.

### Spanish Campaign Modifier (applied on top of geo multiplier):
- MVA / Personal Injury firms requiring Spanish campaigns: Add 50% to total ad spend
- All other practice areas requiring Spanish campaigns: Add 33% to total ad spend

---

<a id="4-ad-spend-calc"></a>
## 4. STEP 3 — CALCULATE AD SPEND USING THE 20% RULE

This is the core ad spend calculation. Follow each sub-step in order.

### Step 3A — Calculate Base Annual Marketing Budget

```
Annual Marketing Budget = Revenue Goal × 20%
```

Use the firm's stated revenue GOAL (not current revenue). If no goal is stated, use 2x current revenue as the target.

**Example:** Firm currently at $500K, goal is $1M
→ $1,000,000 × 20% = $200,000/year

### Step 3B — Convert to Monthly Budget

```
Monthly Marketing Budget = Annual Marketing Budget ÷ 12
```

**Example:** $200,000 ÷ 12 = $16,667/month

### Step 3C — Apply Geographic Multiplier

```
Geo-Adjusted Budget = Monthly Marketing Budget × Market Tier Multiplier
```

**Example:** $16,667 × 1.0 (Tier 4) = $16,667/month
**Example:** $16,667 × 1.5 (Tier 1, NYC) = $25,000/month

### Step 3D — Apply Spanish Campaign Modifier (if applicable)

```
Final Adjusted Budget = Geo-Adjusted Budget × (1 + Spanish Modifier)
```

Where Spanish Modifier = 0.50 for PI/MVA or 0.33 for all other practice areas.

### Step 3E — Separate Management Fees from Ad Spend

The Monthly Marketing Budget calculated above represents TOTAL marketing investment (management fees + ad spend). To isolate the ad spend:

```
Available Ad Spend = Final Adjusted Budget − Marketing Package Management Fee
```

**Example:** Total budget is $16,667. Full Service Marketing Starter is $4,847/month.
→ Available for ad spend: $16,667 − $4,847 = $11,820/month

### Step 3F — Run Reverse Math Validation

Separately calculate the budget needed to hit their case goals:

```
Target Monthly Cases = (Revenue Goal ÷ 12) ÷ Average Case Value
Required Monthly Leads = Target Monthly Cases ÷ Close Rate
Required Ad Spend = Required Monthly Leads × Blended CPL (from Section 13 tables)
```

Compare the reverse math ad spend to the 20% rule ad spend. **Use whichever is higher.** If the reverse math number is significantly higher than the 20% rule number, this signals the firm's goals may be aggressive relative to their budget — note this in the audit.

### Step 3G — Apply Floor: Practice Area Channel Minimums

Check the calculated ad spend against the practice area minimums in Section 13. If the calculated ad spend is below the minimum for the channels being recommended, **use the minimum instead.** Minimums exist because certain channels require threshold spend to be viable.

### Step 3H — Apply Ceiling: Marketing Tier Ad Spend Caps

Check the ad spend against the maximum for their marketing tier:

| Marketing Tier | Max Ad Spend Managed |
|---|---|
| Essentials (Full Service) | $7,500/month |
| Essentials (LSA+PPC or LSA+Social) | $5,000/month |
| Starter (Full Service) | $25,000/month |
| Starter (LSA+PPC) | $20,000/month |
| Starter (LSA+PPC+Social) | $25,000/month |
| Growth | $50,000/month |
| Dominate | $75,000/month |
| Platinum | $150,000/month |

If the calculated ad spend exceeds the tier cap, either:
1. Recommend upgrading to the next marketing tier, OR
2. Note that an overage fee of 10% applies on ad spend above the cap

### Step 3I — Produce a Low-to-High Ad Spend Range

The ad spend recommendation is always presented as a range with two numbers:

**Conservative (Low End):** The sum of the practice area channel minimums for the channels being recommended. This is the minimum viable spend to run those channels effectively. Pull the channel minimums from the table in Step 4.

```
Conservative Ad Spend = Σ (Channel Minimum for each recommended channel)
```

**Example:** Family Law firm running PPC + LSA + Meta Retargeting
→ $3,500 + $2,000 + $1,200 = $6,700/month conservative

**Aggressive (High End):** The full 20% rule calculation from Steps 3A–3H above. This is the spend level designed to hit the firm's growth goals.

If the conservative number is higher than the aggressive number (rare, but possible for very small firms), use the conservative number as both ends — the firm cannot spend less than the minimums.

If the aggressive number exceeds the marketing tier cap, note the overage or recommend a tier upgrade per Step 3H.

### Summary: Ad Spend Calculation Flow

```
CONSERVATIVE (LOW END):
    Sum of practice area channel minimums for recommended channels
    → Check against Tier Cap
    → Conservative Ad Spend

AGGRESSIVE (HIGH END):
    Revenue Goal × 20% ÷ 12
    → × Geo Multiplier
    → × Spanish Modifier (if applicable)
    → − Management Fee = Available Ad Spend
    → Compare to Reverse Math (use higher)
    → Check against Practice Area Minimums (use higher if below)
    → Check against Tier Cap (upgrade tier or note overage)
    → Aggressive Ad Spend

Present as: "$[Conservative] – $[Aggressive]/month"
```

---

<a id="5-validate-minimums"></a>
## 5. STEP 4 — VALIDATE AGAINST PRACTICE AREA CHANNEL MINIMUMS

The following are the minimum monthly ad spends by channel for each practice area. These represent the floor for running viable campaigns. If a firm's budget cannot support at least the minimums for the channels being recommended, reduce the number of channels rather than running any channel below its minimum.

### Channel Minimums by Practice Area:

| Practice Area | Google PPC Min | PMax/YouTube Min | LSA Min | Meta Retargeting Min | Meta Lead Gen Min |
|---|---|---|---|---|---|
| MVA (Car/Truck) | $10,000 | $1,000 | $2,000 | $1,500 | $6,000 |
| Accident/Injury (General) | $6,000 | $1,000 | $2,000 | $1,200 | $5,500 |
| Criminal Defense | $5,500 | $500 | $2,000 | $1,200 | $4,500 |
| Bankruptcy | $4,500 | $500 | $2,000 | $1,200 | $3,500 |
| Family Law | $3,500 | $500 | $2,000 | $1,200 | $3,500 |
| Estate Planning | $3,500 | $500 | $2,000 | $1,200 | $3,500 |
| Business Law | $3,500 | $500 | $2,000 | $1,200 | $3,500 |
| Immigration | $3,000 | $500 | $2,000 | $1,200 | $3,000 |
| Other (Niche) | $3,000 | $500 | $2,000 | $1,200 | $3,000 |

### Channel Priority Order (when budget is limited):

If the firm's budget cannot support all channels, prioritize in this order:

1. **Google PPC (Search Ads)** — highest intent leads, fastest to produce results
2. **Local Service Ads (LSA)** — pay-per-lead, appears above all other ads, strong for local firms
3. **Meta Retargeting** — recaptures website visitors who didn't convert, low cost
4. **Meta Lead Gen (Cold)** — builds awareness and generates leads from new audiences
5. **PMax / YouTube Awareness** — brand building, lowest priority for ROI-focused budgets

**Minimum viable ad spend for ANY paid ads package: $3,000/month**

**Minimum for running all 3 primary channels (PPC + LSA + Meta): Typically $8,000/month**

### Practice Area-Specific Ad Spend Floors (from CPQ rules):

These are hard floors. If the recommended ad spend falls below these, the recommendation must be flagged:

| Condition | Minimum Ad Spend |
|---|---|
| Personal Injury + Low competitiveness market | $5,500/month |
| Personal Injury + Medium competitiveness market | $7,500/month |
| Personal Injury + High competitiveness market | $10,000/month |
| Criminal Defense + High competitiveness market | $5,000/month |

**Competitiveness Assessment:** Determine competitiveness based on the audit's digital presence findings:
- **Low:** Few competitors running ads, sparse LSA results, moderate review counts
- **Medium:** Multiple competitors running ads, competitive LSA landscape, strong review counts
- **High:** Saturated ad space, aggressive LSA competition, 500+ review competitors, Tier 1-2 market

---

<a id="6-marketing-package"></a>
## 6. STEP 5 — SELECT THE MARKETING PACKAGE

### Step 5A — Apply Eligibility Filters

Before selecting, remove ineligible packages:

**Practice Area Filters:**
- **Personal Injury firms:** Remove ALL Essentials marketing packages AND the LSA-only add-on. Minimum starting tier is Starter.
- **Criminal Defense in High competitiveness markets:** Remove ALL Essentials marketing packages. LSA-only still permitted.

**Revenue Filters:**
- **Over $1M revenue:** Remove ALL Essentials marketing products.
- **Under $1M revenue:** Remove Dominate and Platinum marketing tiers.
- **Under $250K revenue:** Must verify client has funds to cover 4 months of services. If not verified, do not proceed.

### Step 5B — Determine Marketing Package Type

Based on the firm's needs identified during the audit, determine which type of marketing package fits:

**Full Service Marketing** (recommended for most firms) — includes Website, SEO, LSA, Google PPC, and Social. Best value, most comprehensive.

**Web + SEO only** — for firms that only need organic presence and a website rebuild, not paid ads. Uncommon for audit recommendations since most firms need leads now.

**Ads only (LSA+PPC, LSA+PPC+Social, LSA+Social)** — for firms that already have a strong website and SEO. CANNOT be sold standalone; must be paired with another core service (coaching/advisory).

### Step 5C — Select the Tier by Revenue

| Revenue Range | Default Tier | Full Service Price (Bundled) | Notes |
|---|---|---|---|
| $250K–$400K | Essentials | $3,397/mo | Hidden for PI; if hidden, move to Starter |
| $400K–$1M | Starter | $4,847/mo | Most common starting point |
| $1M–$3M | Growth | $7,397/mo | For firms with substantial growth goals |
| $1M+ aggressive goals | Dominate | $10,497/mo | For firms wanting to dominate their market |
| $3M+ | Platinum | $15,997/mo | Highest tier |

**Boundary decisions:** When a firm falls on the border between tiers, the deciding factor is their goals:
- If they want to maintain and grow steadily → lower tier
- If they want aggressive growth and market dominance → higher tier
- If their calculated ad spend exceeds the lower tier's cap → must use higher tier

### Step 5D — Marketing Package Sub-Options by Tier

Each tier offers sub-packages. Default recommendation is Full Service Marketing unless there's a specific reason not to:

**Essentials Tier:**
| Sub-Package | Bundled Price | Ad Spend Cap | Best For |
|---|---|---|---|
| LSA + PPC Essentials | $1,497/mo | $5,000 | Firms that only need paid ads + have good website |
| LSA + Social Essentials | $1,497/mo | $5,000 | Firms wanting social over PPC |
| Web + SEO Essentials | $1,497/mo | N/A | Firms that only need a website and SEO |
| Web + SEO + LSA Essentials | $2,797/mo | $5,000 | Website + SEO + basic paid |
| Full Service Marketing Essentials | $3,397/mo | $7,500 | Everything (DEFAULT recommendation) |

**Starter Tier:**
| Sub-Package | Bundled Price | Ad Spend Cap | Best For |
|---|---|---|---|
| LSA + PPC Starter | $1,997/mo | $20,000 | Ads-only with good existing website |
| LSA + PPC + Social Starter | $2,497/mo | $25,000 | All ads, good existing website |
| Web + SEO Starter | $3,497/mo | N/A | Website + SEO only |
| Full Service Marketing Starter | $4,847/mo | $25,000 | Everything (DEFAULT recommendation) |

**Growth Tier:**
| Sub-Package | Bundled Price | Ad Spend Cap | Best For |
|---|---|---|---|
| LSA + PPC + Social Growth | $3,497/mo | $50,000 | All ads, strong existing website |
| Web + SEO Growth | $4,897/mo | N/A | Website + SEO only |
| Full Service Marketing Growth | $7,397/mo | $50,000 | Everything (DEFAULT recommendation) |

**Dominate Tier:**
| Sub-Package | Bundled Price | Ad Spend Cap | Best For |
|---|---|---|---|
| LSA + PPC + Social Dominate | $5,000/mo | $75,000 | All ads, strong existing website |
| Web + SEO Dominate | $6,597/mo | N/A | Website + SEO only |
| Full Service Marketing Dominate | $10,497/mo | $75,000 | Everything (DEFAULT recommendation) |

**Platinum Tier:**
| Sub-Package | Bundled Price | Ad Spend Cap | Best For |
|---|---|---|---|
| LSA + PPC + Social Platinum | $7,497/mo | $150,000 | All ads, strong existing website |
| Web + SEO Platinum | $9,597/mo | N/A | Website + SEO only |
| Full Service Marketing Platinum | $15,997/mo | $150,000 | Everything (DEFAULT recommendation) |

### Step 5E — Determine If Website Build Is Needed

Evaluate from the audit's website findings:
- **Site needs rebuild if:** PageSpeed mobile score below 50, design is outdated (5+ years), not mobile responsive, poor messaging, no practice area pages, no attorney bios, significant trust signal gaps
- **Site is acceptable if:** Modern design, mobile responsive, reasonable speed scores, clear messaging, practice area pages exist

If the site needs a rebuild, the marketing package MUST include Web + SEO (Full Service or Web+SEO sub-package). If the site is acceptable, an ads-only sub-package is possible but Full Service is still preferred for comprehensive coverage.

**Website contract timing rule:**
- If existing website contract is up within 4 months OR site doesn't meet standards → build new site, sell Full Service Marketing
- If existing contract is up in 5-12 months → sell "gateway plan" (coaching only or ads-only) until 3 months before renewal, then transition to Full Service

---

<a id="7-non-marketing-package"></a>
## 7. STEP 6 — SELECT THE NON-MARKETING PACKAGE

Every client must have at least one non-marketing package. Clients with marketing + non-marketing services churn at half the rate.

### Step 6A — Apply Eligibility Filters

**ELIMINATED PRODUCTS — never recommend:**
- Coach Essentials (eliminated)
- Coach Essentials Plus (eliminated)

**Revenue Filters:**
- **Under $500K:** Remove ALL Fractional COO and Fractional CFO products and all bundles containing them
- **Under $1M:** Remove Master's Circle and all bundles containing it
- **Over $1M:** Remove all remaining Essentials coaching products

**Team Filters:**
- **Fewer than 5 team members:** Remove ALL Master's Circle options
- **No dedicated ops, marketing, or intake team member:** Remove ALL Master's Circle options

### Step 6B — Select Based on Revenue, Team, and Needs

| Revenue | Team Size | Primary Need | Recommended Package | Bundled Price |
|---|---|---|---|---|
| $250K–$400K | Any | Growth coaching | Elite Coach | $2,600/mo |
| $400K–$1M | Any | Growth coaching + accountability | Elite Coach Plus | $3,200/mo |
| $400K–$1M | Growing team | Coaching + operations help | Elite Coach + FCOO Advisor | $5,694/mo |
| $1M+ | Under 5 | Coaching + strategy | Elite Coach Plus | $3,200/mo |
| $1M+ | Under 5 | Operations + team building | FCOO Advisor (standalone) | $3,297/mo |
| $1M+ | 5+ with dedicated staff | Community + team training | Master's Circle | $4,600/mo |
| $1M+ | 5+ with dedicated staff | Community + operations | Master's Circle + FCOO Advisor | $6,694/mo |
| $1M+ | 5+ established leaders | Advanced operations | FCOO Director (standalone) | $4,997/mo |
| $2M+ | 5+ with dedicated staff | Full support | Master's Circle + FCOO Director | $8,394/mo |
| $3M+ | Large team | Executive-level operations | FCOO Partner | $8,997/mo |
| $3M+ | Large established team | Full ecosystem | Master's Circle + FCOO Partner | $12,394/mo |

### Step 6C — When to Add Fractional CFO

Add Fractional CFO Advisor ($3,297/mo bundled) when ANY of these signals appear in the transcript:
- Owner mentions profit problems or cash flow issues
- Revenue is growing but owner isn't taking home more
- No financial reporting or visibility into margins
- Owner doesn't know their cost per acquisition
- Explicitly mentions wanting help with finances

**Revenue minimum for FCFO:** $400K+ for Advisor, $1M+ for Director, $3M+ for Partner

### Step 6D — When to Add Bookkeeping

Add Bookkeeping when the firm has no current bookkeeper or their financials are a mess:

| Revenue | Bookkeeping Level | Bundled Price | Setup Fee |
|---|---|---|---|
| Under $1M | Level 1 | $1,697/mo | $1,500 (CANNOT be waived) |
| $1M–$2.9M | Level 2 | $2,197/mo | $2,000 (CANNOT be waived) |
| $3M–$3.9M | Level 3 | $3,497/mo | $2,500 (CANNOT be waived) |
| $4M+ | Level 4 | Custom | Custom |

**Note:** Bookkeeping is typically a Phase 3 recommendation (growth roadmap), not Phase 1 — unless the firm's financials are in such poor shape that it's an immediate need.

### Step 6E — LSA Add-On for Coaching-Only Clients

If a client is getting coaching only (no marketing package), they can add LSA management for $900/month. This gives them a basic lead generation channel while they build toward full marketing.

---

<a id="8-validate-cap"></a>
## 8. STEP 7 — VALIDATE TOTAL INVESTMENT AGAINST 35% CAP

### Calculate Total Monthly SMB Spend:

```
Total Monthly Spend = Marketing Package Fee + Non-Marketing Package Fee + Ad Spend + Any Add-Ons
```

### Check Against 35% Revenue Cap:

```
Monthly Revenue = Annual Revenue ÷ 12
Maximum Recommended Spend = Monthly Revenue × 35%
```

**If Total Monthly Spend exceeds 35% of monthly revenue:**

1. First, check if the client is growing — if their GOAL revenue supports the spend at 35%, note this: "Your current revenue of $X supports a maximum investment of $Y/month. However, as you grow toward your goal of $Z, this investment will represent a decreasing percentage of revenue."
2. If still too high, reduce ad spend first (but not below practice area minimums)
3. If still too high, consider a lower marketing tier
4. If still too high, simplify the non-marketing recommendation (e.g., Elite Coach instead of Elite Coach + FCOO)
5. Never drop below $3,497/month total MRR

### Calculate Savings for Block 3:

```
Total Savings = Σ (Stand Alone Price − Bundled Price) for EVERY package in the recommendation
```

Always show savings from EVERY package combined, not just one.

**Stand Alone vs. Bundled Reference:**

| Package | Stand Alone | Bundled | Savings |
|---|---|---|---|
| Full Service Marketing Starter | $5,697 | $4,847 | $850 |
| Full Service Marketing Growth | $8,997 | $7,397 | $1,600 |
| Full Service Marketing Dominate | $12,497 | $10,497 | $2,000 |
| Full Service Marketing Platinum | $18,997 | $15,997 | $3,000 |
| Elite Coach | $3,497 | $2,600 | $897 |
| Elite Coach Plus | $3,497 | $3,200 | $297 |
| Master's Circle | $4,997 | $4,600 | $397 |
| FCOO Advisor | $3,797 | $3,297 | $500 |
| FCOO Director | $5,797 | $4,997 | $800 |
| FCOO Partner | $9,997 | $8,997 | $1,000 |
| FCFO Advisor | $3,797 | $3,297 | $500 |
| FCFO Director | $5,797 | $4,997 | $800 |
| FCFO Partner | $9,997 | $8,997 | $1,000 |

---

<a id="9-roi-projections"></a>
## 9. STEP 8 — CALCULATE ROI PROJECTIONS

This section produces the numbers for Block 4 of section_11_next_steps.html. All values are labeled as "estimates" in the output.

### Step 8A — Determine Blended CPL

Based on the channels being recommended, calculate a blended (weighted average) CPL using the benchmarks below. Weight by the proportion of ad spend going to each channel.

**2025 Average CPLs by Practice Area and Channel (Rolling 90 Days, Updated 4/14/2026):**

| Practice Area | LSA Avg | Google Search Avg | Meta Retarget Avg | Meta Cold Avg |
|---|---|---|---|---|
| Accident & Injury | $207 | $627 | $95 | $174 |
| Criminal Defense | $137 | $153 | $64 | $90 |
| Disability | $72 | $77 | — | — |
| Estate Planning | $54 | $118 | $93 | $43 |
| Family Law | $66 | $88 | $51 | $61 |
| Immigration | $55 | $83 | $56 | $61 |
| Business Law | $109 | $95 | — | — |
| Bankruptcy | $92 | $78 | — | — |

**Client-Facing CPL Ranges (use these in the audit presentation, not internal averages):**

| Practice Area | Google Search CPL | LSA CPL | Meta Retargeting CPL | Meta Cold CPL |
|---|---|---|---|---|
| Accident & Injury | $630–$780 | $210–$260 | $80–$100 | $150–$190 |
| Criminal Defense | $155–$205 | $140–$180 | $50–$70 | $80–$100 |
| Bankruptcy | $80–$100 | $90–$120 | $60–$80 | $70–$90 |
| Business Law | $100–$120 | $110–$140 | $60–$80 | $70–$90 |
| Estate Planning | $120–$150 | $55–$75 | $45–$60 | $45–$65 |
| Family Law | $90–$110 | $70–$90 | $50–$65 | $75–$95 |
| Immigration | $85–$110 | $55–$75 | $50–$65 | $65–$85 |

**Blended CPL calculation:** For projections, use a blended CPL based on recommended channel mix. Use the MID-POINT of client-facing ranges, then add a 20% cushion for conservative projections.

```
Blended CPL = Σ (Channel CPL × Channel % of Ad Spend) × 1.20
```

**Example:** Criminal Defense firm running PPC (50% of spend), LSA (30%), Meta retargeting (20%)
- PPC CPL midpoint: $180
- LSA CPL midpoint: $160
- Meta Retargeting CPL midpoint: $60
- Blended = ($180 × 0.50) + ($160 × 0.30) + ($60 × 0.20) = $90 + $48 + $12 = $150
- With 20% cushion: $150 × 1.20 = $180 blended CPL

### Step 8B — Calculate Expected Monthly Leads for Both Ad Spend Levels

Run the lead calculation separately for the conservative and aggressive ad spend amounts from Step 3I:

```
Conservative Leads = Conservative Ad Spend ÷ Blended CPL (with 20% cushion)
Aggressive Leads = Aggressive Ad Spend ÷ Blended CPL (without cushion)
```

**Example:** Family Law firm, conservative $6,700, aggressive $11,500, blended CPL $150 (no cushion) / $180 (with cushion)
- Conservative: $6,700 ÷ $180 = 37 leads/month
- Aggressive: $11,500 ÷ $150 = 77 leads/month
→ Present as "37–77 estimated leads per month"

### Step 8C — Calculate Expected Monthly Cases for Both Levels

```
Conservative Cases = Conservative Leads × Close Rate
Aggressive Cases = Aggressive Leads × Close Rate
```

Use the close rate from the discovery call. If not provided, default to 15%.

**Example:** 37–77 leads × 15% close rate = 6–12 estimated new cases per month

### Step 8D — Calculate Expected Monthly Revenue Impact for Both Levels

```
Conservative Revenue = Conservative Cases × Average Case Value
Aggressive Revenue = Aggressive Cases × Average Case Value
```

Use the case value from the discovery call. If not provided, use practice area defaults from Section 2.

**Example:** 6–12 cases × $4,000 average case value = $24,000–$48,000 estimated monthly revenue

### Step 8E — Present the ROI Summary

For Block 4 of section_11_next_steps.html, present BOTH scenarios:

1. **Recommended Monthly Ad Spend:** $[conservative] – $[aggressive] range
2. **Estimated Case Value:** $[amount] (from discovery call or practice area default)
3. **Conservative Scenario:** $[low spend]/month → [leads] leads → [cases] cases → $[revenue]/month revenue → [X.X]x return
4. **Aggressive Scenario:** $[high spend]/month → [leads] leads → [cases] cases → $[revenue]/month revenue → [X.X]x return

**Narrative framing:** "At the conservative level ($[X]/month), you can expect [A]–[B] new cases per month. At the aggressive level ($[Y]/month), that grows to [C]–[D] cases. Both scenarios produce a positive return on ad spend."

The Sales Companion PDF mirrors this structure. See Step K in the system prompt.

---

<a id="10-seo-scoping"></a>
## 10. STEP 9 — SCOPE WEBSITE AND SEO REQUIREMENTS

This section determines the appropriate level of website and SEO deliverables based on the firm's current state, competitive landscape, and the marketing tier being recommended.

### Step 9A — Assess Current Website

Using audit findings from Pass 1, evaluate:

| Factor | Assessment | Implication |
|---|---|---|
| PageSpeed mobile score | Below 50 = rebuild needed | Directly impacts which tier is needed |
| Design age | Over 5 years = likely rebuild | Modern design is table stakes |
| Mobile responsiveness | Not responsive = rebuild mandatory | Google requirement |
| Practice area pages | Fewer than competitors = content gap | Determines content scope |
| Attorney bios | Missing or weak = priority fix | Trust signal |
| Blog/content | Stale or absent = content strategy needed | SEO factor |
| Trust signals | Missing awards, results, testimonials | Conversion factor |

### Step 9B — Assess Competitive Content Gap

During the digital presence audit, identify the top 2-3 local competitors. Evaluate:

1. **Number of practice area pages:** Count the firm's pages vs. top competitor's pages. The gap determines initial content needs.
2. **Total indexed pages:** Rough estimate of site size compared to competitors.
3. **Blog content velocity:** How often competitors publish vs. this firm.
4. **Domain Authority:** If available, note the gap.
5. **Review volume and velocity:** Reviews per month compared to competitors.

### Step 9C — Determine SEO Content Needs by Tier

Each marketing tier includes different content allocations. Map the firm's needs to the right tier:

| Tier | Initial Content at Launch | Annual Content After Launch | Content Import | GBP Locations | Backlinks/Year | Monthly Edits |
|---|---|---|---|---|---|---|
| Essentials | 5,000 words | 5,000 words (Year 2+) | Up to 10 pages | 1 | — | 30 min |
| Starter | 10,000 words | 6,000 words | Up to 250 pages | Up to 2 | — | 30 min |
| Growth | 15,000 words | 12,000 words | Up to 500 pages | Up to 4 | 4 premium | 60 min |
| Dominate | 20,000 words | 24,000 words | Up to 750 pages | Up to 6 | 8 premium | 90 min |
| Platinum | 30,000 words | 48,000 words | Up to 1,000 pages | Up to 8 | 16 premium | 240 min |

### Step 9D — Match Content Needs to Tier

**Factors that push toward higher content tiers:**
- Multiple practice areas (each needs dedicated pages): +1 tier if 4+ practice areas
- Multiple locations (each needs geo-targeted content): +1 tier if 3+ locations
- Significant competitor content gap (competitors have 2x+ more content): +1 tier
- AI readiness needs (FAQ content, structured data for AI answer engines): adds content volume requirements
- Weak or no existing content to import: need more initial content at launch

**If the content needs push the firm into a higher marketing tier than their revenue suggests:**
- Note this in the recommendation: "Based on your competitive landscape and [X] locations, we recommend the [Tier] level to ensure adequate content coverage."
- Alternatively, recommend the Web+SEO sub-package at the higher tier paired with an ads-only sub-package at the appropriate revenue tier.

### Step 9E — GBP Optimization Scope

| Number of Locations | GBP Scope |
|---|---|
| 1 | Standard optimization included in all tiers |
| 2 | Starter tier minimum (includes up to 2 locations) |
| 3-4 | Growth tier minimum (includes up to 4 locations) |
| 5-6 | Dominate tier minimum (includes up to 6 locations) |
| 7-8 | Platinum tier minimum (includes up to 8 locations) |
| 9+ | Custom scoping required |

### Step 9F — AI Readiness Assessment

Evaluate the firm's content for AI answer engine visibility (ChatGPT search, Google AI Overviews):
- Does the site have FAQ sections with clear, definitive answers?
- Are practice area pages structured with clear definitions and explanations?
- Is there content that directly answers common legal questions in the firm's practice areas?

If lacking, note this as a priority in the SEO content strategy. AI-optimized content should be included in the initial content allocation.

---

<a id="11-escalation"></a>
## 11. STEP 10 — CHECK ESCALATION FLAGS

After completing all calculations, check the recommendation against these escalation triggers. These are internal flags — they DO NOT appear in the client-facing audit. They are noted in the research notes file for the sales team.

### Flags Requiring Scoping Approval:

| Trigger | Action |
|---|---|
| Annual revenue under $300K | Flag: "Revenue under $300K — scoping approval required" |
| Recommended marketing MRR over $10K/month | Flag: "Marketing MRR exceeds $10K — scoping approval required" |
| Non-standard package combination | Flag: "Non-standard package combination — scoping approval required" |
| Multiple websites needed | Flag: "Multiple websites — scoping and custom agreement required" |
| Nationwide targeting | Flag: "Nationwide targeting — scoping and custom agreement required" |
| Monthly ad spend over $25K (all channels) | Flag: "Ad spend over $25K — scoping approval required" |

### Flags Requiring Additional Approval:

| Trigger | Action |
|---|---|
| Criminal Defense in a top 10 metro | Flag: "Criminal Defense in top 10 metro — approval required" |
| Family Law in a top 10 metro | Flag: "Family Law in top 10 metro — approval required" |
| Personal Injury in a top 40 metro | Flag: "Personal Injury in top 40 metro — approval required" |
| Upgrade increase of $5K+ in MRR | Flag: "Upgrade $5K+ MRR increase — approval required" |

### Flags Requiring Paid Ads Team Review:

| Trigger | Action |
|---|---|
| Ad spend below practice area minimums | Flag: "Ad spend below [practice area] minimum — paid ads team review" |
| Revenue goal exceeds projected ad-generated revenue | Flag: "Revenue goal exceeds projection — paid ads team review" |
| Any AI Virtual Video Growth package | Flag: "AI Video package — Alexis review required" |
| Ad spend under $3,000 with any paid ads component | Flag: "Ad spend under $3K — paid ads team review" |

---

<a id="12-edge-cases"></a>
## 12. STEP 11 — HANDLE MISSING DATA AND EDGE CASES

### Tiered Approach for Missing Data:

**Tier 1 — Infer from Context:**
If certain data points aren't explicitly stated but can be reasonably inferred from other information in the transcript, do so. Examples:
- Revenue not stated but firm mentions "5 attorneys and a paralegal" + PI practice area → likely $1M+ revenue
- Close rate not stated but firm says "we sign about 1 in 5 consultations" → 20% close rate
- Case value not stated but firm mentions "we handle car accident cases in Houston" → use PI default range

**Tier 2 — Use Conservative Defaults with Transparency:**
When inference isn't possible, use the defaults listed in Section 2's Required Data Points table and disclose it:
- "Based on industry benchmarks for [practice area] firms in your market, we're estimating a [X]% close rate. If your actual rate differs, your results will scale accordingly."
- "Using an average case value of $[X] for [practice area]. Your projected revenue will adjust based on your actual case values."

**Tier 3 — Flag for Follow-Up:**
If truly critical data is missing and cannot be estimated, flag it in the research notes:
- Practice area unknown → CANNOT proceed. Flag: "Practice area not identified — follow-up required before finalizing."
- Revenue completely unknown and no context clues → Flag: "Revenue not stated and cannot be inferred — follow-up required."

### Special Situations:

**Multi-Practice-Area Firms:**
- Use the MOST competitive (highest cost) practice area to determine ad spend minimums
- Calculate separate lead projections for each practice area if ad spend supports it
- Apply practice area hiding rules based on ALL practice areas (e.g., if they do PI + Family Law, PI rules apply to hide Essentials)

**Firms Under $250K Revenue:**
- Must verify client has funds to cover 4 months of services
- If the transcript shows they're consistently generating $15K+/month, they likely qualify
- Be conservative with ad spend recommendations — these firms have less margin for error
- Consider coaching-only (Elite Coach at $2,600) + LSA add-on ($900) as an entry point = $3,500/mo
- The goal is to get them to $400K+ so they qualify for Starter tier

**Firms Over $3M Revenue:**
- Default to Platinum marketing tier
- Master's Circle is the default coaching recommendation (if team qualifies)
- Consider FCOO Director or Partner level (not just Advisor)
- Bookkeeping is likely needed at this size

**Gateway Plan Situations:**
- If the firm has a website contract that doesn't expire for 5-12 months, recommend coaching only until 3 months before contract expiration
- Then transition to Full Service Marketing at the appropriate tier
- Note this timing in the growth roadmap phases

---

<a id="13-reference-tables"></a>
## 13. REFERENCE TABLES

### PPC Lead Projections — Non-PI Practice Areas

**Low Conversion Tier (10%):**

| Practice Area | CPC | $2,000 Spend | $5,000 Spend |
|---|---|---|---|
| Criminal | $30 | 7 leads | 17 leads |
| Disability | $10.65 | 19 leads | 47 leads |
| Estate Planning | $19.45 | 10 leads | 26 leads |
| Family | $10 | 20 leads | 50 leads |
| Immigration | $6.72 | 30 leads | 74 leads |

**Mid Conversion Tier (15%):**

| Practice Area | CPC | $3,000 Spend | $6,500 Spend |
|---|---|---|---|
| Criminal | $39.95 | 11 leads | 24 leads |
| Disability | $10.65 | 42 leads | 92 leads |
| Estate Planning | $19.45 | 23 leads | 50 leads |
| Family | $17.83 | 25 leads | 55 leads |
| Immigration | $6.72 | 67 leads | 145 leads |

**High Conversion Tier (20%):**

| Practice Area | CPC | $3,500 Spend | $10,000 Spend |
|---|---|---|---|
| Criminal | $45 | 16 leads | 44 leads |
| Disability | $10.65 | 66 leads | 188 leads |
| Estate Planning | $19.45 | 36 leads | 103 leads |
| Family | $17.83 | 39 leads | 112 leads |
| Immigration | $15 | 47 leads | 133 leads |

### PPC Lead Projections — Personal Injury by Market Size

**Small Market PI:**

| Niche | CPC | $10,000 Spend | $20,000 Spend | $50,000 Spend |
|---|---|---|---|---|
| Accident/Injury General | $100 | 11 leads | 22 leads | 55 leads |
| Car Accidents | $94.76 | 12 leads | 23 leads | 58 leads |
| Motorcycle Accidents | $150 | 7 leads | 13 leads | 33 leads |
| Truck Accidents | $150 | 7 leads | 13 leads | 33 leads |
| Slip & Fall | $100 | 10 leads | 20 leads | 50 leads |
| Wrongful Death | $100 | 10 leads | 20 leads | 50 leads |

**Mid Market PI:**

| Niche | CPC | $8,000 Spend | $20,000 Spend | $30,000 Spend |
|---|---|---|---|---|
| Accident/Injury General | $150 | 8 leads | 20 leads | 30 leads |
| Car Accidents | $200 | 4 leads | 11 leads | 17 leads |
| Motorcycle Accidents | $200 | 4 leads | 11 leads | 17 leads |
| Truck Accidents | $200 | 4 leads | 11 leads | 17 leads |
| Slip & Fall | $150 | 8 leads | 20 leads | 30 leads |
| Wrongful Death | $150 | 8 leads | 20 leads | 30 leads |

**Large Market PI:**

| Niche | CPC | $10,000 Spend | $20,000 Spend | $50,000 Spend |
|---|---|---|---|---|
| Accident/Injury General | $300 | 5 leads | 10 leads | 25 leads |
| Car Accidents | $325 | 5 leads | 9 leads | 23 leads |
| Motorcycle Accidents | $250 | 8 leads | 16 leads | 40 leads |
| Truck Accidents | $250 | 8 leads | 16 leads | 40 leads |
| Slip & Fall | $200 | 10 leads | 20 leads | 50 leads |
| Wrongful Death | $200 | 10 leads | 20 leads | 50 leads |

### Meta Lead Gen Projections — By Geography Size

**Small Geography:**

| Practice Area | CPL | $1,200 Spend | $3,000 Spend | $5,000 Spend |
|---|---|---|---|---|
| Personal Injury | $175 | 7 leads | 17 leads | 29 leads |
| Family Law | $60 | 20 leads | 50 leads | 83 leads |
| Criminal Defense | $100 | 12 leads | 30 leads | 50 leads |
| Business Law | $100 | 12 leads | 30 leads | 50 leads |
| Immigration | $50 | 24 leads | 60 leads | 100 leads |
| Estate Planning | $60 | 20 leads | 50 leads | 83 leads |

**Mid Geography:**

| Practice Area | CPL | $1,500 Spend | $3,000 Spend | $6,300 Spend |
|---|---|---|---|---|
| Personal Injury | $200 | 8 leads | 15 leads | 32 leads |
| Family Law | $75 | 20 leads | 40 leads | 84 leads |
| Criminal Defense | $150 | 10 leads | 20 leads | 42 leads |
| Business Law | $100 | 15 leads | 30 leads | 63 leads |
| Immigration | $50 | 30 leads | 60 leads | 126 leads |
| Estate Planning | $75 | 20 leads | 40 leads | 84 leads |

**Large Geography:**

| Practice Area | CPL | $1,500 Spend | $2,400 Spend | $3,000 Spend |
|---|---|---|---|---|
| Personal Injury | $300 | 5 leads | 8 leads | 10 leads |
| Family Law | $100 | 15 leads | 24 leads | 30 leads |
| Criminal Defense | $200 | 8 leads | 12 leads | 15 leads |
| Business Law | $150 | 10 leads | 16 leads | 20 leads |
| Immigration | $50 | 30 leads | 48 leads | 60 leads |
| Estate Planning | $75 | 20 leads | 32 leads | 40 leads |

**PI-Specific Large Market Note:** For firms in Atlanta, Houston, Dallas, Los Angeles, Denver, or New York — use $300 average CPL for Meta.

### YouTube / PMax Estimates (Awareness, not lead gen):

| Monthly Spend | CPM Range | Estimated Impressions |
|---|---|---|
| $500 | $7–$10 | 50,000–71,000 |
| $1,500 | $7–$10 | 150,000–214,000 |
| $2,500 | $7–$10 | 250,000–357,000 |
| $5,000 | $7–$10 | 500,000–714,000 |

### Meta Benchmarks — Internal vs. Client-Facing (for reference only):

**Lead Gen:**

| Practice Area | Client-Facing CPL | Internal Avg CPL | Average Ad Spend |
|---|---|---|---|
| Personal Injury | $200–$300 | $107 | $6,144 |
| Family Law | $75–$125 | $58 | $3,084 |
| Criminal Defense | $100–$200 | $108 | $2,732 |
| General Law | $75–$150 | $96 | $3,918 |
| Immigration | $40–$80 | $67 | $2,770 |
| Estate Planning | $75–$125 | $26 | $4,228 |

**Retargeting:**

| Practice Area | Client-Facing CPL | Internal Avg CPL |
|---|---|---|
| Personal Injury | $200–$300 | $97 |
| Family Law | $75–$150 | $33 |
| Criminal Defense | $75–$150 | $53 |
| General Law | $50–$100 | $50 |
| Immigration | $25–$75 | $56 |
| Estate Planning | $50–$100 | $50 |

**IMPORTANT:** Always use client-facing ranges in audit presentations. Internal averages are for validation only — they confirm that the client-facing ranges are conservative and achievable.

---

## END OF SCOPING GUIDE

This guide is referenced by the SMB Team Audit Agent System Prompt during Part Three — Package Recommendation Logic. All calculations and recommendations produced by this guide feed into the section files as specified in Part Four of the system prompt.
