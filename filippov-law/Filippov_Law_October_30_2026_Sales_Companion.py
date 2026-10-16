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

# FILL: Output path — use format [FirmName]_[MMDDYYYY]_Sales_Companion.pdf
OUTPUT_PATH = "filippov-law/Filippov_Law_October_30_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Filippov Law Group, PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  October 30, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Victoria Filippov Nemeth", S["snap_value"]),
     Paragraph("~$10K/mo now (was ~$100K/mo)", S["snap_value"]),
     Paragraph("Solo + contractors", S["snap_value"]),
     Paragraph("3", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Houston, TX", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: FREEDOM", S["section"]))
story.append(Paragraph("Victoria wants a firm that runs on its own with other people, so she can be the face of the business and do the legal work she likes.", S["subsection"]))

story.append(quote_block("I would like for the business to just kind of run on its own with other people where I'm not doing every type of day-in, day-out work."))
story.append(Spacer(1, 1))
story.append(quote_block("I'm not really doing the fun legal work I would like to do, I'm just running the firm, which is frustrating."))
story.append(Spacer(1, 1))
story.append(quote_block("I have the luxury of time right now... I want to build it out before I bring them in."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>A firm that runs without her.</b> Other people carry the day-to-day work."))
story.append(bd("<b>Five mid-sized retainer clients.</b> \"That's my goal\"; a flat-fee subscription model."))
story.append(bd("<b>Automation.</b> \"Interested in automating my work\"; wants to learn AI herself first."))
story.append(bd("<b>To be the face of the firm.</b> More of the high-level legal work."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Lost anchor client.</b> Revenue fell from about $100K to $10K a month; other clients were sold or restructured."))
story.append(b("<b>Work runs through her.</b> Contractors are \"asking for work\"; she has very little to give them."))
story.append(b("<b>No lead system.</b> Past business-development hires failed; the plan is in-person networking."))
story.append(b("<b>Weak local visibility.</b> Not in any of about 15 Houston searches; 17 reviews vs. 107-256."))
story.append(b("<b>Confidentiality worry.</b> \"A lot of confidential information would go in there.\""))

story.append(thin_rule())

story.append(Paragraph("Why No Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Keeps her limited cash on infrastructure first, which is her stated plan."))
story.append(bd("Matches the call: AI-led, no marketing, ads or website questions from her."))

story.append(Paragraph("<b>No Marketing Package  |  $0/mo</b>", S["subsection"]))
story.append(b("Call-purpose override: the call was about AI; she did not ask about marketing."))
story.append(b("Seller override (Slack, 10/16/26): marketing and ad spend removed."))
story.append(b("Lead-gen gap is real (\"need new clients\"); revisit after the proposal call."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives her structure to build roles and handoffs so work moves to contractors."))
story.append(bd("Monthly 1:1 call to build the flat-fee offer and first-call-to-retainer path."))

story.append(Paragraph("<b>Coach Essentials Plus  |  $2,497/mo standalone</b>", S["subsection"]))
story.append(b("Sold standalone, so no bundle discount ($0 savings); the $1,997 bundled rate needs marketing."))
story.append(b("Normal band is $250K-$400K revenue; she is below it. Confirm intent and term with sales."))
story.append(b("On the call, coaching was suggested with no product or price named; she said \"Absolutely.\""))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Filippov Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This AI Package (Not Ad Spend)", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Moves repeatable work off her desk without her building every skill alone."))
story.append(bd("Keeps her in control: she wanted to learn AI herself before hiring anyone."))

story.append(Paragraph("<b>AI Workforce Pro - Starter (1 user)  |  $350/mo</b>", S["subsection"]))
story.append(b("Month-to-month; 1M AI credits per user; weekly AI Implementation Session."))
story.append(b("No standalone price exists; do not quote a discount. She asked \"Is it monthly? Can you cancel?\""))
story.append(b("Fractional CTO was mentioned with no level named; not in this proposal."))
story.append(b("1 seat assumed (team size not stated). Confirm seat count and LAW launch capacity."))

story.append(Paragraph("<b>No ROI projection built.</b>", S["subsection"]))
story.append(b("No marketing or ads package is in the recommendation, so Block 4 was removed."))
story.append(b("Her numbers if asked: goal is five retainer clients; case value and close rate not stated."))
story.append(Paragraph("<i>Any return talk is an estimate only. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>Flags for scoping:</b>", S["subsection"]))
story.append(b("Revenue under $300K and under $250K: scoping approval, confirm 4 months of funds (about $11,388)."))
story.append(b("Package is about 28.5% of current monthly revenue (35% cap passes); consider $350 AI-only fallback."))
story.append(b("Yelp may show a different address; Google Ads, LSA and competitor Meta ads not verified."))

story.append(thin_rule())

story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"There\'s a lot of confidential information that would go in there."', S["objection_q"]))
story.append(Paragraph("On the call she was told it is a closed platform, SOC2, with no training on client data. Have the written security details ready and promise nothing beyond them. She is holding some integrations back for privacy.", S["objection_a"]))

story.append(Paragraph('"I wanted to learn it myself versus hiring someone to do it."', S["objection_q"]))
story.append(Paragraph("That is why this is Starter, not a Fractional CTO. She keeps control. She called building skills herself \"just kind of painful,\" so pre-built skills and a weekly session save her time.", S["objection_a"]))

story.append(Paragraph('"Revenue is down to about $10,000 a month. Can I afford this?"', S["objection_q"]))
story.append(Paragraph("Be direct: the AI seat is $350 and month-to-month. Coaching is the larger cost, so tie it to her goal of five retainer clients. If budget is tight, offer AI-only first.", S["objection_a"]))

story.append(Paragraph('"I am going to network in person, not market."', S["objection_q"]))
story.append(Paragraph("Agree. This plan builds the offer and systems first, as she wants. Free fixes remain: her 17 five-star reviews, a form above the fold, and exit-planning pages.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>No Marketing Package</b>", S["price_main"]),
     Paragraph("$0/mo", S["price_main"])],
    [Paragraph("Per the AI-led call and the seller override.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>Coach Essentials Plus</b>", S["price_main"]),
     Paragraph("$2,497/mo", S["price_main"])],
    [Paragraph("Sold standalone; no bundle discount applies.", S["price_detail"]),
     Paragraph("$2,497 stand-alone", S["price_detail"])],
    [Paragraph("<b>AI Workforce Pro - Starter (1 user)</b>", S["price_main"]),
     Paragraph("$350/mo", S["price_main"])],
    [Paragraph("Month-to-month; no standalone price exists.", S["price_detail"]),
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
    "Total: $2,847/mo  |  No bundle savings  |  28.5% of current monthly revenue (under 35% cap)",
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
