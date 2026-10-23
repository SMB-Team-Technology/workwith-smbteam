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

OUTPUT_PATH = "allied-defense-law/Allied Defense Law_November 3, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Allied Defense Law", S["title"]))
story.append(Paragraph("Sales Companion  |  November 3, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Rebecca Montoya", S["snap_value"]),
     Paragraph("~$250K this year (her words)", S["snap_value"]),
     Paragraph("Solo", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Phoenix, AZ", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: CAPACITY WITHOUT STAFF", S["section"]))
story.append(Paragraph("She wants to take on more cases without hiring people or becoming a bigger firm.", S["subsection"]))

story.append(quote_block("I don't have any aspirations to like grow and like hire more attorneys and everything, but I think that I could take on more cases if I had, you know, assistance with some of the admin stuff."))
story.append(Spacer(1, 1))
story.append(quote_block("I would prefer to have an AI because then I'm not worried about them all of a sudden up and quitting and me having to like retrain and like do all of that."))
story.append(Spacer(1, 1))
story.append(quote_block("I think the one I want to focus on first is, you know, intake first."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Intake handled fast.</b> Every new lead gets a quick response, even when she is in court."))
story.append(bd("<b>AI, not hires.</b> She fears staff quitting and retraining more than she fears tech."))
story.append(bd("<b>Her top ask.</b> AI pulls LegalMatch leads into MyCase and reaches out right away."))
story.append(bd("<b>Admin off her desk.</b> Template motions to withdraw and the morning email pile."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>She is the whole firm.</b> No attorney, paralegal, receptionist, or admin."))
story.append(b("<b>Slow follow-up.</b> She loses an estimated 5 to 10 leads a month."))
story.append(b("<b>After-hours gap.</b> Google Voice goes to voicemail; a past answering service failed."))
story.append(b("<b>LegalMatch no-shows.</b> She says 40 to 50% do not answer on LegalMatch leads."))
story.append(b("<b>Feasibility unknown.</b> LegalMatch has no public API and MyCase access is unconfirmed."))

story.append(thin_rule())

# ── Why This Fractional CTO Package (replaces Marketing section: no marketing recommended) ──
story.append(Paragraph("Why This Fractional CTO Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives her one person who leads the AI rollout so she is not doing it between hearings."))
story.append(bd("Points the first automations at intake, her stated priority."))
story.append(bd("Turns her wish list into a monthly plan of skills and automations."))

story.append(Paragraph("<b>Fractional CTO Level 1  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Includes one monthly 1:1 session and up to 2 extra 1-hour sessions."))
story.append(b("Includes up to 2 skills deployed and up to 1 custom automation per month."))
story.append(b("Training videos and a monthly automation report are included. Setup fee is $0."))
story.append(b("Rep and seller locked this package. Foundation Sprint is not part of Level 1."))

story.append(thin_rule())

# ── Why This AI Workforce Package (replaces Coaching section) ──
story.append(Paragraph("Why This AI Workforce Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives her a working AI seat now, at the lowest entry cost."))
story.append(bd("Adds a weekly session so she keeps learning while the fCTO builds."))

story.append(Paragraph("<b>AI Workforce Pro \u2013 Starter (1 user)  |  $350/mo</b>", S["subsection"]))
story.append(b("1 seat assumed because team size was not stated. Confirm the seat count."))
story.append(b("1M AI credits per user, month-to-month. No stand-alone price exists. Never quote one."))
story.append(b("Seller replaced Elite Coach Plus. Marketing stays excluded."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Allied Defense Law \u2014 Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Marketing or Ad Spend (replaces Ad Spend section) ──
story.append(Paragraph("Why No Marketing or Ad Spend", S["section"]))
story.append(bd("She said she is happy with her leads. Her problem is reaching them fast enough."))
story.append(bd("You asked if marketing can wait since she cannot handle more leads. She said \u201cat right now.\u201d"))
story.append(b("No ad spend, ROI table, or Block 4 in the report. Marketing is a Phase 2 idea only."))
story.append(b("If marketing is added later: Phoenix criminal defense and DUI needs approval, and Essentials is off the table."))

story.append(thin_rule())

# ── Confirm Before The Call (internal flags) ──
story.append(Paragraph("Confirm Before The Call", S["section"]))
story.append(b("<b>Revenue fit.</b> Fractional CTO L1 requires $400K+. She said ~$250K. HubSpot range is $180K\u2013$960K."))
story.append(b("<b>Solo rule.</b> LAW is normally not sold to a solo with no staff. Confirm she can run the sessions."))
story.append(b("<b>Delivery.</b> Confirm LAW delivery has launched and there is capacity."))
story.append(b("<b>Under $300K.</b> Scoping approval applies. Confirm she can fund the first months."))
story.append(b("<b>Missing data.</b> No live reviews, PageSpeed, maps, or ads data. Re-run in a browser if you want figures."))
story.append(b("<b>Name and phone.</b> Directories show 928 and 602 numbers and three firm-name variants."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"Is $3,647 a month too much at my revenue?"', S["objection_q"]))
story.append(Paragraph("It is about 17.5% of her stated pace (under the 35% cap). She lost 5 to 10 leads a month at ~$4,000 a case, about $20K to $40K in case value (her numbers, not a promise).", S["objection_a"]))

story.append(Paragraph('"Can the AI really link LegalMatch and MyCase?"', S["objection_q"]))
story.append(Paragraph("Do not promise it. Feasibility is unconfirmed. Her wish list comes first, then the fCTO confirms what is possible.", S["objection_a"]))

story.append(Paragraph('"I already have an AI account I have not used."', S["objection_q"]))
story.append(Paragraph("Time is the blocker: intake is \u201ctaking away from the time that I have for my cases.\u201d The fCTO does the building with her.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Fractional CTO Level 1</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Monthly fCTO sessions, skills, and one custom automation.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>AI Workforce Pro \u2013 Starter (1 user)</b>", S["price_main"]),
     Paragraph("$350/mo", S["price_main"])],
    [Paragraph("AI workspace seat plus a weekly implementation session.", S["price_detail"]),
     Paragraph("No stand-alone price", S["price_detail"])],
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
    "Total: $3,647/mo  |  Save $500/mo by bundling  |  17.5% of stated revenue (under 35% cap)",
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
