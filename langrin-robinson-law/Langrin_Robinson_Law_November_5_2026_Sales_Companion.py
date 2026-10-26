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

OUTPUT_PATH = "langrin-robinson-law/Langrin_Robinson_Law_November_5_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Langrin-Robertson Law, LLC", S["title"]))
story.append(Paragraph("Sales Companion  |  November 5, 2026  |  Rep: Dan Bryant", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Hazel Langrin-Robertson", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("4", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Snellville, GA", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: TIME (inferred)", S["section"]))
story.append(Paragraph("Hazel was not on the call; her helper wants systems set so the firm runs and Hazel gets time back.", S["subsection"]))

story.append(quote_block("I'll tell you right now, she works six days a week."))
story.append(Spacer(1, 1))
story.append(quote_block("The staff that we wind up hiring can take over, and it's already set. It's ready to go. I don't have to retrain somebody on whatever."))
story.append(Spacer(1, 1))
story.append(quote_block("I need to know how many different things that I need to get her out of that this can replace."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What the firm wants:</b>", S["subsection"]))
story.append(bd("<b>Time back for Hazel.</b> Fewer hours in email and admin."))
story.append(bd("<b>One hub.</b> Projects, schedules, content, and email in one place."))
story.append(bd("<b>Set SOPs.</b> New hires take over without being retrained."))
story.append(bd("<b>Right people.</b> A strong case manager and fewer hiring misses."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping them:</b>", S["subsection"]))
story.append(b("<b>Owner not on the call.</b> The helper spoke for Hazel and says \"I am not the attorney.\""))
story.append(b("<b>Staff are not technical.</b> \"They do not know AI.\""))
story.append(b("<b>Turnover.</b> Case manager role; Hazel is wary of hiring full-time."))
story.append(b("<b>Helper is temporary.</b> She wants to set it up, then step back."))
story.append(b("<b>Past vendor burn.</b> A $2,000/mo vendor was cut off for quality."))

story.append(thin_rule())

story.append(Paragraph("Why This AI Workforce Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("One AI workspace replaces several separate tools."))
story.append(bd("AI staff take on email, calendar, and follow-up triage."))
story.append(bd("A weekly session helps non-technical staff learn it."))

story.append(Paragraph("<b>AI Workforce Pro, 5 users  |  $1,597/mo bundled</b>", S["subsection"]))
story.append(b("Matches the AI-led call. The helper said to \"buy that 5, that 5-team package.\""))
story.append(b("Team is 4 people. Extra users are $120/mo each. Yearly contract."))
story.append(b("No stand-alone price, so no savings shown. Starter option: $350/user/mo."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("A coach and peer group help build SOPs once, for every hire."))
story.append(bd("Hiring and delegation support targets the case manager gap."))
story.append(bd("It builds the structure so the firm needs Hazel less."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Seller override (Slack, 2026-10-26). Not discussed by name on the call."))
story.append(b("Stand-alone is $3,497/mo, so bundling saves $297/mo."))
story.append(b("Table fit is $400K-$1M. HubSpot band is $180K-$960K. Confirm revenue."))

# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Langrin-Robertson Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why There Is No Ad Spend", S["section"]))

story.append(Paragraph("<b>What this does for her:</b>", S["subsection"]))
story.append(bd("The proposal stays on what the call was about: AI, SOPs, and time back."))
story.append(bd("It avoids selling marketing with no stated lead-gen gap."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> None. No marketing or ads package is recommended."))
story.append(b("<b>Aggressive:</b> None. Nobody asked for leads, ads, SEO, or a new website."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("Not calculated. There is no ad spend, so there is no ROI projection."))
story.append(Paragraph("<i>Marketing can be revisited later if Hazel asks about lead generation.</i>", S["disclaimer"]))

story.append(Paragraph("<b>Cap check and approvals:</b>", S["subsection"]))
story.append(b("<b>35% cap:</b> $4,797/mo is 32.0% of revenue at $180K and 10.1% at $570K. Under the cap."))
story.append(b("<b>Revenue under $300K:</b> scoping approval needed. Under $250K, confirm 4 months of funds."))
story.append(b("<b>LAW:</b> confirm LAW delivery has launched and capacity is open before sending."))
story.append(b("<b>Reviews and PageSpeed:</b> unconfirmed or not obtained. Verify Google live before the call."))
story.append(b("<b>Name:</b> report says Langrin-Robertson (real site). Trigger said Robinson. Confirm."))

story.append(thin_rule())

story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"Hazel needs to see this before we decide."', S["objection_q"]))
story.append(Paragraph("Fair. The helper is not the attorney and was not the decision maker. Ask for Hazel on the Nov 5 call, or a short follow-up with her.", S["objection_a"]))

story.append(Paragraph('"How many different things can this replace?"', S["objection_q"]))
story.append(Paragraph("She raised project, schedule, content, and email tools on the call. Ask which tools Hazel pays for today, then map each one to the workspace.", S["objection_a"]))

story.append(Paragraph('"Why coaching if we came for AI?"', S["objection_q"]))
story.append(Paragraph("The call raised SOPs, turnover, and hiring. AI cannot fix those alone. If budget is tight, AI Workforce Pro alone is $1,597/mo.", S["objection_a"]))

story.append(Paragraph('"She will need to see results immediately."', S["objection_q"]))
story.append(Paragraph("Promise no outcomes. Start with email triage and one SOP, which she called an hour or two a day. Confirm security and role access in writing.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>AI Workforce Pro, 5 users</b>", S["price_main"]),
     Paragraph("$1,597/mo", S["price_main"])],
    [Paragraph("Managed AI workspace and a weekly implementation session.", S["price_detail"]),
     Paragraph("No stand-alone price", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, masterminds, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("None", S["price_main"])],
    [Paragraph("No marketing or ads package is part of this recommendation.", S["price_detail"]),
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
    "Total: $4,797/mo  |  Save $297/mo by bundling  |  10.1% of revenue at $570K, 32.0% at $180K (35% cap)",
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
