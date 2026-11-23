"""
Audit PowerPoint Template — SMB Team
======================================
Generates the 7-slide proposal PPTX (a cover + 6 content slides). Uses python-pptx. Do not modify the
layout engine below the FILL section. Only replace the # FILL: placeholders
with audit-specific content (rules: .claude/commands/audit-pptx.md).

The deck makes the case for the recommendation in one line of argument:
one number from the call → what drives it → what we do about each driver →
what we're recommending → what it costs.

Cover   — Growth, Profit, and Freedom Roadmap (firm name, seller and date —
          filled in by the engine; no FILL values)
LeadsOS — Vanessa's marketing slides, copied in when the package has marketing
          (from .source-decks/LeadsOS.pptx; no FILL values)
Slide 1 — Your Priorities, In Your Words  (the call KPI + the client's quotes)
Slide 2 — The Diagnosis                   (the root causes behind that KPI)
Slide 3 — The Plan                        (actions tied to causes + what we'll measure)
Slide 4 — The Recommended Strategy        (each product: why, and its deliverables)
Slide 5 — Your Investment                 (what $X/mo buys, year one, ad spend, return —
                                           every number read from package_decision.json)
Slide 6 — What Happens Next               (the Phase 1/2/3 growth roadmap — no prices)
A Rollout Plan slide exists in the engine but is left out (SHOW_ROLLOUT) until
real onboarding content is ready.

Data rules (enforced by the build where it can, by audit-pptx.md everywhere):
- Every number comes from the call (client or seller) or from a verified
  research observation, exactly as said or measured. Never invented, never
  estimated.
- Targets are labelled "Target:" by the engine and must rest on call data.
  With nothing to base one on, leave it None — no target line is drawn and
  the seller prep notes it.
- Seller-only guidance goes in SELLER_NOTES (the seller prep file), never on a slide or in the speaker notes.

Output: [friendly-name]/[FirmName]_[Date]_Proposal.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_LINE
from pptx.oxml.ns import qn
from lxml import etree
from functools import lru_cache
from PIL import ImageFont
import os
import re

# ═══════════════════════════════════════════════════════════════════
# FILL — Replace every placeholder. Do not delete any variable.
# ═══════════════════════════════════════════════════════════════════

# Report metadata
FIRM_NAME      = "FIRM NAME HERE"                    # FILL: full firm name
SALES_REP      = "Sales Rep Name"                    # FILL: rep's full name
OUTPUT_PATH    = "friendly-name/FirmName_Date_Proposal.pptx"  # FILL: output path

# ── Slide 1 — Your Priorities, In Your Words ─────────────────────
# The one number from the call that the recommendation moves — copied from
# the research notes' "KPI AND DIAGNOSIS" block (STEP 9B). Never invented,
# never estimated, never a number we computed.
#   kind:     "kpi" when the call gave a usable number; "qualitative" when it
#             didn't — headline is then the pain point in the client's words
#             and SELLER_NOTES[1] must tell the seller what number to ask for.
#   label:    the KPI's name for the pill, 1–3 words (e.g. "Cost per case").
#   headline: a short verbatim client line about the KPI (headline_is_quote
#             True — the engine adds the quote marks) or, with no verbatim
#             transcript, a plain statement of the number (False).
#   detail:   one sentence with the exact figures said on the call.
#   baseline: the KPI's current value in 2–5 words (shown again in the
#             "What we'll measure" row on slide 3).
#   stats:    0–2 (label, value) supporting figures from the call. A goal
#             the client stated is labelled "Your goal", never "Target".
#   said_by:  who said the headline quote and when — "Full Name (client),
#             00:07:22" — from the research notes. The client or another
#             attendee from the firm, never the seller. Shown in the speaker
#             notes. Required when headline_is_quote is True.
KPI_FOCUS = {
    "kind": "kpi",                                                     # FILL
    "label": "KPI name",                                               # FILL
    "headline": "Short verbatim client line about this number",        # FILL
    "headline_is_quote": True,                                         # FILL
    "detail": "One sentence with the exact figures said on the call.", # FILL
    "baseline": "Value today",                                         # FILL
    "stats": [
        ("Supporting figure", "Value said on the call"),               # FILL
    ],
    "said_by": "Full Name (client), 00:00:00",                         # FILL
}

# 0–3 more client quotes: (topic, quote, tie_line, said_by). topic: 1–3
# words. quote: verbatim prospect line about a problem or priority they
# raised (≤120 chars; engine adds the quote marks). tie_line: how the
# proposal answers it (≤70 chars). said_by: "Full Name (client), 00:00:00".
# Set to [] with no verbatim transcript — never invent quotes.
PROSPECT_QUOTES = [
    ("Topic", "Verbatim prospect line", "How the proposal answers it", "Full Name (client), 00:00:00"),   # FILL
    ("Topic", "Verbatim prospect line", "How the proposal answers it", "Full Name (client), 00:00:00"),   # FILL
]

# The client's why and the cost of inaction, in their own words — from the
# research notes' STEP 9B "Client's why" / "Cost of inaction" quotes. Each is
# (quote, speaker_label, said_by): speaker_label "" for the owner or "<First
# name>" for another attendee from the firm; quote ≤140 chars, verbatim (the
# engine adds the quote marks); said_by "Full Name (client), 00:00:00".
# None when the call didn't give one — never invent it.
CLIENT_WHY = ("Verbatim line: what they really want and why it matters to them", "",
              "Full Name (client), 00:00:00")                                       # FILL or None
COST_OF_INACTION = ("Verbatim line: what happens if nothing changes", "",
                    "Full Name (client), 00:00:00")                                 # FILL or None

# ── Optional slide — Lawyer Legacy Staircase (after What We Heard) ─
# Only when the rep actually walked the client through the staircase on the
# call (STEP 9B "Legacy Staircase discussed"). None = no slide.
#   current: the stage (1–8) the client and rep placed the firm at on the
#            call, or None when no position was discussed
#   goal:    the stage named as the goal on the call, or None
STAIRCASE = None   # FILL: None, or {"current": 4, "goal": 6}

# ── Slide 2 — The Diagnosis ───────────────────────────────────────
DIAGNOSIS_TITLE = "Why Each Case Costs $X,XXX"   # FILL: names the KPI, ≤40 chars
DIAGNOSIS_INTRO = "N things drive that number."  # FILL ≤90 chars, one plain line (no "here's each one in plain English")

# 3–4 root causes behind the KPI, biggest first. Each is a dict:
#   title:        the cause in plain words, ≤32 chars ("Each lead costs too much")
#   metric:       the evidence number exactly as said/measured, or "" when the
#                 cause has no number (the card then leads with the title)
#   metric_label: what the number is, ≤40 chars ("per divorce lead")
#   target:       a target backed by call data, or None (no "Target:" prefix)
#   body:         one short line: what's happening (≤80 chars). A second
#                 major problem from the call gets its own cause — never
#                 fold two problems into one card
#   source:       where the number/finding came from ("Discovery call, Oct 26",
#                 "Lighthouse test, Oct 26", "Seller, on the call")
DIAGNOSIS = [
    {"title": "Cause one", "metric": "$X", "metric_label": "what the number is",
     "target": None, "body": "What's happening and what it costs them.",
     "source": "Discovery call"},                                      # FILL
    {"title": "Cause two", "metric": "", "metric_label": "",
     "target": None, "body": "What's happening and what it costs them.",
     "source": "Discovery call"},                                      # FILL
    {"title": "Cause three", "metric": "", "metric_label": "",
     "target": None, "body": "What's happening and what it costs them.",
     "source": "Research"},                                            # FILL
]

# One line for the strip under the cards: how the plan answers the causes.
DIAGNOSIS_FIX_LINE = "One line on how the plan answers these causes."     # FILL ≤140 chars

# ── Slide 3 — The Plan ────────────────────────────────────────────
PLAN_KICKER = "Product area"                 # FILL: the product area, e.g. Paid media and website
PLAN_TITLE  = "Lower What Each Case Costs"   # FILL: the outcome, ≤40 chars

# 3–4 actions, each tied to one diagnosed cause. Each is a dict:
#   title:   the action, ≤34 chars ("Restructure the divorce campaign")
#   fixes:   the DIAGNOSIS number it answers (1-based)
#   actions: 2–4 bullets, each a deliverable of the recommended products, ≤60 chars
#   metric:  what it moves, 1–4 words ("Cost per lead") — shown, numbered to
#            its action, in the "What we'll measure" row under the cards.
#            Not the slide 1 KPI again (that's always the first tile).
#   target:  the target, based on call data, or None (no target line is
#            drawn; the seller prep notes it automatically)
#   baseline: today's value of the metric, as said on the call or measured
#            in research ("24/100"), or None. With no target and no
#            baseline, the metric is left out of the row.
PLAN = [
    {"title": "Action one", "fixes": 1,
     "actions": ["Specific deliverable", "Specific deliverable"],
     "metric": "Metric", "target": None, "baseline": "Value today"},   # FILL
    {"title": "Action two", "fixes": 2,
     "actions": ["Specific deliverable", "Specific deliverable"],
     "metric": "Metric", "target": None, "baseline": "Value today"},   # FILL
    {"title": "Action three", "fixes": 3,
     "actions": ["Specific deliverable", "Specific deliverable"],
     "metric": "Metric", "target": None, "baseline": "Value today"},   # FILL
]

# Optional strip under the plan cards ("Also included: …"), or None.
PLAN_NOTE = None                                                       # FILL ≤160 chars

# ── Slide 4 — The Recommended Strategy ────────────────────────────
STRATEGY_TITLE = "N Pieces, One Strategy"    # FILL ≤40 chars

# 1–3 pieces, in package_decision.json order. A product may be split into
# pieces (e.g. Full Service Marketing → "Get found" + "Get the call").
#   product:      catalog product name exactly as in the BUILD NOTES
#   title:        the piece in 1–3 words ("Build demand")
#   channels:     what it covers, ≤40 chars ("Website · SEO · AI search")
#   deliverables: 3–5 bullets, only catalog deliverables, ≤55 chars each
#   why:          why we chose it for THIS firm, tied to slide 2 (≤110 chars)
STRATEGY = [
    {"product": "Catalog product name", "title": "Piece", "channels": "Channels",
     "deliverables": ["Catalog deliverable", "Catalog deliverable", "Catalog deliverable"],
     "why": "Why this firm needs it, tied to a diagnosed cause."},     # FILL
]

# Rollout Plan: left out of the deck until real onboarding content exists
# (no FILL values). Never add onboarding steps or timelines anywhere.

# ── Seller prep (never in the deck) ───────────────────────────────
# {slide: "note"} keyed by slide name: "priorities", "staircase",
# "diagnosis", "plan", "strategy", "investment", "roadmap" — what to ask, what to
# confirm, deal context. Required on "priorities" when KPI_FOCUS kind is
# "qualitative". The deck's speaker notes stay EMPTY (the .pptx goes out on
# a public link and may reach the client): these notes, the engine's own
# notes and who said each quote go to <deck>_Seller_Prep.txt next to the
# deck, which the pipeline sends to the seller by email and Slack and never
# commits. Escalation flags still stay in the BUILD NOTES.
SELLER_NOTES = {
}

# ── Slide 5 — Your Investment ─────────────────────────────────────
# Every number on this slide (prices, monthly and year-one totals, ad spend,
# return) is read from package_decision.json → "investment", which
# scripts/reprice.mjs computes in code. Never type a price or figure here.
#
# One deliverables line per product, keyed by the product name exactly as in
# package_decision.json (marketing_name / coaching_name / law_name), ≤70 chars.
PRODUCT_LINES = {
    "Full Service Marketing — Growth": "Website · SEO · Google Ads · LSA · Meta Ads · Google profile",  # FILL
}

# Why this ad spend, in one short payoff clause (≤90 chars), e.g. "to turn
# high-intent divorce searches into signed cases". None when the package has
# no paid ads (the engine then leaves the ad spend panel out).
AD_SPEND_WHY = "to turn high-intent searches into signed cases"     # FILL

# The closing line on the investment slide: a verbatim client line about the
# outcome they want — (quote, said_by), ≤160 chars, engine adds the quote
# marks. Never reworded, never a quote already used elsewhere in the deck.
# None when there's no other verbatim line worth closing on (the bar is left
# off).
CLOSING_QUOTE = ("Verbatim client line about the outcome they want",
                 "Full Name (client), 00:00:00")                                   # FILL or None

# ── Slide 6 — What Happens Next (the growth roadmap) ──────────────
# Three phases: where the firm starts (exactly the package on the investment
# slide) and what it graduates into as it grows. Direction, not a quote: no
# prices, no dates or timelines, no promised outcomes. Rules for choosing
# each phase's products: audit-pptx.md "Slide 6".
ROADMAP_TITLE = "Your Growth Roadmap"         # FILL ≤40 chars

# Exactly 3 phases, each a dict:
#   phase:    the phase name, ≤24 chars ("Foundation", "Operational Scale", "Optimize")
#   when:     what starts it, ≤60 chars. Phase 1 is "Starting now"; phases 2
#             and 3 name a milestone from this firm's trajectory or its own
#             stated goal ("Once intake runs without you") — no invented numbers
#   products: catalog product names. Phase 1 = every product in the package,
#             exactly as in package_decision.json → investment.products (the
#             build checks); phases 2–3 = products the firm doesn't have yet
#   items:    2–4 bullets, ≤55 chars: what the phase puts in place
#   unlocks:  one sentence, ≤120 chars: what it unlocks for the owner, in
#             client-facing DBM language (no promised results)
ROADMAP = [
    {"phase": "Foundation", "when": "Starting now",
     "products": ["Full Service Marketing — Growth"],
     "items": ["What the package puts in place", "What the package puts in place"],
     "unlocks": "What this phase unlocks for the owner, in their terms."},             # FILL
    {"phase": "Operational Scale", "when": "Once the firm hits a milestone from the call",
     "products": ["Managed Operations"],
     "items": ["What gets added, and why", "What gets added, and why"],
     "unlocks": "What this phase unlocks for the owner, in their terms."},             # FILL
    {"phase": "Optimize", "when": "Once the firm hits the next milestone",
     "products": ["Fractional CFO", "Bookkeeping"],
     "items": ["What gets added, and why", "What gets added, and why"],
     "unlocks": "What this phase unlocks for the owner, in their terms."},             # FILL
]

# ── ProfitOS slides (added by the engine after the roadmap) ───────
# When package_decision.json includes Fractional CFO or Bookkeeping, the
# engine adds the ProfitOS slides (Vanessa's ProfitOS proposal deck, in her
# wording, in the Loom order). Only two things come from this firm's call:
#
# The goals the client named that FCFO / bookkeeping answers: up to 3
# (heading ≤28 chars, line ≤90 chars), in plain words, each traceable to a
# line in the research notes (record it in the BUILD NOTES). Never invented.
# [] when the call gave none — the engine then shows ProfitOS's standard
# three goals and tells the seller in the prep file.
PROFITOS_GOALS = [
    # ("Numbers you can trust", "You want a view of your financials you can rely on each month"),  # FILL
]
# Why the recommended FCFO level fits this firm, one sentence ≤160 chars,
# from the call. None → the level's standard line from the ProfitOS deck.
PROFITOS_WHY = None                                                   # FILL or None
# Both are ignored when the package has no FCFO or Bookkeeping.

# ═══════════════════════════════════════════════════════════════════
# LAYOUT ENGINE — DO NOT MODIFY BELOW THIS LINE
# ═══════════════════════════════════════════════════════════════════

# ── Color palette ─────────────────────────────────────────────────
def rgb(h): return RGBColor(int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))

# SMB Team brand colors (see brand book): Deep Wood Blue, Ocean Blue, Lime Green.
NAVY        = rgb("003A59")   # Deep Wood Blue — primary brand color
OCEAN_BLUE  = rgb("0091C9")   # brand accent — numbers, badges, kickers
LIME_GREEN  = rgb("69CD2B")   # brand accent — small "pop" text/labels on navy
WHITE       = rgb("FFFFFF")

BG_WASH       = rgb("F4F7F9")   # full-bleed slide background
GREEN       = rgb("3F8F1A")     # "Target:" lines and client goals
CORAL       = rgb("C8553D")     # the problem numbers on the diagnosis slide

DARK_TEXT   = rgb("1B2A38")   # near-black body/label text on white cards
BODY_TEXT   = rgb("4A5C6B")   # neutral gray-blue for card copy
SLATE       = rgb("7C8D9B")   # lighter captions (sources, retail price, services line)
FOOTER_TEXT = rgb("8FB2C6")
RULE_GRAY   = rgb("D9E2E8")
SOFT_BLUE   = rgb("DCEAF3")   # "why we chose it" strips
NAVY_TEXT_SOFT = rgb("C2D8E6")  # body copy on navy
NAVY_RULE   = rgb("2F6F94")

ROI_BG      = rgb("F0FAF4")
ROI_GREEN   = rgb("0B6B4A")
ROI_HILIGHT = rgb("E2F3E9")

BUNDLE_SAVINGS_TEXT = rgb("A9D68C")   # lighter green — reads as "money saved"

# The Rollout Plan slide is built but left out of the deck until real
# onboarding content exists — flip this to True to add it back.
SHOW_ROLLOUT = False

# Where the computed investment lives: the firm's package_decision.json,
# next to this script. The master template has none, so it renders a sample.
DECISION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "package_decision.json")


def load_decision():
    import json
    if not os.path.isfile(DECISION_PATH):
        return {}
    with open(DECISION_PATH) as f:
        return json.load(f)


def profitos_scope():
    """(FCFO level or None, bookkeeping level or None) from the package.
    Read from package_decision.json, so the ProfitOS slides always match the
    products priced on the investment slide."""
    d = load_decision()
    names = " + ".join(str(d.get(k) or "") for k in ("marketing_name", "coaching_name", "law_name"))
    fcfo = re.search(r"FCFO (Advisor|Director|Partner)", names)
    books = re.search(r"Bookkeeping Level ([1-4])", names)
    return (fcfo.group(1) if fcfo else None, int(books.group(1)) if books else None)


PROFITOS_LEVEL, BOOKKEEPING_LEVEL = profitos_scope()

# The ProfitOS slides, in the order of Vanessa's walkthrough: the firm's
# goals → bookkeeping vs CFO → (bookkeeping levels) → questions → analysis
# → the plan for this firm → the recommended level → the level ladder.
# Bookkeeping alone gets bookkeeping vs CFO and the bookkeeping levels.
if PROFITOS_LEVEL:
    PROFITOS_SLIDES = (["pos_goals", "pos_two_sides"] + (["pos_books"] if BOOKKEEPING_LEVEL else []) +
                       ["pos_questions", "pos_analysis", "pos_plan", "pos_level", "pos_ladder"])
elif BOOKKEEPING_LEVEL:
    PROFITOS_SLIDES = ["pos_two_sides", "pos_books"]
else:
    PROFITOS_SLIDES = []

# ── LeadsOS marketing slides (copied from Vanessa's deck) ─────────
# Any package with a marketing product gets the client-facing slides of
# Vanessa's LeadsOS deck between the cover and the proposal (her deck leads
# into "what we discovered + what we recommend"). The deck is a private file in
# the HubSpot "Proposal Source Decks" folder — never in this public repo — that
# scripts/fetch-source-deck.mjs downloads to .source-decks/LeadsOS.pptx before
# a build. Her slides are copied as they are, scaled to this deck's size; her
# speaker notes go to the seller prep, never into the deck.
#   - Everything from her "SUPPLEMENTAL" divider on (client results that need
#     client consent) is left out.
#   - A slide containing a phrase in LEADSOS_HOLD is left out until it is
#     confirmed for every client deck: delete the phrase here to add it back.
LEADSOS_HOLD = ()   # nothing held: Vanessa cleared the 37% and $100M+ figures (Nov 20)
LEADSOS_DECK = os.environ.get("LEADSOS_DECK") or os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".source-decks", "LeadsOS.pptx")


def _slide_text(slide):
    return "\n".join(sh.text_frame.text for sh in slide.shapes if sh.has_text_frame)


def _slide_title(slide):
    """Her slide's headline: the text set in the largest font."""
    best, size = "", 0
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        for para in sh.text_frame.paragraphs:
            for r in para.runs:
                if r.text.strip() and r.font.size and r.font.size > size:
                    best, size = para.text, r.font.size
    return " ".join(best.split())[:70]


def _package_names():
    d = load_decision()
    return " + ".join(str(d.get(k) or "") for k in ("marketing_name", "coaching_name", "law_name"))


def load_source_deck(wanted, path, label, stop, hold=()):
    """(source Presentation or None, [(source slide number, slide, title)], [held numbers], why-left-out).
    Copies nothing unless the package wants this deck (`wanted`). Stops at
    the first slide whose text starts with the `stop` divider word."""
    if not wanted:
        return None, [], [], None
    if not os.path.isfile(path):
        return None, [], [], (f"the {label} source deck wasn't found at {path} "
                              "(the build downloads it from HubSpot: node scripts/fetch-source-deck.mjs)")
    try:
        src = Presentation(path)
    except Exception as e:  # a corrupt download must not stop the proposal
        return None, [], [], f"the {label} source deck couldn't be opened ({e})"
    keep, held = [], []
    for n, slide in enumerate(src.slides, 1):
        text = _slide_text(slide)
        if re.match(rf"\s*{stop}\b", text):
            break
        if any(h in text for h in hold):
            held.append(n)
            continue
        keep.append((n, slide, _slide_title(slide)))
    return src, keep, held, None


def load_leadsos():
    return load_source_deck(bool(load_decision().get("marketing_name")), LEADSOS_DECK,
                            "LeadsOS", "SUPPLEMENTAL", LEADSOS_HOLD)


LEADSOS_SRC, LEADSOS_SLIDES, LEADSOS_HELD, LEADSOS_MISSING = load_leadsos()

# ── AI Workforce Pro / Fractional CTO slides (copied from the AIWP deck) ──
# Any package with AI Workforce Pro (either tier) or a Fractional CTO level
# gets the client-facing slides of the "AI Workforce Pro + FCTO" mini deck
# after the cover (after the LeadsOS slides when both apply). Same handling
# as LeadsOS: a private file in the HubSpot "Proposal Source Decks" folder,
# downloaded by scripts/fetch-source-deck.mjs (newest .pptx with "Workforce"
# in its name) to .source-decks/AIWP.pptx; slides copied as they are; speaker
# notes go to the seller prep, never into the deck.
#   - Everything from its "APPENDIX" divider on (use-case deep dives) is left out.
#   - A slide containing a phrase in AIWP_HOLD is left out until confirmed.
AIWP_HOLD = ()
AIWP_DECK = os.environ.get("AIWP_DECK") or os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".source-decks", "AIWP.pptx")
AIWP_SRC, AIWP_SLIDES, AIWP_HELD, AIWP_MISSING = load_source_deck(
    bool(re.search(r"AI Workforce Pro|Fractional CTO", _package_names())),
    AIWP_DECK, "AI Workforce Pro / FCTO", "APPENDIX", AIWP_HOLD)

# Slide order. The staircase slide is optional (STAIRCASE in the FILL).
SLIDE_ORDER = (["cover"] + [f"leadsos_{n}" for n, _, _ in LEADSOS_SLIDES] +
               [f"aiwp_{n}" for n, _, _ in AIWP_SLIDES] + ["priorities"] + (["staircase"] if STAIRCASE else []) +
               ["diagnosis", "plan", "strategy"] + (["rollout"] if SHOW_ROLLOUT else []) +
               ["investment", "roadmap"] + PROFITOS_SLIDES)
PAGE = {key: i + 1 for i, key in enumerate(SLIDE_ORDER)}
TOTAL_SLIDES = len(SLIDE_ORDER)
INVESTMENT_PAGE = PAGE["investment"]

FONT = "Poppins"
LOGO_PATH = os.path.join(os.path.dirname(__file__), "smb_team_logo.png")
# This script is copied into each firm's own folder (a sibling of "Design
# Files/" at the repo root) to run — the logo above sits right next to it
# because it's copied too, but fonts/ is not, so it's addressed relative to
# the repo root instead.
FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "Design Files", "fonts")

# ── Core helpers ──────────────────────────────────────────────────

def emu(*inches):
    return tuple(int(x * 914400) for x in inches)


# Fields with a documented character budget (see .claude/commands/audit-pptx.md)
# get hard-capped where they're placed on the slide — a backstop so oversized
# content can never spill past its box, no matter what the FILL section
# contains. auto-shrink (set in add_text below) is the first line of defense;
# this cap keeps the shrunk font from having to go microscopic.
_TRUNCATED = []  # (label, original_text) pairs — reported just before saving

def cap(text, max_chars, label=""):
    text = "" if text is None else str(text)
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars - 1].rstrip()
    if " " in truncated:
        truncated = truncated.rsplit(" ", 1)[0]
    truncated = truncated.rstrip(" ,.;:-—–") + "…"
    _TRUNCATED.append((label or text[:24], text))
    return truncated


def add_rect(slide, left, top, w, h, fill=None, line=False):
    from pptx.util import Emu as E
    shape = slide.shapes.add_shape(1, E(int(left*914400)), E(int(top*914400)),
                                   E(int(w*914400)), E(int(h*914400)))
    shape.line.fill.background() if not line else None
    if not line:
        shape.line.color.rgb = WHITE
        shape.line.width = 0
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    return shape


# ── Text fitting ──────────────────────────────────────────────────
# PowerPoint's own "shrink text on overflow" (normAutofit) is only a flag:
# python-pptx can't compute the scale, PowerPoint applies it only after a
# human edits the box, and Google Slides / Keynote / previews ignore it. So
# every text box is measured here instead, against the same Poppins files
# that get embedded, and the font size actually written to the file is the
# one that fits — every viewer then renders exactly the same thing.

_INSET_X = 0.10        # python-pptx's default left/right text-box padding (in)
_INSET_Y = 0.05        # ... and top/bottom padding (in)
_WIDTH_SAFETY = 0.97   # small margin for renderer kerning differences
_FIT_STEP = 0.5        # "drop one font size" = 0.5pt per step
_SHRUNK = []           # (label, from_pt, to_pt) — reported just before saving


@lru_cache(maxsize=None)
def _font_file(bold, italic):
    name = "Poppins-Bold.ttf" if bold else ("Poppins-Italic.ttf" if italic else "Poppins-Regular.ttf")
    # Measured at 1000px; widths scale linearly with point size.
    return ImageFont.truetype(os.path.join(FONT_DIR, name), 1000)


def text_width(text, size, bold=False, italic=False):
    """Rendered width of a single line of text, in inches."""
    return _font_file(bold, italic).getlength(text) * size / 1000 / 72


def line_height(size, bold=False, italic=False):
    """Single-spaced line height in inches (Poppins: ascent + descent ≈ 1.4em)."""
    ascent, descent = _font_file(bold, italic).getmetrics()
    return (ascent + descent) * size / 1000 / 72


def baseline_offset(size, bold=False, italic=False):
    """Distance from a text box's top edge to its first line's baseline."""
    ascent, _ = _font_file(bold, italic).getmetrics()
    return _INSET_Y + ascent * size / 1000 / 72


def wrap_lines(text, size, max_w, bold=False, italic=False):
    """Greedy word wrap the way PowerPoint does it. Returns the lines."""
    lines = []
    for para in str(text).split("\n"):
        cur = ""
        for word in para.split():
            trial = f"{cur} {word}" if cur else word
            if cur and text_width(trial, size, bold, italic) > max_w:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        lines.append(cur)
    return lines


def fit_text(text, w, h, size, bold=False, italic=False, max_lines=None, min_size=None):
    """Largest size <= `size` (in _FIT_STEP steps, down to `min_size`) at which
    `text` wraps inside a w x h box. Returns (size, lines), or (None, None)
    when it doesn't fit even at min_size. A box is always allowed one line
    even if it's shorter than that line — small single-line labels are
    positioned for that on purpose; what must never happen is extra lines."""
    if min_size is None:
        min_size = max(6.0, round(size * 0.75 * 2) / 2)
    max_w = (w - 2 * _INSET_X) * _WIDTH_SAFETY
    avail_h = h - 2 * _INSET_Y
    s = size
    while s >= min_size - 1e-6:
        lines = wrap_lines(text, s, max_w, bold, italic)
        fits_h = max(1, int(avail_h / line_height(s, bold, italic) + 0.15))
        allowed = min(fits_h, max_lines) if max_lines else fits_h
        if len(lines) <= allowed and all(text_width(l, s, bold, italic) <= max_w for l in lines):
            return s, lines
        s -= _FIT_STEP
    return None, None


def _truncate_to_fit(text, w, h, size, bold, italic, max_lines):
    words = str(text).split()
    while len(words) > 1:
        words.pop()
        trial = " ".join(words).rstrip(" ,.;:-—–·") + "…"
        if fit_text(trial, w, h, size, bold, italic, max_lines, min_size=size)[0]:
            return trial
    return words[0] if words else ""


def add_text(slide, text, left, top, w, h, size, color, bold=False,
             align=PP_ALIGN.LEFT, italic=False, wrap=True,
             cap_chars=None, cap_label="", fit=True, max_lines=None,
             min_size=None, anchor=None, strike=False):
    from pptx.util import Emu as E, Pt as P
    if cap_chars is not None:
        text = cap(text, cap_chars, label=cap_label)
    if fit and text:
        fitted, _ = fit_text(text, w, h, size, bold, italic, max_lines, min_size)
        if fitted is None:
            # Doesn't fit even at the smallest allowed size — keep the floor
            # size and trim at a word boundary instead of spilling the box.
            floor = min_size if min_size is not None else max(6.0, round(size * 0.75 * 2) / 2)
            original = text
            text = _truncate_to_fit(text, w, h, floor, bold, italic, max_lines)
            _TRUNCATED.append((cap_label or original[:24], original))
            fitted = floor
        if fitted < size:
            _SHRUNK.append((cap_label or str(text)[:32], size, fitted))
        size = fitted
    txb = slide.shapes.add_textbox(E(int(left*914400)), E(int(top*914400)),
                                   E(int(w*914400)), E(int(h*914400)))
    tf = txb.text_frame
    tf.word_wrap = wrap
    if anchor is not None:
        tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = FONT
    run.font.size = P(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic
    if strike:
        run.font._rPr.set("strike", "sngStrike")
    # The size above is already the measured fit — turn PowerPoint's own
    # autofit off so no viewer rescales it a second time.
    tf.auto_size = MSO_AUTO_SIZE.NONE
    return txb


def add_title(slide, text, w):
    """Slide title inside the 0.92in navy header. One line at 20pt, dropping
    a half-size at a time to 15pt; if a long firm name still doesn't fit,
    two bottom-anchored lines from 15pt down to 12pt. Never crosses the
    header's bottom edge at 0.92in."""
    one_line, _ = fit_text(text, w, 0.44, 20, bold=True, max_lines=1, min_size=15)
    if one_line:
        add_text(slide, text, 0.32, 0.42, w, 0.44, one_line, WHITE, bold=True,
                 fit=False, anchor=MSO_ANCHOR.MIDDLE)
    else:
        add_text(slide, text, 0.32, 0.30, w, 0.60, 15, WHITE, bold=True,
                 max_lines=2, min_size=12, anchor=MSO_ANCHOR.BOTTOM,
                 cap_label="slide title")


def add_header(slide, title, title_w, kicker="LAW FIRM GROWTH AUDIT"):
    """Background wash, navy header, kicker and title — shared by every
    slide. The kicker names the slide's step in the story ("THE DIAGNOSIS")
    followed by the firm. No divider stripe under the header: the deck stays
    quiet so it supports the rep instead of competing."""
    add_rect(slide, 0, 0, 10, 5.625, fill=BG_WASH)
    add_rect(slide, 0, 0, 10, 0.92, fill=NAVY)
    add_text(slide, f"{kicker}  ·  {FIRM_NAME.upper()}",
             0.32, 0.20, title_w, 0.18, 7.5, LIME_GREEN, bold=True,
             max_lines=1, cap_label="header kicker")
    add_title(slide, title, title_w)


def add_footer(slide, page, total, logo_path):
    add_rect(slide, 0, 5.27, 10, 0.35, fill=NAVY)
    if logo_path and os.path.isfile(logo_path):
        from pptx.util import Emu as E
        slide.shapes.add_picture(logo_path,
                                 E(int(0.30*914400)), E(int(5.33*914400)),
                                 E(int(1.03*914400)), E(int(0.21*914400)))
    add_text(slide, f"CONFIDENTIAL  ·  PREPARED BY {SALES_REP.upper()} | SMB TEAM",
             1.55, 5.35, 5.40, 0.20, 7, FOOTER_TEXT)
    add_text(slide, f"{page} / {total}", 8.40, 5.35, 1.30, 0.20, 7, FOOTER_TEXT,
             align=PP_ALIGN.RIGHT)


_BULLET_INDENT = 0.16   # hanging indent for bullet text (in)
_BULLET_GAP_PT = 6      # space before each bullet after the first


def add_bullets(slide, items, left, top, w, h, size, color, bullet_color, label=""):
    """One text box with a real bulleted paragraph per item, sized so all
    items fit: drops 0.5pt at a time (down to 75%) until the wrapped lines
    plus inter-bullet spacing fit the box."""
    from pptx.util import Emu as E, Pt as P
    max_w = (w - 2 * _INSET_X - _BULLET_INDENT) * _WIDTH_SAFETY
    avail_h = h - 2 * _INSET_Y
    floor = max(6.0, round(size * 0.75 * 2) / 2)
    s = size
    while s > floor:
        n_lines = sum(len(wrap_lines(t, s, max_w)) for t in items)
        need = n_lines * line_height(s) + (len(items) - 1) * _BULLET_GAP_PT / 72
        if need <= avail_h:
            break
        s -= _FIT_STEP
    if s < size:
        _SHRUNK.append((label, size, s))

    txb = slide.shapes.add_textbox(E(int(left*914400)), E(int(top*914400)),
                                   E(int(w*914400)), E(int(h*914400)))
    tf = txb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    hex_bullet = "%02X%02X%02X" % tuple(bullet_color)
    for i, text in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        if i:
            p.space_before = P(_BULLET_GAP_PT)
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", str(int(_BULLET_INDENT * 914400)))
        pPr.set("indent", str(-int(_BULLET_INDENT * 914400)))
        for tag, attrs in [("a:buClr", None), ("a:buFont", {"typeface": "Arial"}),
                           ("a:buChar", {"char": "•"})]:
            el = etree.SubElement(pPr, qn(tag))
            if tag == "a:buClr":
                etree.SubElement(el, qn("a:srgbClr")).set("val", hex_bullet)
            else:
                for k, v in attrs.items():
                    el.set(k, v)
        run = p.add_run()
        run.text = text
        run.font.name = FONT
        run.font.size = P(s)
        run.font.color.rgb = color
    return txb

def add_rich_text(slide, paras, left, top, w, h, label="", anchor=None, min_scale=0.75):
    """One text box holding several paragraphs, each a list of runs
    (text, size, bold, italic, color) plus a space-before in pt. Every size
    is scaled down together, a half-point at a time on the largest run,
    until all wrapped lines fit the box."""
    from pptx.util import Emu as E, Pt as P
    max_w = (w - 2 * _INSET_X) * _WIDTH_SAFETY
    avail_h = h - 2 * _INSET_Y
    top_size = max(r[1] for runs, _ in paras for r in runs)
    scale = 1.0
    while True:
        need = 0.0
        for i, (runs, space) in enumerate(paras):
            # Measure a paragraph at its largest run's style — runs in one
            # paragraph here share a line style (label vs quote).
            big = max(runs, key=lambda r: r[1])
            s = big[1] * scale
            text = "".join(r[0] for r in runs)
            need += len(wrap_lines(text, s, max_w, big[2], big[3])) * line_height(s)
            if i:
                need += space * scale / 72
        if need <= avail_h or scale <= min_scale:
            break
        scale = max(min_scale, (top_size * scale - _FIT_STEP) / top_size)
    if scale < 1.0:
        _SHRUNK.append((label, top_size, round(top_size * scale * 2) / 2))

    txb = slide.shapes.add_textbox(E(int(left*914400)), E(int(top*914400)),
                                   E(int(w*914400)), E(int(h*914400)))
    tf = txb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    if anchor is not None:
        tf.vertical_anchor = anchor
    for i, (runs, space) in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        if i and space:
            p.space_before = P(space * scale)
        for text, size, bold, italic, color in runs:
            r = p.add_run()
            r.text = text
            r.font.name = FONT
            r.font.size = P(round(size * scale * 2) / 2)
            r.font.bold = bold
            r.font.italic = italic
            r.font.color.rgb = color
    return txb


def add_rule(slide, x1, y1, x2, y2, color, weight_pt=0.75):
    """A thin straight divider line (a connector, so no fill or shadow)."""
    from pptx.enum.shapes import MSO_CONNECTOR
    from pptx.util import Emu as E, Pt as P
    conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(int(x1*914400)),
                                      E(int(y1*914400)), E(int(x2*914400)), E(int(y2*914400)))
    conn.line.color.rgb = color
    conn.line.width = P(weight_pt)


def add_shape(slide, kind, left, top, w, h, fill=None, line_color=None,
              line_pt=1.0, dash=False):
    """Any autoshape (oval, rounded rectangle, …) with an optional solid
    fill and optional (dashed) outline; no outline when line_color is None."""
    from pptx.util import Emu as E, Pt as P
    shp = slide.shapes.add_shape(kind, E(int(left*914400)), E(int(top*914400)),
                                 E(int(w*914400)), E(int(h*914400)))
    if fill is not None:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    else:
        shp.fill.background()
    if line_color is not None:
        shp.line.color.rgb = line_color
        shp.line.width = P(line_pt)
        if dash:
            shp.line.dash_style = MSO_LINE.DASH
    else:
        shp.line.fill.background()
    return shp


def add_badge(slide, n, left, top, d, fill, color=WHITE):
    """A numbered circle (diagnosis and plan cards)."""
    add_shape(slide, MSO_SHAPE.OVAL, left, top, d, d, fill=fill)
    add_text(slide, str(n), left - 0.05, top, d + 0.10, d, 10 if d < 0.34 else 11,
             color, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
             fit=False)


def add_pill(slide, text, left, top, h, fill, color=WHITE, size=7.5, max_w=4.0):
    """A rounded label sized to its text."""
    text = str(text).upper()
    w = min(max_w, text_width(text, size, bold=True) + 2 * _INSET_X + 0.30)
    pill = add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h, fill=fill)
    pill.adjustments[0] = 0.5
    add_text(slide, text, left, top, w, h, size, color, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, max_lines=1,
             cap_label="pill")
    return w


def add_strip(slide, lead, text, top, h=0.48, label=""):
    """White strip with an Ocean Blue edge: bold lead-in + one line of copy."""
    text = re.sub(r"^\s*" + re.escape(lead.rstrip(":")) + r"\s*:?\s*", "", str(text), flags=re.I)
    add_rect(slide, 0.30, top, 9.40, h, fill=WHITE)
    add_rect(slide, 0.30, top, 0.05, h, fill=OCEAN_BLUE)
    add_rich_text(slide, [([(lead + " ", 9.5, True, False, NAVY),
                            (text, 9.5, False, False, DARK_TEXT)], 0)],
                  0.50, top, 9.10, h, label=label, anchor=MSO_ANCHOR.MIDDLE)


def new_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])  # blank


# Seller prep notes, collected per slide while building (written to the prep file, not the deck).
_NOTES = {}


def note(key, text):
    if text:
        _NOTES.setdefault(key, []).append(str(text).strip())


def seller_note(key):
    """SELLER_NOTES entry for a slide name ("priorities", "plan", …)."""
    return SELLER_NOTES.get(key) if isinstance(SELLER_NOTES, dict) else None


SLIDE_TITLES = {"cover": "Cover", "priorities": "Your Priorities, In Your Words", "staircase": "Lawyer Legacy Staircase",
                "diagnosis": "The Diagnosis", "plan": "The Plan", "strategy": "The Recommended Strategy",
                "rollout": "Rollout Plan", "investment": "Your Investment",
                "roadmap": "What Happens Next",
                "pos_goals": "Managed Financials — Your Goals", "pos_two_sides": "Managed Financials — Reliable Numbers to Confident Action",
                "pos_books": "Managed Financials — Bookkeeping Levels", "pos_questions": "Managed Financials — Questions You Can Answer",
                "pos_analysis": "Managed Financials — The Analysis", "pos_plan": "Managed Financials — Your Plan",
                "pos_level": "Managed Financials — Your Level", "pos_ladder": "Managed Financials — Leadership Matched to Your Stage"}


def seller_prep_path():
    base = re.sub(r"_Proposal\.pptx$|\.pptx$", "", OUTPUT_PATH)
    return base + "_Seller_Prep.txt"


def _source_theme_colors(src):
    """scheme color name → hex, from the source deck's theme (her slides refer
    to a few theme colors, which this deck's theme would otherwise recolor)."""
    try:
        theme = next(r.target_part for r in src.slide_masters[0].part.rels.values()
                     if r.reltype.endswith("/theme"))
        root = etree.fromstring(theme.blob)
    except Exception:
        return {}
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    out = {}
    for el in root.findall(".//a:clrScheme/*", ns):
        c = el.find("a:srgbClr", ns)
        if c is None:
            c = el.find("a:sysClr", ns)
            val = c.get("lastClr") if c is not None else None
        else:
            val = c.get("val")
        if val:
            out[etree.QName(el).localname] = val
    for alias, real in (("tx1", "dk1"), ("bg1", "lt1"), ("tx2", "dk2"), ("bg2", "lt2")):
        if real in out:
            out[alias] = out[real]
    return out


# Attributes that carry a length and shrink with the slide: positions and
# sizes (EMU), font sizes and spacing (hundredths of a point), line widths,
# text insets and shadow offsets.
_SCALE_ATTRS = {"off": ("x", "y"), "chOff": ("x", "y"), "ext": ("cx", "cy"), "chExt": ("cx", "cy"),
                "rPr": ("sz", "spc", "kern"), "defRPr": ("sz", "spc", "kern"),
                "endParaRPr": ("sz", "spc", "kern"), "ln": ("w",),
                "bodyPr": ("lIns", "tIns", "rIns", "bIns"), "spcPts": ("val",),
                "outerShdw": ("blurRad", "dist"), "innerShdw": ("blurRad", "dist")}
_FOOTER_NUM = re.compile(r"(LeadsOS for Law Firms\s*·\s*\d{4})\s*·\s*\d+\s*$")


def copy_source_slide(prs, src_slide, scale, theme):
    """Append a copy of another deck's slide: its background, shapes and
    pictures (links kept), scaled to this deck's size. Speaker notes are not
    copied. Returns the new slide."""
    import copy, io
    dst = new_slide(prs)
    R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    rid = {}
    for old, rel in src_slide.part.rels.items():
        kind = rel.reltype.rsplit("/", 1)[-1]
        if kind in ("notesSlide", "slideLayout"):
            continue
        if rel.is_external:
            rid[old] = dst.part.relate_to(rel.target_ref, rel.reltype, is_external=True)
        elif kind == "image":
            rid[old] = dst.part.get_or_add_image_part(io.BytesIO(rel.target_part.blob))[1]
    csld = copy.deepcopy(src_slide._element.cSld)
    for el in csld.iter():
        if not isinstance(el.tag, str):
            continue
        for a in [a for a in el.attrib if a.startswith("{%s}" % R)]:
            if el.get(a) in rid:
                el.set(a, rid[el.get(a)])
            else:
                del el.attrib[a]   # a link to something not copied (e.g. her notes)
        name = etree.QName(el).localname
        for a in _SCALE_ATTRS.get(name, ()):
            v = el.get(a)
            if v is not None and re.fullmatch(r"-?\d+", v) and not (name == "ext" and "uri" in el.attrib):
                el.set(a, str(int(round(int(v) * scale))))
        if name == "schemeClr" and el.get("val") in theme:
            el.tag = "{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr"
            el.set("val", theme[el.get("val")])
        if name == "t" and el.text and _FOOTER_NUM.search(el.text):
            el.text = _FOOTER_NUM.sub(r"\1", el.text)   # her page number won't match this deck
    dst._element.replace(dst._element.cSld, csld)
    return dst


def build_source_slides(prs, src, slides, held, hold, missing, prefix, label, whose, skipped):
    """Copy a source deck's kept slides into the deck, with seller-prep notes."""
    if missing:
        note("cover", f"The {label} slides were left out: {missing}.")
        print(f"WARNING: {label} slides left out — {missing}.")
        return
    if not slides:
        return
    scale = prs.slide_width / src.slide_width
    theme = _source_theme_colors(src)
    for n, slide, title in slides:
        copy_source_slide(prs, slide, scale, theme)
        key = f"{prefix}_{n}"
        SLIDE_TITLES[key] = f"{label} — {title}" if title else f"{label} slide {n}"
        if slide.has_notes_slide:
            text = " ".join(slide.notes_slide.notes_text_frame.text.split())
            if text:
                note(key, f"{whose} speaker notes (source slide {n}): {text}")
    first, last = f"{prefix}_{slides[0][0]}", f"{prefix}_{slides[-1][0]}"
    note(first, f"Slides {PAGE[first]}–{PAGE[last]} are the {label} slides, copied as they are. {skipped}"
         + (f" Held until confirmed for every client deck: source slide(s) "
            f"{', '.join(str(h) for h in held)} ({' / '.join(hold)})." if held else ""))
    print(f"{label}: {len(slides)} slides added (source slides "
          f"{', '.join(str(n) for n, _, _ in slides)})"
          + (f"; held: {', '.join(str(h) for h in held)}" if held else ""))


def build_leadsos(prs):
    build_source_slides(prs, LEADSOS_SRC, LEADSOS_SLIDES, LEADSOS_HELD, LEADSOS_HOLD, LEADSOS_MISSING,
                        "leadsos", "LeadsOS marketing", "Vanessa's",
                        "Her client results slides are left out.")


def build_aiwp(prs):
    build_source_slides(prs, AIWP_SRC, AIWP_SLIDES, AIWP_HELD, AIWP_HOLD, AIWP_MISSING,
                        "aiwp", "AI Workforce Pro / FCTO", "The AIWP deck's",
                        "Its appendix (use-case deep dives) is left out.")


def write_notes(prs):
    """Seller prep goes to a text file beside the deck, never into the
    .pptx: its speaker notes are left empty because the deck is shared on a
    public link and may be forwarded to the client."""
    for slide in prs.slides:
        if slide.has_notes_slide:
            slide.notes_slide.notes_text_frame.text = ""
    sections = []
    for key in SLIDE_ORDER:
        lines = list(_NOTES.get(key, []))
        own = seller_note(key)
        if own:
            lines.insert(0, str(own).strip())
        if lines:
            sections.append(f"Slide {PAGE[key]} — {SLIDE_TITLES.get(key, key)}\n" +
                            "\n".join("- " + l.replace("\n", "\n  ") for l in lines))
    path = seller_prep_path()
    if sections:
        head = (f"SELLER PREP — {FIRM_NAME}\n"
                "For the seller only. Not in the deck; don't forward it to the client.\n\n")
        if os.path.dirname(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(head + "\n\n".join(sections) + "\n")
    elif os.path.exists(path):
        os.remove(path)


def _quote(text):
    return "“" + str(text).strip().strip('"“”') + "”"


# ── Quotes: verbatim, attributed, never repeated ──────────────────

def deck_quotes():
    """Every client quote on the deck: (slide key, where, text, said_by)."""
    out = []
    if KPI_FOCUS.get("headline_is_quote"):
        out.append(("priorities", "KPI headline", KPI_FOCUS.get("headline"), KPI_FOCUS.get("said_by")))
    for i, q in enumerate(PROSPECT_QUOTES or []):
        if q and len(q) >= 2 and q[1]:
            out.append(("priorities", f"PROSPECT_QUOTES[{i}]", q[1], q[3] if len(q) > 3 else None))
    for name, q in (("CLIENT_WHY", CLIENT_WHY), ("COST_OF_INACTION", COST_OF_INACTION)):
        if q:
            out.append(("priorities", name, q[0], q[2] if len(q) > 2 else None))
    if CLOSING_QUOTE:
        out.append(("investment", "CLOSING_QUOTE", CLOSING_QUOTE[0],
                    CLOSING_QUOTE[1] if len(CLOSING_QUOTE) > 1 else None))
    return out


def _tokens(text):
    return re.findall(r"[a-z0-9]+", str(text).lower().replace("’", "'").replace("'", ""))


def _found_in(segment, hay, slack=3):
    """Is `segment` in `hay` word for word, allowing up to `slack` dropped
    filler words ("you know", "um") inside the quoted stretch?"""
    seg = _tokens(segment)
    if len(seg) < 3:
        return True
    for j, tok in enumerate(hay):
        if tok != seg[0]:
            continue
        k, skipped = j + 1, 0
        ok = True
        for want in seg[1:]:
            while k < len(hay) and hay[k] != want and skipped <= slack:
                k += 1
                skipped += 1
            if k >= len(hay) or hay[k] != want or skipped > slack:
                ok = False
                break
            k += 1
        if ok:
            return True
    return False


def _research_notes_text():
    import glob
    here = os.path.dirname(os.path.abspath(__file__))
    files = sorted(glob.glob(os.path.join(here, "*_Research_Notes.txt")), key=os.path.getmtime)
    return open(files[-1], encoding="utf-8").read() if files else None


def check_quotes(problems):
    if FIRM_NAME == "FIRM NAME HERE":
        return  # the unfilled master template's placeholders
    quotes = deck_quotes()
    seller = [t for t in _tokens(SALES_REP) if len(t) > 2]
    for _, where, text, said_by in quotes:
        if not str(said_by or "").strip():
            problems.append(f'{where}: add who said it ("Full Name (client), 00:00:00").')
        elif (seller and all(t in _tokens(said_by) for t in seller)) or re.search(
                r"\b(seller|smb team|rep)\b", str(said_by), re.I):
            problems.append(f"{where}: said by the seller ({said_by}) — only the client's own words go on the deck.")
    # No quote twice (the closing line is the usual offender).
    for i in range(len(quotes)):
        for j in range(i + 1, len(quotes)):
            a, b = set(_tokens(quotes[i][2])), set(_tokens(quotes[j][2]))
            if a and b and len(a & b) / min(len(a), len(b)) >= 0.6:
                problems.append(f"{quotes[j][1]} repeats {quotes[i][1]} — use a different verbatim line, or None.")
    # Verbatim: every quote (each piece between "…" cuts) must be in the
    # research notes, which carry the transcript lines word for word.
    notes = _research_notes_text()
    if notes is None:
        if FIRM_NAME != "FIRM NAME HERE":
            print("NOTE: no research notes next to this script — verbatim quote check skipped.")
        return
    hay = _tokens(notes)
    for _, where, text, _ in quotes:
        for seg in re.split(r"…|\.\.\.", str(text)):
            if seg.strip() and not _found_in(seg, hay):
                problems.append(f'{where}: "{seg.strip()[:60]}" is not word for word in the research notes '
                                "— copy the client's exact words.")
                break


def attribution_notes():
    by_slide = {}
    for key, _, text, said_by in deck_quotes():
        t = str(text).strip().strip('"“”')
        by_slide.setdefault(key, []).append(f"“{t[:70]}{'…' if len(t) > 70 else ''}” — {said_by}")
    for key, lines in by_slide.items():
        note(key, "Who said the quotes on this slide:\n" + "\n".join(lines))


def _base_name(name):
    return re.sub(r"\s*\(\d+ seats?\)$", "", str(name)).strip()


_TIMELINE = re.compile(r"\b\d+\s*(?:-|to|–)?\s*\d*\s*(?:days?|weeks?|months?|years?|quarters?)\b|"
                       r"\b(?:day|week|month|year|quarter)\s+\d+\b|\bQ[1-4]\b", re.I)


def check_roadmap(problems):
    """The roadmap is direction, not a quote: 3 phases, phase 1 is exactly
    the package being priced, later phases add what the firm doesn't have,
    and no prices or timelines anywhere on it."""
    if not isinstance(ROADMAP, (list, tuple)) or len(ROADMAP) != 3:
        problems.append("ROADMAP needs exactly 3 phases.")
        return
    for i, p in enumerate(ROADMAP):
        if not isinstance(p, dict):
            problems.append(f"ROADMAP[{i}] must be a dict.")
            return
        for k in ("phase", "when", "unlocks"):
            if not str(p.get(k) or "").strip():
                problems.append(f'ROADMAP[{i}]["{k}"] is empty.')
        if not 2 <= len(p.get("items") or []) <= 4:
            problems.append(f'ROADMAP[{i}]["items"] needs 2–4 bullets.')
        if not [x for x in (p.get("products") or []) if str(x).strip()]:
            problems.append(f'ROADMAP[{i}]["products"] is empty.')
        text = " ".join([str(p.get(k) or "") for k in ("phase", "when", "unlocks")] +
                        [str(x) for x in (p.get("items") or [])])
        if "$" in text:
            problems.append(f"ROADMAP[{i}] shows a price — the roadmap never quotes one "
                            "(phase 1 is priced on the investment slide; later phases are scoped when the firm gets there).")
        m = _TIMELINE.search(text)
        if m:
            problems.append(f'ROADMAP[{i}] has a timeline ("{m.group(0)}") — phases start at a milestone, never a date.')
    seen = set()
    for i, p in enumerate(ROADMAP[1:], start=2):
        names = {_base_name(x) for x in p.get("products") or []}
        if names & seen:
            problems.append(f"ROADMAP phase {i} repeats {', '.join(sorted(names & seen))} from an earlier phase.")
        seen |= names
    inv = load_decision().get("investment") or {}
    package = {_base_name(x.get("name")) for x in inv.get("products") or [] if x.get("name")}
    if package and FIRM_NAME != "FIRM NAME HERE":
        phase1 = {_base_name(x) for x in ROADMAP[0].get("products") or []}
        if phase1 != package:
            problems.append("ROADMAP phase 1 products must be exactly the package on the investment slide "
                            f"({', '.join(sorted(package))}); got {', '.join(sorted(phase1)) or 'none'}.")
        later = seen & package
        if later:
            problems.append(f"ROADMAP phases 2–3 list {', '.join(sorted(later))}, which is already in the package.")


def validate_fill():
    """Stop the build on structural mistakes instead of drawing a broken
    slide. Content rules (sources, exact figures) live in audit-pptx.md."""
    problems = []
    kind = KPI_FOCUS.get("kind")
    if kind not in ("kpi", "qualitative"):
        problems.append('KPI_FOCUS["kind"] must be "kpi" or "qualitative".')
    for key in ("label", "headline", "detail"):
        if not str(KPI_FOCUS.get(key) or "").strip():
            problems.append(f'KPI_FOCUS["{key}"] is empty.')
    if kind == "qualitative" and not str(seller_note("priorities") or "").strip():
        problems.append('KPI_FOCUS is "qualitative": SELLER_NOTES["priorities"] must tell the '
                        "seller there was no usable number on the call and what to ask for.")
    if STAIRCASE is not None:
        if not isinstance(STAIRCASE, dict):
            problems.append('STAIRCASE must be None or {"current": N or None, "goal": N or None}.')
        else:
            for k in ("current", "goal"):
                v = STAIRCASE.get(k)
                if v is not None and v not in range(1, 9):
                    problems.append(f'STAIRCASE["{k}"] must be a stage 1–8 or None.')
    for name, val in (("CLIENT_WHY", CLIENT_WHY), ("COST_OF_INACTION", COST_OF_INACTION)):
        if val is not None and not (isinstance(val, (tuple, list)) and val and str(val[0]).strip()):
            problems.append(f"{name} must be None or (quote, speaker_label).")
    if not 3 <= len(DIAGNOSIS) <= 4:
        problems.append(f"DIAGNOSIS has {len(DIAGNOSIS)} causes; slide 2 needs 3 or 4.")
    if not 3 <= len(PLAN) <= 4:
        problems.append(f"PLAN has {len(PLAN)} actions; slide 3 needs 3 or 4.")
    for i, p in enumerate(PLAN):
        if not isinstance(p.get("fixes"), int) or not 1 <= p["fixes"] <= len(DIAGNOSIS):
            problems.append(f'PLAN[{i}]["fixes"] must be a DIAGNOSIS number (1–{len(DIAGNOSIS)}).')
        if not 1 <= len(p.get("actions") or []) <= 4:
            problems.append(f'PLAN[{i}]["actions"] needs 1–4 bullets.')
    covered = {p.get("fixes") for p in PLAN}
    for n in range(1, len(DIAGNOSIS) + 1):
        if n not in covered:
            problems.append(f"DIAGNOSIS {n} has no PLAN action — every cause needs a fix.")
    if not 1 <= len(STRATEGY) <= 3:
        problems.append(f"STRATEGY has {len(STRATEGY)} pieces; slide 4 needs 1–3.")
    for label, items in (("DIAGNOSIS", DIAGNOSIS), ("PLAN", PLAN)):
        for i, d in enumerate(items):
            t = d.get("target")
            if t and re.match(r"\s*target\s*:", str(t), re.I):
                problems.append(f'{label}[{i}]["target"] starts with "Target:" — the engine adds it.')
    if not isinstance(PROFITOS_GOALS, (list, tuple)) or len(PROFITOS_GOALS) > 3:
        problems.append("PROFITOS_GOALS must be a list of up to 3 (heading, line) pairs.")
    else:
        for i, g in enumerate(PROFITOS_GOALS):
            if not (isinstance(g, (tuple, list)) and len(g) == 2 and all(str(x).strip() for x in g)):
                problems.append(f"PROFITOS_GOALS[{i}] must be (heading, line).")
            elif len(str(g[0])) > 28 or len(str(g[1])) > 90:
                problems.append(f"PROFITOS_GOALS[{i}]: heading ≤28 chars, line ≤90 chars.")
    if PROFITOS_WHY is not None and not (str(PROFITOS_WHY).strip() and len(str(PROFITOS_WHY)) <= 160):
        problems.append("PROFITOS_WHY must be None or one sentence of ≤160 chars.")
    check_roadmap(problems)
    check_quotes(problems)
    if problems:
        raise SystemExit("Deck not built — fix the values above the LAYOUT ENGINE line:\n  - " + "\n  - ".join(problems))


# ── Cover: Growth, Profit, and Freedom Roadmap ────────────────────
# The name the marketing CTA uses — the cover ties the deck back to it.

COVER_NAME = "Growth, Profit, and Freedom Roadmap"
_MONTHS = ("January|February|March|April|May|June|July|August|September|"
           "October|November|December")


def deck_date():
    """The audit date from the output file name ("…_November 17, 2026_Proposal.pptx"
    or "…_November_17_2026_…"), or None when the name doesn't carry one."""
    m = re.search(rf"({_MONTHS})[ _]+(\d{{1,2}}),?[ _]+(\d{{4}})", os.path.basename(OUTPUT_PATH))
    return f"{m.group(1)} {int(m.group(2))}, {m.group(3)}" if m else None


def build_cover(prs):
    slide = new_slide(prs)
    add_rect(slide, 0, 0, 10, 5.625, fill=NAVY)
    add_rect(slide, 0, 5.555, 10, 0.07, fill=LIME_GREEN)
    if LOGO_PATH and os.path.isfile(LOGO_PATH):
        from pptx.util import Emu as E
        from PIL import Image
        lw, lh = Image.open(LOGO_PATH).size
        slide.shapes.add_picture(LOGO_PATH, E(int(0.60 * 914400)), E(int(0.55 * 914400)),
                                 E(int(1.70 * 914400)), E(int(1.70 * lh / lw * 914400)))
    add_text(slide, "YOUR PERSONALIZED PROPOSAL", 0.60, 1.62, 8.0, 0.24, 9, LIME_GREEN,
             bold=True, fit=False)
    add_text(slide, COVER_NAME, 0.60, 1.90, 8.60, 1.30, 34, WHITE, bold=True,
             max_lines=2, min_size=26)
    add_rect(slide, 0.62, 3.30, 0.90, 0.04, fill=OCEAN_BLUE)
    add_text(slide, FIRM_NAME, 0.60, 3.42, 8.60, 0.70, 22, NAVY_TEXT_SOFT, bold=True,
             max_lines=2, min_size=14, anchor=MSO_ANCHOR.TOP, cap_label="cover firm name")
    date = deck_date()
    add_rich_text(slide, [([("Prepared by ", 9, False, False, NAVY_TEXT_SOFT),
                            (f"{SALES_REP} | SMB Team", 9, True, False, WHITE)], 0),
                          ([((f"{date}  ·  " if date else "") + "CONFIDENTIAL", 7.5, True, False,
                             NAVY_TEXT_SOFT)], 2)],
                  0.60, 4.45, 6.0, 0.60, label="cover prepared by")


# ── Slide 1: Your Priorities, In Your Words ───────────────────────

def build_priorities(prs):
    slide = new_slide(prs)
    add_header(slide, "Your Priorities, In Your Words", 9.30, kicker="WHAT WE HEARD")
    quotes = [q for q in PROSPECT_QUOTES[:3] if q and len(q) >= 2 and q[1]]
    voice = [(lab, v, col) for lab, v, col in
             (("WHY IT MATTERS TO YOU", CLIENT_WHY, LIME_GREEN),
              ("IF NOTHING CHANGES", COST_OF_INACTION, CORAL))
             if v and str(v[0]).strip()]

    # With the client's why / cost of inaction there's a bottom row for them,
    # so the KPI card and quote cards get shorter and quotes cap at two.
    x, y = 0.30, 1.08
    h = 2.56 if voice else 4.00
    if voice:
        quotes = quotes[:2]
    w = 4.60 if quotes else 9.40
    compact = bool(voice)

    # Left (full width with no quotes): the one number from the call.
    add_rect(slide, x, y, w, h, fill=NAVY)
    add_pill(slide, KPI_FOCUS["label"], x + 0.24, y + (0.18 if compact else 0.24), 0.27,
             OCEAN_BLUE, max_w=w - 0.48)
    headline = KPI_FOCUS["headline"]
    if KPI_FOCUS.get("headline_is_quote"):
        headline = _quote(headline)
    hl_top = y + (0.52 if compact else 0.64)
    hl_h, hl_size, hl_lines = (0.86, 19, 2) if compact else (1.40, 22, 3)
    add_text(slide, headline, x + 0.18, hl_top, w - 0.36, hl_h, hl_size, WHITE,
             bold=True, max_lines=hl_lines, min_size=13, anchor=MSO_ANCHOR.TOP,
             cap_label="KPI_FOCUS headline")
    # The detail line sits right under the headline, however many lines it took.
    h_size, h_lines = fit_text(headline, w - 0.36, hl_h, hl_size, bold=True,
                               max_lines=hl_lines, min_size=13)
    used = (len(h_lines) * line_height(h_size, bold=True) + 2 * _INSET_Y) if h_lines else hl_h
    stats = [s for s in (KPI_FOCUS.get("stats") or [])[:2] if s and s[1]]
    rule_y = y + h - (0.98 if not compact else 0.74)
    detail_top = hl_top + used + (0.06 if compact else 0.12)
    add_text(slide, KPI_FOCUS["detail"], x + 0.18, detail_top, w - 0.36,
             max(0.30, (rule_y if stats else y + h - 0.10) - detail_top - 0.04),
             10 if compact else 10.5, NAVY_TEXT_SOFT, max_lines=3, min_size=8,
             cap_label="KPI_FOCUS detail")
    if stats:
        add_rule(slide, x + 0.24, rule_y, x + w - 0.24, rule_y, NAVY_RULE)
        col = (w - 0.36) / len(stats)
        for i, (lab, val) in enumerate(stats):
            sx = x + 0.18 + i * col
            add_text(slide, str(lab).upper(), sx, rule_y + 0.08, col - 0.08, 0.22, 7.5,
                     LIME_GREEN, bold=True, max_lines=1, cap_label=f"KPI stat {i+1} label")
            add_text(slide, val, sx, rule_y + 0.28, col - 0.08, (y + h) - (rule_y + 0.30), 10,
                     WHITE, max_lines=2, min_size=8, cap_label=f"KPI stat {i+1} value")

    # Right: the client's other priorities, one card each.
    if quotes:
        qx, qw, gap = 5.08, 4.62, 0.12
        ch = (h - gap * (len(quotes) - 1)) / len(quotes)
        for i, q in enumerate(quotes):
            topic, text = q[0], q[1]
            tie = q[2] if len(q) > 2 else ""
            cy = y + i * (ch + gap)
            add_rect(slide, qx, cy, qw, ch, fill=WHITE)
            add_rect(slide, qx, cy, 0.06, ch, fill=OCEAN_BLUE)
            add_text(slide, str(topic).upper(), qx + 0.20, cy + 0.10, qw - 0.34, 0.22,
                     7.5, OCEAN_BLUE, bold=True, max_lines=1,
                     cap_label=f"PROSPECT_QUOTES[{i}] topic")
            tie_h = 0.30 if tie else 0
            add_text(slide, _quote(cap(str(text).strip().strip('"“”'), 130,
                                       f"PROSPECT_QUOTES[{i}] quote")),
                     qx + 0.20, cy + 0.30, qw - 0.34, ch - 0.38 - tie_h, 11, DARK_TEXT,
                     min_size=8.5, cap_label=f"PROSPECT_QUOTES[{i}] quote")
            if tie:
                add_text(slide, tie, qx + 0.20, cy + ch - 0.36, qw - 0.34, 0.28, 8.5,
                         NAVY, bold=True, max_lines=1, min_size=7.5, cap_chars=80,
                         cap_label=f"PROSPECT_QUOTES[{i}] tie line")

    # Bottom row: their why, and what happens if nothing changes — their words.
    if voice:
        vy, vh, gap = y + h + 0.12, 5.12 - (y + h + 0.12), 0.20
        vw = (9.40 - gap * (len(voice) - 1)) / len(voice)
        for i, (label, quote_fill, accent) in enumerate(voice):
            text, who = quote_fill[0], (quote_fill[1] if len(quote_fill) > 1 else "")
            vx = 0.30 + i * (vw + gap)
            add_rect(slide, vx, vy, vw, vh, fill=WHITE)
            add_rect(slide, vx, vy, vw, 0.05, fill=accent)
            kicker = label + (f"  ·  {str(who).upper()}" if who else "")
            add_text(slide, kicker, vx + 0.18, vy + 0.12, vw - 0.36, 0.20, 7.5,
                     GREEN if accent == LIME_GREEN else CORAL, bold=True, max_lines=1,
                     cap_label=f"{label} kicker")
            add_text(slide, _quote(cap(str(text).strip().strip('"“”'), 150, label)),
                     vx + 0.18, vy + 0.34, vw - 0.36, vh - 0.42, 12, NAVY, bold=True,
                     italic=False, max_lines=3, min_size=9, anchor=MSO_ANCHOR.MIDDLE,
                     cap_label=label)

    if KPI_FOCUS.get("kind") == "qualitative":
        note("priorities", "No usable number came out of the call, so this slide leads with the "
                "client's pain point instead of a KPI.")
    add_footer(slide, PAGE["priorities"], TOTAL_SLIDES, LOGO_PATH)


# ── Optional: Lawyer Legacy Staircase ─────────────────────────────
# The original SMB Team staircase graphic, rebuilt as native shapes so every
# number and label is editable text. Colors are sampled from that graphic.

STAIR_NAMES = {1: "Law Student", 2: "Lawyer", 3: "Solo Practitioner",
               4: "Small Business Manager", 5: "Law Firm CEO", 6: "Law Firm Owner",
               7: "Freedom Entrepreneur", 8: "Wealth Multiplier"}
STAIR_COLORS = {1: "053C5B", 2: "125072", 3: "16658D", 4: "147DAD",
                5: "1F95C3", 6: "3DA1A4", 7: "55AC81", 8: "6DBC4E"}
STAIR_NAVY = rgb("053A59")
STAIR_GREEN = rgb("71BF44")
ABYSS_RED = rgb("ED1C24")
LEAP_GRAY = rgb("818285")
HERE_YELLOW = rgb("FFDB4F")


def _line(slide, x1, y1, x2, y2, color, pt, dash=False, arrow=False):
    from pptx.enum.shapes import MSO_CONNECTOR
    from pptx.util import Emu as E, Pt as P
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(int(x1*914400)), E(int(y1*914400)),
                                   E(int(x2*914400)), E(int(y2*914400)))
    c.line.color.rgb = color
    c.line.width = P(pt)
    if dash:
        c.line.dash_style = MSO_LINE.DASH
    if arrow:
        ln = c.line._get_or_add_ln()
        tail = etree.SubElement(ln, qn("a:tailEnd"))
        tail.set("type", "triangle"); tail.set("w", "med"); tail.set("len", "med")
    return c


def build_staircase(prs):
    slide = new_slide(prs)
    add_rect(slide, 0, 0, 10, 5.625, fill=WHITE)
    add_text(slide, f"WHERE YOU ARE  ·  {FIRM_NAME.upper()}", 0.32, 0.16, 6.0, 0.18, 7.5,
             rgb("147DAD"), bold=True, max_lines=1, cap_label="staircase kicker")
    add_text(slide, "LAWYER LEGACY STAIRCASE", 0.30, 0.28, 9.40, 0.52, 24, STAIR_NAVY,
             bold=True, align=PP_ALIGN.CENTER, max_lines=1, min_size=18)

    cur = (STAIRCASE or {}).get("current")
    goal = (STAIRCASE or {}).get("goal")
    right, left0, dx = 7.05, 1.05, 0.40
    bar_h, gap, base = 0.36, 0.05, 4.74
    tops = {}
    for n in range(1, 9):
        top = base - n * bar_h - (n - 1) * gap
        lx = left0 + (n - 1) * dx
        tops[n] = (lx, top)
        add_rect(slide, lx, top, right - lx, bar_h, fill=rgb(STAIR_COLORS[n]))
        add_text(slide, STAIR_NAMES[n].upper(), lx + 0.10, top, right - lx - 0.20, bar_h,
                 12.5, WHITE, bold=True, max_lines=1, min_size=9, anchor=MSO_ANCHOR.MIDDLE,
                 cap_label=f"stage {n} name")
        # Stage number: its own text box, editable like everything else.
        add_text(slide, str(n), lx - 0.40, top - 0.02, 0.36, bar_h + 0.04, 18,
                 rgb(STAIR_COLORS[n]) if n != 1 else STAIR_NAVY, bold=True,
                 align=PP_ALIGN.RIGHT, fit=False, anchor=MSO_ANCHOR.MIDDLE)

    # The green climb line hugging each step, with an arrow out of the top.
    for n in range(1, 9):
        lx, top = tops[n]
        x = lx - 0.045
        _line(slide, x, top + bar_h + (0.03 if n == 1 else gap / 2), x, top - gap / 2,
              STAIR_GREEN, 2.75)
        if n < 8:
            nx = tops[n + 1][0] - 0.045
            _line(slide, x, top - gap / 2, nx, top - gap / 2, STAIR_GREEN, 2.75)
    lx8, top8 = tops[8]
    _line(slide, lx8 - 0.045, top8 - gap / 2, lx8 + 0.55, top8 - gap / 2, STAIR_GREEN, 2.75)
    _line(slide, lx8 + 0.55, top8 - gap / 2, lx8 + 0.55, top8 - 0.30, STAIR_GREEN, 2.75, arrow=True)
    _line(slide, left0 - 0.30, base + 0.03, left0 - 0.045, base + 0.03, STAIR_GREEN, 2.75)

    # The Leap (between 2 and 3) and the Abyss (between 4 and 5).
    leap_y = tops[2][1] - gap / 2
    _line(slide, 0.35, leap_y, right + 0.25, leap_y, LEAP_GRAY, 1.5)
    add_text(slide, "THE LEAP", 0.30, leap_y - 0.24, 1.20, 0.22, 8, LEAP_GRAY, bold=True,
             fit=False)
    abyss_y = tops[4][1] - gap / 2
    _line(slide, 0.30, abyss_y, 9.70, abyss_y, ABYSS_RED, 3.25, dash=True)
    add_text(slide, "THE ABYSS", 7.42, abyss_y + 0.04, 2.30, 0.34, 15, ABYSS_RED, bold=True,
             fit=False)
    add_text(slide, "More revenue, but more of it runs through you.", 7.42, abyss_y + 0.36,
             2.30, 0.44, 8.5, LEAP_GRAY, max_lines=2, min_size=7, cap_label="abyss below")
    # The far side of the Abyss: more profit and more freedom.
    add_shape(slide, MSO_SHAPE.UP_ARROW, 7.48, tops[7][1] + 0.05, 0.34, abyss_y - tops[7][1] - 0.14,
              fill=STAIR_GREEN)
    add_text(slide, "MORE PROFIT", 7.90, tops[7][1] + 0.02, 1.85, 0.34, 14, rgb("3F8F1A"),
             bold=True, max_lines=1, min_size=10)
    add_text(slide, "+ MORE FREEDOM", 7.90, tops[7][1] + 0.34, 1.85, 0.34, 14, rgb("3F8F1A"),
             bold=True, max_lines=1, min_size=10)
    add_text(slide, "The firm runs without you in every decision.", 7.90, tops[7][1] + 0.68,
             1.85, 0.44, 8.5, STAIR_NAVY, max_lines=2, min_size=7, cap_label="abyss above")

    # Time axis.
    _line(slide, left0, base + 0.14, right, base + 0.14, LEAP_GRAY, 1)
    add_text(slide, "TIME", left0, base + 0.16, 1.0, 0.30, 11, STAIR_NAVY, bold=True, fit=False)

    # You are here / your goal — only when discussed on the call.
    def marker(n, text, fill, color):
        lx, top = tops[n]
        w = text_width(text, 10, bold=True) + 0.34
        px = right - w - 0.10
        pill = add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, px, top + 0.04, w, bar_h - 0.08, fill=fill)
        pill.adjustments[0] = 0.5
        add_text(slide, text, px, top + 0.04, w, bar_h - 0.08, 10, color, bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, fit=False)
        add_shape(slide, MSO_SHAPE.LEFT_ARROW, px - 0.42, top + 0.09, 0.36, bar_h - 0.18, fill=fill)
    if cur:
        marker(cur, "You Are Here!", HERE_YELLOW, rgb("114E6E"))
    if goal and goal != cur:
        marker(goal, "Your Goal", STAIR_GREEN, WHITE)

    note("staircase", "Optional slide: it's here because the Legacy Staircase came up on the call. "
         "Delete it if you won't walk through it." +
         ("" if cur else " The client's stage wasn't placed on the call, so no 'You Are Here' marker is shown."))
    add_footer(slide, PAGE["staircase"], TOTAL_SLIDES, LOGO_PATH)


# ── Slide 2: The Diagnosis ────────────────────────────────────────

def build_diagnosis(prs):
    slide = new_slide(prs)
    add_header(slide, DIAGNOSIS_TITLE, 9.30, kicker="THE DIAGNOSIS")

    add_rect(slide, 0.30, 1.08, 9.40, 0.40, fill=NAVY)
    add_text(slide, DIAGNOSIS_INTRO, 0.48, 1.08, 9.04, 0.40, 11, WHITE, bold=True,
             max_lines=1, min_size=8.5, anchor=MSO_ANCHOR.MIDDLE, cap_label="DIAGNOSIS_INTRO")

    n = len(DIAGNOSIS)
    gap = 0.15
    cw = (9.40 - gap * (n - 1)) / n
    y, h = 1.60, 2.94
    for i, d in enumerate(DIAGNOSIS):
        cx = 0.30 + i * (cw + gap)
        add_rect(slide, cx, y, cw, h, fill=WHITE)
        add_badge(slide, i + 1, cx + 0.14, y + 0.15, 0.30, OCEAN_BLUE)
        add_text(slide, d["title"], cx + 0.50, y + 0.08, cw - 0.60, 0.46, 10, NAVY,
                 bold=True, max_lines=2, min_size=8, anchor=MSO_ANCHOR.MIDDLE,
                 cap_label=f"DIAGNOSIS[{i}] title")
        cy = y + 0.62
        if d.get("metric"):
            add_text(slide, d["metric"], cx + 0.08, cy, cw - 0.16, 0.50, 26, CORAL,
                     bold=True, max_lines=1, min_size=14, cap_label=f"DIAGNOSIS[{i}] metric")
            cy += 0.50
            if d.get("metric_label"):
                add_text(slide, d["metric_label"], cx + 0.08, cy, cw - 0.16, 0.40, 9,
                         DARK_TEXT, bold=True, max_lines=2, min_size=7.5,
                         cap_label=f"DIAGNOSIS[{i}] metric_label")
                lines = len(fit_text(d["metric_label"], cw - 0.16, 0.40, 9, bold=True,
                                     max_lines=2, min_size=7.5)[1] or [1])
                cy += 0.06 + 0.20 * lines
        if d.get("target"):
            add_text(slide, "Target: " + str(d["target"]), cx + 0.08, cy, cw - 0.16, 0.24,
                     8.5, GREEN, bold=True, max_lines=1, min_size=7,
                     cap_label=f"DIAGNOSIS[{i}] target")
            cy += 0.28
        add_text(slide, d["body"], cx + 0.08, cy + 0.02, cw - 0.16, (y + h - 0.30) - (cy + 0.02),
                 9.5, BODY_TEXT, min_size=8, cap_chars=100, cap_label=f"DIAGNOSIS[{i}] body")
        if d.get("source"):
            add_text(slide, "Source: " + str(d["source"]), cx + 0.08, y + h - 0.28,
                     cw - 0.16, 0.22, 7, SLATE, max_lines=1, min_size=6,
                     cap_label=f"DIAGNOSIS[{i}] source")

    add_strip(slide, "How we fix it:", DIAGNOSIS_FIX_LINE, 4.64, label="DIAGNOSIS_FIX_LINE")
    add_footer(slide, PAGE["diagnosis"], TOTAL_SLIDES, LOGO_PATH)


# ── Slide 3: The Plan ─────────────────────────────────────────────

def build_plan(prs):
    slide = new_slide(prs)
    kicker = "THE PLAN" + (f"  ·  {PLAN_KICKER.upper()}" if PLAN_KICKER else "")
    add_header(slide, PLAN_TITLE, 9.30, kicker=kicker)

    n = len(PLAN)
    gap = 0.15
    cw = (9.40 - gap * (n - 1)) / n
    y = 1.08
    h = 2.30 if PLAN_NOTE else 2.74   # leaves the measure row ~1in either way
    for i, p in enumerate(PLAN):
        cx = 0.30 + i * (cw + gap)
        add_rect(slide, cx, y, cw, 0.62, fill=NAVY)
        add_badge(slide, i + 1, cx + 0.14, y + 0.15, 0.32, OCEAN_BLUE)
        add_text(slide, p["title"], cx + 0.52, y + 0.03, cw - 0.60, 0.56, 11, WHITE,
                 bold=True, max_lines=2, min_size=8.5, anchor=MSO_ANCHOR.MIDDLE,
                 cap_label=f"PLAN[{i}] title")
        add_rect(slide, cx, y + 0.62, cw, h - 0.62, fill=WHITE)

        fixes = p["fixes"]
        cause = DIAGNOSIS[fixes - 1]["title"]
        add_text(slide, f"FIXES  {fixes}  ·  {cause.upper()}", cx + 0.10, y + 0.68,
                 cw - 0.20, 0.34, 7, CORAL, bold=True, max_lines=2, min_size=6,
                 cap_label=f"PLAN[{i}] fixes")
        add_text(slide, "WHAT WE DO", cx + 0.10, y + 1.02, cw - 0.20, 0.20, 7,
                 OCEAN_BLUE, bold=True, fit=False)
        add_bullets(slide, [cap(a, 70, f"PLAN[{i}] action {j+1}")
                            for j, a in enumerate(p["actions"][:4])],
                    cx + 0.08, y + 1.20, cw - 0.16, h - 1.26, 9,
                    DARK_TEXT, OCEAN_BLUE, label=f"PLAN[{i}] actions")

    build_measures(slide, top=y + h + 0.06, bottom=4.62 if PLAN_NOTE else 5.12)

    if PLAN_NOTE:
        add_strip(slide, "Also included:", PLAN_NOTE, 4.70, h=0.42, label="PLAN_NOTE")
    missing = [f"“{p['title']}” ({p['metric']})" for p in PLAN if not p.get("target")]
    if missing:
        note("plan", "No target on the call to base these on, so none is shown — agree a "
                "number with the client rather than quoting one: " + "; ".join(missing) + ".")
    add_footer(slide, PAGE["plan"], TOTAL_SLIDES, LOGO_PATH)


_METRIC_STOP = {"the", "a", "an", "per", "of", "to", "your", "each", "a", "monthly", "month", "today"}


def _metric_tokens(text):
    return {t for t in re.findall(r"[a-z0-9]+", str(text).lower()) if t not in _METRIC_STOP}


_METRIC_QUALIFIERS = {"retained", "signed", "new", "average", "avg", "overall", "total"}


def same_metric(a, b):
    """True when two metric names are the same measure ("Cost per client" /
    "Cost per retained client") — but not a narrower one ("Meta cost per
    client" is its own metric)."""
    ta = _metric_tokens(a) - _METRIC_QUALIFIERS
    tb = _metric_tokens(b) - _METRIC_QUALIFIERS
    return bool(ta) and ta == tb


def build_measures(slide, top, bottom):
    """"What we'll measure": the call KPI (today's value, plus its target if
    a plan action targets it), then the measure for each other action,
    labelled with that action, showing its target — or, with no target,
    today's value. A measure with neither, or that repeats the KPI, is left
    out; there are no numbers, so nothing is ever skipped."""
    add_text(slide, "WHAT WE'LL MEASURE", 0.30, top, 4.0, 0.20, 7.5, NAVY, bold=True,
             fit=False)
    kpi_sub = ("Today: " + KPI_FOCUS["baseline"]) if KPI_FOCUS.get("baseline") else ""
    tiles = []
    for p in PLAN:
        if same_metric(p["metric"], KPI_FOCUS["label"]):
            if p.get("target"):
                kpi_sub = (kpi_sub + "  ·  " if kpi_sub else "") + "Target: " + str(p["target"])
            continue
        if p.get("target"):
            tiles.append((p["title"], p["metric"], "Target: " + str(p["target"]), True))
        elif p.get("baseline"):
            tiles.append((p["title"], p["metric"], "Today: " + str(p["baseline"]), False))
    tiles = [(None, KPI_FOCUS["label"], kpi_sub, False)] + tiles
    gap = 0.12
    ty = top + 0.22
    th = bottom - ty
    tw = min(2.80, (9.40 - gap * (len(tiles) - 1)) / len(tiles))
    for i, (action, title, sub, is_target) in enumerate(tiles):
        tx = 0.30 + i * (tw + gap)
        lead = action is None
        add_rect(slide, tx, ty, tw, th, fill=NAVY if lead else WHITE)
        if not lead:
            add_rect(slide, tx, ty, tw, 0.04, fill=OCEAN_BLUE)
        kicker = "THE NUMBER FROM THE CALL" if lead else str(action).upper()
        add_text(slide, kicker, tx + 0.10, ty + 0.07, tw - 0.20, 0.18, 6.5,
                 LIME_GREEN if lead else OCEAN_BLUE, bold=True, max_lines=1, min_size=5.5,
                 cap_label="measure kicker")
        add_text(slide, title, tx + 0.10, ty + 0.24, tw - 0.20, 0.38, 9.5,
                 WHITE if lead else NAVY, bold=True, max_lines=2, min_size=7.5,
                 cap_label=f"measure tile {i+1}")
        if sub:
            sub_y = ty + 0.62
            add_text(slide, sub, tx + 0.10, sub_y, tw - 0.20, max(0.22, ty + th - sub_y - 0.04),
                     8.5, NAVY_TEXT_SOFT if lead else (GREEN if is_target else DARK_TEXT),
                     bold=not lead, max_lines=2, min_size=7, cap_label=f"measure tile {i+1} sub")


# ── Slide 4: The Recommended Strategy ─────────────────────────────

def build_strategy(prs):
    slide = new_slide(prs)
    add_header(slide, STRATEGY_TITLE, 9.30, kicker="THE RECOMMENDED STRATEGY")

    n = len(STRATEGY)
    gap = 0.25
    cw = (9.40 - gap * (n - 1)) / n
    y, h = 1.08, 2.80
    for i, s in enumerate(STRATEGY):
        cx = 0.30 + i * (cw + gap)
        add_rect(slide, cx, y, cw, h, fill=WHITE)
        add_rect(slide, cx, y, cw, 0.05, fill=OCEAN_BLUE)
        add_badge(slide, i + 1, cx + 0.18, y + 0.22, 0.34, NAVY)
        add_text(slide, str(s["title"]).upper(), cx + 0.60, y + 0.18, cw - 0.74, 0.42,
                 12.5, NAVY, bold=True, max_lines=1, min_size=9, anchor=MSO_ANCHOR.MIDDLE,
                 cap_label=f"STRATEGY[{i}] title")
        add_text(slide, s["channels"], cx + 0.14, y + 0.62, cw - 0.28, 0.22, 8.5,
                 OCEAN_BLUE, bold=True, max_lines=1, min_size=7,
                 cap_label=f"STRATEGY[{i}] channels")
        add_text(slide, client_name(s["product"]), cx + 0.14, y + 0.84, cw - 0.28, 0.22, 8, SLATE,
                 max_lines=1, min_size=6.5, cap_label=f"STRATEGY[{i}] product")
        add_bullets(slide, [cap(b, 70, f"STRATEGY[{i}] deliverable {j+1}")
                            for j, b in enumerate(s["deliverables"][:5])],
                    cx + 0.10, y + 1.12, cw - 0.20, h - 1.22, 9.5, DARK_TEXT, OCEAN_BLUE,
                    label=f"STRATEGY[{i}] deliverables")

    add_text(slide, "WHY WE CHOSE IT", 0.30, 3.96, 4.0, 0.20, 7.5, SLATE, bold=True,
             fit=False)
    for i, s in enumerate(STRATEGY):
        cx = 0.30 + i * (cw + gap)
        add_rect(slide, cx, 4.18, cw, 0.94, fill=SOFT_BLUE)
        add_text(slide, s["why"], cx + 0.10, 4.20, cw - 0.20, 0.90, 9.5, NAVY,
                 min_size=7.5, anchor=MSO_ANCHOR.MIDDLE, cap_chars=160,
                 cap_label=f"STRATEGY[{i}] why")
    add_footer(slide, PAGE["strategy"], TOTAL_SLIDES, LOGO_PATH)


# ── Rollout Plan (placeholder — left out while SHOW_ROLLOUT is False) ─

def build_rollout(prs):
    slide = new_slide(prs)
    add_header(slide, "Rollout Plan", 9.30, kicker="WHAT HAPPENS AFTER YOU SIGN")

    add_shape(slide, MSO_SHAPE.RECTANGLE, 0.30, 1.10, 9.40, 3.98, fill=WHITE,
              line_color=SLATE, line_pt=1.25, dash=True)
    add_pill(slide, "Placeholder", 0.56, 2.14, 0.28, CORAL)
    add_text(slide, "Your rollout plan is being finalized", 0.50, 2.54, 8.90, 0.46, 18,
             NAVY, bold=True, max_lines=1, min_size=13)
    add_text(slide, "Your onboarding team will fill in what happens after you sign: "
                    "the steps, who does what, and when. Nothing on this slide is a "
                    "commitment or a timeline yet.",
             0.50, 3.04, 8.90, 0.80, 10.5, BODY_TEXT, max_lines=3, min_size=9)

    note("rollout", "PLACEHOLDER: real onboarding content isn't ready yet. Don't promise "
            "onboarding steps, dates or timelines from this slide.")
    add_footer(slide, PAGE["rollout"], TOTAL_SLIDES, LOGO_PATH)

# ── Last slide: Your Investment (numbers from package_decision.json) ──

_SAMPLE_INVESTMENT = {
    "products": [
        {"name": "Full Service Marketing — Growth", "charged": 7497, "standalone": 8997},
    ],
    "monthly_total": 7497, "total_savings": 0, "pricing_mode": "standalone",
    "setup_fees": [{"product": "Full Service Marketing — Growth", "label": "AI Avatar setup",
                    "amount": 1850, "charged": 1850, "waived": False}],
    "setup_total": 1850,
    "year_one_total": 91814,
    "ad_spend": {"conservative": 6700, "aggressive": 25000, "current_stated": None,
                 "year_one_range": [80400, 300000], "cap": 50000, "overage": None},
    "return": {"method": "benchmark_cpl", "share_of_case_value": None,
               "basis": "Sample figures — the firm's package_decision.json supplies the real ones.",
               "disclaimer": "Illustrative arithmetic — not a forecast or guarantee.",
               "scenarios": [
                   {"label": "Conservative", "ad_spend": 6700, "cases": 9.2, "revenue": 27600, "return_multiple": 4.1},
                   {"label": "Aggressive", "ad_spend": 25000, "cases": 41.0, "revenue": 123000, "return_multiple": 4.9}]},
}


def load_investment():
    """The computed investment block. Stops the build when it's missing,
    so a deck never goes out with hand-typed or stale numbers."""
    import json
    if not os.path.isfile(DECISION_PATH):
        if FIRM_NAME == "FIRM NAME HERE":
            return _SAMPLE_INVESTMENT
        raise SystemExit(f"Deck not built — {DECISION_PATH} not found. "
                         "Run: node scripts/reprice.mjs <friendly-name>")
    with open(DECISION_PATH) as f:
        inv = json.load(f).get("investment")
    if not inv or not inv.get("products"):
        raise SystemExit("Deck not built — package_decision.json has no \"investment\" block. "
                         "Run: node scripts/reprice.mjs <friendly-name>")
    return inv


def usd(n):
    return f"${int(round(n)):,}"


def short_usd(n):
    """$25,000 → $25K, $1,250,000 → $1.25M (for tight table cells)."""
    n = float(n)
    if n >= 1_000_000:
        return f"${n / 1_000_000:.2f}".rstrip("0").rstrip(".") + "M"
    if n >= 10_000:
        k = n / 1_000
        return f"${k:.0f}K" if abs(k - round(k)) < 0.05 else f"${k:.1f}K"
    return usd(n)


def product_line(name):
    base = re.sub(r"\s*\(\d+ seats?\)$", "", name)
    line = PRODUCT_LINES.get(name) or PRODUCT_LINES.get(base)
    if not line:
        raise SystemExit(f'Deck not built — PRODUCT_LINES has no entry for "{base}". '
                         "Add one deliverables line per product in package_decision.json.")
    return line


# Product names as the pricing sheet lists them. The package data keeps the
# internal FCFO Advisor / Director / Partner names (the Managed Financials
# slides key off them); anything a client reads shows the sheet's name.
_SHEET_NAMES = [(re.compile(r"\b(?:FCFO|Fractional CFO)\s+(Advisor|Director|Partner)\b"),
                 lambda m: "Managed Financials Level " + {"Advisor": "1", "Director": "2", "Partner": "3"}[m.group(1)])]


def client_name(text):
    """A product name (or a line naming products) as the client should see it."""
    text = str(text)
    for pat, sub in _SHEET_NAMES:
        text = pat.sub(sub, text)
    return text


def build_buys_card(slide, inv, x, w, top, bottom):
    """"What $X/mo buys": one row per product — name, deliverables, price."""
    add_text(slide, f"WHAT {usd(inv['monthly_total'])}/MO BUYS", x, top, w, 0.20, 7.5,
             NAVY, bold=True, fit=False)
    card_top = top + 0.22
    add_rect(slide, x, card_top, w, bottom - card_top, fill=WHITE)
    add_rect(slide, x, card_top, 0.05, bottom - card_top, fill=OCEAN_BLUE)
    rows = inv["products"]
    rh_used = (bottom - card_top - 0.12) / max(1, len(rows))
    y = card_top + 0.06
    standalone_mode = inv.get("pricing_mode") == "standalone"
    # Deliverables as a two-column list only when every row has room for it,
    # so the rows always match.
    def _items(p):
        return [t.strip() for t in re.split(r"\s*[·•|]\s*", product_line(p["name"])) if t.strip()]
    as_list = all(len(_items(p)) >= 3 and rh_used - 0.70 >= ((len(_items(p)) + 1) // 2) * 0.27
                  for p in rows)
    for i, p in enumerate(rows):
        ry = y + i * rh_used
        if i:
            add_rule(slide, x + 0.20, ry, x + w - 0.16, ry, RULE_GRAY)
        name_w = w - 1.85
        add_text(slide, client_name(p["name"]), x + 0.18, ry + 0.06, name_w, 0.30, 10.5, NAVY, bold=True,
                 max_lines=1, min_size=8, cap_label=f"product {i+1} name")
        items = [t.strip() for t in re.split(r"\s*[·•|]\s*", product_line(p["name"])) if t.strip()]
        if as_list:
            # Room to spare: the deliverables as a two-column list, below the
            # price and its stand-alone note.
            half = (len(items) + 1) // 2
            col_w = (w - 0.36) / 2
            box_h = rh_used - 0.70
            size = 10 if len(rows) == 1 else 9
            for c, chunk in enumerate([items[:half], items[half:]]):
                if chunk:
                    add_bullets(slide, chunk, x + 0.14 + c * col_w, ry + 0.62, col_w, box_h,
                                size, DARK_TEXT, OCEAN_BLUE, label=f"product {i+1} deliverables")
        else:
            add_text(slide, " · ".join(items), x + 0.18, ry + 0.34, name_w, rh_used - 0.40,
                     8.5, BODY_TEXT, max_lines=2, min_size=7, cap_label=f"product {i+1} line")
        price = f"{usd(p['charged'])}/mo" if p.get("charged") is not None else "price TBD"
        add_text(slide, price, x + w - 1.70, ry + 0.04, 1.58, 0.34, 13, NAVY, bold=True,
                 align=PP_ALIGN.RIGHT, max_lines=1, min_size=10, cap_label=f"product {i+1} price")
        # The list (stand-alone) price sits right beside the bundle price.
        discounted = (p.get("standalone") and p.get("charged") is not None
                      and p["standalone"] > p["charged"])
        if discounted:
            pw = text_width(price, 13, bold=True) + 2 * _INSET_X
            lw = 1.05
            add_text(slide, usd(p["standalone"]), x + w - 0.12 - pw - lw, ry + 0.08, lw, 0.28,
                     10, SLATE, align=PP_ALIGN.RIGHT, fit=False, strike=True)
            sub = "list price · bundle price"
        elif standalone_mode and p.get("standalone"):
            sub = "list price (no bundle)"
        else:
            sub = ""
        if sub:
            add_text(slide, sub, x + w - 2.20, ry + 0.36, 2.08, 0.22, 7.5, SLATE,
                     align=PP_ALIGN.RIGHT, max_lines=1, fit=False)


def setup_fee_line(f):
    """One setup fee for the slide: "AI Avatar setup $1,850" (or "… waived")."""
    name = f["label"] if f["label"] != "Setup fee" else f"{client_name(f['product'])} setup"
    return f"{name} {usd(f['amount'])}" + (" waived" if f.get("waived") else "")


def build_totals_block(slide, inv, x, w, top, bottom):
    """Navy block: the monthly investment, any one-time setup fees, and the
    year-one total (12 months of fees + the setup fees charged)."""
    h = bottom - top
    add_rect(slide, x, top, w, h, fill=NAVY)
    add_rect(slide, x, top, 0.05, h, fill=LIME_GREEN)
    list_total = inv.get("list_total") or inv["monthly_total"]
    fees = inv.get("setup_fees") or []
    setup_total = inv.get("setup_total") or 0
    cells = [("MONTHLY" if fees else "MONTHLY INVESTMENT", f"{usd(inv['monthly_total'])}/mo",
              (f"List {usd(list_total)}/mo · save {usd(inv['total_savings'])}/mo"
               if inv.get("total_savings") else "List price (no bundle)"))]
    if fees:
        # One fee: its name (the amount is the big number). Several: each
        # with its amount, so they add up on the slide.
        if len(fees) == 1:
            sub = setup_fee_line(fees[0]).rsplit(" $", 1)[0] + (" (waived)" if fees[0].get("waived") else "")
        else:
            short = lambda f: (client_name(f["product"]) if f["label"] == "Setup fee"
                               else f["label"].replace(" setup", "").replace("Video Ads Express ", ""))
            sub = " · ".join(f"{short(f)} {usd(f['amount'])}" + (" waived" if f.get("waived") else "")
                             for f in fees)
            if len(fees) > 2:
                # Too many to list: group the coaching / advisory fees.
                advisory = [f for f in fees if f["label"] == "Setup fee"]
                rest = [f for f in fees if f["label"] != "Setup fee"]
                parts = [f"{short(f)} {usd(f['charged'])}" for f in rest]
                if advisory:
                    parts.append(f"Advisory {usd(sum(f['charged'] for f in advisory))}")
                sub = " · ".join(parts)
        cells.append(("ONE-TIME SETUP", usd(setup_total), sub))
    cells.append(("YEAR ONE", usd(inv["year_one_total"]),
                  "12 months of fees + setup" if setup_total else "12 months of fees"))
    # The monthly figure is the widest; with a setup cell, give it more room.
    shares = ([1] * len(cells) if len(cells) == 2 else
              [0.32, 0.36, 0.32] if len(fees) > 2 else [0.38, 0.28, 0.34])
    widths = [(w - 0.10) * f / sum(shares) for f in shares]
    for i, (kicker, big, sub) in enumerate(cells):
        cw = widths[i]
        cx = x + 0.10 + sum(widths[:i])
        if i:
            add_rule(slide, cx - 0.04, top + 0.14, cx - 0.04, bottom - 0.14, NAVY_RULE)
        add_text(slide, kicker, cx + 0.12, top + 0.10, cw - 0.24, 0.20, 7.5, LIME_GREEN,
                 bold=True, fit=False)
        add_text(slide, big, cx + 0.12, top + 0.28, cw - 0.24, 0.42, 20, WHITE, bold=True,
                 max_lines=1, min_size=13, cap_label=f"total {i+1}")
        add_text(slide, sub, cx + 0.12, top + 0.68, cw - 0.24, h - 0.74, 8, BUNDLE_SAVINGS_TEXT
                 if i == 0 else NAVY_TEXT_SOFT, max_lines=3 if len(fees) > 2 else 2, min_size=6.5,
                 cap_label=f"total {i+1} sub")


def build_ad_spend_card(slide, ad, x, w, top, bottom):
    h = bottom - top
    add_rect(slide, x, top, w, h, fill=WHITE)
    add_rect(slide, x, top, w, 0.05, fill=OCEAN_BLUE)
    add_text(slide, "RECOMMENDED AD SPEND", x + 0.18, top + 0.12, w - 0.36, 0.20, 7.5,
             OCEAN_BLUE, bold=True, fit=False)
    lo, hi = ad["conservative"], ad["aggressive"]
    rng = f"{usd(lo)}/mo" if lo == hi else f"{usd(lo)} – {usd(hi)}/mo"
    add_text(slide, rng, x + 0.18, top + 0.32, w - 0.36, 0.46, 22, NAVY, bold=True,
             max_lines=1, min_size=14, cap_label="ad spend range")
    cur = ad.get("current_stated")
    if cur:
        line = f"Today: {usd(cur)}/mo, held at launch" + (f" · up to {usd(ad['cap'])} managed" if ad.get("cap") else "")
    elif cur == 0:
        line = "Today: no paid ads. Starts at the channel minimums."
    else:
        line = "Starts at the channel minimums for your practice area."
    add_text(slide, line, x + 0.18, top + 0.80, w - 0.36, 0.24, 8.5, DARK_TEXT, bold=True,
             max_lines=1, min_size=7, cap_label="ad spend today")
    why = (AD_SPEND_WHY or "").strip()
    y1 = ad.get("year_one_range") or [lo * 12, hi * 12]
    tail = f"Paid directly to Google and Meta. Year one: {short_usd(y1[0])}–{short_usd(y1[1])}."
    text = (why[0].upper() + why[1:] + ". " if why else "") + tail
    add_text(slide, text, x + 0.18, top + 1.06, w - 0.36, h - 1.12, 8.5, BODY_TEXT,
             max_lines=3, min_size=7, cap_chars=200, cap_label="ad spend why")


def build_return_card(slide, ret, x, w, top, bottom):
    h = bottom - top
    add_rect(slide, x, top, w, h, fill=ROI_BG)
    add_text(slide, "WHAT THAT AD SPEND BUYS", x + 0.18, top + 0.10, w - 0.36, 0.20, 7.5,
             ROI_GREEN, bold=True, fit=False)
    cols = [("Ad spend", 0.00, 0.95), ("Cases / mo", 0.95, 0.85), ("Revenue / mo", 1.80, 1.05),
            ("Return", 2.85, 0.80)]
    tx = x + 0.18
    for label, off, cwid in cols:
        add_text(slide, label, tx + off, top + 0.32, cwid, 0.20, 7.5, SLATE, bold=True,
                 align=PP_ALIGN.LEFT if off == 0 else PP_ALIGN.RIGHT, fit=False)
    for i, sc in enumerate(ret["scenarios"][:2]):
        ry = top + 0.54 + i * 0.30
        if i == 0:
            add_rect(slide, x + 0.10, ry - 0.02, w - 0.20, 0.30, fill=ROI_HILIGHT)
        vals = [f"{short_usd(sc['ad_spend'])}/mo", f"{sc['cases']:g}", usd(sc["revenue"]),
                f"{sc['return_multiple']:g}×"]
        for (label, off, cwid), v in zip(cols, vals):
            add_text(slide, v, tx + off, ry, cwid, 0.26, 10, ROI_GREEN if off else DARK_TEXT,
                     bold=True, align=PP_ALIGN.LEFT if off == 0 else PP_ALIGN.RIGHT,
                     max_lines=1, min_size=8, anchor=MSO_ANCHOR.MIDDLE, cap_label="return cell")
    y = top + 0.54 + min(2, len(ret["scenarios"])) * 0.30 + 0.06
    if ret.get("share_of_case_value"):
        add_text(slide, f"Today {ret['share_of_case_value']}% of each case's value goes to landing it.",
                 x + 0.18, y, w - 0.36, 0.22, 8.5, DARK_TEXT, bold=True, max_lines=1, min_size=7,
                 cap_label="share of case value")
        y += 0.24
    add_text(slide, f"{ret['basis']} {ret.get('disclaimer', '')}".strip(), x + 0.18, y,
             w - 0.36, bottom - y - 0.06, 7.5, SLATE, min_size=6.5, cap_label="return basis")


def build_investment(prs):
    inv = load_investment()
    slide = new_slide(prs)
    add_header(slide, "Your Investment", 9.30, kicker="THE INVESTMENT")

    ad, ret = inv.get("ad_spend"), inv.get("return")
    # Without a closing quote the content runs down to the footer.
    bottom = 4.74 if CLOSING_QUOTE else 5.12
    # Room for two-line notes under the totals when setup fees are listed.
    nfees = len(inv.get("setup_fees") or [])
    th = 0.98 if not nfees else 1.14 if nfees <= 2 else 1.24
    if ad:
        left_w = 5.00
        build_buys_card(slide, inv, 0.30, left_w, 1.04, bottom - th - 0.10)
        build_totals_block(slide, inv, 0.30, left_w, bottom - th, bottom)
        rx, rw = 5.50, 4.20
        if ret:
            build_ad_spend_card(slide, ad, rx, rw, 1.04, 2.56)
            build_return_card(slide, ret, rx, rw, 2.64, bottom)
        else:
            build_ad_spend_card(slide, ad, rx, rw, 1.04, bottom)
    else:
        build_buys_card(slide, inv, 0.30, 9.40, 1.04, bottom - th - 0.10)
        build_totals_block(slide, inv, 0.30, 9.40, bottom - th, bottom)

    # Closing line — the owner's outcome, in their own verbatim words. Left
    # off when there's no verbatim line that isn't already on the deck.
    if CLOSING_QUOTE:
        add_rect(slide, 0, 4.84, 10, 0.43, fill=rgb("002A41"))
        add_rect(slide, 0, 4.84, 10, 0.02, fill=LIME_GREEN)
        add_text(slide, _quote(CLOSING_QUOTE[0]), 0.70, 4.86, 8.60, 0.40, 9.5, NAVY_TEXT_SOFT,
                 align=PP_ALIGN.CENTER, max_lines=1, min_size=7.5, anchor=MSO_ANCHOR.MIDDLE,
                 cap_chars=170, cap_label="CLOSING_QUOTE")
    add_footer(slide, INVESTMENT_PAGE, TOTAL_SLIDES, LOGO_PATH)


# ── Slide 6: What Happens Next (the growth roadmap) ───────────────

def build_roadmap(prs):
    slide = new_slide(prs)
    add_header(slide, ROADMAP_TITLE, 9.30, kicker="WHAT HAPPENS NEXT")

    gap = 0.28
    cw = (9.40 - gap * 2) / 3
    y, h, band = 1.06, 2.90, 0.62
    for i, p in enumerate(ROADMAP):
        cx = 0.30 + i * (cw + gap)
        now = i == 0
        add_rect(slide, cx, y, cw, h, fill=WHITE)
        add_rect(slide, cx, y, cw, band, fill=NAVY if now else SOFT_BLUE)
        add_text(slide, f"PHASE {i + 1}", cx + 0.08, y + 0.06, cw - 0.16, 0.20, 7.5,
                 LIME_GREEN if now else OCEAN_BLUE, bold=True, fit=False)
        add_text(slide, str(p["phase"]).upper(), cx + 0.08, y + 0.24, cw - 0.16, 0.34, 12.5,
                 WHITE if now else NAVY, bold=True, max_lines=1, min_size=9,
                 anchor=MSO_ANCHOR.MIDDLE, cap_chars=30, cap_label=f"ROADMAP[{i}] phase")
        add_text(slide, p["when"], cx + 0.08, y + band + 0.02, cw - 0.16, 0.46, 9,
                 GREEN if now else OCEAN_BLUE, bold=True, max_lines=2, min_size=7.5,
                 cap_chars=70, cap_label=f"ROADMAP[{i}] when")
        add_text(slide, client_name(" + ".join(str(x) for x in p["products"])), cx + 0.08, y + band + 0.46,
                 cw - 0.16, 0.24, 8, SLATE, max_lines=1, min_size=6.5,
                 cap_chars=80, cap_label=f"ROADMAP[{i}] products")
        add_rule(slide, cx + 0.16, y + band + 0.74, cx + cw - 0.16, y + band + 0.74, RULE_GRAY)
        top = y + band + 0.82
        add_bullets(slide, [cap(b, 65, f"ROADMAP[{i}] item {j+1}") for j, b in enumerate(p["items"][:4])],
                    cx + 0.08, top, cw - 0.18, y + h - top - 0.08, 9.5, DARK_TEXT, OCEAN_BLUE,
                    label=f"ROADMAP[{i}] items")
        if i < 2:
            add_shape(slide, MSO_SHAPE.CHEVRON, cx + cw + 0.07, y + band / 2 - 0.08, 0.14, 0.16,
                      fill=OCEAN_BLUE)

    add_text(slide, "WHAT EACH PHASE UNLOCKS FOR YOU", 0.30, 4.04, 5.0, 0.20, 7.5, SLATE,
             bold=True, fit=False)
    for i, p in enumerate(ROADMAP):
        cx = 0.30 + i * (cw + gap)
        add_rect(slide, cx, 4.26, cw, 0.86, fill=SOFT_BLUE)
        add_text(slide, p["unlocks"], cx + 0.12, 4.28, cw - 0.24, 0.82, 9.5, NAVY, italic=True,
                 min_size=7.5, anchor=MSO_ANCHOR.MIDDLE, cap_chars=140,
                 cap_label=f"ROADMAP[{i}] unlocks")

    note("roadmap", "Phases 2 and 3 are direction, not a quote: no prices, no dates. If the "
            "client asks, they're scoped and priced when the firm reaches that milestone.")
    add_footer(slide, PAGE["roadmap"], TOTAL_SLIDES, LOGO_PATH)


# ── ProfitOS slides (FCFO / Bookkeeping) ──────────────────────────
# Wording from the ProfitOS Strategic Financial Proposal deck (Sales
# Enablement, Nov 2026), drawn in this deck's style. Only the goals and the
# plan slide come from the firm's call (PROFITOS_GOALS / PROFITOS_WHY);
# the recommended levels come from package_decision.json.

POS_KICKER = "MANAGED FINANCIALS"
POS_DISCLAIMER = ("Examples are illustrative. Reporting formats, analyses and deliverables "
                  "vary by firm and agreed engagement scope.")
POS_STANDARD_GOALS = [
    ("Financial Visibility", "Make profit drivers, spending trends and cash timing easy to see."),
    ("Growth Decisions", "Back your next hires and investments with a clear view of their financial impact."),
    ("Confident Leadership", "A financially stronger firm with defined priorities, measurable progress and a plan for growth."),
]
POS_LEVELS = {
    "Advisor": {
        "n": 1, "label": "Level 1",
        "ladder": "Financial statement deep dive, review and discussion. Clear, reliable numbers.",
        "ask": "“Where should we focus?”",
        "title": "Understand your numbers. Know where to focus.",
        "work_head": "What Level 1 is",
        "work": "A financial strategy engagement built on a monthly deep dive into your P&L and "
                "balance sheet, with red flags turned into clear priorities and goals.",
        "decisions": ["Are we becoming more profitable?", "Where are we spending too much?",
                      "Which financial issues need attention first?",
                      "What should our financial goals be next quarter?"],
        "quote": "“I understand what my numbers are telling me.”*",
        "foot": "*Level 1 is a financial statement review and discussion: no quarterly projects or between-call questions.",
        "includes": None,
        "focus": "Financial statement deep dive · Red flags · Quarterly priorities and financial goals",
    },
    "Director": {
        "n": 2, "label": "Level 2",
        "ladder": "Adds a custom quarterly roadmap of financial projects and a KPI dashboard.",
        "ask": "“How do we move forward?”",
        "title": "Turn financial insight into a plan for growth.",
        "work_head": "Example of the work",
        "work": "A custom quarterly roadmap of done-with-you financial projects and a recurring KPI "
                "dashboard. Examples: budget, forecast, cash flow, compensation and marketing ROI analysis.",
        "decisions": ["Can we afford our next hire?", "How much can we safely invest in marketing?",
                      "Will a compensation change improve profitability?",
                      "What needs to happen this quarter to reach our goals?"],
        "quote": "“I can make growth decisions with a financial plan behind them.”",
        "foot": None,
        "includes": "Includes everything in Level 1, plus quarterly projects",
        "focus": "Quarterly roadmap · KPI dashboard · Cash flow and hiring analysis",
    },
    "Partner": {
        "n": 3, "label": "Level 3",
        "ladder": "Adds comprehensive projects for expansion, capital strategy and succession or exit planning.",
        "ask": "“How do we navigate major decisions?”",
        "title": "Make big decisions about your firm’s future.",
        "work_head": "Example of the work",
        "work": "The most advanced done-with-you projects each quarter. Examples: pricing analysis, "
                "profitability by practice area, location or attorney, expansion modeling, capital strategy, "
                "multi-year financial modeling, and succession or exit planning.",
        "decisions": ["Should we expand into another market?", "How should we fund our next stage of growth?",
                      "Which practice areas are creating the most value?",
                      "How do we prepare for succession or a transition?"],
        "quote": "“I have financial leadership to navigate bigger decisions.”",
        "foot": None,
        "includes": "Includes everything in Levels 1 and 2, plus advanced projects",
        "focus": "Expansion modeling · Capital strategy · Succession planning · Profitability by practice area",
    },
}
# (level, transactions a month, what it is) — bookkeeping is placed by monthly
# transaction volume first; revenue is a guide (Vanessa's deck, Nov 20).
POS_BOOKS = [(1, "Up to 100", "Financials by the 20th*. Clean books and simple accounts, no trust "
                              "accounting. Typically up to $1M in revenue."),
             (2, "Up to 250", "Financials by the 15th*. Adds monthly three-way trust reconciliation. "
                              "Typically $1M–$2M in revenue."),
             (3, "Up to 500", "Financials by the 10th*, our fastest close, with trust reconciliation. "
                              "Typically $2M–$4M in revenue."),
             (4, "Above 500", "Firms above these limits are scoped with a custom agreement.")]
# Her speaker notes that the seller needs (they go to the seller prep, never the deck).
POS_SELLER_NOTES = {
    "pos_ladder": "Levels distinguish engagement scope and complexity, not hours. Level 1 is financial "
                  "statement review and discussion with no quarterly projects; quarterly projects begin at "
                  "Level 2. Lead with your Finance Team rather than an individual title; if asked who is on "
                  "it, a CFO is assigned to the account and bookkeepers and support work alongside, so not "
                  "every call is with the CFO. Managed Financials requires SMB Bookkeeping, or books that are "
                  "current with complete, accurate, timely financials each month by the 10th, including "
                  "properly allocated payroll. Set-up fees apply.",
    "pos_books": "Bookkeeping is placed by monthly transaction volume first (up to 100, 250, 500); revenue "
                 "and team size are a secondary guide. Confirm with the department before quoting a firm "
                 "whose volume and revenue point to different levels. Payroll/W-2 and AP/1099 work is not "
                 "included at any level. Included cleanup: up to 2 months at Level 2 and up to 4 months at "
                 "Level 3; Level 1 needs clean books. Prior-period cleanup is billed separately.",
    "pos_level": "Examples are tailored and scope-confirmed; not every example applies to every engagement. "
                 "Each level includes everything in the one before it.",
}


def pos_slide(prs, key, title, sub=None, disclaimer=True):
    slide = new_slide(prs)
    add_header(slide, title, 9.30, kicker=POS_KICKER)
    if sub:
        add_text(slide, sub, 0.30, 1.00, 9.40, 0.40, 10, BODY_TEXT, max_lines=2, min_size=8,
                 cap_label=f"{key} sub")
    if disclaimer:
        add_text(slide, POS_DISCLAIMER, 0.30, 5.02, 9.40, 0.20, 6.5, SLATE, max_lines=1,
                 fit=False)
    add_footer(slide, PAGE[key], TOTAL_SLIDES, LOGO_PATH)
    return slide


def build_pos_goals(prs):
    goals = [tuple(g) for g in PROFITOS_GOALS] or POS_STANDARD_GOALS
    if not PROFITOS_GOALS:
        note("pos_goals", "No financial goals were recorded from the call, so this slide shows "
                          "the three standard Managed Financials goals. Recap the firm's own goals out loud.")
    slide = pos_slide(prs, "pos_goals", "Your goals point to a clearer path forward.",
                      "After our conversation, these are the areas where we can help improve your "
                      "firm's financial health." if PROFITOS_GOALS else None, disclaimer=False)
    n = len(goals)
    gap = 0.25
    cw = (9.40 - gap * (n - 1)) / n
    y, h = 1.56, 2.70
    for i, (head, line) in enumerate(goals):
        cx = 0.30 + i * (cw + gap)
        add_rect(slide, cx, y, cw, h, fill=WHITE)
        add_rect(slide, cx, y, cw, 0.05, fill=OCEAN_BLUE)
        add_badge(slide, i + 1, cx + 0.20, y + 0.28, 0.36, NAVY)
        add_text(slide, head, cx + 0.18, y + 0.80, cw - 0.36, 0.60, 15, NAVY, bold=True,
                 max_lines=2, min_size=11, cap_label=f"PROFITOS_GOALS[{i}] heading")
        add_text(slide, line, cx + 0.18, y + 1.44, cw - 0.36, h - 1.56, 10.5, BODY_TEXT,
                 min_size=8.5, cap_label=f"PROFITOS_GOALS[{i}] line")
    add_strip(slide, "Next:", "Your specific opportunities and priorities shape the recommended engagement.",
              4.44, label="pos_goals strip")


def build_pos_two_sides(prs):
    slide = pos_slide(prs, "pos_two_sides", "From reliable numbers to confident action.",
                      "Bookkeeping establishes visibility. Your Finance Team helps you "
                      "interpret the numbers and decide what to do next.")
    cols = [("BOOKKEEPING  ·  THE FOUNDATION", "Know where you stand",
             ["Accurate, timely financials", "Organized financial reporting",
              "Visibility into cash, expenses and profit", "A trusted foundation for decision-making"],
             "SEE CLEARLY", OCEAN_BLUE),
            ("MANAGED FINANCIALS  ·  THE STRATEGY", "Know where to go",
             ["Monthly deep dive into your P&L and balance sheet",
              "Red flags and profit leaks turned into clear priorities",
              "A KPI dashboard and quarterly projects at higher levels",
              "Books aligned to a proven law firm Chart of Accounts"],
             "DECIDE CONFIDENTLY", LIME_GREEN)]
    cw, y, h = 4.45, 1.52, 3.36
    for i, (kick, head, items, tag, accent) in enumerate(cols):
        cx = 0.30 + i * (cw + 0.50)
        add_rect(slide, cx, y, cw, h, fill=WHITE if i == 0 else NAVY)
        add_rect(slide, cx, y, 0.06, h, fill=accent)
        add_text(slide, kick, cx + 0.24, y + 0.16, cw - 0.40, 0.22, 8, OCEAN_BLUE if i == 0 else LIME_GREEN,
                 bold=True, max_lines=1, fit=False)
        add_text(slide, head, cx + 0.24, y + 0.40, cw - 0.40, 0.44, 18, NAVY if i == 0 else WHITE,
                 bold=True, max_lines=1, min_size=13)
        add_bullets(slide, items, cx + 0.20, y + 0.98, cw - 0.40, 1.80, 11,
                    DARK_TEXT if i == 0 else NAVY_TEXT_SOFT, accent, label=f"pos_two_sides {i}")
        add_text(slide, tag, cx + 0.24, y + h - 0.44, cw - 0.40, 0.30, 10,
                 OCEAN_BLUE if i == 0 else LIME_GREEN, bold=True, max_lines=1, fit=False)
    add_shape(slide, MSO_SHAPE.RIGHT_ARROW, 4.82, 3.00, 0.36, 0.40, fill=OCEAN_BLUE)


def build_pos_books(prs):
    slide = pos_slide(prs, "pos_books", "Bookkeeping that fits the size of your firm.",
                      "Your monthly transaction volume sets the level. Revenue and team size are a guide. "
                      "Higher levels add trust compliance and a faster close.", disclaimer=False)
    note("pos_books", POS_SELLER_NOTES["pos_books"])
    gap = 0.18
    cw = (9.40 - 3 * gap) / 4
    y, h = 1.52, 2.06
    for i, (lvl, rev, line) in enumerate(POS_BOOKS):
        cx = 0.30 + i * (cw + gap)
        mine = lvl == BOOKKEEPING_LEVEL
        add_rect(slide, cx, y, cw, h, fill=NAVY if mine else WHITE)
        add_rect(slide, cx, y, cw, 0.05, fill=LIME_GREEN if mine else OCEAN_BLUE)
        add_text(slide, f"LEVEL {lvl}" if lvl < 4 else "CUSTOM", cx + 0.16, y + 0.14, cw - 0.32, 0.22, 8,
                 LIME_GREEN if mine else OCEAN_BLUE, bold=True, max_lines=1, fit=False)
        add_text(slide, rev, cx + 0.16, y + 0.38, cw - 0.32, 0.40, 15, WHITE if mine else NAVY,
                 bold=True, max_lines=1, min_size=11)
        add_text(slide, "transactions a month", cx + 0.16, y + 0.76, cw - 0.32, 0.20, 8,
                 NAVY_TEXT_SOFT if mine else SLATE, max_lines=1, fit=False)
        add_text(slide, line, cx + 0.16, y + 0.98, cw - 0.32, h - 1.02 - (0.32 if mine else 0.04), 8.5,
                 NAVY_TEXT_SOFT if mine else BODY_TEXT, min_size=7, cap_label=f"pos_books {lvl}")
        if mine:
            add_pill(slide, "Recommended for you", cx + 0.16, y + h - 0.30, 0.22, LIME_GREEN, NAVY, size=6.5)
    add_rect(slide, 0.30, 3.70, 9.40, 1.22, fill=WHITE)
    add_rect(slide, 0.30, 3.70, 0.05, 1.22, fill=OCEAN_BLUE)
    add_text(slide, "INCLUDED AT EVERY LEVEL", 0.50, 3.78, 6.0, 0.22, 8, OCEAN_BLUE, bold=True, fit=False)
    items = ["Done-with-you setup connecting QuickBooks Online, your banks and your legal platform",
             "Books built on our law firm Chart of Accounts",
             "Every transaction categorized and accounts reconciled",
             "A reviewed P&L and balance sheet every month"]
    add_bullets(slide, items[:2], 0.46, 4.02, 4.60, 0.86, 9, DARK_TEXT, OCEAN_BLUE, label="pos_books included 1")
    add_bullets(slide, items[2:], 5.06, 4.02, 4.56, 0.86, 9, DARK_TEXT, OCEAN_BLUE, label="pos_books included 2")
    add_text(slide, "*Delivery dates depend on timely receipt of your data. Firms above these limits require "
                    "a custom agreement.", 0.30, 5.00, 9.40, 0.22, 6.5, SLATE, max_lines=1, fit=False)


def build_pos_questions(prs):
    slide = pos_slide(prs, "pos_questions", "Questions you can answer with confidence.",
                      "The right questions change as your firm grows. Higher levels add planning and "
                      "projects to support the decisions behind them.")
    cards = [("Profitability", ["Which parts of our firm create the most value?",
                                "Why is revenue rising faster than profit?"]),
             ("Cash flow", ["How much can we safely invest?", "Where can we improve collections?"]),
             ("Growth decisions", ["When can we afford our next hire?", "Is marketing driving profitable growth?"]),
             ("Long-term strategy", ["How should we finance expansion?", "How do we prepare for succession?"])]
    gap = 0.20
    cw = (9.40 - gap) / 2
    ch = 1.62
    for i, (head, qs) in enumerate(cards):
        cx = 0.30 + (i % 2) * (cw + gap)
        cy = 1.52 + (i // 2) * (ch + 0.18)
        add_rect(slide, cx, cy, cw, ch, fill=WHITE)
        add_rect(slide, cx, cy, 0.05, ch, fill=OCEAN_BLUE)
        add_text(slide, head, cx + 0.22, cy + 0.12, cw - 0.40, 0.34, 13, NAVY, bold=True,
                 max_lines=1, min_size=10)
        add_bullets(slide, qs, cx + 0.18, cy + 0.52, cw - 0.36, ch - 0.62, 10.5, DARK_TEXT,
                    OCEAN_BLUE, label=f"pos_questions {i}")


def _mini_bars(slide, x, y, w, h, values, colors):
    n = len(values)
    bw = w / (n * 1.6)
    top = max(values)
    for i, v in enumerate(values):
        bh = h * v / top
        add_rect(slide, x + i * bw * 1.6, y + h - bh, bw, bh, fill=colors[i % len(colors)])
    add_rule(slide, x - 0.04, y + h, x + w, y + h, RULE_GRAY)


def build_pos_analysis(prs):
    slide = pos_slide(prs, "pos_analysis", "See the analysis behind better decisions.",
                      "Illustrative examples of the financial insight and planning available across the levels.")
    cards = [("MONTHLY FINANCIAL REVIEW", "Where do we stand?", "P&L AND BALANCE SHEET  ·  THIS MONTH",
              "Red flags surfaced for discussion"),
             ("QUARTERLY ROADMAP  ·  LEVEL 2+", "What should happen next?", "90-DAY ROADMAP",
              "Priorities and goals set each quarter"),
             ("KPI DASHBOARD  ·  LEVEL 2+", "How is the firm really doing?", "FIRM HEALTH AT A GLANCE", None)]
    gap = 0.22
    cw = (9.40 - 2 * gap) / 3
    y, h = 1.52, 3.12
    for i, (kick, q, panel, caption) in enumerate(cards):
        cx = 0.30 + i * (cw + gap)
        add_rect(slide, cx, y, cw, h, fill=WHITE)
        add_rect(slide, cx, y, cw, 0.05, fill=OCEAN_BLUE)
        add_text(slide, kick, cx + 0.16, y + 0.14, cw - 0.32, 0.22, 7.5, OCEAN_BLUE, bold=True,
                 max_lines=1, min_size=6.5)
        add_text(slide, q, cx + 0.16, y + 0.38, cw - 0.32, 0.36, 12, NAVY, bold=True,
                 max_lines=1, min_size=9)
        bx, by, bw, bh = cx + 0.16, y + 0.86, cw - 0.32, 2.12
        add_rect(slide, bx, by, bw, bh, fill=BG_WASH)
        add_text(slide, panel, bx + 0.10, by + 0.06, bw - 0.86, 0.20, 6.5, SLATE, bold=True, max_lines=1,
                 min_size=5)
        add_text(slide, "SAMPLE", bx + bw - 0.76, by + 0.06, 0.70, 0.20, 6, SLATE, bold=True,
                 align=PP_ALIGN.RIGHT, fit=False)
        px, py, pw = bx + 0.14, by + 0.36, bw - 0.28
        if i == 0:      # this month's P&L lines, with a flag on one
            for r, (label, frac, color) in enumerate([("Revenue", 0.92, OCEAN_BLUE), ("Payroll", 0.58, NAVY),
                                                      ("Marketing", 0.30, CORAL), ("Net income", 0.22, GREEN)]):
                ry = py + 0.08 + r * 0.32
                add_text(slide, label, px, ry - 0.02, 0.80, 0.22, 7, DARK_TEXT, max_lines=1, fit=False)
                add_rect(slide, px + 0.82, ry + 0.03, (pw - 0.86) * frac, 0.14, fill=color)
        elif i == 1:    # three months across, projects below
            step = pw / 3.0
            for mth in range(3):
                add_text(slide, f"Month {mth + 1}", px + mth * step, py, step, 0.22, 7.5, NAVY, bold=True,
                         align=PP_ALIGN.CENTER, fit=False)
            add_rule(slide, px, py + 0.26, px + pw, py + 0.26, NAVY_RULE, 1.5)
            for r, (start, span, color, label) in enumerate([(0, 1.0, LIME_GREEN, "Budget"),
                                                             (0.6, 1.4, OCEAN_BLUE, "Cash flow forecast"),
                                                             (1.6, 1.4, NAVY, "Marketing ROI analysis")]):
                ry = py + 0.40 + r * 0.36
                add_rect(slide, px + start * step + 0.03, ry, span * step - 0.06, 0.24, fill=color)
                add_text(slide, label, px + start * step + 0.03, ry, span * step - 0.06, 0.24, 6.5,
                         NAVY if color == LIME_GREEN else WHITE, bold=True, max_lines=1, min_size=4.5,
                         anchor=MSO_ANCHOR.MIDDLE)
        else:           # four KPI tiles
            tw, th = (pw - 0.12) / 2, 0.70
            for t, label in enumerate(("Revenue", "Profit", "Cash", "Collections")):
                tx, ty = px + (t % 2) * (tw + 0.12), py + 0.04 + (t // 2) * (th + 0.12)
                add_rect(slide, tx, ty, tw, th, fill=WHITE)
                add_text(slide, label, tx + 0.08, ty + 0.06, tw - 0.16, 0.20, 7, SLATE, bold=True,
                         max_lines=1, fit=False)
                _mini_bars(slide, tx + 0.12, ty + 0.30, tw - 0.30, 0.30, [3, 4, 3.6, 5][:4],
                           [OCEAN_BLUE] if t != 1 else [GREEN])
        if caption:
            add_text(slide, caption, bx + 0.10, by + bh - 0.32, bw - 0.20, 0.26, 7.5, NAVY, bold=True,
                     max_lines=1, min_size=6.5)
    add_text(slide, "Illustrative concepts, not screenshots of actual SMBTeam reporting or guaranteed deliverables.",
             0.30, 4.70, 9.40, 0.22, 7.5, SLATE, max_lines=1, fit=False)


def build_pos_plan(prs):
    lvl = POS_LEVELS[PROFITOS_LEVEL]
    if not PROFITOS_WHY:
        note("pos_plan", "PROFITOS_WHY was not set, so 'Why this fits' uses the level's standard line. "
                         "Say why this level fits the firm in your own words.")
    slide = pos_slide(prs, "pos_plan", "A plan built around your priorities.",
                      "How we matched the engagement to the questions your firm needs to answer.",
                      disclaimer=False)
    program = f"Managed Financials  ·  {lvl['label']}" + (f"  +  Bookkeeping Level {BOOKKEEPING_LEVEL}" if BOOKKEEPING_LEVEL else "")
    add_rect(slide, 0.30, 1.52, 9.40, 0.92, fill=NAVY)
    add_rect(slide, 0.30, 1.52, 0.06, 0.92, fill=LIME_GREEN)
    add_text(slide, "RECOMMENDED PROGRAM", 0.56, 1.62, 6.0, 0.22, 8, LIME_GREEN, bold=True, fit=False)
    add_text(slide, program, 0.56, 1.86, 8.90, 0.48, 20, WHITE, bold=True, max_lines=1, min_size=13,
             cap_label="pos_plan program")
    rows = ([("YOUR PRIMARY GOALS", " · ".join(g[0] for g in PROFITOS_GOALS))] if PROFITOS_GOALS else []) + \
           [("INITIAL FOCUS", lvl["focus"]), ("WHY THIS FITS", PROFITOS_WHY or lvl["ladder"])]
    y = 2.58
    for i, (head, text) in enumerate(rows):
        add_rect(slide, 0.30, y, 9.40, 0.72, fill=SOFT_BLUE if head == "WHY THIS FITS" else WHITE)
        add_rect(slide, 0.30, y, 0.05, 0.72, fill=OCEAN_BLUE)
        add_text(slide, head, 0.52, y + 0.08, 2.20, 0.56, 8, OCEAN_BLUE, bold=True, max_lines=2,
                 anchor=MSO_ANCHOR.MIDDLE, fit=False)
        add_text(slide, text, 2.70, y + 0.06, 6.86, 0.60, 11, NAVY, bold=head != "WHY THIS FITS", max_lines=2,
                 min_size=8.5, anchor=MSO_ANCHOR.MIDDLE, cap_label=f"pos_plan {head.lower()}")
        y += 0.80


def _level_tracker(slide, current, x, y, w):
    gap = 0.12
    cw = (w - 2 * gap) / 3
    for name, d in POS_LEVELS.items():
        cx = x + (d["n"] - 1) * (cw + gap)
        done, mine = d["n"] < POS_LEVELS[current]["n"], name == current
        add_rect(slide, cx, y, cw, 0.36, fill=NAVY if mine else (SOFT_BLUE if done else WHITE))
        add_text(slide, ("✓ " if done else f"{d['n']} · ") + d["label"], cx, y, cw, 0.36, 9,
                 WHITE if mine else NAVY, bold=mine, align=PP_ALIGN.CENTER,
                 anchor=MSO_ANCHOR.MIDDLE, max_lines=1, fit=False)


def build_pos_level(prs):
    lvl = POS_LEVELS[PROFITOS_LEVEL]
    slide = pos_slide(prs, "pos_level", lvl["title"])
    note("pos_level", POS_SELLER_NOTES["pos_level"])
    _level_tracker(slide, PROFITOS_LEVEL, 0.30, 1.06, 9.40)
    y, h = 1.58, 2.36
    add_rect(slide, 0.30, y, 4.40, h, fill=WHITE)
    add_rect(slide, 0.30, y, 4.40, 0.05, fill=OCEAN_BLUE)
    add_text(slide, lvl["work_head"], 0.48, y + 0.16, 4.04, 0.32, 12, NAVY, bold=True, max_lines=1, fit=False)
    add_text(slide, lvl["work"], 0.48, y + 0.52, 4.04, h - 0.64, 10.5, BODY_TEXT, min_size=8.5,
             cap_label="pos_level work")
    add_rect(slide, 4.90, y, 4.80, h, fill=WHITE)
    add_rect(slide, 4.90, y, 4.80, 0.05, fill=LIME_GREEN)
    add_text(slide, "Decisions that become easier", 5.08, y + 0.16, 4.44, 0.32, 12, NAVY, bold=True,
             max_lines=1, fit=False)
    add_bullets(slide, lvl["decisions"], 5.04, y + 0.54, 4.50, h - 0.62, 10.5, DARK_TEXT, GREEN,
                label="pos_level decisions")
    add_rect(slide, 0.30, 4.06, 9.40, 0.62, fill=NAVY)
    add_text(slide, lvl["quote"], 0.50, 4.06, 9.00, 0.62, 14, WHITE, bold=True, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE, max_lines=1, min_size=10)
    tail = lvl["foot"] or ("✓ " + lvl["includes"])
    add_text(slide, tail, 0.30, 4.72, 9.40, 0.24, 8, SLATE if lvl["foot"] else GREEN, bold=not lvl["foot"],
             max_lines=1, fit=False)


def build_pos_ladder(prs):
    slide = pos_slide(prs, "pos_ladder", "Leadership matched to your stage of growth.",
                      "Each level includes everything in the one before it, then adds more, matched to the "
                      "size and complexity of your firm.")
    note("pos_ladder", POS_SELLER_NOTES["pos_ladder"])
    gap = 0.20
    cw = (9.40 - 2 * gap) / 3
    base = 4.62
    for name, d in POS_LEVELS.items():
        i = d["n"] - 1
        cx = 0.30 + i * (cw + gap)
        h = 2.30 + 0.40 * i
        top = base - h
        mine = name == PROFITOS_LEVEL
        add_rect(slide, cx, top, cw, h, fill=NAVY if mine else WHITE)
        add_rect(slide, cx, top, cw, 0.06, fill=LIME_GREEN if mine else OCEAN_BLUE)
        add_text(slide, d["label"], cx + 0.18, top + 0.16, cw - 0.36, 0.36, 15,
                 WHITE if mine else NAVY, bold=True, max_lines=1, min_size=11)
        add_text(slide, d["ladder"], cx + 0.18, top + 0.58, cw - 0.36, 0.80, 10,
                 NAVY_TEXT_SOFT if mine else BODY_TEXT, min_size=8, cap_label=f"pos_ladder {name}")
        add_text(slide, d["ask"], cx + 0.18, top + 1.42, cw - 0.36, 0.50, 10.5,
                 LIME_GREEN if mine else OCEAN_BLUE, bold=True, max_lines=2, min_size=8.5)
        if mine:
            add_pill(slide, "Recommended for you", cx + 0.18, base - 0.38, 0.24, LIME_GREEN, NAVY, size=6.5)
    add_text(slide, "Scope examples are illustrative; larger or more complex firms may require a custom agreement.",
             0.30, 4.70, 9.40, 0.22, 7.5, SLATE, max_lines=1, fit=False)


POS_BUILDERS = {"pos_goals": build_pos_goals, "pos_two_sides": build_pos_two_sides,
                "pos_books": build_pos_books, "pos_questions": build_pos_questions,
                "pos_analysis": build_pos_analysis, "pos_plan": build_pos_plan,
                "pos_level": build_pos_level, "pos_ladder": build_pos_ladder}


# ── Font embedding ────────────────────────────────────────────────
# python-pptx has no font-embedding API, so this patches the saved .pptx's
# raw OOXML directly. Mirrors what sales_companion_template.py already does
# for the PDF via reportlab's registerFont — without it, "Poppins" is just a
# name any viewer without the font installed (Google Slides, a PowerPoint
# missing the font) will silently substitute, which is why fonts can look
# inconsistent across machines even though the script never changes.

def embed_fonts(pptx_path, font_dir):
    import zipfile, shutil, tempfile

    faces = [
        ("regular", "Poppins-Regular.ttf"),
        ("bold",    "Poppins-Bold.ttf"),
        ("italic",  "Poppins-Italic.ttf"),
    ]
    faces = [(role, os.path.join(font_dir, fname)) for role, fname in faces
             if os.path.isfile(os.path.join(font_dir, fname))]
    if not faces:
        return

    NS = {
        "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
        "r":  "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
        "p":  "http://schemas.openxmlformats.org/presentationml/2006/main",
    }

    tmp_dir = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(pptx_path) as zin:
            zin.extractall(tmp_dir)

        # 1. Copy the font binaries into ppt/fonts/
        fonts_dir = os.path.join(tmp_dir, "ppt", "fonts")
        os.makedirs(fonts_dir, exist_ok=True)
        font_parts = []  # (role, part_filename)
        for i, (role, src_path) in enumerate(faces, start=1):
            part_name = f"font{i}.fntdata"
            shutil.copyfile(src_path, os.path.join(fonts_dir, part_name))
            font_parts.append((role, part_name))

        # 2. Register the .fntdata extension in [Content_Types].xml
        ct_path = os.path.join(tmp_dir, "[Content_Types].xml")
        ct_tree = etree.parse(ct_path)
        ct_root = ct_tree.getroot()
        if not ct_root.xpath("ct:Default[@Extension='fntdata']", namespaces=NS):
            default = etree.SubElement(ct_root, f"{{{NS['ct']}}}Default")
            default.set("Extension", "fntdata")
            default.set("ContentType", "application/x-fontdata")
        ct_tree.write(ct_path, xml_declaration=True, encoding="UTF-8", standalone=True)

        # 3. Add a relationship from presentation.xml to each font part
        rels_path = os.path.join(tmp_dir, "ppt", "_rels", "presentation.xml.rels")
        rels_tree = etree.parse(rels_path)
        rels_root = rels_tree.getroot()
        existing_ids = {el.get("Id") for el in rels_root}

        def new_rid(n=[1]):
            while f"rIdEmbedFont{n[0]}" in existing_ids:
                n[0] += 1
            rid = f"rIdEmbedFont{n[0]}"
            n[0] += 1
            return rid

        rel_ids = {}
        for role, part_name in font_parts:
            rid = new_rid()
            rel = etree.SubElement(rels_root, f"{{{NS['pr']}}}Relationship")
            rel.set("Id", rid)
            rel.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/font")
            rel.set("Target", f"fonts/{part_name}")
            rel_ids[role] = rid
        rels_tree.write(rels_path, xml_declaration=True, encoding="UTF-8", standalone=True)

        # 4. Declare the embedded font in presentation.xml and flip the
        #    embedTrueTypeFonts switch on.
        pres_path = os.path.join(tmp_dir, "ppt", "presentation.xml")
        pres_tree = etree.parse(pres_path)
        pres_root = pres_tree.getroot()
        pres_root.set("embedTrueTypeFonts", "1")

        embedded_font = etree.Element(f"{{{NS['p']}}}embeddedFont")
        font_el = etree.SubElement(embedded_font, f"{{{NS['p']}}}font")
        font_el.set("typeface", FONT)
        for role, rid in rel_ids.items():
            face_el = etree.SubElement(embedded_font, f"{{{NS['p']}}}{role}")
            face_el.set(f"{{{NS['r']}}}id", rid)

        embedded_font_lst = etree.Element(f"{{{NS['p']}}}embeddedFontLst")
        embedded_font_lst.append(embedded_font)

        # Schema order (CT_Presentation) requires embeddedFontLst to sit
        # after notesSz and before defaultTextStyle/custShowLst/etc.
        notes_sz = pres_root.find(f"{{{NS['p']}}}notesSz")
        default_text_style = pres_root.find(f"{{{NS['p']}}}defaultTextStyle")
        if notes_sz is not None:
            insert_at = list(pres_root).index(notes_sz) + 1
        elif default_text_style is not None:
            insert_at = list(pres_root).index(default_text_style)
        else:
            insert_at = len(pres_root)
        pres_root.insert(insert_at, embedded_font_lst)

        pres_tree.write(pres_path, xml_declaration=True, encoding="UTF-8", standalone=True)

        # 5. Re-zip in place
        tmp_pptx = pptx_path + ".tmp"
        with zipfile.ZipFile(tmp_pptx, "w", zipfile.ZIP_DEFLATED) as zout:
            for root_dir, _, files in os.walk(tmp_dir):
                for fname in files:
                    full = os.path.join(root_dir, fname)
                    arcname = os.path.relpath(full, tmp_dir)
                    zout.write(full, arcname)
        shutil.move(tmp_pptx, pptx_path)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


# ── Assemble ──────────────────────────────────────────────────────

validate_fill()

prs = Presentation()
prs.slide_width  = Inches(10)
prs.slide_height = Inches(5.625)

build_cover(prs)
build_leadsos(prs)
build_aiwp(prs)
build_priorities(prs)
if STAIRCASE:
    build_staircase(prs)
build_diagnosis(prs)
build_plan(prs)
build_strategy(prs)
if SHOW_ROLLOUT:
    build_rollout(prs)
build_investment(prs)
build_roadmap(prs)
for key in PROFITOS_SLIDES:
    POS_BUILDERS[key](prs)
attribution_notes()
write_notes(prs)

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True) if os.path.dirname(OUTPUT_PATH) else None
prs.save(OUTPUT_PATH)
embed_fonts(OUTPUT_PATH, FONT_DIR)

if _SHRUNK:
    print(f"NOTE: {len(_SHRUNK)} field(s) were shrunk to fit their box:")
    for label, before, after in _SHRUNK:
        print(f"  - {label}: {before:g}pt → {after:g}pt")

if _TRUNCATED:
    print(f"WARNING: {len(_TRUNCATED)} field(s) exceeded their character budget "
          f"and were truncated — consider shortening the source copy instead:")
    for label, original in _TRUNCATED:
        print(f"  - {label}: {original!r}")

noted = [k for k in SLIDE_ORDER if _NOTES.get(k) or seller_note(k)]
if noted:
    print(f"Seller prep: {seller_prep_path()} (slides: " +
          ", ".join(f"{k} {PAGE[k]}" for k in noted) + ") — speaker notes left empty")

print(f"Saved: {OUTPUT_PATH}  ({len(prs.slides)} slides)")
