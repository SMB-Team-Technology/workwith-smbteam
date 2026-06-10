# Trigger Audit Pipeline

Creates a trigger JSON for the audit pipeline. Looks up the Fathom recording for the VIP call, populates `fathom_url`, and pushes the file to kick off the pipeline.

## How to invoke

```
/trigger
Firm Name: [Full legal name]
Friendly Name: [lowercase-hyphenated]
URL: [firm website]
Sales Rep: [full name]
Sales Rep Email: [rep@smbteam.com]
Date: [Proposal call date — Month DD, YYYY]
Proposal Call Date: [ISO datetime — e.g. 2026-06-11T20:00:00Z]
Contact Email: [prospect email]
HubSpot Contact ID: [numeric ID]
Deal ID: [numeric deal ID]
Triggered Date: [YYYY-MM-DD — today's date]
Fathom URL: [optional — paste if known, e.g. https://fathom.video/calls/123456]
```

All fields except `Fathom URL` are required.

---

## STEP 1 — Find the Fathom call

If `Fathom URL` was provided by the user, skip to STEP 2.

Otherwise, search for the Fathom recording using the MCP tools:

### Strategy A — Search by name
Use the `search_meetings` MCP tool with the contact's first and last name (and firm name as a fallback keyword). If a match is found, resolve it with `get_recording_by_url` to confirm, then extract the URL.

### Strategy B — List recent meetings by date
Use the `list_meetings` MCP tool. Page through results to find meetings near `Proposal Call Date` (±3 days). Look for a meeting whose title contains the contact name, firm name, or "VIP". Once identified, extract the Fathom URL from the meeting metadata.

### If no match found
Proceed without `fathom_url`. The field will be omitted from the trigger JSON. Warn the user:
> "Could not find a Fathom recording for [contact name]. The pipeline will use the transcript from the trigger file or research from Pass 1 without Fathom data. To add the Fathom recording later, update `fathom_url` in `triggers/audit-research/[friendly-name].json` and re-run Pass 1 via the `rerun-research` workflow."

---

## STEP 2 — Write the trigger JSON

Create the file `triggers/audit-research/[friendly-name].json` with this structure:

```json
{
  "firm_name": "[Firm Name]",
  "friendly_name": "[friendly-name]",
  "url": "[URL]",
  "sales_rep": "[Sales Rep]",
  "sales_rep_email": "[Sales Rep Email]",
  "date": "[Date]",
  "hubspot_contact_id": "[HubSpot Contact ID]",
  "contact_email": "[Contact Email]",
  "deal_id": "[Deal ID]",
  "proposal_call_date": "[Proposal Call Date]",
  "_triggered_date": "[Triggered Date]"
}
```

If a Fathom URL was found or provided, add:
```json
  "fathom_url": "[Fathom URL]"
```

Do NOT include a `transcript` field — the pipeline will fetch it from Fathom automatically using `fathom_url`.

---

## STEP 3 — Commit and push

```bash
git add triggers/audit-research/[friendly-name].json
git commit -m "Trigger audit: [Firm Name]"
git push origin main
```

After pushing, confirm: "Audit pipeline triggered for [Firm Name]. The pipeline will run Pass 1 (research), Pass 1.5 (package selection), and Pass 2+3 (report + PPTX). Expect results in ~30–60 minutes."

If `fathom_url` was not found, add: "No Fathom recording was found — Pass 1 will research without transcript data. If you find the call URL in Fathom later, add it to the trigger file and re-run research."
