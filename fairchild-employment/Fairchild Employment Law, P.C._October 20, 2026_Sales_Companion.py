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
_FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "Design Files", "fonts")
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

OUTPUT_PATH = "fairchild-employment/Fairchild Employment Law, P.C._October 20, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Fairchild Employment Law, P.C.", S["title"]))
story.append(Paragraph("Sales Companion  |  October 20, 2026  |  Rep: Dan Bryant", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Jillian Fairchild", S["snap_value"]),
     Paragraph("~$500K (2026 pace)", S["snap_value"]),
     Paragraph("4 incl. owner", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("San Diego, CA", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.7*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 4))

story.append(Paragraph("Dominant Buying Motive: PEACE OF MIND", S["section"]))
story.append(Paragraph("She wants a firm that runs without her holding every piece, so she can sleep at night and be present in her free time.", S["subsection"]))

story.append(quote_block("I mean, also just be able to sleep at night, being able to pay all the bills without having to worry about it."))
story.append(Spacer(1, 1))
story.append(quote_block("Be in my free time and be more present and not have to be stressed about it."))
story.append(Spacer(1, 1))
story.append(quote_block("I want&hellip; intake to&hellip; run more smoothly without me having to be involved in every step of the process."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Sleep at night.</b> She wants every bill covered without worry."))
story.append(bd("<b>Fewer hours.</b> She works about 50 a week and wants 40 or less."))
story.append(bd("<b>Intake without her.</b> She wants it smooth with her out of every step."))
story.append(bd("<b>Owner pay back up.</b> She named $195K, and said $225K would be better."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No KPIs.</b> She says she is bad at KPIs and has no time to build them."))
story.append(b("<b>Owner bottleneck.</b> \"I can't do everything.\" Case movement runs through her."))
story.append(b("<b>Weak case prioritization.</b> Not enough urgency, and no clear way to spot good cases."))
story.append(b("<b>Cash flow gap.</b> By her figures, about $41-42K comes in and about $55K goes out."))
story.append(b("<b>Decision clock.</b> She may decide in six months whether to keep the firm (speaker inferred)."))

story.append(thin_rule())

story.append(Paragraph("Why No Marketing Package", S["section"]))
story.append(Paragraph("<b>What we heard:</b>", S["subsection"]))
story.append(bd("She is not calling about marketing. \"I don't have a problem with leads coming in.\""))
story.append(bd("Leads are \"halfway decent\" once she works them, so the gap is operations."))
story.append(b("<b>Existing vendor:</b> iLawyer runs her SEO and Google profile, and she says it does well enough."))
story.append(b("<b>Budget:</b> adding ad spend while cash is tight would not match what she asked for."))
story.append(b("<b>Free wins:</b> GBP category, review habit, and the old MapQuest address are already in the audit."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives her a KPI system for a contingency practice she says she cannot build alone."))
story.append(bd("Puts intake and case movement on a rhythm so the team can run it without her."))
story.append(bd("Moves her toward 40 hours and a firm she does not have to carry home."))

story.append(Paragraph("<b>Elite Coach + FCOO Advisor  |  $5,694/mo bundled</b>", S["subsection"]))
story.append(b("Revenue band $400K-$1M with a small team: this is the table pick for coaching plus ops."))
story.append(b("Seller locked this package on 2026-10-20. Revenue-table default was Elite Coach Plus at $3,200/mo."))
story.append(b("Rep framed the choice as 1:1 fractional COO vs. group coaching, and said coaching fits first."))
story.append(b("Includes weekly group coaching, masterminds, virtual quarterly workshops, and one in-person workshop."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Fairchild Employment Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why No Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Keeps every dollar on the operations help she asked for."))
story.append(bd("Avoids new ad spend while cash flow is the main stress."))

story.append(Paragraph("<b>Budget fit:</b>", S["subsection"]))
story.append(b("<b>Ad spend:</b> none. No marketing or ads package is part of this plan."))
story.append(b("<b>Share of revenue:</b> $5,694/mo is about 13.7% of about $41.7K monthly. Cap is 35%."))
story.append(b("<b>Fallback:</b> Elite Coach Plus at $3,200/mo if the price is the sticking point."))
story.append(b("<b>Stretch risk:</b> she has drawn down savings. Confirm what she can commit before sending."))
story.append(Paragraph("<i>Rep pitch numbers from the call (ROI multiples, guarantees) are not firm facts. Do not repeat them.</i>", S["disclaimer"]))

story.append(thin_rule())

story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I wasn\'t sure my last purchase was the best use of my money."', S["objection_q"]))
story.append(Paragraph("She said this about the earlier AI product (00:02:06). Tie this plan to two gaps she named: no KPIs and intake that needs her. Offer Elite Coach Plus if she wants a smaller first step.", S["objection_a"]))

story.append(Paragraph('"I can\'t take on more cost right now."', S["objection_q"]))
story.append(Paragraph("The plan is about 13.7% of her monthly revenue with no ad spend. She said she would draw on credit \"if I'm planning strategically and what I'm doing makes sense\" (00:38:25).", S["objection_a"]))

story.append(Paragraph('"Do I need both coaching and a COO?"', S["objection_q"]))
story.append(Paragraph("She was weighing exactly these two. Coaching is the first fit (00:27:39). The FCOO Advisor adds hands-on ops help. Bundling saves $1,600/mo versus stand alone.", S["objection_a"]))

story.append(Paragraph('"I already have a marketing company."', S["objection_q"]))
story.append(Paragraph("Agreed, and this plan does not replace iLawyer. The report only flags quick fixes for them: the GBP category and the old MapQuest address.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Elite Coach + FCOO Advisor</b>", S["price_main"]),
     Paragraph("$5,694/mo", S["price_main"])],
    [Paragraph("Group coaching plus a fractional COO for KPIs, intake, and team rhythm.", S["price_detail"]),
     Paragraph("<strike>$7,294</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("None", S["price_main"])],
    [Paragraph("No marketing package in this plan. She already has leads and an SEO vendor.", S["price_detail"]),
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
    "Total: $5,694/mo  |  Save $1,600/mo by bundling  |  13.7% of current monthly revenue (under 35% cap)",
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
