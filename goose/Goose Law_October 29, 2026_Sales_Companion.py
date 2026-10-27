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

OUTPUT_PATH = "goose/Goose Law_October 29, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Goose Law (GOOSELAW Professional Corporation)", S["title"]))
story.append(Paragraph("Sales Companion  |  October 29, 2026  |  Rep: Daniel Lowe", S["subtitle"]))
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
    [Paragraph("Donovan Francis", S["snap_value"]),
     Paragraph("~CAD 1M", S["snap_value"]),
     Paragraph("10", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("10-15%", S["snap_value"]),
     Paragraph("Mississauga, ON", S["snap_value"])],
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
story.append(Paragraph("He wants a firm that grows at least fivefold without depending on one big client or on him closing every lead.", S["subsection"]))

# Use quote_block() for each. Separate with Spacer(1, 1).
story.append(quote_block("I feel confident closing leads, but I shouldn't be the guy. It shouldn't be dependent on me."))
story.append(Spacer(1, 1))
story.append(quote_block("We have one major client, a corporate client, from whom 80% of our revenue comes, right? It's a good position, but it's also very risky."))
story.append(Spacer(1, 1))
story.append(quote_block("at a minimum, I'd want to increase that fivefold."))
story.append(Spacer(1, 2))

# Each bullet: bold lead phrase + one short sentence. One idea per bullet.
story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>A second lead source.</b> Meta alone is fading, and he wants an agency to own the ads."))
story.append(bd("<b>Out of the closer seat.</b> He wants intake that does not depend on him."))
story.append(bd("<b>Less client risk.</b> One corporate client brings most of the revenue."))
story.append(bd("<b>Fivefold growth.</b> His goal is about CAD 5M at a minimum."))

story.append(Spacer(1, 2))

# Each bullet: bold lead phrase + one short sentence. One idea per bullet.
story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>One shrinking funnel.</b> Registrations, consultations and attendance (now near 40%) are all down."))
story.append(b("<b>He is the closer.</b> A second practitioner is in training, but volume is too low to hand off calls."))
story.append(b("<b>Agency skepticism.</b> He fears an agency will not give his account enough attention."))
story.append(b("<b>Cost worry.</b> He has always worried about cost, yet says he will spend more if ROAS is there."))
story.append(b("<b>A bad recent month.</b> Spend outran results, he cannot state a CPL, and past Google leads felt cold."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

# Transformation statements. What the package makes possible. Not deliverables.
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives him a second, managed lead source so growth is not tied to one webinar."))
story.append(bd("Puts one accountable team on the ads, so he is not the one watching them daily."))
story.append(bd("Ties spend to booked consultations and signed files, so spending more is a measured call."))

story.append(Paragraph("<b>Full Service Marketing Essentials  |  $3,797/mo (stand-alone price, no bundle discount)</b>", S["subsection"]))
story.append(b("Seller override locked this package, so no coaching is paired and there is no bundle savings."))
story.append(b("Warning: Essentials needs one practice area, and Goose Law has two (business and individual immigration)."))
story.append(b("Warning: Essentials is hidden above $750K. He says about CAD 1M; HubSpot shows $180K to $960K. Confirm revenue."))
story.append(b("Essentials caps ad spend at $7,500, so Starter is the likely next tier as he scales."))

story.append(thin_rule())

# ── Why No Coaching Package ──
story.append(Paragraph("Why No Coaching Package", S["section"]))
story.append(Paragraph("<b>Why it was left out:</b>", S["subsection"]))
story.append(b("The call was about ad management, and the seller locked a marketing-only package."))
story.append(b("The revenue table picked Elite Coach Plus. It was not shown to the client."))
story.append(b("Phase 2 is the FCOO Advisor ($3,297/mo), which fits taking him out of the middle."))
story.append(b("He named intake as the next need. Intake OS has no price in our tables, so none is quoted."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Goose Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Funds a second paid channel so one Meta funnel no longer carries the firm."))
story.append(bd("Builds a tested cost per consultation and per client, so spend can grow with proof."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — minimum viable spend across the recommended channels."))
story.append(b("<b>Aggressive:</b> $7,500/mo — the Essentials tier cap."))

# Use data from Scoping Guide: CPL benchmarks, close rate, avg case value
story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 5.4 cases x CAD 10K = about CAD 54K/mo vs. $3.5K spend = 15.5x return."))
story.append(b("<b>Aggressive:</b> 14.0 cases x CAD 10K = about CAD 140K/mo vs. $7.5K spend = 18.6x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Ad currency (CAD or USD) is unconfirmed; verify with him.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500 from the package decision file. Immigration Google minimum is $3,000."))
story.append(b("<b>Aggressive:</b> the uncapped floor was $14,000, so it is capped at the $7,500 Essentials limit."))
story.append(b("Blended CPL $80.50 (Google 40%, Meta cold 40%, retargeting 20%), 15% close. Total at aggressive: $11,297/mo = 13.6% of revenue, under the 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
# Each: red question (objection_q style) + gray response (objection_a style)
# Responses use specific data from the audit — competitor numbers, transcript quotes, etc.
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I am skeptical that an agency will give my account enough attention."', S["objection_q"]))
story.append(Paragraph("He worried agencies favor larger clients [0:27:00]. Point to monthly reporting and strategy calls, and offer to name his Onboarding contact at kickoff.", S["objection_a"]))

story.append(Paragraph('"What is your success rate in Canada specifically?"', S["objection_q"]))
story.append(Paragraph("He asked this at [0:31:19]. Confirm real Canadian client results with sales ops first. Do not quote a figure you cannot back up.", S["objection_a"]))

story.append(Paragraph('"I have always been concerned about the cost."', S["objection_q"]))
story.append(Paragraph("The fee is a flat $3,797/mo and ads can start near $3,500. He said spend matters less than ROAS [0:19:57], so anchor on cost per signed client.", S["objection_a"]))

story.append(Paragraph('"Google Ads gave me cold leads before."', S["objection_q"]))
story.append(Paragraph("Cold leads often trace to keywords, landing page and follow-up speed. Today his only paid channel is Meta, so Google is untested in this setup.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Essentials</b>", S["price_main"]),
     Paragraph("$3,797/mo", S["price_main"])],
    [Paragraph("Managed Google, Local Service Ads and Meta, plus local SEO and reporting.", S["price_detail"]),
     Paragraph("$3,797 stand alone (no discount)", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,500–$7,500/mo", S["price_main"])],
    [Paragraph("Goes to Google and Meta — not to SMB Team.", S["price_detail"]),
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
    "Total: $3,797/mo + $3,500–$7,500 ad spend  |  No bundle savings  |  8.8%–13.6% of revenue (under 35% cap)",
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
