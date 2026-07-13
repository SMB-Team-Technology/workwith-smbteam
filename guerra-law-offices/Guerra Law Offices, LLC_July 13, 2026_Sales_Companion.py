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

OUTPUT_PATH = "guerra-law-offices/Guerra Law Offices, LLC_July 13, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Guerra Law Offices, LLC", S["title"]))
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
    [Paragraph("Stella Guerra, Esq.", S["snap_value"]),
     Paragraph("$500,000", S["snap_value"]),
     Paragraph("Solo (1)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Warwick, RI", S["snap_value"])],
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
story.append(Paragraph("Stella wants a firm that generates and converts its own clients so she is no longer the single point of failure — freedom to step away, without giving up control by adding a partner.", S["subsection"]))

story.append(quote_block("A vacation requires pausing new business."))
story.append(Spacer(1, 1))
story.append(quote_block("Entirely from organic referrals."))
story.append(Spacer(1, 1))
story.append(quote_block("Scale as a solo practitioner, avoiding partnerships."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Double revenue.</b> Grow from $500K to $1M+ within 12 months, led by Personal Injury and Real Estate."))
story.append(bd("<b>Stay solo.</b> Scale without adding a partner."))
story.append(bd("<b>Real time off.</b> Take a vacation without the business grinding to a halt."))
story.append(bd("<b>Bilingual edge.</b> Leverage her English/Spanish skills as a market differentiator."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No paid lead gen.</b> 100% of new business is referrals she cannot control or scale."))
story.append(b("<b>No team.</b> She personally handles every case, call, and decision."))
story.append(b("<b>No review presence.</b> Zero reviews after 15+ years, versus competitors with 49-290."))
story.append(b("<b>Broken website.</b> Not mobile responsive, no contact form, no CTA."))
story.append(b("<b>No financial visibility.</b> No cost-per-case data by practice area."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Replaces referral dependency with a paid lead engine she owns and controls."))
story.append(bd("Gives her a mobile-ready, conversion-focused website that works while she's in court."))
story.append(bd("Opens the bilingual PI/RE lane no local competitor has claimed yet."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Personal Injury requires minimum Starter tier — Essentials is excluded for PI."))
story.append(b("Revenue of $500K falls in the $400K-$1M Starter tier band."))
story.append(b("Website needs a full rebuild (5+ years old, not mobile responsive) — requires Full Service, not ads-only."))
story.append(b("Starter's $25,000/mo ad spend cap covers both scenarios modeled below."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Builds the profit plan and cost-per-case visibility she currently has none of."))
story.append(bd("Gives her a structured path to delegate without adding a partner."))
story.append(bd("Connects her with peer masterminds of other solo/small-team owners scaling the same way."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue of $500K falls in the $400K-$1M / Any team size band for Elite Coach Plus."))
story.append(b("Fractional CFO/COO products are excluded — revenue is under $1M."))
story.append(b("Team size is 1 (solo) — Master's Circle is excluded (requires 5+ staff)."))
story.append(b("No profitability data exists yet; coaching builds that visibility before adding fractional advisors later."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Guerra Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Converts Personal Injury and Real Estate into a predictable monthly case pipeline instead of a referral guessing game."))
story.append(bd("Moves toward her stated targets — PI 10 to 20 cases/mo, RE 20 to 50 cases/mo — with a channel mix built for Warwick/Providence."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,500/mo — minimum viable spend across recommended channels."))
story.append(b("<b>Aggressive:</b> $25,000/mo — full budget to hit growth goals, at the Starter tier's spend cap."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~2 cases x $6.5K = ~$13K/mo vs. $7.5K spend = ~1.7x return."))
story.append(b("<b>Aggressive:</b> ~8-9 cases x $6.5K = ~$55.25K/mo vs. $25K spend = ~2.2x return."))
story.append(Paragraph("<i>All figures are estimates using a default 15% close rate and default $6.5K PI case value — neither confirmed by the firm. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Accident & Injury blended CPL across Google/LSA/Meta with 20% cushion (~$530/lead); $7,500 / $530 = ~14 leads x 15% close = ~2 cases."))
story.append(b("<b>Aggressive:</b> Pipeline-set $25,000/mo (matches Starter tier's ad spend cap); blended CPL ~$440/lead (no cushion) = ~57 leads x 15% close = ~8-9 cases."))
story.append(b("<b>Flag:</b> Total spend at aggressive ($8,047 mgmt + $25,000 ads = $33,047/mo) is ~79% of current $41,667/mo revenue — over the 35% cap. Review with client before presenting the aggressive number."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"We\'ve grown to $500K on referrals alone — why pay for ads now?"', S["objection_q"]))
story.append(Paragraph("Referrals got her to $500K, but named PI competitors in Warwick — Rob Levine Law (290 reviews, 4.9★) and d'Oliveira & Associates (235 reviews, 4.9★) — have a review and ad advantage that grows every month she has no paid channel of her own.", S["objection_a"]))

story.append(Paragraph('"I don\'t have anyone to answer more calls if ads bring in more leads."', S["objection_q"]))
story.append(Paragraph("Fixing intake is built into the first 90 days, and Elite Coach Plus builds the delegation plan — so more leads doesn't mean more of her personal time.", S["objection_a"]))

story.append(Paragraph('"$8,047/month plus ad spend feels like a lot for a solo practice."', S["objection_q"]))
story.append(Paragraph("The Starter marketing bundle alone saves $850/mo versus stand-alone pricing, and Elite Coach Plus saves another $297/mo — $1,147/mo in bundled savings before ad spend is even considered.", S["objection_a"]))

story.append(Paragraph('"How do I know the ad spend will pay off?"', S["objection_q"]))
story.append(Paragraph("Even the conservative $7,500/mo scenario is projected to return $13,000/mo in new case revenue (1.7x) using industry-standard defaults, with upside as her review count and organic presence grow.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, Google Ads, LSA, Meta ads, local SEO for PI + RE.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, masterminds, quarterly + annual workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,500–$25,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $7,500–$25,000 ad spend  |  Save $1,147/mo by bundling  |  37.3%–79.3% of revenue (aggressive exceeds 35% cap — flag with client)",
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
