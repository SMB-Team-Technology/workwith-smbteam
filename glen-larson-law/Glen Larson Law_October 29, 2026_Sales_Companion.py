"""
Sales Companion PDF Template — SMB Team
========================================
This template generates the 2-page internal Sales Companion PDF for the sales rep.
It uses reportlab. Do not modify the layout, colors, fonts, styles, or structure.
Only replace the # FILL: placeholders with audit-specific content.

IMPORTANT: The final PDF must be exactly 2 pages. If content overflows to a third
page, shorten bullet text — do not remove sections.

All bullet text must be scannable: one idea per bullet, 8th-grade reading level.
Each "What it does for her/him:" bullet states the transformation, not the deliverable.
Each scoping rationale bullet states one fact with one conclusion.

Output filename: [FirmName]_[Date]_Sales_Companion.pdf
  - FirmName: spaces replaced with underscores
  - Date: MMDDYYYY format
  - Save to the root of the project folder (same location as the Growth Audit HTML)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Fonts — SMB Team brand font is Poppins. Embedded so it renders the
# same regardless of what's installed on the machine opening the PDF. ──
_FONT_DIR = "Design Files/fonts"
pdfmetrics.registerFont(TTFont("Poppins", os.path.join(_FONT_DIR, "Poppins-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Bold", os.path.join(_FONT_DIR, "Poppins-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Italic", os.path.join(_FONT_DIR, "Poppins-Italic.ttf")))
pdfmetrics.registerFontFamily(
    "Poppins", normal="Poppins", bold="Poppins-Bold",
    italic="Poppins-Italic", boldItalic="Poppins-Bold",
)

# ── Colors — SMB Team brand colors (Deep Wood Blue, Ocean Blue) plus the
# existing semantic grays/reds/savings-green, which stay as they were. ──
DARK_NAVY = HexColor("#003A59")     # Deep Wood Blue — brand primary
SECTION_BLUE = HexColor("#0091C9")  # Ocean Blue — brand accent, section headers
ACCENT_GREEN = HexColor("#3B6D11")  # savings/positive-outcome green — matches the audit report
MEDIUM_GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#888888")
RULE_GRAY = HexColor("#CCCCCC")
QUOTE_BG = HexColor("#F5F7F0")
WHITE = HexColor("#FFFFFF")
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "glen-larson-law/Glen Larson Law_October 29, 2026_Sales_Companion.pdf"


def add_page_elements(canvas, doc):
    """Draws red warning header and confidential footer on every page. DO NOT MODIFY."""
    canvas.saveState()
    width, height = letter
    canvas.setFont("Poppins-Bold", 10)
    canvas.setFillColor(RED_WARNING)
    canvas.drawCentredString(width / 2, height - 0.38 * inch,
                             "FOR INTERNAL USE ONLY; DO NOT SHARE.")
    canvas.setStrokeColor(RED_WARNING)
    canvas.setLineWidth(0.5)
    canvas.line(0.6 * inch, height - 0.44 * inch,
                width - 0.6 * inch, height - 0.44 * inch)
    canvas.setFont("Poppins", 7)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawCentredString(width / 2, 0.28 * inch,
                             "SMB Team  |  Confidential  |  Internal Document")
    canvas.restoreState()


doc = SimpleDocTemplate(
    OUTPUT_PATH, pagesize=letter,
    topMargin=0.72 * inch, bottomMargin=0.42 * inch,
    leftMargin=0.6 * inch, rightMargin=0.6 * inch,
)

# ── Styles — DO NOT MODIFY ──
S = {}
S["title"] = ParagraphStyle(
    "title", fontName="Poppins-Bold", fontSize=16, leading=20,
    textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle(
    "subtitle", fontName="Poppins", fontSize=9.5, leading=13,
    textColor=LIGHT_GRAY, spaceAfter=3)
S["section"] = ParagraphStyle(
    "section", fontName="Poppins-Bold", fontSize=11, leading=15,
    textColor=SECTION_BLUE, spaceBefore=6, spaceAfter=2)
S["subsection"] = ParagraphStyle(
    "subsection", fontName="Poppins-Bold", fontSize=10, leading=13,
    textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle(
    "bullet", fontName="Poppins", fontSize=9.5, leading=13,
    textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0,
    spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle(
    "bullet_dark", fontName="Poppins", fontSize=9.5, leading=13,
    textColor=DARK_NAVY, leftIndent=12, bulletIndent=0,
    spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle(
    "quote", fontName="Poppins-Italic", fontSize=9.5, leading=13,
    textColor=DARK_NAVY, leftIndent=6, rightIndent=6,
    spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle(
    "snap_label", fontName="Poppins-Bold", fontSize=8.5, leading=11,
    textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle(
    "snap_value", fontName="Poppins", fontSize=9.5, leading=12,
    textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle(
    "objection_q", fontName="Poppins-Bold", fontSize=9.5, leading=13,
    textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle(
    "objection_a", fontName="Poppins", fontSize=9.5, leading=13,
    textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle(
    "price_main", fontName="Poppins-Bold", fontSize=9.5, leading=13,
    textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle(
    "price_detail", fontName="Poppins", fontSize=8.5, leading=12,
    textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle(
    "savings", fontName="Poppins-Bold", fontSize=9.5, leading=13,
    textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle(
    "disclaimer", fontName="Poppins-Italic", fontSize=8.5, leading=11,
    textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


# ── Helpers — DO NOT MODIFY ──
def b(text):
    """Gray bullet for scoping rationale, obstacles, and technical details."""
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    """Dark bullet for transformation statements and what she/he wants."""
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY,
                       spaceBefore=3, spaceAfter=3)

def quote_block(text):
    """Quote block with subtle background for prospect's own words."""
    p = Paragraph(f'"{text}"', S["quote"])
    t = Table([[p]], colWidths=[6.5 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), QUOTE_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t



# ══════════════════════════════════════════════════════════
# PAGE 1
# ══════════════════════════════════════════════════════════
story = []

story.append(Paragraph("Glen Larson Law", S["title"]))
story.append(Paragraph("Sales Companion  |  October 29, 2026  |  Rep: Randy Gold", S["subtitle"]))
story.append(thin_rule())

# ── Prospect Snapshot ──
story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Glen Larson", S["snap_value"]),
     Paragraph("~$3.0-3.3M (2026 pace)", S["snap_value"]),
     Paragraph("15", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("Not stated (strong)", S["snap_value"]),
     Paragraph("Austin, TX (+ Dallas, El Paso)", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.0*inch, 1.25*inch, 0.6*inch, 0.7*inch, 1.05*inch, 1.4*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 4))

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: TIME FREEDOM", S["section"]))
story.append(Paragraph("A firm that runs on its managers and systems so he has time and a clear role.", S["subsection"]))

story.append(quote_block("I take 10% more time than 5% less money all day long. I'm 51 years old, I need time, freedom."))
story.append(Spacer(1, 1))
story.append(quote_block("I need clarity on what my role is."))
story.append(Spacer(1, 1))
story.append(quote_block("That's what's keeping me up at night is the operations."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Time and freedom.</b> A fully offline two-week vacation by June or July."))
story.append(bd("<b>Role clarity.</b> To stop wearing so many hats."))
story.append(bd("<b>Managers who run ops.</b> Trained leaders who optimize the firm."))
story.append(bd("<b>A 90-day plan.</b> Something in place by the end of the year."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>He is the bottleneck.</b> He authorizes every case; there is no closer."))
story.append(b("<b>Untrained managers.</b> No one owns operational optimization."))
story.append(b("<b>Disconnected tools.</b> RingCentral and Salesforce do not talk."))
story.append(b("<b>Boom-and-bust cycles.</b> He wants a caterpillar, not a roller coaster."))
story.append(b("<b>Key-person risk.</b> Cash transfers break if he leaves without systems."))

story.append(thin_rule())

# ── Why This Legal AI Workforce Package (replaces Marketing section: no marketing recommended) ──
story.append(Paragraph("Why This Legal AI Workforce Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Automates the reports and case scrubs he asked for, so gaps are caught early."))
story.append(bd("A Fractional CTO leads the AI rollout, so he does not have to."))
story.append(bd("Frees manager and owner time for work only people can do."))

story.append(Paragraph("<b>Fractional CTO Level 1 + AI Workforce Pro (15 seats)  |  $6,094/mo bundled</b>", S["subsection"]))
story.append(b("FCTO Level 1 ($3,297) fits $400K+ revenue; AI Workforce Pro is $1,597 for 5 users + 10 x $120."))
story.append(b("He only uses AI for demand drafting today; he wants automated reports and an omission scrub."))
story.append(b("He is not open to AI signing cases, so keep AI to reports, scrubs, drafting and message-taking."))
story.append(b("Rep check: confirm LAW delivery has launched; AI Workforce Pro is a yearly contract."))

story.append(thin_rule())

# ── Why This Operations Package (replaces Coaching section) ──
story.append(Paragraph("Why This Operations Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Moves case authorization and daily decisions from him to trained managers."))
story.append(bd("Gives him the coach-style weekly rhythm he asked for."))
story.append(bd("Makes a two-week offline break realistic."))

story.append(Paragraph("<b>FCOO Director  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("Call was about ops; he asked about a fractional COO and wants a regular check-in with a coach."))
story.append(b("Seller set FCOO Director in Slack; Partner is no longer offered."))
story.append(b("$3M+ revenue and 15 staff qualify; includes Elite Coach group deliverables."))
story.append(b("He has used a fractional CMO and CFO before, but never a COO."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Glen Larson Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Marketing / Ad Spend (replaces Ad Spend section) ──
story.append(Paragraph("Why No Marketing or Ad Spend", S["section"]))

story.append(Paragraph("<b>What this protects:</b>", S["subsection"]))
story.append(bd("Keeps the proposal on what he actually asked for: operations and AI."))
story.append(bd("Avoids selling a marketing gap he told us he does not have."))

story.append(Paragraph("<b>Why it was left out:</b>", S["subsection"]))
story.append(b("<b>His words:</b> He does not want marketing right now and feels confident in his systems."))
story.append(b("<b>Active vendors:</b> An SEO company and a marketing company are already engaged."))
story.append(b("<b>Capacity limit:</b> Case count is at max for the current teams, so more leads do not help."))
story.append(b("<b>Possible seed:</b> The fractional CMO retired in September, so vendor oversight is vacant."))
story.append(Paragraph("<i>No ad spend or ROI projection applies to this proposal.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph("&quot;I don't need a cheerleader.&quot;", S["objection_q"]))
story.append(Paragraph("Agree. He said it at 00:36:25. Frame the FCOO as an operator who builds structure, with a coach-style check-in rhythm he asked for.", S["objection_a"]))

story.append(Paragraph("&quot;We're not, like, signing cases with robots.&quot;", S["objection_q"]))
story.append(Paragraph("Agree. Humans keep signing authority. AI handles reports, case scrubs, drafting and message-taking, which he accepted on the call.", S["objection_a"]))

story.append(Paragraph('"What about the price? I want a plan within 90 days."', S["objection_q"]))
story.append(Paragraph("$11,091/mo total, about 4.4% of ~$250K monthly revenue. He asked for a 90-day plan, and no price was quoted on the call.", S["objection_a"]))

story.append(Paragraph('"Why not just hire a COO or another manager?"', S["objection_q"]))
story.append(Paragraph("He tried all year to hire the right senior person. A fractional COO starts now and trains the managers he already has.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>FCOO Director</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("Fractional COO plus Elite Coach group deliverables.", S["price_detail"]),
     Paragraph("<strike>$5,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Legal AI Workforce (FCTO Level 1 + AI Workforce Pro, 15 seats)</b>", S["price_main"]),
     Paragraph("$6,094/mo", S["price_main"])],
    [Paragraph("AI rollout lead plus AI Workforce Pro for 15 users. No stand-alone price.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
]
pt = Table(price_data, colWidths=[4.5 * inch, 1.7 * inch])
pt.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 4),
    ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ("TOPPADDING", (0,0), (-1,-1), 2),
    ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
    ("LINEBELOW", (0,3), (-1,3), 0.5, RULE_GRAY),
]))
story.append(pt)
story.append(Paragraph(
    "Total: $11,091/mo  |  Save $800/mo by bundling  |  ~4.4% of revenue (under 35% cap)",
    S["savings"]))

# ── Build ──
doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
