# SMB Team — Audit Write (Pass 2)

Fill in all section templates, assemble the final HTML report, and push to GitHub. Run this after `/audit-research` has completed and the research notes file exists.

## How to invoke

```
/audit-write
Firm Name: [Full legal name of the firm]
Friendly Name: [same value used in /audit-research, e.g. angel-law]
Sales Rep: [rep's full name]
Date: [same date used in /audit-research — Month DD, YYYY]
Package Criteria: [optional — include if ready to complete the recommendation section]
```

Revenue, Practice Area, and Market Competitiveness are read from the research notes file — do not re-enter them here.

---

## STEP 0 — READ THE SYSTEM PROMPT AND RESEARCH NOTES

Before doing anything else, read both of these files in order:

1. `Design Files/SMB_Team_Audit_Agent_System_Prompt.txt`
2. `[friendly-name]/[FirmName]_[Date]_Research_Notes.txt`

If the research notes file does not exist, stop immediately and tell the user to run `/audit-research` first.

---

## YOUR ONLY JOB IN THIS COMMAND

Complete **Pass 2 — Verify Then Write** from the system prompt. Use only data from the research notes file — do not open a browser. Do not re-run any research.

---

## FILE PATH OVERRIDES

- **Design Files folder** → `Design Files/` at the repo root — read-only, never modify
- **Working section files** → write filled-in copies to `[friendly-name]/sections/`
- **Final assembled output** → `[friendly-name]/index.html`
- **CSS** → copy `Design Files/audit_styles.css` to `[friendly-name]/audit_styles.css` at assembly time

Create `[friendly-name]/sections/` if it does not already exist.

---

## WHAT TO DO

Work through every section file one at a time. Complete and save each before starting the next. Do not batch multiple sections into a single write operation.

**STEP A — section_01_cover.html**
Read `Design Files/section_01_cover.html`. Fill in all `<!-- FILL: -->` placeholders. Save the completed file to `[friendly-name]/sections/section_01_cover.html`. Verify it was saved before continuing.

**STEP B — section_02_toc.html**
Read `Design Files/section_02_toc.html`. Fill in all placeholders. Save to `[friendly-name]/sections/section_02_toc.html`. Verify saved.

**STEP C — section_03_firm_overview.html**
Read `Design Files/section_03_firm_overview.html`. Fill in all placeholders. Uncomment the correct staircase image for the assigned stage and delete the others. Save to `[friendly-name]/sections/section_03_firm_overview.html`. Verify saved.

**STEP D — section_04_about_smb.html**
Read `Design Files/section_04_about_smb.html`. This file is static — copy it as-is to `[friendly-name]/sections/section_04_about_smb.html`. No changes needed. Verify saved.

**STEP E — section_05_growth_health.html**
Read `Design Files/section_05_growth_health.html`. Fill in all placeholders — traffic light colors, pillar findings, DBM sentences, urgency score, urgency sentence, competitor cards. Save to `[friendly-name]/sections/section_05_growth_health.html`. Verify saved.

**STEP F — section_06_lead_generation.html**
Read `Design Files/section_06_lead_generation.html`. Fill in all placeholders — lead gen intro, website findings with actual PageSpeed scores, all local SEO findings, Google Ads findings per practice area, LSA findings, Meta Ads findings. Delete any blind spot divs that do not apply. Save to `[friendly-name]/sections/section_06_lead_generation.html`. Verify saved.

**STEP G — section_07_08_09_intake_team_profit.html**
Read `Design Files/section_07_08_09_intake_team_profit.html`. Fill in all three sections — Intake, Team, Profit — in order. For each: intro sentence, traffic light, transcript quote or delete if none, problem bullets, blind spot or delete if not applicable, positives or delete if nothing genuine, gap bullets, DBM closing. Save to `[friendly-name]/sections/section_07_08_09_intake_team_profit.html`. Verify saved.

**STEP H — section_10_whats_possible.html**
Read `Design Files/section_10_whats_possible.html`. Fill in all placeholders — firm name, bridge text, three transformation cards tied to DBM. Save to `[friendly-name]/sections/section_10_whats_possible.html`. Verify saved.

**STEP I — section_11_next_steps.html**
Read `Design Files/section_11_next_steps.html`. Fill in all placeholders — minimum 6 quick win cards, all 8 recommendation blocks in order per the system prompt. Apply package eligibility logic from Step 11 of the system prompt. If `Package Criteria` was not provided, insert the clearly marked placeholder instead of the recommendation section. Save to `[friendly-name]/sections/section_11_next_steps.html`. Verify saved.

---

## ASSEMBLY

1. Read `Design Files/audit_master_assembly.html` — do not modify it
2. Build a new file by replacing each `<!-- INSERT SECTION XX CONTENT HERE -->` comment with the full HTML content of the corresponding file from `[friendly-name]/sections/`
3. Confirm the `<link rel="stylesheet" href="audit_styles.css">` tag is present and the href is exactly `audit_styles.css`
4. Save the assembled file as `[friendly-name]/index.html`
5. Copy `Design Files/audit_styles.css` to `[friendly-name]/audit_styles.css`
6. Verify both files exist and are not empty

---

## FINAL CHECK

Before committing, verify:
- All 11 sections are present in the assembled file
- No `<!-- FILL: -->` placeholder text remains anywhere in the output
- No inline styles or `<style>` blocks were introduced
- Only class names from `audit_styles.css` are used
- All image URLs are intact (not modified)
- The `audit_styles.css` file is present in `[friendly-name]/`

Fix anything that fails before committing.

---

## COMMIT AND PUSH TO MAIN

```bash
git checkout main
git add "[friendly-name]/"
git commit -m "Add growth audit: [Firm Name] ([Date])"
git push origin main
```

Always commit directly to main — never create a branch. Confirm the push succeeded and report the commit hash.
