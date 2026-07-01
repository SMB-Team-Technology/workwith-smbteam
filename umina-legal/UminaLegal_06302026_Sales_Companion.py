"""
Sales Companion PDF — Umina Legal
SMB Team Internal Document — Do Not Share
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

OUTPUT_PATH = "umina-legal/UminaLegal_06302026_Sales_Companion.pdf"


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

story.append(Paragraph("Umina Legal PLLC — Ryan Umina", S["title"]))
story.append(Paragraph("Sales Companion  |  June 30, 2026  |  Rep: Nick Holderman  |  Package: FCOO + FCFO (No Marketing)", S["subtitle"]))
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
    [Paragraph("Ryan Umina", S["snap_value"]),
     Paragraph("~$1.2M/yr", S["snap_value"]),
     Paragraph("2 people", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("~15% (est.)", S["snap_value"]),
     Paragraph("Morgantown, WV", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM WITHOUT BURNOUT", S["section"]))
story.append(Paragraph("Ryan wants to scale to $1.5M–$2M while working ~30 hours a week — shifting from operator to owner without repeating a prior burnout.", S["subsection"]))

story.append(quote_block("I want to shift from operator to owner — the firm needs to run without me handling everything."))
story.append(Spacer(1, 1))
story.append(quote_block("Speed to lead is critical — I handle every call personally so we don't lose cases at first contact."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>$2M without more hours.</b> Scale revenue without scaling his personal workload."))
story.append(bd("<b>Delegation that preserves quality.</b> Move intake off his plate without losing his standards."))
story.append(bd("<b>Burnout-proof growth.</b> Systems and financial clarity that protect him the way the prior attempt didn't."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Intake bottleneck.</b> Every call goes to Ryan personally — growth multiplies his load."))
story.append(b("<b>No ops layer.</b> Two-person firm with no management structure between Ryan and the work."))
story.append(b("<b>Weak bookkeeping.</b> Ryan acknowledged this — no monthly P&L, no cost-per-acquisition data."))
story.append(b("<b>Unusable CRM.</b> Practice Panther has years of disorganized data — no pipeline visibility."))
story.append(b("<b>Burnout caution.</b> Prior scaling attempt failed — he needs a structured plan, not just spend."))

story.append(thin_rule())

# ── Why the FCOO Advisor ──
story.append(Paragraph("Why the Fractional COO Advisor", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the operations layer that lets intake leave Ryan's plate without losing his quality standards."))
story.append(bd("Creates the team structure, role clarity, and accountability that makes the next hire a system — not a gamble."))
story.append(bd("Gives Ryan a strategic partner to build the operational infrastructure that supports $2M without burnout."))

story.append(Paragraph("<b>Fractional COO Advisor  |  $1,297/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1M+, team under 5: FCOO Advisor is the correct eligibility match for this stage."))
story.append(b("Ryan's primary pain: no ops layer, no delegation, no ability to step away — exactly what FCOO solves."))
story.append(b("Includes Elite Coach group deliverables: weekly coaching, masterminds, quarterly and annual workshops."))
story.append(b("Retail stand-alone is $1,797/mo — bundled saves $500/mo vs. stand-alone."))

story.append(thin_rule())

# ── Why the FCFO Advisor ──
story.append(Paragraph("Why the Fractional CFO Advisor", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns $100K/month in revenue from a feel-good number into a transparent financial picture with actual margins."))
story.append(bd("Establishes the bookkeeping infrastructure Ryan called out as a weakness — clean P&L from month one."))
story.append(bd("Tracks cost-per-acquisition on his Google Ads so every budget decision is grounded in real ROI data."))

story.append(Paragraph("<b>Fractional CFO Advisor  |  $1,297/mo bundled</b>", S["subsection"]))
story.append(b("Ryan explicitly acknowledged bookkeeping is a weakness — financial clarity is a stated need, not an assumption."))
story.append(b("Practice Panther is unusable — FCFO engagement includes financial systems implementation support."))
story.append(b("At $1.2M revenue with no P&L visibility, every scaling decision is a guess. FCFO fixes that."))
story.append(b("Retail stand-alone is $1,797/mo — bundled saves $500/mo vs. stand-alone."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Umina Legal — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Advisory: Google Ads Investment (Self-Managed)", S["section"]))

story.append(Paragraph("<b>Context:</b>", S["subsection"]))
story.append(b("Ryan currently runs $3,000/mo in Google Ads self-managed — strong signal that this market responds to paid search."))
story.append(b("No SMB Team marketing package recommended at this stage — existing campaign is working; internal systems are the gap."))
story.append(b("Audit includes advisory ad spend targets for when internal systems are ready to handle higher lead volume."))

story.append(Paragraph("<b>Recommended Self-Managed Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,500/mo — step up from $3K adds satellite markets (Parkersburg, Waynesburg, Charleston) + LSA layer."))
story.append(b("<b>Aggressive:</b> $25,000/mo — full multi-channel coverage across all markets when intake is delegated and systems are ready."))

story.append(Paragraph("<b>Estimated Return (for context):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~16 leads x 15% close = 2–3 cases x $7K avg = ~$17,500/mo vs. $7,500 spend = ~2x return."))
story.append(b("<b>Aggressive:</b> ~62 leads x 15% close = 9–10 cases x $7K avg = ~$63,000/mo vs. $25,000 spend = ~2.5x return."))
story.append(Paragraph("<i>All figures are estimates using practice area defaults ($7K midpoint). Case value not stated on call. Not guaranteed.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"My Google Ads are already working — why not just add a marketing package?"', S["objection_q"]))
story.append(Paragraph("More leads hitting a firm with no intake coordinator will accelerate burnout, not prevent it. The bottleneck right now is internal — every additional lead means another call Ryan has to personally take. Fix the system first; add marketing fuel when the intake coordinator is trained and running.", S["objection_a"]))

story.append(Paragraph('"I don\'t want to grow too fast — I burned out before."', S["objection_q"]))
story.append(Paragraph("That caution is exactly right, which is why this recommendation leads with operations and financial clarity before adding any marketing. The FCOO Advisor builds the structure that makes growth safe. The prior burnout happened because systems weren't there — this is how you build them first.", S["objection_a"]))

story.append(Paragraph('"Will the FCOO actually help me hire an intake coordinator?"', S["objection_q"]))
story.append(Paragraph("Yes — the FCOO Advisor delivers the job description, interview scoring rubric, training framework, and accountability structure in the first 30 days. Ryan does not have to figure this out from scratch; the role is designed and ready to hire into.", S["objection_a"]))

story.append(Paragraph('"$2,594/mo feels like a lot for something that isn\'t marketing."', S["objection_q"]))
story.append(Paragraph("One additional criminal defense case per month covers both packages — and Ryan is currently losing cases every hour he's in court without backup. The FCOO Advisor turns the next hire into a revenue multiplier, not an expense. The FCFO Advisor shows him exactly what he is actually keeping from each case.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Fractional COO Advisor</b>", S["price_main"]),
     Paragraph("$1,297/mo", S["price_main"])],
    [Paragraph("Operations advisory, intake framework, team structure, coaching included.", S["price_detail"]),
     Paragraph("<strike>$1,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Fractional CFO Advisor</b>", S["price_main"]),
     Paragraph("$1,297/mo", S["price_main"])],
    [Paragraph("Financial advisory, bookkeeping oversight, monthly P&L, coaching included.", S["price_detail"]),
     Paragraph("<strike>$1,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend (Self-Managed, Advisory)</b>", S["price_main"]),
     Paragraph("$7,500–$25,000/mo", S["price_main"])],
    [Paragraph("Goes directly to Google, LSA — not to SMB Team.", S["price_detail"]),
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
    "Total SMB Investment: $2,594/mo  |  Save $1,000/mo by bundling  |  2.6% of revenue (well under 35% cap)",
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
