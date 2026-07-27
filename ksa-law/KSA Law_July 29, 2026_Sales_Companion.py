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

OUTPUT_PATH = "ksa-law/KSA Law_July 29, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("KSA Law", S["title"]))
story.append(Paragraph("Sales Companion  |  July 29, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Kelly Sullivan Angles", S["snap_value"]),
     Paragraph("$480K-$720K (indiv. run rate)", S["snap_value"]),
     Paragraph("7", S["snap_value"]),
     Paragraph("3", S["snap_value"]),
     Paragraph("Unstated (15% default)", S["snap_value"]),
     Paragraph("Kansas City, MO", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE / STOP SELF-FUNDING", S["section"]))
story.append(Paragraph("Kelly wants to scale KSA Law toward $5M ARR as the definitive fractional-GC platform in her market — without continuing to personally capitalize the firm's cash flow gaps to get there.", S["subsection"]))

story.append(quote_block("The litigation team is at capacity, preventing pursuit of new work."))
story.append(Spacer(1, 1))
story.append(quote_block("Cash Flow: Strain from slow-paying clients (30-45 day cycles) requires Kelly to capitalize expenses."))
story.append(Spacer(1, 1))
story.append(quote_block("Goal: Break-even by October 2026; profitability by EOY 2026."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Scale to $5M ARR.</b> As the definitive fractional-GC platform in her market."))
story.append(bd("<b>Stop personally funding the firm.</b> End the cash flow strain of capitalizing expenses herself."))
story.append(bd("<b>Close more proposals.</b> Close more of the VC-fund engagements already coming her way."))
story.append(bd("<b>Protect her team's growth.</b> Her stated personal motivation as the firm scales."))

story.append(Spacer(1, 1))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No proposal process.</b> Every pitch runs through Kelly with no framework or close-rate baseline."))
story.append(b("<b>No financial visibility.</b> No view into engagement profitability; firm hasn't hit break-even."))
story.append(b("<b>Litigation at capacity.</b> The newest practice line is already turning away work."))
story.append(b("<b>No leadership layer.</b> No manager beneath Kelly, who also runs Sandberg Phoenix's KC office."))
story.append(b("<b>Marketing wasn't the topic.</b> Coaching and Fractional CFO are the stated starting point, not marketing."))

story.append(thin_rule())

# ── Why This Fractional CFO Package ──
# NOTE: No marketing package is recommended this phase — the Call-Purpose
# Override applies (see section_11_workings.txt). The call was scoped around
# Business Coaching + Fractional CFO, not marketing/lead-gen, and no
# marketing gap was identified in the transcript. This section covers the
# Fractional CFO package in the marketing package's slot.
story.append(Paragraph("Why This Fractional CFO Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives Kelly a real cash flow view so she can stop personally covering firm expenses."))
story.append(bd("Builds the profit plan behind her stated break-even (Oct 2026) and profitability (EOY 2026) targets."))

story.append(Paragraph("<b>Fractional CFO (FCFO) Advisor  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ($480K-$720K stated individual run rate) clears the $400K minimum for FCFO Advisor."))
story.append(b("Cash flow strain and no financial visibility are explicit signals for adding FCFO Advisor."))
story.append(b("Transcript names Fractional CFO as one of two proposed starting engagements — stated need, not an upsell."))
story.append(b("Bundled price includes weekly group coaching, masterminds, and workshops — no separate charge."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives Kelly a coaching framework to build a repeatable proposal process and improve close rates."))
story.append(bd("Supports building a leadership layer beneath her as the team grows past 7."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue band ($400K-$1M) and a team of 7 point to Elite Coach Plus, not Master's Circle."))
story.append(b("Coach Essentials and Essentials Plus are eliminated products — not eligible regardless of revenue."))
story.append(b("Transcript names Business Coaching as the other of the two proposed starting engagements."))
story.append(b("Combined investment ($6,497/mo) is well under the 35% of revenue cap (~$16,625/mo)."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("KSA Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
# NOTE: No ad spend is recommended this phase — see Call-Purpose Override.
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Nothing to project this phase — marketing wasn't the subject of this call, so no ad spend is proposed."))
story.append(bd("Once coaching + FCFO are in place, marketing and ad spend can be scoped separately — the firm's own stated future add-on."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("Not applicable this phase — no marketing package is being recommended. Revisit at Growth Roadmap Phase 3/4."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("N/A this phase — no ad spend recommended."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("Not part of this call's scope — stated next step is coaching + Fractional CFO, marketing named only as a future add-on."))
story.append(b("Total spend this phase: $6,497/mo in coaching + CFO fees only — 0% ad spend, well under the 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"Why isn’t marketing part of this proposal?"', S["objection_q"]))
story.append(Paragraph("Marketing wasn't the subject of this call. The transcript's own proposed solution names Business Coaching and Fractional CFO as the starting point, with marketing explicitly framed as a future add-on.", S["objection_a"]))

story.append(Paragraph('"Can we afford this given the cash flow strain?"', S["objection_q"]))
story.append(Paragraph("$6,497/mo is under 14% of Kelly's own stated $40K-$60K/month individual run rate, and well under the firm's 35% cap. The FCFO Advisor engagement is built specifically to fix the cash flow strain driving this concern.", S["objection_a"]))

story.append(Paragraph('"How do we know this will improve our close rate?"', S["objection_q"]))
story.append(Paragraph("KSA Law already grew from solo to 7 people in 4 months on referrals alone with no formal process. Elite Coach Plus gives that same momentum a repeatable framework instead of leaving it to instinct.", S["objection_a"]))

story.append(Paragraph('"We don’t have bandwidth for another initiative right now."', S["objection_q"]))
story.append(Paragraph("Both packages are built around what Kelly is already doing (proposals, financial oversight), not a new initiative. Phase 2 (FCOO Advisor) is specifically what relieves her bandwidth once Phase 1 is running.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
# FILL: All pricing from the scoping calculation
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Fractional CFO (FCFO) Advisor</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Financial visibility, cash flow plan, and profit plan.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly 1:1 coaching, proposal strategy, accountability.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("Not part of this phase", S["price_main"])],
    [Paragraph("Marketing was not the subject of this call — see Growth Roadmap Phase 3/4.", S["price_detail"]),
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
    "Total: $6,497/mo, no ad spend this phase  |  Save $797/mo by bundling  |  0% of revenue this phase (well under 35% cap)",
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
