"""
Sales Companion PDF — SMB Team
Fiore Legal, Inc | July 1, 2026 | Rep: Randy Gold
Internal use only — do not share with client.
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

OUTPUT_PATH = "fiore-legal/FioreLegal_07012026_Sales_Companion.pdf"


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
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY,
                       spaceBefore=3, spaceAfter=3)

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

story.append(Paragraph("Fiore Legal, Inc", S["title"]))
story.append(Paragraph("Sales Companion  |  July 1, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Mauro Fiore Jr.", S["snap_value"]),
     Paragraph("~$1.5M est.", S["snap_value"]),
     Paragraph("9 attys, 8 offices", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("Los Angeles, CA", S["snap_value"])],
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

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: SCALE AND DOMINATE", S["section"]))
story.append(Paragraph("Mauro wants a firm that generates consistent case flow across all 8 locations without him personally driving every client relationship.", S["subsection"]))

story.append(quote_block("No transcript provided — DBM inferred from firm website and market research. Confirm on discovery call."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable case flow at scale.</b> A paid system generating leads across all 8 markets — not referrals or organic alone."))
story.append(bd("<b>A firm that runs without him.</b> 25 years and 9 attorneys should produce revenue without Mauro driving every relationship."))
story.append(bd("<b>Market dominance in LA PI.</b> His footprint and reputation should translate to digital dominance — not ceding ground to newcomers with bigger budgets."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No paid marketing system.</b> No Google Ads, LSA, or Meta confirmed — competitors own all paid visibility in his markets."))
story.append(b("<b>No intake coordination across 8 offices.</b> Leads likely lost with no visibility into how many or where."))
story.append(b("<b>No ops layer.</b> Mauro is the decision-maker for 9 attorneys across 8 offices — a ceiling on growth."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Launches paid case acquisition across all 8 markets — capturing high-intent PI and MVA searches competitors are currently winning."))
story.append(bd("Adds Spanish-language campaigns — Fiore's bilingual team and Spanish site are ready; CPLs run 20-40% lower than English with identical case values."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $7,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$1.5M — Growth tier is correct for $1M–$3M. Growth tier ad spend cap: $40,000/mo."))
story.append(b("PI in Tier 1 mega market (LA) — high-competitiveness floor applied; Spanish campaign multiplier also applies."))
story.append(b("8-location GBP optimization, local SEO, and city-specific landing pages all covered under one management fee."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Mauro the framework to build the ops layer, intake system, and financial visibility the firm needs to run at scale."))
story.append(bd("Peer network of PI firm owners at the same revenue and complexity level — people who have solved the same problems he is facing now."))

story.append(Paragraph("<b>Master's Circle  |  $4,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1.5M+, 9 attorneys — firm is above $1M threshold; Master's Circle is the appropriate coaching tier."))
story.append(b("No confirmed ops staff — coaching will provide the roadmap to build this layer; verify ops readiness with Randy Gold before finalizing."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Fiore Legal — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("At conservative, generates est. 5 signed cases/month = $37,500 revenue from ads — a 3.75x return on spend."))
story.append(bd("At aggressive, generates est. 28 cases/month = $210,000 revenue — a 5x return, dominating every market Fiore Legal serves."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $10,000/mo — MVA minimums: PPC $5,000 + LSA $2,000 + Meta $3,000."))
story.append(b("<b>Aggressive:</b> $40,000/mo — Growth tier cap; full depth across all markets and Spanish campaigns."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 5 cases x $7,500 = $37,500 vs. $10,000 spend = 3.75x. (CPL ~$261 w/ cushion; 15% close; default case value.)"))
story.append(b("<b>Aggressive:</b> 28 cases x $7,500 = $210,000 vs. $40,000 spend = 5.25x. (CPL ~$210; no cushion; English + Spanish.)"))
story.append(Paragraph("<i>Estimates only. Not guaranteed. Confirm revenue and case value on discovery call.</i>", S["disclaimer"]))

story.append(Paragraph("<b>Cap note:</b>", S["subsection"]))
story.append(b("At aggressive: $51,997 total (fees + ads) = 41.6% of estimated $125K/mo revenue — exceeds 35% cap. Confirm actual revenue; if above $1.5M estimate, this resolves."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We\'ve grown on referrals for 25 years — I\'m not sure paid ads will work for us."', S["objection_q"]))
story.append(Paragraph("Downtown LA Law Group has 624 Avvo reviews and a full paid marketing stack in every Fiore market. Sweet James has 600+ five-star reviews and multi-million dollar verdicts marketed digitally. Referrals built the firm — paid search is what wins in LA PI today. Spanish-language PI campaigns here show CPLs 20-40% below English with identical case values.", S["objection_a"]))

story.append(Paragraph('"The $11,997/month is a significant commitment."', S["objection_q"]))
story.append(Paragraph("Conservative scenario: 5 cases x $7,500 = $37,500/mo from ads on $10,000 spend — 3.75x return. Bundled pricing saves $1,997/month vs. retail. And a 25-year LA PI firm's average case value is likely above the $7,500 default — actual ROI will be higher.", S["objection_a"]))

story.append(Paragraph('"We don\'t have revenue figures ready."', S["objection_q"]))
story.append(Paragraph("Revenue estimated at ~$1.5M from team size. Getting the verified baseline is one of the explicit Master's Circle first-90-days deliverables. We start with the estimate and refine quickly — it doesn't block starting the marketing campaigns.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, Spanish campaigns, GBP optimization, SEO — all 8 markets.", S["price_detail"]),
     Paragraph("<strike>$8,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle</b>", S["price_main"]),
     Paragraph("$4,600/mo", S["price_main"])],
    [Paragraph("Weekly coaching, PI masterminds, quarterly workshops, annual in-person event.", S["price_detail"]),
     Paragraph("<strike>$4,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$10,000–$40,000/mo", S["price_main"])],
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
    "Total: $11,997/mo + $10,000–$40,000 ad spend  |  Save $1,997/mo by bundling  |  17.6%–41.6% of est. revenue (confirm actuals)",
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
