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

OUTPUT_PATH = "totaro-shanahan/TotaroShanahan_October212026_Sales_Companion.pdf"


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

story.append(Paragraph("Totaro &amp; Shanahan", S["title"]))
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
    [Paragraph("Michael Totaro", S["snap_value"]),
     Paragraph("~$600K; goal $1.5M", S["snap_value"]),
     Paragraph("3 people", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("Not stated (15% used)", S["snap_value"]),
     Paragraph("Pacific Palisades, CA", S["snap_value"])],
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
story.append(Paragraph("Michael wants more time on the legal work, with someone else running marketing and administration so the firm can grow.", S["subsection"]))

story.append(quote_block("I want to turn that around and spend more time on the legal work, and I'm also trying to expand the administrative aspect to somebody else. So that we can actually grow."))
story.append(Spacer(1, 1))
story.append(quote_block("we'd like to get this chapter sevens up to about 20 or 30 a month."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>More Chapter 7 cases.</b> About 2 a month today; he wants 20 to 30, which he put at about $40K a month."))
story.append(bd("<b>Time on legal work.</b> Someone else owns marketing and admin. \"I just don't want to learn more.\""))
story.append(bd("<b>A $1.5M year.</b> He called it a comfortable range, up from about $600K now."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No online footprint.</b> 1 Google review; not seen in LA, OC, or SD map results."))
story.append(b("<b>No digital ad history.</b> Only radio, now stopped. Facebook shows the firm as banned."))
story.append(b("<b>No budget benchmark.</b> Open to about $10K/mo but has \"no base to go from.\""))
story.append(b("<b>Wary of SEO talk.</b> He passed on a vendor pitching Google placement. Lead with calls."))
story.append(b("<b>Referral-only base.</b> Treat Tyson Takeuchi as a referral partner, never a competitor."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts the firm in front of Chapter 7 searchers where competitors hold 231 to 641 reviews."))
story.append(bd("Gives him a team that runs the ads, so he never has to learn the platforms."))
story.append(bd("Turns \"more exposure\" into calls and cases he can count."))

story.append(Paragraph("<b>Paid Ads Starter  |  $3,497/mo stand-alone</b>", S["subsection"]))
story.append(b("Revenue is about $600K with two practice areas, so Essentials is hidden and Starter is the tier."))
story.append(b("Site is modern and fast (Lighthouse 88 mobile, 98 desktop), so ads-only fits and no rebuild is needed."))
story.append(b("Seller set this per Slack on Oct 19: ads-only, no coaching. Catalog says ads-only normally pairs with coaching. Confirm."))
story.append(b("Paid Ads Starter ad spend cap is $20,000/mo. The range sits inside it."))

story.append(thin_rule())

# ── Why the AI Avatar Add-On (replaces coaching block — no coaching in this proposal) ──
story.append(Paragraph("Why the AI Avatar Add-On", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Lets him test social video without being on camera himself."))
story.append(bd("Answers his interest in social media and Instagram video with no recurring commitment."))

story.append(Paragraph("<b>One-Time AI Avatar (kickoff + 5 videos)  |  $1,850 one-time</b>", S["subsection"]))
story.append(b("Needs Alexis approval before it goes in any proposal. Confirm first, or remove it from the report."))
story.append(b("Facebook shows the firm as banned. Fix account access before any video runs as a Meta ad."))
story.append(b("Roadmap: Phase 2 FCOO Advisor ($3,297) for admin. Phase 3 adds FCFO, bookkeeping, AI."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Totaro &amp; Shanahan — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Funds enough Google and LSA clicks to move Chapter 7 from about 2 a month toward 20 to 30."))
story.append(bd("Gives him numbers on what spend turns into cases, the base he said he does not have."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $4,500/mo, the bankruptcy Google PPC minimum."))
story.append(b("<b>Aggressive:</b> $14,000/mo, held at the 35% cap. The decision file said $18,000."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~6 cases x $2K = ~$12.5K/mo vs. $4.5K spend = 2.8x return."))
story.append(b("<b>Aggressive:</b> ~23 cases x $2K = ~$46K/mo vs. $14K spend = 3.3x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Uses his $2K Chapter 7 case value and a default 15% close rate. Chapter 11 not included.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Bankruptcy minimum: PPC $4,500 (only channel). $4,500 / $108 CPL ($90 mid + 20%) = ~42 leads x 15% = ~6 cases."))
story.append(b("<b>Aggressive:</b> $1.5M x 20% / 12 = $25,000. LA Tier 1 (1.5x) = $37,500. Minus $3,497 fee = $34,003, above the 35% cap, so held to $14,000."))
story.append(b("Mix at $14K: Google 50%, LSA 30%, Meta cold 15%, retargeting 5%. ~154 leads at about $91 each."))
story.append(b("Total spend at aggressive: $17,497/mo = 35.0% of ~$50K monthly revenue. At the 35% cap. Conservative: 16.0%."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I just don\'t have any idea what this should cost."', S["objection_q"]))
story.append(Paragraph("Show the range: $3,497/mo fee plus $4,500 to $14,000 of ad spend that goes to Google, not SMB Team. At $4,500 the estimate is about 6 Chapter 7 cases. That is the base he said he lacked. He was open to about $10K/mo.", S["objection_a"]))

story.append(Paragraph('"The last vendor only talked about where they could place us on Google."', S["objection_q"]))
story.append(Paragraph("This is paid ads, not rankings. It is judged on calls and signed cases. OakTree Law (357 reviews) already holds the top sponsored spot in LA and OC for Chapter 7.", S["objection_a"]))

story.append(Paragraph('"Referrals have worked for 30 years. Why change?"', S["objection_q"]))
story.append(Paragraph("Referrals feed Chapter 11, not Chapter 7. He gets about 2 Chapter 7s a month and wants 20 to 30. He also said that without referrals the firm would be out of business or scale back. Ads add a second source and leave referrals alone.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Paid Ads Starter</b>", S["price_main"]),
     Paragraph("$3,497/mo", S["price_main"])],
    [Paragraph("Google search ads, LSAs, Facebook and Instagram. Stand-alone rate, no bundle discount.", S["price_detail"]),
     Paragraph("stand alone", S["price_detail"])],
    [Paragraph("<b>One-Time AI Avatar (kickoff + 5 videos)</b>", S["price_main"]),
     Paragraph("$1,850 one-time", S["price_main"])],
    [Paragraph("Needs Alexis approval. Not part of the monthly total.", S["price_detail"]),
     Paragraph("one-time", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$4,500–$14,000/mo", S["price_main"])],
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
story.append(Paragraph(
    "Total: $3,497/mo + $4,500–$14,000 ad spend (+ $1,850 one-time)  |  No bundle savings  |  16.0%–35.0% of revenue (at the 35% cap)",
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
