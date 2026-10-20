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
_FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Design Files", "fonts")
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
OUTPUT_PATH = "the-woods/The Woods Law Firm_October 20, 2026_Sales_Companion.pdf"


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
story.append(Paragraph("The Woods Law Firm", S["title"]))
# FILL: Sales Companion  |  [Month Day, Year]  |  Rep: [Rep Name]
story.append(Paragraph("Sales Companion  |  October 20, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Freddy Woods", S["snap_value"]),
     Paragraph("~$2M (his est.)", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("50%+", S["snap_value"]),
     Paragraph("Greer, SC + 2 offices", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: CASH FLOW", S["section"]))
# FILL: One sentence summarizing what the owner wants — plain language, connects to DBM
story.append(Paragraph("Freddy wants the fastest cash he can get right now, so the firm runs on house money instead of his own.", S["subsection"]))

# FILL: 2-4 direct quotes from the transcript that reveal the DBM
# Use quote_block() for each. Separate with Spacer(1, 1).
story.append(quote_block("I want to be playing with house money, not my money, which I've been doing forever."))
story.append(Spacer(1, 1))
story.append(quote_block("I'm just trying to get the most collection of cash I can right now. That's all that really matters right now."))
story.append(Spacer(1, 1))
story.append(quote_block("Right now it's about walking people in that door."))
story.append(Spacer(1, 2))

# FILL: "What she/he wants:" — 3-5 dark bullets (use bd())
# Each bullet: bold lead phrase + one short sentence. One idea per bullet.
story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Fast cash.</b> He wants the quickest return on ad dollars, then long-term SEO later."))
story.append(bd("<b>More cases in the door.</b> &quot;It's lead flow&quot; — he sees about 60 added cases a month across three counties as worth any spend."))
story.append(bd("<b>Spend on ads, not management.</b> He wants more of the budget on PPC and landing pages than on fees."))
story.append(bd("<b>Proof of return.</b> He tracks every case and will send a monthly signed-case list."))

story.append(Spacer(1, 2))

# FILL: "What is stopping her/him:" — 3-5 gray bullets (use b())
# Each bullet: bold lead phrase + one short sentence. One idea per bullet.
story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Two bad SMB experiences.</b> Radius targeting over the ocean near Georgetown, and a video shoot about 3 months late."))
story.append(b("<b>Contract length.</b> He wants month-to-month; the standard term is 12 months."))
story.append(b("<b>Tight cash.</b> He wants the lowest fee to start and said a setup fee is not workable right now."))
story.append(b("<b>Ad tests that did not work.</b> $3K, $5K, and $10K tests showed no lift; the one-county $3K test did best."))
story.append(b("<b>Weak assets.</b> 2019 website, about 9% DUI map coverage vs. 43–65% for rivals, no Spartanburg page."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

# FILL: "What it does for her/him:" — 2-3 dark bullets (use bd())
# Transformation statements. What the package makes possible. Not deliverables.
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("It takes LSA and PPC off his plate so he can stay in court."))
story.append(bd("It puts spend into county-level campaigns and pages, where his own $3,000 test worked best."))
story.append(bd("It shows what each county returns, so he can scale only what pays."))

# FILL: "[Package Name]  |  $[bundled price]/mo bundled"
story.append(Paragraph("<b>Full Service Marketing — Essentials  |  $3,797/mo (stand-alone)</b>", S["subsection"]))
# FILL: 3-4 gray bullets (use b()) — scoping rationale. One fact per bullet.
story.append(b("Seller picked the lowest full-service tier for his budget; Essentials normally needs under $750K, one office, one practice area — approval needed."))
story.append(b("Price shown is $3,797 as quoted on the call; the decision file says $3,497 bundled with no bundle — confirm with the seller."))
story.append(b("LSA and PPC takeover, 4 landing pages, web/SEO, maps, and AI visibility all answer &quot;it's lead flow.&quot;"))
story.append(b("No coaching, ops, or AI product: the call was only about lead flow. Meta stays with his vendor."))

story.append(thin_rule())


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

# FILL: "[Firm Short Name] — Sales Companion (continued)"
story.append(Paragraph("The Woods Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

# FILL: "What it does for her/him:" — 2 dark bullets (use bd())
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("It puts money on high-intent DUI, domestic violence, and drug searches in his best counties."))
story.append(bd("It starts near the $5,000 he suggested, with room to grow after he sees results."))

# FILL: Ad spend range — conservative (channel minimums) to aggressive (20% rule)
story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $4,500/mo — seller-set low end; below the $7,500 criminal defense channel minimums (flag for paid ads review)."))
story.append(b("<b>Aggressive:</b> $6,000/mo — seller-set high end; under the $7,500 Essentials cap."))

# FILL: ROI projection bullets for BOTH levels — all labeled as estimates
# Use data from Scoping Guide: CPL benchmarks, close rate, avg case value
story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~11 cases x $5K = ~$54.8K/mo vs. $4.5K spend = ~12.2x return."))
story.append(b("<b>Aggressive:</b> ~17 cases x $5K = ~$87.4K/mo vs. $6K spend = ~14.6x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Uses his own 50% close rate and $5,000 case; treat as best case, since his 2026 tests showed no lift.</i>", S["disclaimer"]))

# FILL: How both numbers were calculated — from Scoping Guide Steps 3-4
story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $4,500 split PPC $2,500 + LSA $2,000. Blended cost per lead $171 + 20% cushion = $205, so ~22 leads x 50% = ~11 cases."))
story.append(b("<b>Aggressive:</b> $6,000 split PPC $3,500 + LSA $2,500, ~$172 per lead, so ~35 leads x 50% = ~17 cases. No goal stated; the 20% rule on 2x revenue (~$66K/mo) is far above the cap."))
story.append(b("Total at aggressive: $9,797/mo = ~5.9% of est. monthly revenue ($165K from HubSpot range midpoint). Under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
# FILL: 2-4 objections anticipated from the transcript
# Each: red question (objection_q style) + gray response (objection_a style)
# Responses use specific data from the audit — competitor numbers, transcript quotes, etc.
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I don\'t want to sign a one year contract on something I don\'t know."', S["objection_q"]))
story.append(Paragraph("The standard term is 12 months, and a shorter term needs sales-ops approval, so do not promise one. Lead with the Jerry Novak reference, LSA quick wins in the first weeks, and his written county approval before launch.", S["objection_a"]))

story.append(Paragraph('"I\'ve already had two bad experiences."', S["objection_q"]))
story.append(Paragraph("Name both: the ocean radius targeting and the late video shoot. This plan is county by county with his sign-off on the targets, and Dan joins the first 2–3 calls so he is not handed off.", S["objection_a"]))

story.append(Paragraph('"$130,000 is a lot to see if you can move the needle."', S["objection_q"]))
story.append(Paragraph("His math is ~$50K a year in fees plus ~$75–80K in ads. Fees are $3,797 x 12 = $45,564, there is no setup fee, and ads start at $4,500–$6,000 so he scales only after seeing cost per signed case.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
# FILL: All pricing from the scoping calculation
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Essentials</b>", S["price_main"]),
     Paragraph("$3,797/mo", S["price_main"])],
    [Paragraph("LSA + PPC takeover, 4 landing pages, web/SEO, maps, AI visibility. Sold stand-alone.", S["price_detail"]),
     Paragraph("no bundle discount", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$4,500–$6,000/mo", S["price_main"])],
    [Paragraph("Goes to Google and LSA — not to SMB Team.", S["price_detail"]),
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
    "Total: $3,797/mo + $4,500–$6,000 ad spend  |  $0 bundling savings  |  5.0%–5.9% of est. revenue (under 35% cap)",
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
