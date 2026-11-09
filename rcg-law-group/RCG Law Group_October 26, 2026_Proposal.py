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
Slide 5 — Your Investment                 (what $X/mo buys, year one, ad spend, return —
                                           every number read from package_decision.json)
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
# Year one: $121,164 (from package_decision.json → investment.year_one_total)
# Ad spend (copied from investment.ad_spend — computed in code, never by hand):
#   $25,000–$50,000/mo · low end: current spend stated on the call ($25,000/mo) held at launch — above the $6,700 channel floor
#   · high end: 20% rule $159,170 → reverse math $412,088 (91.6 cases/mo × $4,500 stated) → capped at the $50,000 the package manages
# Return (copied from investment.return): stated_cost_per_case · At today's $4,500 cost per signed case and a $9,100 average case (said on the call),
#   no improvement assumed · scenarios: $25,000 → 5.6 cases → $50,600 → 2× · $50,000 → 11.1 cases → $101,100 → 2×
# Investment inputs used: practice area Family Law (research notes) · geo tier 4 (research notes) · competitiveness High (research notes) ·
#   case value $9,100 (call) · close rate 21% (call) · current ad spend $25,000 (call) · cost per case $4,500 (call) ·
#   revenue goal $10,000,000 = 2× current revenue (not stated) · flags: reverse math far above 20% rule (paid ads team review);
#   goal-based spend above $50,000 Growth cap — capped, tier upgrade or 10% overage is the seller's call; ad spend over $25K.
# Why this range: to turn high-intent family law searches into signed cases.
# Pillar review: Lead Gen amber — paid cost per retained client ~$4,500 and referrals carry growth · Intake amber — close rate 21% on cold leads, intake process not discussed ·
#   Team amber — COO and two VAs, business partner left ~4 months ago · Profit amber — Ryan: paid cost is "50%" of case value; margins otherwise not stated
# KPI (slide 1): Cost per client (LSA + PPC) — "about $4,500 cost per retained client" — client, 00:07:10 (STEP 9B)
# Diagnosis (slide 2): 1. Website too slow — PageSpeed mobile 24/100 — call seller 00:10:10, Ryan 00:11:42; Lighthouse re-run Nov 9 mobile 24
#   · 2. Paid cost half a case — about $4,500 LSA/PPC vs $9,100 case; Meta about $5,000 — Ryan 00:07:10–00:07:51
#   · 3. Referrals/organic carry growth — "ton of referrals or just website stuff" 00:07:53; seller's search "three down the line" 00:12:50–00:13:18 (seller observation, not re-verified)
#   · 4. No coaching rhythm — Ryan 00:00:59, 00:01:17 (STEP 9B)
# Targets (slides 2–3): none — seller note. PageSpeed: seller flag line "sub 60 or 70" (00:11:44) is a threshold, not a goal; paid cost: none stated;
#   revenue: seller-quoted prior $6M target not restated by Ryan.
# What You Told Us (slide 1 quotes and tie lines):
#   1. Cost vs. case value — transcript line: "So when that's the average case value and that's the cost per retained client, that's 50% and that is horrible." — supports: Full Service Marketing — Growth
#   2. Paid results — transcript line: "But when I look and isolate PPC and LSA and meta, it's freaking, I can't keep doing it." — supports: Full Service Marketing — Growth
#   3. Coaching — transcript line: "I got so much value in getting out of the office, dedicated time to learning stuff, being with others…" — supports: Elite Coach
# Overrides applied: seller override (package_source trigger_override: "Full Service Marketing — Growth + Elite Coach") used as-is; the four Transcript-Stated Need
#   overrides do not apply. Rules it departs from: revenue ~$5M implies Platinum marketing tier (decision selection_notes) and Master's Circle / Elite Coach Plus
#   rather than Elite Coach; 97th Floor is a current marketing vendor (existing-vendor override would exclude FSM) — Ryan said 90% likelihood of changing agency to SMB Team.
#   Ad spend cap for Growth is $50,000.
# Escalation flags: Ad spend over $25K — scoping approval required · reverse math ($412,088) well above 20% rule — paid ads team review ·
#   goal-based spend above Growth cap — tier upgrade or 10% overage (seller decision) · Review counts unconfirmed — verify live before the call ·
#   "5" read as $5M revenue [transcript unclear] — confirm gross vs collected · Elite Coach price quoted on call as "$34.97" [transcript unclear] ·
#   trigger Fathom link (860679147) is not the Oct 14 transcript supplied — confirm what was agreed on the Oct 26 follow-up and read-only Google Ads access ·
#   Ryan's objection that SMB Team quality dropped the last six months — confirm he is comfortable ·
#   Competitor review counts and the "three down the line" search are unverified — recheck live.

# Report metadata
FIRM_NAME      = "RCG Law Group"
SALES_REP      = "Nick Holderman"
OUTPUT_PATH    = "rcg-law-group/RCG Law Group_October 26, 2026_Proposal.pptx"

# ── Slide 1 — Your Priorities, In Your Words ─────────────────────
KPI_FOCUS = {
    "kind": "kpi",
    "label": "Cost per client",
    "headline": "Averages about $4,500 cost per retained client",
    "headline_is_quote": True,
    "detail": "About $4,500 per retained client on LSA and PPC, on a $9,100 average family law case.",
    "baseline": "About $4,500",
    "stats": [
        ("Avg. family law case", "$9,100"),
        ("Last month's ad spend", "About $25K"),
    ],
}

PROSPECT_QUOTES = [
    ("Cost vs. case value",
     "So when that's the average case value and that's the cost per retained client, that's 50% and that is horrible.",
     "Ads, website and SEO planned together around each signed case"),
    ("Paid results",
     "When I look and isolate PPC and LSA and meta, it's freaking, I can't keep doing it.",
     "Google Ads, LSA and Meta managed under one plan"),
    ("Coaching",
     "I got so much value in getting out of the office, dedicated time to learning stuff, being with others…",
     "Elite Coach: group coaching, masterminds, quarterly workshops"),
]

# ── Slide 2 — The Diagnosis ───────────────────────────────────────
DIAGNOSIS_TITLE = "Why Each Client Costs About $4,500"
DIAGNOSIS_INTRO = "Four things sit behind that number. Here's each one in plain English."

DIAGNOSIS = [
    {"title": "Website too slow to convert", "metric": "24/100", "metric_label": "PageSpeed mobile score",
     "target": None, "body": "Mobile scored 24 out of 100 when we ran it live. Slow pages lose visitors before they call.",
     "source": "PageSpeed, run live on the call"},
    {"title": "Paid ads cost half a case", "metric": "$4,500", "metric_label": "per retained client, LSA + PPC",
     "target": None, "body": "LSA and PPC have run near this for about a year. Meta is about $5,000 a client.",
     "source": "Discovery call"},
    {"title": "Growth leans on referrals", "metric": "", "metric_label": "",
     "target": None, "body": "You said referrals and website content carry growth. A live search on the call showed the firm three down.",
     "source": "Discovery call, live search"},
    {"title": "No coaching or planning rhythm", "metric": "", "metric_label": "",
     "target": None, "body": "Since leaving coaching you've missed the quarterly conferences and the planning time that came with them.",
     "source": "Discovery call"},
]

DIAGNOSIS_FIX_LINE = "A faster website, managed ads, local SEO and Google profile work, and Elite Coach planning: one for each cause."

# ── Slide 3 — The Plan ────────────────────────────────────────────
PLAN_KICKER = "Paid media, website and coaching"
PLAN_TITLE  = "Lower What Each Client Costs"

PLAN = [
    {"title": "Rebuild the website for speed", "fixes": 1,
     "actions": ["Website rebuild for speed",
                 "Up to 500 pages imported",
                 "15,000 words of new content",
                 "60 minutes of edits a month"],
     "metric": "Mobile PageSpeed", "target": None},
    {"title": "Restructure the paid campaigns", "fixes": 2,
     "actions": ["Google Ads management",
                 "Local Services Ads management",
                 "Meta retargeting management"],
     "metric": "Cost per client", "target": None},
    {"title": "Win local search and reviews", "fixes": 3,
     "actions": ["Local and organic SEO",
                 "Google profile, up to 4 locations",
                 "Review requests, up to 250 a month"],
     "metric": "Local search position", "target": None},
    {"title": "Restore quarterly planning", "fixes": 4,
     "actions": ["Weekly group coaching sessions",
                 "Quarterly workshops, virtual access",
                 "One annual in-person workshop"],
     "metric": "Planning rhythm", "target": None},
]

PLAN_NOTE = "12,000 words of content a year after launch · 4 premium backlinks a year · practice area masterminds"

# ── Slide 4 — The Recommended Strategy ────────────────────────────
STRATEGY_TITLE = "Marketing and Coaching, One Plan"

STRATEGY = [
    {"product": "Full Service Marketing — Growth", "title": "Get found", "channels": "Website · SEO · Google profile",
     "deliverables": ["Website rebuild for speed and conversion",
                      "15,000 words of content at launch",
                      "Up to 500 pages of existing content imported",
                      "Google profile optimization, up to 4 locations",
                      "4 premium backlinks a year"],
     "why": "Answers the 24/100 mobile score and the firm's place in local search."},
    {"product": "Full Service Marketing — Growth", "title": "Get the call", "channels": "Google Ads · LSA · Meta",
     "deliverables": ["Google Ads management",
                      "Local Services Ads management",
                      "Meta retargeting management",
                      "Review requests, up to 250 a month"],
     "why": "Goes after the $4,500 cost per retained client in today's paid campaigns."},
    {"product": "Elite Coach", "title": "Plan and grow", "channels": "Group coaching · Workshops",
     "deliverables": ["Weekly group coaching sessions",
                      "Practice area masterminds",
                      "Virtual access to quarterly workshops",
                      "One annual in-person workshop"],
     "why": "Brings back the quarterly planning time you said you've missed."},
]

# ── Speaker notes for the seller (never shown on a slide) ─────────
SELLER_NOTES = {
    1: "The $4,500, $9,100 and about $25K figures are Ryan's from the call; the 50% is his own wording. Confirm the window behind the $4,500 and how 'retained' is counted. Ask what growth would let him do personally.",
    2: "The 24 was read live on the call and re-checked afterward. Ask what PageSpeed target Ryan wants. The 'three down the line' search was your on-screen observation, so re-check it live before the call.",
    3: "No cost-per-client or planning goals were stated. Ask Ryan what he would want to pay per client and what planning rhythm he wants.",
}

# ── Slide 5 — Your Investment ─────────────────────────────────────
PRODUCT_LINES = {
    "Full Service Marketing — Growth": "Website · SEO · Google Ads · LSA · Meta · Google profile · Reviews",
    "Elite Coach": "Group coaching · Masterminds · Quarterly workshops · Annual workshop",
}

AD_SPEND_WHY = "to turn high-intent family law searches into signed cases"

CLOSING_QUOTE = (
    '"Dedicated time to learning stuff, being with others… being able to do my quarterly planning."'
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

# ── Last slide: Your Investment (numbers from package_decision.json) ──

# Where the computed investment lives: the firm's package_decision.json,
# next to this script. The master template has none, so it renders a sample.
DECISION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "package_decision.json")
_SAMPLE_INVESTMENT = {
    "products": [
        {"name": "Full Service Marketing — Growth", "charged": 7497, "standalone": 8997},
    ],
    "monthly_total": 7497, "total_savings": 0, "pricing_mode": "standalone",
    "year_one_total": 89964,
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
    for i, p in enumerate(rows):
        ry = y + i * rh_used
        if i:
            add_rule(slide, x + 0.20, ry, x + w - 0.16, ry, RULE_GRAY)
        name_w = w - 1.85
        add_text(slide, p["name"], x + 0.18, ry + 0.06, name_w, 0.30, 10.5, NAVY, bold=True,
                 max_lines=1, min_size=8, cap_label=f"product {i+1} name")
        items = [t.strip() for t in re.split(r"\s*[·•|]\s*", product_line(p["name"])) if t.strip()]
        half_rows = (len(items) + 1) // 2
        if len(items) >= 3 and rh_used - 0.70 >= half_rows * 0.27:
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
        sub = ""
        if standalone_mode and p.get("standalone"):
            sub = "stand-alone price"
        elif p.get("standalone") and p.get("charged") is not None and p["standalone"] > p["charged"]:
            sub = f"stand-alone {usd(p['standalone'])}/mo"
        if sub:
            add_text(slide, sub, x + w - 1.70, ry + 0.36, 1.58, 0.22, 7.5, SLATE,
                     align=PP_ALIGN.RIGHT, max_lines=1, fit=False)


def build_totals_block(slide, inv, x, w, top, bottom):
    """Navy block: the monthly investment beside the year-one total."""
    h = bottom - top
    add_rect(slide, x, top, w, h, fill=NAVY)
    add_rect(slide, x, top, 0.05, h, fill=LIME_GREEN)
    cells = [("MONTHLY INVESTMENT", f"{usd(inv['monthly_total'])}/mo",
              (f"Saves {usd(inv['total_savings'])}/mo by bundling" if inv.get("total_savings")
               else "Stand-alone pricing (no bundle)")),
             ("YEAR ONE", usd(inv["year_one_total"]),
              "12 months of fees")]
    cw = (w - 0.10) / 2
    for i, (kicker, big, sub) in enumerate(cells):
        cx = x + 0.10 + i * cw
        if i:
            add_rule(slide, cx - 0.04, top + 0.14, cx - 0.04, bottom - 0.14, NAVY_RULE)
        add_text(slide, kicker, cx + 0.12, top + 0.10, cw - 0.24, 0.20, 7.5, LIME_GREEN,
                 bold=True, fit=False)
        add_text(slide, big, cx + 0.12, top + 0.28, cw - 0.24, 0.42, 20, WHITE, bold=True,
                 max_lines=1, min_size=13, cap_label=f"total {i+1}")
        add_text(slide, sub, cx + 0.12, top + 0.68, cw - 0.24, h - 0.74, 8, BUNDLE_SAVINGS_TEXT
                 if i == 0 else NAVY_TEXT_SOFT, max_lines=2, min_size=6.5, cap_label=f"total {i+1} sub")


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
    if ad:
        left_w = 5.00
        build_buys_card(slide, inv, 0.30, left_w, 1.04, 3.66)
        build_totals_block(slide, inv, 0.30, left_w, 3.76, 4.74)
        rx, rw = 5.50, 4.20
        if ret:
            build_ad_spend_card(slide, ad, rx, rw, 1.04, 2.56)
            build_return_card(slide, ret, rx, rw, 2.64, 4.74)
        else:
            build_ad_spend_card(slide, ad, rx, rw, 1.04, 4.74)
    else:
        build_buys_card(slide, inv, 0.30, 9.40, 1.04, 3.66)
        build_totals_block(slide, inv, 0.30, 9.40, 3.76, 4.74)

    # Closing line — the owner's outcome, in their words.
    add_rect(slide, 0, 4.84, 10, 0.43, fill=rgb("002A41"))
    add_rect(slide, 0, 4.84, 10, 0.02, fill=LIME_GREEN)
    add_text(slide, CLOSING_QUOTE, 0.70, 4.86, 8.60, 0.40, 9.5, NAVY_TEXT_SOFT,
             align=PP_ALIGN.CENTER, max_lines=1, min_size=7.5, anchor=MSO_ANCHOR.MIDDLE,
             cap_chars=160, cap_label="CLOSING_QUOTE")
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
