"""
Sales Companion PDF — Alpha Center for Divorce Mediation
SMB Team | Jacob Meissner | May 26, 2026
FOR INTERNAL USE ONLY; DO NOT SHARE.
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

OUTPUT_PATH = "alpha-center-for-divorce-mediation/Alpha_Center_for_Divorce_Mediation_05262026_Sales_Companion.pdf"


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

story.append(Paragraph("Alpha Center for Divorce Mediation", S["title"]))
story.append(Paragraph("Sales Companion  |  May 26, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Keila M. Gilbert, Esq.", S["snap_value"]),
     Paragraph("~$900K est.", S["snap_value"]),
     Paragraph("14+ staff", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("Doylestown, PA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: LEGACY + FREEDOM", S["section"]))
story.append(Paragraph("Keila wants the firm to sustain and grow its mission without her daily involvement.", S["subsection"]))

story.append(quote_block("Founded after her own divorce in 1994 — built to serve families the way she wished she had been served."))
story.append(Spacer(1, 1))
story.append(quote_block("Launched the Alpha Community Education Foundation in 2021 — the mission extends beyond the law firm itself."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>The firm runs without her.</b> Step back from managing four offices."))
story.append(bd("<b>More families served.</b> Scale the mission — more mediation, less adversarial litigation."))
story.append(bd("<b>Time for the Foundation.</b> Focus on the non-profit she cannot fully attend to now."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No ops layer.</b> 4+ offices, 14+ staff, no COO — she is the coordination center."))
story.append(b("<b>Stalled reviews.</b> 4.3 stars vs. SnapDivorce 4.8 (same ZIP) — last review ~4 years ago."))
story.append(b("<b>LSA untapped.</b> BBB A+ qualifies her for Google Screened — never activated."))
story.append(b("<b>No cost tracking.</b> Multiple service lines, no cost-per-case data."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Every Eastern PA mediation search returns Alpha Center at the top — without her managing campaigns."))
story.append(bd("LSA activation gives her Google Screened status — top-of-page placement she is currently ceding."))
story.append(bd("Review program closes the 4.3 vs. 4.8 gap — map pack rankings improve across all office markets."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$900K — places firm in $400K–$1M Starter tier."))
story.append(b("Existing PPC infrastructure (call.alpha-divorce.com) already built — optimization accelerates results."))
story.append(b("57+ geo-targeted pages indexed — Full Service SEO maximizes their ranking potential."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Case acquisition cost tracked per office — she knows exactly where her marketing dollars are working."))
story.append(bd("Accountability structure built — the firm stops depending on Keila to coordinate everything."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M, any team — Elite Coach Plus is correct for this tier."))
story.append(b("No transcript: coaching establishes KPIs and measurement that do not currently exist."))
story.append(b("Bundle saves $1,147/mo vs. stand-alone pricing for both packages combined."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Alpha Center for Divorce Mediation — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Consistent new mediation cases — the firm serves more families without Keila generating each lead."))
story.append(bd("Measurable ROI — for the first time, every case has a known acquisition cost."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,000/mo — PPC $3,500 + LSA $2,000 + Meta Retargeting $1,500."))
story.append(b("<b>Aggressive:</b> $17,000/mo — full multi-channel coverage; 35%-cap compliant."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~11 cases x $3,500 avg = ~$38,500/mo vs. $7,000 spend = ~5.5x (est.)."))
story.append(b("<b>Aggressive:</b> ~30 cases x $3,500 avg = ~$105,000/mo vs. $17,000 spend = ~6.2x (est.)."))
story.append(Paragraph("<i>Estimates only. Case value uses competitor proxy. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Family Law channel minimums: PPC $3,500 + LSA $2,000 + Meta $1,500 = $7,000."))
story.append(b("<b>Aggressive:</b> $1.8M goal x 20% / 12 = $30K. Tier 4 (1.0x). Capped at $17K for 35% compliance."))
story.append(b("At aggressive: $25,047 total SMB spend = 33.4% of ~$75K/mo revenue — under the 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"We already have Google Ads — why do we need SMB Team?"', S["objection_q"]))
story.append(Paragraph("Current ads target 'divorce attorney' keywords for a mediation firm — a mismatch that suppresses conversion. SMB Team optimizes for mediation intent, activates LSA (untapped despite BBB A+), and launches Meta — channels generating zero leads today.", S["objection_a"]))

story.append(Paragraph('"Our reviews are fine — we have 39 reviews."', S["objection_q"]))
story.append(Paragraph("SnapDivorce has 22 reviews at 4.8 stars from the same ZIP. Rubin Glickman has 69 at 4.8 with a review from April 2026. Alpha Center's most recent visible review is ~4 years old. Google ranks by recency — older reviews suppress map pack position.", S["objection_a"]))

story.append(Paragraph('"I\'m not sure this is the right time."', S["objection_q"]))
story.append(Paragraph("SnapDivorce is at 4.8 stars today. Rubin Glickman is adding reviews this month. LSA slots fill up — BBB A+ eligibility does not guarantee Google Screened approval speed. Every month without action is a month competitors extend their lead.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta Ads, Local SEO, GBP, website CRO.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, masterminds, quarterly + annual workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,000–$17,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $7,000–$17,000 ad spend  |  Save $1,147/mo by bundling  |  20%–33.4% of revenue (under 35% cap)",
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
