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

OUTPUT_PATH = "rebel-brown/RebelBrownLawGroup_July21_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Rebel Brown Law Group", S["title"]))
story.append(Paragraph("Sales Companion  |  July 21, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Marianne Rebel Brown", S["snap_value"]),
     Paragraph("$400K (SSD, stated)", S["snap_value"]),
     Paragraph("~2.5 (lean)", S["snap_value"]),
     Paragraph("3 — Solo", S["snap_value"]),
     Paragraph("80%", S["snap_value"]),
     Paragraph("Glassboro/Haddon Hts, NJ", S["snap_value"])],
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
story.append(Paragraph("Marianne wants the SSD practice to scale to 1,000 clients on a lean team so she is no longer the operational bottleneck in her own business.", S["subsection"]))

# Only one verbatim transcript fragment is documented in research notes ("babysitting") —
# no other word-for-word quotes were captured this session, so no additional quote
# blocks are fabricated here.
story.append(quote_block("The other 70% of my time is non-billable babysitting."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>A self-running SSD practice.</b> Scale to 1,000 clients without personally holding every piece together."))
story.append(bd("<b>Her time back.</b> Currently capped at 2-3 billable hours a day; wants that flipped toward casework and strategy."))
story.append(bd("<b>The SSD pivot to fully take hold.</b> Family Law is being handed off on purpose so SSD, her stronger and better-reviewed practice, becomes the whole business."))
story.append(bd("<b>Leads that don't go to waste.</b> She's already generating ~80 leads a month; she wants them worked, not lost."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Intake bottleneck.</b> Only ~20 of ~80 monthly leads are actually answered."))
story.append(b("<b>No delegation structure.</b> The lean 2.5-person team has no defined roles yet."))
story.append(b("<b>Invisible SSD SEO.</b> No city/county pages despite claiming 8-county coverage."))
story.append(b("<b>No profitability visibility.</b> No practice-level tracking of SSD vs. Family Law."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gets the SSD site ranking in the exact counties it claims to serve instead of losing those searches to named competitors."))
story.append(bd("Puts a real paid lead-gen system in place instead of relying on referrals and inbound alone."))
story.append(bd("Frees her from personally being the firm's only source of visibility."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("$400K stated SSD revenue sits at the Essentials/Starter boundary; the aggressive 1,000-client goal pushes to Starter."))
story.append(b("Starter's $25,000 ad spend cap covers both the conservative and aggressive recommended spend."))
story.append(b("Full Service (not ads-only) matches the SEO/content rebuild identified in the audit."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Builds the delegation and accountability structure the lean 2.5-person team doesn't have yet."))
story.append(bd("Gives her a coaching cadence to build role clarity instead of carrying every operational decision herself."))
story.append(bd("Puts group coaching and practice-area mastermind access behind the SSD growth push specifically."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue band ($400K-$1M) qualifies for Elite Coach Plus regardless of exact team size."))
story.append(b("No stated profit complaints yet — FCOO/FCFO not triggered; Phase 2/3 of roadmap revisits this."))
story.append(b("Revenue is under the $500K LAW minimum, so Legal AI Workforce is not included."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Rebel Brown — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Converts the SSD site's SEO and local visibility into an active paid lead pipeline instead of waiting on organic alone."))
story.append(bd("Buys the case volume needed to make real progress toward the 1,000-client goal within a reasonable timeframe."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — minimum viable spend, single-channel floor using the closest listed proxy row (SSD has no dedicated row in the approved tables)."))
story.append(b("<b>Aggressive:</b> $14,000/mo — full budget sized to the $800K derived revenue goal (2x current stated SSD revenue)."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 5 cases x $4K = $20K/mo vs. $3.5K spend = 5.7x return."))
story.append(b("<b>Aggressive:</b> 25 cases x $4K = $100K/mo vs. $14K spend = 7.1x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. SSD-specific CPL benchmarks should be validated by the paid ads team before finalizing.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Closest approved channel row (Family Law) PPC floor = $3,500."))
story.append(b("<b>Aggressive:</b> $800K goal x 20% / 12 = $13,333. Tier 4 (1.0x) ≈ $14,000. Under the $25,000 cap."))
story.append(b("Total at aggressive: $22,047/mo ≈ 33% of the $66,667/mo goal run rate. Under the 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"SSD isn\'t in your standard pricing tables — how do I know this ad spend number is real?"', S["objection_q"]))
story.append(Paragraph("We used the closest comparable, real approved benchmark rather than guessing, and flagged it clearly for our paid ads team to validate SSD-specific costs before the first dollar is spent.", S["objection_a"]))

story.append(Paragraph('"We\'re already handling 80 leads a month — why do we need more?"', S["objection_q"]))
story.append(Paragraph("Only about 20 of those 80 are being worked today. The fastest, cheapest win is fixing intake on leads you already have — worth an estimated $200K/year — before adding more volume.", S["objection_a"]))

story.append(Paragraph('"I don\'t have time to manage a coaching program on top of everything else."', S["objection_q"]))
story.append(Paragraph("Elite Coach Plus is built to remove time from your plate, not add to it — it's the delegation structure that gets you out of the 70% of your day that's currently non-billable admin.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Local SEO, SSD-focused paid ads, LSA, and city/county landing pages.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, masterminds, and quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
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
    "Total: $8,047/mo + $3,500–$14,000 ad spend  |  Save $1,147/mo by bundling  |  ~34.6% of current revenue–33.1% of goal revenue (under 35% cap)",
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
