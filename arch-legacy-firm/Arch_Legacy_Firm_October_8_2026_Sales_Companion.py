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
_FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Design Files", "fonts")
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

OUTPUT_PATH = "arch-legacy-firm/Arch_Legacy_Firm_October_8_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Arch Legacy Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  October 8, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Name not captured", S["snap_value"]),
     Paragraph("~$3M (2026 pace)", S["snap_value"]),
     Paragraph("~18", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Watkinsville, GA (2 offices)", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: TIME FREEDOM", S["section"]))
story.append(Paragraph("A firm that runs on systems, so the team can stop hiring and grow into business and tax planning.", S["subsection"]))

story.append(quote_block("I'm tired of hiring employees… implement systems… so that we can quit hiring for a hot minute."))
story.append(Spacer(1, 1))
story.append(quote_block("We're leaving a lot of money on the table by not pushing forward into business and tax… I'm out of bandwidth."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What the owner wants:</b>", S["subsection"]))
story.append(bd("<b>Stop hiring.</b> Growth should not mean another round of headcount."))
story.append(bd("<b>Secure, firmwide AI.</b> Roll AI out to the whole team safely."))
story.append(bd("<b>New verticals.</b> Add business and tax planning without more strain."))
story.append(bd("<b>A balanced team.</b> Protect work-life balance for a team of moms."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping the owner:</b>", S["subsection"]))
story.append(b("<b>No bandwidth.</b> The owner has no time to lead an AI rollout personally."))
story.append(b("<b>Manual handoffs.</b> Recaps, file organization, and task handoffs run on people."))
story.append(b("<b>Weak after-hours.</b> The Abby Connect voice AI is viewed as subpar."))
story.append(b("<b>Split systems.</b> Intake data sits in both GoHighLevel and DecisionVault."))
story.append(b("<b>Pricing pending.</b> Formal AI Workforce Pro and fCTO pricing is still to come."))

story.append(thin_rule())

# ── Why This Fractional CTO Package ──
story.append(Paragraph("Why This Fractional CTO Package", S["section"]))

story.append(Paragraph("<b>What it does for the owner:</b>", S["subsection"]))
story.append(bd("A dedicated leader runs the AI rollout, so no one on the team has to find the time."))
story.append(bd("Recaps, file work, and handoffs become automations instead of coordinator hours."))
story.append(bd("The SOP-trained knowledge base lets a third office launch on the firm's own systems."))

story.append(Paragraph("<b>Fractional CTO Level 2  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue is about $3M, above the $1M requirement for Level 2."))
story.append(b("Levels 1 and 2 were both discussed on the call; Level 2 adds speed for a firmwide rollout."))
story.append(b("Level 2: 2 monthly 1:1s, up to 4 skills, up to 2 custom automations. $0 setup fee."))
story.append(b("Level 3 ($8,997/mo) also qualifies at $3M+ if the owner wants weekly sessions."))

story.append(thin_rule())

# ── Why This AI Workforce Pro Package ──
story.append(Paragraph("Why This AI Workforce Pro Package", S["section"]))

story.append(Paragraph("<b>What it does for the owner:</b>", S["subsection"]))
story.append(bd("Every team member works in one secure, firmwide AI workspace."))
story.append(bd("The weekly implementation session turns tools into daily habits."))
story.append(bd("The workspace gives the fCTO a place to deploy skills the whole team uses."))

story.append(Paragraph("<b>AI Workforce Pro, 20 seats  |  $3,397/mo bundled</b>", S["subsection"]))
story.append(b("$1,597/mo covers 5 users, plus $120/mo for each of 15 more users."))
story.append(b("20 seats was a planning count on the call. Confirm the real number."))
story.append(b("Yearly contract with 10M usage and 10M bonus credits. No stand-alone price exists."))
story.append(b("Overages are billed at $150/mo."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Arch Legacy Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Marketing Package ──
story.append(Paragraph("Why No Marketing Package", S["section"]))

story.append(Paragraph("<b>What this does for the owner:</b>", S["subsection"]))
story.append(bd("The proposal matches what the owner asked for: AI implementation, not lead generation."))
story.append(bd("Every dollar goes to the problem the owner named, which is bandwidth and hiring."))

story.append(Paragraph("<b>Why the default package was overridden:</b>", S["subsection"]))
story.append(b("The pricing logic suggested Platinum marketing plus Elite Coach Plus, about $19,197/mo."))
story.append(b("The call was about AI. LSAs already bring in qualified trust clients."))
story.append(b("The default also assumed a team of 3. The firm has about 18 people."))
story.append(b("Marketing can be revisited later if the owner raises lead volume."))
story.append(b("Spend check: $8,394/mo is about 3.4% of monthly revenue, under the 35% cap."))

story.append(thin_rule())

# ── If The Owner Pushes Back ──
story.append(Paragraph("If The Owner Pushes Back", S["section"]))

story.append(Paragraph('"We already pay about $430 a month for Claude."', S["objection_q"]))
story.append(Paragraph("Those seats are the tools. The fCTO decides what to automate, builds it, and the weekly session drives adoption. The owner said \"I'm out of bandwidth.\" This is the bandwidth.", S["objection_a"]))

story.append(Paragraph('"Can we start with Level 1?"', S["objection_q"]))
story.append(Paragraph("Level 1 is $3,297/mo with one monthly session, 2 skills, and 1 automation. Level 2 gives twice the sessions and automations for a firmwide rollout ahead of the third office.", S["objection_a"]))

story.append(Paragraph('"Do we really need 20 seats?"', S["objection_q"]))
story.append(Paragraph("20 was the planning count. Each seat past 5 is $120/mo, so the price moves in simple steps. Confirm the exact number on the Solution Call.", S["objection_a"]))

story.append(thin_rule())

# ── Before You Send ──
story.append(Paragraph("Before You Send", S["section"]))
story.append(b("<b>LAW delivery.</b> Confirm LAW delivery has launched and capacity is open."))
story.append(b("<b>Reviews.</b> Review counts are unconfirmed (Birdeye only). Verify on Google first."))
story.append(b("<b>Not captured.</b> PageSpeed, live GBP, Google Ads, and Meta Ads data were not obtained."))
story.append(b("<b>Phone numbers.</b> The site shows (706) 702-5749 and (706) 352-9060. Confirm which is right."))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Fractional CTO — Level 2</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("2 monthly 1:1s, up to 4 skills, up to 2 custom automations.", S["price_detail"]),
     Paragraph("<strike>$5,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>AI Workforce Pro — 20 seats</b>", S["price_main"]),
     Paragraph("$3,397/mo", S["price_main"])],
    [Paragraph("Secure firmwide workspace with weekly implementation sessions.", S["price_detail"]),
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
    "Total: $8,394/mo  |  Save $800/mo by bundling  |  3.4% of revenue (under 35% cap)",
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
