# SMB Team — Law Firm Growth Audit Repository

This repository stores completed Law Firm Growth Audit reports generated for prospective SMB Team clients.

## Session Initialization — REQUIRED

At the start of every session, before doing anything else, run:

```bash
git pull origin main
```

This ensures you have the latest version of all slash commands and configuration files before proceeding.

## Purpose

Each audit is a branded HTML report produced by the `/audit` slash command. Reports are generated from browser research and a discovery call transcript, then committed directly to this repo.

## Folder Structure

```
SMB Team Client Audit/
└── Outputs/
    └── [FirmName]_[Date]_Growth_Audit.html
```

File naming convention: `[FirmName]_[Date]_Growth_Audit.html`
- Spaces in firm name replaced with underscores
- Date in MMDDYYYY format
- Example: `Mandel_Law_Firm_04102026_Growth_Audit.html`

## How to Run an Audit

Use the `/audit` slash command. It handles research, report generation, and git push end to end. See `.claude/commands/audit.md` for full usage.

## Important Notes

- Never modify completed audit HTML files after they are committed without noting the change in the commit message
- The `Outputs/` folder is the only place audit reports should be saved
- Do not commit partial or incomplete audits — only run `/audit` when you have all required inputs (firm name, URL, sales rep, date, revenue, practice area, and transcript)
