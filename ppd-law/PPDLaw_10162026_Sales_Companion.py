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

OUTPUT_PATH = "ppd-law/PPDLaw_10162026_Sales_Companion.pdf"


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

story.append(Paragraph("PPD Law (PPD Law Office)", S["title"]))
story.append(Paragraph("Sales Companion  |  October 16, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Premmal Patel-David", S["snap_value"]),
     Paragraph("~$500K (stated)", S["snap_value"]),
     Paragraph("4 (owner + 3)", S["snap_value"]),
     Paragraph("4", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Brandon, MB (Canada)", S["snap_value"])],
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
story.append(Paragraph("A firm that runs without constant owner involvement, so there is time for other ventures.", S["subsection"]))

# The call record is a Fathom AI summary, not a verbatim transcript — lines below are summary text.
story.append(quote_block("[Summary, not verbatim] Evolve from 'Small Business Manager' to 'Wealth Multiplier' (true CEO) to gain time for other ventures."))
story.append(Spacer(1, 1))
story.append(quote_block("[Summary, not verbatim] Double revenue to $1M by 2027, but not at the expense of health or work-life balance."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What Premmal wants:</b>", S["subsection"]))
story.append(bd("<b>Time back.</b> Move from Small Business Manager to Wealth Multiplier with time for other ventures."))
story.append(bd("<b>A firm that runs without them.</b> Operations should not stop when the owner is away."))
story.append(bd("<b>Less training load.</b> Newer staff need less of the owner's day."))
story.append(bd("<b>Double to $1M by 2027.</b> Growth must stay sustainable for the owner."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping Premmal:</b>", S["subsection"]))
story.append(b("<b>Owner dependence.</b> The firm is entirely dependent on Premmal."))
story.append(b("<b>Training burden.</b> About 20% of the day goes to training inexperienced staff."))
story.append(b("<b>Thin hiring pool.</b> Trained staff are hard to find, so new grads are hired."))
story.append(b("<b>Full capacity.</b> Intake is 3-8 new files a month and there is no room for more."))
story.append(b("<b>No profit plan described.</b> Flat-fee and hourly work, with margins not discussed."))

story.append(thin_rule())

# ── Why This AI Package (replaces marketing section — no marketing recommended) ──
story.append(Paragraph("Why This AI Package", S["section"]))

story.append(Paragraph("<b>What it does for Premmal:</b>", S["subsection"]))
story.append(bd("Newer staff get AI-drafted first passes and research, reviewed by a human."))
story.append(bd("Training takes less of the owner's day as AI handles repeatable work."))
story.append(bd("All four team members share one AI workspace to learn on."))

story.append(Paragraph("<b>AI Workforce Pro - Starter (4 users)  |  $1,400/mo ($350/user)</b>", S["subsection"]))
story.append(b("Team size is 4, so Starter (1-4 users) fits; 5+ users moves to AI Workforce Pro at $1,597/mo."))
story.append(b("Month-to-month, 1M AI credits per user, weekly AI Implementation Session."))
story.append(b("Seller-set package (Slack, Oct 22). There is no stand-alone price for this product."))
story.append(b("Self-implemented tier. If Premmal lacks bandwidth, Fractional CTO Level 1 ($3,297/mo) has an fCTO lead it."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for Premmal:</b>", S["subsection"]))
story.append(bd("A coach and accountability to build delegation and written systems."))
story.append(bd("The firm learns to run on process, not on the owner's memory."))
story.append(bd("Peer masterminds show how other firms made the move to CEO."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,497/mo stand-alone (no marketing bundle)</b>", S["subsection"]))
story.append(b("Revenue of ~$500K sits in the $400K-$1M band, which calls for Elite Coach Plus."))
story.append(b("Under 5 team members, so Master's Circle is not available."))
story.append(b("Bundled price of $3,200 only applies with a marketing package, so none is shown."))
story.append(b("Includes weekly group coaching, masterminds, virtual quarterly and one in-person workshop."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("PPD Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Ad Spend (replaces ad spend section — no marketing recommended) ──
story.append(Paragraph("Why No Ad Spend (Yet)", S["section"]))

story.append(Paragraph("<b>What this does for Premmal:</b>", S["subsection"]))
story.append(bd("Keeps the proposal on the problem raised: owner dependence."))
story.append(bd("Avoids adding more leads to a firm already at full capacity."))

story.append(Paragraph("<b>Marketing position:</b>", S["subsection"]))
story.append(b("<b>No marketing in this proposal.</b> The call was about ops, AI, and coaching, with no lead-gen gap."))
story.append(b("<b>No vendor or budget limit raised.</b> Capacity is full at 3-8 files a month."))
story.append(b("<b>First marketing gap later:</b> immigration, absent from 3 of 3 map searches; Shivay has 240 reviews vs PPD's 59."))

story.append(Paragraph("<b>Estimated return:</b>", S["subsection"]))
story.append(b("No ads recommended, so no ad ROI is projected."))
story.append(b("The return is time: about 20% of the owner's day is roughly one workday a week."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>Checks before the call:</b>", S["subsection"]))
story.append(b("Total SMB spend is $4,897/mo = 11.8% of monthly revenue ($41,667). Under the 35% cap."))
story.append(b("PageSpeed 43 mobile / 71 desktop are local Lighthouse lab scores. Re-check on PSI."))
story.append(b("Confirm LAW delivery has launched and has capacity before sending the proposal."))

story.append(thin_rule())

# ── If Premmal Pushes Back ──
story.append(Paragraph("If Premmal Pushes Back", S["section"]))

story.append(Paragraph('"Is AI good enough for legal work?"', S["objection_q"]))
story.append(Paragraph("A human reviews every output. Starter is month-to-month, so the team can try four seats with a weekly implementation session.", S["objection_a"]))

story.append(Paragraph('"I do not have time to roll this out."', S["objection_q"]))
story.append(Paragraph("Coaching plus the weekly session keeps it small. If bandwidth is the limit, Fractional CTO Level 1 ($3,297/mo) is led by an fCTO.", S["objection_a"]))

story.append(Paragraph('"I want to grow to $1M. Why no marketing?"', S["objection_q"]))
story.append(Paragraph("Capacity is full at 3-8 files a month. More leads now add load. Immigration is the first marketing step once the team can absorb it.", S["objection_a"]))

story.append(Paragraph('"$4,897 a month is a lot at $500K."', S["objection_q"]))
story.append(Paragraph("It is 11.8% of monthly revenue, and training alone costs about a workday a week of the owner's time.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,497/mo", S["price_main"])],
    [Paragraph("Weekly coaching, masterminds, workshops, and accountability.", S["price_detail"]),
     Paragraph("stand alone, no bundle", S["price_detail"])],
    [Paragraph("<b>AI Workforce Pro - Starter (4 users)</b>", S["price_main"]),
     Paragraph("$1,400/mo", S["price_main"])],
    [Paragraph("4 users x $350/user/mo, month-to-month.", S["price_detail"]),
     Paragraph("no stand-alone price", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("None", S["price_main"])],
    [Paragraph("No marketing package or ad spend in this proposal.", S["price_detail"]),
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
    "Total: $4,897/mo  |  No bundle savings apply  |  11.8% of monthly revenue (under 35% cap)",
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
