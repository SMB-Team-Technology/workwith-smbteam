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

OUTPUT_PATH = "cfs/CFS_Attorneys_August_7_2026_Sales_Companion.pdf"


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

story.append(Paragraph("CFS Attorneys (Cable, Fleisher &amp; Sosebee, PLLC)", S["title"]))
story.append(Paragraph("Sales Companion  |  August 7, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Blake Mensing (Champion)", S["snap_value"]),
     Paragraph("$570K est. (low conf.)", S["snap_value"]),
     Paragraph("5 attorneys", S["snap_value"]),
     Paragraph("3", S["snap_value"]),
     Paragraph("Unstated (15% default)", S["snap_value"]),
     Paragraph("Northampton, MA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: AI-FORWARD OPERATING MODEL / RETENTION", S["section"]))
story.append(Paragraph("Blake wants to prove CFS can become a modern, AI-run firm before his October contract decision — and the firm-level need is freeing partners from admin work that is costing billable hours and clients.", S["subsection"]))

story.append(quote_block("Partners are a bottleneck, wasting billable hours on admin (e.g., drafting licensing/service agreements) and causing client attrition."))
story.append(Spacer(1, 1))
story.append(quote_block("Blake's contract expires in October; he is also considering a move to an AI-forward firm."))
story.append(Spacer(1, 1))
story.append(quote_block("Blake receives unpredictable, handwritten paychecks, sometimes weeks late."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Prove the AI-forward move</b> before his October contract decision."))
story.append(bd("<b>Get partners out of admin work</b> — drafting is costing billable hours and clients."))
story.append(bd("<b>Real financial visibility</b> — his own pay is manual and sometimes weeks late."))
story.append(bd("<b>A firm that runs itself</b> — not more leads, but less dependence on 4 partners."))

story.append(Spacer(1, 1))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No admin/ops staff.</b> Partners absorb 100% of non-legal work."))
story.append(b("<b>No formal AI policy.</b> Only ad hoc ChatGPT/Claude use, no firm-wide rollout."))
story.append(b("<b>No financial visibility.</b> No profit tracking; payroll itself is informal."))
story.append(b("<b>The October clock is already running.</b> A hard external deadline."))

story.append(thin_rule())

# ── Why This AI Package ──
# NOTE: No marketing package is recommended this phase — the Call-Purpose
# Override applies (see section_11_workings.txt). The Aug 7 call was scoped
# entirely around SMB Team's AI Workforce platform, not marketing/lead-gen,
# and no marketing gap was raised in the transcript. This section covers the
# Legal AI Workforce package in the marketing package's slot.
story.append(Paragraph("Why This AI Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts a dedicated Fractional CTO in charge of the rollout — Blake doesn't manage it himself."))
story.append(bd("Turns Blake's own local-LLM experiment into a firm-wide, supported system."))

story.append(Paragraph("<b>Fractional CTO Level 1 (AI Accelerator)  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Revenue est. $570K clears the $500K LAW floor; firm is not solo (5 attorneys), so LAW is not excluded."))
story.append(b("Blake's own local-LLM build makes him an adopter, not a skeptic to convince."))
story.append(b("Stated call focus is explicitly the AI Workforce platform — the actual product asked for, not an upsell."))
story.append(b("Foundation Sprint ($14,997 bundled w/ L1, vs. $19,997 standalone) gets first Skills live in 90 days."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the SOPs/delegation framework that turn \"we have AI now\" into a firm that runs differently."))
story.append(bd("Builds a real profit plan — first read on what each practice area pays per hour."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue band ($400K-$1M) and team under 5 point to Elite Coach Plus, not Master's Circle."))
story.append(b("Coach Essentials/Essentials Plus are eliminated products — not eligible regardless of revenue."))
story.append(b("Not named on the call, but the firm-level DBM (partners bottlenecked on admin) is what its SOP work addresses."))
story.append(b("Combined investment ($6,497/mo) is well under the 35% of revenue cap (~$16,625/mo)."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("CFS Attorneys — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
# NOTE: No ad spend is recommended this phase — see Call-Purpose Override.
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Nothing to project this phase — marketing wasn't the subject of this call, so no ad spend is proposed."))
story.append(bd("Once AI + coaching are in place, marketing can be scoped separately — CFS has a genuine wide-open paid-search gap worth revisiting."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("Not applicable this phase — no marketing package is being recommended. Revisit at Growth Roadmap Phase 3."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("N/A this phase — no ad spend recommended."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("Not part of this call's scope — stated focus is the AI Workforce platform; marketing was never raised in the transcript."))
story.append(b("Total spend this phase: $6,497/mo in AI + coaching fees only — 0% ad spend, well under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"Why isn’t marketing part of this proposal?"', S["objection_q"]))
story.append(Paragraph("Marketing wasn't the subject of this call. Blake's own ask was a custom AI Workforce plan — deliverables, roadmap, pricing, timeline — and no marketing gap was raised on the discovery call.", S["objection_a"]))

story.append(Paragraph('"Can the firm afford $6,497/mo given how informal our finances are?"', S["objection_q"]))
story.append(Paragraph("$6,497/mo is under 14% of the firm's estimated $47,500/mo revenue run rate, well under the 35% cap. Elite Coach Plus's profit-plan work is built specifically to fix the financial visibility problem driving this concern.", S["objection_a"]))

story.append(Paragraph('"Is a Fractional CTO overkill for a firm this size?"', S["objection_q"]))
story.append(Paragraph("Partners are already at capacity on billable work and admin. A done-with-you Fractional CTO means no one has to personally manage the rollout — the alternative, DIY-only AI Essentials, assumes spare bandwidth this firm doesn't have.", S["objection_a"]))

story.append(Paragraph('"How do we protect attorney-client privilege with AI tools?"', S["objection_q"]))
story.append(Paragraph("Blake flagged this directly — confirm zero data retention and anonymization details with the implementation team ahead of the call. This is the exact question the Foundation Sprint's security review is scoped to answer.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Fractional CTO Level 1 (AI Accelerator)</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("AI implementation led by a dedicated Fractional CTO, no partner bandwidth needed.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, SOPs, delegation framework, profit-plan groundwork.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("Not part of this phase", S["price_main"])],
    [Paragraph("Marketing was not the subject of this call — see Growth Roadmap Phase 3.", S["price_detail"]),
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
    "Total: $6,497/mo, no ad spend this phase  |  Save $797/mo by bundling  |  ~13.7% of est. revenue this phase (well under 35% cap)",
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
