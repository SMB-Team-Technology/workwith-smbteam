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

OUTPUT_PATH = "truce-resolutions/Truce_Resolutions_December_1_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Truce Resolutions, PC", S["title"]))
story.append(Paragraph("Sales Companion  |  December 1, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
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
    [Paragraph("Tamara Arnold", S["snap_value"]),
     Paragraph("~$200K-$250K (2026 proj.)", S["snap_value"]),
     Paragraph("Solo + 1 part-time", S["snap_value"]),
     Paragraph("3", S["snap_value"]),
     Paragraph("100% (stated, in-meeting)", S["snap_value"]),
     Paragraph("Solvang, CA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM + COMMUNITY", S["section"]))
story.append(Paragraph("Tamara wants a firm that runs without her doing everything, so she can step in and out and be the go-to estate planner in her town.", S["subsection"]))

story.append(quote_block("I can step in and out and just do the presentations and the meetings with high value clients and then offload everything else to staff."))
story.append(Spacer(1, 1))
story.append(quote_block("I'm just trying to be the go-to attorney in my community."))
story.append(Spacer(1, 1))
story.append(quote_block("I don't need an empire."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>More people in the door.</b> \"I need butts in seats\" - she closes once they are in front of her."))
story.append(bd("<b>A plan that fits her town.</b> A marketing strategy for a small budget, not a big agency retainer."))
story.append(bd("<b>A team behind her.</b> 1-2 junior associates, a paralegal, a caseworker."))
story.append(bd("<b>A right-sized firm.</b> $250-300K in 2027, about $1M by 2029, then decide on the pace."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Grassroots only.</b> Presentations, referrals and word of mouth; $0 spent on marketing."))
story.append(b("<b>Weak local visibility.</b> Not in organic local results on the call; GBP category says General Law Firm."))
story.append(b("<b>Small review base.</b> Rep read about 7 Google reviews on the call (unconfirmed; verify live)."))
story.append(b("<b>Solo capacity.</b> She is attorney, presenter, marketer and intake; \"you can never turn it off.\""))
story.append(b("<b>Tight budget.</b> $2,000-$3,000/mo total, ad spend included; no more website spend."))

story.append(thin_rule())

# ── Why No Marketing Package ──
story.append(Paragraph("Why No Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Keeps her limited budget out of a managed retainer she said she cannot afford yet."))
story.append(bd("Matches the call: coaching plus self-run Local Service Ads, no teardown, no website rebuild."))

story.append(Paragraph("<b>No Marketing Package  |  $0/mo</b>", S["subsection"]))
story.append(b("Rep advised her on the call to run LSAs herself instead of a ~$1,000/mo managed add-on."))
story.append(b("Budget-Reality Override: Essentials marketing ($3,497/mo) exceeds her stated budget."))
story.append(b("Seller override (Slack, 10/16/26): marketing removed, Coach Essentials Plus only."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives her the written plan, structure and accountability she said she is missing."))
story.append(bd("Monthly 1:1 call to sequence her first hires and hand-offs toward a team."))

story.append(Paragraph("<b>Coach Essentials Plus  |  $2,497/mo standalone</b>", S["subsection"]))
story.append(b("Rep quoted about $2,500/mo on a 12-month term; tier not named (Plus vs Elite Coach) - confirm Plus."))
story.append(b("Sold standalone - no marketing to bundle against, so no bundle discount ($0 savings)."))
story.append(b("Leaves about $500/mo of her $2,000-$3,000 budget for self-run LSAs."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Truce Resolutions — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Ad Spend Package ──
story.append(Paragraph("Why No Managed Ad Spend (Self-Run LSAs)", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Lets her test pay-per-lead Local Service Ads cheaply while she builds a plan."))
story.append(bd("Puts a Solvang-based firm against LSA advertisers who only list the town as a service area."))

story.append(Paragraph("<b>Self-Managed LSA Budget (not sold, goes to Google):</b>", S["subsection"]))
story.append(b("<b>Rep guidance:</b> start at $1,000-$2,000/mo, pay per lead, run it herself."))
story.append(b("<b>Her math:</b> $2,497 coaching leaves about $500/mo; she may do more in a couple of months."))

story.append(Paragraph("<b>No ROI projection built.</b>", S["subsection"]))
story.append(b("No marketing/ads package is in the recommendation, so Block 4 was removed from the report."))
story.append(b("Her numbers if asked: ~$6,000 avg case, 3-4 clients/mo now, needs 6-7/mo for $250K."))
story.append(Paragraph("<i>Any LSA return talk is an estimate only. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>Flags for scoping:</b>", S["subsection"]))
story.append(b("Revenue under $300K and under $250K: scoping approval, confirm 4 months of funds (~$9,988)."))
story.append(b("Review counts unconfirmed. Verify live before the call. Competitor counts not obtained."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I\'m already paying about $2,000 a month for Ali\'s program and I can\'t jump out of it."', S["objection_q"]))
story.append(Paragraph("Do not ask her to leave it. Her program licenses her legal materials; this plan covers what she said it lacks: \"not like a full plan in place\" for marketing. Position this as the marketing plan and accountability layer, not a replacement.", S["objection_a"]))

story.append(Paragraph('"I don\'t have the budget for another $2,500 a month."', S["objection_q"]))
story.append(Paragraph("It is the smallest coaching program the rep quoted, about 12-15% of her revenue. At about $6,000 a client, one extra signed client a month covers it. Confirm she is comfortable with the roughly $500 left for LSAs.", S["objection_a"]))

story.append(Paragraph('"Can\'t I just do this myself with the GBP and review fixes you showed me?"', S["objection_q"]))
story.append(Paragraph("Yes, those fixes are free and we want her to do them. The gap is a plan and accountability: she told us \"I just don't ask\" for reviews and has tried no paid channel yet. Lawvex already runs LSAs and workshops in Solvang.", S["objection_a"]))

story.append(Paragraph('"I need to see the program details before I decide."', S["objection_q"]))
story.append(Paragraph("She asked for details and cost before the Dec 1 call. Walk her through weekly group sessions, the monthly 1:1 call, the written plan, and the 12-month term with a 3-month check on results.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>No Marketing Package</b>", S["price_main"]),
     Paragraph("$0/mo", S["price_main"])],
    [Paragraph("Self-run LSAs instead, per the call and the seller override.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>Coach Essentials Plus</b>", S["price_main"]),
     Paragraph("$2,497/mo", S["price_main"])],
    [Paragraph("Sold standalone - no bundle discount applies.", S["price_detail"]),
     Paragraph("$2,497 stand-alone", S["price_detail"])],
    [Paragraph("<b>Self-Managed LSA Budget (to Google)</b>", S["price_main"]),
     Paragraph("~$500/mo (her math)", S["price_main"])],
    [Paragraph("Not sold by SMB Team; her choice inside her $2,000-$3,000 budget.", S["price_detail"]),
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
    "Total: $2,497/mo  |  No bundle savings  |  12%-15% of revenue (under 35% cap)",
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
