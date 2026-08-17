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

OUTPUT_PATH = "velie-global/Velie_Global_Law_Firm_August_17_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Velie Global Law Firm, P.L.L.C.", S["title"]))
story.append(Paragraph("Sales Companion  |  August 17, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Jon Velie", S["snap_value"]),
     Paragraph("~$2.5M (2026 proj.)", S["snap_value"]),
     Paragraph("12+ attys / 2 offices", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Norman, OK / Dallas, TX", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM (+ SCALE, downstream)", S["section"]))
story.append(Paragraph("Jon wants Dallas systematized so he can step back from daily litigation and lead the firm's strategy and expansion into new markets.", S["subsection"]))

story.append(Paragraph("<i>No verbatim transcript — points below are paraphrased from an AI meeting summary.</i>", S["disclaimer"]))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Step back from daily Dallas litigation.</b> Jon is personally handling casework that should belong to a system."))
story.append(bd("<b>Systemize Dallas before expanding.</b> Dallas must run independently before New York or San Francisco."))
story.append(bd("<b>Know his real numbers.</b> Profitability is unknown today; goal is a 20–30% margin within 12 months."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No delegation structure in Dallas.</b> Jon is the intake system, the closer, and the litigator all at once."))
story.append(b("<b>Dallas has no formal marketing or intake process.</b> It runs entirely on referrals with no documented follow-up."))
story.append(b("<b>No financial visibility.</b> There is no system to show what the firm actually keeps."))
story.append(b("<b>Pam Velie's CGO role is brand new.</b> She was just hired and has a system to build, not one to run yet."))

story.append(thin_rule())

# ── Why This Operations Package ──
# NOTE: Call-purpose override applied — this was a Fractional COO/CTO call, not a
# marketing call. The two recommended packages are Operations (FCOO Advisor) and
# Technology (AI Accelerator L2), not Marketing + Coaching. See section_11_workings.txt.
story.append(Paragraph("Why This Operations Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Jon a dedicated operator to build the Dallas systems he doesn't have time to build."))
story.append(bd("Turns Pam's new CGO role into an actual system to run, and replicates Norman's intake model in Dallas."))

story.append(Paragraph("<b>Fractional COO Advisor  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ($2.5M) and team structure (under 5 dedicated ops staff) point to FCOO Advisor over Master's Circle, which requires 5+ dedicated staff."))
story.append(b("Directly matches the transcript's stated ask for Fractional COO support. Includes Elite Coach group deliverables."))
story.append(b("Stand-alone price is $3,797/mo — bundling saves $500/mo."))

story.append(thin_rule())

# ── Why This Technology Package ──
story.append(Paragraph("Why This Technology Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Integrates Clio, QuickBooks, and Stripe into one stack, eliminating manual work costing the firm money."))
story.append(bd("Deploys AI Workforce Pro-style skills for intake and billing, led by a dedicated Fractional CTO."))

story.append(Paragraph("<b>AI Accelerator L2 — Fractional CTO Level 2  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("Corrected revenue of $2.5M (transcript-stated, not the earlier HubSpot estimate) places the firm in the $1.5M–$3M L2 band."))
story.append(b("Directly matches the transcript's stated ask for a Fractional CTO to integrate the tech stack and build automations."))
story.append(b("Stand-alone price is $5,797/mo — bundling saves $800/mo. Foundation Sprint add-on available ($14,997 one-time)."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Velie Global — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend (Phase 2 — Not Part of Current Recommendation)", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Once Dallas's operations and tech stack are systematized, ad spend gives the office its own real lead generation engine instead of relying on referrals."))
story.append(bd("This is a Phase 2 investment, introduced only after the operational foundation is in place — matching the sequencing Jon himself described on the call."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $13,000/mo — channel minimums across Immigration + PI (Google PPC + LSA)."))
story.append(b("<b>Aggressive:</b> $30,000/mo — based on Dallas's stated 2026 revenue goal and Dallas Tier 1 geo multiplier."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 6 cases x $5.5K = $33K/mo vs. $13K spend = 2.5x return."))
story.append(b("<b>Aggressive:</b> 16 cases x $5.5K = $88K/mo vs. $30K spend = 2.9x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Immigration (PPC $3,000 + LSA $2,000) + PI (PPC $6,000 + LSA $2,000) = $13,000."))
story.append(b("<b>Aggressive:</b> $1.25M Dallas goal x 20% ÷ 12 = $20,833. Tier 1 Dallas (1.5x) = $31,250, rounded to $30,000."))
story.append(b("Total spend at aggressive ($30,000) + Phase 1 fees ($8,294) = $38,294/mo = 18.4% of monthly revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We already have Pam auditing operations — why do we need an outside COO too?"', S["objection_q"]))
story.append(Paragraph("Pam's role is strategic oversight. The Fractional COO builds and implements the day-to-day systems (intake replication, case screening, tech integration) so her audit turns into a working system instead of a plan on a shelf.", S["objection_a"]))

story.append(Paragraph("\"Isn't Norman's system already working — why spend on this at all?\"", S["objection_q"]))
story.append(Paragraph("Norman's system works because someone built it deliberately. Dallas is a different office with none of that infrastructure — replicating it takes dedicated implementation time neither Jon nor Pam currently has.", S["objection_a"]))

story.append(Paragraph("\"We're not ready to talk about marketing yet.\"", S["objection_q"]))
story.append(Paragraph("Agreed — that's why marketing isn't part of this recommendation. This proposal is built entirely around the Fractional COO and CTO services discussed on the call; ad spend is flagged only as a Phase 2 step once Dallas's systems are in place.", S["objection_a"]))

story.append(Paragraph('"How do we know this pays for itself?"', S["objection_q"]))
story.append(Paragraph("The $8,400/year cost of one unintegrated Clio feature, cited on the call, already offsets a meaningful share of the CTO investment — before counting the unprofitable Dallas cases the FCOO's screening process is designed to prevent.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Fractional COO Advisor</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Builds and implements Dallas's operating systems.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>AI Accelerator L2 — Fractional CTO Level 2</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("Integrates tech stack and deploys AI Workforce Pro skills.", S["price_detail"]),
     Paragraph("<strike>$5,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend (Phase 2)</b>", S["price_main"]),
     Paragraph("$13,000–$30,000/mo", S["price_main"])],
    [Paragraph("Goes to Google, LSA, and Meta — not to SMB Team. Introduced once Dallas ops are systematized.", S["price_detail"]),
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
    "Total: $8,294/mo + $13,000–$30,000 Phase 2 ad spend  |  Save $1,300/mo by bundling  |  4.0%–18.4% of revenue (under 35% cap)",
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
