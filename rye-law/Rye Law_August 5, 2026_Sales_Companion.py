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

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the leadership and delegation structure Rick doesn't have yet, using his 3 clerks and bookkeeper."))
story.append(bd("Frees Rick from being personally entrenched in every file — step one toward the independence he wants."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Proposal narrowed to Elite Coach Plus only per sales request — marketing removed from the immediate ask."))
story.append(b("~$400K-$1M estimated revenue band independently qualifies for Elite Coach Plus."))
story.append(b("$3,200/mo bundled is well below the $5,000/mo figure Rick was already evaluating."))

story.append(thin_rule())

# ── Why No Marketing Package (Yet) ──
story.append(Paragraph("Why No Marketing Package (Yet)", S["section"]))

story.append(Paragraph("<b>What holding it back does for him:</b>", S["subsection"]))
story.append(bd("Keeps the ask at $3,200/mo — well under the $4,997/mo Starter price Rick was previously evaluating."))
story.append(bd("Avoids asking Rick to fund ad spend on top of a new commitment while the AR is still outstanding."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  held for Phase 2 ($4,997/mo if added later)</b>", S["subsection"]))
story.append(b("Rick postponed the existing $5K/mo ask over ~$60K expenses + ~$50K AR — coaching alone is a lower, easier re-entry point."))
story.append(b("Revenue and practice-area mix would otherwise qualify Starter — reintroduce it once coaching builds the leadership structure."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Rye Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Ad Spend This Phase ──
story.append(Paragraph("Why No Ad Spend This Phase", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Keeps this engagement entirely inside SMB Team's management fee — no third-party dollars to Google/Meta to approve right now."))
story.append(bd("Lead generation (and the ad-spend conversation) is revisited once the leadership structure is in place and cash flow is predictable — see Phase 2 of the roadmap."))

story.append(Paragraph("<b>If Ad Spend Comes Up:</b>", S["subsection"]))
story.append(b("Reference range once Starter is reintroduced: Conservative $3,500/mo, Aggressive $11,500/mo — both scoped to all 5 practice areas."))
story.append(b("Do not quote ROI/ROAS figures for this engagement — coaching has no ad-spend component to project a return against."))
story.append(Paragraph("<i>Marketing figures above are reference-only for the Phase 2 conversation, not part of this proposal.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We already said we need to wait until January."', S["objection_q"]))
story.append(Paragraph("This proposal is built at $3,200/mo — well under the $5,000/mo figure Rick already reviewed — with no ad spend attached, so it's an easier re-engagement, not a harder one. It's ready to activate the moment the AR clears.", S["objection_a"]))

story.append(Paragraph('"The guarantee isn’t enforceable here, so how do I know this works?"', S["objection_q"]))
story.append(Paragraph("The guarantee applies to the marketing/ad-spend engagement, not to coaching — reframe around the concrete deliverables instead: weekly coaching, a delegation framework for his existing team, and financial visibility on the AR/expense cycle that's delaying him.", S["objection_a"]))

story.append(Paragraph('"I don’t have a marketing budget line yet — can this wait until the AR is in?"', S["objection_q"]))
story.append(Paragraph("That's exactly why this proposal doesn't include marketing or ad spend right now — Elite Coach Plus fits inside the management fee alone, with lead generation revisited in Phase 2 once the AR clears.", S["objection_a"]))

story.append(Paragraph('"Is coaching alone actually going to move the needle for 5 practice areas?"', S["objection_q"]))
story.append(Paragraph("Coaching isn't the lead-gen lever — it's the leadership and delegation structure that lets Rick step back from personally holding all 5 practice areas together, which is the prerequisite he described needing before scaling lead flow.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, delegation frameworks, and financial visibility work.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("Held for Phase 2", S["price_main"])],
    [Paragraph("Not included in this proposal — revisit once leadership structure is in place.", S["price_detail"]),
     Paragraph("$4,997/mo if added later", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("Not part of this phase", S["price_main"])],
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
    "Total: $3,200/mo  |  Save $297/mo by bundling  |  6.7% of estimated revenue (well under the 35% cap)",
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
