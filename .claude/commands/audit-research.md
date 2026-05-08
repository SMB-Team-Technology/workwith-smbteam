# SMB Team — Audit Research (Pass 1)

Run all browser research for a Growth, Profit, and Freedom Roadmap and save a verified research notes file. Does not generate any HTML. Run this first, then run `/audit-write` when complete.

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

## SETUP

Create `[friendly-name]/` at the repo root if it does not exist. The research notes file saves to `[friendly-name]/[FirmName]_[Date]_Research_Notes.txt`.

Save after each major section below — do not wait until the end. If research is interrupted, completed sections are preserved.

---

## TRANSCRIPT-FIRST RULE — READ BEFORE OPENING ANY BROWSER TAB

The discovery call transcript is ground truth. Before searching for any data point, check whether the transcript already provides it. If yes, use it directly — do not open a browser to verify.

**Trust the transcript for:** practice areas, revenue, revenue goal, team size and roles, average case value, close rate, current lead sources, whether ads have ever been run, ad budgets and platforms, hiring plans, technology in use, pain points, and DBM.

**Only verify these live — they change too frequently to trust a transcript:**
- Google review count and star rating for the firm
- Competitor review counts and star ratings
- Whether ads are currently running right now
- PageSpeed scores
- Local 3-pack positions

---

## ADS FRAMING RULE

Never state with certainty that a firm is not running ads unless the prospect confirmed it on the call. When ads are not visible, say the firm "does not appear to be running ads for this search" or "may be getting outbid by competitors." Always frame as an opportunity gap. Never write "You are not currently running ads."

---

## STEP 1 — WEBSITE RESEARCH

Navigate to the firm's URL. Observe and record:

- Website URL confirmed live: [yes/no]
- Last redesign date or estimated age: [actual observation]
- Mobile responsive: [yes/no/not observed]
- Homepage headline: [exact text]
- CTA above fold: [yes/no — what does it say]
- Contact form location: [above fold/buried/not found]
- Live chat present: [yes/no]
- Attorney bio present: [yes/no]
- Video present: [yes/no]
- Blog present: [yes/no — last post date if yes]

Then navigate to **pagespeed.web.dev** and run the firm's URL. Record the exact scores:
- PageSpeed mobile score: [actual number — must be a real number, never an estimate]
- PageSpeed desktop score: [actual number — must be a real number]

If PageSpeed tool fails, try again. The actual numbers must be recorded.

**→ SAVE research notes now with website section complete.**

---

## STEP 2 — GOOGLE BUSINESS PROFILE

Search for the firm by name on Google. Record:

- GBP found: [yes/no]
- Star rating: [actual number]
- Total review count: [actual number — verify live]
- Most recent review date: [actual date]
- Primary category: [exact category listed]
- Photos active: [yes/no]
- Posts active: [yes/no]

---

## STEP 3 — LOCAL 3-PACK SEARCHES

For **each practice area** the firm handles, run a minimum of 3 keyword searches. Record results for every search.

```
Practice Area 1: [name]
- Search 1 "[keyword]": firm appears [yes/no] — competitors in pack: [name, review count], [name, review count], [name, review count]
- Search 2 "[keyword]": firm appears [yes/no] — competitors in pack: [name, review count], [name, review count], [name, review count]
- Search 3 "[keyword]": firm appears [yes/no] — competitors in pack: [name, review count], [name, review count], [name, review count]

Practice Area 2 (if applicable): [name]
- Search 1 "[keyword]": firm appears [yes/no] — competitors in pack: [name, review count], [name, review count], [name, review count]
- Search 2 "[keyword]": firm appears [yes/no] — competitors in pack: [name, review count], [name, review count], [name, review count]
- Search 3 "[keyword]": firm appears [yes/no] — competitors in pack: [name, review count], [name, review count], [name, review count]
```

---

## STEP 4 — COMPETITOR REVIEW COUNTS

Verify every number live before recording. Never cite a competitor as having more reviews than the prospect if the prospect actually has more.

```
- Competitor 1: [name] — reviews: [actual number verified live] — rating: [actual number]
- Competitor 2: [name] — reviews: [actual number verified live] — rating: [actual number]
- Competitor 3: [name] — reviews: [actual number verified live] — rating: [actual number]
```

---

## STEP 5 — DIRECTORY LISTINGS

Check Avvo, Justia, FindLaw, Yelp, and at least two other relevant directories. Note any NAP inconsistencies. Note whether the firm has geo-targeting landing pages for surrounding cities.

**→ SAVE research notes now with GBP, local SEO, and directory sections complete.**

---

## STEP 6 — GOOGLE ADS

Search Google for **each practice area** plus city. Run separate searches per practice area. For each:

```
Practice Area 1: [name]
- Firm ads observed: [yes — exact headline and description / not observed]
- Named local competitors running ads: [name — ad copy summary], [name — ad copy summary]

Practice Area 2 (if applicable): [name]
- Firm ads observed: [yes — exact headline and description / not observed]
- Named local competitors running ads: [name — ad copy summary], [name — ad copy summary]
```

Only use specific named local firms as competitors. Never use national firms or generic categories.

---

## STEP 7 — LOCAL SERVICE ADS

Search for the firm's primary practice area plus city. Examine the top of the results page.

```
- Firm appears in LSA: [yes/no/not observed]
- Google Screened: [yes/no/not observed]
- LSA review count: [actual number if applicable]
- Named local competitors in LSA: [name, review count], [name, review count]
```

---

## STEP 8 — META ADS

Navigate to https://www.facebook.com/ads/library/ and search for the firm's name.

```
- Firm has active ads: [yes — count, formats, duration / not observed]
- Named local competitor 1: [name] — active ads: [count, format, how long running]
- Named local competitor 2: [name] — active ads: [count, format, how long running]
```

Only use specific named local firms. Never use national brands.

**→ SAVE research notes now with all ads sections complete.**

---

## STEP 9 — TRANSCRIPT EXTRACTION

Extract from the discovery call transcript. Trust these values exactly as stated — do not search for them:

```
- Practice areas confirmed: [list all]
- Current lead sources: [exact quotes if available]
- Ads ever run: [yes/no — what platform, what budget, what result]
- Team size: [number and roles]
- Annual revenue: [stated figure or range]
- Revenue goal: [stated figure — if not stated, note "not stated, use 2x current revenue"]
- Average case value: [stated figure or practice area]
- Current close rate: [stated figure or "not stated — default to 15%"]
- Number of locations: [stated figure or "1 if not mentioned"]
- Spanish campaign needed: [yes/no]
- Dominant buying motive: [exact quote or closest inference]
- Any profitability claims made by prospect: [exact quotes only — if none stated, write "none stated"]
- Any claims about case types or practice areas: [exact quotes only]
```

**Dominant buying motive:** Do not accept surface answers. "More money" and "more clients" are not DBMs. The real answer is what the money or growth will allow the owner to do personally — coach their kid's team, retire, take a vacation, stop missing weekends. If not clearly stated, infer from context. Most fall into: (1) firm that runs itself so they have more time, (2) grow and sell, (3) scale and dominate.

---

## STEP 10 — COMPETITIVE URGENCY SCORE

Assign a score from 1 to 10 based on how aggressively local competitors are marketing compared to this firm.

- 1–3: Market is relatively quiet
- 4–6: Competitors have meaningful advantages in one or more areas
- 7–9: Competitors are dominating multiple channels
- 10: Competitors running comprehensive campaigns across all channels; firm is largely invisible

Record: score, 2–3 named specific local competitor threats with reasons, and the matching dynamic sentence below:

- **Score 1–3:** "A score of [X] means no single competitor is dominating your market yet — but that will not last forever. The firms that win markets do so by moving first. Getting your systems in place now means you set the standard before someone else does."
- **Score 4–6:** "A score of [X] means competitors have meaningful advantages in one or more areas and are pulling ahead. You are not invisible yet — but the window to close the gap is narrowing. Every month without action is a month they extend their lead."
- **Score 7–10:** "A score of [X] means competitors are actively dominating multiple channels in your market and the gap is getting wider every month you wait. This is not a future problem — it is a right now problem."

**→ SAVE final research notes file.**

---

## PASS 2 — VERIFICATION CHECKLIST

Before finishing, check every item. Fix anything unchecked before saving.

- [ ] Every number in the notes matches actually observed data
- [ ] Every competitor review count has been verified live — prospect does not have more reviews than any competitor cited as "dominating"
- [ ] Every ad section covers ALL practice areas listed in the transcript
- [ ] No section says "you are not running ads" — only "does not appear to be running" or "not observed"
- [ ] No profitability or business claim appears unless it came from the transcript
- [ ] No competitor reference uses generic labels — only specific named local firms
- [ ] PageSpeed scores are real numbers — not estimates
- [ ] DBM is recorded (exact quote or clear inference)
- [ ] Revenue goal is recorded (or flagged if not stated)
- [ ] Close rate is recorded (stated or defaulted to 15%)
- [ ] Average case value is recorded (stated or practice area default noted)

---

## COMMIT AND CONFIRM

```bash
git checkout main
git add "[friendly-name]/[FirmName]_[Date]_Research_Notes.txt"
git commit -m "Add research notes: [Firm Name] ([Date])"
GIT_TERMINAL_PROMPT=0 git push origin main
git log -1 --format="%H %s"
```

Report the commit hash. Then tell the user: **research complete — run `/audit-write` to generate the report.**


IMPORTANT NOTE:

Git vs. GitHub MCP — when to use which (Claude Code on the Web)

Sessions running on Claude Code on the Web have two distinct GitHub paths and should use both, not just one:

Local git CLI for git-shaped operations: git pull, git fetch, git add, git commit, git push, git diff, etc. The session's harness sets up local clones at /home/user/<repo>/ with the origin remote pointing at a local HTTP proxy (http://local_proxy@127.0.0.1:<port>/git/...). That proxy is authenticated, sanctioned, and identical to what the MCP server is using under the hood. You can git push normally. This is the right path for any change that involves committing files — especially large ones, where the GitHub MCP write tools (create_or_update_file, push_files) hit a stream-idle timeout above ~14–25 KB of inline file content per call.

GitHub MCP tools (prefixed mcp__github__) for GitHub-platform operations that aren't a git command: opening / commenting on / reviewing PRs, reading issues, querying CI status, browsing repo metadata, etc. These are the only path for those operations since you don't have gh / hub / direct REST access.

Anti-pattern to avoid: routing every file edit through mcp__github__create_or_update_file because the system prompt says "use the GitHub MCP server tools for ALL GitHub interactions." That phrasing was written to differentiate from forbidden tools likeghCLI, and it's been causing sessions to stall on stream timeouts when committing modest-sized files. Read it as: use MCP for GitHub-the-platform operations (PRs, issues, comments, CI), not for git-the-tool operations (commits, pushes, pulls). The session's own setup already points you at how to commit — see the "Git Operations" block in your system prompt for the canonical git push -u origin <branch> recipe.

Quick check at start of session:

ls /home/user/                        # see what repos are cloned
cd /home/user/<repo> && git remote -v # see the proxy URL
git fetch origin                       # confirm push/pull plumbing is live
If git fetch works, git push will work too — use it for commits.
