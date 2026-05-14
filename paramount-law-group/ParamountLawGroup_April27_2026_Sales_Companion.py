"""
Sales Companion PDF — Paramount Law Group
SMB Team Internal Document — DO NOT SHARE WITH CLIENT
Rep: Dan Bryant | April 27, 2026
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

OUTPUT_PATH = "paramount-law-group/ParamountLawGroup_04272026_Sales_Companion.pdf"


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

story.append(Paragraph("Paramount Law Group — Calgary, AB", S["title"]))
story.append(Paragraph("Sales Companion  |  April 27, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Donna Gee", S["snap_value"]),
     Paragraph("$1.2M billed / $800k collected", S["snap_value"]),
     Paragraph("~10 total", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Calgary, AB", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM + EXIT", S["section"]))
story.append(Paragraph("Donna wants a firm that runs without her so she can travel freely, earn what she deserves, and sell it for what she has built.", S["subsection"]))

story.append(quote_block("HR drains 8-10 hrs/week causing burnout. Wants 2 months in Mexico, Tue-Thu schedule, reduce dependence on her. Mid-term exit: >= $600k, aspirational $1M via ~3x EBITDA."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Time freedom.</b> Two months in Mexico + Tue-Thu schedule — non-negotiable personal goals."))
story.append(bd("<b>Firm runs without her.</b> Ops, intake, and team perform without Donna's daily involvement."))
story.append(bd("<b>Double take-home to $200k.</b> On $1.2M billings, this is a structural fix, not a revenue problem."))
story.append(bd("<b>Sellable asset.</b> Exit $600k+ minimum; aspirational $1M within 3 years via ~3x EBITDA."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>HR consuming her capacity.</b> 8-10 hrs/week on people issues = $218k-$273k/yr lost at $525/hr."))
story.append(b("<b>No marketing system.</b> 13 Google reviews vs. 381-467 for top competitors; invisible in local search."))
story.append(b("<b>No accountability structure.</b> No KPIs, no SOPs, no org chart — knowledge lives in heads, not systems."))
story.append(b("<b>Cash flow constraints.</b> $150-175k AR tied up; $100-125k debt; cautious about committing spend now."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Creates inbound case flow from estates/probate/guardianship/corporate — leads that arrive without Donna personally generating them."))
story.append(bd("Builds the online footprint a buyer will evaluate — GBP, reviews, website, content — directly supporting the exit goal."))
story.append(bd("Makes Donna's CBA Elder Law Chair credentials visible online — a competitive moat no Calgary competitor can match."))

story.append(Paragraph("<b>Full Service Marketing — Growth Tier  |  $7,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue: $1.2M billed / $800k collected. Growth tier appropriate for $1M+ billing firm with aggressive collection target."))
story.append(b("All practice areas (estates, probate, guardianship, corporate) eligible for Ads/LSA — no PI or criminal restrictions."))
story.append(b("Website rebuild required: no practice area pages, no CTA above fold, no SEO content — full service is the right entry point."))
story.append(b("No ads ever run: $3,500-$6,500 spend is proportionate to goals and well within the 35% revenue cap."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Operations Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Frees 8-10 hrs/week from HR — worth $218k-$273k/yr at her $525/hr rate."))
story.append(bd("Builds KPIs and SOPs that make the Mexico trip and Tue-Thu schedule structurally possible, not aspirational."))
story.append(bd("Creates a self-managing team a buyer pays a premium for — directly increasing exit valuation."))

story.append(Paragraph("<b>Fractional COO Advisor  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Dan's call notes list Fractional COO as Option B — this is exactly what Donna and Tim were evaluating."))
story.append(b("Tim is in place as an ops ally — FCOO works with Tim to build systems, not replace him."))
story.append(b("The $218k/yr HR time-loss is the most concrete ROI anchor from the call — FCOO directly addresses it."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Paramount Law Group — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Puts Paramount in front of Calgary families and businesses searching for estate, probate, guardianship, and corporate services — capturing demand that competitors are taking every day right now."))
story.append(bd("Generates 7-15 new cases per month from paid channels, creating the revenue growth needed to double owner take-home and fund the exit valuation target."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — Google PPC for estates/probate + corporate, LSA foundation-building."))
story.append(b("<b>Aggressive:</b> $6,500/mo — full channel deployment across Google, LSA, and Meta for all four target practice areas."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~7 cases x $3,500 avg = ~$24,500/mo vs. $3,500 spend = ~7x return."))
story.append(b("<b>Aggressive:</b> ~15 cases x $3,500 avg = ~$52,500/mo vs. $6,500 spend = ~8x return."))
story.append(Paragraph("<i>All figures are estimates using blended case value ~$3,500 (estates/corporate mix) and 15% close rate. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Estate Planning PPC $1,500 + LSA $900 + Corporate PPC $800 + Meta retargeting $300 = $3,500."))
story.append(b("<b>Aggressive:</b> $1.2M target x 20% / 12 = $20,000. Calgary Tier 3 (1.15x) = $23,000. Minus $3,397 fee = $19,603. Capped at Growth tier max of $7,000; using $6,500 under cap."))
story.append(b("Total SMB spend at aggressive: $10,694 + $6,500 = $17,194/mo = 21.5% of $800k collected revenue. Well under the 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"The timing is not right — new hire starting, senior lawyer may be leaving."', S["objection_q"]))
story.append(Paragraph("Transitions are exactly when systems matter most. A new hire without KPIs learns bad habits day one. The FCOO builds the structure that makes transitions manageable. Starting now means the new lawyer onboards into a system, not into Donna's inbox.", S["objection_a"]))

story.append(Paragraph('"Cash flow is tight until the AR comes in."', S["objection_q"]))
story.append(Paragraph("AR recovery is one of the first FCOO deliverables. $150-175k tied in estate files — recovering half in 60-90 days funds months of investment. Repricing underquoted complex wills alone more than offsets the monthly fee.", S["objection_a"]))

story.append(Paragraph('"Can we start smaller and see results first?"', S["objection_q"]))
story.append(Paragraph("Option A (coaching only) or Option B (FCOO only, 1hr/week) are both available as entry points. Frame honestly: starting smaller means slower results and a longer runway to the $200k take-home and $600k+ exit she described.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth Tier</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("Website rebuild + local SEO + Google Ads + LSA + Meta Ads.", S["price_detail"]),
     Paragraph("<strike>$7,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Fractional COO Advisor</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Weekly 1:1, KPIs by role, SOP build, accountability cadence.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,500–$6,500/mo", S["price_main"])],
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
    "Total: $10,694/mo + $3,500–$6,500 ad spend  |  Save $1,100/mo by bundling  |  17.8%–21.5% of collected revenue (under 35% cap)",
    S["savings"]))

# ── Build ──
doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

import re as _re
with open(OUTPUT_PATH, "rb") as _f:
    _data = _f.read().decode("latin-1")
page_count = len(_re.findall(r"/Type\s*/Page[^s]", _data))
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
