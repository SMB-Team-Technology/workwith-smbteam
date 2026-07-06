"""
Sales Companion PDF — Abogada Vida PLLC
SMB Team Internal Document
Sales Rep: Dan Bryant | Date: July 13, 2026
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

OUTPUT_PATH = "abogada-vida/AbogadaVida_07132026_Sales_Companion.pdf"


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

story.append(Paragraph("Abogada Vida PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  July 13, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Mahsa Mohkamkar", S["snap_value"]),
     Paragraph("~$600K est.", S["snap_value"]),
     Paragraph("9 total", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("40.7% signing", S["snap_value"]),
     Paragraph("Schnecksville, PA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE AND FREEDOM", S["section"]))
story.append(Paragraph("Mahsa wants a $1M/$3M/$7M multi-attorney firm that runs without her — and time back as a result.", S["subsection"]))

story.append(quote_block("Attorney hiring cost: $140k salary + benefits = ~$200k total cost"))
story.append(Spacer(1, 1))
story.append(quote_block("Vivid Vision: $1M in year 1, $3M in year 2, $7M in year 3"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Second attorney.</b> 30% of leads referred out — needs removal defense capacity to stop giving away high-value cases."))
story.append(bd("<b>Predictable lead flow.</b> No confirmed active ads; needs campaigns that produce cases consistently."))
story.append(bd("<b>Intake that converts.</b> Karen books 66%; firm averages 20% — wants the whole team at Karen's level."))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No paid campaigns active.</b> Competitors hold Allentown 3-pack while firm has no confirmed Google Ads, LSA, or Meta presence."))
story.append(b("<b>Solo attorney bottleneck.</b> All cases require Mahsa — cannot scale past her individual capacity."))
story.append(b("<b>PageSpeed unconfirmed.</b> Site load ~14s; API rate-limited during research — verify at pagespeed.web.dev before call."))
story.append(b("<b>Revenue estimate only.</b> No explicit annual figure; ~$600K from 3 months of data. Confirm actual revenue on call."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Spanish-language family immigration ads capture high-intent prospects in an unclaimed channel at $3–$6 CPC."))
story.append(bd("LSA enrollment converts 96 five-star reviews into pay-per-call leads above all organic results."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$600K ($400K–$1M band): Starter tier is the correct level."))
story.append(b("Website rebuild needed: ~14s load, no embedded form, no geo-targeted pages — Starter includes full rebuild."))
story.append(b("Conservative ad spend $3,000/mo; aggressive $12,000/mo (Starter cap). Upgrade to Growth at $1M revenue."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Replicates Karen's 66% booking process across all three intakers — the fastest revenue lever with no new marketing spend."))
story.append(bd("Builds the financial model that de-risks the $200K attorney hire and determines the case volume trigger to pull it."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M, team of 9: Elite Coach Plus is correct; Master's Circle requires $1M+."))
story.append(b("Intake coaching is the first priority: 39-point gap between top and bottom intaker needs a scripted solution."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Abogada Vida PLLC — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Activates paid leads in the Spanish-language immigration channel — uncaptured in the Allentown market, lowest CPC competition."))
story.append(bd("Fills case volume at a projected 3–5x return on spend — making the $200K attorney hire financially viable sooner."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000/mo — immigration minimums: Google PPC $1,000 + LSA $1,000 + Meta $1,000."))
story.append(b("<b>Aggressive:</b> $12,000/mo — Starter tier cap; full 20% rule + Spanish multiplier yields $17,320, capped at $12,000."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~2–3 cases x $5,000 = $10K–$15K/mo vs. $3,000 spend = 3.3–5x. (Est.)"))
story.append(b("<b>Aggressive:</b> ~7–9 cases x $5,000 = $35K–$45K/mo vs. $12,000 spend = 3–4x. (Est.)"))
story.append(Paragraph("<i>All figures are estimates. Case value based on inferred ~$5,000 avg. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Google PPC $1,000 + LSA $1,000 + Meta retargeting $200 + Meta lead gen $800 = $3,000."))
story.append(b("<b>Aggressive:</b> $1M x 20% / 12 = $16,667. Tier 4 (1.0x). Spanish (1.33x) = $22,167. Minus $4,847 = $17,320. Cap: $12,000."))
story.append(b("Total at aggressive: $12,000 + $4,847 = $16,847/mo = ~28% of revenue. Under 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I need to hire an attorney before I invest in marketing."', S["objection_q"]))
story.append(Paragraph("Marketing comes first. The $200K attorney hire only makes sense when case volume justifies it — and that volume requires a lead system. Ads now create the cases that make the attorney hire profitable, not the other way around.", S["objection_a"]))

story.append(Paragraph('"My intake is already good — Karen has a 66% booking rate."', S["objection_q"]))
story.append(Paragraph("Karen is excellent, but the firm averages 20%. May had 177 leads and ~35 consultations. At Karen's rate that is 117 consultations, 47 cases, and ~$173K additional monthly revenue potential — with no new marketing spend.", S["objection_a"]))

story.append(Paragraph('"We\'ve tried ads before and cut back."', S["objection_q"]))
story.append(Paragraph("Ads were cut for referred-out case types (removal/detainee) — not family immigration. Spanish-language family immigration PPC is a different campaign in a largely uncaptured channel. The referral constraint does not apply here.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, bilingual Google Ads, LSA, Meta, local SEO.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, intake conversion, masterminds, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000–$12,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $3,000–$12,000 ad spend  |  Save $1,147/mo by bundling  |  18.4%–27.6% of revenue (under 35% cap)",
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
