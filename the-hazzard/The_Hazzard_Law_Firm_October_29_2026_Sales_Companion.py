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
_FONT_DIR = os.path.join("Design Files", "fonts")
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

# FILL: Output path — use format [FirmName]_[MMDDYYYY]_Sales_Companion.pdf
OUTPUT_PATH = "the-hazzard/The_Hazzard_Law_Firm_October_29_2026_Sales_Companion.pdf"


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

# FILL: Firm's full legal name
story.append(Paragraph("The Hazzard Law Firm, LLC", S["title"]))
# FILL: Sales Companion  |  [Month Day, Year]  |  Rep: [Rep Name]
story.append(Paragraph("Sales Companion  |  October 29, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Wakisha Hazzard", S["snap_value"]),
     Paragraph("Not stated (HubSpot: $500K-$1M)", S["snap_value"]),
     Paragraph("3 attys (site)", S["snap_value"]),
     Paragraph("3 (prov.)", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Birmingham, AL", S["snap_value"])],
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
# FILL: "Dominant Buying Motive: [DBM KEYWORD IN CAPS]" — e.g. FREEDOM, SECURITY, LEGACY
story.append(Paragraph("Dominant Buying Motive: NOT STATED", S["section"]))
# FILL: One sentence summarizing what the owner wants — plain language, connects to DBM
story.append(Paragraph("No motive was stated on this call. Ask what the firm should make possible for her before the proposal call.", S["subsection"]))

# FILL: 2-4 direct quotes from the transcript that reveal the DBM
# Use quote_block() for each. Separate with Spacer(1, 1).
story.append(quote_block("I don't wanna get rid of you, Dan. You brought me back."))
story.append(Spacer(1, 1))
story.append(quote_block("So, end of the month is right here, Dan."))
story.append(Spacer(1, 2))

# FILL: "What she/he wants:" — 3-5 dark bullets (use bd())
# Each bullet: bold lead phrase + one short sentence. One idea per bullet.
story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>To stay with SMB Team.</b> She told Dan, \"You brought me back.\""))
story.append(bd("<b>To review her agreement.</b> She asked to meet tomorrow at 4 pm Central."))
story.append(bd("<b>To join the Marco Island event.</b> She is trying to make Dec 3-5."))
story.append(bd("<b>Her business goals are unknown.</b> Revenue, goal and lead sources never came up."))

story.append(Spacer(1, 2))

# FILL: "What is stopping her/him:" — 3-5 gray bullets (use b())
# Each bullet: bold lead phrase + one short sentence. One idea per bullet.
story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No objections stated.</b> No budget limit or vendor contract came up on this call."))
story.append(b("<b>Slow mobile site.</b> Mobile PageSpeed is 67; desktop is 99."))
story.append(b("<b>Reviews unverified.</b> Her Google count reads 103, 149 or 153 by source; verify live."))
story.append(b("<b>Thin ad tracking.</b> No Meta pixel in the homepage code; GTM contents not checked."))
story.append(b("<b>Mixed listings.</b> Yelp says Divorce &amp; Family Law; the site lists two phone numbers."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

# FILL: "What it does for her/him:" — 2-3 dark bullets (use bd())
# Transformation statements. What the package makes possible. Not deliverables.
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Puts her website, local SEO and ads under one team instead of several vendors."))
story.append(bd("Turns three practice areas into a steady, measurable flow of consultations."))
story.append(bd("Adds tracking and retargeting that may be missing today."))

# FILL: "[Package Name]  |  $[bundled price]/mo bundled"
story.append(Paragraph("<b>Full Service Marketing - Starter  |  $4,997/mo bundled</b>", S["subsection"]))
# FILL: 3-4 gray bullets (use b()) — scoping rationale. One fact per bullet.
story.append(b("HubSpot revenue band $500K-$1M (not stated by her) points to Starter."))
story.append(b("Personal injury and multiple practice areas rule out Essentials."))
story.append(b("Seller override on Oct 28 removed Elite Coach Plus; marketing only."))
story.append(b("This was a coaching call, not marketing discovery. Confirm this matches her earlier agreement in HubSpot."))

story.append(thin_rule())

# ── Why No Coaching Package ──
story.append(Paragraph("Why No Coaching Package", S["section"]))
story.append(Paragraph("<b>What to know before the call:</b>", S["subsection"]))
story.append(b("The seller removed Elite Coach Plus from this proposal on Oct 28."))
story.append(b("She is already on a coaching call with Michael Kruchko; do not oversell coaching."))
story.append(b("Phase 2 and 3 in the report preview FCOO, FCFO, bookkeeping and Legal AI Workforce only as future steps, with no prices."))
story.append(b("Confirm Legal AI Workforce delivery has launched before you discuss it."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

# FILL: "[Firm Short Name] — Sales Companion (continued)"
story.append(Paragraph("The Hazzard Law Firm - Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

# FILL: "What it does for her/him:" — 2 dark bullets (use bd())
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Puts the firm in front of people searching for a Birmingham lawyer right now."))
story.append(bd("Lets her start at a lower spend and scale as the results show."))

# FILL: Ad spend range — conservative (channel minimums) to aggressive (20% rule)
story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,500/mo - minimum viable spend; matches the PI floor."))
story.append(b("<b>Aggressive:</b> $16,500/mo - the most the 35% cap allows after the fee."))

# FILL: ROI projection bullets for BOTH levels — all labeled as estimates
# Use data from Scoping Guide: CPL benchmarks, close rate, avg case value
story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~5.3 cases x ~$4.2K = ~$22.3K/mo vs. $7.5K spend = ~3.0x return."))
story.append(b("<b>Aggressive:</b> ~14 cases x ~$4.2K = ~$58.9K/mo vs. $16.5K spend = ~3.6x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Assumes 15% close rate, default case values and an even split across 3 practice areas.</i>", S["disclaimer"]))

# FILL: How both numbers were calculated — from Scoping Guide Steps 3-4
story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> PI medium-competition hard floor = $7,500. Channel minimums for all 3 areas would total more; paid ads team to review."))
story.append(b("<b>Aggressive:</b> No goal stated; 2x $750K = $1.5M x 20% ÷ 12 = $25,000. Tier 4 (1.00x) = $25,000. Minus $4,997 fee = $20,003. Over cap, cut to $16,500."))
story.append(b("Total at aggressive: $21,497/mo = 34.4% of est. revenue ($62,500/mo, HubSpot midpoint). Under the 35% cap. Confirm revenue."))

story.append(thin_rule())

# ── If She Pushes Back ──
# FILL: 2-4 objections anticipated from the transcript
# Each: red question (objection_q style) + gray response (objection_a style)
# Responses use specific data from the audit — competitor numbers, transcript quotes, etc.
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I already have an agreement. Why is this different?"', S["objection_q"]))
story.append(Paragraph("Check HubSpot first. Confirm this proposal matches what she, Gabby and Dan reviewed. Dan mentioned an end-of-month promotion; confirm its terms before quoting.", S["objection_a"]))

story.append(Paragraph('"I am already in coaching with Michael."', S["objection_q"]))
story.append(Paragraph("Coaching shapes how the firm runs. This audit points to the site, local profile and tracking: mobile 67 vs desktop 99, no Meta pixel in the homepage code. Marketing fills the pipeline.", S["objection_a"]))

story.append(Paragraph('"Why spend $7,500 or more on ads?"', S["objection_q"]))
story.append(Paragraph("Start at $7,500 and scale. The estimate is ~3.0x on default case values, so ask her real numbers. Revill, Harris and Farris Riley &amp; Pitt show in Birmingham roundups; their ads and review counts were not verified.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
# FILL: All pricing from the scoping calculation
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing - Starter</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    # FILL: One-line description and stand-alone price with strikethrough
    [Paragraph("Website, SEO and Google, LSA and Meta ads under one team.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    # FILL: Recommended ad spend range (conservative to aggressive)
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,500–$16,500/mo", S["price_main"])],
    [Paragraph("Goes to Google, LSA, and Meta — not to SMB Team.", S["price_detail"]),
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
# FILL: Total line — bundled total + ad spend range | savings | % of revenue at aggressive level
story.append(Paragraph(
    "Total: $4,997/mo + $7,500–$16,500 ad spend  |  Save $700/mo by bundling  |  20.0%–34.4% of est. revenue (under 35% cap)",
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
