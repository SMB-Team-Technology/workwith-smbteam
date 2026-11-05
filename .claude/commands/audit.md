# SMB Team — Proposal Audit (research + deck)

Run the full proposal audit for a prospective client end to end: browser research, package selection and the 3-slide proposal deck, then commit it. The "Growth, Profit & Freedom Roadmap" website and the Sales Companion PDF are retired — the deck is the only output.

## How to invoke

```
/audit
Firm Name: [Full legal name of the firm]
Friendly Name: [lowercase-hyphenated, e.g. angel-law or mandel-law-firm]
URL: [firm website URL]
Sales Rep: [rep's full name]
Date: [Month DD, YYYY — e.g. April 13, 2026]
Revenue: [annual revenue, e.g. $450K]
Practice Area: [e.g. Personal Injury, Criminal Defense, Family Law]
Market Competitiveness: [Low / Medium / High]
Transcript: [paste full discovery call transcript here]
Package Criteria: [optional — include if ready to complete the recommendation section]
```

All fields except `Package Criteria` are required.

**Package Override** (optional): If you have already agreed on specific packages with the prospect, include the phrase `sales override` followed by the package names anywhere in your input to bypass automatic package selection. Pricing will still be pulled from the official tables — never estimated.
Example: `sales override: Growth marketing + Master's Circle + FCOO Advisor`

**Friendly Name rules:** lowercase, hyphens only, no spaces or underscores. Examples: `angel-law`, `mandel-law-firm`, `smith-injury-law`.

---

## STEP 1 — RESEARCH

Run `/audit-research` with the Firm Name, Friendly Name, URL, Sales Rep, Date, Revenue, Practice Area, Market Competitiveness and Transcript above. It saves `[friendly-name]/[FirmName]_[Date]_Research_Notes.txt`.

## STEP 2 — PACKAGE SELECTION

```bash
node scripts/select-package.mjs [friendly-name]
```

This writes `[friendly-name]/package_decision.json`. If you gave a `sales override`, apply it the way the Slack "propose changes" reply does: set the product name fields (`marketing_name`, `coaching_name`, `law_name`, `law_seats`) to the catalog names, add a `"Seller override: …"` entry to `selection_notes`, then run `node scripts/reprice.mjs [friendly-name]` — never type a price yourself.

## STEP 3 — BUILD THE DECK

Run `/audit-write` with the same Firm Name, Friendly Name, Sales Rep and Date. It applies the package rules, does the ad spend and ROI workings, builds `[friendly-name]/[FirmName]_[Date]_Proposal.pptx` from `Design Files/audit_pptx_template.py`, and commits to the current branch.

**Design Files are read-only.** Never modify, overwrite, move, rename, or delete any file inside `Design Files/`. Do not use the retired website templates (`section_*.html`, `audit_master_assembly.html`, `audit_styles.css`, `SMB_Team_Audit_Agent_System_Prompt.txt`) or `sales_companion_template.py`.

Report the commit hash.
