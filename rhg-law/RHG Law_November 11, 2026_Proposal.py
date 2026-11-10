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

# ── BUILD NOTES (internal — never shown on a slide) ──────────────
# Marketing package: none — coaching/ops-led call, no lead-gen need ("I don't think that marketing will be a problem", 00:18:26)
# Non-marketing package(s): Elite Coach Plus — bundled $3,497/mo, stand-alone $3,497/mo, savings $0/mo
# LAW package: AI Workforce Pro – Starter (1 seat) — $350/mo, no stand-alone price (does not count toward a bundle)
# Total monthly investment: $3,847/mo · total savings: $0/mo · pricing_mode: standalone
# Year one: $46,164 (from package_decision.json → investment.year_one_total)
# Ad spend (copied from investment.ad_spend): none — no paid-ads package, no ad spend or return panels
# Return (copied from investment.return): none
# Investment inputs used: none stated (investment.inputs empty) · flags: none (investment.flags empty)
# Why this range: n/a — no paid ads
# Pillar review: Lead Gen green — reviews and word of mouth bring more calls than he can handle · Intake red — owner not doing intakes for half of inbound ("half of them") · Team red — owner holds 40 to 60 files, one intern, per diem attorneys, first associate not yet hired · Profit amber — manual QuickBooks billing, believes some time goes unbilled, no figures given
# KPI (slide 1): Active files — "I'm the bottleneck right now" — client, 00:04:55 · detail figures "40 to 60 files" (00:10:00 / goal quote 00:11:45) and goal "10… 15 files at a time" (00:11:45) · no STEP 9B block in these notes, so only STEP 9 figures used
# Diagnosis (slide 2): 1. Files all sit with you — 40 to 60 files — client, 00:11:45 / 00:13:06 · 2. Intakes are going undone — "half of them" — client, 00:05:06 · 3. Billing takes hours every month — "takes hours every month" — client, 00:21:06 · 4. A merger is coming — "within the next six months or so" — client, 00:07:26
# Targets (slides 2–3): Files you handle — 10… 15 files at a time — basis: client's stated five-year goal (00:11:45–00:12:00), worded as theirs · all other targets: none — seller note
# Client's why (slide 1): "I want, obviously, more time and more money" — Roy Gordon (client), 00:12:06 · Cost of inaction: none on the call
# Closing quote (slide 5): "Me to be handling maybe 10… 15 files at a time, and consulting the other attorneys…" — Roy Gordon (client), 00:11:45
# Legacy Staircase slide: left out — not walked through on the call
# Plan (slide 3): Plan the associate hire — tied to: "It's kind of scary to hire another attorney…" · Write the intake SOP — tied to: "I'm not even doing the intakes for them anymore" · Put AI to work on billing — tied to: "get the AI employee to do like the billing stuff for me" · Get the merger ready — tied to: planned merger "within the next six months or so"
# What You Told Us (slide 1 quotes and tie lines):
#   1. Intakes — transcript line: "I'm not even, half of them, I'm not even doing the intakes for them anymore." — supports: Elite Coach Plus
#   2. Hiring — transcript line: "It's kind of scary to hire another attorney when I don't know if it's going to work out…" — supports: Elite Coach Plus
#   (third card dropped — client's why and the quote cards share the slide)
# Overrides applied: seller overrides in Slack on 2026-11-10 (selection_notes): AI Workforce Pro – Starter re-added (1 seat; client signed up at the workshop); revenue confirmed $300,000; coaching switched to Elite Coach Plus. Built as-is. Rule note: the revenue table gives Elite Coach for $250K–$400K and Elite Coach Plus for $400K–$1M — seller chose Plus anyway. 35% cap check: $3,847/mo is 15.4% of $25,000/mo revenue — within the cap.
# Escalation flags: Legal AI Workforce (LAW) package — confirm with sales rep that LAW delivery has launched and capacity is available · AI Workforce Pro – Starter seat count assumed 1 (team size not stated) — confirm · Prospect bought AI Workforce Pro – Starter himself before the proposal — confirm it is billed through SMB Team · Review counts unconfirmed — verify live before the call (no count used in the deck)

# Report metadata
FIRM_NAME      = "RHG Law"
SALES_REP      = "Daniel Lowe"
OUTPUT_PATH    = "rhg-law/RHG Law_November 11, 2026_Proposal.pptx"

# ── Slide 1 — Your Priorities, In Your Words ─────────────────────
KPI_FOCUS = {
    "kind": "kpi",
    "label": "Active files",
    "headline": "I'm the bottleneck right now",
    "headline_is_quote": True,
    "detail": "You handle 40 to 60 files; your goal is 10… 15 at a time.",
    "baseline": "40 to 60 files",
    "stats": [
        ("Your goal", "10… 15 files at a time"),
        ("Merger planned", "Within the next six months or so"),
    ],
    "said_by": "Roy Gordon (client), 00:04:55",
}

PROSPECT_QUOTES = [
    ("Intakes", "I'm not even, half of them, I'm not even doing the intakes for them anymore.",
     "An intake process your team can run without you", "Roy Gordon (client), 00:05:06"),
    ("Hiring", "It's kind of scary to hire another attorney when I don't know if it's going to work out",
     "Coaching to plan the hire and the hand-off", "Roy Gordon (client), 00:14:02"),
]

CLIENT_WHY = ("I want, obviously, more time and more money", "",
              "Roy Gordon (client), 00:12:06")
COST_OF_INACTION = None

# ── Optional slide — Lawyer Legacy Staircase ─────────────────────
STAIRCASE = None

# ── Slide 2 — The Diagnosis ───────────────────────────────────────
DIAGNOSIS_TITLE = "Why You Handle 40 to 60 Files"
DIAGNOSIS_INTRO = "Four things keep that caseload on your desk. Here's each one."

DIAGNOSIS = [
    {"title": "Files all sit with you", "metric": "40 to 60", "metric_label": "files in your own caseload",
     "target": "10… 15 files (your goal)",
     "body": "Past associate hires didn't work out, so the files stay with you.",
     "source": "Discovery call, Oct 30"},
    {"title": "Intakes are going undone", "metric": "Half", "metric_label": "of inbound intakes not being done",
     "target": None,
     "body": "Callers wait while you catch up on the files you already have.",
     "source": "Discovery call, Oct 30"},
    {"title": "Billing takes hours every month", "metric": "", "metric_label": "",
     "target": None,
     "body": "Monthly billing is done by hand, and some time never gets billed.",
     "source": "Discovery call, Oct 30"},
    {"title": "A merger is coming", "metric": "", "metric_label": "",
     "target": None,
     "body": "Two solo practices are joining within the next six months or so.",
     "source": "Discovery call, Oct 30"},
]

DIAGNOSIS_FIX_LINE = "Each cause gets its own action, worked through in weekly coaching and AI sessions."

# ── Slide 3 — The Plan ────────────────────────────────────────────
PLAN_KICKER = "Coaching and AI"
PLAN_TITLE  = "Get Files Off Your Desk"

PLAN = [
    {"title": "Plan the associate hire", "fixes": 1,
     "actions": ["Build the hiring and hand-off plan in group coaching",
                 "Accountability to see the plan through"],
     "metric": "Files you handle", "target": None, "baseline": None},
    {"title": "Write the intake SOP", "fixes": 2,
     "actions": ["Build the intake process in weekly group coaching",
                 "Practice area masterminds to compare intake setups"],
     "metric": "Intakes you do yourself", "target": None, "baseline": "Half not being done"},
    {"title": "Put AI to work on billing", "fixes": 3,
     "actions": ["Weekly AI Implementation Session on billing",
                 "AI Workforce Pro access for time-keeping"],
     "metric": "Billing hours", "target": None, "baseline": "Hours every month"},
    {"title": "Get the merger ready", "fixes": 4,
     "actions": ["Work the merger plan in weekly group coaching",
                 "Virtual quarterly workshops on running the firm"],
     "metric": "Merger plan", "target": None, "baseline": None},
]

PLAN_NOTE = "Weekly group coaching, practice area masterminds, virtual quarterly workshops and one annual in-person workshop."

# ── Slide 4 — The Recommended Strategy ────────────────────────────
STRATEGY_TITLE = "Two Pieces, One Strategy"

STRATEGY = [
    {"product": "Elite Coach Plus", "title": "Run the firm",
     "channels": "Coaching · Accountability",
     "deliverables": ["Weekly group coaching sessions",
                      "Practice area masterminds",
                      "Virtual access to quarterly workshops",
                      "One annual in-person workshop"],
     "why": "You're the bottleneck; coaching builds the hiring, intake and merger system."},
    {"product": "AI Workforce Pro – Starter", "title": "Automate billing",
     "channels": "AI employees · Weekly session",
     "deliverables": ["Access to AI Workforce Pro",
                      "Weekly AI Implementation Session",
                      "1M AI credits per user",
                      "Month-to-month contract"],
     "why": "Billing takes hours every month; an AI employee can take it on."},
]

# ── Seller prep (never in the deck) ───────────────────────────────
SELLER_NOTES = {
    "priorities": "These research notes have no STEP 9B block, so slide 1 uses only figures recorded from the call. Confirm Roy's current open-file count (he said 40 to 60 of his own, and 10… 15 at a time as the five-year goal) before the call. No cost-of-inaction line was said, so that block is empty. Ask what happens to the firm if he keeps declining half the intakes.",
    "diagnosis": "Every card is from the discovery call. Only the caseload goal (10… 15 files at a time) is a target, and it is Roy's own. Ask for a number on billing (hours a month, or time he thinks goes unbilled) and on intakes declined a week; with those, targets can be added.",
    "plan": "No plan inputs were recorded, so each action is built from the products' catalog deliverables and tied to what Roy said. Confirm Elite Coach Plus deliverables with delivery; the group coaching, masterminds and workshops listed are the Elite Coach group deliverables. Roy asked whether summit material fits a firm that is not one specialty — expect that objection and be ready with an example of how coaching works for a general practice.",
    "strategy": "Elite Coach Plus was chosen by the seller in Slack (the revenue table gives Elite Coach at $300K). AI Workforce Pro – Starter: Roy already bought it himself at the workshop and has not set up AI employees yet; the seat count is assumed at 1 — confirm it and that billing runs through SMB Team. The transcript shows the price as '$3.50' and it was read as $350.",
    "investment": "Revenue $300K was confirmed by the seller. Only one product is bundle-eligible, so both are at stand-alone price with no bundle savings. There are no paid ads in this package, so no ad spend or return panels. Roy's follow-up is Wednesday Nov 11, 11:30 AM Eastern, and he is weighing a merger and a first associate hire at the same time.",
}

# ── Slide 5 — Your Investment ─────────────────────────────────────
PRODUCT_LINES = {
    "Elite Coach Plus": "Group coaching · Masterminds · Quarterly workshops · Annual workshop",
    "AI Workforce Pro – Starter": "AI Workforce Pro access · Weekly AI Implementation Session",
}

AD_SPEND_WHY = None

CLOSING_QUOTE = ("Me to be handling maybe 10… 15 files at a time, and consulting the other attorneys in my firm with their cases.",
                 "Roy Gordon (client), 00:11:45")

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

# Slide order. The staircase slide is optional (STAIRCASE in the FILL).
SLIDE_ORDER = (["priorities"] + (["staircase"] if STAIRCASE else []) +
               ["diagnosis", "plan", "strategy"] + (["rollout"] if SHOW_ROLLOUT else []) +
               ["investment"])
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


SLIDE_TITLES = {"priorities": "Your Priorities, In Your Words", "staircase": "Lawyer Legacy Staircase",
                "diagnosis": "The Diagnosis", "plan": "The Plan", "strategy": "The Recommended Strategy",
                "rollout": "Rollout Plan", "investment": "Your Investment"}


def seller_prep_path():
    base = re.sub(r"_Proposal\.pptx$|\.pptx$", "", OUTPUT_PATH)
    return base + "_Seller_Prep.txt"


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
    check_quotes(problems)
    if problems:
        raise SystemExit("Deck not built — fix the values above the LAYOUT ENGINE line:\n  - " + "\n  - ".join(problems))


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
        add_text(slide, p["name"], x + 0.18, ry + 0.06, name_w, 0.30, 10.5, NAVY, bold=True,
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


def build_totals_block(slide, inv, x, w, top, bottom):
    """Navy block: the monthly investment beside the year-one total."""
    h = bottom - top
    add_rect(slide, x, top, w, h, fill=NAVY)
    add_rect(slide, x, top, 0.05, h, fill=LIME_GREEN)
    list_total = inv.get("list_total") or inv["monthly_total"]
    cells = [("MONTHLY INVESTMENT", f"{usd(inv['monthly_total'])}/mo",
              (f"List {usd(list_total)}/mo · save {usd(inv['total_savings'])}/mo"
               if inv.get("total_savings") else "List price (no bundle)")),
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
    # Without a closing quote the content runs down to the footer.
    bottom = 4.74 if CLOSING_QUOTE else 5.12
    if ad:
        left_w = 5.00
        build_buys_card(slide, inv, 0.30, left_w, 1.04, bottom - 1.08)
        build_totals_block(slide, inv, 0.30, left_w, bottom - 0.98, bottom)
        rx, rw = 5.50, 4.20
        if ret:
            build_ad_spend_card(slide, ad, rx, rw, 1.04, 2.56)
            build_return_card(slide, ret, rx, rw, 2.64, bottom)
        else:
            build_ad_spend_card(slide, ad, rx, rw, 1.04, bottom)
    else:
        build_buys_card(slide, inv, 0.30, 9.40, 1.04, bottom - 1.08)
        build_totals_block(slide, inv, 0.30, 9.40, bottom - 0.98, bottom)

    # Closing line — the owner's outcome, in their own verbatim words. Left
    # off when there's no verbatim line that isn't already on the deck.
    if CLOSING_QUOTE:
        add_rect(slide, 0, 4.84, 10, 0.43, fill=rgb("002A41"))
        add_rect(slide, 0, 4.84, 10, 0.02, fill=LIME_GREEN)
        add_text(slide, _quote(CLOSING_QUOTE[0]), 0.70, 4.86, 8.60, 0.40, 9.5, NAVY_TEXT_SOFT,
                 align=PP_ALIGN.CENTER, max_lines=1, min_size=7.5, anchor=MSO_ANCHOR.MIDDLE,
                 cap_chars=170, cap_label="CLOSING_QUOTE")
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
if STAIRCASE:
    build_staircase(prs)
build_diagnosis(prs)
build_plan(prs)
build_strategy(prs)
if SHOW_ROLLOUT:
    build_rollout(prs)
build_investment(prs)
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
