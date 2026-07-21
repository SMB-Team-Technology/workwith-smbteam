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

OUTPUT_PATH = "fabbrini/Fabbrini Law Group LLC_July 24, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Fabbrini Law Group LLC", S["title"]))
story.append(Paragraph("Sales Companion  |  July 24, 2026  |  Rep: Nick Holderman", S["subtitle"]))
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
    [Paragraph("Jim Fabbrini", S["snap_value"]),
     Paragraph("$3M+ (HubSpot est.)", S["snap_value"]),
     Paragraph("5 staff + owner", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Chicago, IL (2 loc.)", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: STRATEGIC FREEDOM", S["section"]))
story.append(Paragraph("Jim wants to stop personally handling daily casework and tech-building, and become a strategic, KPI-driven owner who monitors the numbers instead of building every tool himself.", S["subsection"]))

story.append(quote_block("escape daily legal work and focus on business strategy"))
story.append(Spacer(1, 1))
story.append(quote_block("shift from daily legal work to a strategic, data-driven ownership role, monitoring key performance indicators (KPIs) to identify and fix bottlenecks"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Step back from casework.</b> A strategic, KPI-driven role, not daily case and tool work."))
story.append(bd("<b>One place to see the numbers.</b> A dashboard, not one he builds himself."))
story.append(bd("<b>Case flow beyond referrals.</b> A predictable pipeline, not reputation alone."))
story.append(bd("<b>Proof the team is real.</b> He's been burned by weak vendor pitches before."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Zero digital visibility.</b> Absent from all 6 local searches tested."))
story.append(b("<b>NAP is fragmented.</b> 4+ address variants, 2 unmerged GBP listings."))
story.append(b("<b>No ops layer.</b> Jim builds his own AI tools/dashboard solo."))
story.append(b("<b>No centralized KPI view.</b> No dashboard tracks case-to-revenue yet."))
story.append(b("<b>Vendor skepticism.</b> Burned by prior Fractional CTO pitches."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns 25 years of reputation into a system that produces cases on its own."))
story.append(bd("Fixes the NAP/local invisibility losing cases to Disparti, Salvi, and Rosenfeld."))
story.append(bd("Establishes a trackable lead-flow KPI his own dashboard is trying to capture."))

story.append(Paragraph("<b>Full Service Marketing — Platinum  |  $15,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $3M+ (HubSpot-sourced) qualifies for Platinum per the tier table."))
story.append(b("PI requires at minimum Starter; Platinum justified by total invisibility."))
story.append(b("2 confirmed locations rule out Essentials-tier regardless of revenue."))
story.append(b("Platinum's $150K/mo ad cap covers both spend ranges recommended here."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Dedicated Fractional COO Director builds/runs the KPI dashboard he's building alone."))
story.append(bd("Peer group of firm owners solving the same step-back-from-day-to-day problem."))
story.append(bd("Moves the operational/strategic workload off his plate without losing accountability."))

story.append(Paragraph("<b>Master's Circle + FCOO Director  |  $8,394/mo bundled</b>", S["subsection"]))
story.append(b("CORRECTED: notes confirm 5 dedicated staff — system's 'under 5 team' default was wrong."))
story.append(b("Revenue $3M+ clears the $2M+ threshold for Master's Circle + FCOO Director."))
story.append(b("FCOO Director matches Jim's goal: strategic, KPI-driven ownership role."))
story.append(b("Includes weekly coaching, masterminds, quarterly + 1 annual in-person workshop."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Fabbrini — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts dollars behind Google Search, LSA, and Meta — channels where competitors are already winning cases that should be his."))
story.append(bd("Gives Jim a real, trackable cost-per-case number instead of an unmeasured referral pipeline."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,500/mo — minimum viable spend across Google Search, LSA, and Meta for personal injury in a high-competition Chicago market."))
story.append(b("<b>Aggressive:</b> $30,000/mo — scaled toward growth, capped well under Platinum's $150,000 ceiling and the firm's 35% total-spend cap."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 2-3 cases x $6.5K = $16.9K/mo vs. $7.5K spend = 2.3x return."))
story.append(b("<b>Aggressive:</b> 12-13 cases x $6.5K = $81.9K/mo vs. $30K spend = 2.7x return."))
story.append(Paragraph("<i>All figures are estimates using a default case value (none was discussed on this call). Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Accident & Injury blended CPL (~$428 with 20% cushion). $7,500 / $428 = ~17-18 leads x 15% close rate = 2-3 cases."))
story.append(b("<b>Aggressive:</b> No revenue goal stated; used 2x current revenue default ($6M) x 20% / 12 = $100K, x1.5 Chicago Tier 1 multiplier. Capped down to $30,000 by the 35% total-spend rule ($87,500 cap minus $24,391 fixed MRR = $54,112 max)."))
story.append(b("Total spend at aggressive: $24,391 + $30,000 = $54,391/mo = 21.8% of revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"This call was supposed to be about a Fractional CTO, not marketing."', S["objection_q"]))
story.append(Paragraph("Acknowledge that directly — the growth audit surfaced a separate, immediate opportunity (zero digital visibility, NAP fragmented across 4+ addresses) costing him cases today. Flag internally that this is also an unusually strong Legal AI Workforce / Fractional CTO fit and route that conversation to the LAW team in parallel.", S["objection_a"]))

story.append(Paragraph('"I already get plenty of referrals — why spend on ads?"', S["objection_q"]))
story.append(Paragraph("Disparti Law Group has ~3,400+ reviews and dominates personal injury search results; Fabbrini did not appear in any of 6 local searches tested despite 25 years in practice. Referrals alone are not converting into digital visibility.", S["objection_a"]))

story.append(Paragraph('"I built my own AI tools — why pay for a dashboard?"', S["objection_q"]))
story.append(Paragraph("The FCOO Director builds and runs the KPI dashboard so Jim is no longer the one maintaining it on top of a full caseload — this is delegation of work he is already doing, not duplication.", S["objection_a"]))

story.append(Paragraph('"Is this within budget?"', S["objection_q"]))
story.append(Paragraph("Total spend at the aggressive ad level is $54,391/mo, or 21.8% of estimated monthly revenue — comfortably under the firm's 35% total-spend cap.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Platinum</b>", S["price_main"]),
     Paragraph("$15,997/mo", S["price_main"])],
    [Paragraph("Website, local SEO, Google Ads, LSA, and Meta management.", S["price_detail"]),
     Paragraph("<strike>$18,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle + FCOO Director</b>", S["price_main"]),
     Paragraph("$8,394/mo", S["price_main"])],
    [Paragraph("Dedicated FCOO Director plus Master's Circle peer coaching.", S["price_detail"]),
     Paragraph("<strike>$10,794</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,500–$30,000/mo", S["price_main"])],
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
    "Total: $24,391/mo + $7,500–$30,000 ad spend  |  Save $5,400/mo by bundling  |  12.8%–21.8% of revenue (under 35% cap)",
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
