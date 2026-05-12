"""
Sales Companion PDF — Beacon Legacy Group
SMB Team Internal Document — FOR INTERNAL USE ONLY
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

DARK_NAVY = HexColor("#1a2332")
ACCENT_GREEN = HexColor("#3B6D11")
MEDIUM_GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#888888")
RULE_GRAY = HexColor("#CCCCCC")
QUOTE_BG = HexColor("#F5F7F0")
WHITE = HexColor("#FFFFFF")
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "beacon-legacy-group/BeaconLegacyGroup_05072026_Sales_Companion.pdf"


def add_page_elements(canvas, doc):
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

S = {}
S["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=9.5, leading=13, textColor=LIGHT_GRAY, spaceAfter=3)
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=ACCENT_GREEN, spaceBefore=5, spaceAfter=2)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9, leading=11, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


def b(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY, spaceBefore=3, spaceAfter=3)

def quote_block(text):
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


# ════════════════════════════════════════════════════════
# PAGE 1
# ════════════════════════════════════════════════════════
story = []

story.append(Paragraph("Beacon Legacy Group", S["title"]))
story.append(Paragraph("Sales Companion  |  May 7, 2026  |  Rep: Dan Bryant", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Tyler Lannom", S["snap_value"]),
     Paragraph("$1.4M (2024)", S["snap_value"]),
     Paragraph("9 staff", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Cookeville, TN", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.7*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 3))

story.append(Paragraph("Dominant Buying Motive: FREEDOM FROM THE SEMINAR CIRCUIT", S["section"]))
story.append(Paragraph("Tyler wants a firm that generates consistent inbound leads automatically — so he can step off the stage and lead the business instead of running it.", S["subsection"]))

story.append(quote_block("Energy intensive — that’s the seminar model right now."))
story.append(Spacer(1, 1))
story.append(quote_block("Goal to reach $2–3M by diversifying channels. Can’t keep doing it this way."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Digital leads that replace the stage.</b> Every seminar costs a weekend — he wants Google to do that work."))
story.append(bd("<b>All three offices generating inbound.</b> Crossville and Mt. Juliet are digitally dark; he wants them as productive as Cookeville."))
story.append(bd("<b>Revenue that doesn’t swing month to month.</b> Seminar swings $30k–$60k; he wants predictability."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No multi-location digital infrastructure.</b> Crossville and Mt. Juliet have zero LSA, zero local SEO, near-zero reviews."))
story.append(b("<b>Seminar declining 12 consecutive months.</b> Primary revenue engine losing pressure with no replacement yet."))
story.append(b("<b>$18k+/mo in fragmented vendor spend.</b> No per-channel ROI — can’t know what’s working."))
story.append(b("<b>Both owners on the seminar circuit.</b> No one else can run it, so neither attorney can step back."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Replaces seminar-dependent revenue with three digital pipelines generating estate planning leads across all three markets around the clock."))
story.append(bd("Activates the probate/conservatorship PPC whitespace Tyler confirmed is uncontested — capturing high-intent Middle Tennessee searches before a competitor claims it."))

story.append(Paragraph("<b>Full Service Marketing Growth  |  $7,397/mo</b>", S["subsection"]))
story.append(b("Revenue $1.4M — Growth tier is correct for $1M–$3M; Essentials is ineligible above $1M."))
story.append(b("Three locations with no location-specific SEO require full-service (not ads-only) to build multi-location web and local search infrastructure."))
story.append(b("Meta Pixel already installed — retargeting audiences activate immediately within the package."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Connects Tyler with $1M+ firm owners who have already solved the seminar-to-digital transition — the shortcut, not the learning curve."))
story.append(bd("Gives the non-attorney SMB liaison a structured accountability framework so Tyler gains visibility without personal micromanagement."))

story.append(Paragraph("<b>Master’s Circle  |  $4,600/mo</b>", S["subsection"]))
story.append(b("Eligibility met: $1.4M revenue, 9 staff, dedicated non-attorney roles in place — Master’s Circle is the correct coaching tier."))
story.append(b("Includes weekly group coaching, masterminds, quarterly virtual workshops, and annual in-person workshop."))


# ════════════════════════════════════════════════════════
# PAGE 2
# ════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Beacon Legacy Group — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Launches paid coverage in LSA, probate PPC, and Meta retargeting — capturing estate planning families across all three markets the moment they search."))
story.append(bd("At $5k/mo recommended spend, estimated return is 3–5 cases/month x $9k avg = $27k–$45k vs. $5k spend = 5.4x–9x ROAS."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — Estate Planning minimums: PPC $1,500 + LSA $1,000 + Meta Retargeting $1,000."))
story.append(b("<b>Aggressive:</b> $8,000/mo — $2.5M goal x 20% ÷ 12 = $41,667. Tier 5 (0.85x), capped at Growth tier $10k; $8k used given Tyler’s stated preference for measured scaling."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative ($3,500):</b> ~23 leads x 15% = ~3 cases x $9,000 = $27,000/mo — 7.7x return."))
story.append(b("<b>Aggressive ($8,000):</b> ~53 leads x 15% = ~8 cases x $9,000 = $72,000/mo — 9x return."))
story.append(Paragraph("<i>All figures are estimates based on blended estate planning CPL benchmarks. Not guaranteed.</i>", S["disclaimer"]))
story.append(b("Total at $5k/mo: $5k ad + $7,397 mgmt + $4,600 coaching = $16,997/mo = 14.6% of revenue. Well under 35% cap."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We\'re already spending $18k/month on marketing."', S["objection_q"]))
story.append(Paragraph("SMB replaces the AI/avatar spend ($5k+) and underperforming seminar gap with attributable digital results. This is reallocation, not addition — and for the first time each dollar gets a channel attribution.", S["objection_a"]))

story.append(Paragraph('"The seminar still generates $30k/month — why change it?"', S["objection_q"]))
story.append(Paragraph("The seminar has declined 12 consecutive months at a 2.2x ROAS. The question is whether the digital replacement is built before the seminar stalls, not after. Waiting makes the transition more expensive.", S["objection_a"]))

story.append(Paragraph('"Vanderpool Law already has 138 reviews in Mt. Juliet — are we behind?"', S["objection_q"]))
story.append(Paragraph("Vanderpool operates from Franklin with a landing page; BLG has a physical office. Physical presence + SMB digital execution beats a remote competitor’s page. BLG can close the review gap in 6–9 months with a review velocity program.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Growth</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("Multi-location SEO, LSA mgmt, PPC, Meta retargeting, website rebuild.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>Master’s Circle</b>", S["price_main"]),
     Paragraph("$4,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,500–$8,000/mo", S["price_main"])],
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
    "Total: $11,997/mo + $3,500–$8,000 ad spend  |  14.6%–17.1% of revenue (well under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from PyPDF2 import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
