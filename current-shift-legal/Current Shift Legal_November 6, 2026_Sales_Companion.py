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

OUTPUT_PATH = "current-shift-legal/Current Shift Legal_November 6, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Current Shift Legal", S["title"]))
story.append(Paragraph("Sales Companion  |  November 6, 2026  |  Rep: Nick Holderman", S["subtitle"]))
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
    [Paragraph("Jacqueline Radebaugh", S["snap_value"]),
     Paragraph("~$1.2M", S["snap_value"]),
     Paragraph("~9 on site", S["snap_value"]),
     Paragraph("4", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Remote (Boulder, CO HQ)", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: TIME AND MARGIN", S["section"]))
story.append(Paragraph("She wants a leaner, higher-margin firm that grows without adding headcount, with her team's time freed for creative work.", S["subsection"]))

story.append(quote_block("so that we're not spending time on things that can be automatized and then we can use our brains for more creative stuff."))
story.append(Spacer(1, 1))
story.append(quote_block("I don't want us to ... be hiring more people ... without increasing profit margin. I don't need to have 20 attorneys to grow."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Intake on autopilot.</b> Only the 30-minute call needs a human."))
story.append(bd("<b>Scheduling and reporting automated.</b> No more dashboards built by hand in Excel."))
story.append(bd("<b>Matter follow-up that never lapses.</b> Quiet matters surface on their own."))
story.append(bd("<b>Margin, not headcount.</b> More billable time without hiring."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Manual operations.</b> Intake, scheduling, and reporting run by hand across separate tools."))
story.append(b("<b>Stretched team.</b> Attorneys bill about 40% yet feel at their limit."))
story.append(b("<b>No follow-up process.</b> Nothing makes sure clients get regular check-ins."))
story.append(b("<b>Thin ops bench.</b> One role covers assistant, client experience, and marketing."))

story.append(thin_rule())

# ── Why This AI Package (replaces Marketing section: no marketing recommended) ──
story.append(Paragraph("Why This AI Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives her team an AI workspace instead of another assistant hire."))
story.append(bd("Puts pre-built legal skills to work on intake and follow-up, with weekly support."))

story.append(Paragraph("<b>AI Workforce Pro – Starter (1 user)  |  $350/mo bundled</b>", S["subsection"]))
story.append(b("The call was about AI and automation. She stated no lead-gen need."))
story.append(b("Seat count was not stated. Priced at 1 user; Starter covers 1 to 4 users. Confirm."))
story.append(b("5+ users moves to AI Workforce Pro at $1,597/mo. Site lists nine people."))
story.append(b("Her custom asks (LeanLaw and QuickBooks dashboards) are Fractional CTO scope. Confirm fit on the Nov 6 call."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Turns \"grow margin, not headcount\" into a plan with numbers."))
story.append(bd("Gives her a pricing and scoping playbook for the move to fixed fees."))
story.append(bd("Adds weekly accountability and peer masterminds for a lean leadership team."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue is about $1.2M. Team size was not stated; the file assumed under 5."))
story.append(b("She did not ask for coaching. Tie it to margin and the hourly-to-fixed-fee shift."))
story.append(b("Master's Circle ($4,600/mo) only fits a team of 5+ with dedicated staff. Confirm headcount."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Current Shift Legal — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Marketing or Ad Spend (replaces Ad Spend section) ──
story.append(Paragraph("Why No Marketing or Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Keeps the plan on her stated need: automation, not more leads."))
story.append(bd("Protects team capacity. Referrals are already \"getting out of hand a little bit.\""))

story.append(Paragraph("<b>Why marketing is left out:</b>", S["subsection"]))
story.append(b("About 70 to 90% of clients come by referral, and she named no lead-gen gap."))
story.append(b("No marketing vendor was mentioned. The website is brand new (Sept to Oct 2026)."))
story.append(b("Google profile, ads, LSA, and Meta data could not be observed. Do not claim gaps on the call."))
story.append(b("Marketing is a later talk, once intake can absorb more volume."))
story.append(Paragraph("<i>No ad spend or ROI projection: no marketing package is in this proposal.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"That is a lot for a super small team."', S["objection_q"]))
story.append(Paragraph("Total is $3,550/mo, about 3.6% of her ~$1.2M revenue. It is far below the $10K to $12K/mo custom range you called overkill. She has also weighed a tool against hiring another assistant.", S["objection_a"]))

story.append(Paragraph('"Will it connect LeanLaw and QuickBooks?"', S["objection_q"]))
story.append(Paragraph("Be straight: Starter is the workspace, pre-built skills, and a weekly session. Custom integrations are Fractional CTO scope. Walk it through with the CTO on the Nov 6 call. The report promises no custom builds.", S["objection_a"]))

story.append(Paragraph('"I did not ask about coaching."', S["objection_q"]))
story.append(Paragraph("True. Tie it to her words: attorneys bill about 40%, and she is shifting from hourly to fixed fees and wants to understand that process. Coaching plans margin and pricing so automation turns into profit.", S["objection_a"]))

story.append(Paragraph('"I need to know the goals can be reached first."', S["objection_q"]))
story.append(Paragraph("She said the budget is worthwhile if she is confident the goals can be reached. Agree on one measure: billable share rises with the same or more clients, as her team put it.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>AI Workforce Pro – Starter (1 user)</b>", S["price_main"]),
     Paragraph("$350/mo", S["price_main"])],
    [Paragraph("Managed AI workspace, pre-built legal skills, weekly implementation session.", S["price_detail"]),
     Paragraph("Per-user price, no stand-alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, 1:1 accountability, masterminds, profit planning.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("None", S["price_main"])],
    [Paragraph("No marketing package in this proposal.", S["price_detail"]),
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
    "Total: $3,550/mo  |  Save $297/mo by bundling  |  3.6% of stated revenue (under 35% cap)",
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
