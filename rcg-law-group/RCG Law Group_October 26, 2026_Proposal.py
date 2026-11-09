"""
Audit PowerPoint Template — SMB Team
======================================
Generates the 5-slide proposal PPTX. Uses python-pptx. Do not modify the
layout engine below the FILL section. Only replace the # FILL: placeholders
with audit-specific content (rules: .claude/commands/audit-pptx.md).

The deck makes the case for the recommendation in one line of argument:
one number from the call → what drives it → what we do about each driver →
what we're recommending → what it costs.

Slide 1 — Your Priorities, In Your Words  (the call KPI + the client's quotes)
Slide 2 — The Diagnosis                   (the root causes behind that KPI)
Slide 3 — The Plan                        (actions tied to causes + what we'll measure)
Slide 4 — The Recommended Strategy        (each product: why, and its deliverables)
Slide 5 — Your Investment                 (pricing — numbers unchanged from the 3-slide deck)
A Rollout Plan slide exists in the engine but is left out (SHOW_ROLLOUT) until
real onboarding content is ready.

Data rules (enforced by the build where it can, by audit-pptx.md everywhere):
- Every number comes from the call (client or seller) or from a verified
  research observation, exactly as said or measured. Never invented, never
  estimated.
- Targets are labelled "Target:" by the engine and must rest on call data.
  With nothing to base one on, leave it None — no target line is drawn and
  the seller gets a speaker note.
- Seller-only guidance goes in SELLER_NOTES (speaker notes), never on a slide.

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

# ── BUILD NOTES (internal — never shown on a slide) ──────────────
# Marketing package: Full Service Marketing — Growth — bundled $7,497/mo, stand-alone $8,997/mo, savings $1,500/mo
# Non-marketing package(s): Elite Coach — bundled $2,600/mo, stand-alone $3,497/mo, savings $897/mo
# LAW package: none
# Total monthly investment: $10,097/mo · total savings: $2,397/mo · pricing_mode: bundled
# Ad spend: conservative $3,500 (channel: Google PPC family-law minimum, per package_decision.json), aggressive $14,000 (decision file: 4x the conservative floor)
#   Rule-derived aggressive check: no goal stated, 2x $5M = $10M x 20% / 12 = $166,667 x 1.0 (Salt Lake mid-size market) - $7,497 = $159,170, far above the $50,000 Growth cap;
#   reverse math ($10M/12 / $9,100 = 91.6 cases / 21% = 436 leads x $100) = $43,600 < 20% rule. Decision-file range kept; flagged below.
# ROI conservative: blended CPL $120 (Google family-law midpoint $100 + 20% cushion) → 29 leads → 6 cases (close rate 21%) → $54,600 revenue → 15.6×
# ROI aggressive:   blended CPL $100 (Google family-law midpoint, no cushion) → 140 leads → 29 cases → $263,900 revenue → 18.9× (18.85)
#   Single-channel (Google Search) basis because the decision file gives no channel split. Cases rounded down before revenue.
# Case value: $9,100 (source: transcript — client, 00:07:18). Close rate 21% (client, 00:17:23, "conversion rate on cold leads"; not stated as consults-to-signed)
# Why this range: To turn high-intent South Jordan divorce searches into signed cases before nearby firms capture them first.
# Pillar review: Lead Gen amber — paid channels cost about half of case value, rest is referrals and content · Intake green — client says sales process is "pretty good" (not examined) · Team amber — COO in place, owner has lost protected planning time · Profit amber — ad cost about 50% of case value (client's words)
# KPI (slide 1): Cost per client — "About $4,500 cost per retained client" — client, 00:07:10 (STEP 9B)
# Diagnosis (slide 2): 1. Website too slow — 24 out of 100 mobile, ~23 s LCP — seller ran Google tool live, client re-ran, 00:10:10–00:11:42 (STEP 9B 1) · 2. Ads cost about half a case — $4,500 Google/LSA, $5,000 Meta vs $9,100 — client, 00:07:10–00:07:47 (STEP 9B 2) · 3. Rivals outrank the firm locally — "three down the line", seller live, 00:12:50–00:13:18; no review counts printed (STEP 9B 3) · 4. Coaching gone, agency learning — client, 00:01:17–00:01:32 and 00:04:41–00:04:54 (STEP 9B 4)
# Targets (slides 2–3): none — STEP 9B gives no firm-specific target basis for any cause; engine adds seller notes. Seller's "sub 60 or 70" flag is not a firm target and is not used.
# What You Told Us (slide 1 quotes and tie lines):
#   1. Ad costs — transcript line: "So when that's the average case value and that's the cost per retained client, that's 50% and that is horrible." — supports: Full Service Marketing — Growth
#   2. Coaching — transcript line: "I got so much value in getting out of the office, dedicated time to learning stuff, being with others, and then like, being able to do my quarterly planning." — supports: Elite Coach
#   3. Paid ads — transcript line: "I'm at the point right now where I'm going to tell them not to run any more pay-per-click or local service ads." — supports: Full Service Marketing — Growth
# Overrides applied: Seller override (package_source "trigger_override": "Full Service Marketing — Growth + Elite Coach") — built as-is; the four Transcript-Stated Need overrides do not apply to a seller choice.
#   Rules it departs from, for sales: (a) existing-vendor — 97th Floor is the active ad/website vendor (client says "90% likelihood" a change goes to SMB Team); (b) revenue $5M would normally map to Platinum, Growth is normally $1M–$2M; (c) Elite Coach is normally the $250K–$400K band and Master's Circle fits a 10-person team over $1M.
#   Checks: 35% cap — $10,097 + $14,000 ad spend = $24,097 vs $145,833 (35% of $416,667/mo) OK; ad spend under the $50,000 Growth cap.
# Escalation flags:
#   - Review counts unconfirmed — verify live before the call (all firm and competitor counts are aggregator-sourced; none printed)
#   - Revenue unconfirmed — "We're going to end up at 5" read as $5M [transcript unclear]; confirm gross vs collected and next year's goal
#   - Ad spend range $3,500–$14,000 is far below the ~$25,000/mo the client said they spend now (transcript unclear) and the rule-derived aggressive figure exceeds the $50,000 Growth cap — paid ads team review
#   - ROI card uses benchmark CPL; client's own results (~$4,500 per client on a $9,100 case, about 2x) are far below the 15.6×–18.9× shown — seller must present it as a projection only
#   - Elite Coach price was garbled on the call ("$34.97"); client asked about a conference-only option for himself and his COO — not in this package
#   - Existing 97th Floor management fee and contract end date unknown; whether ads land on the firm's site or off-site unknown
#   - Revenue $3M+ and 4 locations: Growth tier chosen by seller; Growth covers up to 4 GBP locations (firm has 4 offices)

# Report metadata
FIRM_NAME      = "RCG Law Group"
SALES_REP      = "Nick Holderman"
OUTPUT_PATH    = "rcg-law-group/RCG Law Group_October 26, 2026_Proposal.pptx"

# ── Slide 1 — Your Priorities, In Your Words ─────────────────────
KPI_FOCUS = {
    "kind": "kpi",
    "label": "Cost per client",
    "headline": "About $4,500 cost per retained client.",
    "headline_is_quote": True,
    "detail": "About $4,500 per retained client on LSA and PPC, against a $9,100 average family law case.",
    "baseline": "$4,500 per client",
    "stats": [
        ("Average case value", "$9,100"),
        ("Cost per client on Meta", "$5,000"),
    ],
}

PROSPECT_QUOTES = [
    ("Ad costs",
     "When that's the average case value and that's the cost per retained client, that's 50% and that is horrible.",
     "Ad accounts audited first, then managed by our ads team"),
    ("Coaching",
     "Dedicated time to learning stuff, being with others, and then like, being able to do my quarterly planning.",
     "Elite Coach: weekly group coaching and quarterly workshops"),
    ("Paid ads",
     "I'm at the point right now where I'm going to tell them not to run any more pay-per-click or local service ads.",
     "A faster site and landing pages for ad clicks to land on"),
]

# ── Slide 2 — The Diagnosis ───────────────────────────────────────
DIAGNOSIS_TITLE = "Why Each Client Costs About $4,500"
DIAGNOSIS_INTRO = "Four things drive that number. Here's each one in plain English."

DIAGNOSIS = [
    {"title": "The website is too slow", "metric": "24 out of 100",
     "metric_label": "mobile speed score",
     "target": None,
     "body": "Homepage content took almost 23 seconds to show. A slow page can waste clicks you already paid for.",
     "source": "Seller test, on the call"},
    {"title": "Ads cost about half a case", "metric": "About $4,500",
     "metric_label": "per client, Google ads + LSA",
     "target": None,
     "body": "Google runs about $4,500 and Meta $5,000 per client. Your average family law case is $9,100.",
     "source": "Discovery call"},
    {"title": "Rivals outrank you locally", "metric": "",
     "metric_label": "",
     "target": None,
     "body": "On a live South Jordan search, the firm showed three down the line. Rivals ranked above it, with more reviews.",
     "source": "Seller, live on the call"},
    {"title": "Coaching gone, agency learning", "metric": "",
     "metric_label": "",
     "target": None,
     "body": "You've missed the quarterly conferences and planning time. Your agency has very few law firm clients.",
     "source": "Discovery call"},
]

DIAGNOSIS_FIX_LINE = "Marketing fixes the site, ads and local search; Elite Coach brings back the planning time and peer group."

# ── Slide 3 — The Plan ────────────────────────────────────────────
PLAN_KICKER = "Paid media, website and coaching"
PLAN_TITLE  = "Lower What Each Client Costs"

PLAN = [
    {"title": "Rebuild the site for speed", "fixes": 1,
     "actions": ["Site rebuilt for mobile speed",
                 "Up to 500 existing pages moved over",
                 "15,000 words of content at launch"],
     "metric": "Mobile speed score", "target": None},
    {"title": "Run law firm ad campaigns", "fixes": 2,
     "actions": ["Google, Local Service and Meta Ads managed",
                 "Meta retargeting of site visitors"],
     "metric": "Cost per client", "target": None},
    {"title": "Win more local searches", "fixes": 3,
     "actions": ["Google Business Profile, up to 4 offices",
                 "Review requests, up to 250 a month",
                 "4 premium backlinks a year"],
     "metric": "Local search position", "target": None},
    {"title": "Bring back planning, peers", "fixes": 4,
     "actions": ["Weekly group coaching sessions",
                 "Practice area masterminds",
                 "Virtual quarterly workshops"],
     "metric": "Planning sessions held", "target": None},
]

PLAN_NOTE = "60 minutes of website edits each month, and one annual in-person workshop."

# ── Slide 4 — The Recommended Strategy ────────────────────────────
STRATEGY_TITLE = "Three Pieces, One Strategy"

STRATEGY = [
    {"product": "Full Service Marketing — Growth", "title": "Fix the site",
     "channels": "Website · SEO · GBP · Reviews",
     "deliverables": ["Website rebuilt for mobile speed",
                      "15,000 words of content at launch",
                      "Up to 4 Google Business Profile locations",
                      "Review requests, up to 250 a month",
                      "4 premium backlinks a year"],
     "why": "The site scored 24 out of 100 on mobile, and rivals show above the firm in local search."},
    {"product": "Full Service Marketing — Growth", "title": "Run the ads",
     "channels": "Google Ads · LSA · Meta Ads",
     "deliverables": ["Google Ads campaign management",
                      "Local Service Ads management",
                      "Meta Ads management, including retargeting"],
     "why": "Paid clients cost about $4,500 each against a $9,100 average case."},
    {"product": "Elite Coach", "title": "Coaching",
     "channels": "Group coaching · Workshops",
     "deliverables": ["Weekly group coaching sessions",
                      "Practice area masterminds",
                      "Virtual access to quarterly workshops",
                      "One annual in-person workshop"],
     "why": "You want coaching packaged with marketing and your quarterly planning time back."},
]

# ── Speaker notes for the seller (never shown on a slide) ─────────
SELLER_NOTES = {
    1: "The $4,500, $5,000 and $9,100 figures are Ryan's own, from the call. Confirm that $4,500 covers Google Ads and Local Service Ads together before you present it.",
    2: "The 24 out of 100 speed score and the almost 23-second load time came from the free Google tool you ran live; Ryan re-ran it on his screen. The 'three down the line' result is what you saw in a live search. Ask whether his ads land on a page on his own site or off-site (he wasn't sure).",
    3: "Ask Ryan what cost per retained client he would count as a win before putting a target on this plan.",
    4: "Ryan asked about a conference-only option for himself and his COO. It is not part of this strategy, so ask what he has in mind.",
}

# ── Slide 5 — Your Investment ─────────────────────────────────────
PACKAGES = [
    (
        "FULL SERVICE MARKETING — GROWTH",
        "$7,497", "$8,997/mo",
        "Website · Google Ads · LSA · Meta Ads · GBP · review requests",
        "0091C9",
    ),
    (
        "ELITE COACH",
        "$2,600", "$3,497/mo",
        "Weekly group coaching · masterminds · quarterly workshops",
        "003A59",
    ),
]

BUNDLE_TOTAL   = "$10,097 / mo"
BUNDLE_SAVINGS = "Save $2,397/mo by bundling"

AD_SPEND_NOTE = (
    "+ Recommended ad spend: $3,500–$14,000/mo, paid to Google/Meta, to win local divorce searches"
)

AVG_CASE_VALUE     = "$9,100"
CONSERVATIVE_LABEL = "Conservative  (6 cases/mo):"
CONSERVATIVE_RESULT = "$54,600 revenue · 15.6× ROAS"
AGGRESSIVE_LABEL   = "Aggressive  (29 cases/mo):"
AGGRESSIVE_RESULT  = "$263,900 revenue · 18.9× ROAS"

CLOSING_QUOTE = (
    '"Marketing I can trust, and real time out of the office to plan with people who get it."'
)

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
# onboarding content exists — flip this to True to add it back (slide 5).
SHOW_ROLLOUT = False
TOTAL_SLIDES = 6 if SHOW_ROLLOUT else 5
INVESTMENT_PAGE = TOTAL_SLIDES

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
             min_size=None, anchor=None):
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


# Seller-only speaker notes, collected per slide while building.
_NOTES = {}


def note(page, text):
    if text:
        _NOTES.setdefault(page, []).append(str(text).strip())


def write_notes(prs):
    for page, slide in enumerate(prs.slides, start=1):
        lines = list(_NOTES.get(page, []))
        own = SELLER_NOTES.get(page) if isinstance(SELLER_NOTES, dict) else None
        if own:
            lines.insert(0, str(own).strip())
        if lines:
            slide.notes_slide.notes_text_frame.text = (
                "FOR THE SELLER — not shown on the slide.\n\n" + "\n\n".join(lines))


def _quote(text):
    return "“" + str(text).strip().strip('"“”') + "”"


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
    if kind == "qualitative" and not str(SELLER_NOTES.get(1, "")).strip():
        problems.append('KPI_FOCUS is "qualitative": SELLER_NOTES[1] must tell the '
                        "seller there was no usable number on the call and what to ask for.")
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
    if problems:
        raise SystemExit("Deck not built — fix the values above the LAYOUT ENGINE line:\n  - " + "\n  - ".join(problems))


# ── Slide 1: Your Priorities, In Your Words ───────────────────────

def build_priorities(prs):
    slide = new_slide(prs)
    add_header(slide, "Your Priorities, In Your Words", 9.30, kicker="WHAT WE HEARD")
    quotes = [q for q in PROSPECT_QUOTES[:3] if q and len(q) >= 2 and q[1]]

    # Left (full width with no quotes): the one number from the call.
    x, y, h = 0.30, 1.10, 3.98
    w = 4.60 if quotes else 9.40
    add_rect(slide, x, y, w, h, fill=NAVY)
    add_pill(slide, KPI_FOCUS["label"], x + 0.24, y + 0.24, 0.27, OCEAN_BLUE,
             max_w=w - 0.48)
    headline = KPI_FOCUS["headline"]
    if KPI_FOCUS.get("headline_is_quote"):
        headline = _quote(headline)
    add_text(slide, headline, x + 0.18, y + 0.64, w - 0.36, 1.40, 22, WHITE,
             bold=True, max_lines=3, min_size=14, anchor=MSO_ANCHOR.TOP,
             cap_label="KPI_FOCUS headline")
    # The detail line sits right under the headline, however many lines it took.
    h_size, h_lines = fit_text(headline, w - 0.36, 1.40, 22, bold=True, max_lines=3, min_size=14)
    used = (len(h_lines) * line_height(h_size, bold=True) + 2 * _INSET_Y) if h_lines else 1.40
    add_text(slide, KPI_FOCUS["detail"], x + 0.18, y + 0.64 + used + 0.12, w - 0.36, 0.74, 10.5,
             NAVY_TEXT_SOFT, max_lines=3, min_size=8.5, cap_label="KPI_FOCUS detail")
    stats = [s for s in (KPI_FOCUS.get("stats") or [])[:2] if s and s[1]]
    if stats:
        add_rule(slide, x + 0.24, y + 2.94, x + w - 0.24, y + 2.94, NAVY_RULE)
        col = (w - 0.36) / len(stats)
        for i, (lab, val) in enumerate(stats):
            sx = x + 0.18 + i * col
            add_text(slide, str(lab).upper(), sx, y + 3.04, col - 0.08, 0.22, 7.5,
                     LIME_GREEN, bold=True, max_lines=1, cap_label=f"KPI stat {i+1} label")
            add_text(slide, val, sx, y + 3.26, col - 0.08, 0.64, 10, WHITE,
                     max_lines=2, min_size=8, cap_label=f"KPI stat {i+1} value")

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

    if KPI_FOCUS.get("kind") == "qualitative":
        note(1, "No usable number came out of the call, so this slide leads with the "
                "client's pain point instead of a KPI.")
    add_footer(slide, 1, TOTAL_SLIDES, LOGO_PATH)


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
                 9, BODY_TEXT, min_size=7.5, cap_label=f"DIAGNOSIS[{i}] body")
        if d.get("source"):
            add_text(slide, "Source: " + str(d["source"]), cx + 0.08, y + h - 0.28,
                     cw - 0.16, 0.22, 7, SLATE, max_lines=1, min_size=6,
                     cap_label=f"DIAGNOSIS[{i}] source")

    add_strip(slide, "How we fix it:", DIAGNOSIS_FIX_LINE, 4.64, label="DIAGNOSIS_FIX_LINE")
    add_footer(slide, 2, TOTAL_SLIDES, LOGO_PATH)


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
        note(3, "No target on the call to base these on, so none is shown — agree a "
                "number with the client rather than quoting one: " + "; ".join(missing) + ".")
    add_footer(slide, 3, TOTAL_SLIDES, LOGO_PATH)


def build_measures(slide, top, bottom):
    """"What we'll measure": the call KPI (today's value), then each plan
    action's metric, numbered to its card, with its target when there is one.
    No target → no target line (never "to be confirmed")."""
    add_text(slide, "WHAT WE'LL MEASURE", 0.30, top, 4.0, 0.20, 7.5, NAVY, bold=True,
             fit=False)
    tiles = [(None, KPI_FOCUS["label"],
              ("Today: " + KPI_FOCUS["baseline"]) if KPI_FOCUS.get("baseline") else "")]
    tiles += [(i + 1, p["metric"], ("Target: " + str(p["target"])) if p.get("target") else "")
              for i, p in enumerate(PLAN)]
    gap = 0.12
    ty = top + 0.22
    th = bottom - ty
    tw = (9.40 - gap * (len(tiles) - 1)) / len(tiles)
    for i, (num, title, sub) in enumerate(tiles):
        tx = 0.30 + i * (tw + gap)
        lead = num is None
        add_rect(slide, tx, ty, tw, th, fill=NAVY if lead else WHITE)
        if lead:
            add_text(slide, "THE NUMBER FROM THE CALL", tx + 0.10, ty + 0.06, tw - 0.20, 0.18,
                     6.5, LIME_GREEN, bold=True, max_lines=1, min_size=5.5,
                     cap_label="measure kicker")
            title_x, title_w = tx + 0.10, tw - 0.20
        else:
            add_badge(slide, num, tx + 0.10, ty + 0.08, 0.24, OCEAN_BLUE)
            title_x, title_w = tx + 0.38, tw - 0.46
        title_y = ty + (0.22 if lead else 0.04)
        add_text(slide, title, title_x, title_y, title_w, 0.40, 9.5,
                 WHITE if lead else NAVY, bold=True, max_lines=2, min_size=7.5,
                 anchor=MSO_ANCHOR.MIDDLE if not lead else None,
                 cap_label=f"measure tile {i+1}")
        if sub:
            sub_y = title_y + 0.40
            add_text(slide, sub, tx + 0.10, sub_y, tw - 0.20, max(0.22, ty + th - sub_y - 0.04),
                     8.5, NAVY_TEXT_SOFT if lead else GREEN, bold=not lead, max_lines=2,
                     min_size=7, cap_label=f"measure tile {i+1} sub")


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
        add_text(slide, s["product"], cx + 0.14, y + 0.84, cw - 0.28, 0.22, 8, SLATE,
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
    add_footer(slide, 4, TOTAL_SLIDES, LOGO_PATH)


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

    note(5, "PLACEHOLDER: real onboarding content isn't ready yet. Don't promise "
            "onboarding steps, dates or timelines from this slide.")
    add_footer(slide, 5, TOTAL_SLIDES, LOGO_PATH)

# ── Last slide: Your Investment (numbers unchanged from the 3-slide deck) ──

def build_investment(prs):
    layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(layout)

    # Background wash + header (shared with every slide)
    add_header(slide, "Your Investment", 9.30, kicker="THE INVESTMENT")

    # Package cards — white with a thin colored left accent bar
    pkg_ys = [1.10, 2.25]
    for i, (label, price, retail, services, hex_c) in enumerate(PACKAGES[:2]):
        y = pkg_ys[i]
        ac = rgb(hex_c)
        add_rect(slide, 0.30, y, 4.42, 1.05, fill=WHITE)
        add_rect(slide, 0.30, y, 0.04, 1.05, fill=ac)
        add_text(slide, label, 0.56, y+0.12, 3.96, 0.20, 7.5, ac, bold=True,
                 max_lines=1, cap_label=f"PACKAGES[{i}] label")
        # Price, "/mo" and retail price share one baseline; "/mo" follows the
        # price's measured width so it never collides or wraps.
        price_top = y + 0.27
        price_size, _ = fit_text(price, 2.60, 0.58, 30, bold=True, max_lines=1)
        price_size = price_size or 22
        add_text(slide, price, 0.56, price_top, 2.60, 0.58, price_size, NAVY,
                 bold=True, fit=False)
        baseline = price_top + baseline_offset(price_size, bold=True)
        mo_x = 0.56 + _INSET_X + text_width(price, price_size, bold=True) + 0.04 - _INSET_X
        add_text(slide, "/mo", mo_x, baseline - baseline_offset(10), 0.50, 0.24, 10,
                 SLATE, wrap=False, fit=False)
        retail_x = mo_x + 2 * _INSET_X + text_width("/mo", 10) + 0.06
        add_text(slide, retail, retail_x, baseline - baseline_offset(10),
                 4.62 - retail_x, 0.24, 10, SLATE, align=PP_ALIGN.RIGHT,
                 max_lines=1, cap_label=f"PACKAGES[{i}] retail")
        add_text(slide, services, 0.56, y+0.80, 3.96, 0.22, 8.5, SLATE, max_lines=1,
                 cap_chars=61, cap_label=f"PACKAGES[{i}] services")

    # Bundle total — same 0.10in gap used between the two package cards above
    add_rect(slide, 0.30, 3.40, 4.42, 0.72, fill=NAVY)
    add_rect(slide, 0.30, 3.40, 0.04, 0.72, fill=LIME_GREEN)
    add_text(slide, "BUNDLE TOTAL", 0.56, 3.50, 1.70, 0.18, 7.5, LIME_GREEN, bold=True,
             fit=False)
    total_size, _ = fit_text(BUNDLE_TOTAL, 2.40, 0.40, 17, bold=True, max_lines=1)
    total_size = total_size or 13
    add_text(slide, BUNDLE_TOTAL, 0.56, 3.66, 2.40, 0.40, total_size, WHITE, bold=True,
             fit=False)
    # Savings line sits to the right of the measured total, on its baseline,
    # and shrinks to fit the space left inside the card.
    total_baseline = 3.66 + baseline_offset(total_size, bold=True)
    savings_x = 0.56 + text_width(BUNDLE_TOTAL, total_size, bold=True) + 0.20
    add_text(slide, BUNDLE_SAVINGS, savings_x, total_baseline - baseline_offset(8.5),
             4.62 - savings_x, 0.22, 8.5, BUNDLE_SAVINGS_TEXT, align=PP_ALIGN.RIGHT,
             max_lines=1, cap_label="BUNDLE_SAVINGS")

    # Ad spend note + ROI-on-ad-spend card — both omitted entirely when no
    # marketing/ads package was sold. Showing a return-on-ad-spend projection
    # for ad spend that isn't part of the recommendation is the same bug as
    # the missing-rationale note, just in a second spot on this slide.
    has_ad_spend = bool(AD_SPEND_NOTE)

    if has_ad_spend:
        add_rect(slide, 0.30, 4.22, 4.42, 0.42, fill=rgb("EEF2F5"))
        add_text(slide, AD_SPEND_NOTE, 0.50, 4.22, 4.02, 0.42, 8, BODY_TEXT,
                 cap_chars=120, cap_label="AD_SPEND_NOTE")

        # ROI card
        add_rect(slide, 5.00, 1.10, 4.70, 1.42, fill=ROI_BG)
        add_text(slide, "PROJECTED RETURN ON AD SPEND",
                 5.22, 1.26, 4.26, 0.16, 7.5, ROI_GREEN, bold=True)
        add_text(slide, "Average case value:", 5.22, 1.58, 1.95, 0.18, 8.5, DARK_TEXT, bold=True)
        add_text(slide, AVG_CASE_VALUE, 7.25, 1.58, 2.30, 0.18, 8.5, ROI_GREEN)
        add_rect(slide, 5.14, 1.83, 4.42, 0.28, fill=ROI_HILIGHT)
        add_text(slide, CONSERVATIVE_LABEL, 5.22, 1.90, 1.95, 0.18, 8.5, DARK_TEXT, bold=True)
        add_text(slide, CONSERVATIVE_RESULT, 7.25, 1.90, 2.30, 0.18, 8.5, ROI_GREEN, bold=True)
        add_text(slide, AGGRESSIVE_LABEL, 5.22, 2.21, 1.95, 0.18, 8.5, DARK_TEXT, bold=True)
        add_text(slide, AGGRESSIVE_RESULT, 7.25, 2.21, 2.30, 0.18, 8.5, ROI_GREEN, bold=True)

    # Closing quote bar — taller, darker navy, with the same lime accent stripe
    add_rect(slide, 0, 4.66, 10, 0.61, fill=rgb("002A41"))
    add_rect(slide, 0, 4.66, 10, 0.02, fill=LIME_GREEN)
    add_text(slide, CLOSING_QUOTE, 0.70, 4.70, 8.60, 0.54, 9.5, rgb("C2D8E6"),
             align=PP_ALIGN.CENTER, max_lines=2, anchor=MSO_ANCHOR.MIDDLE,
             cap_chars=200, cap_label="CLOSING_QUOTE")

    add_footer(slide, INVESTMENT_PAGE, TOTAL_SLIDES, LOGO_PATH)

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

build_priorities(prs)
build_diagnosis(prs)
build_plan(prs)
build_strategy(prs)
if SHOW_ROLLOUT:
    build_rollout(prs)
build_investment(prs)
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

if _NOTES or SELLER_NOTES:
    pages = sorted(set(_NOTES) | {k for k, v in SELLER_NOTES.items() if v})
    print("SELLER NOTES on slide(s): " + ", ".join(str(p) for p in pages))

print(f"Saved: {OUTPUT_PATH}  ({len(prs.slides)} slides)")
