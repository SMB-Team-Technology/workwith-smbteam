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

# FILL: Output path — use format [FirmName]_[MMDDYYYY]_Sales_Companion.pdf
OUTPUT_PATH = "kommer-bave-ciccone/Kommer_Bave_Ciccone_LLP_November_4_2026_Sales_Companion.pdf"


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
story.append(Paragraph("Kommer Bave &amp; Ciccone LLP", S["title"]))
# FILL: Sales Companion  |  [Month Day, Year]  |  Rep: [Rep Name]
story.append(Paragraph("Sales Companion  |  November 4, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Rachel Ciccone", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("4 attys listed", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("White Plains + New City, NY", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: TIME + REPUTATION", S["section"]))
# FILL: One sentence summarizing what the owner wants — plain language, connects to DBM
story.append(Paragraph("Rachel wants marketing that works without her time and an online presence that matches the firm's reputation.", S["subsection"]))

# FILL: 2-4 direct quotes from the transcript that reveal the DBM
# Use quote_block() for each. Separate with Spacer(1, 1).
story.append(quote_block("I'm in court every day. And when I'm not in court, I'm doing consults. I'm writing briefs, et cetera."))
story.append(Spacer(1, 1))
story.append(quote_block("I feel like I'm losing a lot of the market share or clients because of my less than stellar web page."))
story.append(Spacer(1, 1))
story.append(quote_block("I want to centralize everything so that I'm not doing these Google click things&hellip; I want just one centralized."))
story.append(Spacer(1, 2))

# FILL: "What she/he wants:" — 3-5 dark bullets (use bd())
# Each bullet: bold lead phrase + one short sentence. One idea per bullet.
story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>One centralized partner.</b> Website, Google, and ads under one team, not separate vendors."))
story.append(bd("<b>Marketing that works without her.</b> She is in court daily with little time to manage ads."))
story.append(bd("<b>A presence that matches her name.</b> She fears losing clients to lawyers who advertise better."))

story.append(Spacer(1, 2))

# FILL: "What is stopping her/him:" — 3-5 gray bullets (use b())
# Each bullet: bold lead phrase + one short sentence. One idea per bullet.
story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Weak web presence.</b> Dated site, generic headline, mobile Lighthouse 44&ndash;67."))
story.append(b("<b>Ads aimed wrong.</b> Current Google Ads lean to PI and wills/trusts, not family law."))
story.append(b("<b>No spare time.</b> She wants her house in order before hiring."))
story.append(b("<b>Price worry.</b> She expects SMB Team to cost more than her $2,900 vendor."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

# FILL: "What it does for her/him:" — 2-3 dark bullets (use bd())
# Transformation statements. What the package makes possible. Not deliverables.
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("One team runs her website, Google presence, and ads so she can stay in court."))
story.append(bd("Family-law LSAs and search ads reach the divorce searches she misses today."))
story.append(bd("Her site and Google profile finally look like a 40-year firm."))

# FILL: "[Package Name]  |  $[bundled price]/mo bundled"
story.append(Paragraph("<b>Option 1: Full Service Marketing Starter  |  $5,697/mo stand-alone</b>", S["subsection"]))
# FILL: 3-4 gray bullets (use b()) — scoping rationale. One fact per bullet.
story.append(b("Seller locked Starter; revenue is not stated."))
story.append(b("Starter covers 2 GBP locations and 250 imported pages."))
story.append(b("Family law plus PI rules out Essentials, so Starter is the eligible tier."))
story.append(b("No coaching, so no bundle: $5,697 stand-alone and $0 savings."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why The Second Option (Essentials, No Coaching)", S["section"]))

# FILL: "What it does for her/him:" — 2-3 dark bullets (use bd())
# Transformation statements. What the package makes possible. Not deliverables.
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("A lower starting cost if her price worry wins out."))
story.append(bd("Same Full Service system: site, local SEO, LSA, Google, and social."))

# FILL: "[Package Name]  |  $[bundled price]/mo bundled"
story.append(Paragraph("<b>Option 2: Full Service Marketing Essentials  |  $3,797/mo stand-alone</b>", S["subsection"]))
# FILL: 3-4 gray bullets (use b()) — scoping rationale. One fact per bullet.
story.append(b("Essentials needs one practice area and one office; seller requested it."))
story.append(b("Scope is tighter: 1 GBP location, 10 imported pages, 5,000 initial words."))
story.append(b("It costs $1,900/mo less than Option 1 (5,697 minus 3,797)."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

# FILL: "[Firm Short Name] — Sales Companion (continued)"
story.append(Paragraph("Kommer Bave &amp; Ciccone — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

# FILL: "What it does for her/him:" — 2 dark bullets (use bd())
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Family-law LSAs and search ads reach divorce and custody searches that go to others today."))
story.append(bd("Spend moves off PI and wills/trusts toward the cases she wants most."))

# FILL: Ad spend range — conservative (channel minimums) to aggressive (20% rule)
story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,000/mo &mdash; seller-set, same for both options."))
story.append(b("<b>Aggressive:</b> $5,000/mo &mdash; seller-set; no revenue goal was stated."))

# FILL: ROI projection bullets for BOTH levels — all labeled as estimates
# Use data from Scoping Guide: CPL benchmarks, close rate, avg case value
story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 6.8 cases x $10.8K = $73K/mo vs. $5.0K spend = 14.7x return."))
story.append(b("<b>Aggressive:</b> 8.2 cases x $10.8K = $88K/mo vs. $5.0K spend = 17.6x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

# FILL: How both numbers were calculated — from Scoping Guide Steps 3-4
story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Family law split LSA $2,000 + Google $3,000. CPL $92 + 20% = $110. 45 leads x 15% default close."))
story.append(b("<b>Aggressive:</b> Same spend, CPL $92, no cushion. 54 leads x 15% close. Case value $10.8K = avg of her 3 retainers."))
story.append(b("Revenue is not stated: 35% cap needs $30.6K/mo (Opt 1) or $25.1K/mo (Opt 2). Spend is under the $5,500 channel minimum: paid ads review."))

story.append(thin_rule())

# ── If She Pushes Back ──
# FILL: 2-4 objections anticipated from the transcript
# Each: red question (objection_q style) + gray response (objection_a style)
# Responses use specific data from the audit — competitor numbers, transcript quotes, etc.
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"You guys are much more expensive, I imagine."', S["objection_q"]))
story.append(Paragraph("She pays about $2,900/mo for ads plus website and does not know the split. Option 2 is $3,797 and Option 1 is $5,697, with ad spend set at $5,000 for both.", S["objection_a"]))

story.append(Paragraph('"I do not want PI ads hurting my matrimonial brand."', S["objection_q"]))
story.append(Paragraph("The plan leads with family law and keeps those campaigns and pages separate. PI comes later and carefully, on her terms.", S["objection_a"]))

story.append(Paragraph('"I already have a vendor."', S["objection_q"]))
story.append(Paragraph("She called that work lackluster and wants one centralized partner. Ask the contract end date and cancellation terms first.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
# FILL: All pricing from the scoping calculation
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    # FILL: Marketing package name and bundled price
    [Paragraph("<b>Option 1: Full Service Marketing Starter</b>", S["price_main"]),
     Paragraph("$5,697/mo", S["price_main"])],
    # FILL: One-line description and stand-alone price with strikethrough
    [Paragraph("Website, local SEO, LSA, Google, and social. Up to 2 GBP locations.", S["price_detail"]),
     Paragraph("stand-alone price", S["price_detail"])],
    # FILL: Coaching package name and bundled price
    [Paragraph("<b>Option 2: Full Service Marketing Essentials</b>", S["price_main"]),
     Paragraph("$3,797/mo", S["price_main"])],
    # FILL: One-line description and stand-alone price with strikethrough
    [Paragraph("Same system, smaller scope. 1 GBP location, 10 imported pages.", S["price_detail"]),
     Paragraph("stand-alone price", S["price_detail"])],
    # FILL: Recommended ad spend range (conservative to aggressive)
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,000/mo", S["price_main"])],
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
    ("LINEBELOW", (0,5), (-1,5), 0.5, RULE_GRAY),
]))
story.append(pt)
# FILL: Total line — bundled total + ad spend range | savings | % of revenue at aggressive level
story.append(Paragraph(
    "Option 1: $5,697/mo  |  Option 2: $3,797/mo  |  plus $5,000 ad spend  |  No bundle savings  |  Revenue not stated",
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
