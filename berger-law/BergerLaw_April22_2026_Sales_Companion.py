"""
Sales Companion PDF — Berger Law
SMB Team Internal Document — DO NOT SHARE WITH CLIENT
Rep: Randy Gold  |  April 22, 2026
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

OUTPUT_PATH = "berger-law/BergerLaw_April22_2026_Sales_Companion.pdf"


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
    """Dark bullet for transformation statements and what he wants."""
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

story.append(Paragraph("Berger Law", S["title"]))
story.append(Paragraph("Sales Companion  |  April 22, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Alex Berger", S["snap_value"]),
     Paragraph("$600K–$1M", S["snap_value"]),
     Paragraph("6 (4 atty)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("51% consult.", S["snap_value"]),
     Paragraph("Marquette, MI", S["snap_value"])],
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
story.append(Paragraph("Alex wants a 10-hour strategic week by 2029 — the firm earns without him, income is predictable, and his time is his own.", S["subsection"]))

story.append(quote_block("I want to be working 10 hours a week by 2029 — strategic, not operational."))
story.append(Spacer(1, 1))
story.append(quote_block("My goal is $250,000 a year in personal W-2 income from the firm."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>A firm that runs itself.</b> Cases, intake, and KPIs operate without him in the room."))
story.append(bd("<b>Predictable $250K personal W-2.</b> Income that arrives regardless of monthly volatility."))
story.append(bd("<b>10-hour strategic weeks by 2029.</b> Freed from daily operations on a documented timeline."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Intake leaking revenue.</b> 51% consultation-to-hire rate — one in two prospects walks away unsigned."))
story.append(b("<b>No marketing ROI visibility.</b> $5K/month with zero cost-per-signed-case tracking."))
story.append(b("<b>Team not self-managing.</b> Manual KPIs, no management layer — the firm depends on Alex to function."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns blind ad spend into a measurable lead engine with cost-per-signed-case tracking on every dollar."))
story.append(bd("Closes the gap on Grabel &amp; Associates, who are actively targeting U.P. criminal defense clients with a dedicated Marquette strategy."))
story.append(bd("Builds the predictable lead flow that makes a 10-hour strategic week structurally possible."))

story.append(Paragraph("<b>Full Service Starter  |  $3,847/mo bundled</b>", S["subsection"]))
story.append(b("$600K–$1M revenue places Berger Law in Starter tier — Essentials excluded for Criminal Defense at high competitiveness."))
story.append(b("AI SEO is underperforming competitors despite $5K/month spend — a restructured managed strategy is needed."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Fixes the consultation-to-hire gap — a structured intake framework converts the 49% of prospects currently walking away."))
story.append(bd("Installs the KPI accountability and team operating system that lets Alex step back on a documented 2029 timeline."))
story.append(bd("FCFO Advisor delivers financial clarity across both firms — so Alex knows what he earns, keeps, and needs to target."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("$400K+ revenue and $250K W-2 goal require Elite Coach Plus — Elite Coach alone is insufficient."))
story.append(b("FCFO Advisor ($1,297/mo bundled) added alongside: profit volatility across two firms, no financial visibility into per-case margins."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Berger Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Replaces guesswork with a measurable case pipeline — every dollar tracked to a signed client."))
story.append(bd("Generates the ROI data that proves exactly what each case cost to acquire, making every future budget decision evidence-based."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000/mo — Criminal Defense channel minimums across PPC and LSA."))
story.append(b("<b>Aggressive:</b> $4,000/mo — Starter tier cap; upgrade to Growth tier to unlock the full 20% rule budget."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 5 cases x $4K avg = $20K/mo vs. $3K spend = 6.7x return (estimate)."))
story.append(b("<b>Aggressive:</b> 8 cases x $4K avg = $32K/mo vs. $4K spend = 8.0x return (estimate)."))
story.append(Paragraph("<i>Estimates only. Assumes intake improvements are implemented. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> PPC $2,000 + LSA $900 = $2,900. Blended CPL $200 (+20% cushion) = 15 leads x 80% improved close = 5 cases."))
story.append(b("<b>Aggressive:</b> 20% rule x Tier 5 (0.85x) yields $7,486 — capped at Starter limit of $4,000. Total: $11,344/mo = 17.0% of revenue."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I\'m already spending $5K/month — why spend more?"', S["objection_q"]))
story.append(Paragraph("The current $5K has no cost-per-signed-case tracking. SMB Team installs measurement first — so every dollar is accountable before the budget grows.", S["objection_a"]))

story.append(Paragraph('"My current agency has been with me a while."', S["objection_q"]))
story.append(Paragraph("Grabel &amp; Associates has a dedicated Marquette landing page targeting Berger Law's exact clients. Every month the current SEO underperforms is a month Grabel extends their lead.", S["objection_a"]))

story.append(Paragraph('"$7,344 a month — I\'m not sure the budget is there."', S["objection_q"]))
story.append(Paragraph("Berger Law loses an estimated $5K–$10K/month from a 51% consultation rate. Closing 2 more cases/month at $4K average covers the coaching package on its own.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Starter</b>", S["price_main"]),
     Paragraph("$3,847/mo", S["price_main"])],
    [Paragraph("PPC, LSA, Local SEO, Google Business Profile management.", S["price_detail"]),
     Paragraph("<strike>$4,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Intake system, KPI dashboard, team accountability, conversion coaching.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>FCFO Advisor</b>", S["price_main"]),
     Paragraph("$1,297/mo", S["price_main"])],
    [Paragraph("Profit plan, financial visibility, cost-per-signed-case reporting.", S["price_detail"]),
     Paragraph("<strike>$2,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000–$4,000/mo", S["price_main"])],
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
    ("LINEBELOW", (0,7), (-1,7), 0.5, RULE_GRAY),
]))
story.append(pt)
story.append(Paragraph(
    "Total: $8,344/mo + $2,900–$4,000 ad spend  |  Save $2,647/mo by bundling  |  16.1%–17.5% of revenue (under 35% cap)",
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
