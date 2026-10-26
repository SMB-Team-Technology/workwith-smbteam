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

OUTPUT_PATH = "church-page-gailan/Church_Page_Gailan_October_19_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Church, Page &amp; Gailan, PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  October 19, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Kevin Page", S["snap_value"]),
     Paragraph("Not stated (HubSpot $3M+)", S["snap_value"]),
     Paragraph("19 (4 + 15)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Yakima, WA (4 offices)", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM (inferred)", S["section"]))
story.append(Paragraph("The firm wants AI and automation to take manual, tedious work off the support team and to connect its systems.", S["subsection"]))
story.append(Paragraph("<i>The DBM is an inference. The call source is a Fathom summary, not a full transcript, so no verbatim quotes are shown.</i>", S["disclaimer"]))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What they want:</b>", S["subsection"]))
story.append(bd("<b>Reliable Filevine automation.</b> The current automation process is not working well."))
story.append(bd("<b>Less manual support work.</b> Records requests, status updates, and scheduling."))
story.append(bd("<b>Connected systems.</b> Cross-platform integrations are on the list."))
story.append(bd("<b>Understand AI first.</b> They want to see what AI can do before defining automations."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping them:</b>", S["subsection"]))
story.append(b("<b>No defined scenarios yet.</b> They are still evaluating AI before choosing what to automate."))
story.append(b("<b>Filevine limits.</b> Native AI (Lois) has helped some, but automation is weak."))
story.append(b("<b>Hiring ramp.</b> Support staff grow from about 15 toward 22 to 23."))
story.append(b("<b>Marketing off the table.</b> They called it outside the scope of this call."))
story.append(b("<b>Trial only.</b> AI Workforce Pro is a free trial, with no tier or price named."))

story.append(thin_rule())

# ── Why This AI Leadership Package ──
story.append(Paragraph("Why This AI Leadership Package", S["section"]))
story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("A Fractional CTO leads the AI and Filevine work so it does not land on staff."))
story.append(bd("Each month adds working skills and a custom automation."))
story.append(bd("Manual work leaves the team before the next wave of hires arrives."))

story.append(Paragraph("<b>Fractional CTO Level 1  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Revenue fits: HubSpot shows $3M+ against the $400K floor for Level 1."))
story.append(b("The fCTO came up on the call as the way to scope Filevine automations."))
story.append(b("The level was not named on the call. Seller chose Level 1; confirm with the rep."))
story.append(b("Level 1: one monthly 1:1, up to 2 skills, and up to 1 custom automation a month."))

story.append(thin_rule())

# ── Why This AI Platform Package ──
story.append(Paragraph("Why This AI Platform Package", S["section"]))
story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("The whole team works from one shared, firm-managed AI workspace."))
story.append(bd("Pre-built skills turn the trial they started into daily practice."))
story.append(bd("A weekly implementation session keeps adoption moving."))

story.append(Paragraph("<b>AI Workforce Pro (19 users)  |  $3,277/mo bundled</b>", S["subsection"]))
story.append(b("Price: $1,597 for the first 5 users plus 14 x $120 = $3,277. No stand-alone price."))
story.append(b("Seat count of 19 equals 4 attorneys plus 15 support staff. Confirm before sending."))
story.append(b("Yearly contract; 20M credits (10M + 10M bonus); overage $150/mo."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Church, Page &amp; Gailan — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Marketing Package or Ad Spend ──
story.append(Paragraph("Why No Marketing or Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Keeps the proposal on AI, which is what the call was about."))
story.append(bd("Leaves room to add services later once automation is in place."))
story.append(Paragraph("<b>Why marketing was left out:</b>", S["subsection"]))
story.append(b("The call was AI-led, and no lead-gen need was stated."))
story.append(b("Google Ads and LSA are already active, so there is no ad spend or ROI to project."))
story.append(b("They are a former SMB Team marketing client (parted 2024)."))
story.append(b("Elite Coach Plus from the package file had no transcript basis and was removed."))
story.append(Paragraph("<b>Check before the call:</b>", S["subsection"]))
story.append(b("Review counts are UNCONFIRMED. Verify live; the report uses no exact numbers."))
story.append(b("3-pack, ads, LSA, and Meta data were not reachable. PageSpeed is local Lighthouse (37 / 86)."))
story.append(b("Revenue is HubSpot only. Confirm seat count, fCTO level, and AI delivery capacity."))

story.append(thin_rule())

# ── If They Push Back ──
story.append(Paragraph("If They Push Back", S["section"]))

story.append(Paragraph('"Marketing and SEO are outside what I wanted to discuss."', S["objection_q"]))
story.append(Paragraph("Agree. This proposal has no marketing. The website and SEO audit stays optional, and the PageSpeed 37 mobile score is the only item worth a mention.", S["objection_a"]))

story.append(Paragraph('"We already use Filevine\'s AI and it helps some."', S["objection_q"]))
story.append(Paragraph("Keep it. The call said Filevine automation is where it falls short. The fCTO scopes what to build, and AI Workforce Pro covers the work across other tools.", S["objection_a"]))

story.append(Paragraph('"Why pay for 19 seats when we are still on a trial?"', S["objection_q"]))
story.append(Paragraph("19 matches 4 attorneys plus 15 support staff. $1,597 covers the first 5, then $120 each, so the count is easy to adjust. The fCTO turns the trial into a rollout.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Fractional CTO Level 1</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Monthly 1:1 sessions, skills deployed, and a custom automation.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>AI Workforce Pro (19 users)</b>", S["price_main"]),
     Paragraph("$3,277/mo", S["price_main"])],
    [Paragraph("Shared AI workspace plus a weekly implementation session.", S["price_detail"]),
     Paragraph("No stand-alone price", S["price_detail"])],
    [Paragraph("<b>Marketing and Ad Spend</b>", S["price_main"]),
     Paragraph("Not included", S["price_main"])],
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
    "Total: $6,574/mo  |  Save $500/mo by bundling  |  2.6% of the HubSpot $3M+ revenue figure (under 35% cap)",
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
