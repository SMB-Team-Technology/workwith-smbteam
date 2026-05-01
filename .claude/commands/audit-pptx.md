# SMB Team — Audit PowerPoint (Pass 3)

Generates a 3-slide proposal PowerPoint from a completed audit. Run this after `/audit-write` finishes (all section files must exist).

## How to invoke

```
/audit-pptx
Firm Name: [Full legal name]
Friendly Name: [same lowercase-hyphenated value used in /audit-write]
Sales Rep: [rep's full name]
Date: [same date used in /audit-write — Month DD, YYYY]
```

---

## BEFORE STARTING

Read the following files (all data comes from them — no new research):
1. `[friendly-name]/sections/section_05_growth_health.html` — urgency score, pillar traffic lights
2. `[friendly-name]/sections/section_11_next_steps.html` — packages, prices, ROI, timeline
3. `[friendly-name]/sections/section_06_lead_generation.html` — competitor data
4. `[friendly-name]/sections/section_executive_summary.html` — top priorities, closing statement
5. `[friendly-name]/[FirmName]_[Date]_Research_Notes.txt` — DBM, stage, goals

If any of these files does not exist, stop and tell the user to run `/audit-write` first.

---

## WHAT THE PPTX CONTAINS

**Slide 1 — Where [Firm] Stands Today**
Assessment overview: urgency score, 4-pillar health indicators, key findings (3 negative + 1 positive), competitor review table, stage strip.

**Slide 2 — Your Growth Plan: 3 Priorities to Reach [Goal]**
Action plan: SMB model description, goal statement tied to DBM, three priority columns (Marketing Engine / Fix Intake / Team & Profit Systems) with 5 bullets each.

**Slide 3 — Your Investment & What Happens Next**
Pricing: two package cards with bundled and retail prices, bundle total + savings, ad spend note, ROI projections, first-90-days timeline, closing quote.

---

## EXTRACTION RULES

Copy values exactly — do not rewrite or recompute.

**From section_05_growth_health.html:**
- `URGENCY_SCORE` — the number in the urgency-score element
- `PILLARS` — for each of the four sc-cards, extract: traffic light class (`red`→`"RED"`, `amber`→`"AMBER"`, `green`→`"GREEN"`), status label text, and the first finding bullet as the one-line detail (max ~20 chars — trim if needed)

**From section_11_next_steps.html:**
- `PACKAGES` — package name (from package-label div), bundled price, retail/stand-alone price, deliverables summary line (condense to one line, ≤65 chars)
- `BUNDLE_TOTAL` — copy from investment-total
- `BUNDLE_SAVINGS` — copy savings callout text
- `AD_SPEND_NOTE` — copy recommended ad spend range row
- `AVG_CASE_VALUE`, conservative/aggressive cases + revenue + ROAS — copy from Block 4 ROI table
- `TIMELINE` — 5 first-90-days milestone items (Day 1 / Day 14 / Week 2 / Week 3 / Month 3), condense each action to ≤55 chars

**From section_06_lead_generation.html:**
- `COMPETITORS` — 3 named competitors with review counts and a one-phrase note each

**From section_executive_summary.html:**
- `FINDINGS` — copy top priorities as findings (first 3 as "neg", last as "pos" if a strength exists — check section_05 for the positive finding)
- `CLOSING_QUOTE` — copy exec-closing statement as the slide 3 quote

**From research notes:**
- `STAGE_TEXT` — current stage and goal stage
- `GOAL_HEADLINE` — e.g. "$1M → $1.8M revenue" (from DBM / revenue goal)
- `GOAL_DBM` — brief DBM phrase (e.g. "Jesse takes real time off")
- `SLIDE_2_TITLE` — "Your Growth Plan: 3 Priorities to Reach [monthly goal]"

**Priority column titles and bullets (Slide 2):**
Derive from section_11 Block 1 / quick wins and section_06–09 findings. Map to three themes:
- Priority 1 → Marketing Engine (lead gen actions)
- Priority 2 → Fix Intake & Stop Losing Cases (intake actions)
- Priority 3 → Install Team & Profit Systems (team + profit actions)

Each bullet: one specific action for this firm, ≤55 chars.

---

## GENERATING THE PPTX

1. Copy `Design Files/audit_pptx_template.py` to `[friendly-name]/[FirmName]_[Date]_Proposal.py`
2. Fill every `# FILL:` placeholder using the extraction rules above
3. Set `OUTPUT_PATH = "[friendly-name]/[FirmName]_[Date]_Proposal.pptx"`
4. Set `SALES_REP` to the sales rep name
5. For images: set `WEBSITE_SCREENSHOT_PATH = None` and `STAIRCASE_IMAGE_PATH = None` unless screenshot files exist in the firm's folder (name them `website_screenshot.png` and `staircase.png` to enable)
6. Verify no `# FILL:` placeholder text remains (the word "FILL" should not appear in any string value)
7. Run the script:

```bash
python3 "[friendly-name]/[FirmName]_[Date]_Proposal.py"
```

8. Confirm the output prints "Saved: … (3 slides)"
9. Verify the file exists and is not empty:

```bash
wc -c "[friendly-name]/[FirmName]_[Date]_Proposal.pptx"
```

---

## CRITICAL RULES

- Copy prices exactly from section_11 — never round or estimate
- Bullet text: one idea, one sentence, ≤55 chars, 8th-grade reading level
- Priority column bullets must be firm-specific — no generic language
- The closing quote on Slide 3 should be in quotation marks, tied to the owner's DBM
- Do not add a fourth package card — maximum two packages per the template
- Never modify `Design Files/audit_pptx_template.py` — work in the firm's copy only

---

## COMMIT AND PUSH

After the PPTX is confirmed saved:

```bash
git add "[friendly-name]/[FirmName]_[Date]_Proposal.pptx" "[friendly-name]/[FirmName]_[Date]_Proposal.py"
git commit -m "Add proposal PPTX: [Firm Name] ([Date])"
GIT_TERMINAL_PROMPT=0 git push origin main
git log -1 --format="%H %s"
```

Report the commit hash. Done.
