"""
Sales Companion PDF — The Bledsoe Firm
SMB Team  |  August 12, 2026  |  Rep: Jacob Meissner
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

OUTPUT_PATH = "the-bledsoe/The Bledsoe Firm_08122026_Sales_Companion.pdf"


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

story.append(Paragraph("The Bledsoe Firm (John Bledsoe)", S["title"]))
story.append(Paragraph("Sales Companion  |  August 12, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("John Bledsoe", S["snap_value"]),
     Paragraph("~$2M est. (medium conf.)", S["snap_value"]),
     Paragraph("John + Kate + staff", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("17% stated", S["snap_value"]),
     Paragraph("Lake Forest, CA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE + FREEDOM", S["section"]))
story.append(Paragraph("John wants to open new offices in San Diego and LA while handing day-to-day marketing and intake ownership to Kate, so growth no longer depends on his personal, hands-on involvement.", S["subsection"]))

story.append(quote_block("Firm has 'tripled in size' and aims to 'double again in the next year,' with plans for new offices in San Diego and LA."))
story.append(Spacer(1, 1))
story.append(quote_block("John is delegating marketing and intake ownership to Kate to free himself for high-level strategy."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Market expansion.</b> Open new offices in San Diego and LA on top of a proven system, not a fragmented one."))
story.append(bd("<b>Operational freedom.</b> Let Kate fully own marketing and intake so he can focus on strategy."))
story.append(bd("<b>Conversion leverage.</b> Double the 17% close rate so existing ad spend produces twice the clients."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Fragmented vendor spend.</b> $36K/mo across 4 vendors with no unified reporting."))
story.append(b("<b>Weak conversion.</b> 17% close rate means most paid leads never become a case."))
story.append(b("<b>NAP inconsistency.</b> Website phone does not match directory listings — a fixable SEO drag."))
story.append(b("<b>Review gap.</b> Minyard Morris (246, 4.9) already out-paces the firm (201, 4.8)."))
story.append(b("<b>No profit visibility.</b> No case value or channel ROI data across the 4 vendors."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Replaces 4 disconnected vendors with one accountable partner and one consolidated reporting view."))
story.append(bd("Fixes the NAP inconsistency and Yelp fragmentation that are actively working against the firm's existing $36K/mo spend."))

story.append(Paragraph("<b>Full Service Marketing — Dominate  |  $10,497/mo bundled</b>", S["subsection"]))
story.append(b("Revenue estimate ~$2M (medium confidence) places firm in the $2M-$3M Dominate band."))
story.append(b("Media spend (~$26.5K/mo) is directionally consistent with the $2M estimate — confirm on call."))
story.append(b("Transcript named 'Starter' by rough figure — likely a pre-revenue-confirmation reference; verify with John."))
story.append(b("Stand-alone $12,497/mo — bundled saves $2,000/mo."))

story.append(thin_rule())

# ── Why This AI Package ──
story.append(Paragraph("Why This AI &amp; Intake Automation Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Delivers the exact Intake Qualifier tool discussed on the call — grading calls, tailoring follow-ups, and coaching staff to double the 17% close rate."))
story.append(bd("A dedicated Fractional CTO builds this without adding to John or Kate's workload."))

story.append(Paragraph("<b>Fractional CTO Level 2 (AI Accelerator L2)  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("Call-purpose override: FCTO/AI-automation was a co-equal, explicit topic on the call — replaces the pipeline's default Elite Coach Plus."))
story.append(b("Revenue ~$2M fits the $1.5M-$3M L2 band; matches the ask for custom agent builds, not just DIY (L1)."))
story.append(b("Stand-alone $5,797/mo — bundled saves $800/mo. Foundation Sprint $14,997 one-time optional."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("The Bledsoe Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("$5,500/mo conservative launches consolidated Google PPC + LSA coverage for divorce and custody terms across Lake Forest and Orange County."))
story.append(bd("$70,000/mo aggressive scales toward the firm's own stated goal of doubling revenue, adding Meta retargeting and cold audiences."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,500/mo — Google PPC $3,500 + LSA $2,000. Minimum viable search-intent coverage."))
story.append(b("<b>Aggressive:</b> $70,000/mo — 20% rule: $4M goal (2x current) x 20% / 12 = $66,667; Tier 2 (1.3x) = $86,667; minus $15,494 fees = ~$71K; using $70K."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative ($5,500/mo):</b> ~9 cases x $4K avg = ~$36K/mo vs. $5,500 spend = ~6.5x return (est.)."))
story.append(b("<b>Aggressive ($70,000/mo):</b> ~140 cases x $4K avg = ~$560K/mo vs. $70,000 spend = ~8x return (est.)."))
story.append(Paragraph("<i>All figures are estimates. Case value is Family Law practice-area default ($4K) — confirm on call. ~140 cases/mo is a formula ceiling under the revenue-doubling goal, not a literal near-term forecast at current staffing. Results not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Family Law minimums: Google PPC $3,500 + LSA $2,000 = $5,500."))
story.append(b("<b>Aggressive:</b> $4M goal (2x current) x 20% / 12 = $66,667. Tier 2 (1.3x) = $86,667. Minus $15,494 fees = ~$70,000."))
story.append(b("Total aggressive = $85,494 = ~51% of CURRENT revenue (over 35% cap), ~26% of the GOAL (under cap). Confirm revenue first."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I already have Noble and like the Lawmatics integration — why switch?"', S["objection_q"]))
story.append(Paragraph("Noble is one of four vendors already costing $36K/mo — the call itself framed this as replacing that spend, not adding a fifth. Dominate consolidates reporting without losing the CRM workflow he values.", S["objection_a"]))

story.append(Paragraph('"Is $15,494/mo too much before we confirm revenue?"', S["objection_q"]))
story.append(Paragraph("Revenue is a medium-confidence ~$2M estimate, cross-checked against ~$26.5K/mo current media spend. If confirmed under $2M, downgrade to Growth ($7,497/mo) and re-run the math.", S["objection_a"]))

story.append(Paragraph('"Can we just do the AI/intake piece, skip the marketing?"', S["objection_q"]))
story.append(Paragraph("The marketing gap is real and verified — NAP inconsistency, split Yelp listings, Minyard Morris out-pacing on reviews. Both were co-equal call topics; addressing only one leaves money on the table.", S["objection_a"]))

story.append(Paragraph('"140 cases a month sounds unrealistic."', S["objection_q"]))
story.append(Paragraph("Correct — that's the aggressive scenario's math ceiling under the firm's own doubling goal, not a near-term plan. The realistic near-term target is the firm's stated 20-25 clients/month.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Dominate</b>", S["price_main"]),
     Paragraph("$10,497/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, local SEO/directory cleanup, monthly reporting.", S["price_detail"]),
     Paragraph("<strike>$12,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Legal AI Workforce — Fractional CTO Level 2</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("Custom Intake Qualifier tool, Claude Enterprise, bi-monthly CTO calls. Foundation Sprint $14,997 one-time (optional).", S["price_detail"]),
     Paragraph("<strike>$5,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,500–$70,000/mo", S["price_main"])],
    [Paragraph("Goes to Google and Meta — not to SMB Team.", S["price_detail"]),
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
    "Total: $15,494/mo + $5,500–$70,000 ad spend  |  Save $2,800/mo by bundling  |  Confirm revenue on call",
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
