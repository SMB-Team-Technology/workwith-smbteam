"""
Sales Companion PDF — Just Jurist Law Firm, PLLC
SMB Team | Dan Bryant | May 12, 2026
FOR INTERNAL USE ONLY — DO NOT SHARE WITH CLIENT
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

OUTPUT_PATH = "just-jurist-law-firm/JustJuristLawFirm_May12_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Just Jurist Law Firm, PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  May 12, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Pablo Gonzalez Zepeda", S["snap_value"]),
     Paragraph("~$400K–$600K est.", S["snap_value"]),
     Paragraph("3 (atty + paralegal)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Miami, FL", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.7*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 2))

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: AUTONOMY", S["section"]))
story.append(Paragraph("Pablo wants a firm that runs without him so he can stop attending board meetings every evening.", S["subsection"]))

story.append(quote_block("Goal: make the firm autonomous to reduce my workload, not just increase revenue. Seeking to step out of the nucleus."))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Evening freedom.</b> Board meetings every evening are his single biggest personal constraint."))
story.append(bd("<b>An A-player associate</b> experienced enough to handle board meetings and client work independently."))
story.append(bd("<b>A firm on systems</b> — not dependent on Pablo's presence at every client decision."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No lead gen.</b> 40 associations came from inherited books — no pipeline Pablo controls exists."))
story.append(b("<b>Hiring fear.</b> No financial model to de-risk the hire; worried the associate will leave to compete."))
story.append(b("<b>Zero digital presence.</b> No GBP, no reviews, invisible in local search for his own practice area."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("<b>Funds the hire</b> — consistent new inquiries give Pablo the financial confidence to bring on the A-player."))
story.append(bd("<b>Makes Just Jurist findable</b> — GBP + reviews from 40 clients beats ALG's 2.9-star profile in search."))

story.append(Paragraph("<b>Full Service Marketing Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$600K — Starter tier correct; under $1M threshold."))
story.append(b("Zero paid ads confirmed — Google Ads, GBP, LSA, and Meta all unbuilt from scratch."))
story.append(b("Spanish campaign needed — bilingual firm in a heavily Spanish-speaking Miami condo market."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("<b>Builds the delegation protocol</b> — board meeting handoff requires a defined system; coaching builds it."))
story.append(bd("<b>Peer group for stepping out of the nucleus</b> — Pablo said he wants this mastermind; this is it."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M — correct non-marketing tier; under $1M rules out Master's Circle."))
story.append(b("Fractional exec 1–2 hrs/week builds delegation protocols Pablo cannot create alone."))
story.append(b("Weekly coaching + workshops match the peer accountability Pablo said he is seeking."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Just Jurist Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("<b>Funds the hire.</b> 1–4 new associations per month at $9,000 first-year retainer value generates $13,500–$33,750 in monthly revenue from ads alone — more than enough to cover an associate's salary."))
story.append(bd("<b>Replaces the ceiling.</b> Pablo's current growth ceiling is inherited books and referrals; paid ads create a predictable new-client pipeline that removes that ceiling permanently."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $2,500/mo — minimum viable spend; Google PPC $1,500 + LSA $1,000."))
story.append(b("<b>Aggressive:</b> $5,000/mo — Starter tier cap; Miami Tier 2 market (1.3x multiplier applied)."))

story.append(Paragraph("<b>Estimated ROI (all figures are estimates):</b>", S["subsection"]))
story.append(b("<b>Conservative ($2,500/mo):</b> 10 leads x 15% = 1–2 associations x $9K = $13,500/mo. Return: 5.4x."))
story.append(b("<b>Aggressive ($5,000/mo):</b> 25 leads x 15% = 3–4 associations x $9K = $33,750/mo. Return: 6.75x."))
story.append(Paragraph("<i>Case value = first-year retainer $750/mo. Close rate defaulted 15%. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>Calculation basis:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Business Law minimums — PPC $1,500 + LSA $1,000 = $2,500."))
story.append(b("<b>Aggressive:</b> $1M goal x 20% / 12 = $16,667. Miami Tier 2 (1.3x) = $21,667. Capped at Starter $5,000."))
story.append(b("Total aggressive: $8,047 + $5,000 ads = $13,047/mo = ~31.3% of revenue. Under 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"Spending $8,000/month on ads is ridiculous — my peers are throwing money away."', S["objection_q"]))
story.append(Paragraph("We are recommending $2,500 to start — not $8,000. At 5.4x estimated return, one new association covers the spend in month one and recurs for the full contract life.", S["objection_a"]))

story.append(Paragraph('"What if the associate I hire leaves and starts competing with me?"', S["objection_q"]))
story.append(Paragraph("That is a hiring design problem, not a revenue problem. Our coaching covers A-player hiring, non-compete structuring, and retention systems. Not hiring means Pablo is at every board meeting indefinitely.", S["objection_a"]))

story.append(Paragraph('"I already have 40 clients — do I really need marketing?"', S["objection_q"]))
story.append(Paragraph("Those 40 came from inherited books — not a system Pablo controls. Association Law Group added 100+ new associations in March 2026. The market is moving; standing still means falling behind.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, GBP, review acquisition, LSA, Facebook/Instagram, Spanish campaign.", S["price_detail"]),
     Paragraph("<strike>$6,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, masterminds, quarterly workshops, fractional exec 1-2 hrs/week.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$2,500–$5,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $2,500–$5,000 ad spend  |  Save $2,147/mo by bundling  |  ~31% of revenue (under 35% cap)",
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
