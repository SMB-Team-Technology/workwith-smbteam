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

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)

# ── Colors — DO NOT MODIFY ──
DARK_NAVY = HexColor("#1a2332")
ACCENT_GREEN = HexColor("#3B6D11")
MEDIUM_GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#888888")
RULE_GRAY = HexColor("#CCCCCC")
QUOTE_BG = HexColor("#F5F7F0")
WHITE = HexColor("#FFFFFF")
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "cooper-cooper-p-a/Cooper & Cooper, P.A._July 13, 2026_Sales_Companion.pdf"


def add_page_elements(canvas, doc):
    """Draws red warning header and confidential footer on every page. DO NOT MODIFY."""
    canvas.saveState()
    width, height = letter
    canvas.setFont("Helvetica-Bold", 10)
    canvas.setFillColor(RED_WARNING)
    canvas.drawCentredString(width / 2, height - 0.38 * inch,
                             "FOR INTERNAL USE ONLY; DO NOT SHARE.")
    canvas.setStrokeColor(RED_WARNING)
    canvas.setLineWidth(0.5)
    canvas.line(0.6 * inch, height - 0.44 * inch,
                width - 0.6 * inch, height - 0.44 * inch)
    canvas.setFont("Helvetica", 7)
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
    "title", fontName="Helvetica-Bold", fontSize=16, leading=20,
    textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle(
    "subtitle", fontName="Helvetica", fontSize=9.5, leading=13,
    textColor=LIGHT_GRAY, spaceAfter=3)
S["section"] = ParagraphStyle(
    "section", fontName="Helvetica-Bold", fontSize=11, leading=15,
    textColor=ACCENT_GREEN, spaceBefore=6, spaceAfter=2)
S["subsection"] = ParagraphStyle(
    "subsection", fontName="Helvetica-Bold", fontSize=10, leading=13,
    textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle(
    "bullet", fontName="Helvetica", fontSize=9.5, leading=13,
    textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0,
    spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle(
    "bullet_dark", fontName="Helvetica", fontSize=9.5, leading=13,
    textColor=DARK_NAVY, leftIndent=12, bulletIndent=0,
    spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle(
    "quote", fontName="Helvetica-Oblique", fontSize=9.5, leading=13,
    textColor=DARK_NAVY, leftIndent=6, rightIndent=6,
    spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle(
    "snap_label", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
    textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle(
    "snap_value", fontName="Helvetica", fontSize=9.5, leading=12,
    textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle(
    "objection_q", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
    textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle(
    "objection_a", fontName="Helvetica", fontSize=9.5, leading=13,
    textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle(
    "price_main", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
    textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle(
    "price_detail", fontName="Helvetica", fontSize=8.5, leading=12,
    textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle(
    "savings", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
    textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle(
    "disclaimer", fontName="Helvetica-Oblique", fontSize=8.5, leading=11,
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

story.append(Paragraph("Cooper &amp; Cooper, P.A.", S["title"]))
story.append(Paragraph("Sales Companion  |  July 13, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Anthony &amp; Charlean Cooper", S["snap_value"]),
     Paragraph("$1M (pacing $2.3M)", S["snap_value"]),
     Paragraph("11 (12 next wk)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("20–25%", S["snap_value"]),
     Paragraph("Fleming Island, FL", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM (secondary: SCALE)", S["section"]))
story.append(Paragraph("Anthony and Charlean want the firm to run without them so they can take real time off — with a longer-term ambition to expand across Florida.", S["subsection"]))

story.append(quote_block("Charlean is stuck in casework, preventing her from focusing on management."))
story.append(Spacer(1, 1))
story.append(quote_block("to enable a vacation without disruption, ideally by October"))
story.append(Spacer(1, 1))
story.append(quote_block("profit is currently murky"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What they want:</b>", S["subsection"]))
story.append(bd("<b>A vacation that actually happens.</b> Systems in place to step away by October — not just a plan to."))
story.append(bd("<b>Charlean out of casework, into leadership.</b> A senior attorney hired so she can move fully into management."))
story.append(bd("<b>Marketing that finally works.</b> A real return on the ad spend they already doubled."))
story.append(bd("<b>A Florida-wide firm.</b> Long-term vision to expand into Tampa, St. Augustine, Boca, Fort Lauderdale, and the Panhandle."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping them:</b>", S["subsection"]))
story.append(b("<b>Doubled spend, flat results.</b> Budget went from $5K–$7.5K/mo to ~$20K/mo, but new clients stayed flat at ~15/mo."))
story.append(b("<b>Agency conflict of interest.</b> Their current agency also represents direct competitor Florida Women's Law Group."))
story.append(b("<b>Low intake conversion.</b> Only 20–25% of consults become retainers, against a 50% goal, with no automation live yet."))
story.append(b("<b>Charlean stuck in casework.</b> She cannot step into management while carrying a full caseload."))
story.append(b("<b>No financial visibility.</b> Profit is 'currently murky' and a bookkeeper is only now being hired."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Replaces the conflicted agency with a team focused only on Cooper &amp; Cooper's growth."))
story.append(bd("Gives the underfed Probate division its own lead flow to justify its high-cost attorney."))
story.append(bd("Turns the existing ~$20K/mo-equivalent spend into a return they can actually see."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $7,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue is $1M+ this year, pacing toward $2.3M — squarely in the Growth tier's $1M–$3M band."))
story.append(b("PageSpeed mobile score of 47/100 signals real conversion leakage a Full Service build is designed to fix."))
story.append(b("Current combined PPC/LSA/Meta spend already runs ~$20K/mo — well within the Growth tier's $50,000 ad spend cap."))
story.append(b("A dedicated Probate/Estate Planning campaign needs the same full-service build-out as Family Law."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Gives Anthony and Charlean a structured framework to hire a senior attorney and build real management."))
story.append(bd("Practice-area mastermind access connects them with other fast-growing family law/probate owners."))
story.append(bd("Builds the accountability that makes the October vacation achievable, not just aspirational."))

story.append(Paragraph("<b>Master's Circle  |  $4,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue is $1M+ with 11 employees (12 after next week) — in Master's Circle's target band."))
story.append(b("Pipeline flagged no dedicated ops lead detected — confirm ops capacity with Anthony before finalizing."))
story.append(b("Owners are explicitly focused on hiring and management structure — the core use case for this coaching tier."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Cooper &amp; Cooper — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Gives the Probate division dedicated lead flow instead of Family Law's budget leftovers."))
story.append(bd("Replaces the current conflicted-agency spend with campaigns built to convert, not just run."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — Family Law Google PPC minimum floor, single-channel reset."))
story.append(b("<b>Aggressive:</b> $14,000/mo — pipeline-set budget aligned to the firm's own goal of ~30 new clients/mo."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 5–6 cases x $4K = $23K/mo vs. $3.5K spend = 6.6x return."))
story.append(b("<b>Aggressive:</b> 37–38 cases x $4K = $150K/mo vs. $14K spend = 10.7x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Family Law Google PPC minimum floor = $3,500/mo (single most efficient channel)."))
story.append(b("<b>Aggressive:</b> Pipeline-computed at $14,000/mo — within the Growth tier's $50,000 cap; the 20% rule off the $2.3M pace would suggest a higher ceiling, so confirm with Anthony before scaling further."))
story.append(b("Total spend at aggressive: $25,997/mo = 31.2% of monthly revenue ($83,333 at $1M/yr pace). Under the 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If They Push Back", S["section"]))

story.append(Paragraph('"We already spend $20K/mo on marketing — why isn\'t that working?"', S["objection_q"]))
story.append(Paragraph("Their current agency also represents direct competitor Florida Women's Law Group in the same market — a conflict of interest that caps differentiation no matter how much the budget grows.", S["objection_a"]))

story.append(Paragraph('"We just started hiring a bookkeeper — can we really add more monthly spend right now?"', S["objection_q"]))
story.append(Paragraph("Total investment stays well under the 35% of revenue guideline even at the aggressive ad spend level, and Master's Circle coaching directly supports the financial visibility work the bookkeeper is starting.", S["objection_a"]))

story.append(Paragraph('"Charlean can\'t take on one more thing while she\'s stuck in casework."', S["objection_q"]))
story.append(Paragraph("Master's Circle is built for exactly this — it gives Anthony and Charlean a structured framework to hire the senior attorney who frees her, not one more task for her to manage alone.", S["objection_a"]))

story.append(Paragraph('"Our reviews and reputation are already strong — do we really need this?"', S["objection_q"]))
story.append(Paragraph("Their 4.9-star, 50+ review profile already outperforms every named competitor in this audit — the gap is visibility and conversion, exactly what Growth-tier marketing and better intake are built to fix.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("Dedicated PPC, LSA, SEO, and Meta across Family Law and Probate.", S["price_detail"]),
     Paragraph("<strike>$8,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle</b>", S["price_main"]),
     Paragraph("$4,600/mo", S["price_main"])],
    [Paragraph("Weekly coaching, masterminds, and a hiring/leadership framework.", S["price_detail"]),
     Paragraph("<strike>$4,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,500–$14,000/mo", S["price_main"])],
    [Paragraph("Goes to Google, LSA, and Meta — not to SMB Team.", S["price_detail"]),
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
    "Total: $11,997/mo + $3,500–$14,000 ad spend  |  Save $1,997/mo by bundling  |  18.6%–31.2% of revenue (under 35% cap)",
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
