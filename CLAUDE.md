# SMB Team — Law Firm Growth Audit Repository

This repository stores the Law Firm Growth Audit proposal decks (and their research) generated for prospective SMB Team clients.

## Session Initialization — REQUIRED

At the start of every session, before doing anything else, run:

```bash
git pull origin main
```

This ensures you have the latest version of all slash commands and configuration files before proceeding.

## Purpose

Each audit produces a 5-slide proposal PowerPoint (6 with the optional Legacy Staircase slide) for a prospective SMB Team client, built by the `/audit-write` command (Pass 2) from the research notes and `package_decision.json`, then uploaded to the HubSpot file manager and emailed to the seller.

The "Growth, Profit & Freedom Roadmap" website (`index.html`, `sections/`) and the Sales Companion PDF are **retired**. New builds never create them. Older firm folders still contain them — do not edit or read them for a new build.

## Folder Structure

```
Design Files/                          ← templates, read-only, never modified
├── audit_pptx_template.py             ← the deck template (used)
├── smb_team_logo.png, fonts/          ← used by the deck
├── Scoping_and_Ad_Spend_Guide.md      ← reference
└── section_*.html, audit_styles.css, audit_master_assembly.html,
    SMB_Team_Audit_Agent_System_Prompt.txt, sales_companion_template.py
                                       ← retired website / PDF templates (not used)

[friendly-name]/                       ← at the repo root
├── [FirmName]_[Date]_Research_Notes.txt
├── package_decision.json
├── proposal_review.json               ← Slack review-thread state
├── [FirmName]_[Date]_Proposal.py      ← filled deck script; its BUILD NOTES record the workings
├── [FirmName]_[Date]_Proposal.pptx    ← the deliverable
└── smb_team_logo.png
```

Each firm gets its own folder at the repo root, named with a lowercase hyphenated friendly name (e.g. `mandel-law-firm/`, `angel-law/`).

**Design Files are permanent templates. Never modify them.** Claude Code reads from them and writes working copies to the firm's folder.

## How to Run an Audit

Use the `/audit` slash command (research + deck), or `/audit-research` then `/audit-write`. In the pipeline, `audit-pipeline.yml` and `audit-write.yml` run them. See `README.md` for the pipeline and test mode.

## Important Notes

- Never modify a committed deck without noting the change in the commit message
- Do not commit partial or incomplete audits — only run `/audit` when you have all required inputs (firm name, URL, sales rep, date, revenue, practice area, and transcript)
