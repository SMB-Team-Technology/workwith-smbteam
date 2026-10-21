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
_FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
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

OUTPUT_PATH = "the-moloney/TheMoloneyLawFirm_October292026_Sales_Companion.pdf"


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

story.append(Paragraph("The Moloney Law Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  October 29, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Bradley Moloney", S["snap_value"]),
     Paragraph("~$250K", S["snap_value"]),
     Paragraph("1 (solo)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Denver, CO", S["snap_value"])],
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

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: FREEDOM", S["section"]))
story.append(Paragraph("Brad wants a firm with no staff, run by systems he builds, so the process itself is the asset.", S["subsection"]))

story.append(quote_block("I wanted to set up the firm such that it would just be me. So everything else could be automated."))
story.append(Spacer(1, 1))
story.append(quote_block("…the thing that I'm building would be the actual process, the actual architecture behind the business, not the practice of law…"))
story.append(Spacer(1, 1))
story.append(quote_block("I love working on the business more than I like working in the business."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Automation first.</b> A daily discovery routine and new-lead follow-up that run without him."))
story.append(bd("<b>No staff, ever.</b> He has managed people since age 19 and is done with that."))
story.append(bd("<b>A system worth owning.</b> The architecture behind the firm is the product, not the practice."))
story.append(bd("<b>Room for more business.</b> Goal is about $350K next year, after the automation is in."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>He is the whole firm.</b> Only one doing intake, court, and filings (00:45:39)."))
story.append(b("<b>Tool sprawl.</b> Clio, Lawmatics, Dialpad, Make.com overlap. Software is his biggest expense."))
story.append(b("<b>He likes building it.</b> On a CTO: \"I enjoy it too much\" (00:45:17)."))
story.append(b("<b>Not lead-starved.</b> \"Not in a stage of hurting\" (00:06:49), so marketing is not the pitch."))
story.append(b("<b>Budget unknown.</b> No pricing was quoted on the call. Revenue is about $250K."))

story.append(thin_rule())

# ── Why This AI Package ──
story.append(Paragraph("Why This Legal AI Workforce Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives him a managed AI workspace for the daily admin he wants off his desk."))
story.append(bd("A weekly session turns his wish list into working routines, one at a time."))
story.append(bd("Builds toward a firm whose process, not his hours, holds the value."))

story.append(Paragraph("<b>AI Workforce Pro – Starter (1 seat)  |  $350/mo bundled</b>", S["subsection"]))
story.append(b("The call was AI-led. Jacob said AI Workforce Pro makes the most sense (00:44:49)."))
story.append(b("Starter (1-4 users): 1 seat x $350/mo. Month-to-month. No stand-alone price."))
story.append(b("Seller override (Slack, 10/21): AI Workforce Pro only. No marketing, coaching, or fCTO."))
story.append(b("Confirm LAW delivery has launched and has capacity before sending."))

story.append(thin_rule())

# ── Why No Fractional CTO ──
story.append(Paragraph("Why No Fractional CTO", S["section"]))

story.append(Paragraph("<b>Why it is left out:</b>", S["subsection"]))
story.append(b("<b>Seller excluded it.</b> The 10/21 override limits the proposal to AI Workforce Pro."))
story.append(b("<b>He wants to build it himself.</b> Jacob called a CTO \"possibly\" a fit."))
story.append(b("<b>Revenue floor.</b> Fractional CTO Level 1 needs $400K+. He is at about $250K."))
story.append(b("Revisit if revenue passes $400K or the build load outgrows his time."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("The Moloney Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Marketing Or Ad Spend ──
story.append(Paragraph("Why No Marketing Or Ad Spend", S["section"]))

story.append(Paragraph("<b>What this does for him:</b>", S["subsection"]))
story.append(bd("Frees his capacity before any new leads land on a one-person desk."))
story.append(bd("Keeps the first proposal small, matching what he asked about."))

story.append(Paragraph("<b>Why it is left out:</b>", S["subsection"]))
story.append(b("<b>SEO is covered.</b> His vendor contract runs to about April 2027 (00:05:06). He will not renew."))
story.append(b("<b>Lead flow is fine.</b> Referrals and organic Google bring most work (00:06:25)."))
story.append(b("<b>He already runs small ads.</b> Limited Microsoft ads, self-managed. Budget not stated."))
story.append(b("No ad spend, ROI projection, or ad-range math applies. Total spend is $350/mo, 1.7% of monthly revenue."))

story.append(Paragraph("<b>Free wins to lead with now:</b>", S["subsection"]))
story.append(bd("Export SEO rankings and reports before the vendor contract ends."))
story.append(bd("Start a review-request routine. Review counts are unconfirmed, so verify live first."))
story.append(Paragraph("<i>No competitor ad, LSA, or 3-pack data was observed. PageSpeed was not obtained. Do not cite any.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I would rather build the automations myself."', S["objection_q"]))
story.append(Paragraph("He already uses Claude, ChatGPT, and Make.com, yet discovery and lead follow-up are still manual. Pre-built Law Firm AI Skills and a weekly session give him structure, not a blank page.", S["objection_a"]))

story.append(Paragraph('"I am not short on leads, so why change anything?"', S["objection_q"]))
story.append(Paragraph("Agreed. Nothing here adds leads. It frees his time first, so more business later adds revenue instead of hours. He said he wants automation \"so that I can make room for more business\" (00:07:00).", S["objection_a"]))

story.append(Paragraph('"I already have too many tools and subscriptions."', S["objection_q"]))
story.append(Paragraph("Software is his biggest expense. Pitch this as one workspace to absorb work, not another tool to manage. It is $350/mo and month-to-month, so he can test it with low risk.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>AI Workforce Pro – Starter (1 seat)</b>", S["price_main"]),
     Paragraph("$350/mo", S["price_main"])],
    [Paragraph("1 seat x $350/user/mo. Month-to-month.", S["price_detail"]),
     Paragraph("no stand-alone price", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("None", S["price_main"])],
    [Paragraph("Marketing is not part of this proposal.", S["price_detail"]),
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
    "Total: $350/mo  |  No bundle savings (no stand-alone price)  |  1.7% of monthly revenue (under 35% cap)",
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
