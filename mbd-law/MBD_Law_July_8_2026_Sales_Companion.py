"""
Sales Companion PDF — MBD Law (Marotta Blazini Dunleavy LLC)
Sales Rep: Jonathan Farace
Date: July 8, 2026
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

OUTPUT_PATH = "mbd-law/MBD_Law_07082026_Sales_Companion.pdf"


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

story.append(Paragraph("MBD Law (Marotta Blazini Dunleavy LLC)", S["title"]))
story.append(Paragraph("Sales Companion  |  July 8, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
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
    [Paragraph("Genevieve Blazini", S["snap_value"]),
     Paragraph("$2.0M (2025); $2.4M run rate", S["snap_value"]),
     Paragraph("6 (5 atty + DOO)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("75% of consults", S["snap_value"]),
     Paragraph("Maywood, NJ (Bergen County)", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE AND DOMINATE", S["section"]))
story.append(Paragraph("Build a $10M Bergen County family law firm that runs on systems — not on luck, referrals, or whether the leads decide to show up this week.", S["subsection"]))

story.append(quote_block("Partners are fully aligned on an aggressive growth goal — $3M this year, $10M in 5 years — and are prepared to invest heavily to achieve it."))
story.append(Spacer(1, 1))
story.append(quote_block("75% of consults retained. A healthy 40-45% net profit margin provides ample room for investment without jeopardizing the business."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable leads.</b> No more 10-day droughts — 20-25 new clients/month consistently."))
story.append(bd("<b>$10M in 5 years.</b> Not as a wish — as a plan with a clear system behind it."))
story.append(bd("<b>Operational independence.</b> Natalie and the team execute without partner involvement at every step."))
story.append(bd("<b>Attribution data.</b> Know which channels generate the best cases so every dollar is justified."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>GBP miscategorization.</b> $10K/month in LSA suppressed — listed as 'General Law Firm' not 'Family Law Firm.'"))
story.append(b("<b>No Meta advertising.</b> Entire paid social channel unclaimed while competitors build awareness before prospects search Google."))
story.append(b("<b>Ops infrastructure early-stage.</b> Natalie joined 2024; systems for a $10M firm still being built."))
story.append(b("<b>Buried intake.</b> Contact form at bottom only — ad visitors who don't scroll leave without contacting the firm."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>Full Service Marketing — Dominate  |  $10,497/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1M+, aggressive $3M/2026 and $10M/5yr goals — Dominate tier is the correct match."))
story.append(b("Already spending $12,500/mo; SMB restructures that budget and fixes the GBP suppressor immediately."))
story.append(b("86 reviews at 4.8 stars exceeds Burke Williams (69) — correct category fix unlocks the local pack position the firm should already own."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>Master's Circle + FCOO Director  |  $5,394/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $2M+; team of 6 with dedicated DOO — $2M+ eligibility tier confirmed."))
story.append(b("Natalie joined 2024; FCOO Director accelerates the infrastructure build she was hired to complete."))
story.append(b("Includes group coaching, practice area masterminds, quarterly workshops, and one annual in-person event."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("MBD Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Conservative ($3,500/mo) establishes per-channel ROI proof — demonstrates what a properly managed campaign produces from week one."))
story.append(bd("Aggressive ($14,000/mo) reaches the Dominate tier cap and positions MBD Law for the 20-25 new client/month Q3 target."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — minimum viable spend across LSA, PPC, and Meta retargeting."))
story.append(b("<b>Aggressive:</b> $14,000/mo — Dominate tier cap; positions MBD Law to dominate Bergen County family law searches."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~6 cases x $10K avg = $60K/mo vs. $3.5K spend = ~17x return (estimated)."))
story.append(b("<b>Aggressive:</b> ~28 cases x $10K avg = $280K/mo vs. $14K spend = ~20x return (estimated)."))
story.append(Paragraph("<i>Estimates only. Case value not confirmed — verify at proposal call. Not guaranteed.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"We\'re already spending $12,500/month — why pay more to manage it?"', S["objection_q"]))
story.append(Paragraph("The $12,500 is producing 10-day droughts because the GBP is miscategorized. SMB management fixes the structural suppressor, restructures the budget, and launches Meta (unclaimed). The question is whether the current $12,500 should keep producing droughts.", S["objection_a"]))

story.append(Paragraph('"We have a Director of Operations — why do we need the FCOO package?"', S["objection_q"]))
story.append(Paragraph("Natalie joined in 2024 and is building systems from scratch. FCOO Director pairs elite coaching with a seasoned COO who has built $10M law firm infrastructure before — Natalie gets a partner who has done exactly this, not a program to figure it out alone.", S["objection_a"]))

story.append(Paragraph('"$15,891/month is a big number."', S["objection_q"]))
story.append(Paragraph("At conservative ($3,500 ad spend): ~6 cases x $10K = $60K/mo revenue from ads vs. $3.5K spend. Total SMB fee is under 8% of current monthly revenue ($200K). MBD already has 86 reviews and a 75% close rate — the system just needs to match the talent. All ROI figures are estimates.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Dominate</b>", S["price_main"]),
     Paragraph("$10,497/mo", S["price_main"])],
    [Paragraph("Full-funnel Google Ads, LSA, Meta, SEO, website optimization — Bergen County family law.", S["price_detail"]),
     Paragraph("<strike>$12,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle + FCOO Director</b>", S["price_main"]),
     Paragraph("$5,394/mo", S["price_main"])],
    [Paragraph("Elite coaching, practice area masterminds, quarterly workshops, dedicated FCOO Director support.", S["price_detail"]),
     Paragraph("<strike>$7,794</strike> stand alone", S["price_detail"])],
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
    "Total: $15,891/mo + $3,500–$14,000 ad spend  |  Save $4,400/mo by bundling  |  7.9%–14.9% of revenue (under 35% cap)",
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
