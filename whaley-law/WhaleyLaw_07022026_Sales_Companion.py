"""
Sales Companion PDF — Whaley Law
SMB Team | Jacob Meissner | July 2, 2026
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

OUTPUT_PATH = "whaley-law/WhaleyLaw_07022026_Sales_Companion.pdf"


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


# PAGE 1
story = []

story.append(Paragraph("Whaley Law", S["title"]))
story.append(Paragraph("Sales Companion  |  July 2, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Stewart Whaley", S["snap_value"]),
     Paragraph("$20–30K/mo (~$300K/yr)", S["snap_value"]),
     Paragraph("Solo (0 staff)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Little Rock, AR", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: FINANCIAL STABILITY + PERSONAL FREEDOM", S["section"]))
story.append(Paragraph("Stewart wants $1M/year so he can work 40 hours a week, take real vacations, and stop carrying the financial pressure of a solo practice alone.", S["subsection"]))

story.append(quote_block("$1M+ annual revenue to gain financial stability and personal freedom."))
story.append(Spacer(1, 1))
story.append(quote_block("Revenue doubled year-over-year — $15K/mo in June 2025 to $30K/mo in June 2026."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>$1M annual revenue.</b> Explicitly stated goal — the number he needs for family financial stability."))
story.append(bd("<b>A 40-hour work week and real vacations.</b> Stated directly on the call as the lifestyle target."))
story.append(bd("<b>Financial relief at home.</b> Supporting a spouse's new medical practice is adding household pressure."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No team.</b> Solo practice — every task (intake, admin, billing, legal work) falls on Stewart alone."))
story.append(b("<b>Website offline.</b> Expired SSL certificate has made whaley.law inaccessible to clients and Google."))
story.append(b("<b>18 reviews at 4.1★.</b> Invisible in the 3-pack; Lemley Law has 102 reviews at 4.9★ in Little Rock."))
story.append(b("<b>Underpriced felony cases.</b> $7,000 flat fee vs. $30,000 market rate caps income on every felony case."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Rebuilds the website and makes Whaley Law visible in Google search — the prerequisite for every other marketing channel."))
story.append(bd("Launches paid ads that fill the pipeline with traffic ticket and license defense leads while Stewart is in court."))
story.append(bd("Builds review volume and GBP presence to earn 3-pack and LSA placement over the next 6–12 months."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue band: $250K–$400K (transcript-verified: $20K–$30K/month current run rate)."))
story.append(b("Criminal defense + high competitiveness in Little Rock (Ludwig Law Firm, Thompson Law Firm PLLC active in Google Ads) hides Essentials — Starter is minimum."))
story.append(b("Website rebuild included as first deliverable — SSL fix + new site launches before ads go live."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Provides the pricing strategy and profitability framework to turn $300K in revenue into $1M — not just more clients, but more per client."))
story.append(bd("Weekly accountability and peer community for a solo practitioner making every business decision alone."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $250K–$400K → Elite Coach is correct tier (package_decision.json selected Elite Coach Plus in error based on HubSpot $570K estimate)."))
story.append(b("Weekly coaching, practice area masterminds, quarterly workshops, and one annual in-person summit."))
story.append(b("Felony pricing review is a priority first-session agenda item — moving from $7K toward $12K–$15K."))


# PAGE 2
story.append(PageBreak())

story.append(Paragraph("Whaley Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Provides a consistent inbound stream of traffic ticket and license defense leads that arrive even when Stewart is unavailable."))
story.append(bd("Generates the first real CPL data for the Little Rock market — the foundation for scaling spend as revenue grows."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,500/mo — Google Search for traffic tickets and professional license defense."))
story.append(b("<b>Aggressive:</b> $11,500/mo — 20% rule for $1M goal, within Starter tier cap ($15,000/mo)."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 5–6 cases x $1,600 avg = ~$8,500/mo vs. $5,500 spend = ~1.5x return. Estimate only."))
story.append(b("<b>Aggressive:</b> 13–14 cases x $1,700 avg = ~$22,000/mo vs. $11,500 spend = ~2.0x return. Estimate only."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Results vary by market and firm performance.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Traffic tickets + license defense Google Search minimums; blended CPL ~$156 with 20% cushion."))
story.append(b("<b>Aggressive:</b> $1M goal x 20% / 12 = $16,667. Little Rock Tier 4 (1.0x). Minus $4,847 fee = $11,820 → $11,500."))
story.append(b("35% cap note: At current $30K/mo, total including conservative ads = 43%. Recommend starting ads at $3K–$4K, scaling as revenue grows. At $50K/mo, total = 25.9% — well within cap."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I\'ve tried Facebook ads before and they didn\'t work."', S["objection_q"]))
story.append(Paragraph("Facebook boosts are not structured paid lead gen. Google Search ads capture people actively searching for a lawyer right now — high-intent, ready to hire. Previous attempts failed on the wrong channel, not because advertising doesn't work for Whaley Law.", S["objection_a"]))

story.append(Paragraph('"I can\'t afford this right now — money is tight."', S["objection_q"]))
story.append(Paragraph("Management fees alone ($7,447/mo) are 24.8% of current $30K revenue — within the 35% cap. Start with management fees + $3K in ads; scale as revenue grows. One coaching session on felony pricing ($7K → $12K+) can pay for the full investment on a single case.", S["objection_a"]))

story.append(Paragraph('"My website is down — I need to fix that first."', S["objection_q"]))
story.append(Paragraph("The website rebuild is the first deliverable in the Full Service Marketing package. We handle it — Stewart doesn't fix it separately. Ads launch as soon as the new site is live.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, Google Ads, LSA, local SEO, review generation, monthly reporting.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly coaching, practice area masterminds, quarterly workshops, annual in-person summit.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,500–$11,500/mo", S["price_main"])],
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
    "Total: $7,447/mo + $5,500–$11,500 ad spend  |  Save $1,747/mo by bundling  |  Sized for $1M growth trajectory",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
