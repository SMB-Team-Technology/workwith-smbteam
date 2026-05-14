"""
Sales Companion PDF — JJ Law (J. Jackson Law Offices, PLLC)
Sales Rep: Jonathan Farace  |  April 27, 2026
Internal use only. Do not share with client.
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

OUTPUT_PATH = "jj-law/JJLaw_April27_2026_Sales_Companion.pdf"


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

story.append(Paragraph("JJ Law (J. Jackson Law Offices, PLLC)", S["title"]))
story.append(Paragraph("Sales Companion  |  April 27, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
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
    [Paragraph("Jonathan Jackson", S["snap_value"]),
     Paragraph("$1.5M retained (2025)", S["snap_value"]),
     Paragraph("In-house intake + AI after-hrs", S["snap_value"]),
     Paragraph("4 — Small Biz Mgr", S["snap_value"]),
     Paragraph("~15% (default)", S["snap_value"]),
     Paragraph("Houston TX / OKC OK / Tulsa OK", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: REBUILD &amp; CEO", S["section"]))
story.append(Paragraph("Jonathan wants to rebuild from $1.5M to $2.5M — not by working harder, but by building a firm that generates cases without depending on his personal network.", S["subsection"]))

story.append(quote_block("I want to get to $2.5 million in retained fees this year — I've been there before and I know we can do it."))
story.append(Spacer(1, 1))
story.append(quote_block("Texas has been word-of-mouth, all referrals — the digital spend has been in Oklahoma."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Revenue rebuilt.</b> Get from $1.5M back to $2.5M in retained fees in 2026."))
story.append(bd("<b>Houston producing cases.</b> A digital engine in the firm's largest market that works without his personal network."))
story.append(bd("<b>CEO role.</b> Stop being the rainmaker; lead the firm strategically while the team runs operations."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Zero Houston digital presence.</b> Primary market runs entirely on referrals — no ads, LSAs, or SEO traction."))
story.append(b("<b>Intake conversion gap.</b> Signing 5–7 cases/month vs. 10 target — $25K–$42K/month in unrealized fees."))
story.append(b("<b>Fractured OKC spend.</b> $15.5K/month across agency digital and radio with no attribution data showing ROI."))
story.append(b("<b>AI invisibility.</b> Scored 10/100 — zero mentions on ChatGPT, Gemini, or Perplexity while competitors get recommended."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Houston generates PI cases from a digital engine for the first time — not from Jonathan's personal referral list."))
story.append(bd("OKC spend consolidates into one attributed campaign, replacing the fragmented agency arrangement with transparent ROI."))
story.append(bd("The Sneaker Lawyer brand gets deployed as paid media — NFL story, Thurgood Marshall, $70M+ recovered — in both markets."))

story.append(Paragraph("<b>Full Service Growth Marketing  |  $7,397/mo bundled</b>", S["subsection"]))
story.append(b("PI practice requires minimum Starter tier; Growth tier is correct for $1M–$3M revenue range."))
story.append(b("Houston (Tier 1) and OKC (Tier 4) require separate campaign builds with geo-specific strategy and budget allocation."))
story.append(b("Dual domains and stale directory NAP require SEO consolidation — this is a first-90-days deliverable."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Intake converts more leads already being generated — closes the 3–5 case/month gap without additional ad spend."))
story.append(bd("Jonathan shifts from rainmaker to CEO: KPI tracking and team accountability replace his calendar as the firm's engine."))
story.append(bd("The $2.5M goal gets a monthly roadmap with milestones — not just a number, a plan."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("5–7 cases/month vs. 10 target — intake audit and structured follow-up sequence closes this gap directly."))
story.append(b("Revenue dropped 50% from $3M to $1.5M; coaching builds the accountability structure to prevent a repeat."))
story.append(b("No confirmed intake KPIs or tracking — performance dashboard is a first-90-days priority."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("JJ Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Every dollar goes to a tracked channel — for the first time, Jonathan will know exactly which spend produces which cases."))
story.append(bd("Houston enters the paid search market for the first time, creating a case flow that does not depend on his personal relationships."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $12,000/mo — minimum viable spend across Houston and OKC PI channels."))
story.append(b("<b>Aggressive:</b> $20,000/mo — full budget to hit the $2.5M retained fee goal."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~6 cases x $8,375 = ~$50,000/mo vs. $12,000 spend = ~4x return (estimate)."))
story.append(b("<b>Aggressive:</b> ~12 cases x $8,375 = ~$100,000/mo vs. $20,000 spend = ~5x return (estimate)."))
story.append(Paragraph("<i>All figures are estimates based on industry CPL benchmarks and 15% default close rate. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> PI high-comp minimums: PPC $5,000 x2 markets + LSA $900 x2 + Meta $1,500 = ~$13,300; rounded to $12,000."))
story.append(b("<b>Aggressive:</b> $2.5M goal x 20% / 12 = $41,667; Houston Tier 1 weighting applied; rounded to $20,000 available."))
story.append(b("Aggressive total: $10,597 fees + $20,000 ads = $30,597 = 24.5% of monthly revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We\'re already spending $15K a month in Oklahoma — why spend more?"', S["objection_q"]))
story.append(Paragraph("The $15.5K has no confirmed attribution and the firm is not in the OKC 3-pack. SMB replaces fragmented spend with a unified, attributed campaign across both markets.", S["objection_a"]))

story.append(Paragraph('"The referral network in Houston is strong — I don\'t think we need ads there."', S["objection_q"]))
story.append(Paragraph("Zehl &amp; Associates has 1,922 reviews and dominates every Houston PI search. Sutliff &amp; Stout and Arnold &amp; Itkin run six-figure monthly budgets. Those cases go to them — not to referrals.", S["objection_a"]))

story.append(Paragraph('"We\'re already signing cases — is the intake really a problem?"', S["objection_q"]))
story.append(Paragraph("5–7 cases vs. a 10-case target means $25K–$42K/month in unrealized fees from leads already being generated — before any new marketing spend is added.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Growth Marketing</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("Multi-channel Houston + OKC PI campaigns: Google Ads, LSAs, Meta, SEO, AEO.", S["price_detail"]),
     Paragraph("<strike>$7,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, intake audit, KPI dashboard, team accountability framework.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$12,000–$20,000/mo", S["price_main"])],
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
    "Total: $10,597/mo + $12,000–$20,000 ad spend  |  Save $897/mo by bundling  |  18.1%–24.5% of revenue (under 35% cap)",
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
