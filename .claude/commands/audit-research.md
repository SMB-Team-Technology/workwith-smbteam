# SMB Team — Audit Research (Pass 1)

Run all browser research for a Law Firm Growth Audit and save a verified research notes file. Does not generate any HTML. Run this first, then run `/audit-write` when complete.

## How to invoke

```
/audit-research
Firm Name: [Full legal name of the firm]
Friendly Name: [lowercase-hyphenated, e.g. angel-law]
URL: [firm website URL]
Sales Rep: [rep's full name]
Date: [Month DD, YYYY — e.g. April 13, 2026]
Transcript: [paste full discovery call transcript here — or write "none" if not yet available]
```

**Friendly Name rules:** lowercase, hyphens only, no spaces or underscores.

---

## STEP 0 — READ THE SYSTEM PROMPT

Before doing anything else, read the full system prompt from:

```
Design Files/SMB_Team_Audit_Agent_System_Prompt.txt
```

Then return here and follow the instructions below. The sections below override specific parts of the system prompt.

---

## YOUR ONLY JOB IN THIS COMMAND

Complete **Pass 1 — Research and Verification** from the system prompt only. Do not fill in any section files. Do not touch any HTML. Do not assemble anything. Research and notes only.

---

## FILE PATH OVERRIDES

- **Design Files folder** → `Design Files/` at the repo root
- **Research notes file** → save to `[friendly-name]/[FirmName]_[Date]_Research_Notes.txt` at the repo root

Create the `[friendly-name]/` folder at the repo root if it does not already exist.

---

## WHAT TO DO

1. Read the system prompt from `Design Files/SMB_Team_Audit_Agent_System_Prompt.txt`
2. Complete every item in the **Pass 1 — Research and Verification** section:
   - All website data (including actual PageSpeed scores from pagespeed.web.dev — real numbers required)
   - Google Business Profile
   - Local 3-pack searches (minimum 3 searches per practice area)
   - Competitor review counts (verified live)
   - Google Ads (per practice area)
   - Local Service Ads
   - Meta Ads (Facebook Ad Library)
   - Transcript data points extracted from the provided transcript
3. Save the completed research notes file to `[friendly-name]/[FirmName]_[Date]_Research_Notes.txt`
4. Verify the file was saved and is not empty

---

## WHEN RESEARCH IS COMPLETE

Run the **Pass 2 verification checklist** from the system prompt. Check every item. Fix anything unchecked before saving.

Then commit the research notes to main:

```bash
git checkout main
git add "[friendly-name]/[FirmName]_[Date]_Research_Notes.txt"
git commit -m "Add research notes: [Firm Name] ([Date])"
git push origin main
```

Confirm the push succeeded and report back. Then tell the user: **research complete — run `/audit-write` to generate the report.**
