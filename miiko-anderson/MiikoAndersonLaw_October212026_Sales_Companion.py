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

OUTPUT_PATH = "miiko-anderson/MiikoAndersonLaw_October212026_Sales_Companion.pdf"


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

story.append(Paragraph("Miiko Anderson Law", S["title"]))
story.append(Paragraph("Sales Companion  |  October 21, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Miiko Anderson", S["snap_value"]),
     Paragraph("~$25K/mo (~$300K/yr gross)", S["snap_value"]),
     Paragraph("Solo + assistant", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("Unclear", S["snap_value"]),
     Paragraph("Fresno, CA", S["snap_value"])],
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
story.append(Paragraph("She wants a firm that runs without her in every case, so she has space and energy for other things.", S["subsection"]))

story.append(quote_block("It should be scaled to the level that I'm not needed in every case."))
story.append(Spacer(1, 1))
story.append(quote_block("...so that I have some energy to devote to some other things that are of interest... so that it gives me a little bit space and freedom."))
story.append(Spacer(1, 1))
story.append(quote_block("Allow me to focus on other things that I'm better at."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Branding and brand voice.</b> She calls branding her biggest challenge right now."))
story.append(bd("<b>The animated video series.</b> She raised it 3-5 times and it is why she came to us."))
story.append(bd("<b>Predictable lead flow.</b> She wants a framework to see her options."))
story.append(bd("<b>One simple answer.</b> She wants one package and to be done, not pieced together."))
story.append(bd("<b>Associate attorneys.</b> She wants a couple of attorneys so she can focus elsewhere."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Referral-only leads.</b> She has done no marketing, so lead flow is unpredictable."))
story.append(b("<b>She is the whole firm.</b> One assistant plus contract help, and she works 30+ hours a week."))
story.append(b("<b>No set budget.</b> She wants value, not the cheapest price."))
story.append(b("<b>Uneven revenue.</b> Months swing around the average and there is no bookkeeper yet."))
story.append(b("<b>A weak website role.</b> The site only verifies referrals, and her consulting site may outrank it."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives her a second source of clients so quiet months stop making her nervous."))
story.append(bd("Gives her a coach to work through her options and the order of her first hires."))
story.append(bd("Keeps the start small and simple, which fits a solo attorney with no set budget."))

story.append(Paragraph("<b>Coach Essentials Plus  |  $2,497/mo stand-alone</b>", S["subsection"]))
story.append(b("<b>Locked by seller:</b> Randy swapped to this on 10/26. Group coaching plus a monthly 1:1 call."))
story.append(b("<b>Fits on revenue:</b> About $300K sits in the $250K-$400K band for the lower-cost coaching option."))
story.append(b("<b>FLAG, not asked for:</b> She never discussed coaching or LSAs. Pitch it as our recommendation, not her request."))
story.append(Paragraph("<b>LSA Management Add-On  |  Complimentary ($900/mo value)</b>", S["subsection"]))
story.append(b("<b>FLAG, fee waiver:</b> The $0 fee is Randy's call, not a catalog price. Confirm sales-ops approval."))
story.append(b("<b>FLAG, video:</b> The animated series is not in this package. Brand Video is a separate $4,997 add-on. Address it on the call."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Miiko Anderson Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Puts her in front of Fresno people searching for a criminal defense lawyer right now."))
story.append(bd("Gives her a trackable lead source she pays for only when a prospect calls."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $2,000/mo — Randy's minimum, equal to the criminal defense LSA channel minimum."))
story.append(b("<b>Aggressive:</b> $2,500/mo — FLAG: derived ceiling. Randy gave none; the $5,000 total-spend limit minus the $2,497 fee leaves ~$2,500. Confirm it."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 2.6 cases x $4K = ~$10.4K/mo vs. $2K spend = 5.2x return."))
story.append(b("<b>Aggressive:</b> 3.9 cases x $4K = ~$15.6K/mo vs. $2.5K spend = 6.2x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Case value ($4K) is a criminal defense default and the 25% close rate is a planning figure; neither was confirmed on the call. Warm-referral conversion will not carry over to cold paid leads.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $2,000 ÷ $192 per lead (LSA midpoint $160 + 20% cushion) = 10.4 leads x 25% close rate = 2.6 cases."))
story.append(b("<b>Aggressive:</b> $2,500 ÷ $160 per lead = 15.6 leads x 25% close rate = 3.9 cases."))
story.append(b("Total at aggressive: $4,997/mo = 20.0% of $25K revenue. Under the 35% cap. FLAG: $2,000 is under the $3,000 paid-ads minimum, so paid ads team review is needed."))
story.append(b("LSA alone will not reach her likely $600K goal (2x current, default). Phase 2 adds web and local search."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"Is a solo attorney too small a client for this?"', S["objection_q"]))
story.append(Paragraph("She asked this at 00:07:51. This plan is sized for a solo firm around $300K. Her credentials (Certified Criminal Law Specialist, 13,000+ courtroom appearances) are the asset we build on.", S["objection_a"]))

story.append(Paragraph('"I don\'t have an actual budget, and I don\'t want to piece it together."', S["objection_q"]))
story.append(Paragraph("One $2,497/mo coaching plan, with the LSA management fee waived. Ad spend is separate and starts at $2,000. Total stays well inside 35% of her revenue.", S["objection_a"]))

story.append(Paragraph('"I want to see the animated work reflect me before I commit."', S["objection_q"]))
story.append(Paragraph("Be upfront: the animated series is not part of this package, and coaching does not build her brand voice. Video can be scoped separately. Do not promise it in this proposal.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Coach Essentials Plus</b>", S["price_main"]),
     Paragraph("$2,497/mo", S["price_main"])],
    [Paragraph("Group coaching plus a monthly 1:1 coaching call.", S["price_detail"]),
     Paragraph("stand-alone, no bundle discount", S["price_detail"])],
    [Paragraph("<b>LSA Management Add-On</b>", S["price_main"]),
     Paragraph("Complimentary", S["price_main"])],
    [Paragraph("Seller-waived fee. Catalog price is $900/mo.", S["price_detail"]),
     Paragraph("$900/mo value", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$2,000–$2,500/mo", S["price_main"])],
    [Paragraph("Goes to Google Local Services Ads — not to SMB Team.", S["price_detail"]),
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
    "Total: $2,497/mo + $2,000–$2,500 ad spend  |  Savings: $900/mo (waived LSA fee)  |  18.0%–20.0% of revenue (under 35% cap)",
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
