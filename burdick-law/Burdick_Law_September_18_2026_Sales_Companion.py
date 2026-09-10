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

OUTPUT_PATH = "burdick-law/Burdick_Law_September_18_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Burdick Law", S["title"]))
story.append(Paragraph("Sales Companion  |  September 18, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Vanessa Burdick", S["snap_value"]),
     Paragraph("Not stated (per-case)", S["snap_value"]),
     Paragraph("Solo (1)", S["snap_value"]),
     Paragraph("3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("New York, NY", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM + NICHE DOMINANCE", S["section"]))
story.append(Paragraph("Vanessa wants a self-managing, CEO-level practice built on high-value private felony and homicide cases — not another job trading hours for low per-case pay.", S["subsection"]))

story.append(quote_block("Vision: Build a self-managing firm to enable a hands-off, CEO-level role."))
story.append(Spacer(1, 1))
story.append(quote_block("No website, Google Business Profile, or formal intake system."))
story.append(Spacer(1, 1))
story.append(quote_block("Payment is per-case, not monthly, and rates are low."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>A self-managing, CEO-level practice.</b> Not trading hours for low per-case pay."))
story.append(bd("<b>Off assigned-counsel volume.</b> Fewer, higher-value private felony/homicide cases."))
story.append(bd("<b>$700K-$800K profit within 6-7 years.</b> A specific, stated long-term goal."))
story.append(bd("<b>Foundation before marketing.</b> Systems, hiring, and fee structure first."))

story.append(Spacer(1, 1))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Zero digital footprint.</b> No website, GBP, or online presence of any kind."))
story.append(b("<b>No intake process.</b> Nothing converts a future inquiry into a retained client."))
story.append(b("<b>Solo, no staff.</b> She personally handles every case and admin task."))
story.append(b("<b>No private fee structure.</b> Compensation is per-case assigned-counsel pay only."))
story.append(b("<b>Well-funded competitors own the niche.</b> Spodek and Tsigler dominate her target terms."))

story.append(thin_rule())

# ── Why No Marketing Package Yet ──
story.append(Paragraph("Why No Marketing Package Yet", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Protects her spend until a website, GBP, and intake process exist to receive the leads."))
story.append(bd("Matches the phased, foundation-first engagement already proposed on the call."))

story.append(Paragraph("<b>No Marketing Package (Phase 1)  |  $0/mo</b>", S["subsection"]))
story.append(b("This was not a standard marketing/intake-growth call — do not push a marketing bundle."))
story.append(b("No website, GBP, or intake system exists today — ad spend now has nowhere to send leads."))
story.append(b("Original HubSpot-driven suggestion (Elite Coach Plus/Starter marketing) was not transcript-stated."))
story.append(b("Seller override: Jacob dropped Full Service Marketing entirely for this deal via Slack, 9/10/26."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Builds the intake, hiring, and fee-structure frameworks before marketing spend makes sense."))
story.append(bd("1:1 support sequencing the shift from assigned-counsel work to private casework."))

story.append(Paragraph("<b>Coach Essentials Plus  |  $2,497/mo bundled</b>", S["subsection"]))
story.append(b("Matches the $2,497/mo Phase 1 coaching figure already discussed on the call."))
story.append(b("Sold standalone — no marketing to bundle against, so bundled = stand-alone (no discount)."))
story.append(b("4-month-old firm, no tracked revenue — Budget-Reality Override rules out Elite Coach Plus."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Burdick Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Future Ad Spend (Phase 3) ──
story.append(Paragraph("Why This Future Ad Spend (Phase 3 — Not Sold Today)", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Shows what marketing could look like once the foundation is in place — not sold today."))
story.append(bd("Niche case value ($25K-$150K/case) shows strong potential return once she is ready."))

story.append(Paragraph("<b>Recommended Ad Spend Range (Phase 3 planning estimate):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,000/mo — Criminal Defense + High-competitiveness NYC floor."))
story.append(b("<b>Aggressive:</b> $18,750/mo — 20% rule vs. the $700K-$800K profit goal, NYC Tier 1."))

story.append(Paragraph("<b>Estimated Return on Investment (all estimates):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~$100K/mo vs. $5K spend = ~20x. Realistic capacity: 1-3 cases/mo."))
story.append(b("<b>Aggressive:</b> ~$425K/mo vs. $18.75K spend = ~23x. Mechanical case count (~17/mo) exceeds solo capacity — do not quote it to the client."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Criminal Defense + High-competitiveness NYC floor = $5,000 min."))
story.append(b("<b>Aggressive:</b> $750K goal midpoint x 20% / 12 = $12,500 x NYC Tier 1 (1.5x) = $18,750."))

story.append(thin_rule())

# ── If She Pushes Back ──
# FILL: 2-4 objections anticipated from the transcript
# Each: red question (objection_q style) + gray response (objection_a style)
# Responses use specific data from the audit — competitor numbers, transcript quotes, etc.
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"Why isn\'t SMB Team recommending marketing? I need cases now."', S["objection_q"]))
story.append(Paragraph("The call itself was framed around building operational readiness first. She has no website, GBP, or intake process today, so marketing spend now would generate inquiries with nowhere to go. The roadmap lays out exactly when marketing gets added in Phase 3.", S["objection_a"]))

story.append(Paragraph('"$2,497/month feels like a lot for a firm that\'s only 4 months old."', S["objection_q"]))
story.append(Paragraph("This matches the $2,497/mo Phase 1 coaching figure she already discussed on the call. It is scoped to build the intake, hiring, and fee-structure foundation before any marketing spend — not a marketing bundle.", S["objection_a"]))

story.append(Paragraph('"How do I know this gets me to $700K-$800K in profit?"', S["objection_q"]))
story.append(Paragraph("Without a private fee structure or financial visibility today, there is no way to measure progress toward that goal. Coach Essentials Plus builds exactly that tracking system, and the roadmap shows when marketing, hiring, and AI tooling get added as the firm is ready.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
# FILL: All pricing from the scoping calculation
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>No Marketing Package (Phase 1)</b>", S["price_main"]),
     Paragraph("$0/mo", S["price_main"])],
    [Paragraph("Deferred to Phase 3 per the call — see roadmap.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>Coach Essentials Plus</b>", S["price_main"]),
     Paragraph("$2,497/mo", S["price_main"])],
    [Paragraph("Sold standalone — no bundle discount applies.", S["price_detail"]),
     Paragraph("$2,497 stand-alone", S["price_detail"])],
    [Paragraph("<b>Future Ad Spend (Phase 3 estimate)</b>", S["price_main"]),
     Paragraph("$5,000–$18,750/mo", S["price_main"])],
    [Paragraph("Not part of today's recommendation — see roadmap.", S["price_detail"]),
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
    "Total Phase 1: $2,497/mo  |  No marketing spend today  |  Future ad spend $5,000-$18,750/mo shown for Phase 3 planning only",
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
