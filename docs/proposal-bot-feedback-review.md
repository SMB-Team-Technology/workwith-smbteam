# Proposal Bot: Feedback Review Notes

Working notes from going through Vanessa's feedback email (Sept 2026), one topic at a time. These notes are for discussion. The only code change made from them so far is the call-focus fix for the starting package (Oct 1). Last updated Oct 1, 2026.

## Context
- Sellers are holding off on using the bot's proposals until more updates are made.
  - None of the 16 drafts posted since Sep 15 has been locked in and built.
- Since Oct 1, the pipeline runs on `claude-sonnet-5-5` (Eli's update, PR #42).

## Decisions made
- **Seller always wins.**
  - When a seller locks in a package, build it even if it breaks an eligibility rule. Examples of rules this covers:
    - revenue floors
    - "must pair with coaching"
    - FCOO under $500K
    - AI products under $400K
    - "stop" under $250K
    - unknown revenue
  - Prices still come only from the official tables, never estimated.
- **Heads-up in Slack.**
  - When a seller's choice breaks a rule, post one information-only line, e.g. "FCOO normally needs $500K+, building anyway."
  - It never blocks the build.
- **Lare and Morales:** leave them for now.

## Topic 1: Package selection didn't run (McLean, Gaydos, Fowles)
**Already done**
- Sep 14: the package decision is now saved, and it rebuilds itself when a seller replies.
- Sep 15: a Slack failure notice is posted if research didn't finish.
- Gaydos and Fowles both recovered, and every run since Sep 14 has saved its decision.

**Still open**
- **Morales (Sep 28, call Oct 7) failed silently.** The research step crashed, and the failure alert only fires when research finishes without saving anything. It doesn't fire when the step crashes.
- **Lare (Sep 14, call Oct 6) is in limbo.** The Slack post went out, but saving the review record failed, so replies in that thread are ignored.
- McLean and 21 other drafts from before Sep 14 are still "pending" with no saved decision.
- There's no automatic retry. Fowles' first run stopped because PageSpeed rate-limited it.

**Ideas**
- Alert on any research failure, including crashes.
- Retry once automatically.
- Don't let a PageSpeed failure stop the whole run.
- Close out stale pending proposals.

## Topic 2: Audit-write didn't finish (Kareem Abdo, Hiller, Beyond Business Contracts)
**Cause:** every failure was a seller-chosen package that broke a rulebook rule. The AI runs non-interactively, so it stopped instead of asking.

| Firm | Seller's choice | Rule it broke |
|---|---|---|
| Kareem Abdo | Paid Ads Starter standalone | "Ads-only must pair with coaching" (the fix was approved but never merged); also only $40K revenue |
| Hiller | FCOO Advisor standalone | FCOO needs $500K+ (firm at $350K) |
| Beyond Business Contracts | Elite Coach + AI Accelerator | AI products need $400K+ (firm at $250K); Carolyn approved an exception and the build succeeded |
| Feldman | Web + SEO Growth standalone | "Web + SEO must pair with coaching" |
| The Legal Dad | Starter + Elite Coach | No transcript, so revenue was a default; the rulebook says stop |

**Already done**
- Sep 17: Slack now shows why a build stopped.

**Still open**
- The Paid Ads standalone fix (branch `claude/zealous-johnson-qsl1m3`) is unmerged.
- Kareem Abdo, Hiller, Feldman and The Legal Dad were never rebuilt.
- The "seller always wins" decision still needs to be built into the rulebook.

## Topic 3: Understanding seller replies
**How it works today**
- The bot only responds inside the original thread, and only while the proposal is "pending."
- Replies are silently ignored if the proposal is locked, built or failed, or if the thread doesn't match a firm.
- The AI sorts each reply into one of 3 intents: lock it in, ask why, or change.

**Why Vanessa's examples failed**
- **"approve"** should work. Blevins (Aug 25) was stuck before the Sep 14 fix and was never built, which also likely explains the empty resent email.
- **"for Allen Blevins"**: the bot identifies the firm only from the thread, never from a name in the message.
- **"please email me this"**: there's no email intent, and replies are ignored once a proposal is built.
- **"No ready to propose yet"**: there's no hold or not-yet intent.
- **Construction law ad spend**: construction law isn't in any rule file, so the bot falls back to a generic $3,000 minimum.
- **Dan's "change and build"**: by design, a change always needs a second "lock it in."

**Ideas**
- Add intents for "build with this change," "hold / not ready," and "email me / resend."
- Always respond, even when the bot can't act.
- Cover practice areas the rules don't include.
- Pin a short "what you can say to the bot" guide in the channel.

## Open questions for Carolyn
- If a seller picks a product with no standalone price in the tables, what should the bot charge?
- Are Kareem Abdo, Hiller, Feldman and The Legal Dad still live deals that need rebuilding?
- After a seller requests a change, should the bot build right away, or keep waiting for "lock it in"?

## Questions for Vanessa and Sales
- Which eligibility rules are still real policy? Even with seller override, they still decide the starting draft.
- How far ahead of the call does a draft need to be ready?
- Can the August and early-September "pending" proposals be closed?
- Who should be alerted when a run fails?
- What should "not ready yet" do: stay quiet, or set a reminder?
- What should "email me this" send: the draft, or the finished proposal?
- Which practice areas come up that the rules don't cover, and who can provide typical ad spend and case values for them?
- Can Vanessa collect real phrases sellers use, so we can test against them?
- **Elite Coach vs. Elite Coach Plus (awaiting Sales approval; no rule change until approved).** Today a $400K–$1M firm always gets Elite Coach Plus ($3,200/mo). Elite Coach ($2,600/mo) is only picked for $250K–$400K. Revenue alone decides it; the rules don't look at what else is in the package or at budget signals. Example: CNK Lawfirm (~$400K–$570K, two practice areas, coaching-led call) got Elite Coach Plus, but the seller wanted Elite Coach + AI Workforce Pro. Question: should Elite Coach be the default when coaching is paired with an AI product, or at the low end of $400K–$1M? Until then, when the call names a different coaching product than the rules pick, the Phase 1 summary flags it for the seller to confirm.
- When a seller changes the package in Slack and then locks it in, should Pass 2 keep the seller's package even if its own call-purpose check would pick something else? Right now nothing says so.

## Topics not yet reviewed
- Starting package accuracy (revenue, team size): call focus now handled. Research notes record Primary engagement / Products discussed / Lead-gen gap, and select-package.mjs uses them for the Phase 1 package. See CNK Lawfirm, Oct 2026.
- Seller changes and pricing (changes added on top of the package instead of replacing it; standalone vs bundle prices; Davis Miles)
- Replies landing on the wrong firm
- Builds and deliverables (edits not reaching the PPTX/PDF, links to the slides, pending reminders, HubSpot deal links, looking up a firm by email)
