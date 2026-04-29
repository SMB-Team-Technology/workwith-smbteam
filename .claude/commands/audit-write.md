# SMB Team — Audit Write (Pass 2)

Fill in all section templates, assemble the final HTML report, generate the Sales Companion PDF, and push to GitHub. Run this after `/audit-research` completes.

## How to invoke

```
/audit-write
Firm Name: [Full legal name of the firm]
Friendly Name: [same value used in /audit-research, e.g. angel-law]
Sales Rep: [rep's full name]
Date: [same date used in /audit-research — Month DD, YYYY]
```

---

## BEFORE STARTING

Read these two files:
1. `[friendly-name]/[FirmName]_[Date]_Research_Notes.txt` — all data comes from here. Trust it.
2. `Design Files/audit_styles.css` — scan class names so you never invent one.

If the research notes file does not exist, stop and tell the user to run `/audit-research` first.

Create `[friendly-name]/sections/` if it does not exist.

**Transcript-first principle:** The research notes contain data extracted from the transcript. Those values are ground truth. Never search for data that's already in the notes.

---

## CRITICAL RULES — NEVER BREAK THESE

- **NO CSS.** No `<style>` blocks. No inline styles. No `style=""` attributes. Ever.
- Only use class names that already exist in `audit_styles.css`. Never invent new ones.
- Replace only `<!-- FILL: -->` placeholder content — do not touch anything else in any template.
- Direct transcript quotes go in quote boxes only — never paraphrase into a quote box.
- Never say "you are not running ads" — only "does not appear to be running" or "not observed."
- Omit "Who Is Doing It Better" row on any quick win card where no specific named local competitor was identified.
- Omit "The Positive" block in any pillar section where nothing genuine can be said.
- Never mention live chat as an SMB Team service.
- Never mention CRM setup as a first 90 days deliverable.
- Never state profitability facts by practice area unless the prospect explicitly said so on the call.
- Escalation flags are internal only — never appear in the client report.

---

## FIRM STAGE — STAIRCASE IMAGE

Determine stage from the transcript. Assign the lower stage if on the border. In `section_03_firm_overview.html`, uncomment the correct image and delete the others.

- **Stage 2 — The Lawyer:** Employed at another firm, no independent client base. → `LLS-Lawyer`
- **Stage 3 — Solo Practitioner:** Referrals only, handles casework and intake personally, very small or no team, profit unpredictable. → `LLS-Solo-Practitioner`
- **Stage 4 — Small Business Manager:** Has at least one scalable lead gen system, small team, still heavily involved in operations. → `LLS-Small-Business-Manager`
- **Stage 5 — Law Firm CEO:** Multiple lead gen systems, trained intake team, leadership structure, can take time off. → `LLS-Law-Firm-CEO`
- **Stage 6 — Law Firm Owner:** Firm runs without owner, CEO/COO in place, omnipresent marketing, profit predictable. → `LLS-Law-Firm-Owner`

---

## TRAFFIC LIGHT CRITERIA

Assign red / amber / green for each pillar based on the transcript:

**Lead Generation** — Red: referrals only, no system, inconsistent flow. Amber: some paid ads or SEO, inconsistent results. Green: multiple reliable systems running.

**Intake** — Red: attorney personally handles intake, no process, slow follow-up. Amber: some delegation but gaps, no after-hours coverage. Green: trained team, defined process, fast follow-up.

**Team** — Red: owner cannot step away, no accountability, no org structure. Amber: small team but owner manages everything closely. Green: managers exist, team runs without constant owner involvement. Never reference "Stage 6" — describe specifically what a self-managing firm looks like.

**Profit** — Red: no financial visibility, expenses out of control. Amber: revenue growing but margins unclear. Green: knows numbers, profit planned not discovered.

---

## DOMINANT BUYING MOTIVE (DBM)

The DBM is the personal reason behind growth — what success will allow the owner to do. Not "more money" — what the money enables. Use exact transcript words if available. If not stated, infer: most owners want (1) a firm that runs itself so they have time, (2) grow and sell, or (3) scale and dominate. Anchor every section to the DBM.

---

## SECTIONS — WORK THROUGH IN ORDER

Complete and save each section before starting the next. The FILL: comments in each template specify exactly what content goes where. The notes below add rules beyond the templates.

**STEP A — section_01_cover.html**
Fill: firm name (twice), sales rep name, audit date. Save to `[friendly-name]/sections/section_01_cover.html`.

**STEP B — section_02_toc.html**
Fill: firm name wherever FIRM NAME HERE appears in link text. Do not change any href values. Save to `[friendly-name]/sections/section_02_toc.html`.

**STEP C — section_03_firm_overview.html**
Fill: firm name, firm summary (2–3 sentences: who they are, current stage, single most important finding — no generic language), correct staircase image, DBM connector sentence, current stage label, four current reality bullets specific to this firm, connecting sentence, overall growth stage assessment (2–3 sentences: stage description, most urgent limiting area, gap between goals and reality). Save to `[friendly-name]/sections/section_03_firm_overview.html`.

**STEP D — section_04_about_smb.html**
Static file. Copy as-is to `[friendly-name]/sections/section_04_about_smb.html`. No changes.

**STEP E — section_05_growth_health.html**
Fill: firm name, all four traffic light colors and labels, all four pillar findings (2–3 specific bullets each), all four DBM connector sentences (italic), urgency score (1–10), urgency marker left percentage (score ÷ 10 × 100), urgency sentence from the correct range, 2–3 named local competitor threat cards.

Urgency sentences:
- **1–3:** "A score of [X] means no single competitor is dominating your market yet — but that will not last forever. The firms that win markets do so by moving first. Getting your systems in place now means you set the standard before someone else does."
- **4–6:** "A score of [X] means competitors have meaningful advantages in one or more areas and are pulling ahead. You are not invisible yet — but the window to close the gap is narrowing. Every month without action is a month they extend their lead."
- **7–10:** "A score of [X] means competitors are actively dominating multiple channels in your market and the gap is getting wider every month you wait. This is not a future problem — it is a right now problem."

Save to `[friendly-name]/sections/section_05_growth_health.html`.

**STEP F — section_06_lead_generation.html**
Fill: lead gen intro (2 sentences, specific to this firm), website section with actual PageSpeed scores (real numbers only — from research notes), local SEO section with GBP data and local pack results per practice area with actual competitor review counts, Google Ads section covering ALL practice areas, LSA section, Meta Ads section. Delete any blind spot divs that do not apply. Save to `[friendly-name]/sections/section_06_lead_generation.html`.

**STEP G — section_07_08_09_intake_team_profit.html**
Fill all three sections in order — Intake, Team, Profit. For each: intro sentence, traffic light, transcript quote (or delete if none), problem bullets, blind spot (or delete), positives (or delete if nothing genuine), gap bullets, DBM closing. End Intake with: "Fixing intake means converting more of the leads the firm is already generating — without spending another dollar on marketing." End Team with: "Until this changes, the owner cannot have more free time — no matter how much revenue grows." Save to `[friendly-name]/sections/section_07_08_09_intake_team_profit.html`.

**STEP H — section_10_whats_possible.html**
Fill: firm name (twice), bridge text connecting current reality to transformation, three transformation cards tied specifically to this owner's DBM. Save to `[friendly-name]/sections/section_10_whats_possible.html`.

**STEP I — section_11_next_steps.html**

This section is large and must be completed in three sub-steps to avoid API timeouts. Complete and save after each sub-step before continuing.

Apply all package eligibility and calculation logic (below) BEFORE starting Step I-a.

**STEP I-a — Write workings file**
Compute and save `[friendly-name]/sections/section_11_workings.txt` containing:
- Selected marketing package name, bundled price, stand-alone price, savings
- Selected non-marketing package(s) name, bundled price, stand-alone price, savings
- Total monthly investment (sum of bundled prices)
- Total savings (sum of all stand-alone minus bundled)
- Conservative ad spend amount and full ROI projection (leads, cases, revenue, return multiple)
- Aggressive ad spend amount and full ROI projection (leads, cases, revenue, return multiple)
- DBM statement for Block 1
- List of 6+ quick win opportunities identified (pillar, title, why, competitor if any, opportunity)
- First 90 days bullet points (3–5)

Save the workings file. Do not proceed until it is saved.

**STEP I-b — Write section 11 first half**
Fill and save `[friendly-name]/sections/section_11_next_steps.html` with the complete file structure. In this sub-step, fill ONLY:
- Firm name (all three occurrences)
- All quick win cards (minimum 6 across all four pillars). Delete the "Who Is Doing It Better" row on any card where no named competitor was identified.
- Block 1: custom closing statement (formula: "We help [audience] get [external desire] so they can [DBM].")
- Block 2: DBM subheader + package block(s) with deliverables. Each package block must include a package-label div identifying the package type.
- Block 3: investment rows with retail (stand-alone) and bundled prices pulled from your workings file. Total monthly investment row. Savings callout. Use ONLY the prices from the approved tables — never deviate.
- Block 4: recommended ad spend table. **DO NOT change the HTML structure.** Only replace the placeholder dollar amounts, case counts, and return multiples. Structure: ad spend range row → case value row → spacer → "Conservative scenario" header + 3 rows (cases, revenue, return) → spacer → "Aggressive scenario" header + 3 rows → disclaimer.

Leave blocks 5–8 with their original template placeholder text for now. Save the file.

**STEP I-c — Complete section 11 second half**
Edit `[friendly-name]/sections/section_11_next_steps.html` to fill in blocks 5–8:
- Block 5: first 90 days action bullets. Lead with launching ads first, then website work. Include coaching kickoff. Never mention live chat. Never mention CRM setup.
- Block 6: three phase roadmap cards with dynamic milestone triggers and DBM sentences.
- Block 7: three outcome cards (More Profit, More Freedom, Better Client Results), each tied to this owner's DBM.
- Block 8: personal closing paragraph (2–3 italic sentences) + final line with firm name.

Save (edit) the file. Verify no FILL: placeholders remain.

---

## PRICE INTEGRITY — CRITICAL

The prices in the tables below are the ONLY approved prices. Do not estimate, round, interpolate, or use any number not listed here. Every dollar figure in the client report must come from one of the two pricing tables below. The example numbers in HTML template comments are illustrative only — do not use them as actual prices.

---

## PACKAGE ELIGIBILITY AND CALCULATIONS

Complete this entire section before starting Step I.

### ELIMINATED PRODUCTS — never recommend under any circumstances
- Coach Essentials (eliminated)
- Coach Essentials Plus (eliminated)

### ELIGIBILITY FILTERS — apply first, hide anything that fails

**Practice Area:**
- Personal Injury → hide ALL Essentials marketing packages AND the LSA-only add-on. Minimum tier is Starter.
- Criminal Defense + High competitiveness → hide ALL Essentials marketing packages. LSA-only still allowed.

**Revenue:**
- Under $250K → confirm client has funds to cover 4 months of services before proceeding.
- Under $500K → hide all Fractional CFO and Fractional COO products and all bundles containing them.
- Under $1M → hide Master's Circle and all bundles. Hide Dominate and Platinum marketing tiers.
- Over $1M → hide all Essentials marketing products.

**Team:**
- Fewer than 5 team members → hide all Master's Circle options.
- No dedicated ops, marketing, or intake team member → hide all Master's Circle options.

**General:**
- Minimum MRR: $3,497/month — never recommend below this.
- Always include at least one marketing package and one non-marketing package.
- Total SMB spend (management fees + ad spend) must not exceed 35% of monthly revenue.

---

### SELECT MARKETING PACKAGE

Default to Full Service Marketing at the appropriate tier unless there is a specific reason to use a sub-package. Sub-packages (ads-only, web+SEO only) must be paired with a coaching package.

**Marketing Tiers — Full Service Bundled Prices:**

| Revenue | Tier | Bundled Price | Ad Spend Cap |
|---|---|---|---|
| $250K–$400K | Essentials | $3,397/mo | $7,500 |
| $400K–$1M | Starter | $4,847/mo | $25,000 |
| $1M–$3M | Growth | $7,397/mo | $50,000 |
| $1M+ aggressive goals | Dominate | $10,497/mo | $75,000 |
| $3M+ | Platinum | $15,997/mo | $150,000 |

**Stand-alone prices (for savings calculation in Block 3):**
Essentials $N/A | Starter $5,697 | Growth $8,997 | Dominate $12,497 | Platinum $18,997

**Boundary rule:** If the firm's goals are aggressive or their calculated ad spend exceeds the lower tier's cap, move to the higher tier.

**Website rebuild needed if:** PageSpeed mobile below 50, design 5+ years old, not mobile responsive, no practice area pages, no attorney bios. If rebuild needed, must use Full Service (not ads-only).

---

### SELECT NON-MARKETING PACKAGE

Every recommendation must include at least one non-marketing package.

| Revenue | Team | Recommended | Bundled Price |
|---|---|---|---|
| $250K–$400K | Any | Elite Coach | $2,600/mo |
| $400K–$1M | Any | Elite Coach Plus | $3,200/mo |
| $400K–$1M | Growing | Elite Coach Plus + FCOO Advisor | $5,694/mo |
| $1M+ | Under 5 | Elite Coach Plus | $3,200/mo |
| $1M+ | Under 5 operational focus | FCOO Advisor | $3,297/mo |
| $1M+ | 5+ with dedicated staff | Master's Circle | $4,600/mo |
| $1M+ | 5+ with dedicated staff + ops | Master's Circle + FCOO Advisor | $6,694/mo |
| $2M+ | 5+ with dedicated staff | Master's Circle + FCOO Director | $8,394/mo |
| $3M+ | Large team | Master's Circle + FCOO Partner | $12,394/mo |

**Add Fractional CFO Advisor ($3,297/mo bundled)** if: owner mentions profit problems, revenue growing but not taking home more, no financial visibility, doesn't know acquisition cost. Min revenue $400K.

**Stand-alone prices:** Elite Coach $3,497 | Elite Coach Plus $3,497 | Master's Circle $4,997 | FCOO Advisor $3,797 | FCOO Director $5,797 | FCFO Advisor $3,797

---

### AD SPEND CALCULATION — CONSERVATIVE AND AGGRESSIVE

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

---

### ROI PROJECTIONS (Block 4)

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

### ESCALATION FLAGS (internal — never appear in client report)

Note these in the research notes file for the sales team. Do not include in the audit:
- Revenue under $300K → scoping approval required
- Marketing MRR over $10K → scoping approval required
- Ad spend over $25K → scoping approval required
- Criminal Defense in top 10 metro → approval required
- Family Law in top 10 metro → approval required
- Personal Injury in top 40 metro → approval required
- Ad spend below practice area minimums → paid ads team review
- Revenue goal exceeds projected ad revenue → paid ads team review
- Any AI Virtual Video Growth package → Alexis approval required

---

### GROWTH ROADMAP PHASES

- **Phase 1 — Foundation:** Marketing + Coaching. Connect to DBM.
- **Phase 2 — Operational Scale:** Add FCOO Advisor ($3,297/mo). Frame as graduation. Connect to DBM.
- **Phase 3 — Optimize:** Add FCFO Advisor ($3,297/mo). Add Bookkeeping if needed. Connect to DBM.
- **Phase 4 — Market Domination:** Upgrade marketing tier.
- **Phase 5 — Full SMB Ecosystem:** All services. Closing line: "The firms that have the freedom you described all ended up here. And it started exactly where we are starting you."

---

## ASSEMBLY — PYTHON SCRIPT

After all 9 sections are saved, run:

```bash
pip install reportlab pypdf --break-system-packages --quiet
```

Then assemble the audit HTML via Python (avoids loading all sections back into context):

```bash
python3 - << 'PYEOF'
import os

firm_folder = "REPLACE_WITH_FRIENDLY_NAME"

with open("Design Files/audit_master_assembly.html", "r") as f:
    html = f.read()

sections = [
    ("<!-- INSERT SECTION 01 CONTENT HERE -->", "section_01_cover.html"),
    ("<!-- INSERT SECTION 02 CONTENT HERE -->", "section_02_toc.html"),
    ("<!-- INSERT SECTION 03 CONTENT HERE -->", "section_03_firm_overview.html"),
    ("<!-- INSERT SECTION 04 CONTENT HERE -->", "section_04_about_smb.html"),
    ("<!-- INSERT SECTION 05 CONTENT HERE -->", "section_05_growth_health.html"),
    ("<!-- INSERT SECTION 06 CONTENT HERE -->", "section_06_lead_generation.html"),
    ("<!-- INSERT SECTION 07-09 CONTENT HERE -->", "section_07_08_09_intake_team_profit.html"),
    ("<!-- INSERT SECTION 10 CONTENT HERE -->", "section_10_whats_possible.html"),
    ("<!-- INSERT SECTION 11 CONTENT HERE -->", "section_11_next_steps.html"),
]

for marker, fname in sections:
    path = os.path.join(firm_folder, "sections", fname)
    with open(path, "r") as f:
        content = f.read()
    if marker not in html:
        print(f"WARNING: marker not found: {marker}")
    html = html.replace(marker, content)

out = os.path.join(firm_folder, "index.html")
with open(out, "w") as f:
    f.write(html)
print(f"Assembled: {out} ({len(html):,} chars)")
PYEOF
```

Then copy CSS:
```bash
cp "Design Files/audit_styles.css" "[friendly-name]/audit_styles.css"
```

---

## STEP K — SALES COMPANION PDF

After the HTML audit is assembled, generate the internal Sales Companion PDF for the sales rep. This document is never shared with the client.

1. Read `Design Files/sales_companion_template.py` completely.
2. Copy it to `[friendly-name]/[FirmName]_[Date]_Sales_Companion.py`.
3. Fill in every `# FILL:` placeholder with audit-specific content. Content comes from the research notes and transcript — no new research needed.
4. Update the `OUTPUT_PATH` variable to: `"[friendly-name]/[FirmName]_[Date]_Sales_Companion.pdf"`
5. Ad spend section: use the conservative and aggressive amounts calculated above.
6. ROI section: use the projection numbers from Block 4.
7. Objections: anticipate 2–4 objections based on the transcript. Respond with specific data from the audit.

Run the filled script:
```bash
python3 "[friendly-name]/[FirmName]_[Date]_Sales_Companion.py"
```

Verify the output confirms exactly 2 pages. If it prints a WARNING about page count, shorten bullet text (never remove sections) and re-run.

**Writing rules for the Sales Companion:**
- Every bullet: one idea, one sentence, 8th-grade reading level, scannable.
- Transformation bullets use `bd()` (dark). Scoping and obstacle bullets use `b()` (gray).
- Objection responses must reference specific data — competitor review counts, revenue figures, transcript quotes.
- All ROI projections labeled as estimates.

---

## FINAL CHECK

Run bash grep — do not read `index.html` directly:

```bash
grep -c "FILL:" "[friendly-name]/index.html" || true
grep -cE '<style|style="' "[friendly-name]/index.html" || true
grep -c 'href="audit_styles.css"' "[friendly-name]/index.html" || true
wc -c "[friendly-name]/audit_styles.css"
wc -l "[friendly-name]/index.html"
```

If placeholder count > 0 or style count > 0, read only the specific flagged lines:
```bash
grep -n "FILL:" "[friendly-name]/index.html"
grep -nE '<style|style="' "[friendly-name]/index.html"
```

Fix any issues found, then commit.

---

## COMMIT AND PUSH TO MAIN

```bash
git checkout main
git add "[friendly-name]/"
git commit -m "Add growth audit: [Firm Name] ([Date])"
GIT_TERMINAL_PROMPT=0 git push origin main
git log -1 --format="%H %s"
```

Always commit directly to main — never create a branch. Report the commit hash. Done.
