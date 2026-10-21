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

OUTPUT_PATH = "office-of-james-patrick-barrett/BLLegal_October212026_Sales_Companion.pdf"


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

story.append(Paragraph("BL Legal (Brooks LeBoeuf Trial Attorneys)", S["title"]))
story.append(Paragraph("Sales Companion  |  October 21, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
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
    [Paragraph("Catherine Register, COO", S["snap_value"]),
     Paragraph("~$10M (2026)", S["snap_value"]),
     Paragraph("7 attorneys", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("~40% referred", S["snap_value"]),
     Paragraph("Tallahassee, FL", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: MARKET LEADERSHIP", S["section"]))
story.append(Paragraph("She wants BL Legal to run as the digital pioneer of Tallahassee and to show the shareholders a fast, provable return in signed cases.", S["subsection"]))

story.append(quote_block("They've brought me here to build their marketing strategy from the ground up."))
story.append(Spacer(1, 1))
story.append(quote_block("There's a real room for us to run as like the digital pioneers of this market."))
story.append(Spacer(1, 1))
story.append(quote_block("It has to come down to cases signed. And I cannot work with vendors who are like, traffic is up, and impressions are great."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Digital leadership.</b> She sees an open lane while rivals lean on TV and billboards."))
story.append(bd("<b>SEO first.</b> Long-term SEO and her whole Google footprint come first, then paid ads, then YouTube."))
story.append(bd("<b>Proof in signed cases.</b> She wants attribution beyond \"how did you hear about us?\""))
story.append(bd("<b>One strong partner.</b> She fears \"jack of all trades, master of none\" and wants LSA and GBP as core."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Referral-only growth.</b> Almost all cases are referred, and some growth came from lateral hires."))
story.append(b("<b>No marketing team yet.</b> She is building the function from scratch."))
story.append(b("<b>Weak current efforts.</b> The SEO vendor underperforms. One attorney runs ads."))
story.append(b("<b>Budget not final.</b> About $1M to work with. Shareholders review Nov 7."))
story.append(b("<b>Slow intake.</b> Signing takes a week or two. She calls intake \"suboptimal.\""))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("One team owns the whole path from search to signed case."))
story.append(bd("The long-game SEO and Google footprint start now, ahead of her mid-November goal."))
story.append(bd("A fast mobile site and review system sit under every ad dollar she approves."))

story.append(Paragraph("<b>Full Service Marketing, Platinum  |  $18,997/mo stand-alone (seller override)</b>", S["subsection"]))
story.append(b("Revenue is about $10M (HubSpot says $3M+), above the $3M Platinum floor."))
story.append(b("Mobile speed is 36/100, so a rebuild is needed. That requires Full Service."))
story.append(b("Five case types need deep content. Platinum has 30K words at launch."))
story.append(b("Seller locked Platinum only, stand-alone price. Bundle price $15,997 not used."))

story.append(thin_rule())

# ── No coaching package ──
story.append(Paragraph("Why No Coaching Package, and Confirm Before the Call", S["section"]))

story.append(Paragraph("<b>Why the plan is marketing only:</b>", S["subsection"]))
story.append(bd("The seller removed coaching and all other products from this proposal."))
story.append(bd("She is \"exclusively focused on marketing and intake,\" with no intake partner wanted."))

story.append(Paragraph("<b>Confirm before the call</b>", S["subsection"]))
story.append(b("<b>Review counts unconfirmed.</b> Verify live before the call."))
story.append(b("<b>Existing vendor.</b> Get the SEO contract end date and her \"committed partnerships.\""))
story.append(b("<b>Insider info.</b> She was COO at Fasig Brooks. Never quote its numbers."))
story.append(b("<b>Approvals.</b> MRR over $10K and ad spend over $25K need scoping approval."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("BL Legal — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Reaches people searching for a Tallahassee injury lawyer right now, beyond the referral network."))
story.append(bd("Fits inside the $1M she described, with room to grow as results show."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $9,200/mo — minimum viable spend on Google, LSA and Meta retargeting."))
story.append(b("<b>Aggressive:</b> $30,000/mo — most that fits her budget. Needs scoping approval."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 2.2 cases x $35K = $77K/mo vs. $9.2K spend = 8.4x return."))
story.append(b("<b>Aggressive:</b> 9.1 cases x $35K = $318K/mo vs. $30K spend = 10.6x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Uses a 15% close rate, not her 40% referral rate. The $35K fee is her number, skewed by a few big cases.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Injury minimums: PPC $6,000 + LSA $2,000 + Meta $1,200 = $9,200. The file said $7,500, which is below this sum."))
story.append(b("<b>Aggressive:</b> $14.5M goal x 20% ÷ 12 = $241,667, capped at $150K. That is far above her budget, so $30,000 stays."))
story.append(b("Total spend at aggressive: $48,997/mo = 5.9% of revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I\'m meeting Scorpion, Rankings and others. Why you?"', S["objection_q"]))
story.append(Paragraph("Show the Houston PI client's SEMrush chart she called significant growth. Offer signed-case reports she can check against her own accounts.", S["objection_a"]))

story.append(Paragraph('"That fee is a big slice of my budget."', S["objection_q"]))
story.append(Paragraph("$18,997/mo is about $228K a year, under a quarter of the $1M she described. Ad spend starts at $9,200 and grows only as results prove out.", S["objection_a"]))

story.append(Paragraph('"I\'ve seen it done as jack of all trades, master of none."', S["objection_q"]))
story.append(Paragraph("LSA, GBP, SEO, Google and Meta are core deliverables under one team, not add-ons. Ask which channel she wants to test first.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing, Platinum</b>", S["price_main"]),
     Paragraph("$18,997/mo", S["price_main"])],
    [Paragraph("Site rebuild, SEO, GBP, reviews, Google Ads, LSA and Meta.", S["price_detail"]),
     Paragraph("Stand-alone, no bundle discount", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$9,200–$30,000/mo", S["price_main"])],
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
story.append(Paragraph(
    "Total: $18,997/mo + $9,200–$30,000 ad spend  |  No bundle discount (seller override)  |  3.4%–5.9% of $10M revenue (under 35% cap)",
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
