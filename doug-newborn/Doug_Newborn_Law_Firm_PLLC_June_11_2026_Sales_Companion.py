"""
Sales Companion PDF — Doug Newborn Law Firm, PLLC
SMB Team | June 11, 2026 | Rep: Dan Bryant
FOR INTERNAL USE ONLY; DO NOT SHARE.
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

OUTPUT_PATH = "doug-newborn/Doug_Newborn_Law_Firm_PLLC_06112026_Sales_Companion.pdf"


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

story.append(Paragraph("Doug Newborn Law Firm, PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  June 11, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Doug Newborn", S["snap_value"]),
     Paragraph("~$5M", S["snap_value"]),
     Paragraph("25 staff / 7 atty", S["snap_value"]),
     Paragraph("Stage 5", S["snap_value"]),
     Paragraph("~15% (default)", S["snap_value"]),
     Paragraph("Tucson, AZ", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: TIME FREEDOM", S["section"]))
story.append(Paragraph("Doug wants the firm to run itself — fewer fires, less escalation, more time back.", S["subsection"]))

story.append(quote_block("Main constraint is time; operations need support more than top-line growth."))
story.append(Spacer(1, 1))
story.append(quote_block("Clio Draft paid (~$8-12K) but stalled for a year; lacking owner to drive."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Firm runs without him.</b> Team executes without Doug involved in daily decisions."))
story.append(bd("<b>Projects get done.</b> Someone else drives implementation — not stalled for a year."))
story.append(bd("<b>Time back.</b> Fewer fires, fewer escalations, more time for the work he chooses."))
story.append(bd("<b>Predictable profit.</b> Know what each practice pod earns — not discovered quarterly."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No execution layer.</b> Atticus provides strategy; no one executes the weekly playbook between sessions."))
story.append(b("<b>No KPIs.</b> 7 attorneys with no utilization targets — performance gaps are invisible."))
story.append(b("<b>No cadence.</b> No weekly huddles, 1:1s, or dashboards running without Doug driving them."))
story.append(b("<b>Stalled tech debt.</b> Clio Draft paid and dormant — no owner to finish it."))
story.append(b("<b>PI digital gap.</b> PI invisible in paid search; competitors dominate every online PI term."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Opens PI to paid digital for the first time — veteran story and 850+ reviews differentiate immediately."))
story.append(bd("Extends proven Probate Platinum infrastructure to PI without adding a management burden."))
story.append(bd("Geo pages compound over time — each suburb page drives leads without additional ad spend."))

story.append(Paragraph("<b>Full Service Marketing — Platinum  |  $15,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$5M confirmed (transcript) — Platinum tier ($3M+) is correct."))
story.append(b("Lerner &amp; Rowe (870 reviews) and Zanes Law (since 2003) dominate PI paid search unopposed."))
story.append(b("Stand-alone $18,997 — bundled saves $3,000/mo."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching &amp; Operations Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("FCOO builds and runs weekly accountability — KPIs, dashboards, huddles — so Doug does not have to."))
story.append(bd("Drives Clio Draft to completion in a 30-day sprint; $8-12K sunk cost starts generating ROI."))
story.append(bd("Master's Circle adds peer-level coaching at comparable revenue scale alongside the COO execution layer."))

story.append(Paragraph("<b>Master's Circle + FCOO Director  |  $5,394/mo bundled</b>", S["subsection"]))
story.append(b("25 staff / 7 attorneys — qualifies for Master's Circle (5+ with dedicated staff)."))
story.append(b("FCOO explicitly discussed on call: 9 hrs/month, KPIs, dashboards, AR policies."))
story.append(b("$5M revenue ($2M+ threshold) — FCOO Director tier. Corrected from pipeline default of Elite Coach Plus."))
story.append(b("Stand-alone $7,794 — bundled saves $2,400/mo."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Doug Newborn Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts the firm in the PI paid search auction for the first time — capturing intent that currently goes entirely to Lerner &amp; Rowe, Zanes Law, and Husband &amp; Wife."))
story.append(bd("Expands Probate/EP digital presence to surrounding communities (Marana, Oro Valley, Sahuarita) where competition is lower and searches are growing."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $10,000/mo — Probate/EP optimization + PI entry across Google Ads and LSA."))
story.append(b("<b>Aggressive:</b> $40,000/mo — full Platinum tier cap; $20K Probate/EP + $20K PI expansion."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~6 cases x $7K avg = ~$42K/mo vs. $10K spend = 4.2x return (estimate)."))
story.append(b("<b>Aggressive:</b> ~30 cases x $6.8K blended = ~$200K/mo vs. $40K spend = 5x return (estimate)."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Estate Planning PPC $2,500 + LSA $1,000 + Meta $700 + PI PPC $5,000 + LSA $800 = $10,000."))
story.append(b("<b>Aggressive:</b> $10M goal x 20% / 12 = $167K. Tier 4 (1.0x) = $167K. Minus $15,997 fee = capped at $40K (Platinum tier max)."))
story.append(b("Total at aggressive: $40K ad + $21,391 fees = $61,391 = 14.7% of monthly revenue. Well under 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We already have SMB Team on Probate — why change anything?"', S["objection_q"]))
story.append(Paragraph("Not a change — an expansion. PI has zero paid digital presence. Lerner &amp; Rowe (870 reviews) and Zanes Law (since 2003) capture every PI intent search unchallenged. The FCOO package addresses the operational gaps separately.", S["objection_a"]))

story.append(Paragraph('"I already have an Atticus coach — why add SMB Team coaching?"', S["objection_q"]))
story.append(Paragraph("Atticus = big-picture strategy every two weeks. FCOO Director = executes the daily/weekly operational layer between those sessions. Doug said his constraint is implementation, not strategy. These serve different needs.", S["objection_a"]))

story.append(Paragraph('"We tried Meta ads and the content quality was not good enough."', S["objection_q"]))
story.append(Paragraph("That was AI-generated PI content — discontinued by Doug for quality concerns. The new Meta strategy is retargeting via a Pixel on existing PPC pages, not AI content. Different product, different approach.", S["objection_a"]))

story.append(Paragraph('"The team is already stretched."', S["objection_q"]))
story.append(Paragraph("The FCOO takes work off Doug's plate, not the team's. He becomes the Clio Draft project owner and runs the weekly cadence. The team gets more structure — not more tasks.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Platinum</b>", S["price_main"]),
     Paragraph("$15,997/mo", S["price_main"])],
    [Paragraph("PPC + LSA for Probate/EP + PI launch; SEO, geo pages, Meta Pixel.", S["price_detail"]),
     Paragraph("<strike>$18,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle + FCOO Director</b>", S["price_main"]),
     Paragraph("$5,394/mo", S["price_main"])],
    [Paragraph("FCOO 9+ hrs/mo; KPIs, cadence, Clio sprint; Master's Circle peer coaching.", S["price_detail"]),
     Paragraph("<strike>$7,794</strike> stand alone", S["price_detail"])],
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
    "Total: $21,391/mo + $10K–$40K ad spend  |  Save $5,400/mo by bundling  |  14.7%–17.4% of revenue (under 35% cap)",
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
