"""
Sales Companion PDF — Smith & Company PLLC
Sales Rep: Jacob Meissner  |  April 27, 2026
INTERNAL USE ONLY — DO NOT SHARE WITH CLIENT
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

OUTPUT_PATH = "smith-company/Smith_Company_PLLC_04272026_Sales_Companion.pdf"


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

story.append(Paragraph("Smith &amp; Company PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  April 27, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Eon Smith", S["snap_value"]),
     Paragraph("~$250K/yr", S["snap_value"]),
     Paragraph("Eon + Kim + PT", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("~15%", S["snap_value"]),
     Paragraph("Hartford, CT / NY", S["snap_value"])],
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
story.append(Paragraph("Eon wants to stop being the ceiling of his own firm — he wants a business that runs without him in every role.", S["subsection"]))

story.append(quote_block("My goal is to be the law firm CEO — I own the business, I don't run it."))
story.append(Spacer(1, 1))
story.append(quote_block("I'm working 60-plus hours a week and it's all on me — intake, cases, court, everything."))
story.append(Spacer(1, 1))
story.append(quote_block("I want to add $350,000 in revenue in 2026 and double that by 2027."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>40-hour weeks.</b> Work fewer hours, not more, as revenue grows."))
story.append(bd("<b>Cases without asking.</b> Federal criminal and removal cases from a system, not referrals."))
story.append(bd("<b>Kim on intake.</b> She is already there — he just needs the script and structure."))
story.append(bd("<b>A hiring plan.</b> Full-time hire by EOY 2026 — needs the financial blueprint to do it with confidence."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No digital presence.</b> ~2 reviews, 3 competing websites, zero paid ads — invisible for the cases he wants."))
story.append(b("<b>Eon is the intake system.</b> All calls go to him personally — no coverage when he is in court."))
story.append(b("<b>Competitors are far ahead.</b> Norte has 228 reviews, Ruane has 1,000+ — both capturing cases Eon is not visible for."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Federal criminal and removal cases arrive from Google — not from Eon making calls."))
story.append(bd("A consolidated, rebuilt website at smithelaw.com captures leads 24/7, including when Eon is in court."))
story.append(bd("The review gap to Norte closes systematically — Eon stops losing cases to competitors at the search result stage."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $2,847/mo bundled</b>", S["subsection"]))
story.append(b("Criminal Defense + High competitiveness blocks all Essentials tiers — Starter is minimum eligible."))
story.append(b("3 competing websites require consolidation and full rebuild — ads-only cannot fix the domain authority split."))
story.append(b("Immigration LSA is underutilized in Hartford — early-mover advantage available right now."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Kim becomes the intake owner — Eon stops being the first person every prospect talks to."))
story.append(bd("The 2026 full-time hire happens on a plan, not a hope — Elite Coach builds the hiring blueprint so Eon makes that decision with a financial model, not a gut feeling."))
story.append(bd("Revenue tracking by case type goes live from day one — Eon knows which practice area is more profitable within 90 days."))

story.append(Paragraph("<b>Elite Coach  |  $1,400/mo bundled</b>", S["subsection"]))
story.append(b("Revenue under $500K rules out FCOO and FCFO — Elite Coach is the correct package at this stage."))
story.append(b("Kim is on the team; the gap is process — coaching builds intake around the person already in place."))
story.append(b("$350K goal in 2026 has no financial model behind it — coaching builds that model before marketing dollars flow."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Smith &amp; Company PLLC — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("At conservative spend, Eon gets 1–2 retained cases per month from ads alone — that is $5,100–$10,200 in new revenue from a $2,000 investment."))
story.append(bd("At aggressive spend, the 2 federal criminal + 3 removal cases per month goal becomes mathematically achievable within the first year."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $2,000/mo — minimum viable spend across immigration PPC, LSA, and Meta retargeting."))
story.append(b("<b>Aggressive:</b> $3,000/mo — adds criminal defense PPC and increases immigration spend to pursue full case volume goal."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~11 leads x 15% close = 1–2 cases x $5,100 avg = ~$5,100–$10,200/mo vs. $2,000 spend = 2.5x–5.1x return."))
story.append(b("<b>Aggressive:</b> ~20 leads x 15% close = 3 cases x $5,100 avg = ~$15,300/mo vs. $3,000 spend = 5.1x return."))
story.append(Paragraph("<i>All figures are estimates based on industry averages and market data. Not guaranteed. Case value is a blended default (federal criminal $6,000 + removal defense $4,500); confirm actual average fees with Eon.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Immigration PPC $1,000 + LSA $500 + Meta retargeting $500 = $2,000/mo."))
story.append(b("<b>Aggressive:</b> $600K x 20% ÷ 12 = $10,000. Tier 4 (1.0x). Minus $2,847 fee = $7,153 available. Capped at $3,000 to stay under 35% cap at current revenue."))
story.append(b("$4,247 + $3,000 = $7,247/mo = 34.8% of revenue — within the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I\'ve built to $250K on referrals — I\'m not sure I need ads."', S["objection_q"]))
story.append(Paragraph("Norte has 228 reviews and owns Hartford removal defense search. Ruane has 1,000+ and owns criminal. Referrals built $250K — ads are what builds $600K. The question is whether to act before or after competitors lock up the market.", S["objection_a"]))

story.append(Paragraph('"I\'m already at 60+ hours — I don\'t have bandwidth for more leads."', S["objection_q"]))
story.append(Paragraph("That is exactly why coaching and marketing start simultaneously. Kim owns intake before leads arrive — the system is built first. Elite Coach runs in parallel so volume and process scale together.", S["objection_a"]))

story.append(Paragraph('"$4,247 a month feels like a lot for a firm our size."', S["objection_q"]))
story.append(Paragraph("One retained case per month from ads covers the full SMB investment at a $5,100 blended case value. Conservative projections show 1–2 cases/month — the program pays for itself at the low end.", S["objection_a"]))

story.append(Paragraph('"What if Kim can\'t handle intake alone?"', S["objection_q"]))
story.append(Paragraph("Elite Coach builds her script, qualification criteria, and follow-up sequence — she is trained into it, not thrown into it. The system does the heavy lifting.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$2,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, Google Ads, LSA, Local SEO, review generation — all channels.", S["price_detail"]),
     Paragraph("<strike>$3,397</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$1,400/mo", S["price_main"])],
    [Paragraph("Intake system build, hiring blueprint, financial tracking, KPI dashboard.", S["price_detail"]),
     Paragraph("<strike>$1,600</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$2,000–$3,000/mo", S["price_main"])],
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
    "Total: $4,247/mo + $2,000–$3,000 ad spend  |  Save $750/mo by bundling  |  30.0%–34.8% of revenue (under 35% cap)",
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
