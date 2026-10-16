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

OUTPUT_PATH = "boeshaar-law/Boeshaar Law_October 16, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Boeshaar Law", S["title"]))
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
    [Paragraph("Bob Boeshaar", S["snap_value"]),
     Paragraph("~$500K", S["snap_value"]),
     Paragraph("3 (+1 contract)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("~50%", S["snap_value"]),
     Paragraph("Seattle, WA", S["snap_value"])],
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
story.append(Paragraph("Bob wants a firm that runs without him so he can take real time off with his family.", S["subsection"]))

story.append(quote_block("the business side is dependent on me. So I can take like a week off and everything runs fine and they don't need me."))
story.append(Spacer(1, 1))
story.append(quote_block("ideally I'd like to do maybe a 10-hour workweek, something like that, so a quarter time."))
story.append(Spacer(1, 1))
story.append(quote_block("more time for my family, less stress. I'm able to do some volunteer work."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Time back.</b> A week off first, then 30 days, and a roughly 10-hour workweek."))
story.append(bd("<b>The CEO seat.</b> He wants to set the vision, not answer email."))
story.append(bd("<b>AI that works.</b> He booked because he wants AI to raise his productivity."))
story.append(bd("<b>A bigger firm.</b> An associate by June and $2M gross in 2-3 years."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>He is the bottleneck.</b> At least half of his 40-hour week is work others could do."))
story.append(b("<b>Email overload.</b> Two to three hours a day for Bob, about two more for staff."))
story.append(b("<b>Behind on client work.</b> A letter was missed before a deadline."))
story.append(b("<b>Cash crunches.</b> He wants uneven cash flow evened out."))
story.append(b("<b>DIY habit.</b> He has been \"thinking of doing it myself.\""))

story.append(thin_rule())

# ── Why This AI Package ──
story.append(Paragraph("Why This Legal AI Workforce Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Moves email and first drafts off his desk so he gets hours back."))
story.append(bd("Turns his AI experiments into one system for the team."))
story.append(bd("A weekly working session makes AI a daily habit, not a side project."))

story.append(Paragraph("<b>AI Workforce Pro – Starter (3 seats)  |  $1,050/mo bundled</b>", S["subsection"]))
story.append(b("The call was AI-led: he booked for AI Workforce Pro (00:01:37)."))
story.append(b("Starter (1-4 users): 3 seats x $350/mo. Month-to-month. No stand-alone price."))
story.append(b("Seat count assumed from team of 3. Confirm who gets seats."))
story.append(b("Confirm LAW delivery has launched and has capacity before sending."))

story.append(thin_rule())

# ── Why This Operations Package ──
story.append(Paragraph("Why This Operations Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the roles and handoffs so decisions stop routing back to Bob."))
story.append(bd("Plans the associate hire and onboarding ahead of the June target."))
story.append(bd("Turns a week off, then 30 days, into a plan instead of a hope."))

story.append(Paragraph("<b>FCOO Advisor  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Seller override (Slack, 10/14): replaces Starter marketing + Elite Coach Plus."))
story.append(b("Stand-alone is $3,797. Bundling saves $500/mo."))
story.append(b("Revenue is about $500K, the FCOO floor. Confirm it."))
story.append(b("Includes group coaching. Bob is in CRISP, so pitch it as ops, not coaching."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Boeshaar Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Marketing Or Ad Spend ──
story.append(Paragraph("Why No Marketing Or Ad Spend", S["section"]))

story.append(Paragraph("<b>What this does for him:</b>", S["subsection"]))
story.append(bd("Gets his capacity back before adding more leads to a full desk."))
story.append(bd("Leaves marketing for when the associate is hired, as you told him on the call."))

story.append(Paragraph("<b>Why it is left out:</b>", S["subsection"]))
story.append(b("<b>CRISP is active.</b> He is about 5 months into a roughly 18-month term (00:07:12-00:07:47)."))
story.append(b("<b>You set the order.</b> Marketing \"can be down the line to bring in that new hire\" (00:19:02)."))
story.append(b("<b>He is stretched.</b> \"I'm kind of overwhelmed, but I want more\" (00:05:41)."))
story.append(b("<b>Demand exists.</b> About 60% of leads come from Google and AI, about 25 leads a month, half qualified, about half of those sign."))
story.append(b("No ad spend, ROI projection, or ad-range math applies. Total spend is $4,347/mo, 10.4% of monthly revenue."))

story.append(Paragraph("<b>Free wins to lead with now:</b>", S["subsection"]))
story.append(bd("Switch Google hours to match the 7-day answering service."))
story.append(bd("Start a review-request routine. Review counts are unconfirmed, so verify live first."))
story.append(Paragraph("<i>No competitor ad, LSA, or 3-pack data was observed. Do not cite any.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I\'d rather just do the AI myself."', S["objection_q"]))
story.append(Paragraph("He already built email and case-letter agents, yet email still takes 2-3 hours a day and he is behind. Team seats plus a weekly session make it a system, not a side project.", S["objection_a"]))

story.append(Paragraph('"I\'m already in CRISP. I have a coach."', S["objection_q"]))
story.append(Paragraph("Nothing here replaces CRISP, and no marketing is proposed. The FCOO builds roles, accountability, and handoffs. Group coaching comes with it but is not the point.", S["objection_a"]))

story.append(Paragraph('"We have a lot of cash crunches. Can I afford this?"', S["objection_q"]))
story.append(Paragraph("Total is $4,347/mo, about 10% of monthly revenue, under the 35% cap. The AI seats are month-to-month at $1,050/mo, the lowest-commitment piece.", S["objection_a"]))

story.append(Paragraph('"I need more leads, not more operations."', S["objection_q"]))
story.append(Paragraph("He said \"I know I need to increase volume,\" but he is behind today. New leads land on the same bottleneck. Marketing fits once the associate is hired.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>AI Workforce Pro – Starter (3 seats)</b>", S["price_main"]),
     Paragraph("$1,050/mo", S["price_main"])],
    [Paragraph("3 seats x $350/user/mo. Month-to-month.", S["price_detail"]),
     Paragraph("no stand-alone price", S["price_detail"])],
    [Paragraph("<b>FCOO Advisor</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Fractional COO leadership plus group coaching.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("None", S["price_main"])],
    [Paragraph("Marketing is not part of this proposal.", S["price_detail"]),
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
    "Total: $4,347/mo  |  Save $500/mo by bundling  |  10.4% of monthly revenue (under 35% cap)",
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
