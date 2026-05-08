# SMB Team — Growth, Profit, and Freedom Roadmap

Run a full Growth, Profit, and Freedom Roadmap for a prospective client, assemble the branded HTML report from design templates, and push it to GitHub.

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

**Friendly Name rules:** lowercase, hyphens only, no spaces or underscores. Examples: `angel-law`, `mandel-law-firm`, `smith-injury-law`.

---

## STEP 0 — READ THE SYSTEM PROMPT

Before doing anything else, read the full system prompt from:

```
Design Files/SMB_Team_Audit_Agent_System_Prompt.txt
```

Follow every instruction in that file exactly. The sections below override or extend specific parts of it for this repo's file structure.

---

## FILE PATH OVERRIDES

The system prompt references a "project folder" and a "Design Files subfolder." In this repo, those map as follows:

- **Design Files folder** → `Design Files/` at the repo root
- **Research notes file** → `[friendly-name]/[FirmName]_[Date]_Research_Notes.txt`
- **Working section files** → write filled-in copies to `[friendly-name]/sections/` — do NOT write back into `Design Files/`
- **Final assembled output** → `[friendly-name]/index.html`
- **CSS file** → copy `Design Files/audit_styles.css` to `[friendly-name]/audit_styles.css` at assembly time so the relative path in the HTML resolves correctly

Create `[friendly-name]/` and its subdirectories at the repo root if they do not already exist.

**Design Files are read-only.** Never modify, overwrite, move, rename, or delete any file inside `Design Files/`. Read from them. Write working copies elsewhere.

---

## ASSEMBLY OVERRIDE (replaces Steps J and K in the system prompt)

When assembling the final output:

1. Open `Design Files/audit_master_assembly.html` — read it, do not modify it
2. Build a new file by replacing each `<!-- INSERT ... CONTENT HERE -->` comment with the full HTML content of the corresponding completed working section file from `[friendly-name]/sections/`. This includes the executive summary slot (`<!-- INSERT EXECUTIVE SUMMARY CONTENT HERE -->`).
3. In the `<link rel="stylesheet" href="audit_styles.css">` tag, confirm the href is `audit_styles.css` — this resolves correctly because the CSS will be copied to the same folder
4. Save the assembled file as `[friendly-name]/index.html`
5. Copy `Design Files/audit_styles.css` to `[friendly-name]/audit_styles.css`
6. Verify the output file exists and is not empty before proceeding

---

## COMMIT AND PUSH TO MAIN

After the final output is confirmed saved:

```bash
git checkout main
git add "[friendly-name]/"
git commit -m "Add growth audit: [Firm Name] ([Date])"
git push origin main
```

Replace `[friendly-name]`, `[Firm Name]`, and `[Date]` with the actual values used. Always commit directly to main — never create a branch. Confirm the push succeeded and report the commit hash.
