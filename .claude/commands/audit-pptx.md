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

## DBM LANGUAGE — CUSTOMER-FACING TRANSLATION

The research notes contain the owner's **Dominant Buying Motive** in internal shorthand (e.g., "Jay takes real time off"). The deck is shown to the client — translate that shorthand into aspirational language the owner would say about themselves.

**The rule:** The sales companion speaks *about* the client to the rep ("Jay is trapped by his phone"). The deck speaks *to* the client about their future ("The freedom to step away — and trust your firm handles it").

**Translation guide:**

| Internal shorthand (research notes) | Client-facing version (deck) |
|---|---|
| "takes real time off" | "Step away from the firm — and it still runs" |
| "not the one doing everything" | "A team that performs without you in every meeting" |
| "hit $X revenue" | "A firm that generates $X — predictably, every month" |
| "stop working weekends" | "Weekends back. Nights back. A business that works for you." |
| "be proud of the firm" | "A firm you're proud to hand off — or hand over to the next generation" |

Use the client's own words from the transcript wherever possible. If they said something quotable about what they want their life to look like, that is the DBM.

**Where DBM language appears in the deck — all four touchpoints must reflect it:**

1. **`GOAL_DBM`** (Slide 2 goal card, bottom of left panel) — one short phrase, 6–10 words, first-person outcome: *"Step away and trust the firm runs"*. No jargon, no metrics — pure aspiration.

2. **`SMB_MODEL_DESC`** (Slide 2, below the staircase) — 1–2 sentences explaining the SMB model. End with a sentence connecting the model to *this owner's* outcome: *"When all four pillars work, [Owner] can finally [DBM outcome]."*

3. **`CLOSING_QUOTE`** (Slide 3 closing bar) — the most powerful DBM moment. Write it as a vivid, specific version of the outcome the owner described. Should feel like something they almost said on the call. Put it in quotation marks. No metrics, no SMB jargon — pure vision.

4. **Priority column bullets (Slide 2)** — at least one bullet per column should tie the action to a life outcome, not just a business output. Instead of *"Launch Google Ads campaign"*, write *"Turn Google into a client pipeline that runs without you"*.

**What to avoid in the deck:**
- Do not use internal closer language ("DBM", "stage", "pain points", "closes")
- Do not reference the sales process or mention SMB Team's internal framework by name
- Do not use urgency-pressure framing — the deck should feel like a vision, not a pitch

---



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
5. Set `STAIRCASE_STAGE` to the client's current stage number (2–6) — the script downloads the correct image automatically from Dropbox. Set `WEBSITE_SCREENSHOT_PATH = None` (leave as-is unless a local screenshot PNG exists)
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
- The closing quote on Slide 3 must be vivid, specific, and in the owner's voice — not a generic tagline. If the transcript has a direct quote about what they want their life to look like, use it verbatim or near-verbatim
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
