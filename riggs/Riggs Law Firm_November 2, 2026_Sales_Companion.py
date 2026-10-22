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

OUTPUT_PATH = "riggs/Riggs Law Firm_November 2, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Riggs Law Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  November 2, 2026  |  Rep: Nick Holderman", S["subtitle"]))
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
    # FILL: All six snapshot values from Pass 1 research and transcript
    [Paragraph("Dan Riggs", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("3", S["snap_value"]),
     Paragraph("3", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Las Vegas, NV", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE AND DOMINATE", S["section"]))
story.append(Paragraph("Dan wants to build the leading consumer bankruptcy firm in the Las Vegas valley and keep helping people along the way.", S["subsection"]))

# Use quote_block() for each. Separate with Spacer(1, 1).
story.append(quote_block("that's really what it came down to is I missed helping people."))
story.append(Spacer(1, 1))
story.append(quote_block("over time, I'd like to become the firm in this valley."))
story.append(Spacer(1, 1))
story.append(quote_block("I'm missing this opportunity right now while I'm small to simply create the right process so it just builds naturally going forward."))
story.append(Spacer(1, 2))

# Each bullet: bold lead phrase + one short sentence. One idea per bullet.
story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>A 50-case-a-month firm.</b> He files about 20-25 a month and wants 50 within a year."))
story.append(bd("<b>Leads that become clients.</b> He sees leads slip through the cracks."))
story.append(bd("<b>A process that builds itself.</b> He wants it built now, while the firm is small."))

story.append(Spacer(1, 2))

# Each bullet: bold lead phrase + one short sentence. One idea per bullet.
story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No follow-up system.</b> If a lead does not sign that day, the team moves on in a day or two."))
story.append(b("<b>Ad hoc intake.</b> Dan, the paralegal and the receptionist all handle leads informally."))
story.append(b("<b>No time.</b> He is so busy he struggles to find time to build the process."))
story.append(b("<b>Tight budget.</b> Coaching \"feels like a lot to invest in right now.\""))

story.append(thin_rule())

# ── Why No Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

# Transformation statements. What the package makes possible. Not deliverables.
story.append(Paragraph("<b>What leaving it out does for him:</b>", S["subsection"]))
story.append(bd("Keeps the plan on what he asked about: intake and follow-up."))
story.append(bd("Fixes conversion before paying for more leads."))
story.append(bd("Keeps total cost small and clear for a price-sensitive client."))

story.append(Paragraph("<b>No marketing package  |  $0/mo (call-purpose override)</b>", S["subsection"]))
story.append(b("He said \"it's a good problem that more people are inquiring than we're able to capture.\""))
story.append(b("He runs Google Ads and pays two per-lead vendors. No agency contract was stated."))
story.append(b("His \"first two buckets\" comment was hedged; he then agreed intake comes first."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

# Transformation statements. What the package makes possible. Not deliverables.
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives him a coach to build a follow-up routine for leads that do not sign right away."))
story.append(bd("Lets him learn from other law firm owners while the firm is small."))
story.append(bd("Fits a firm that opened this year at the lowest standalone coaching price."))

story.append(Paragraph("<b>Coach Essentials Plus  |  $2,497/mo standalone</b>", S["subsection"]))
story.append(b("Revenue not stated. HubSpot range is $180K-$960K; the system used about $570K. Confirm it."))
story.append(b("The revenue table points to Elite Coach Plus at $3,200/mo. The budget override moved it down."))
story.append(b("Seller approved standalone pricing at $2,497/mo: no bundle discount and $0 savings."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Riggs Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Ad Spend ──
story.append(Paragraph("Why No Ad Spend", S["section"]))

story.append(Paragraph("<b>What leaving it out does for him:</b>", S["subsection"]))
story.append(bd("Keeps every dollar on fixing follow-up before spending more to bring leads in."))
story.append(bd("Leaves room to revisit marketing once follow-up is working."))

story.append(Paragraph("<b>Ad spend and ROI:</b>", S["subsection"]))
story.append(b("No ads package is recommended, so no ad spend range or ROI projection was calculated."))
story.append(b("The 10x ROI line ($2,500 vs. $25,000/mo lost) was the rep's math, not Dan's. Do not present it as measured."))
story.append(b("Dan's own estimates are hedged: \"maybe up to 20%\" lost, \"as high as 10 a month.\" Treat them as upper bounds."))
story.append(b("Case values: Chapter 7 is a $2,000 fee (about $1,500 after costs). Chapter 13 is about $4,500."))
story.append(Paragraph("<b>Verify before the call:</b>", S["subsection"]))
story.append(b("Google ratings and review counts for Riggs and competitors are unconfirmed. None are in the client report."))
story.append(b("PageSpeed scores were not obtained. GBP, 3-pack, Ads, LSA and Meta Ad Library were not observed."))
story.append(b("Phase 3 mentions AI Workforce Pro. Confirm Legal AI Workforce delivery has launched first."))
story.append(b("Revenue is unconfirmed. Under $300K needs scoping approval; under $250K confirm 4 months of funds."))

story.append(thin_rule())

# ── If He Pushes Back ──
# Each: red question (objection_q style) + gray response (objection_a style)
# Responses use specific data from the audit — competitor numbers, transcript quotes, etc.
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph("&quot;I don't have a ton of money right now. Am I too early for this?&quot;", S["objection_q"]))
story.append(Paragraph("Start with his own words: coaching \"feels like a lot... not bringing in more business yet.\" Coach Essentials Plus is one flat $2,497/mo and the lowest standalone coaching option. He already pays about $100 and $40 per vendor lead that can go unfollowed.", S["objection_a"]))

story.append(Paragraph("&quot;Won't the price keep going up as you add phases?&quot;", S["objection_q"]))
story.append(Paragraph("Today's price is $2,497/mo and nothing else. Phases 2 and 3 in the report are optional, priced separately, and only come up if the numbers support them.", S["objection_a"]))

story.append(Paragraph("&quot;Can't I just figure this out myself with Practice Panther?&quot;", S["objection_q"]))
story.append(Paragraph("He said Practice Panther is great after clients retain, and that he is so busy he struggles to find time to build the lead process. Coaching gives him a coach and a routine to follow. It does not replace his tools.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Coach Essentials Plus</b>", S["price_main"]),
     Paragraph("$2,497/mo", S["price_main"])],
    [Paragraph("Group coaching plus a monthly 1:1 coaching call. Standalone price.", S["price_detail"]),
     Paragraph("no bundle discount", S["price_detail"])],
    [Paragraph("<b>Marketing and Ad Spend</b>", S["price_main"]),
     Paragraph("Not included", S["price_main"])],
    [Paragraph("Revisit after intake and follow-up are working.", S["price_detail"]),
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
    "Total: $2,497/mo  |  No bundle savings (standalone)  |  5.3% of est. $570K revenue (under 35% cap)",
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
