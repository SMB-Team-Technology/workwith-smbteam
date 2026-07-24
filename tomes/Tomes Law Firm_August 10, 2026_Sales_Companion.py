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

OUTPUT_PATH = "tomes/Tomes Law Firm_August 10, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Tomes Law Firm, PC", S["title"]))
story.append(Paragraph("Sales Companion  |  August 10, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
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
    [Paragraph("Frances Tomes", S["snap_value"]),
     Paragraph("~$650K (transcript)", S["snap_value"]),
     Paragraph("7 (5 remote)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Freehold, NJ", S["snap_value"])],
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
story.append(Paragraph("Frances wants a firm that runs without her — the 60-hour weeks and staff micromanagement to finally end, not just more revenue.", S["subsection"]))

story.append(quote_block("Frances is struggling with inefficient staff, working 60hr weeks, and feeling overwhelmed despite $650k revenue"))
story.append(Spacer(1, 1))
story.append(quote_block("Address foundation issues before considering lead generation services"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>A team that runs without her.</b> Tired of micromanaging inefficient staff who lack follow-through."))
story.append(bd("<b>Real time back.</b> Fewer than 60-hour weeks — not just more revenue at the same personal cost."))
story.append(bd("<b>A fix that sticks.</b> Unlike the 2-year HTM coaching engagement and the local COO engagement now ending."))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No defined intake process.</b> Staff described as reactive, lacking follow-through."))
story.append(b("<b>WhatsApp coordination.</b> Cuts Frances out of visibility into day-to-day handling."))
story.append(b("<b>High turnover.</b> ~30 employees turned over since 2020 — constant re-training, no bench strength."))
story.append(b("<b>Two prior fixes ending.</b> 2-year HTM coaching and local part-time COO haven't solved the core issue."))

story.append(thin_rule())

# ── Why No Marketing Package This Round ──
story.append(Paragraph("Why No Marketing Package This Round", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Protects her focus and budget for the fix she actually asked about — operations — instead of adding a service she explicitly said to hold off on."))
story.append(bd("Keeps this recommendation matched to what she said on the call, building trust instead of reading as a generic upsell."))

story.append(Paragraph("<b>No marketing package this round</b>", S["subsection"]))
story.append(b("Transcript states directly: \"Address foundation issues before considering lead generation services.\""))
story.append(b("Revenue/practice mix would otherwise qualify for Full Service Marketing Starter ($4,997/mo) — held back intentionally, not due to ineligibility."))
story.append(b("No named competitor (Detzky Hunter & DeFillippo, Manchel, Lyons & Associates) was confirmed running ads either — market isn't urgently contested yet."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Puts a dedicated Fractional COO Advisor directly on the exact problem she called about — an inefficient, high-turnover team she's tired of managing."))
story.append(bd("Pairs that with weekly group coaching and mastermind access, so she isn't rebuilding accountability alone this time."))
story.append(bd("Gives her a real shot at working under 60 hours a week without revenue dropping."))

story.append(Paragraph("<b>Elite Coach Plus + FCOO Advisor  |  $5,694/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$650K sits in the $400K–$1M band; FCOO products require $500K+, which this firm clears."))
story.append(b("Team of 7 mid-transition off a part-time local COO matches the \"growing team\" tier exactly."))
story.append(b("Master's Circle not eligible — no dedicated ops/marketing/intake staff confirmed on the call."))
story.append(b("$5,694/mo is well under the 35% revenue cap ($18,958/mo at $650K annual)."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Tomes — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Ad Spend This Round ──
story.append(Paragraph("Why No Ad Spend This Round", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Avoids spending her budget on lead generation before the team and intake can actually handle more volume."))
story.append(bd("Keeps the recommendation credible — she is not being sold something she told the rep to hold off on."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $0/mo — no ad spend recommended in Phase 1."))
story.append(b("<b>Aggressive:</b> $0/mo — deferred to Phase 2 once operations are stabilized."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> N/A — no ad spend this phase."))
story.append(b("<b>Aggressive:</b> N/A — no ad spend this phase."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("N/A this round — marketing excluded per the call-purpose override (see section_11_workings.txt)."))
story.append(b("Total spend at $5,694/mo bundled (no ad spend) = 10.5% of $650K annual revenue. Well under the 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"Why aren\'t we doing any marketing? Don\'t I need more clients?"', S["objection_q"]))
story.append(Paragraph("You told us directly on the call to fix operations before lead generation — we're following that, not skipping marketing because you don't qualify. Full Service Marketing Starter ($4,997/mo) is ready to add in Phase 2 the moment your team can handle more volume.", S["objection_a"]))

story.append(Paragraph('"I already tried a COO and a coaching program — why will this be different?"', S["objection_q"]))
story.append(Paragraph("Your prior engagements (2-year HTM coaching, local part-time COO) gave you a 180-page policy manual and staff KPIs — real infrastructure already built. What's been missing is someone who owns making the team actually follow it day to day. That's exactly the FCOO Advisor's job.", S["objection_a"]))

story.append(Paragraph('"Is $5,694/month worth it if I don\'t even know my real profit margin yet?"', S["objection_q"]))
story.append(Paragraph("That's exactly why Phase 3 adds a Fractional CFO Advisor once operations stabilize. At $5,694/mo you're at about 10.5% of your stated $650K revenue — well under a level that would strain cash flow even before margins are confirmed.", S["objection_a"]))

story.append(Paragraph('"What about competitors already ahead of me, like Lyons & Associates?"', S["objection_q"]))
story.append(Paragraph("None of the three named threats — Lyons & Associates, Detzky Hunter & DeFillippo, or Robert Manchel — were confirmed running paid ads either. The market isn't moving fast enough to require lead-gen spend before your operations are fixed.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Elite Coach Plus + FCOO Advisor</b>", S["price_main"]),
     Paragraph("$5,694/mo", S["price_main"])],
    [Paragraph("Fractional COO Advisor + Elite Coach Plus coaching, masterminds, workshops.", S["price_detail"]),
     Paragraph("<strike>$7,294</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Marketing Package</b>", S["price_main"]),
     Paragraph("$0/mo — deferred", S["price_main"])],
    [Paragraph("Held per Frances's explicit request to fix operations before lead generation.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$0/mo (Phase 1)", S["price_main"])],
    [Paragraph("Deferred to Phase 2 — see growth roadmap in the audit.", S["price_detail"]),
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
    "Total: $5,694/mo + $0 ad spend  |  Save $1,600/mo by bundling  |  10.5% of revenue (well under 35% cap)",
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
