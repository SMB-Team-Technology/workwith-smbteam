"""
Sales Companion PDF — Kopchian Law (July 30, 2026)
========================================
Generated from sales_companion_template.py. Layout, colors, fonts, and
structure are unmodified — only content placeholders were filled in.

Output filename: Kopchian Law_July 30, 2026_Sales_Companion.pdf
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

OUTPUT_PATH = "kopchian-law/Kopchian Law_July 30, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Kopchian Law", S["title"]))
story.append(Paragraph("Sales Companion  |  July 30, 2026  |  Rep: Nick Holderman", S["subtitle"]))
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
    [Paragraph("Adam Kopchian", S["snap_value"]),
     Paragraph("~$286K/yr", S["snap_value"]),
     Paragraph("Solo (1)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Brooklyn, NY", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: OWNERSHIP / FINANCIAL BUFFER", S["section"]))
story.append(Paragraph("Adam wants to move from player to owner — escaping the day-to-day production bottleneck so the firm builds a real financial buffer instead of running on credit cards.", S["subsection"]))

story.append(quote_block("Growth is limited to referrals and upsells... there is no website or active marketing."))
story.append(Spacer(1, 1))
story.append(quote_block("Weekly revenue of $5,000-$6,000 is insufficient to meet debt obligations, leading to business expenses being put on credit cards."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Become the owner, not just the player.</b> Move from doing every case himself to running a firm."))
story.append(bd("<b>A real financial buffer.</b> The $7-8K/week goal exists to cover debt and stop using credit cards."))
story.append(bd("<b>Systems before spend.</b> He asked for operations fixed first — marketing without them would waste ad spend."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No website at all.</b> Domain is parked at a GoDaddy placeholder — no destination for any lead source."))
story.append(b("<b>No cash cushion.</b> Weekly revenue already falls short of debt obligations."))
story.append(b("<b>Zero staff.</b> Every task in the firm runs through Adam personally."))
story.append(b("<b>1.0-star Google rating.</b> Two reviews describe him as lacking confidence — a live reputation problem."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives the firm a real website for the first time — the prerequisite for every other lead channel."))
story.append(bd("Fixes the NAP inconsistency and 1.0-star GBP that are actively repelling searchers right now."))

story.append(Paragraph("<b>Full Service Marketing — Essentials  |  $3,497/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$286K is under the $750K Essentials ceiling; single location + single practice area (Immigration) qualify."))
story.append(b("Corrects Pass 1's package_decision.json error, which incorrectly flagged multiple practice areas and selected Starter."))
story.append(b("Ad cap is $5,000/mo — aggressive spend ($6,000/mo) exceeds it by ~$1,000-1,250; confirm 10% overage before running it."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the intake process and delegation plan Adam said he needs before marketing spend makes sense."))
story.append(bd("Starts the path from player to owner — the exact shift he described wanting on the call."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$286K falls in the $250K-$400K band for Elite Coach, not Elite Coach Plus ($400K-$1M)."))
story.append(b("Corrects Pass 1, which had incorrectly used the $400K-$1M Elite Coach Plus band."))
story.append(b("Fractional CFO and Legal AI Workforce are both not eligible — revenue and staffing don't reach the minimums."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Kopchian Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts new cases in front of Adam without requiring more of his own time chasing referrals."))
story.append(bd("Starts small enough that it will not compound the credit-card cash pressure he is under."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000/mo — Google Search only, the absolute floor, chosen over the $9,200 four-channel-minimum sum due to the budget-reality override."))
story.append(b("<b>Aggressive:</b> $6,000/mo — blended Google Search + LSA + Meta Cold, sized to the stated $7-8K/week revenue goal."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~4 cases x $4.5K = ~$18K/mo vs. $3K spend = ~6.0x return."))
story.append(b("<b>Aggressive:</b> ~11 cases x $4.5K = ~$49.5K/mo vs. $6K spend = ~8.3x return."))
story.append(Paragraph("<i>Estimates use practice-area default case value ($4,500) and close rate (15%) — not stated on the call.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Full 4-channel Immigration minimum ($9,200) was considered and rejected as unaffordable right now."))
story.append(b("<b>Aggressive:</b> $390K goal midpoint x 20% / 12 = $6,500. Tier 1 NYC (1.5x) = $9,750. Minus $3,497 fee = ~$6,253, rounded to $6,000."))
story.append(b("At aggressive, total spend is ~46.5% of current revenue — above the 35% cap. Flag for scoping approval (revenue is under $300K threshold)."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I can\'t afford fees plus ad spend right now — I\'m already behind on debt."', S["objection_q"]))
story.append(Paragraph("That's why we start with the $3,000/mo conservative spend, not aggressive — investment stays low while fixing the website and reputation first.", S["objection_a"]))

story.append(Paragraph('"Why do I need marketing if my systems aren\'t fixed yet?"', S["objection_q"]))
story.append(Paragraph("You're right — Elite Coach and the website rebuild come first; ads only launch once there's a real site to send traffic to.", S["objection_a"]))

story.append(Paragraph('"I already tried coaching programs and couldn\'t keep up."', S["objection_q"]))
story.append(Paragraph("Elite Coach is built for solo capacity — weekly group sessions and masterminds, not a solo homework program like New Law Business Model or HTM.", S["objection_a"]))

story.append(Paragraph('"My competitors already have hundreds of reviews — can I catch up?"', S["objection_q"]))
story.append(Paragraph("Hargis (100+ reviews) and Shautsova (318) took years to build — the NAP fix and GBP push start closing that gap immediately, before the website even launches.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Essentials</b>", S["price_main"]),
     Paragraph("$3,497/mo", S["price_main"])],
    [Paragraph("Website rebuild, local SEO, NAP fix, GBP repair, managed ad campaign.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, practice masterminds, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000–$6,000/mo", S["price_main"])],
    [Paragraph("Goes to Google Search, LSA, and Meta — not to SMB Team.", S["price_detail"]),
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
    "Total: $6,097/mo + $3,000–$6,000 ad spend  |  Save $1,197/mo by bundling  |  ~34.6%–46.5% of revenue (aggressive exceeds 35% cap — scoping approval required)",
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
