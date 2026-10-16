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

# FILL: Output path — use format [FirmName]_[MMDDYYYY]_Sales_Companion.pdf
OUTPUT_PATH = "oregon-legacy/Oregon_Legacy_10162026_Sales_Companion.pdf"


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

story.append(Paragraph("Oregon Legacy Law, LLC", S["title"]))
story.append(Paragraph("Sales Companion  |  October 16, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Linda &quot;Lin&quot; Ratcliffe", S["snap_value"]),
     Paragraph("~$260K/yr", S["snap_value"]),
     Paragraph("Solo + 2 support", S["snap_value"]),
     Paragraph("3", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Bend, OR", S["snap_value"])],
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
story.append(Paragraph("Lin wants a predictable, self-managing firm so she is no longer the single point of failure.", S["subsection"]))

story.append(Paragraph("<i>Source is a Fathom AI summary, not a verbatim transcript. DBM is inferred, not quoted. Signals below are paraphrased, not her exact words.</i>", S["disclaimer"]))
story.append(b("Handles legal and low-value admin work herself, including about an hour a day on Word templates."))
story.append(b("Misses about a dozen calls a month; paralegal callback process is inefficient."))
story.append(b("12-month goal is systems, SOPs, KPIs, intake, and billing before hiring."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>A firm that runs without her.</b> A predictable, self-managing practice she can delegate to."))
story.append(bd("<b>Foundation first.</b> Systems, SOPs, and KPIs in place before she hires."))
story.append(bd("<b>Her time back.</b> Stop spending the day on low-value administrative work."))
story.append(bd("<b>A bigger firm later.</b> In 3-6 years: 3-4 attorneys, more office space, take-home above $200K a year."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>She is the bottleneck.</b> One attorney, one paralegal, and a virtual receptionist service."))
story.append(b("<b>Leaky intake.</b> About a dozen missed calls a month and a slow callback hand-off."))
story.append(b("<b>Hiring fear.</b> Past staff experiences make her gun-shy about hiring."))
story.append(b("<b>Thin online presence.</b> Two-page site; firm name did not surface in nine Bend searches."))
story.append(b("<b>Reputation risk.</b> Public reviews mention unreturned calls and deadlines. Do not quote them to her."))

story.append(thin_rule())

story.append(Paragraph("Why No Marketing Package (Seller Override)", S["section"]))
story.append(Paragraph("<b>What this does for her:</b>", S["subsection"]))
story.append(bd("Fixes intake and systems first, so any future marketing spend turns into signed clients."))
story.append(bd("Keeps the first investment on the foundation she asked for."))
story.append(b("Call was an ops and coaching conversation, not a lead-gen one."))
story.append(b("Starter ($4,997/mo bundled) was dropped per the September 30, 2026 Slack request."))
story.append(b("Marketing becomes a Phase 2 add once the firm passes $500K and intake can handle volume."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives her a proven playbook for intake and follow-up instead of building it alone."))
story.append(bd("Helps her document and hand off the work that does not need an attorney."))
story.append(bd("Prepares her to hire from written roles and SOPs, not from scratch."))

story.append(Paragraph("<b>Elite Coach  |  $3,497/mo (flat stand-alone price)</b>", S["subsection"]))
story.append(b("$260K revenue sits in the $250K-$400K band, where Elite Coach is the table default."))
story.append(b("The $2,600 bundled price only applies with a bundle partner, so no savings apply here."))
story.append(b("$3,497 x 12 = $41,964, or 16.1% of revenue. Well under the 35% cap."))
story.append(b("Revenue is under $300K, so scoping approval is required."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Oregon Legacy — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("What We Left Out and Why", S["section"]))
story.append(b("<b>Ad spend:</b> none. No marketing package is recommended, so Block 4 and ROI projections are omitted."))
story.append(b("<b>Fractional Business Officer:</b> discussed on the call, but FCOO is hidden under $500K revenue."))
story.append(b("<b>SOP Builder AI tool:</b> no Legal AI Workforce tier was selected. Confirm LAW has launched before adding AI Workforce Pro - Starter ($350/user/mo)."))
story.append(b("<b>Attorney Assistant:</b> mentioned only as a possible third-party stopgap, not an SMB Team service."))

story.append(thin_rule())

story.append(Paragraph("Verify Before the Call", S["section"]))
story.append(b("Review counts and ratings are unconfirmed (aggregator-sourced). The report uses qualitative wording only."))
story.append(b("PageSpeed scores were not obtained (API quota). Ad, LSA, and Meta presence could not be observed."))
story.append(b("Local 3-pack results are an organic proxy, not a rendered map pack."))

story.append(thin_rule())

story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I cannot spend $3,497 a month on a $260K practice."', S["objection_q"]))
story.append(Paragraph("It is 16.1% of revenue, under the 35% cap. The summary cites an estimated $396K a year lost to missed calls and intake. That figure is unverified, so use it as a talking point only, never as an audited number. If budget is a real limit, Coach Essentials Plus ($1,997/mo) is the lower-cost option.", S["objection_a"]))

story.append(Paragraph('"I am gun-shy about hiring."', S["objection_q"]))
story.append(Paragraph("That is why coaching comes first. The plan builds SOPs, KPIs, and a hiring blueprint before any new hire, which is the order she already told us she wants.", S["objection_a"]))

story.append(Paragraph('"We talked about a Fractional Business Officer. Where is it?"', S["objection_q"]))
story.append(Paragraph("FCOO opens at $500K in revenue, and she is at about $260K. Elite Coach starts the systems work now, and FCOO is the Phase 2 step once she reaches that milestone.", S["objection_a"]))

story.append(Paragraph('"Why not fix my website and get more leads first?"', S["objection_q"]))
story.append(Paragraph("A dozen calls a month are already being missed. More leads into a leaky intake process just means more missed calls. Fix the process, then add marketing in Phase 2.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$3,497/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, practice area masterminds, virtual quarterly workshops.", S["price_detail"]),
     Paragraph("Stand-alone price, no bundle", S["price_detail"])],
]
pt = Table(price_data, colWidths=[4.5 * inch, 1.7 * inch])
pt.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 4),
    ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ("TOPPADDING", (0,0), (-1,-1), 2),
    ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(pt)
story.append(Paragraph(
    "Total: $3,497/mo  |  No bundle savings  |  16.1% of revenue (under 35% cap)",
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
