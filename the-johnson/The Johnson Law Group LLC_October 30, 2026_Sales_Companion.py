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
OUTPUT_PATH = "the-johnson/The Johnson Law Group LLC_October 30, 2026_Sales_Companion.pdf"


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
story.append(Paragraph("The Johnson Law Group LLC", S["title"]))
story.append(Paragraph("Sales Companion  |  October 30, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("William Johnson", S["snap_value"]),
     Paragraph("~$300K+ (approx.)", S["snap_value"]),
     Paragraph("3 attorneys", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("Not stated (15% default)", S["snap_value"]),
     Paragraph("Greenbelt, MD", S["snap_value"])],
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
story.append(Paragraph("More profit without more hours, so he is home for his kids.", S["subsection"]))
# Use quote_block() for each. Separate with Spacer(1, 1).
story.append(quote_block("Increase in profit, but, like, not extracting too much time either."))
story.append(Spacer(1, 1))
story.append(quote_block("I got small children and, you know, sort of the work-life balance thing. Like, you know, still need to maintain that."))
story.append(Spacer(1, 1))
story.append(quote_block("if I can get six to eight, or six to ten, I would say, we'll be fine."))
story.append(Spacer(1, 2))
# Each bullet: bold lead phrase + one short sentence. One idea per bullet.
story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Steady retainer cases.</b> Six to ten a month instead of about two."))
story.append(bd("<b>Profit without the hours.</b> Growth that does not cost family time."))
story.append(bd("<b>A firm that stands on its own.</b> Succession without the founder's network."))
story.append(bd("<b>AI and marketing, soon.</b> He wants to start sooner rather than later."))

story.append(Spacer(1, 2))
# Each bullet: bold lead phrase + one short sentence. One idea per bullet.
story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Referral-only flow.</b> About two new clients a month, in hot and cold quarters."))
story.append(b("<b>A bad ad trial.</b> Ads ran well over cap and brought contingency leads."))
story.append(b("<b>Cost worry.</b> Budget is $6-8K (it depends); cost is his main concern."))
story.append(b("<b>The founder decides.</b> His father makes the calls and was not on the call."))
story.append(b("<b>Low urgency on intake.</b> He says intake is fine at today's volume."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))
# Transformation statements. What the package makes possible. Not deliverables.
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("A steady local lead source next to referrals, so slow quarters matter less."))
story.append(bd("Retainer-focused bankruptcy leads, not contingency cases that pay months later."))
story.append(bd("A website and listings that match the firm he wants to build."))
story.append(Paragraph("<b>Full Service Marketing — Essentials  |  $3,497/mo bundled</b>", S["subsection"]))
story.append(b("Lowest-cost Full Service tier; fits his $6-8K all-in budget."))
story.append(b("Starter ($4,997) leaves under $2K for ads; the minimum is $3,000."))
story.append(b("Essentials needs one practice area: scope to bankruptcy; confirm."))
story.append(b("Dated Wix site with mixed messaging, so Full Service over ads-only."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This AI Package", S["section"]))
# Transformation statements. What the package makes possible. Not deliverables.
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("AI handles follow-ups, status updates, drafts, and reminders."))
story.append(bd("Attorneys stay on bigger cases; a closer-to-autopilot practice area."))
story.append(Paragraph("<b>AI Workforce Pro – Starter (3 users)  |  $1,050/mo bundled</b>", S["subsection"]))
story.append(b("Three users at $350 each per month; Starter covers 1-4 users."))
story.append(b("Includes a weekly AI Implementation Session; 1M credits per user."))
story.append(b("AI-only ($1,050) is the fallback; confirm AI delivery capacity first."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph("Johnson Law Group — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts budget on bankruptcy searches from people ready to hire and pay a retainer."))
story.append(bd("Keeps spend under a firm monthly limit after the last trial ran over."))
story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000/mo — the minimum for any paid ads."))
story.append(b("<b>Aggressive:</b> $3,450/mo — the top of his budget after fees."))
# Use data from Scoping Guide: CPL benchmarks, close rate, avg case value
story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative (est.):</b> 3.9 cases x $1,750 = ~$6.8K/mo vs. $3.0K spend = 2.3x return."))
story.append(b("<b>Aggressive (est.):</b> 5.4 cases x $1,750 = ~$9.4K/mo vs. $3.45K spend = 2.7x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))
story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000 absolute minimum. Bankruptcy channel minimums (PPC $4,500 + LSA $2,000) exceed budget: paid ads team review."))
story.append(b("<b>Aggressive:</b> $8,000 budget ceiling minus $4,547 fees = $3,453, rounded to $3,450. The 20% rule on a ~$1M goal (~$16.7K) is out of budget."))
story.append(b("Blended CPL $96 (60% Google, 40% LSA), +20% on conservative; 15% close rate default; $1,750 case value. Total at aggressive: $7,997/mo = 32.0% of ~$25K monthly revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
# Each: red question (objection_q style) + gray response (objection_a style)
# Responses use specific data from the audit — competitor numbers, transcript quotes, etc.
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I need to run this by my father."', S["objection_q"]))
story.append(Paragraph("He said his father \"trusts my judgment.\" Offer a one-page founder summary and invite him to the Oct 30 call.", S["objection_a"]))

story.append(Paragraph('"Last time we spent almost double what we planned."', S["objection_q"]))
story.append(Paragraph("The trial planned $18K and spent about $30K. Now spend is a fixed $3,000-$3,450 a month, aimed at bankruptcy, with injury terms blocked.", S["objection_a"]))

story.append(Paragraph('"It really depends on the cost."', S["objection_q"]))
story.append(Paragraph("Fees $4,547 plus $3,000-$3,450 ads is $7,547-$7,997, inside his $6-8K. AI only is $1,050 a month, month-to-month.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Essentials</b>", S["price_main"]),
     Paragraph("$3,497/mo", S["price_main"])],
    [Paragraph("Website, local SEO, Google Ads, LSA, and social.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>AI Workforce Pro – Starter (3 users)</b>", S["price_main"]),
     Paragraph("$1,050/mo", S["price_main"])],
    [Paragraph("Three seats plus a weekly implementation session.", S["price_detail"]),
     Paragraph("No stand-alone price", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000–$3,450/mo", S["price_main"])],
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
    "Total: $4,547/mo + $3,000–$3,450 ad spend  |  Save $300/mo by bundling  |  30.2%–32.0% of revenue (under 35% cap)",
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
