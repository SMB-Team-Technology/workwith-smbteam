"""
Sales Companion PDF — Hayoon Kane Law Firm
Sales Rep: Nick Holderman
Date: June 25, 2026
FOR INTERNAL USE ONLY — DO NOT SHARE WITH PROSPECT
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

OUTPUT_PATH = "hayoon-kane/HayoonKaneLawFirm_06252026_Sales_Companion.pdf"


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
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=ACCENT_GREEN, spaceBefore=6, spaceAfter=2)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.5, leading=13, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9.5, leading=13, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9.5, leading=13, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9.5, leading=12, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9.5, leading=13, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8.5, leading=11, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


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


# ══════════════════════════════════════════════════════════
# PAGE 1
# ══════════════════════════════════════════════════════════
story = []

story.append(Paragraph("Hayoon Kane Law Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  June 25, 2026  |  Rep: Nick Holderman", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Hayoon Kane", S["snap_value"]),
     Paragraph("~$700K/yr", S["snap_value"]),
     Paragraph("5 people", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("~9% caller-hire", S["snap_value"]),
     Paragraph("Las Vegas, NV", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: MILESTONE + MISSION", S["section"]))
story.append(Paragraph("Reach $1.2–1.5M to buy a San Francisco home and serve the Korean immigrant community at scale.", S["subsection"]))
story.append(quote_block("20% book-to-hire conversion — and I do every consultation myself."))
story.append(Spacer(1, 1))
story.append(quote_block("Past Google Ads failed due to a broad, untargeted strategy."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Revenue milestone.</b> $1.5M/year funds the SF home purchase and expanded community impact."))
story.append(bd("<b>Personal time back.</b> Stop being required for every consultation."))
story.append(bd("<b>Higher-intent leads.</b> Replace Meta's low-intent social scrollers with Google searchers ready to hire."))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Single-channel dependency.</b> 100% of paid leads come from Meta — one algorithm change ends the pipeline."))
story.append(b("<b>Owner bottleneck.</b> Every consultation requires Hayoon; she is the firm's hard growth ceiling."))
story.append(b("<b>Bilingual staffing gap.</b> Finding English/Korean staff in Las Vegas is difficult; Consultation Specialist hire delayed."))
story.append(b("<b>Google Ads scar tissue.</b> Prior broad campaign failed; targeted Korean-language/T-Visa campaigns are a different product."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Adds Google Ads + LSA to Meta — captures high-intent T-Visa and Korean immigration searchers competitors are getting today."))
story.append(bd("Korean-language Google Ads in Las Vegas are uncontested — first firm to launch owns this audience."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$700K: Starter tier ($400K–$1M) is the correct fit."))
story.append(b("Includes Google Ads, LSA (Google Screened), and Meta management — all three channels."))
story.append(b("Stand-alone $5,697/mo; bundled saves $850/mo."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Builds the consultation framework so the Consultation Specialist hire ramps in weeks, not months."))
story.append(bd("Intake and conversion systems turn new Google leads into signed cases without Hayoon's personal time."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M: Elite Coach Plus is the correct tier."))
story.append(b("Includes weekly coaching, masterminds, quarterly and annual workshops."))
story.append(b("Stand-alone $3,497/mo; bundled saves $297/mo."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Hayoon Kane Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("<b>Conservative $3K/mo:</b> ~4 T-Visa cases/month = ~$44K new revenue. Launches in July when firm is ready to absorb leads."))
story.append(bd("<b>Aggressive $12K/mo:</b> ~18 cases/month targets $1.5M trajectory — requires Consultation Specialist in place."))

story.append(Paragraph("<b>Estimated ROI (all figures are estimates, not guaranteed):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~4 cases x $11K = ~$44K/mo vs. $3K spend = ~15x return."))
story.append(b("<b>Aggressive:</b> ~18 cases x $11K = ~$198K/mo vs. $12K spend = ~17x return."))
story.append(b("<b>Conservative calc:</b> Immigration minimums: Google PPC $1K + LSA $1K + Meta retargeting $200 + buffer = $3K."))
story.append(b("<b>Aggressive calc:</b> $1.35M goal x 20% / 12 x 1.3 (Tier 2) = $24.4K; capped at $12K for practical recommendation."))
story.append(b("Total SMB at aggressive: $20,047/mo = 34.4% of monthly revenue — under the 35% cap."))

story.append(thin_rule())

story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"We tried Google Ads before and they didn\'t work."', S["objection_q"]))
story.append(Paragraph("Her words: the prior campaign used a broad, untargeted strategy. Korean-language T-Visa Google Ads are a completely different product — and no Las Vegas competitor is currently running Korean-language Google Ads. This is not a repeat; it is a first-mover opportunity.", S["objection_a"]))

story.append(Paragraph('"I can\'t absorb more leads without hiring first."', S["objection_q"]))
story.append(Paragraph("Correct — and the coaching package delivers the consultation framework that makes the hire ramp in weeks. She has confirmed the firm can absorb leads in July. Campaigns and coaching launch together so the hire and the leads arrive in parallel.", S["objection_a"]))

story.append(Paragraph('"$8,047/mo is a lot when I\'m already spending $9,000 on Meta."', S["objection_q"]))
story.append(Paragraph("She already spends $9K/month closing at 20% booked-to-hired. Google searchers close at 3-5x higher rates. Conservative: 4 new T-Visa cases = $44K/month from $3K in new Google/LSA spend. The $8,047 adds Google + coaching on top of Meta — it does not replace it.", S["objection_a"]))

story.append(Paragraph('"Will this work for immigration and the Korean market?"', S["objection_q"]))
story.append(Paragraph("Her 159 Google reviews at 4.9 stars are the highest of any named Las Vegas immigration competitor (MC Law Group: 79 reviews). That is the foundation Google Screened requires. The Korean-language Google search space in Las Vegas has no confirmed competitors running ads. Her reviews are proof the market trusts her — Google Ads is how the market finds her.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads + LSA + Meta management + website optimization.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching + masterminds + quarterly and annual workshops.", S["price_detail"]),
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
    "Total: $8,047/mo + $3,000–$12,000 ad spend  |  Save $1,147/mo by bundling  |  19.0%–34.4% of revenue (under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
