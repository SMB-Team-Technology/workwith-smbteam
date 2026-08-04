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

OUTPUT_PATH = "rye-law/Rye Law_August 5, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Rye Law", S["title"]))
story.append(Paragraph("Sales Companion  |  August 5, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Rick Rye", S["snap_value"]),
     Paragraph("~$570K (est., low conf.)", S["snap_value"]),
     Paragraph("5 (1 atty + 4 staff)", S["snap_value"]),
     Paragraph("3 - Solo", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Toronto/GTA (4 offices)", S["snap_value"])],
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
story.append(Paragraph(
    "Rick wants Rye Law to run independently of him day-to-day, using automation and a "
    "lean team instead of hiring more staff, so he can step back from being personally "
    "entrenched in operations.", S["subsection"]))

story.append(quote_block("Build a scalable business that runs independently, allowing for more personal freedom and less direct management."))
story.append(Spacer(1, 1))
story.append(quote_block("Leverage automation and “virtual avatars” to avoid hiring more staff — a “sweet spot” for efficiency."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>A firm that runs itself,</b> not just a bigger one."))
story.append(bd("<b>More personal freedom</b> — time back, not just revenue."))
story.append(bd("<b>Efficiency over headcount</b> — automation instead of hiring."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Cash flow timing.</b> ~$60K in year-end expenses + ~$50K unbilled AR are tying up his funds."))
story.append(b("<b>No lead gen system.</b> Zero paid or organic presence across all five practice areas."))
story.append(b("<b>He is the bottleneck.</b> Personally entrenched, no leadership layer beneath him."))
story.append(b("<b>Guarantee skepticism.</b> Flagged enforceability concerns on the guarantee — don't oversell it."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Rye Law its first real lead gen system across all five practice areas, instead of referrals alone."))
story.append(bd("Frees Rick from being the only source of new business — step one toward the independence he wants."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("4 locations + 5 practice areas make Essentials ineligible — Starter or above is required."))
story.append(b("~$570K estimated revenue (low confidence, HubSpot-sourced) independently qualifies for Starter."))
story.append(b("Rick was already evaluating ~$5,000/mo — Starter's $4,997/mo bundled matches almost exactly."))
story.append(b("Starter's $20,000 ad-spend cap comfortably covers the $3,500-$11,500/mo range below."))

story.append(thin_rule())

# ── Why No Coaching Package (Yet) — budget-reality override applied ──
story.append(Paragraph("Why No Coaching Package (Yet)", S["section"]))

story.append(Paragraph("<b>What holding it back does for him:</b>", S["subsection"]))
story.append(bd("Keeps the ask at $4,997/mo — what Rick already reviewed — not $8,197/mo before he's re-engaged."))
story.append(bd("Avoids compounding his cash-flow concern with a second new commitment he didn't ask for."))

story.append(Paragraph("<b>Elite Coach Plus  |  held for Phase 2 ($3,200/mo if added later)</b>", S["subsection"]))
story.append(b("OVERRIDE APPLIED: Rick postponed the existing $5K/mo ask over ~$60K expenses + ~$50K AR — adding coaching now raises the ask 64% above that."))
story.append(b("package_decision.json paired Starter + Elite Coach Plus at $8,197/mo total — intentionally overridden; do not present that number to Rick."))
story.append(b("Revenue and team size would otherwise qualify — reintroduce coaching in the Phase 2 conversation, not this re-engagement."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Rye Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns paid traffic into a predictable stream of new cases across all 5 practice areas instead of relying on referrals."))
story.append(bd("Scales with the firm — starting conservative while AR clears, then expanding once cash flow allows."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — minimum viable spend across recommended channels, well under the 35% cap."))
story.append(b("<b>Aggressive:</b> $11,500/mo — capped by the 35% total-spend rule, not the tier's $20,000 ceiling."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 4 cases x $4.7K = $18.8K/mo vs. $3.5K spend = 5.4x return."))
story.append(b("<b>Aggressive:</b> 16 cases x $4.7K = $75.2K/mo vs. $11.5K spend = 6.5x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Blended practice-area minimums across Immigration, Family, Litigation, Real Estate, and Business Law ~= $3,500."))
story.append(b("<b>Aggressive:</b> 2x current revenue ($1.14M) x 20% / 12 = $19,000. Minus $4,997 mgmt fee = $14,003 uncapped."))
story.append(b("Total spend at aggressive: $4,997 + $11,500 = $16,497/mo = 34.7% of revenue. Under the 35% cap (uncapped figure would have been 37.9% — corrected down)."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We already said we need to wait until January."', S["objection_q"]))
story.append(Paragraph("This proposal is built around the exact $5,000/mo figure Rick already reviewed — Starter alone, no added coaching — so there's nothing new to reconsider financially. It's ready to activate the moment the AR clears.", S["objection_a"]))

story.append(Paragraph('"The guarantee isn’t enforceable here, so how do I know this works?"', S["objection_q"]))
story.append(Paragraph("Point to the named local competitors already outperforming Rye Law in his own market: Chaudhary Law Office (300 reviews, 4.8 stars), Zinati Kay (27,000+ closings marketed), Simple Divorce (doors away from his own office). The risk isn't the guarantee — it's the gap widening every month with zero paid presence.", S["objection_a"]))

story.append(Paragraph('"I don’t have a marketing budget line yet — can this wait until the AR is in?"', S["objection_q"]))
story.append(Paragraph("Recommend using part of the ~$50K AR collection itself to fund the first 1-2 months of ad spend once collected, so the campaign can launch without waiting for a completely clean slate.", S["objection_a"]))

story.append(Paragraph('"Is $5K/mo actually going to move the needle for 5 practice areas?"', S["objection_q"]))
story.append(Paragraph("Starter's $20,000 ad-spend cap and the conservative-to-aggressive $3,500-$11,500/mo range are both scoped specifically to cover all 5 areas — this isn't a single-practice budget stretched thin.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("Ads, local SEO, and website conversion work across all 5 practice areas.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("Held for Phase 2", S["price_main"])],
    [Paragraph("Not included in this proposal — see budget-reality override above.", S["price_detail"]),
     Paragraph("$3,200/mo if added later", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,500–$11,500/mo", S["price_main"])],
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
    "Total: $4,997/mo + $3,500–$11,500 ad spend  |  Save $700/mo by bundling  |  17.9%–34.7% of revenue (under 35% cap)",
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
