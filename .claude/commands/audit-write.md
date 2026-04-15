# SMB Team — Audit Write (Pass 2)

Fill in all section templates, assemble the final HTML report via Python, and push to GitHub. Run this after `/audit-research` completes.

## How to invoke

```
/audit-write
Firm Name: [Full legal name of the firm]
Friendly Name: [same value used in /audit-research, e.g. angel-law]
Sales Rep: [rep's full name]
Date: [same date used in /audit-research — Month DD, YYYY]
Package Criteria: [optional — include if ready to complete the recommendation section]
```

---

## BEFORE STARTING

Read these two files:
1. `[friendly-name]/[FirmName]_[Date]_Research_Notes.txt` — all data comes from here only
2. `Design Files/audit_styles.css` — scan class names so you never invent one

If the research notes file does not exist, stop and tell the user to run `/audit-research` first.

Create `[friendly-name]/sections/` if it does not exist.

---

## CRITICAL RULES — NEVER BREAK THESE

- **NO CSS.** No `<style>` blocks. No inline styles. No `style=""` attributes. Ever. All styling from `audit_styles.css` only.
- Only use class names that already exist in `audit_styles.css`. Never invent new ones.
- Replace only `<!-- FILL: -->` placeholder content — do not touch anything else in any template.
- Direct transcript quotes go in quote boxes only — never paraphrase into a quote box.
- Never say "you are not running ads" — only "does not appear to be running" or "not observed."
- Omit "Who Is Doing It Better" row on any quick win card where no specific named local competitor was identified.
- Omit "The Positive" block in any pillar section where nothing genuine can be said.
- Never mention live chat as an SMB Team service.
- Never mention CRM setup as a first 90 days deliverable.
- Never state profitability facts by practice area unless the prospect explicitly said so on the call.
- Escalation flags from package logic are internal only — never appear in the client report.

---

## FIRM STAGE — STAIRCASE IMAGE

Determine the stage from the transcript. Assign the lower stage if on the border. In `section_03_firm_overview.html`, uncomment the correct image and delete the others.

- **Stage 2 — The Lawyer:** Still employed at another firm, no independent client base. Image: `LLS-Lawyer`
- **Stage 3 — Solo Practitioner:** Referrals only, handles most casework and intake personally, very small or no team, profit unpredictable, cannot step away. Image: `LLS-Solo-Practitioner`
- **Stage 4 — Small Business Manager:** Has at least one scalable lead gen system, small team, still heavily involved in casework, reactive profit management. Image: `LLS-Small-Business-Manager`
- **Stage 5 — Law Firm CEO:** Multiple lead gen systems, trained intake team, leadership structure, working by choice on cases, can take time off. Image: `LLS-Law-Firm-CEO`
- **Stage 6 — Law Firm Owner:** Firm runs without owner involvement, CEO/COO in place, omnipresent marketing, profit predictable. Image: `LLS-Law-Firm-Owner`

---

## TRAFFIC LIGHT CRITERIA

Assign red / amber / green for each of the four pillars based on the transcript:

**Lead Generation** — Red: referrals only, no system, inconsistent flow. Amber: some paid ads or SEO, inconsistent results. Green: multiple reliable systems running.

**Intake** — Red: attorney personally handles intake, no process, slow follow-up. Amber: some delegation but gaps, no after-hours coverage. Green: trained team, defined process, fast follow-up.

**Team** — Red: owner cannot step away, no accountability, no org structure. Amber: small team but owner manages everything closely. Green: managers exist, team runs without constant owner involvement.

**Profit** — Red: no financial visibility, expenses out of control, no acquisition cost awareness. Amber: revenue growing but margins unclear. Green: knows numbers, profit planned not discovered.

---

## DOMINANT BUYING MOTIVE (DBM)

The DBM is the personal reason behind growth — what success will allow the owner to do. Not "more money" — what the money enables. Use exact words from the transcript if available. If not clearly stated, infer: most owners want (1) a firm that runs itself so they have time, (2) grow and sell, or (3) scale and dominate. Every section must connect back to the DBM.

---

## SECTIONS — WORK THROUGH IN ORDER

Complete and save each section before starting the next. Read the FILL: comments in each template — they specify exactly what content goes where. The instructions below add rules beyond what the templates say.

**STEP A — section_01_cover.html**
Fill: firm name (twice), sales rep name, audit date. Save to `[friendly-name]/sections/section_01_cover.html`.

**STEP B — section_02_toc.html**
Fill: firm name wherever FIRM NAME HERE appears in link text. Do not change any href values. Save to `[friendly-name]/sections/section_02_toc.html`.

**STEP C — section_03_firm_overview.html**
Fill: firm name, firm summary (2–3 sentences: who they are, what they do, current stage, single most important finding — no generic language), correct staircase image, DBM connector sentence, current stage label, four current reality bullets specific to this firm, connecting sentence, overall growth stage assessment (2–3 sentences: stage description, most urgent limiting area, gap between goals and reality). Save to `[friendly-name]/sections/section_03_firm_overview.html`.

**STEP D — section_04_about_smb.html**
Static file. Copy as-is to `[friendly-name]/sections/section_04_about_smb.html`. No changes.

**STEP E — section_05_growth_health.html**
Fill: firm name, all four traffic light colors and labels, all four pillar findings (2–3 specific bullets each), all four DBM connector sentences (italic), urgency score (1–10), urgency marker left percentage (score ÷ 10 × 100, e.g. score 7 = 70%), urgency sentence from the matching range, 2–3 named local competitor threat cards. Save to `[friendly-name]/sections/section_05_growth_health.html`.

Urgency sentences:
- **1–3:** "A score of [X] means no single competitor is dominating your market yet — but that will not last forever. The firms that win markets do so by moving first. Getting your systems in place now means you set the standard before someone else does."
- **4–6:** "A score of [X] means competitors have meaningful advantages in one or more areas and are pulling ahead. You are not invisible yet — but the window to close the gap is narrowing. Every month without action is a month they extend their lead."
- **7–10:** "A score of [X] means competitors are actively dominating multiple channels in your market and the gap is getting wider every month you wait. This is not a future problem — it is a right now problem."

**STEP F — section_06_lead_generation.html**
Fill: lead gen intro (2 sentences, specific to this firm), website section with actual PageSpeed scores (real numbers only), local SEO section with GBP data and local pack results per practice area with actual competitor review counts, Google Ads section covering ALL practice areas (never skip a practice area), LSA section, Meta Ads section. Delete any blind spot divs that do not apply. Save to `[friendly-name]/sections/section_06_lead_generation.html`.

**STEP G — section_07_08_09_intake_team_profit.html**
Fill all three sections in order — Intake, Team, Profit. For each: intro sentence, traffic light, transcript quote (or delete if none), problem bullets, blind spot (or delete), positives (or delete if nothing genuine), gap bullets, DBM closing. End Intake with: "Fixing intake means converting more of the leads the firm is already generating — without spending another dollar on marketing." End Team with: "Until this changes, the owner cannot have more free time — no matter how much revenue grows." Never reference "Stage 6" in Team — describe specifically what a self-managing firm looks like. Save to `[friendly-name]/sections/section_07_08_09_intake_team_profit.html`.

**STEP H — section_10_whats_possible.html**
Fill: firm name (twice), bridge text connecting current reality to transformation, three transformation cards tied specifically to this owner's DBM. Save to `[friendly-name]/sections/section_10_whats_possible.html`.

**STEP I — section_11_next_steps.html**
Apply package eligibility rules below before filling anything. Fill: firm name (three times), minimum 6 quick win cards across all four pillars, then all 8 recommendation blocks:
- Block 1: custom closing using DBM formula — "We help [specific description] get [external desire] so they can [DBM]."
- Block 2: DBM subheader + package blocks with deliverables. Each package block must include a package-label above the name (e.g. "Recommended Marketing Package").
- Block 3: investment rows with retail and bundled prices. Savings = sum of ALL packages' (retail minus bundled). Show total bundled investment.
- Block 4: ad spend amount, estimated case value, estimated cases, estimated revenue — all labeled as estimates. Include the disclaimer sentence.
- Block 5: first 90 days bullets. Lead with launching ads first, then website work. Include coaching kickoff. Never mention live chat. Never mention CRM setup.
- Block 6: three phase cards with dynamic milestone triggers and DBM sentences.
- Block 7: three outcome cards (More Profit, More Freedom, Better Client Results) tied to DBM.
- Block 8: personal closing paragraph and final line with firm name.

**If Package Criteria was not provided:** insert a clearly marked navy placeholder in place of blocks 2–8 stating this section will be completed by the sales rep prior to delivery.

Save to `[friendly-name]/sections/section_11_next_steps.html`.

---

## PACKAGE ELIGIBILITY LOGIC

Apply these rules before recommending anything. Hidden packages must not appear anywhere in the report.

**Practice Area Rules:**
- Personal Injury → hide all Essentials marketing packages and the LSA-only add-on
- Criminal Defense + High competitiveness market → hide all Essentials marketing packages (LSA-only still allowed)

**Revenue Rules:**
- Under $250K → confirm client has funds for 4 months of services before proceeding
- Over $250K → hide Coach Essentials
- Under $500K → hide all Fractional CFO, Fractional COO products, and all bundles containing them
- Under $1M → hide Master's Circle and all bundles containing it; hide Dominate and Platinum marketing tiers
- Over $1M → hide Coach Essentials Plus and all Essentials marketing products

**Team Rules:**
- Fewer than 5 team members → hide all Master's Circle options
- No dedicated ops/marketing/intake team member → hide all Master's Circle options

**General Rules:**
- Minimum MRR: $3,497/month — never recommend below this
- Always include at least one marketing package and one non-marketing package
- Total SMB spend (management fees + ad spend) should not exceed 35% of monthly revenue

**Select Marketing Package:**
- $250K–$400K: Essentials Full Service Marketing ($1,497–$3,397/month) — unless hidden by practice area rules
- $400K–$1M: Full Service Marketing Starter ($4,847/month)
- $1M–$3M: Full Service Marketing Growth ($7,397/month)
- $1M+ aggressive growth: Full Service Marketing Dominate ($10,897/month)
- $3M+: Full Service Marketing Platinum ($18,397/month)

**Select Non-Marketing Package:**
- $250K–$1M: Elite Coach ($2,600/month) or Elite Coach Plus ($3,200/month)
- $1M+ operational complexity: Fractional COO Advisor ($3,297/month) bundled with Elite Coach or Master's Circle
- $1M+ financial challenges: Fractional CFO Advisor ($3,297/month)
- $1M+, 5+ team members, dedicated staff: Master's Circle ($4,600/month)

**Ad Spend:**
- Minimum: $3,000/month for any package that includes paid ads
- $250K–$500K firms: $3,000–$5,000/month
- $500K–$1M firms: $5,000–$10,000/month
- $1M+ firms: $10,000–$25,000/month
- Practice area minimums: PI + Low competitiveness $5,500 / PI + Medium $7,500 / PI + High $10,000 / Criminal Defense + High $5,000

**Growth Roadmap Phases:**
- Phase 1 — Foundation: Marketing + Coaching (connect to DBM)
- Phase 2 — Operational Scale: Add Fractional COO Advisor ($3,297/month) — frame as graduation
- Phase 3 — Optimize: Add Fractional CFO Advisor ($3,297/month)
- Phase 4 — Market Domination: Upgrade marketing tier
- Phase 5 — Full SMB Ecosystem: All services. Closing line: "The firms that have the freedom you described all ended up here. And it started exactly where we are starting you."

---

## ASSEMBLY — PYTHON SCRIPT

After all 9 sections are saved, assemble using Python. This avoids loading all sections back into context. Run:

```bash
python3 - << 'PYEOF'
import os

firm_folder = "[friendly-name]"  # replace with actual value

with open("Design Files/audit_master_assembly.html", "r") as f:
    html = f.read()

sections = [
    ("01", "section_01_cover.html"),
    ("02", "section_02_toc.html"),
    ("03", "section_03_firm_overview.html"),
    ("04", "section_04_about_smb.html"),
    ("05", "section_05_growth_health.html"),
    ("06", "section_06_lead_generation.html"),
    ("07", "section_07_08_09_intake_team_profit.html"),
    ("10", "section_10_whats_possible.html"),
    ("11", "section_11_next_steps.html"),
]

for num, fname in sections:
    marker = f"<!-- INSERT SECTION {num} CONTENT HERE -->"
    path = os.path.join(firm_folder, "sections", fname)
    with open(path, "r") as f:
        content = f.read()
    html = html.replace(marker, content)

out = os.path.join(firm_folder, "index.html")
with open(out, "w") as f:
    f.write(html)

print(f"Assembled: {out}")
PYEOF
```

**Note:** Before running, verify the exact `<!-- INSERT SECTION XX CONTENT HERE -->` comment strings in `audit_master_assembly.html` match what the script uses. Adjust section numbers if needed.

Then copy the CSS:
```bash
cp "Design Files/audit_styles.css" "[friendly-name]/audit_styles.css"
```

Verify both `[friendly-name]/index.html` and `[friendly-name]/audit_styles.css` exist and are not empty.

---

## FINAL CHECK

Scan `[friendly-name]/index.html` and confirm:
- No `<!-- FILL: -->` placeholder text remains anywhere
- No `<style>` blocks or `style=""` attributes exist anywhere
- All 11 sections are present
- All image URLs are unmodified
- `<link rel="stylesheet" href="audit_styles.css">` is present with the href exactly as shown
- `audit_styles.css` is present in `[friendly-name]/`

Fix anything that fails before committing.

---

## COMMIT AND PUSH TO MAIN

```bash
git checkout main
git add "[friendly-name]/"
git commit -m "Add growth audit: [Firm Name] ([Date])"
git push origin main
```

Always commit directly to main — never create a branch. Confirm push succeeded and report the commit hash.
