# SMB Team — proposal audit pipeline

Builds a 5-slide proposal deck (6 with the optional Legacy Staircase slide) (`<firm>/<FirmName>_<Date>_Proposal.pptx`) for each prospective client, uploads it to the HubSpot file manager, and emails it to the seller.

The per-client "Growth, Profit & Freedom Roadmap" websites (`workwith.smbteam.com/<firm>`) and the Sales Companion PDF are retired: new builds no longer create `index.html`, `sections/` or a PDF. Older client folders still contain them, and GitHub Pages (`CNAME`, root `index.html`) still serves those existing pages.

## Pipeline

1. **Pass 1 — research** (`audit-pipeline.yml`, `.claude/commands/audit-research.md`): web research and transcript extraction into `<firm>/<FirmName>_<Date>_Research_Notes.txt`, then package selection (`scripts/select-package.mjs` → `<firm>/package_decision.json`), then a review request in Slack.
   Package selection also computes the investment (`scripts/lib/investment.mjs`): ad spend range, return projection, monthly and year-one totals, from the package and the research notes' "Investment inputs" lines. `scripts/reprice.mjs` recomputes it after every package change and before every deck build, and the deck's investment slide reads it from `package_decision.json` — no number on that slide is typed by hand.
2. **Seller review** (`slack-proposal-response.yml`): the seller locks in or changes the package in the Slack thread. Lock-in writes `triggers/audit-write/<firm>.json`.
3. **Pass 2 — deck** (`audit-write.yml`, `.claude/commands/audit-write.md` + `audit-pptx.md`): package, price, ad spend and ROI workings, recorded as BUILD NOTES in `<firm>/<FirmName>_<Date>_Proposal.py`, which builds the `.pptx`.
4. **Delivery** (`audit-write.yml`): `scripts/upload-proposal-to-hubspot.mjs` uploads the deck to the HubSpot file manager ("AI Proposals" folder, public but not indexable; re-runs replace the same file, so the link never changes). The link is written to the contact's `growth_profit_and_freedom_roadmap` property, posted in the Slack thread and put in the seller email, which also attaches the `.pptx`.

Edits after the build go through `slack-change-handler.yml`; `resend-audit-email.yml` re-uploads and re-sends.

## Test mode

Pushing a `triggers/audit-write/<firm>.json` to an `audit-test/**` branch runs `audit-write.yml` in test mode: it commits only to that branch, emails only carolyn.webb@smbteam.com, and skips the HubSpot upload and contact write and all Slack posts. Add `"test_no_email": true` to skip that email (a research test trigger passes it on to the chained deck build). Add `"test_upload": true` to the trigger to also upload the deck to a separate "AI Proposals TEST" folder (no contact write). `resend-audit-email.yml` run from a non-`main` ref is test mode too.

Research has a test mode too: pushing a `triggers/audit-research/<firm>.json` to an `audit-test/**` branch runs `audit-pipeline.yml` on that branch. It fetches the Fathom transcript, runs Pass 1 (including STEP 9B) and package selection, and commits only to that branch. It posts nothing to Slack and writes no `proposal_review.json`. Add `"test_chain_write": true` to the trigger to have it write the `audit-write` trigger itself, standing in for the seller's lock-in, so the deck builds in test mode right after (needs the `GH_PAT` secret). A `"package"` in the trigger still sets the seller's package.

## HubSpot token scopes

The `HUBSPOT_TOKEN` private app needs `files` (file manager upload/replace/search) and `crm.objects.contacts.write` (contact property), plus the read scopes the research scripts already use.

## Tests

```
node --test scripts/tests/*.test.mjs
```
