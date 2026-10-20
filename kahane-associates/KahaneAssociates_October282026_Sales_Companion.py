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
_FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Design Files", "fonts")
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

OUTPUT_PATH = "kahane-associates/KahaneAssociates_October282026_Sales_Companion.pdf"


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

story.append(Paragraph("Kahane &amp; Associates, P.A.", S["title"]))
story.append(Paragraph("Sales Companion  |  October 28, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Robert Kahane (not on call)", S["snap_value"]),
     Paragraph("$15-20M (seller est.)", S["snap_value"]),
     Paragraph("~80", S["snap_value"]),
     Paragraph("4", S["snap_value"]),
     Paragraph("N/A", S["snap_value"]),
     Paragraph("Sunrise, FL (+ Atlanta, Memphis)", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE WITHOUT HEADCOUNT", S["section"]))
story.append(Paragraph("IT wants to handle more work without hiring more people. Owner motive unknown.", S["subsection"]))

story.append(quote_block("Right now, it's not scaling. So, for example, the Notice Mailbox, being that we have a human traffic controller and they're routing things, as that grows, that position, the FTE...would have to grow."))
story.append(Spacer(1, 1))
story.append(quote_block("fees and costs is something that you have maybe one user do almost full-time...a replacement for that user when they take a day off is just almost impossible."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What they want:</b>", S["subsection"]))
story.append(bd("<b>Self-routing notices.</b> No traffic controller role that grows with volume."))
story.append(bd("<b>Reports not tied to one person.</b> Fees-and-costs and billing built automatically."))
story.append(bd("<b>Structure from messy documents.</b> Word reports become importable data."))
story.append(bd("<b>A roadmap, not a genie.</b> A real plan that sets partner expectations."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping them:</b>", S["subsection"]))
story.append(b("<b>Owner not on the call.</b> Robert Kahane decides; management must join (00:03:52)."))
story.append(b("<b>Still exploratory.</b> No dates or numbers set yet (00:23:37)."))
story.append(b("<b>Security rules.</b> AI must have no access to PII in the case system."))
story.append(b("<b>Inflated expectations.</b> IT warns management may expect a genie in a bottle."))
story.append(b("<b>No price seen yet.</b> No level quoted; you promised a custom plan and pricing."))

story.append(thin_rule())

# ── Why Fractional CTO Level 3 ──
story.append(Paragraph("Why Fractional CTO Level 3", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Gives IT a dedicated AI leader so AI stops being a side job."))
story.append(bd("Builds the notice, fees-and-costs and report-import automations they named."))
story.append(bd("Turns a vague partner request into a roadmap leadership can measure."))

story.append(Paragraph("<b>Fractional CTO Level 3  |  $8,997/mo bundled</b>", S["subsection"]))
story.append(b("Level 3 needs $3M+ revenue; the $15-20M seller estimate clears it (unconfirmed)."))
story.append(b("Weekly fCTO sessions, up to 3 custom automations, up to 4 skills each month."))
story.append(b("Foundation Sprint with Readiness Assessment is included at $0 ($19,997 alone)."))
story.append(b("Stand-alone price is $9,997/mo, so bundling saves $1,000/mo."))

story.append(thin_rule())

# ── Why AI Workforce Pro ──
story.append(Paragraph("Why AI Workforce Pro (5 Users)", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Gives five people a managed place to use AI beyond spell-check."))
story.append(bd("A weekly implementation session keeps adoption moving without IT."))
story.append(bd("Lets the firm start small and prove value before adding seats."))

story.append(Paragraph("<b>AI Workforce Pro (5 users)  |  $1,597/mo bundled</b>", S["subsection"]))
story.append(b("Annual contract; 10M usage plus 10M bonus credits (20M total)."))
story.append(b("Priced for five of about 80 employees. No stand-alone price exists; never quote one."))
story.append(b("Say out loud: more users can be added at $120/mo per employee over 5."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Kahane &amp; Associates — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Marketing or Ad Spend ──
story.append(Paragraph("Why No Marketing or Ad Spend", S["section"]))

story.append(Paragraph("<b>What we kept clean:</b>", S["subsection"]))
story.append(bd("This was an AI call. The IT contact declined lead gen: \"that's not, from the IT standpoint, no\" (00:09:00)."))
story.append(bd("New business comes from networking (00:09:05), so only raise marketing if leadership does."))

story.append(Paragraph("<b>Recommended Ad Spend:</b> None.", S["subsection"]))
story.append(b("No marketing package, so there is no ad spend, ROI projection or channel math in this proposal."))
story.append(b("Report Section 6 says \"not observed\" for all ad channels and makes no claim either way."))

story.append(Paragraph("<b>How the recommendation was set:</b>", S["subsection"]))
story.append(b("<b>Seller override:</b> Level 3, revenue $15-20M (low end $15M used), team 80, 5-user AI Workforce Pro added."))
story.append(b("Total spend $10,594/mo is about 0.8% of $15M revenue. The 35% cap would be $437,500/mo."))
story.append(b("<b>Flags:</b> confirm LAW delivery capacity; review counts unconfirmed, verify live before the call."))

story.append(thin_rule())

# ── If They Push Back ──
story.append(Paragraph("If They Push Back", S["section"]))

story.append(Paragraph('"AI is just a genie in the bottle."', S["objection_q"]))
story.append(Paragraph("Agree. IT said the same. The plan starts with their own workflows (Notice Mailbox, fees and costs), and the Readiness Assessment sets realistic scope.", S["objection_a"]))

story.append(Paragraph('"We are still exploratory. Why Level 3?"', S["objection_q"]))
story.append(Paragraph("Level 3 includes the $19,997 Foundation Sprint and weekly sessions, built for a firm that needs a roadmap first. Fallback: Level 2 at $4,997/mo, with the Sprint at $5,003 when packaged.", S["objection_a"]))

story.append(Paragraph('"AI cannot touch our PII."', S["objection_q"]))
story.append(Paragraph("That is a requirement, not an objection. IT said \"AI has no access to PII\". Automations get scoped around data without PII; confirm the approach on the call.", S["objection_a"]))

story.append(Paragraph('"Why only 5 users when we have 80 people?"', S["objection_q"]))
story.append(Paragraph("Start with the people ready to use it, prove value, then add seats at $120/mo per employee over 5.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Fractional CTO Level 3</b>", S["price_main"]),
     Paragraph("$8,997/mo", S["price_main"])],
    [Paragraph("Weekly fCTO leadership, custom automations, Foundation Sprint included.", S["price_detail"]),
     Paragraph("<strike>$9,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>AI Workforce Pro (5 users)</b>", S["price_main"]),
     Paragraph("$1,597/mo", S["price_main"])],
    [Paragraph("Managed AI access for five users with a weekly implementation session.", S["price_detail"]),
     Paragraph("No stand-alone price", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("None", S["price_main"])],
    [Paragraph("No marketing package in this proposal.", S["price_detail"]),
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
    ("LINEBELOW", (0,5), (-1,5), 0.5, RULE_GRAY),
]))
story.append(pt)
story.append(Paragraph(
    "Total: $10,594/mo  |  Save $1,000/mo by bundling  |  0.6%-0.8% of est. revenue (under 35% cap)",
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
