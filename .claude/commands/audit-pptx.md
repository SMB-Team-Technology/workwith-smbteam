# SMB Team — Audit PowerPoint (Pass 3)

Fills and generates the 6-slide proposal PowerPoint. This is STEP 3 of `/audit-write`, which does the package, price, ad spend and ROI workings first (STEP 1–2) and records them as a BUILD NOTES comment block in the firm's `_Proposal.py`. The deck replaces the retired "Growth, Profit & Freedom Roadmap" website and Sales Companion PDF, and is built from the same inputs the website was.

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
1. `[friendly-name]/[FirmName]_[Date]_Research_Notes.txt` — the STEP 9B KPI AND DIAGNOSIS block (slides 1–3), research findings, DBM, goals, STEP 9 transcript extraction and `Key prospect quotes`
2. `[friendly-name]/package_decision.json` — packages and prices (as applied in `/audit-write` STEP 1)
3. The BUILD NOTES block at the top of `[friendly-name]/[FirmName]_[Date]_Proposal.py` (written in `/audit-write` STEP 2) — prices, ad spend, ROI, the "why this range" sentence, the 3 What You Told Us items with their verbatim lines, overrides and escalation flags

If the research notes do not exist, stop and tell the user to run `/audit-research` first. If the BUILD NOTES block is missing, do `/audit-write` STEP 1–2 first.

Never read `[friendly-name]/sections/`, `[friendly-name]/index.html` or `*_Sales_Companion.*` — those are from the retired website and PDF, and older firm folders still contain them.

---

## WHAT THE PPTX CONTAINS

Six slides that make one argument, the way our best hand-built decks run on a call: **one number from the call → what drives it → what we do about each driver → what we're recommending → how it rolls out → what it costs.** The package and prices are decided in `/audit-write` STEP 1 and never change here — these slides only make the case for them. Every slide must tie back to the slide-1 KPI.

**Slide 1 — Your Priorities, In Your Words.** Left: the KPI card — the one financially tangible number from the call that the recommendation moves (e.g. cost per case, caseload, months the books are behind), with the client's own line about it and up to two supporting figures. Right: up to three more client quotes, each with a bold line saying how the proposal answers it. Talk track: "Here's what I heard, and the number you told me matters most."

**Slide 2 — The Diagnosis.** "Why [the KPI] is where it is": 3–4 root causes, each with its evidence number (or finding), a target when call data supports one, two plain sentences and the source. Replaces the old broad "key gaps". Talk track: "Four things drive that number. Here's each one."

**Slide 3 — The Plan.** 3–4 actions built from the recommended products' deliverables. Each card names the diagnosed cause it fixes, what we do, the metric it moves and its target. Talk track: "Here's what we do about each one."

**Slide 4 — The Recommended Strategy.** 1–3 pieces: what we're recommending, why each was chosen for this firm (tied to slide 2), and its deliverables.

**Slide 5 — Rollout Plan.** A clearly marked placeholder drawn by the engine (no FILL values) plus a "What we'll measure" row built from the KPI and the plan metrics. Real onboarding content comes later — never add onboarding steps, commitments or timelines.

**Slide 6 — Your Investment & What Happens Next.** Unchanged from the 3-slide deck: package cards, bundle total and savings, ad spend note, ROI projection, "How this plan addresses it" panel, closing quote.

**Speaker notes.** `SELLER_NOTES = {slide_number: "…"}` carries call prep for the seller that doesn't belong on a slide: which figures are the seller's own, what number to ask for, what to confirm before quoting a target. The engine adds its own notes for plan cards with no target and for the rollout placeholder. **Notes travel inside the .pptx** — it is attached to the seller email, uploaded to a public HubSpot link and may be forwarded to the client — so write nothing you wouldn't want the client to read: never escalation flags, approval requirements, doubts about their revenue, internal pricing or ROI caveats, or criticism of the firm or its staff. Those stay in the BUILD NOTES. Keep notes to slides 1–5.

---

## DATA RULES — APPLY TO EVERY NUMBER ON SLIDES 1–5

- **Source = the research notes' STEP 9B block** ("KPI AND DIAGNOSIS"), plus STEP 1–9 for research evidence. Copy figures exactly as written there ("about 60", "$4,500", "maybe 10"). Never round, convert, combine two figures into a new one, or estimate.
- **Only numbers said on the call** (client or seller) or measured/seen in the research. A seller's figure is presented as discussed on the call ("the cost range quoted on the call"), never as the firm's own result. Never an `UNCONFIRMED` figure (review counts, ratings), a "NOT OBSERVED" item, or a benchmark from our pricing/CPL tables.
- **The KPI must support the recommendation.** It is the number the recommended products move. If the seller changed the package and STEP 9B's headline KPI no longer fits, use its "Alternate KPI" line; if none fits, treat it as "no usable KPI".
- **No usable KPI** (STEP 9B says `none usable`, or nothing fits the package): `KPI_FOCUS["kind"] = "qualitative"`, headline = the pain point in the client's words, no invented number anywhere, and `SELLER_NOTES[1]` tells the seller there was no usable number and what to ask for (from STEP 9B "Seller should confirm"). The build refuses to run without that note.
- **Targets** are always labelled "Target:" by the engine (never type the prefix) and rest on call data — STEP 9B's "Target basis" or the client's stated goal. A client goal is worded as theirs ("10 a month (your goal)"). With no basis, set `target: None`: the slide shows "Target: to be confirmed" and the seller gets a speaker note. Never make one up.
- AI-summary figures tagged `[AI summary — seller to confirm]` may be shown only with a `SELLER_NOTES` line asking the seller to confirm them before the call.
- Record in the BUILD NOTES where each slide 1–3 number came from (STEP 9B line or research step).

---

## DBM LANGUAGE — CUSTOMER-FACING TRANSLATION

The research notes contain the owner's **Dominant Buying Motive** in internal shorthand (e.g., "Jay takes real time off"). The deck is shown to the client — translate that shorthand into aspirational language the owner would say about themselves.

**The rule:** The research notes speak *about* the client to the rep ("Jay is trapped by his phone"). The deck speaks *to* the client about their future ("The freedom to step away — and trust your firm handles it").

| Internal shorthand (research notes) | Client-facing version (deck) |
|---|---|
| "takes real time off" | "Step away from the firm — and it still runs" |
| "not the one doing everything" | "A team that performs without you in every meeting" |
| "hit $X revenue" | "A firm that generates $X — predictably, every month" |
| "stop working weekends" | "Weekends back. Nights back. A business that works for you." |
| "be proud of the firm" | "A firm you're proud to hand off — or hand over to the next generation" |

Use the client's own words from the transcript wherever possible. DBM language belongs in `CLOSING_QUOTE` (slide 6) — a vivid, specific version of the outcome the owner described, in quotation marks, no metrics, no SMB jargon — and may color the `why` lines on slide 4.

**What to avoid in the deck:** internal closer language ("DBM", "stage", "pain points", "closes"); SMB Team's internal frameworks by name; urgency-pressure framing.

---

## FIELD RULES

Copy values exactly — do not rewrite or recompute.

**Slide 1 — `KPI_FOCUS`** (from STEP 9B):
- `kind`: `"kpi"` or `"qualitative"` (see DATA RULES).
- `label`: the KPI's name, 1–3 words ("Cost per case", "Caseload", "Books behind").
- `headline`: a short verbatim client line about the number (≤60 chars; `headline_is_quote: True` — the engine adds the quote marks), from STEP 9B "KPI quotes". With no verbatim transcript, a plain statement of the number instead (`headline_is_quote: False`).
- `detail`: one sentence with the exact figures as said (≤110 chars), e.g. "$4,500 cost per retained client on a $9,100 average family law case."
- `baseline`: the current value in 2–5 words ("About 60 open cases") — reused on slide 5.
- `stats`: 0–2 `(label, value)` supporting figures from STEP 9B, ≤40 chars each. A client goal is labelled "Your goal", never "Target".

**Slide 1 — `PROSPECT_QUOTES`**: 0–3 `(topic, quote, tie_line)` — the most sensitive field in the deck.
- Source: STEP 9B "KPI quotes", then the What You Told Us lines in the BUILD NOTES, then `Key prospect quotes`. Never an AI summary, the seller's words, or our research. Don't repeat the headline quote.
- Only problems or priorities the prospect raised themselves. Copy the words exactly; you may cut from the start or end or mark a middle cut with "…", drop comma-set filler, and capitalize the first letter. Never reword, combine or strengthen. ≤120 chars.
- `topic`: 1–3 words. `tie_line`: how the proposal answers it, ≤70 chars, connected to a real deliverable — no promised outcomes or dates.
- Apply the What You Told Us "Never include" list in `audit-write.md` (no named staff, personal/health/family matters, partner disputes, financial-distress figures).
- No verbatim transcript: `PROSPECT_QUOTES = []` — the KPI card takes the full width.

**Slide 2 — `DIAGNOSIS_TITLE`, `DIAGNOSIS_INTRO`, `DIAGNOSIS`, `DIAGNOSIS_FIX_LINE`** (from STEP 9B "Diagnosis"):
- `DIAGNOSIS_TITLE` names the KPI ("Why Each Case Costs $4,500", "Why Your Caseload Is Shrinking"), ≤40 chars. `DIAGNOSIS_INTRO`: one plain line, ≤90 chars.
- 3–4 causes, biggest first, each specific to this firm — never generic categories like "Lead Generation".
  - `title` ≤32 chars, plain words. `metric`: the evidence number exactly as recorded, or `""` for a cause with no number. `metric_label` ≤40 chars.
  - `target`: per DATA RULES, or `None`.
  - `body`: two short sentences — what's happening and what it costs them (≤120 chars).
  - `source`: where it came from, short ("Discovery call, Oct 26", "Lighthouse test", "Seen live on the call", "Seller, on the call").
- `DIAGNOSIS_FIX_LINE` ≤140 chars: one line pointing to how slide 3 answers the causes, shown after the engine's "How we fix it:" lead-in (don't type that prefix).

**Slide 3 — `PLAN_KICKER`, `PLAN_TITLE`, `PLAN`, `PLAN_NOTE`:**
- `PLAN_KICKER`: the product area ("Paid media and website", "Financial clarity"). `PLAN_TITLE`: the outcome for the KPI, ≤40 chars ("Lower What Each Lead Costs").
- 3–4 actions. Every diagnosed cause must be fixed by at least one action (the build checks).
  - `title` ≤34 chars. `fixes`: the DIAGNOSIS number it answers.
  - `actions`: 2–4 bullets, ≤60 chars, each a deliverable of the recommended products (catalog tables in `audit-write.md` and `Design Files/Scoping_and_Ad_Spend_Guide.md` — e.g. words of content, GBP locations, review requests at that tier). Never a deliverable the package doesn't include; never live chat or CRM setup.
  - `metric`: what it moves, 1–4 words. `target`: per DATA RULES, or `None`.
- `PLAN_NOTE`: optional line shown after the engine's own "Also included:" lead-in — don't type that prefix (≤160 chars) for other deliverables of the package, or `None`.
- Never put a marketing action on this slide unless a marketing/ads package is part of the recommendation.

**Slide 4 — `STRATEGY_TITLE`, `STRATEGY`:**
- 1–3 pieces in `package_decision.json` order (marketing, then coaching/fractional, then LAW). A single product may be split into pieces (Full Service Marketing → "Get found" + "Get the call"); never add a product that isn't in the package.
- `product`: the catalog product name exactly as in the BUILD NOTES. `title`: 1–3 words. `channels` ≤40 chars.
- `deliverables`: 3–5 catalog deliverables for that product/tier, ≤55 chars each — fractional packages include the Elite Coach group deliverables (see `audit-write.md`).
- `why` ≤110 chars: why this firm needs it, tied to a slide 2 cause or the KPI. No promised results.

**Slide 5:** nothing to fill. Do not add onboarding steps, dates or commitments anywhere in the deck.

**Slide 6 — from `package_decision.json` and the BUILD NOTES (unchanged rules):**
- `PACKAGES` — package name, bundled (charged) price and stand-alone price exactly as in the BUILD NOTES / `package_decision.json`, and a deliverables summary line (≤65 chars; fractional packages include the Elite Coach group deliverables). When `pricing_mode` is `"standalone"`, the charged price is the stand-alone price: put it in the bundled-price slot and write `"stand-alone price"` in the retail slot. A product with no stand-alone price (AI Workforce Pro, AI Workforce Pro – Starter) gets `""` in the retail slot. Card order follows `package_decision.json`. Maximum two cards.
- `BUNDLE_TOTAL` — the total monthly investment from the BUILD NOTES. `BUNDLE_SAVINGS` — "Save $X,XXX/mo by bundling" (when `pricing_mode` is `"standalone"`: `"Stand-alone price (no bundle)"`).
- `AD_SPEND_NOTE` — only with a marketing/ads package: the conservative–aggressive range plus a short payoff clause from the "why this range" sentence, under ~110 characters. Otherwise `None` (this also hides the ROI card).
- `AVG_CASE_VALUE`, conservative/aggressive labels and results — copy from the BUILD NOTES ROI projections; "(est.)" or "(assumed)" when the case value is a practice-area default.
- `WHAT_YOU_TOLD_US` — exactly 3 `(short_label ≤16 chars, action ≤55 chars)` items from the BUILD NOTES' What You Told Us list, same order, under the heading "How this plan addresses it".
- `CLOSING_QUOTE` — one sentence tied to the owner's DBM (DBM rules above). No placeholders.

---

## GENERATING THE PPTX

1. Copy `Design Files/audit_pptx_template.py` to `[friendly-name]/[FirmName]_[Date]_Proposal.py`
2. Keep the BUILD NOTES block from `/audit-write` STEP 2 at the top, then fill every `# FILL:` placeholder using the extraction rules above and delete the trailing `# FILL…` comments
3. Set `OUTPUT_PATH = "[friendly-name]/[FirmName]_[Date]_Proposal.pptx"`
4. Set `SALES_REP` to the sales rep name
5. Copy `Design Files/smb_team_logo.png` into `[friendly-name]/` so the footer logo renders
6. Verify no `# FILL:` placeholder text remains (the word "FILL" should not appear in any string value). If `AD_SPEND_NOTE` was deliberately set to `None` because no marketing/ads package was sold, that's expected — not a missed FILL.
7. Before running, diff the copy's layout engine against the master template and confirm there's no output — anything below `LAYOUT ENGINE — DO NOT MODIFY BELOW THIS LINE` must be byte-for-byte identical to `Design Files/audit_pptx_template.py` (this includes `FONT`, every color constant, and every `build_*`/helper function):

```bash
diff <(sed -n '/LAYOUT ENGINE/,$p' "Design Files/audit_pptx_template.py") \
     <(sed -n '/LAYOUT ENGINE/,$p' "[friendly-name]/[FirmName]_[Date]_Proposal.py")
```

8. Run the script:

```bash
python3 "[friendly-name]/[FirmName]_[Date]_Proposal.py"
```

9. Confirm the output prints "Saved: … (6 slides)". If it prints "Deck not built — fix the values above the LAYOUT ENGINE line", fix each listed item and re-run. If it also prints a `WARNING: N field(s) exceeded their character budget…` block, that means the layout engine had to truncate something you filled in — go back and shorten that field's source copy rather than shipping the truncated version. A `NOTE: N field(s) were shrunk to fit their box` block is informational: the engine measured that text against the Poppins font and dropped it a half-point at a time until it fit. That is expected for long firm names and is not an error.
10. Verify the file exists and is not empty:

```bash
wc -c "[friendly-name]/[FirmName]_[Date]_Proposal.pptx"
```

---

## CRITICAL RULES

- Copy prices exactly from the BUILD NOTES / `package_decision.json` — never round or estimate
- Bullet text: one idea, one sentence, 8th-grade reading level, firm-specific — no generic language
- Every number on slides 1–5 follows the DATA RULES above: said on the call or measured in research, copied exactly, never estimated
- The closing quote on Slide 6 must be vivid, specific, and in the owner's voice — not a generic tagline. If the transcript has a direct quote about what they want their life to look like, use it verbatim or near-verbatim
- Do not add a third package card — maximum two packages per the template
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
