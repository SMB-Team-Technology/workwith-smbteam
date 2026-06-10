"""
Sales Companion PDF — Law Offices of David Bliven
Sales Rep: Dan Bryant | Date: June 12, 2026
SMB Team — Internal Use Only
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

OUTPUT_PATH = "law-offices-of-david-bliven/Law_Offices_of_David_Bliven_06122026_Sales_Companion.pdf"


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

story.append(Paragraph("Law Offices of David Bliven", S["title"]))
story.append(Paragraph("Sales Companion  |  June 12, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("David Bliven", S["snap_value"]),
     Paragraph("$500K–$1M est.", S["snap_value"]),
     Paragraph("5 (+assoc. Aug)", S["snap_value"]),
     Paragraph("4 — SM Mgr", S["snap_value"]),
     Paragraph("15% / 40–73% NS", S["snap_value"]),
     Paragraph("White Plains + Bronx, NY", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.9*inch, 0.8*inch, 1.0*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 3))

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: FREEDOM + FINANCIAL STABILITY", S["section"]))
story.append(Paragraph("Build a firm that runs without him as the firefighter — restore cash cushion, pay himself properly, hit $2M–$2.5M by 2027.", S["subsection"]))

story.append(quote_block("Desired outcome: on track to $2.0–$2.5M by 2027; add office manager, 3 VAs, 3 paralegals, 1–2 associates; restore cash cushion; pay self properly."))
story.append(Spacer(1, 1))
story.append(quote_block("Sep: 68 set/30 completed; Oct: 42/15; Nov: 43/14; Dec: 73% no-show"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Pay himself properly.</b> Cash cushion drained; underpaying himself despite growing revenue."))
story.append(bd("<b>Systems so the firm runs without him.</b> KPIs and delegation — attorney, not manager."))
story.append(bd("<b>August associate hire succeeds.</b> Onboarding framework and accountability structure built before the hire."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>40–73% no-show rate.</b> Four months of declining show rate; leads arriving but not converting."))
story.append(b("<b>No KPIs anywhere.</b> No benchmarks for intake, paralegals, or incoming associate."))
story.append(b("<b>Paralegals billing 10 hrs/week at $300/hr.</b> $50K+ monthly billing capacity unused."))
story.append(b("<b>$100K+ AR, no collections system.</b> ~$50K collectible — money earned but not in the bank."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("<b>Turns 147 reviews into rankings.</b> NAP cleanup converts existing review dominance into local pack visibility."))
story.append(bd("<b>More calls, same budget.</b> Campaign optimization raises conversion from the existing 15% floor."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M (est. $750K) — Starter tier correct. No escalation required."))
story.append(b("Firm already on SMB Team marketing; package continues and optimizes the active program."))
story.append(b("Tier 2 market (Westchester/White Plains) — Starter's $15K ad spend cap is appropriate."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("<b>Fixes intake without more ad spend.</b> Clio Grow configuration + KPI framework recovers no-show revenue."))
story.append(bd("<b>Makes the August hire a win.</b> Onboarding framework built before the associate starts."))
story.append(bd("<b>Unlocks paralegal billing capacity.</b> Utilization system recovers $50K+/mo already on payroll."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M, growing team — Elite Coach Plus is correct coaching tier."))
story.append(b("FCOO Advisor considered; recommended as Phase 2 upgrade at $1.2M+ revenue."))
story.append(b("Confirm with Dan Bryant: FCOO may belong in initial proposal given August hire urgency."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Law Offices of David Bliven — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("<b>Top of Google for Westchester family law.</b> Reaches the 85% of prospects who don't call from a referral."))
story.append(bd("<b>Predictable lead flow to $2M.</b> Scalable channel mix David doesn't manage personally."))

story.append(Paragraph("<b>Range: $3,500 (conservative) to $14,000 (aggressive)/mo</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Family Law minimums — PPC $2,500 + LSA $1,000 = $3,500."))
story.append(b("<b>Aggressive:</b> $750K x 20% / 12 x Tier 2 (1.3x) = $16,250; capped at Starter $14K limit."))

story.append(Paragraph("<b>Estimated ROI (not guaranteed):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~15 leads x 20% close x $25K = ~$62,500/mo vs. $3,500 = ~18x return."))
story.append(b("<b>Aggressive:</b> ~55 leads x 20% close x $25K = ~$262,500/mo vs. $14,000 = ~19x return."))
story.append(b("At aggressive: $8,047 fees + $14,000 ads = $22,047/mo = 35.3% of est. revenue — confirm rev first."))
story.append(Paragraph("<i>Case value $25K and close rate 20% from transcript. All figures are estimates.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We are already on SMB Team marketing."', S["objection_q"]))
story.append(Paragraph("Same program — this continues it. The audit shows where the investment is being lost: NAP inconsistency suppresses 147 reviews from ranking, and 40–73% no-shows absorb lead cost without converting.", S["objection_a"]))

story.append(Paragraph('"The problem is operations, not marketing."', S["objection_q"]))
story.append(Paragraph("Elite Coach Plus IS the operations fix. Clio Grow configuration, intake KPI dashboard, paralegal utilization system, and August associate onboarding are all coaching deliverables. That is what converts 15% close rate to 25%+.", S["objection_a"]))

story.append(Paragraph('"I cannot afford $8,047/month right now."', S["objection_q"]))
story.append(Paragraph("Conservative total is $11,547/mo vs. ~$62,500 ad revenue = 18x return. Plus the AR collections workflow recovers ~$50K in collectible revenue already earned in the first 90 days. It funds itself if intake improves.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Virtual Video Growth, SEO, NAP cleanup, GBP management.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, intake KPIs, paralegal utilization, associate onboarding framework, quarterly workshops.", S["price_detail"]),
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
    "Total: $8,047/mo + $3,500–$14,000 ad spend  |  Save $1,147/mo by bundling  |  18.5%–35.3% of revenue (confirm rev before presenting)",
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
