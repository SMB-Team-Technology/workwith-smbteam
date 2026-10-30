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

OUTPUT_PATH = "otorowski-morrow-and-golden/Otorowski Morrow and Golden_October 30, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Otorowski Morrow and Golden", S["title"]))
story.append(Paragraph("Sales Companion  |  October 30, 2026  |  Rep: Michael Kopp", S["subtitle"]))
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
    [Paragraph("Chris Otorowski", S["snap_value"]),
     Paragraph("$3M+ (HubSpot, unverified)", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("~2%", S["snap_value"]),
     Paragraph("Seattle + Bainbridge", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM (inferred)", S["section"]))
story.append(Paragraph("He wants better cases and fewer junk calls, and he does not want to vanish as search moves to ChatGPT.", S["subsection"]))

story.append(quote_block("I am sure that there are higher quality cases that we would like to attract."))
story.append(Spacer(1, 1))
story.append(quote_block("If you're going to get calls, you need to&hellip; come up when somebody uses ChatGPT."))
story.append(Spacer(1, 1))
story.append(quote_block("We get five calls every day. Every day, a malpractice call. And most of them are junk."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Better cases.</b> He wants higher-quality malpractice cases, not more volume."))
story.append(bd("<b>A personal injury mix.</b> He wants good PI cases to dilute a high-risk specialty."))
story.append(bd("<b>ChatGPT visibility.</b> The call came from an ad saying firms invisible in ChatGPT lose out."))
story.append(bd("<b>Dictation.</b> He wants to dictate into his software and not transfer anything."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Low visibility.</b> Google profile is 1.0 stars on 2 reviews and the firm is missing from all 6 Maps lists."))
story.append(b("<b>Hacked site.</b> Hidden pharmacy and casino links sit on the homepage. He only said okay."))
story.append(b("<b>Unknown vendors.</b> He has \"homework\" to learn what SEO and ads he already pays for."))
story.append(b("<b>No budget.</b> He said no budget is earmarked and needs a couple of weeks to gather info."))
story.append(b("<b>Long case cycle.</b> Cases take about three years, so return feels slow."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Makes the firm easy to find on Google, in Maps, and in AI answers."))
story.append(bd("Points ads and site content at the cases he wants, so fewer calls are junk."))
story.append(bd("Opens a PI lane (trucking, auto, product) next to med-mal."))

story.append(Paragraph("<b>Full Service Marketing &ndash; Starter  |  $5,697/mo (stand-alone price)</b>", S["subsection"]))
story.append(b("Seller chose Starter only in Slack, with ad spend of $7,500&ndash;$12,500. Built as-is."))
story.append(b("Only one bundle product, so the stand-alone $5,697 applies. The $4,997 bundle price does not."))
story.append(b("HubSpot revenue of $3M+ would point to Platinum. Revenue is unverified. Confirm it."))
story.append(b("Starter covers 2 GBP locations. He has Seattle and Bainbridge Island. Site is 2018-era, so a rebuild fits."))

story.append(thin_rule())

# ── What We Left Out ──
story.append(Paragraph("What We Left Out, and Why", S["section"]))
story.append(b("<b>Coaching:</b> Not discussed or priced on the call. The seller removed it from the package."))
story.append(b("<b>AI Workforce Pro:</b> He liked the dictation demo. The seller removed it. It is in Phase 3 of the roadmap."))
story.append(b("<b>Before offering AI:</b> Confirm LAW delivery has launched and confirm the seat count."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Otorowski Morrow and Golden &mdash; Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts the firm in front of high-intent Seattle med-mal and injury searches."))
story.append(bd("Keeps spend on wanted cases by blocking dental, mold, and minor-damage terms."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,500/mo &mdash; Google plus Meta retargeting (seller set)."))
story.append(b("<b>Aggressive:</b> $12,500/mo &mdash; Google, LSA, and Meta retargeting (seller set)."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 0.4 cases x $6.5K = $2.4K/mo vs. $7.5K spend = 0.3x return."))
story.append(b("<b>Aggressive:</b> 0.8 cases x $6.5K = $5.1K/mo vs. $12.5K spend = 0.4x return."))
story.append(b("<b>Warning:</b> Returns are under 1x. The 2% close rate is low and the case value is a PI default."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Case value ($5K&ndash;$8K) is a default, not stated on the call.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Accident/Injury minimums: PPC $6,000 + Meta retargeting $1,200 = $7,200. Seller set $7,500."))
story.append(b("<b>Aggressive:</b> Seller set $12,500. No goal stated, so 2x revenue would imply far more, well above Starter's $25K cap."))
story.append(b("CPL midpoints: Google $705, LSA $235, Meta $90. Conservative adds a 20% cushion. Total at aggressive: $18,197/mo = 7.3% of revenue. Under the 35% cap."))
story.append(b("Flag: Seattle PI hard floor is $10,000, so $7,500 needs paid ads team review."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I need a couple of weeks to figure out what we already have going."', S["objection_q"]))
story.append(Paragraph("Fine. Start with a vendor inventory. The spam links and Google profile need fixing either way.", S["objection_a"]))

story.append(Paragraph('"We already reject 800 cases a year. Why get more calls?"', S["objection_q"]))
story.append(Paragraph("The goal is better calls, not more. Ads use negative keywords for dental, mold, and minor-damage cases he already declines.", S["objection_a"]))

story.append(Paragraph('"I have no budget set."', S["objection_q"]))
story.append(Paragraph("Total spend tops out at about 7% of revenue if $3M holds. Confirm revenue first, then set the budget with him.", S["objection_a"]))

story.append(Paragraph('"Cases take three years. When do I see a return?"', S["objection_q"]))
story.append(Paragraph("Be honest: the model shows under 1x. Ask his real fee per case. Birth injury values may be far above the default.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing &ndash; Starter</b>", S["price_main"]),
     Paragraph("$5,697/mo", S["price_main"])],
    [Paragraph("Ads, local SEO, LSA, Meta retargeting, and site updates.", S["price_detail"]),
     Paragraph("stand-alone price, no bundle", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,500&ndash;$12,500/mo", S["price_main"])],
    [Paragraph("Goes to Google, LSA, and Meta &mdash; not to SMB Team.", S["price_detail"]),
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
    "Total: $5,697/mo + $7,500&ndash;$12,500 ad spend  |  No bundle savings (single product)  |  5.3%&ndash;7.3% of revenue (under 35% cap)",
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
