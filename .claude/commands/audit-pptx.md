# SMB Team — Audit PowerPoint (Pass 3)

Fills and generates the 5-slide proposal PowerPoint. This is STEP 3 of `/audit-write`, which does the package, price, ad spend and ROI workings first (STEP 1–2) and records them as a BUILD NOTES comment block in the firm's `_Proposal.py`. The deck replaces the retired "Growth, Profit & Freedom Roadmap" website and Sales Companion PDF, and is built from the same inputs the website was.

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
3. The BUILD NOTES block at the top of `[friendly-name]/[FirmName]_[Date]_Proposal.py` (written in `/audit-write` STEP 2) — prices, ad spend, ROI, the "why this range" sentence, the What You Told Us lines (slide 1 quote sources), the KPI/diagnosis/target sources, overrides and escalation flags

If the research notes do not exist, stop and tell the user to run `/audit-research` first. If the BUILD NOTES block is missing, do `/audit-write` STEP 1–2 first.

Never read `[friendly-name]/sections/`, `[friendly-name]/index.html` or `*_Sales_Companion.*` — those are from the retired website and PDF, and older firm folders still contain them.

---

## WHAT THE PPTX CONTAINS

Five slides that make one argument, the way our best hand-built decks run on a call: **one number from the call → what drives it → what we do about each driver → what we're recommending → what it costs.** The package and prices are decided in `/audit-write` STEP 1 and never change here — these slides only make the case for them. Every slide must tie back to the slide-1 KPI.

**Slide 1 — Your Priorities, In Your Words.** Left: the KPI card — the one financially tangible number from the call that the recommendation moves (e.g. cost per case, caseload, months the books are behind), with the client's own line about it and up to two supporting figures. Right: up to three more client quotes, each with a bold line saying how the proposal answers it. Along the bottom, when the call gave them: **why it matters to them** (what they really want, in their words) and **if nothing changes** (the cost of inaction, in their words) — then the quote cards cap at two. Talk track: "Here's what I heard, the number you told me matters most, why it matters to you, and what happens if nothing changes."

**Optional — Lawyer Legacy Staircase (after slide 1).** Only when the rep actually walked the client through the staircase on the call. The original staircase graphic rebuilt as native shapes (every number and label is editable text), with the Abyss emphasized: a red line through the staircase and "more profit + more freedom" on the far side. "You Are Here!" only when the client's stage was placed on the call; "Your Goal" only when a goal stage was named. Reps delete the slide if they don't use it (the seller prep says so).

**Slide 2 — The Diagnosis.** "Why [the KPI] is where it is": 3–4 root causes, each with its evidence number (or finding), a target when call data supports one, one short line and the source. A second major problem from the call gets its own block — never folded into the first. Replaces the old broad "key gaps". Talk track: "Four things drive that number. Here's each one."

**Slide 3 — The Plan.** 3–4 actions built from the recommended products' deliverables. Each card names the diagnosed cause it fixes and what we do. Under the cards, a "What we'll measure" row: the slide 1 KPI with today's value, then each action's metric (numbered to its card) and its target when call data supports one. With no target, no target line is drawn. Talk track: "Here's what we do about each one, and how we'll know it's working."

**Slide 4 — The Recommended Strategy.** 1–3 pieces: what we're recommending, why each was chosen for this firm (tied to slide 2), and its deliverables.

**Slide 5 — Your Investment.** "What $X/mo buys" by product, each bundle price beside its struck-through list (stand-alone) price; the monthly investment (with list total and savings), the one-time setup fees (when the package has any; a seller-waived fee is shown as waived) and the year-one total (12 months of fees + setup); the recommended ad spend; and what that ad spend buys. Every number comes from `package_decision.json`. The seller is asked to review the ad spend before the deck goes out (Phase 1 Slack post, deck-ready Slack reply and email).

**No Rollout Plan slide for now.** The engine has one (`SHOW_ROLLOUT`), left out until real onboarding content exists. Never add onboarding steps, commitments or timelines anywhere in the deck.

**Seller prep, not speaker notes.** The deck's speaker notes are always empty — the .pptx goes out on a public HubSpot link and may be forwarded to the client. `SELLER_NOTES = {"priorities": "…", "staircase": "…", "diagnosis": "…", "plan": "…", "strategy": "…", "investment": "…"}` (keyed by slide name — the staircase slide is optional, so numbers move) carries the seller's call prep: what to ask, what to confirm before quoting a figure or target, deal context from the call (where they are in their decision, what else they're weighing). The build writes it, with the engine's own notes (missing targets, the optional staircase slide) and who said each quote, to `<deck>_Seller_Prep.txt` beside the deck; the pipeline sends it to the seller in the email and the Slack "Proposal ready" reply and never commits it. Escalation flags and approval requirements still stay in the BUILD NOTES. Write it for the seller's eyes, but plainly — no criticism of the firm or its staff.

---

## DATA RULES — APPLY TO EVERY NUMBER ON THE STORY SLIDES

- **No slide numbers in slide text** ("see slide 6", "Slide 3 shows…") — the deck's order changes; refer to the plan, the investment, etc. instead.

- **Source = the research notes' STEP 9B block** ("KPI AND DIAGNOSIS"), plus STEP 1–9 for research evidence. Copy figures exactly as written there ("about 60", "$4,500", "maybe 10"). Never round, convert, combine two figures into a new one, or estimate.
- **Only numbers said on the call** (client or seller) or measured/seen in the research. A seller's figure is presented as discussed on the call ("the cost range quoted on the call"), never as the firm's own result. Never an `UNCONFIRMED` figure (review counts, ratings), a "NOT OBSERVED" item, or a benchmark from our pricing/CPL tables.
- **The KPI must support the recommendation.** It is the number the recommended products move. If the seller changed the package and STEP 9B's headline KPI no longer fits, use its "Alternate KPI" line; if none fits, treat it as "no usable KPI".
- **No usable KPI** (STEP 9B says `none usable`, or nothing fits the package): `KPI_FOCUS["kind"] = "qualitative"`, headline = the pain point in the client's words, no invented number anywhere, and `SELLER_NOTES["priorities"]` tells the seller there was no usable number and what to ask for (from STEP 9B "Seller should confirm"). The build refuses to run without that note.
- **Targets** are always labelled "Target:" by the engine (never type the prefix) and rest on call data — STEP 9B's "Target basis" or the client's stated goal. A client goal is worded as theirs ("10 a month (your goal)"). With no basis, set `target: None`: no target line is drawn on the slide and the seller prep notes it. Never make one up, and never write a placeholder such as "to be confirmed". A target is a specific figure or goal someone stated ("at least 10 cases a month"); a general wish ("I don't want to break even", "lower the cost") is not a target — leave `None` and put the wish in the seller note.
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

Use the client's own words from the transcript wherever possible. DBM language may color the `why` lines on slide 4. The closing line on the investment slide (`CLOSING_QUOTE`) is a verbatim quote, never a "version" of what they said — see QUOTE RULES.

**What to avoid in the deck:** internal closer language ("DBM", "stage", "pain points", "closes"); SMB Team's internal frameworks by name; urgency-pressure framing.

---

## FIELD RULES

Copy values exactly — do not rewrite or recompute.

**Slide 1 — `KPI_FOCUS`** (from STEP 9B):
- `kind`: `"kpi"` or `"qualitative"` (see DATA RULES).
- `label`: the KPI's name, 1–3 words ("Cost per case", "Caseload", "Books behind").
- `headline`: a short verbatim client line about the number (≤60 chars; `headline_is_quote: True` — the engine adds the quote marks), from STEP 9B "KPI quotes", with `said_by` (QUOTE RULES). With no verbatim transcript, a plain statement of the number instead (`headline_is_quote: False`, no `said_by`).
- `detail`: one sentence with the exact figures as said (≤110 chars), e.g. "$4,500 cost per retained client on a $9,100 average family law case."
- `baseline`: the current value in 2–5 words ("About 60 open cases") — shown as "Today: …" in the slide 3 "What we'll measure" row.
- `stats`: 0–2 `(label, value)` supporting figures from STEP 9B, ≤40 chars each. A client goal is labelled "Your goal", never "Target".

**QUOTE RULES — every quote anywhere in the deck** (KPI headline, `PROSPECT_QUOTES`, `CLIENT_WHY`, `COST_OF_INACTION`, `CLOSING_QUOTE`):
- **Verbatim from the transcript**, as recorded in the research notes. Allowed edits only: cut from the start or end, mark a middle cut with "…", drop comma-set filler ("you know", "um"), capitalize the first letter. Never reword, combine, condense or "tidy" a line. The build checks every quote against the research notes word for word and stops on one that isn't there.
- **The client's words, never the seller's.** Each quote carries `said_by` — "Full Name (client), 00:07:22" (or "(firm)" for another attendee from the firm), copied from the research notes. Fathom's speaker tags can be shifted by a line: the research notes record who actually said it, by context. The build stops on a quote attributed to the seller, and lists who said every quote in the seller prep (never in the deck).
- **Never the same quote twice.** Each line is used once in the deck; the build stops on a repeat or near-repeat.
- **`CLOSING_QUOTE`**: `(quote, said_by)` — a different verbatim client line about the outcome they want (STEP 9B "Client's why" second line, the DBM quote, or `Key prospect quotes` goals), ≤160 chars. `None` when there isn't one that isn't already on the deck — the closing bar is then left off. Never write one yourself.

**Slide 1 — `PROSPECT_QUOTES`**: 0–3 `(topic, quote, tie_line, said_by)` — the most sensitive field in the deck.
- Source: STEP 9B "KPI quotes", then the What You Told Us lines in the BUILD NOTES, then `Key prospect quotes`. Never an AI summary, the seller's words, or our research. Don't repeat the headline quote.
- Only problems or priorities the prospect raised themselves. Copy the words exactly; you may cut from the start or end or mark a middle cut with "…", drop comma-set filler, and capitalize the first letter. Never reword, combine or strengthen. ≤120 chars. Cut the name of anyone from SMB Team the client was speaking to ("…about 60, Jake" → "…about 60") — this applies to the KPI `headline` too.
- `topic`: 1–3 words. `tie_line`: how the proposal answers it, ≤70 chars, connected to a real deliverable — no promised outcomes or dates.
- Apply the What You Told Us "Never include" list in `audit-write.md` (no named staff, personal/health/family matters, partner disputes, financial-distress figures).
- No verbatim transcript: `PROSPECT_QUOTES = []` — the KPI card takes the full width.

**Slide 1 — `CLIENT_WHY`, `COST_OF_INACTION`** (from STEP 9B "Client's why" / "Cost of inaction"): each `(quote, speaker_label, said_by)` — `speaker_label` `""` for the owner, else the attendee's first name; `said_by` per QUOTE RULES. Verbatim client words only, same quote rules as above, ≤140 chars; pick the single strongest line. `None` when STEP 9B says "none on the call" or there's no verbatim transcript — never invent, paraphrase or infer one. Neither is a goal number or a target.

**Optional slide — `STAIRCASE`** (from STEP 9B "Legacy Staircase discussed"): `None` unless the rep walked the client through the staircase on the call. Then `{"current": N or None, "goal": N or None}` with stages 1–8 (1 Law Student, 2 Lawyer, 3 Solo Practitioner, 4 Small Business Manager, 5 Law Firm CEO, 6 Law Firm Owner, 7 Freedom Entrepreneur, 8 Wealth Multiplier). `current` only if the client's position was placed on the call, `goal` only if one was named — otherwise `None` (the slide still shows the staircase and the Abyss, without the marker). Never infer a stage from revenue or team size for this slide.

**Slide 2 — `DIAGNOSIS_TITLE`, `DIAGNOSIS_INTRO`, `DIAGNOSIS`, `DIAGNOSIS_FIX_LINE`** (from STEP 9B "Diagnosis"):
- `DIAGNOSIS_TITLE` names the KPI ("Why Each Case Costs $4,500", "Why Your Caseload Is Shrinking"), ≤40 chars. `DIAGNOSIS_INTRO`: one plain line, ≤90 chars.
- 3–4 causes, biggest first, each specific to this firm — never generic categories like "Lead Generation". One problem per cause: if the call surfaced a second major problem, it gets its own cause rather than being merged into the first (fold minor symptoms into the cause they belong to instead).
  - `title` ≤32 chars, plain words. `metric`: the evidence number exactly as recorded, or `""` for a cause with no number. `metric_label` ≤40 chars.
  - `target`: per DATA RULES, or `None`.
  - `body`: one short line — what's happening (≤80 chars).
  - `source`: where it came from, short ("Discovery call, Oct 26", "Lighthouse test", "Seen live on the call", "Seller, on the call").
- `DIAGNOSIS_FIX_LINE` ≤140 chars: one line pointing to how slide 3 answers the causes, shown after the engine's "How we fix it:" lead-in (don't type that prefix).

**Slide 3 — `PLAN_KICKER`, `PLAN_TITLE`, `PLAN`, `PLAN_NOTE`:**
- `PLAN_KICKER`: the product area ("Paid media and website", "Financial clarity"). `PLAN_TITLE`: the outcome for the KPI, ≤40 chars ("Lower What Each Lead Costs").
- 3–4 actions. Every diagnosed cause must be fixed by at least one action (the build checks).
- **Each action is one layer below the product name, tied to something the client said** — not the product's brochure. Use STEP 9B "Plan inputs":
  - **Fractional CTO / AI Workforce Pro:** the first action is an audit of how work moves through the firm today; then up to three automations, each named after a task the client named on the call ("Automate intake follow-ups", "Draft engagement letters from intake answers").
  - **FCOO and coaching (Elite Coach, Master's Circle, Coach Essentials):** the first concrete process or leadership fix tied to the pain the client stated ("Write the intake SOP so screening doesn't need you", "Weekly leadership meeting with a scorecard").
  - **FCFO / bookkeeping:** what gets built first, tied to what they said they can't see ("Lead-to-signed-case forecast", "Monthly P&L by practice area", "Driver model for hiring decisions").
  - Delivery hasn't approved commitment language: describe what we do first, never a timeline ("in 30 days", "by month 3"), a count we haven't scoped, or a promised outcome. If STEP 9B has no plan input for a product, use its first catalog deliverable and say so in `SELLER_NOTES["plan"]`.
  - `title` ≤34 chars. `fixes`: the DIAGNOSIS number it answers.
  - `actions`: 2–4 bullets, ≤60 chars, each a deliverable of the recommended products (catalog tables in `audit-write.md` and `Design Files/Scoping_and_Ad_Spend_Guide.md` — e.g. words of content, GBP locations, review requests at that tier). Never a deliverable the package doesn't include; never live chat or CRM setup.
  - `metric`: what it moves, 1–4 words — shown in the "What we'll measure" row under the action's name. It must measure **that action** — something the action directly changes (website speed for a site rebuild, cost per lead for ad management, quarterly plans completed or workshops attended for coaching/planning, monthly P&L delivered for FCFO reporting). Never a firm-wide outcome the action doesn't drive on its own (annual revenue, total cases) — if nothing fits with a target or baseline from the call or research, set both `None` and the action is left out of the row. `target`: per DATA RULES, or `None` (then no target line at all). `baseline`: today's value of that metric, exactly as said on the call or measured in research ("24/100"), or `None`.
  - The "What we'll measure" row starts with the slide 1 KPI (today's value). A plan metric that is the KPI again isn't repeated — its target, if any, moves onto the KPI tile. Each other metric shows its target, or with no target its baseline ("Today: 24/100"); a metric with neither is left out of the row. The row has no numbers, so leaving one out never leaves a gap.
- `PLAN_NOTE`: optional line shown after the engine's own "Also included:" lead-in — don't type that prefix (≤160 chars) for other deliverables of the package, or `None`.
- Never put a marketing action on this slide unless a marketing/ads package is part of the recommendation.

**Slide 4 — `STRATEGY_TITLE`, `STRATEGY`:**
- 1–3 pieces in `package_decision.json` order (marketing, then coaching/fractional, then LAW). A single product may be split into pieces (Full Service Marketing → "Get found" + "Get the call"); never add a product that isn't in the package.
- `product`: the catalog product name exactly as in the BUILD NOTES. `title`: 1–3 words. `channels` ≤40 chars.
- `deliverables`: 3–5 catalog deliverables for that product/tier, ≤55 chars each — fractional packages include the Elite Coach group deliverables (see `audit-write.md`).
- `why` ≤110 chars: why this firm needs it, tied to a slide 2 cause or the KPI. No promised results.

**Slide 5 — Your Investment.** Every number on it — each product's price, the monthly total, the one-time setup fees, the year-one total, savings, the ad spend range and the return table — is read by the engine from `package_decision.json` → `investment`, which `scripts/reprice.mjs` computes in code (`scripts/lib/investment.mjs`). You never type a price or figure for this slide. If the build stops with "no investment block", run `node scripts/reprice.mjs [friendly-name]`. You fill only:
- `PRODUCT_LINES` — one deliverables line per product, keyed by the product name exactly as in `package_decision.json` (`marketing_name`, `coaching_name`, `law_name`, without any "(N seats)"), ≤70 chars, items separated by " · " (the engine shows them as a list when there's room). Only catalog deliverables; fractional packages include the Elite Coach group deliverables (see `audit-write.md`). The build stops if a product has no line.
- `AD_SPEND_WHY` — only with a paid-ads package: one short payoff clause, ≤90 chars, from the BUILD NOTES' "why this range" sentence (e.g. "to turn high-intent divorce searches into signed cases"). No calculation basis. `None` when there are no paid ads (the engine then leaves the ad spend and return panels out).
- `CLOSING_QUOTE` — `(quote, said_by)` or `None`, per QUOTE RULES.

---

## GENERATING THE PPTX

1. Copy `Design Files/audit_pptx_template.py` to `[friendly-name]/[FirmName]_[Date]_Proposal.py`
2. Keep the BUILD NOTES block from `/audit-write` STEP 2 at the top, then fill every `# FILL:` placeholder using the extraction rules above and delete the trailing `# FILL…` comments
3. Set `OUTPUT_PATH = "[friendly-name]/[FirmName]_[Date]_Proposal.pptx"`
4. Set `SALES_REP` to the sales rep name
5. Copy `Design Files/smb_team_logo.png` into `[friendly-name]/` so the footer logo renders
6. Verify no `# FILL:` placeholder text remains (the word "FILL" should not appear in any string value). If `AD_SPEND_WHY` was deliberately set to `None` because no paid-ads package was sold, that's expected — not a missed FILL.
7. Before running, diff the copy's layout engine against the master template and confirm there's no output — anything below `LAYOUT ENGINE — DO NOT MODIFY BELOW THIS LINE` must be byte-for-byte identical to `Design Files/audit_pptx_template.py` (this includes `FONT`, every color constant, and every `build_*`/helper function):

```bash
diff <(sed -n '/LAYOUT ENGINE/,$p' "Design Files/audit_pptx_template.py") \
     <(sed -n '/LAYOUT ENGINE/,$p' "[friendly-name]/[FirmName]_[Date]_Proposal.py")
```

8. Run the script:

```bash
python3 "[friendly-name]/[FirmName]_[Date]_Proposal.py"
```

9. Confirm the output prints "Saved: … (5 slides)" — or (6 slides) when `STAIRCASE` is set. If it prints "Deck not built — fix the values above the LAYOUT ENGINE line", fix each listed item and re-run. If it also prints a `WARNING: N field(s) exceeded their character budget…` block, that means the layout engine had to truncate something you filled in — go back and shorten that field's source copy rather than shipping the truncated version. A `NOTE: N field(s) were shrunk to fit their box` block is informational: the engine measured that text against the Poppins font and dropped it a half-point at a time until it fit. That is expected for long firm names and is not an error.
10. Verify the file exists and is not empty:

```bash
wc -c "[friendly-name]/[FirmName]_[Date]_Proposal.pptx"
```

---

## CRITICAL RULES

- Copy prices exactly from the BUILD NOTES / `package_decision.json` — never round or estimate
- Bullet text: one idea, one sentence, 8th-grade reading level, firm-specific — no generic language
- Every number on the story slides (everything before the investment slide) follows the DATA RULES above: said on the call or measured in research, copied exactly, never estimated
- Every quote is verbatim, the client's own, attributed in `said_by`, and used once (QUOTE RULES). The closing quote is a verbatim client line or `None` — never written or reworded
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
