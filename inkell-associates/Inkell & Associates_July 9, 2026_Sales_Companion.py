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

OUTPUT_PATH = "inkell-associates/Inkell & Associates_July 9, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Inkell &amp; Associates (The Inkell Firm, LLC)", S["title"]))
story.append(Paragraph("Sales Companion  |  July 9, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Yuri Griffin", S["snap_value"]),
     Paragraph("$2.2M ('25) / $5M+ ('26 proj.)", S["snap_value"]),
     Paragraph("24 + 2-3 outsourced", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("~50% (target 80%)", S["snap_value"]),
     Paragraph("Wilmington, DE", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM FROM BEING THE BOTTLENECK", S["section"]))
story.append(Paragraph("Griffin wants an autonomous firm where systems — not him personally — drive performance and catch what falls through.", S["subsection"]))

story.append(quote_block("An autonomous firm where systems drive performance, allowing Griffin to focus on strategic work."))
story.append(Spacer(1, 1))
story.append(quote_block("Primarily PPC and LSA. High lead volume but low quality (e.g., already represented, looking to switch firms)."))
story.append(Spacer(1, 1))
story.append(quote_block("Shifting focus to litigation, which generates double the revenue per day ($40.22) compared to pre-litigation ($34.33)."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Step out of the bottleneck seat.</b> Stop being the only one who can solve problems firm-wide."))
story.append(bd("<b>An accountability system.</b> Catch dropped follow-ups and missed scripts without him watching."))
story.append(bd("<b>Focus on strategy.</b> Spend time on growth strategy, not day-to-day firefighting."))

story.append(Spacer(1, 1))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No management layer.</b> All operational knowledge still runs through Griffin."))
story.append(b("<b>Intake gaps.</b> ~50% close rate vs. 80% target; ~1/3 of opportunities mishandled."))
story.append(b("<b>Invisible financials.</b> Visibility lives only in Griffin's personal dashboard."))
story.append(b("<b>Lead quality, not volume.</b> PPC/LSA generate volume, but many leads are already represented."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns two channels that already work (PPC, LSA) into channels that convert."))
story.append(bd("Builds the geo pages and review consolidation to match review strength (4.9★/324) to search visibility."))

story.append(Paragraph("<b>Dominate — Full Service Marketing  |  $10,497/mo bundled</b>", S["subsection"]))
story.append(b("2025 revenue ($2.2M) sits in the Growth band, but the firm is tracking to double its own $3M 2026 goal."))
story.append(b("Aggressive goals within the $1M+ band move the tier up to Dominate per the boundary rule."))
story.append(b("Dominate's $75,000 ad spend cap comfortably covers the $50,000 aggressive recommendation."))
story.append(b("Stand-alone price is $12,497/mo — bundled saves $2,000/mo."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts a Fractional COO Director on the exact solution Griffin proposed on the call — 10-15+ years building systems."))
story.append(bd("Gives leadership beyond Griffin group coaching so accountability is reinforced firm-wide, not just at the top."))

story.append(Paragraph("<b>Master's Circle + FCOO Director  |  $8,394/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $2M+ and team 5+ with dedicated staff matches this table row exactly."))
story.append(b("Deliverables include weekly group coaching, masterminds, quarterly workshops, one annual in-person workshop — all included."))
story.append(b("Stand-alone price is $10,794/mo ($4,997 + $5,797) — bundled saves $2,400/mo."))
story.append(b("Directly answers the DBM: no independent management layer exists beneath Griffin today."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Inkell &amp; Associates — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Keeps spend inside the two channels the firm already trusts (PPC, LSA) instead of forcing new channels the firm has not asked for."))
story.append(bd("Gives a clear, defensible range from minimum viable to full growth-goal-matching spend, both under Dominate's $75,000 cap."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $12,000/mo — MVA/Car Accident channel minimums: Google PPC $10,000 + LSA $2,000."))
story.append(b("<b>Aggressive:</b> $50,000/mo — full budget matching the firm's own $3M 2026 goal via the 20% rule."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 8 cases x $7.5K = $60K/mo vs. $12K spend = 5.0x return."))
story.append(b("<b>Aggressive:</b> 40 cases x $7.5K = $300K/mo vs. $50K spend = 6.0x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Case value of $7,500 is the MVA/Car Accident default midpoint — not a transcript-stated figure.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> MVA/Car Accident minimums: PPC $10,000 + LSA $2,000 = $12,000. No Meta — firm's stated goal is optimizing existing channels."))
story.append(b("<b>Aggressive:</b> $3M goal x 20% / 12 = $50,000. Wilmington DE is Tier 4 (1.0x) = $50,000. Reverse-math check (~$31,000) is lower, so 20% rule figure is used."))
story.append(b("Total spend at aggressive: $50,000/mo ad spend + $18,891/mo management = $68,891/mo = ~2.8% of projected $2.2M-5M annualized revenue base. Well under the 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We are already running PPC and LSA ourselves — why do we need to pay someone else to manage it?"', S["objection_q"]))
story.append(Paragraph("The channels work — cost per lead is reasonable ($644 PPC, $252 LSA) — but quality is the problem, not access. Dominate is built to fix targeting and qualification on the channels already proven to work, not replace them.", S["objection_a"]))

story.append(Paragraph('"$18,891/mo plus ad spend feels like a lot for a firm our size."', S["objection_q"]))
story.append(Paragraph("At 2025 revenue of $2.2M projected to exceed $5M in 2026, this investment is well under the 35% total spend cap even at the aggressive ad spend level — and it targets the exact gap (close rate near 50% vs. 80% target) that is costing more in lost cases than the investment itself.", S["objection_a"]))

story.append(Paragraph('"Griffin already has people running intake and operations — why do we need a fractional COO?"', S["objection_q"]))
story.append(Paragraph("The team exists, but there is no accountability layer independent of Griffin — that is Griffin's own words on the call. An FCOO Director does not replace the team; it gives the team a structure that does not depend on Griffin catching every gap personally.", S["objection_a"]))

story.append(Paragraph('"Our reviews are already strong (4.9/324) — why does local SEO matter?"', S["objection_q"]))
story.append(Paragraph("That review strength is currently not converting into organic visibility — the firm did not surface in top results for its own core search terms this session, while a weaker-reviewed competitor (Silverman, McDonald & Friedman, 4.8/313) consistently does.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Dominate — Full Service Marketing</b>", S["price_main"]),
     Paragraph("$10,497/mo", S["price_main"])],
    [Paragraph("Optimized PPC/LSA management, geo pages, review/local SEO consolidation.", S["price_detail"]),
     Paragraph("<strike>$12,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle + FCOO Director</b>", S["price_main"]),
     Paragraph("$8,394/mo", S["price_main"])],
    [Paragraph("Fractional COO Director, group coaching, masterminds, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$10,794</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$12,000–$50,000/mo", S["price_main"])],
    [Paragraph("Goes to Google and LSA — not to SMB Team.", S["price_detail"]),
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
    "Total: $18,891/mo + $12,000–$50,000 ad spend  |  Save $4,400/mo by bundling  |  Well under the 35% of revenue cap",
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
