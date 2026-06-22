"""
Sales Companion PDF — McNeil Law Firm
SMB Team — Jacob Meissner | June 22, 2026
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

DARK_NAVY = HexColor("#1a2332")
ACCENT_GREEN = HexColor("#3B6D11")
MEDIUM_GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#888888")
RULE_GRAY = HexColor("#CCCCCC")
QUOTE_BG = HexColor("#F5F7F0")
WHITE = HexColor("#FFFFFF")
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "mcneil-law-firm/McNeil_Law_Firm_June_22_2026_Sales_Companion.pdf"


def add_page_elements(canvas, doc):
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

S = {}
S["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=9.5, leading=13, textColor=LIGHT_GRAY, spaceAfter=3)
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=ACCENT_GREEN, spaceBefore=5, spaceAfter=1)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9, leading=11, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8, leading=11, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=2)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


def b(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY, spaceBefore=2, spaceAfter=2)

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

story.append(Paragraph("McNeil Law Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  June 22, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]), Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]), Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]), Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("John McNeil", S["snap_value"]), Paragraph("~$720K (−30% YoY)", S["snap_value"]),
     Paragraph("4 staff", S["snap_value"]), Paragraph("Stage 4", S["snap_value"]),
     Paragraph("26%", S["snap_value"]), Paragraph("Raleigh, NC", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.7*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 3))

story.append(Paragraph("Dominant Buying Motive: FINANCIAL CERTAINTY", S["section"]))
story.append(Paragraph("John wants a predictable pipeline — so slow seasons are planned for and payroll is never a question.", S["subsection"]))

story.append(quote_block("Cash flow visibility needs improvement to better plan for slow seasons."))
story.append(Spacer(1, 1))
story.append(quote_block("The firm ranks on page 2 of Google for 'family law Raleigh.'"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What John wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable pipeline.</b> 6–9 months of cases booked in advance; slow seasons planned, not survived."))
story.append(bd("<b>Payroll certainty.</b> Never running the mental math on whether the firm covers payroll this month."))
story.append(bd("<b>Path to $1.5M.</b> Revenue recovery from $720K to and past $1M on a system that scales without adding his hours."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Attribution gap.</b> Runs Google PPC + LSAs in-house but cannot distinguish paid from organic — spending money he cannot measure."))
story.append(b("<b>Julia's skepticism.</b> Past negative experience with SMB Team; she is the gatekeeper and reviews the proposal before John sees it."))
story.append(b("<b>Revenue decline.</b> Down ~30% YoY; no financial projections, no budget, no cost-per-acquisition tracking in place."))
story.append(b("<b>Sole attorney ceiling.</b> John handles every matter — no paralegal, no production redundancy, no path to 30 cases/month at current capacity."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for John:</b>", S["subsection"]))
story.append(bd("Replaces in-house ad guesswork with a fully attributed system — every case traced to its source, every ad dollar accountable."))
story.append(bd("Manages LSAs + Google Ads while building reviews past 100 — improving 3-pack and LSA visibility simultaneously."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $7,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $720K places firm in $400K–$1M Starter band per eligibility rules; Platinum/Growth hidden under $1M."))
story.append(b("Starter ad spend cap $5,000 fits: $11,047 packages + $5,000 = $16,047 = 26.7% of $60K/mo — under 35% cap."))
story.append(b("Review acquisition + GBP management included; closing gap with McIlveen (102 reviews) is first unlock for 3-pack visibility."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for John:</b>", S["subsection"]))
story.append(bd("Provides accountability framework to hold the firm to its $1.5M goal and build operational habits that sustain the marketing lift."))
story.append(bd("Weekly group coaching + practice area masterminds connect John with attorneys who have already made the $700K–$1.5M jump."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("$400K–$1M revenue, any team size — correct tier; Master's Circle hidden (requires 5+ team members; firm has 4)."))
story.append(b("Addresses financial visibility gap — coaching framework builds the P&amp;L review habit Julia's manual bookkeeping cannot provide."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("McNeil Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for John:</b>", S["subsection"]))
story.append(bd("Conservative ($3,500): ~6 cases/mo x ~$4,100 = ~$24,600/mo from ads — a ~7x return on ad spend (estimate)."))
story.append(bd("Aggressive ($5,000): ~11 cases/mo x ~$4,100 = ~$45,100/mo from ads — a ~9x return on ad spend (estimate)."))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Family law minimums: PPC $1,500 + LSA $1,000 + Meta $700 = $3,200, rounded to $3,500."))
story.append(b("<b>Aggressive:</b> $1.5M goal x 20% / 12 x 1.15 (Raleigh Tier 3) = $28,750 minus $7,847 fee = $20,903; capped at Starter maximum $5,000."))
story.append(Paragraph("<i>All ROI figures are estimates based on industry averages. Not guaranteed.</i>", S["disclaimer"]))

story.append(thin_rule())

story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"We tried something like this before and it did not work."', S["objection_q"]))
story.append(Paragraph("Ask specifically what failed — attribution? reporting? communication? SMB Team's campaigns include monthly cost-per-acquisition reporting so results are visible every month, not a black box.", S["objection_a"]))

story.append(Paragraph('"We cannot afford $11,000 a month with revenue down 30%."', S["objection_q"]))
story.append(Paragraph("At $60K/mo revenue, $11,047 is 18.4% — well under 35% cap. Conservative scenario projects ~$24,600/mo in new ad revenue. The question is whether the firm can afford to stay at $720K without a recovery plan.", S["objection_a"]))

story.append(Paragraph('"We already run our own Google Ads."', S["objection_q"]))
story.append(Paragraph("Julia confirmed the firm cannot distinguish paid from organic leads. McIlveen (102 reviews) pays less per click for identical keywords due to higher Quality Scores. Managed campaigns fix tracking and competitive positioning simultaneously.", S["objection_a"]))

story.append(Paragraph('"We need to hire a paralegal before we can handle more leads."', S["objection_q"]))
story.append(Paragraph("Hiring before the pipeline is confirmed is the higher-risk sequence. Build the marketing system first, verify case volume, then hire into confirmed demand — the coaching package covers exactly this sequencing.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$7,847/mo", S["price_main"])],
    [Paragraph("Google Ads, LSAs, website optimization, review acquisition, monthly reporting.", S["price_detail"]),
     Paragraph("<strike>$9,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,500–$5,000/mo", S["price_main"])],
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
    "Total: $11,047/mo + $3,500–$5,000 ad spend  |  Save $2,147/mo by bundling  |  24.2%–26.7% of revenue (under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
