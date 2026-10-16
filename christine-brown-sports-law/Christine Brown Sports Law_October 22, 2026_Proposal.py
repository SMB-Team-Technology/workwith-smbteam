"""
Audit PowerPoint Template — SMB Team
======================================
Generates a 3-slide proposal PPTX from the Growth, Profit, and Freedom Roadmap.
Uses python-pptx. Do not modify the layout engine below the FILL section.
Only replace the # FILL: placeholders with audit-specific content.

Slide 1 — Where [Firm] Stands Today         (assessment overview)
Slide 2 — Your Growth Plan: 3 Priorities    (action plan)
Slide 3 — Your Investment & What's Next     (pricing + what you told us)

Output: [friendly-name]/[FirmName]_[Date]_Proposal.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE, MSO_ANCHOR
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
FIRM_NAME      = "Christine Brown Sports Law"
SALES_REP      = "Jonathan Farace"
OUTPUT_PATH    = "christine-brown-sports-law/Christine Brown Sports Law_October 22, 2026_Proposal.pptx"

# Optional images
WEBSITE_SCREENSHOT_PATH = None   # Set to a local PNG path to show a screenshot; None = skip entirely

# ── Slide 1 ──────────────────────────────────────────────────────
URGENCY_SCORE = "4"

PILLARS = [
    ("AMBER", "AMBER", "Content-led visibility"),
    ("AMBER", "AMBER", "Form linked off-page"),
    ("AMBER", "AMBER", "Roles clearly defined"),
    ("AMBER", "AMBER", "Baseline not visible"),
]
PILLAR_NAMES = ["Lead Generation", "Intake", "Team", "Profit Plan"]

FINDINGS = [
    ("neg", "Phone visitors likely leave before the site loads: mobile performance is 28/100."),
    ("neg", "No clear consultation button, and the intake form is linked off the homepage."),
    ("neg", "Growth keeps landing on Christine until AI workflows and an operating rhythm carry the repeatable work."),
    ("pos", "About 30 years of experience, a defined team, and active press coverage are strong foundations."),
]

# Review counts were not confirmed for the firm or any competitor — no figures are shown.
COMPETITORS = [
    ("Duffy Law, LLC",           "Not verified", "New Haven · Title IX since 2015"),
    ("Barry, Taylor & Levesque", "Not verified", "Hartford · NCAA infractions pages"),
    ("Athlete Defender",         "Not verified", "25+ yrs · many keyword pages"),
]
CLIENT_REVIEWS      = "Not verified"
CLIENT_REVIEWS_NOTE = "← You are here"

STAGE_TEXT = "Stage 4: Small Business Manager  →  Goal: Stage 6, Law Firm Owner"

# ── Slide 2 ──────────────────────────────────────────────────────
SLIDE_2_TITLE = "Your Growth Plan: 3 Priorities for a Firm That Scales"

SMB_MODEL_DESC = (
    "Lead generation, intake, a self-managing team, and a profit plan all have to work together. "
    "When all four work, Christine can step back while the firm keeps growing."
)

GOAL_HEADLINE = "A firm that scales beyond you"
GOAL_DBM      = "Step away and trust the firm runs"

PRIORITIES = [
    (
        "Put AI to Work", "for Your Team", "0091C9",
        [
            "Kick off with your Fractional CTO and map repeat work",
            "Deploy the first AI skills for drafting and research",
            "Roll out AI Workforce Pro to all 12 seats",
            "Build one custom automation each month",
            "Free attorney hours for athletes, coaches, and teams",
        ],
    ),
    (
        "Fix Intake &", "Stop Losing Cases", "69CD2B",
        [
            "Add a clear consultation button above the fold",
            "Embed the intake form right on the homepage",
            "Speed up the mobile site from 28/100",
            "Set a response and follow-up standard for inquiries",
            "Turn more of the visitors you earn into clients",
        ],
    ),
    (
        "Install Team &", "Profit Systems", "003A59",
        [
            "Set a weekly operating rhythm with your FCOO",
            "Give every role clear goals and accountability",
            "Build a monthly profit snapshot by matter type",
            "Let decisions happen without waiting on you",
            "Join weekly coaching and law-firm masterminds",
        ],
    ),
]

# ── Slide 3 ──────────────────────────────────────────────────────
PACKAGES = [
    (
        "LEGAL AI WORKFORCE — FCTO L1 + AI WORKFORCE PRO",
        "$5,734", "FCTO $3,797/mo",
        "Monthly fCTO session · AI skills · automations · 12 seats",
        "0091C9",
    ),
    (
        "FCOO ADVISOR",
        "$3,297", "$3,797/mo",
        "Ops leadership · Weekly group coaching · Workshops",
        "003A59",
    ),
]

BUNDLE_TOTAL   = "$9,031 / mo"
BUNDLE_SAVINGS = "Save $1,000/mo by bundling"

# No marketing/ads package is part of this recommendation (seller override), so no ad spend note
# and no ROI-on-ad-spend card. The ROI variables below are unused.
AD_SPEND_NOTE = None

AVG_CASE_VALUE     = "$X,XXX"
CONSERVATIVE_LABEL = "Conservative  (X cases/mo):"
CONSERVATIVE_RESULT = "$XX,XXX revenue · X.X× ROAS"
AGGRESSIVE_LABEL   = "Aggressive  (X cases/mo):"
AGGRESSIVE_RESULT  = "$XX,XXX revenue · X.X× ROAS"

# No discovery call transcript exists, so section 11 Block 5 is the "What We Found" fallback
# (research findings from Sections 7–8, not client statements).
TOLD_US_TITLE = "WHAT WE FOUND"

WHAT_YOU_TOLD_US = [
    ("Repetitive work", "Monthly AI skills, rolled out to all 12 users"),
    ("Escalations", "FCOO builds rhythm + role-level accountability"),
    ("Follow-up gaps", "Defined inquiry process, built as an automation"),
]

CLOSING_QUOTE = (
    '"The credentials, the team, and the reputation are already in place — what is missing is '
    'the system that lets the firm run on them instead of on Christine alone."'
)

# ═══════════════════════════════════════════════════════════════════
# LAYOUT ENGINE — DO NOT MODIFY BELOW THIS LINE
# ═══════════════════════════════════════════════════════════════════

# ── Color palette ─────────────────────────────────────────────────
def rgb(h): return RGBColor(int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))

# SMB Team brand colors (see brand book): Deep Wood Blue, Ocean Blue, Lime Green.
# These three anchor the palette and are unchanged from the previous design —
# what changed in this pass is how they're applied (thin accents/pills instead
# of large solid fills) plus several supporting tones below, retuned to softer,
# lower-saturation values matched from the reference redesign.
NAVY        = rgb("003A59")   # Deep Wood Blue — primary brand color
OCEAN_BLUE  = rgb("0091C9")   # brand accent — large numbers, decorative accents
LIME_GREEN  = rgb("69CD2B")   # brand accent — small "pop" text/labels on navy
WHITE       = rgb("FFFFFF")

BG_WASH       = rgb("F4F7F9")   # full-bleed slide background
URGENCY_CARD  = rgb("0B4C6E")   # header-docked urgency widget
URGENCY_SUB   = rgb("9CC0D6")   # urgency widget's "Score out of 10" subtitle

RED         = rgb("B32D2D")
AMBER       = rgb("B5770B")
GREEN       = rgb("3F8F1A")
RED_PILL_BG   = rgb("FBEEEE")
AMBER_PILL_BG = rgb("FDF4E3")
GREEN_PILL_BG = rgb("ECF7E4")

DARK_TEXT   = rgb("1B2A38")   # near-black body/label text on white cards
BODY_TEXT   = rgb("4A5C6B")   # neutral gray-blue for card copy (findings, ad spend note, timeline actions)
SLATE       = rgb("7C8D9B")   # lighter captions (competitor detail, retail price, services line)
LIGHT_BLUE  = rgb("B8CDDD")   # SMB Team Model description text (on navy)
FOOTER_TEXT = rgb("8FB2C6")

ROI_BG      = rgb("F0FAF4")
ROI_GREEN   = rgb("0B6B4A")
ROI_HILIGHT = rgb("E2F3E9")

BUNDLE_SAVINGS_TEXT = rgb("A9D68C")   # lighter green — reads as "money saved"
GOAL_TEXT_DARK      = rgb("143306")   # goal headline, on Lime Green card
GOAL_TEXT_DARKER    = rgb("1F470C")   # goal DBM line, on Lime Green card

STATUS_COLOR    = {"RED": RED, "AMBER": AMBER, "GREEN": GREEN}
STATUS_PILL_BG  = {"RED": RED_PILL_BG, "AMBER": AMBER_PILL_BG, "GREEN": GREEN_PILL_BG}
# Priority/package accent colors cycle through the brand palette. Lime Green
# is light, so anything filled with it uses a dark green text instead of
# WHITE/navy — see ACCENT_TEXT_COLOR below.
PRIORITY_LIGHT = {
    "0091C9": rgb("ECF5FA"),   # light Ocean Blue tint
    "69CD2B": rgb("ECF7E4"),   # light Lime Green tint
    "003A59": rgb("EEF2F5"),   # light Deep Wood Blue tint
}
# Header text color to use for each accent fill — defaults to WHITE elsewhere.
ACCENT_TEXT_COLOR = {"69CD2B": GOAL_TEXT_DARK}

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


def add_pill(slide, text, left, top, w, h, bg, text_color, size=6.5, bold=True):
    """A small rounded-rectangle chip, optionally with centered text — used
    for status badges (RED/AMBER/GREEN), the header's urgency-score widget,
    and (with text=None) as a plain colored background for a vector icon
    drawn on top by the caller."""
    from pptx.util import Emu as E
    shape = slide.shapes.add_shape(5, E(int(left*914400)), E(int(top*914400)),
                                   E(int(w*914400)), E(int(h*914400)))
    shape.line.fill.background()
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg
    if text:
        add_text(slide, text, left, top, w, h, size, text_color, bold=bold, align=PP_ALIGN.CENTER)
    return shape


def add_check(slide, left, top, size, color, weight_pt=1.75):
    """A vector checkmark (two line segments) — used instead of a ✓ glyph so
    it renders identically everywhere, regardless of what fonts a given
    viewer (PowerPoint, Keynote, Google Slides, ...) has or substitutes."""
    from pptx.enum.shapes import MSO_CONNECTOR
    from pptx.util import Emu as E, Pt as P
    points = [(0.22, 0.55), (0.42, 0.74), (0.80, 0.26)]
    abs_pts = [(left + px*size, top + py*size) for px, py in points]
    for (x1, y1), (x2, y2) in zip(abs_pts, abs_pts[1:]):
        conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                          E(int(x1*914400)), E(int(y1*914400)),
                                          E(int(x2*914400)), E(int(y2*914400)))
        conn.line.color.rgb = color
        conn.line.width = P(weight_pt)


def add_x_mark(slide, left, top, size, color, weight_pt=1.75, inset=0.24):
    """A vector X (two crossed line segments) — same rationale as add_check."""
    from pptx.enum.shapes import MSO_CONNECTOR
    from pptx.util import Emu as E, Pt as P
    a, b = inset*size, (1-inset)*size
    for (x1, y1), (x2, y2) in [((left+a, top+a), (left+b, top+b)),
                                ((left+a, top+b), (left+b, top+a))]:
        conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                          E(int(x1*914400)), E(int(y1*914400)),
                                          E(int(x2*914400)), E(int(y2*914400)))
        conn.line.color.rgb = color
        conn.line.width = P(weight_pt)


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
    lime stripe at 0.92in."""
    one_line, _ = fit_text(text, w, 0.44, 20, bold=True, max_lines=1, min_size=15)
    if one_line:
        add_text(slide, text, 0.32, 0.42, w, 0.44, one_line, WHITE, bold=True,
                 fit=False, anchor=MSO_ANCHOR.MIDDLE)
    else:
        add_text(slide, text, 0.32, 0.30, w, 0.60, 15, WHITE, bold=True,
                 max_lines=2, min_size=12, anchor=MSO_ANCHOR.BOTTOM,
                 cap_label="slide title")


def add_header(slide, title, title_w):
    """Background wash, navy header, lime stripe, kicker and title — shared
    by all three slides."""
    add_rect(slide, 0, 0, 10, 5.625, fill=BG_WASH)
    add_rect(slide, 0, 0, 10, 0.92, fill=NAVY)
    add_rect(slide, 0, 0.92, 10, 0.04, fill=LIME_GREEN)
    add_text(slide, f"LAW FIRM GROWTH AUDIT  ·  {FIRM_NAME.upper()}",
             0.32, 0.20, min(title_w, 6.90), 0.18, 7.5, LIME_GREEN, bold=True,
             max_lines=1, cap_label="header kicker")
    add_title(slide, title, title_w)


def add_image_or_placeholder(slide, path, left, top, w, h, label=""):
    from pptx.util import Emu as E
    if path and os.path.isfile(path):
        slide.shapes.add_picture(path, E(int(left*914400)), E(int(top*914400)),
                                 E(int(w*914400)), E(int(h*914400)))
    else:
        ph = add_rect(slide, left, top, w, h, fill=rgb("D1D5DB"))
        if label:
            add_text(slide, label, left+0.05, top+(h/2)-0.12, w-0.1, 0.24,
                     7, SLATE, align=PP_ALIGN.CENTER)


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


# Competitor table columns: name / reviews / detail. Reviews is short
# ("XXX reviews", "Not verified"), so the detail note gets the room it needs.
COMP_COLS = [(5.40, 1.80), (7.20, 0.98), (8.18, 1.46)]


def add_competitor_row(slide, y, name, reviews, detail, name_color, reviews_color,
                       bold, label):
    for (x, w), text, size, color, b, cap_n, part in [
        (COMP_COLS[0], name,    8.5, name_color,    bold,  30, "name"),
        (COMP_COLS[1], reviews, 8,   reviews_color, bold,  30, "reviews"),
        (COMP_COLS[2], detail,  7,   SLATE,         False, 34, "detail"),
    ]:
        add_text(slide, text, x, y, w, 0.39, size, color, bold=b, max_lines=2,
                 anchor=MSO_ANCHOR.MIDDLE, cap_chars=cap_n,
                 cap_label=f"{label} {part}")


def parse_stage_text(text):
    """Split STAGE_TEXT ("Stage 4: Small Business Manager → Goal: Stage 6,
    Law Firm Owner") into (current, goal, current_n, goal_n). Any part that
    can't be found comes back as None."""
    parts = [p.strip() for p in re.split(r"\s*(?:→|->)\s*", str(text), maxsplit=1)]
    current = parts[0] or None
    goal = parts[1] if len(parts) > 1 and parts[1] else None
    def stage_n(s):
        m = re.search(r"Stage\s*(\d)", s or "", re.I)
        n = int(m.group(1)) if m else None
        return n if n and 1 <= n <= 6 else None
    return current, goal, stage_n(current), stage_n(goal)


def build_stage_card(slide, x, y, w, h):
    """Navy "You are here" card: current stage on one line, goal on the next,
    and a 6-step staircase on the right with the current stage filled and
    the goal stage outlined."""
    from pptx.util import Emu as E, Pt as P
    add_rect(slide, x, y, w, h, fill=NAVY)
    add_rect(slide, x, y, 0.04, h, fill=LIME_GREEN)
    current, goal, cur_n, goal_n = parse_stage_text(STAGE_TEXT)
    show_steps = cur_n is not None
    text_w = w - 0.40 - (1.20 if show_steps else 0)

    add_text(slide, "YOU ARE HERE", x+0.20, y+0.10, text_w, 0.18, 7.5, LIME_GREEN,
             bold=True, fit=False)
    if goal:
        add_text(slide, current, x+0.20, y+0.27, text_w, 0.30, 11, WHITE, bold=True,
                 max_lines=1, cap_label="STAGE_TEXT current")
        add_text(slide, f"→  {goal}", x+0.20, y+0.53, text_w, 0.22, 8.5, LIGHT_BLUE,
                 max_lines=1, cap_label="STAGE_TEXT goal")
    else:
        add_text(slide, current or "", x+0.20, y+0.27, text_w, 0.48, 11, WHITE,
                 bold=True, max_lines=2, cap_label="STAGE_TEXT")

    if show_steps:
        bar_w, gap = 0.13, 0.05
        base = y + h - 0.14
        left = x + w - 0.20 - (6 * bar_w + 5 * gap)
        for n in range(1, 7):
            bh = 0.08 + (n - 1) * 0.08
            bx = left + (n - 1) * (bar_w + gap)
            bar = slide.shapes.add_shape(1, E(int(bx*914400)), E(int((base-bh)*914400)),
                                         E(int(bar_w*914400)), E(int(bh*914400)))
            if n <= cur_n:
                bar.fill.solid()
                bar.fill.fore_color.rgb = LIME_GREEN if n == cur_n else rgb("4F8F2A")
                bar.line.fill.background()
            elif n == goal_n:
                bar.fill.solid()
                bar.fill.fore_color.rgb = NAVY
                bar.line.color.rgb = LIME_GREEN
                bar.line.width = P(1)
            else:
                bar.fill.solid()
                bar.fill.fore_color.rgb = URGENCY_CARD
                bar.line.fill.background()


# ── Slide 1: Assessment Overview ──────────────────────────────────

def build_slide1(prs):
    layout = prs.slide_layouts[6]  # blank
    slide = prs.slides.add_slide(layout)

    # Full-bleed background wash + header banner (shared with slides 2 and 3).
    # Title width stops short of the urgency widget at x=7.42.
    add_header(slide, f"Where {FIRM_NAME} Stands Today", 6.90)

    # Urgency widget — docked in the header, not a large block in the content area
    add_rect(slide, 7.42, 0.18, 2.26, 0.56, fill=URGENCY_CARD)
    add_text(slide, URGENCY_SCORE, 7.58, 0.23, 0.42, 0.42, 21, WHITE, bold=True,
             align=PP_ALIGN.CENTER)
    add_text(slide, "COMPETITIVE URGENCY", 8.04, 0.30, 1.55, 0.18, 7, LIME_GREEN, bold=True)
    add_text(slide, "Score out of 10", 8.04, 0.47, 1.55, 0.18, 7, URGENCY_SUB)

    # Pillar cards — a full-width row of 4, each a white card with a colored
    # top accent bar and a pill-shaped status badge
    pillar_xs = [0.30, 2.68, 5.07, 7.45]
    for i, (status, label, detail) in enumerate(PILLARS):
        x = pillar_xs[i]
        sc = STATUS_COLOR[status]
        add_rect(slide, x, 1.10, 2.26, 0.96, fill=WHITE)
        add_rect(slide, x, 1.10, 2.26, 0.04, fill=sc)
        add_text(slide, PILLAR_NAMES[i], x+0.16, 1.26, 1.94, 0.24, 12, DARK_TEXT, bold=True)
        add_pill(slide, label, x+0.16, 1.56, 0.64, 0.19, STATUS_PILL_BG[status], sc, size=7.5)
        add_text(slide, detail, x+0.16, 1.82, 1.94, 0.22, 9.5, SLATE,
                 cap_chars=40, cap_label=f"PILLARS[{i}] detail")

    # Key findings label
    add_text(slide, "KEY FINDINGS", 0.30, 2.20, 4.70, 0.18, 7.5, NAVY, bold=True)

    # Finding cards — white with a colored left accent bar and a rounded icon chip.
    # The check/X are drawn as vector line shapes, not text glyphs, so they
    # render identically in every viewer instead of depending on font coverage.
    finding_ys = [2.48, 3.16, 3.84, 4.52]
    for i, (ftype, text) in enumerate(FINDINGS[:4]):
        y = finding_ys[i]
        dot = RED if ftype == "neg" else GREEN
        add_rect(slide, 0.30, y, 4.72, 0.61, fill=WHITE)
        add_rect(slide, 0.30, y, 0.04, 0.61, fill=dot)
        add_pill(slide, None, 0.47, y+0.21, 0.18, 0.18, dot, WHITE)
        if ftype == "neg":
            add_x_mark(slide, 0.47, y+0.21, 0.18, WHITE)
        else:
            add_check(slide, 0.47, y+0.21, 0.18, WHITE)
        add_text(slide, text, 0.75, y+0.13, 3.77, 0.41, 8.5, BODY_TEXT,
                 cap_chars=115, cap_label=f"FINDINGS[{i}]")

    # Website screenshot — only shown when a local PNG is provided
    if WEBSITE_SCREENSHOT_PATH and os.path.isfile(WEBSITE_SCREENSHOT_PATH):
        from pptx.util import Emu as E
        slide.shapes.add_picture(WEBSITE_SCREENSHOT_PATH,
                                 E(int(5.28*914400)), E(int(1.10*914400)),
                                 E(int(4.42*914400)), E(int(1.00*914400)))

    # "You are here" card
    build_stage_card(slide, 5.28, 2.20, 4.42, 0.82)

    # Competitor table header
    add_text(slide, "COMPETITOR LANDSCAPE", 5.28, 3.14, 4.42, 0.18, 7.5, NAVY, bold=True)

    comp_ys = [3.42, 3.86, 4.30]
    for i, (name, reviews, detail) in enumerate(COMPETITORS[:3]):
        y = comp_ys[i]
        add_rect(slide, 5.28, y, 4.42, 0.39, fill=WHITE)
        add_competitor_row(slide, y, name, reviews, detail, DARK_TEXT, GREEN,
                           bold=False, label=f"COMPETITORS[{i}]")

    # Client row — a "you are here" highlight, not a warning, so it uses the
    # same red accent-bar language as the RED pillar/finding cards rather than
    # a solid warning block (which reads as an error next to the neutral rows above it).
    add_rect(slide, 5.28, 4.74, 4.42, 0.39, fill=RED_PILL_BG)
    add_rect(slide, 5.28, 4.74, 0.04, 0.39, fill=RED)
    add_competitor_row(slide, 4.74, FIRM_NAME, CLIENT_REVIEWS, CLIENT_REVIEWS_NOTE,
                       RED, RED, bold=True, label="CLIENT row")

    add_footer(slide, 1, 3, LOGO_PATH)


# ── Slide 2: Growth Plan ───────────────────────────────────────────

def build_slide2(prs):
    layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(layout)

    # Background wash + header (mirrors slides 1 and 3)
    add_header(slide, SLIDE_2_TITLE, 9.30)

    # Left column — model card and goal card, as two separate cards with a
    # gap between them rather than one continuous box with an inset panel
    add_rect(slide, 0.30, 1.10, 2.42, 2.50, fill=NAVY)
    add_rect(slide, 0.30, 1.10, 2.42, 0.04, fill=LIME_GREEN)
    add_text(slide, "THE SMB TEAM MODEL", 0.50, 1.28, 2.02, 0.16, 7.5, LIME_GREEN, bold=True)
    add_text(slide, SMB_MODEL_DESC, 0.50, 1.56, 2.02, 1.90, 8.5, LIGHT_BLUE)

    add_rect(slide, 0.30, 3.78, 2.42, 1.23, fill=LIME_GREEN)
    add_text(slide, GOAL_HEADLINE, 0.50, 3.96, 2.02, 0.52, 12, GOAL_TEXT_DARK, bold=True)
    add_text(slide, GOAL_DBM, 0.50, 4.50, 2.02, 0.46, 8.5, GOAL_TEXT_DARKER,
             cap_label="GOAL_DBM")

    # 3 priority columns
    priority_xs = [2.92, 5.30, 7.68]
    bullet_ys   = [2.04, 2.65, 3.25, 3.85, 4.46]

    for col_i, (line1, line2, hex_color, bullets) in enumerate(PRIORITIES):
        x = priority_xs[col_i]
        ac = rgb(hex_color)
        light = PRIORITY_LIGHT.get(hex_color, rgb("F8F8FF"))
        header_text = ACCENT_TEXT_COLOR.get(hex_color, WHITE)

        # Header
        add_rect(slide, x, 1.10, 2.26, 0.92, fill=ac)
        add_text(slide, f"0{col_i+1}", x+0.18, 1.20, 0.50, 0.24, 13, header_text, bold=True)
        add_text(slide, line1, x+0.18, 1.44, 2.00, 0.24, 14, header_text, bold=True)
        add_text(slide, line2, x+0.18, 1.68, 2.00, 0.24, 14, header_text, bold=True)

        # Bullet rows
        for row_i, bullet in enumerate(bullets[:5]):
            y = bullet_ys[row_i]
            bg = light if row_i % 2 == 0 else WHITE
            add_rect(slide, x, y, 2.26, 0.56, fill=bg)
            add_rect(slide, x+0.16, y+0.25, 0.07, 0.07, fill=ac)
            add_text(slide, bullet, x+0.33, y+0.02, 1.80, 0.52, 8, DARK_TEXT,
                     anchor=MSO_ANCHOR.MIDDLE,
                     cap_chars=60, cap_label=f"PRIORITIES[{col_i}] bullet {row_i+1}")

    add_footer(slide, 2, 3, LOGO_PATH)


# ── Slide 3: Investment & Next Steps ──────────────────────────────

def build_slide3(prs):
    # Never render an empty panel: with no transcript, Block 5 becomes
    # "What We Found" and this list still gets 3 research-based items.
    if len(WHAT_YOU_TOLD_US) != 3:
        raise SystemExit(
            f"WHAT_YOU_TOLD_US has {len(WHAT_YOU_TOLD_US)} items; Slide 3 needs exactly 3. "
            "With no discovery call transcript, set TOLD_US_TITLE = \"WHAT WE FOUND\" and "
            "copy the 3 research-based rows from section_11 Block 5.")

    layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(layout)

    # Background wash + header (mirrors slides 1 and 2)
    add_header(slide, "Your Investment & What Happens Next", 9.30)

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

        told_us_y = 2.72
        timeline_ys = [2.99, 3.37, 3.75, 4.13]
    else:
        # No ROI card above it — give What You Told Us the full right-column height.
        told_us_y = 1.10
        timeline_ys = [1.46, 2.06, 2.66, 3.26]

    # What You Told Us — alternating light/white rows; the first dot pops in
    # lime green, the rest in ocean blue, so the lead item stands out
    add_text(slide, TOLD_US_TITLE,
             5.00, told_us_y, 4.70, 0.18, 7.5, NAVY, bold=True)
    for i, (milestone, action) in enumerate(WHAT_YOU_TOLD_US[:3]):
        y = timeline_ys[i]
        row_bg = rgb("EEF2F5") if i % 2 == 0 else WHITE
        dot_color = LIME_GREEN if i == 0 else OCEAN_BLUE
        add_rect(slide, 5.00, y, 4.70, 0.29, fill=row_bg)
        add_rect(slide, 5.14, y+0.09, 0.10, 0.10, fill=dot_color)
        add_text(slide, milestone, 5.30, y, 1.25, 0.29, 8, NAVY, bold=True,
                 max_lines=1, anchor=MSO_ANCHOR.MIDDLE,
                 cap_chars=16, cap_label=f"WHAT_YOU_TOLD_US[{i}] label")
        add_text(slide, action, 6.50, y, 3.20, 0.29, 8, BODY_TEXT,
                 max_lines=1, anchor=MSO_ANCHOR.MIDDLE,
                 cap_chars=55, cap_label=f"WHAT_YOU_TOLD_US[{i}] action")

    # Closing quote bar — taller, darker navy, with the same lime accent stripe
    add_rect(slide, 0, 4.66, 10, 0.61, fill=rgb("002A41"))
    add_rect(slide, 0, 4.66, 10, 0.02, fill=LIME_GREEN)
    add_text(slide, CLOSING_QUOTE, 0.70, 4.70, 8.60, 0.54, 9.5, rgb("C2D8E6"),
             align=PP_ALIGN.CENTER, max_lines=2, anchor=MSO_ANCHOR.MIDDLE,
             cap_chars=200, cap_label="CLOSING_QUOTE")

    add_footer(slide, 3, 3, LOGO_PATH)


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

prs = Presentation()
prs.slide_width  = Inches(10)
prs.slide_height = Inches(5.625)

build_slide1(prs)
build_slide2(prs)
build_slide3(prs)

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

print(f"Saved: {OUTPUT_PATH}  ({len(prs.slides)} slides)")
