# SMB Team — Audit PowerPoint (Pass 3)

Fills and generates the 3-slide proposal PowerPoint. This is STEP 3 of `/audit-write`, which does the package, price, ad spend and ROI workings first (STEP 1–2) and records them as a BUILD NOTES comment block in the firm's `_Proposal.py`. The deck replaces the retired "Growth, Profit & Freedom Roadmap" website and Sales Companion PDF, and is built from the same inputs the website was.

Run it through `/audit-write`. Running `/audit-pptx` on its own is only for re-filling an existing deck whose `_Proposal.py` already has its BUILD NOTES.

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
1. `[friendly-name]/[FirmName]_[Date]_Research_Notes.txt` — findings by pillar, competitors, stage, DBM, goals, STEP 9 transcript extraction and `Key prospect quotes`
2. `[friendly-name]/package_decision.json` — packages and prices (as applied in `/audit-write` STEP 1)
3. The BUILD NOTES block at the top of `[friendly-name]/[FirmName]_[Date]_Proposal.py` (written in `/audit-write` STEP 2) — prices, ad spend, ROI, the "why this range" sentence, the 3 What You Told Us items with their verbatim lines, overrides and escalation flags

If the research notes do not exist, stop and tell the user to run `/audit-research` first. If the BUILD NOTES block is missing, do `/audit-write` STEP 1–2 first.

Never read `[friendly-name]/sections/`, `[friendly-name]/index.html` or `*_Sales_Companion.*` — those are from the retired website and PDF, and older firm folders still contain them.

---

## WHAT THE PPTX CONTAINS

**Slide 1 — Where [Firm] Stands Today**
A recap of the discovery call, not a scorecard. Three blocks only: "What you told us" (2–3 of the prospect's own lines, each labelled "You said:"), "Where you are today" (current stage and goal stage on the legacy staircase), and "Your key gaps" (3 audit gaps, each under a category). No scores, ratings, urgency numbers or competitor table — reps can't explain them at a glance and prospects ask what gets them to the next number. The rep's talk track: "To summarize our prior discussion, here's what I heard and took back to the team. You said ___. Here's where you are today and where you want to be." Keep every line short — the prospect should be listening, not reading.

**Slide 2 — Your Growth Plan: 3 Priorities to Reach [Goal]**
Action plan focused on the prospect: just three priority columns (themed to what this firm is actually buying and its real priorities — see below), each with up to 5 bullets in a single bulleted list. Columns are always navy / green / navy and labelled "Priority 1–3" — the engine sets this, not the FILL values. The rep's talk track: "Based on everything I've seen, there are three areas we need to focus on: X, Y and Z. Here are the key benefits of each. Next, I'll show you what it looks like to have that in place." Keep the column titles short enough to say out loud in that sentence.

**Slide 3 — Your Investment & What Happens Next**
Pricing: two package cards with bundled and retail prices, bundle total + savings, ad spend note, ROI projections, "How this plan addresses it" panel (the What You Told Us items), closing quote.

---

## DBM LANGUAGE — CUSTOMER-FACING TRANSLATION

The research notes contain the owner's **Dominant Buying Motive** in internal shorthand (e.g., "Jay takes real time off"). The deck is shown to the client — translate that shorthand into aspirational language the owner would say about themselves.

**The rule:** The research notes speak *about* the client to the rep ("Jay is trapped by his phone"). The deck speaks *to* the client about their future ("The freedom to step away — and trust your firm handles it").

**Translation guide:**

| Internal shorthand (research notes) | Client-facing version (deck) |
|---|---|
| "takes real time off" | "Step away from the firm — and it still runs" |
| "not the one doing everything" | "A team that performs without you in every meeting" |
| "hit $X revenue" | "A firm that generates $X — predictably, every month" |
| "stop working weekends" | "Weekends back. Nights back. A business that works for you." |
| "be proud of the firm" | "A firm you're proud to hand off — or hand over to the next generation" |

Use the client's own words from the transcript wherever possible. If they said something quotable about what they want their life to look like, that is the DBM.

**Where DBM language appears in the deck — both touchpoints must reflect it:**

1. **`CLOSING_QUOTE`** (Slide 3 closing bar) — the most powerful DBM moment. Write it as a vivid, specific version of the outcome the owner described. Should feel like something they almost said on the call. Put it in quotation marks. No metrics, no SMB jargon — pure vision.

2. **Priority column bullets (Slide 2)** — at least one bullet per column should tie the action to a life outcome, not just a business output. Instead of *"Launch Google Ads campaign"*, write *"Turn Google into a client pipeline that runs without you"*.

**What to avoid in the deck:**
- Do not use internal closer language ("DBM", "stage", "pain points", "closes")
- Do not reference the sales process or mention SMB Team's internal framework by name
- Do not use urgency-pressure framing — the deck should feel like a vision, not a pitch

---



Copy values exactly — do not rewrite or recompute.

**Slide 1 — `PROSPECT_QUOTES` (the prospect's own words):**
2–3 `(speaker_label, quote)` pairs. This is the most sensitive field in the deck — it puts words in the prospect's mouth on screen in front of them.
- Source: the verbatim transcript lines logged for the What You Told Us items in the BUILD NOTES first (so slide 1 and slide 3 tell the same story), then the research notes' `Key prospect quotes` list. Never from an AI summary, the seller's notes, or our research.
- Only problems the prospect raised themselves. Do not present something we consider a problem (e.g. "no AI agents running workflows", a slow website) as their pain unless they said it. Goals, small talk, budget and objections are not eligible.
- Copy the words exactly. You may cut words from the start or end, or replace a cut in the middle with "…", but never reword, combine lines, or strengthen what they said. Drop filler ("you know", "um") only where it is set off by commas. You may capitalize the first letter. Each quote ≤130 characters; shorter is better.
- `speaker_label` is `"You said"` for the owner the deck is addressed to, or `"<First name> said"` for another attendee from the firm (e.g. `"Jennifer said"`).
- Apply the What You Told Us "Never include" list in `audit-write.md`: no named employees or criticism of staff, personal/health/family matters, partner disputes, or financial-distress figures.
- No full verbatim transcript (none, or only a Fathom AI summary): set `PROSPECT_QUOTES = []`. The slide then drops the panel and the staircase takes the full width — never invent or paraphrase a quote to fill it.

**Slide 1 — `KEY_GAPS` (from the research notes):**
- Exactly 3 `(category, gap)` pairs — the three biggest gaps the audit found, most important first. `category` is one of `"Lead Generation"`, `"Intake"`, `"Team"`, `"Profit Plan"` (the pillar the finding sits under); use each category at most once where possible.
- `gap` is one plain-language sentence, consequence first, ≤90 characters, taken from a finding stated in the research notes (rank pillars with the traffic-light criteria in `audit-write.md`, reddest first). Apply the `UNCONFIRMED` review-count rule in `audit-write.md`. No scores, ratings or "Amber/Red" language.
- These are our findings, so never word them as something the prospect said.

**From `package_decision.json` and the BUILD NOTES:**
- `PACKAGES` — package name, bundled (charged) price and stand-alone price exactly as in the BUILD NOTES / `package_decision.json`, and a deliverables summary line for that package (condense to one line, ≤65 chars; fractional packages include the Elite Coach group deliverables — see `audit-write.md`). When `pricing_mode` is `"standalone"`, the charged price is the stand-alone price.
- `BUNDLE_TOTAL` — the total monthly investment from the BUILD NOTES
- `BUNDLE_SAVINGS` — "Save $X,XXX/mo by bundling" with the total savings from the BUILD NOTES (when `pricing_mode` is `"standalone"` there are no savings: set `BUNDLE_SAVINGS = ""`)
- `AD_SPEND_NOTE` — only fill this if a marketing/ads package is part of the recommendation (the BUILD NOTES have an ad spend range). Copy the recommended ad spend range (conservative–aggressive) and append a short clause distilled from the BUILD NOTES' "why this range" sentence — the payoff, not the calculation basis, e.g. `"+ Recommended ad spend: $X,XXX–$XX,XXX/mo — to turn high-intent [practice area] searches into signed cases"`. Keep the full note under ~110 characters so it doesn't get truncated on the slide. If no marketing/ads package is part of the recommendation, set `AD_SPEND_NOTE = None` — do not show an ad spend note or rationale for a service this firm isn't buying. This also controls whether the "Projected Return on Ad Spend" card renders on Slide 3 (they're gated together in the layout engine) — when `AD_SPEND_NOTE` is `None`, `AVG_CASE_VALUE`/`CONSERVATIVE_*`/`AGGRESSIVE_*` are unused and can be left at their placeholder values.
- `AVG_CASE_VALUE`, conservative/aggressive cases + revenue + ROAS — copy from the ROI projections in the BUILD NOTES (calculated with the ROI PROJECTIONS rules in `audit-write.md`; say "(est.)" or "(assumed)" when the case value is a practice-area default)
- `WHAT_YOU_TOLD_US` — exactly 3 items from the BUILD NOTES' What You Told Us list (or the What We Found fallback), in the same order — selected with the WHAT YOU TOLD US rules in `audit-write.md`. They appear on slide 3 under the fixed heading "How this plan addresses it". Each item is `(short_label, action)`: `short_label` names the owner's issue in 2–3 words (≤16 chars, e.g. "Missed calls"); `action` condenses that row's "how this plan addresses it" clause (≤55 chars). Never add anything that isn't in that list, and never add outcomes, dates, or lead/click counts. Never leave the list empty — the build stops if it doesn't have exactly 3 items.

**Closing quote:**
- `CLOSING_QUOTE` — one sentence tied to this firm's central opportunity and the owner's DBM, written per the DBM rules above (the retired website's executive-summary closing line used the same rule). No placeholders.

**From research notes:**
- `STAGE_TEXT` — current stage and goal stage, in the form `"Stage 4: Small Business Manager  →  Goal: Stage 6, Law Firm Owner"`. Keep the `→` and both `Stage N` numbers: the engine draws the legacy staircase (stages 2–6) from the numbers and labels each end with the official stage name, so the names after the numbers are only a fallback.
- `SLIDE_2_TITLE` — "Your Growth Plan: 3 Priorities to Reach [monthly goal]"

**Priority column titles and bullets (Slide 2):**
Derive from the research notes' findings and opportunities (lead generation, intake, team, profit), the DBM, and — critically — what this firm is actually buying (`package_decision.json` and the BUILD NOTES). Each of the 3 columns must reflect a real priority for this firm; do not default to a generic theme regardless of what was sold.

- A column may be themed "Build the Marketing Engine" (lead gen actions) **only if a marketing/ads package is part of this firm's recommendation.** If no marketing/ads package was sold (check `marketing_tier`/`marketing_name` in `package_decision.json`, or that a Transcript-Stated Need Override in `audit-write.md` dropped marketing), do not title any column "Marketing Engine" or imply ad spend is part of this plan — theme that column after an actual sold service or genuine next priority instead (e.g., intake, team systems, profit systems, a coaching foundation phase, or a phased "future marketing" note only if the roadmap genuinely calls for one later).
- Intake and Team/Profit themes ("Fix Intake & Stop Losing Cases", "Install Team & Profit Systems") generally still apply regardless of package mix, since those pillars matter to every firm — but their bullets must stay firm-specific and reflect what was actually found/recommended, never generic filler.

Each bullet: one specific action for this firm, ≤55 chars.

---

## GENERATING THE PPTX

1. Copy `Design Files/audit_pptx_template.py` to `[friendly-name]/[FirmName]_[Date]_Proposal.py`
2. Keep the BUILD NOTES block from `/audit-write` STEP 2 at the top, then fill every `# FILL:` placeholder using the extraction rules above and delete the trailing `# FILL…` comments
3. Set `OUTPUT_PATH = "[friendly-name]/[FirmName]_[Date]_Proposal.pptx"`
4. Set `SALES_REP` to the sales rep name
5. Copy `Design Files/smb_team_logo.png` into `[friendly-name]/` so the footer logo renders
6. Verify no `# FILL:` placeholder text remains (the word "FILL" should not appear in any string value). If `AD_SPEND_NOTE` was deliberately set to `None` because no marketing/ads package was sold, that's expected — not a missed FILL.
7. Before running, diff the copy's layout engine against the master template and confirm there's no output — anything below `LAYOUT ENGINE — DO NOT MODIFY BELOW THIS LINE` must be byte-for-byte identical to `Design Files/audit_pptx_template.py` (this includes `FONT`, every color constant, `PRIORITY_STYLE`, and every `build_slideN`/helper function):

```bash
diff <(sed -n '/LAYOUT ENGINE/,$p' "Design Files/audit_pptx_template.py") \
     <(sed -n '/LAYOUT ENGINE/,$p' "[friendly-name]/[FirmName]_[Date]_Proposal.py")
```

8. Run the script:

```bash
python3 "[friendly-name]/[FirmName]_[Date]_Proposal.py"
```

9. Confirm the output prints "Saved: … (3 slides)". If it also prints a `WARNING: N field(s) exceeded their character budget…` block, that means the layout engine had to truncate something you filled in — go back and shorten that field's source copy rather than shipping the truncated version. A `NOTE: N field(s) were shrunk to fit their box` block is informational: the engine measured that text against the Poppins font and dropped it a half-point at a time until it fit. That is expected for long firm names and is not an error.
10. Verify the file exists and is not empty:

```bash
wc -c "[friendly-name]/[FirmName]_[Date]_Proposal.pptx"
```

---

## CRITICAL RULES

- Copy prices exactly from the BUILD NOTES / `package_decision.json` — never round or estimate
- Bullet text: one idea, one sentence, ≤55 chars, 8th-grade reading level
- Priority column bullets must be firm-specific — no generic language
- The closing quote on Slide 3 must be vivid, specific, and in the owner's voice — not a generic tagline. If the transcript has a direct quote about what they want their life to look like, use it verbatim or near-verbatim
- Do not add a fourth package card — maximum two packages per the template
- Never modify `Design Files/audit_pptx_template.py` — work in the firm's copy only
- Never modify anything below `LAYOUT ENGINE — DO NOT MODIFY BELOW THIS LINE` in the firm's copy either — this includes `FONT` and every color constant. That section is what keeps every deck on-brand and visually consistent with every other deck in the portfolio; the diff in step 7 is the check. The layout engine measures every text box against the bundled Poppins fonts and writes the largest font size that fits. It drops 0.5pt at a time, down to 75% of the design size, and only truncates at a word boundary if the text still doesn't fit. Titles, the header kicker, "/mo", the retail price and the bundle savings line are all positioned from those measurements, so long firm names never spill out of their boxes. It also hard-caps a handful of fields as a backstop (see the `WARNING:` note in step 9) and embeds the Poppins font files into the saved `.pptx` — none of that requires anything from you beyond filling in the `# FILL:` values.

---

## COMMIT AND PUSH

`/audit-write` commits the deck (see its COMMIT AND PUSH section — always to the current branch, never a branch switch). When running `/audit-pptx` on its own:

```bash
git add "[friendly-name]/"*_Proposal.pptx "[friendly-name]/"*_Proposal.py "[friendly-name]/smb_team_logo.png"
git commit -m "Update proposal deck: [Firm Name] ([Date])"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
git pull --rebase origin "$BRANCH" && GIT_TERMINAL_PROMPT=0 git push origin "HEAD:$BRANCH"
git log -1 --format="%H %s"
```

Report the commit hash. Done.
