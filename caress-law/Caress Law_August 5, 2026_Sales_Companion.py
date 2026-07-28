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

OUTPUT_PATH = "caress-law/Caress Law_August 5, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Caress Law", S["title"]))
story.append(Paragraph("Sales Companion  |  August 5, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Tammi Caress", S["snap_value"]),
     Paragraph("$2.2M-$2.7M", S["snap_value"]),
     Paragraph("~3 + COO", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Portland, OR", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: TIME / FREEDOM", S["section"]))
story.append(Paragraph(
    "Tammi wants a firm that runs on automation and qualified leadership, not on her "
    "personal follow-through, so she can focus on strategy instead of every system.",
    S["subsection"]))

story.append(quote_block(
    "Tammi is the operational fallback for all systems and processes, preventing her "
    "from focusing on strategic growth."))
story.append(Spacer(1, 1))
story.append(quote_block(
    "The Fractional CTO role should free up owner time, increase team capacity, and "
    "enable growth without adding staff."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Time back.</b> Stop being the fallback for every system and process in the firm."))
story.append(bd("<b>Real delegation.</b> Operational leadership she can actually trust, not just a title."))
story.append(bd("<b>Predictable profit.</b> Move probate/trust admin from hourly to flat fees."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Underqualified COO.</b> Current fractional COO lacks law-firm-specific experience."))
story.append(b("<b>Manual workflows.</b> 39-step probate process, bill review, mail, and expenses all done by hand."))
story.append(b("<b>No attorney KPIs yet.</b> Accountability structure has not been built."))
story.append(b("<b>Call was CTO-focused, not marketing.</b> No lead-gen/SEO/ads gap was raised — do not lead with a marketing pitch."))

story.append(thin_rule())

# ── Why This AI & Automation Package ──
story.append(Paragraph("Why This AI & Automation Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Puts a dedicated Fractional CTO on the named automation targets — not a generic tool."))
story.append(bd("Turns the probate reduction, bill review, mail, and expense compilation into monthly deliverables."))

story.append(Paragraph("<b>Legal AI Workforce — Fractional CTO Level 2  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $2.2M-$2.7M sits squarely in this tier's $1.5M-$3M target band."))
story.append(b("1-3 custom automations/month, bi-monthly CTO calls, Clio/Lawmatics/Outlook integration."))
story.append(b("Plus one-time Foundation Sprint: $14,997 (standalone $19,997) for upfront discovery/build."))
story.append(b("ESCALATION: confirm LAW delivery capacity with sales rep before proposing."))

story.append(thin_rule())

# ── Why This Operational Package ──
story.append(Paragraph("Why This Operational Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Replaces an underqualified COO relationship with real law-firm operational experience."))
story.append(bd("Finally gets attorney KPIs and accountability structure built — work that has stalled with Tammi."))

story.append(Paragraph("<b>FCOO Advisor  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1M+, team under 5, explicitly operational-focus fit per the transcript."))
story.append(b("Includes weekly group coaching, practice area masterminds, quarterly workshop access, one annual in-person workshop."))
story.append(b("No separate Elite Coach Plus needed — these deliverables are bundled into this price."))
story.append(b("Directly replaces the current external COO's gap: law-firm-specific experience she does not have today."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Caress Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Marketing Package / Ad Spend ──
story.append(Paragraph("Why No Marketing Package or Ad Spend", S["section"]))

story.append(Paragraph("<b>What this protects for her:</b>", S["subsection"]))
story.append(bd("Keeps the proposal matched to what she actually asked for on the call — automation and operations."))
story.append(bd("Avoids pitching a $10K+/mo marketing bundle she never raised a need for, which would hurt trust, not build it."))

story.append(Paragraph("<b>Why marketing was excluded:</b>", S["subsection"]))
story.append(b("The 57-minute call never discussed marketing, SEO, ads, or lead generation."))
story.append(b("package_decision.json flagged Full Service Marketing Dominate ($10,497/mo) on revenue alone — it cannot read the transcript."))
story.append(b("Growth Health/Lead Gen findings (urgency 5/10) are real competitive context, not a package trigger here."))
story.append(Paragraph("<i>If she raises marketing later, it's a legitimate future-phase add — see roadmap Phase 3.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"Why not just fix our current COO instead of paying for a new one?"', S["objection_q"]))
story.append(Paragraph(
    "Her current fractional COO lacks law-firm-specific experience — that is the root problem, not a fixable "
    "skills gap. FCOO Advisor replaces that gap with operators who know law firm KPIs and workflows specifically.",
    S["objection_a"]))

story.append(Paragraph('"Is $8,294/mo justified without a marketing pitch?"', S["objection_q"]))
story.append(Paragraph(
    "This price reflects exactly what she asked for: a Fractional CTO building the automations she named, plus "
    "qualified operational leadership. Every dollar maps to a stated call need, not an unrequested add-on.",
    S["objection_a"]))

story.append(Paragraph('"What does the $14,997 Foundation Sprint add on top of the monthly fee?"', S["objection_q"]))
story.append(Paragraph(
    "It is the one-time discovery/build phase for the four named automation targets before ongoing CTO "
    "management begins. Standalone Sprint pricing is $19,997, so this is a bundled $5,000 savings.",
    S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Legal AI Workforce — Fractional CTO Level 2</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("Monthly custom automation builds + CTO strategy calls.", S["price_detail"]),
     Paragraph("<strike>$5,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>FCOO Advisor</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Law-firm-experienced ops leadership + bundled group coaching.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>One-Time Foundation Sprint</b>", S["price_main"]),
     Paragraph("$14,997 one-time", S["price_main"])],
    [Paragraph("Paired with Fractional CTO Level 2 (standalone $19,997).", S["price_detail"]),
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
    "Total Monthly: $8,294/mo  |  Save $1,300/mo by bundling  |  Plus $14,997 one-time Foundation Sprint (not in monthly total)  |  No ad spend recommended",
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
