"""
Sales Companion PDF Template — SMB Team
========================================
This template generates the 2-page internal Sales Companion PDF for the sales rep.
It uses reportlab. Do not modify the layout, colors, fonts, styles, or structure.
Only replace the # FILL: placeholders with audit-specific content.

IMPORTANT: The final PDF must be exactly 2 pages. If content overflows to a third
page, shorten bullet text — do not remove sections.

All bullet text must be scannable: one idea per bullet, 8th-grade reading level.
Each "What it does for her/him:" bullet states the transformation, not the deliverable.
Each scoping rationale bullet states one fact with one conclusion.

Output filename: [FirmName]_[Date]_Sales_Companion.pdf
  - FirmName: spaces replaced with underscores
  - Date: MMDDYYYY format
  - Save to the root of the project folder (same location as the Growth Audit HTML)
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

OUTPUT_PATH = "silversmith-legal/SilversmithLegal_06222026_Sales_Companion.pdf"


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

story.append(Paragraph("Silversmith Legal", S["title"]))
story.append(Paragraph("Sales Companion  |  June 22, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Christopher Silversmith", S["snap_value"]),
     Paragraph("~$800K legal", S["snap_value"]),
     Paragraph("3 (Chris, Amy, Steph)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Avon/Vail, CO", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: OPERATIONAL FREEDOM", S["section"]))
story.append(Paragraph("Chris wants Amy to run estate planning so he can focus on selective probate work and stop being the firm's single point of failure.", S["subsection"]))

story.append(quote_block("Focus marketing on probate first — more urgency, higher willingness to pay, easier close. Estate plans are secondary; cross-sell post-probate."))
story.append(Spacer(1, 1))
story.append(quote_block("Amy handles estate planning volume. I want her to run that side. I'd focus on the probates."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Amy runs estate planning end-to-end.</b> Chris handles probates by choice, not necessity."))
story.append(bd("<b>Predictable client flow.</b> New cases arrive from a system, not from who Chris called last month."))
story.append(bd("<b>Denver/Front Range presence.</b> Digital marketing is the only path into that market."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No digital presence.</b> Zero ads, no contact form — invisible to anyone who searches."))
story.append(b("<b>Referral-only model.</b> Every new client still requires Chris personally; scale is impossible."))
story.append(b("<b>Amy not yet probate-capable.</b> Chris cannot step back from that practice area yet."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Fills Amy's pipeline — Chris stops being the bottleneck to growth."))
story.append(bd("Claims Vail Valley digital position before a competitor does; $50/call LSA market is untapped now."))
story.append(bd("Builds Front Range authority before Denver competitors consolidate further."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $7,397/mo bundled</b>", S["subsection"]))
story.append(b("~$800K legal revenue; aggressive Denver goals + $14K ad spend exceed Starter cap — Growth justified."))
story.append(b("Mountain market: low paid search competition; first-mover window available now, not indefinitely."))
story.append(b("Website needs full rebuild — no contact form, no landing pages; Full Service required."))
story.append(b("Dual-market strategy (Vail + Denver) requires full-service; piecemeal won't cover both."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Chris a weekly framework for hiring, intake, and systems decisions growth will force him to make."))
story.append(bd("Holds Chris to a revenue target — turns 'I want to grow' into a weekly, measurable commitment."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Team of 3 (under 5), ~$800K revenue — Elite Coach Plus correct tier; Master's Circle requires 5+."))
story.append(b("No intake system or team processes — coaching is where those get built before volume arrives."))
story.append(b("No revenue goal set on call — coaching kicks off with 12-month target and KPI tracking."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Silversmith Legal — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Generates estate planning and probate leads in the Vail Valley at the lowest CPL in Colorado — market is untapped by paid ads."))
story.append(bd("Scales to cover the Denver Front Range as revenue grows, allowing Chris to enter that market without waiting years for organic SEO alone."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — Google PPC $2,000 + LSA $1,000 + Meta $500. Mountain market starting spend."))
story.append(b("<b>Aggressive:</b> $14,000/mo — Growth tier cap; includes Front Range expansion spend."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~4 cases x $4K avg = $16K/mo vs. $3.5K spend = ~4.6x return (est.)."))
story.append(b("<b>Aggressive:</b> ~13 cases x $4K avg = $52K/mo vs. $14K spend = ~3.7x return (est.)."))
story.append(Paragraph("<i>All figures are estimates based on industry CPL benchmarks and 15% close rate default. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Estate planning/probate mountain market minimums: PPC $2,000 + LSA $1,000 + Meta $500 = $3,500."))
story.append(b("<b>Aggressive:</b> $1.6M goal x 20% / 12 = $26.7K. Growth cap = $14K (applied). Blended CPL ~$150, 93 leads, 15% close."))
story.append(b("Aggressive total spend: $10,597 + $14,000 = $24,597/mo = ~35.8% of revenue. At cap; conservative start recommended."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"Will digital ads bring the right clients? My HNW clients come from referrals."', S["objection_q"]))
story.append(Paragraph("Legacy Law Group (245 reviews) built their entire Front Range practice on digital. Probate clients in crisis search Google — they don't wait for a referral. Probate is the primary focus precisely because of urgency and high willingness to pay.", S["objection_a"]))

story.append(Paragraph('"I am not sure the spend makes sense at my revenue level."', S["objection_q"]))
story.append(Paragraph("Conservative total investment is 20.5% of monthly revenue — well under 35% cap. LSA market is ~$50/qualified call with no dominant competitor. Estimated 4 cases x $4K = $16K/mo from $3.5K spend.", S["objection_a"]))

story.append(Paragraph('"Referrals are already working — why change it?"', S["objection_q"]))
story.append(Paragraph("Referrals cap growth at whatever Chris's network generates. Heckman O'Connor (40+ years, Vail Valley) is not running ads yet — that window closes when they do. Denver requires digital; referrals won't get the firm there.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("Website rebuild, Google Ads + LSA + Meta, local SEO, GBP management.", S["price_detail"]),
     Paragraph("<strike>$8,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, practice area masterminds, quarterly workshops.", S["price_detail"]),
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
    "Total: $10,597/mo + $3,500–$14,000 ad spend  |  Save $1,897/mo by bundling  |  20.5%–35.8% of revenue",
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
