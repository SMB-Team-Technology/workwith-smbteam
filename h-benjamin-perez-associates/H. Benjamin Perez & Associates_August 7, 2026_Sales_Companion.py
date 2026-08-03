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

OUTPUT_PATH = "h-benjamin-perez-associates/H. Benjamin Perez & Associates_August 7, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("H. Benjamin Perez & Associates, P.C.", S["title"]))
story.append(Paragraph("Sales Companion  |  August 7, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("H. Benjamin Perez (Hector Perez, COO, on the call)", S["snap_value"]),
     Paragraph("~$1.98M (est., medium conf.)", S["snap_value"]),
     Paragraph("~5", S["snap_value"]),
     Paragraph("4", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Manhattan, NYC", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: A FIRM THAT RUNS ITSELF", S["section"]))
story.append(Paragraph("Hector wants growth that doesn't require the team working three times as hard — automation absorbing the repeatable work instead of more headcount.", S["subsection"]))

story.append(quote_block("Hector Perez manages operations for H. Benjamin Perez, a family/criminal law firm"))
story.append(Spacer(1, 1))
story.append(quote_block("3x revenue within one year"))
story.append(Spacer(1, 1))
story.append(quote_block("numb to tech (describing H. Benjamin Perez)"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Growth without proportional manual work.</b> 3x revenue without the team working 3x as hard."))
story.append(bd("<b>Someone else driving the rollout.</b> Wants a Fractional CTO leading it, not himself."))
story.append(bd("<b>Proof before Ben leaps.</b> Ben is \"numb\" to tech and needs a clear ROI case first."))
story.append(bd("<b>Relief on named bottlenecks.</b> After-hours coverage and the 27-of-39-step probate workflow."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Ben must personally approve every system.</b> Nothing moves without his sign-off."))
story.append(b("<b>A prior vendor pitch was rejected.</b> A ~$50k proposal was cut — they were already doing that work in-house."))
story.append(b("<b>No financial baseline exists.</b> No revenue/case-value/close-rate figures — frame ROI as time/capacity, not dollars."))
story.append(b("<b>No in-house AI expertise.</b> Exactly why a Fractional CTO fits better than a DIY tool."))
story.append(b("<b>This was an evaluation call.</b> $3,797–$9,000/mo discussed was a range, not a confirmed budget."))

story.append(thin_rule())

# ── Why This AI Automation Package ──
story.append(Paragraph("Why This AI Automation Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts a dedicated Fractional CTO in charge, so Hector isn't managing it himself."))
story.append(bd("Targets his two named bottlenecks first — manual probate steps and uncovered after-hours calls."))
story.append(bd("Gives Ben a measurable Phase 1 time-savings number before any Phase 2 ask."))

story.append(Paragraph("<b>Legal AI Workforce — Fractional CTO Level 1  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Matches the call: Hector was quoted $3,797/mo for one automation — this tier's exact stand-alone price."))
story.append(b("L1's \"done-with-you\" profile fits an owner who won't manage this himself — not L2's larger transformation scope."))
story.append(b("Optional: Law Firm AI Foundation Sprint paired with L1 — $14,997 one-time — full build-out if scoped now."))

story.append(Paragraph("<b>Why not marketing:</b>", S["subsection"]))
story.append(b("He asked to evaluate AI/CTO services, not marketing — package_decision.json's Full Service Marketing pick ($7,497/mo) is overridden per the Call-Purpose Override (see section_11_workings.txt)."))
story.append(b("Real lead-gen/SEO gaps exist (Sections 05–06) but weren't raised by Hector — flagged as a Phase 3 roadmap item, not pitched now."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("H. Benjamin Perez & Associates — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Ad Spend (This Round) ──
story.append(Paragraph("Why No Ad Spend (This Round)", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts 100% of the investment into the manual work he called about — no split budget before either is proven."))
story.append(bd("Every dollar goes to the Fractional CTO work already priced out on the call — no new spend category for Ben."))

story.append(Paragraph("<b>Ad Spend Status:</b>", S["subsection"]))
story.append(b("<b>This round:</b> $0/mo — automation-only engagement, no paid ad spend included."))
story.append(b("<b>Future phase:</b> Once intake/case-prep capacity is built, a marketing package can be scoped from live research — audit Sections 05–06 already flag the gaps."))

story.append(Paragraph("<b>Automation ROI Framing:</b>", S["subsection"]))
story.append(b("<b>Time recovered:</b> Automating probate steps and after-hours coverage removes recurring manual work. No hours/dollar figure was given — quantify with Hector during onboarding, not upfront."))
story.append(Paragraph("<i>No revenue figures were shared. Build any dollar ROI with Hector post-kickoff.</i>", S["disclaimer"]))

story.append(Paragraph("<b>Why Level 1, Not Level 2:</b>", S["subsection"]))
story.append(b("Transcript-quoted $3,797/mo for one automation matches L1's stand-alone price exactly."))
story.append(b("Owner is \"numb to tech\" and wants done-with-you leadership — L1's profile, not L2's larger scope."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We already got burned by a $50k proposal for stuff we were already doing."', S["objection_q"]))
story.append(Paragraph("Scoped to the exact automations Hector named — probate steps, after-hours coverage, intake-to-portal — at $3,297/mo, close to the $3,797/mo he was already quoted.", S["objection_a"]))

story.append(Paragraph('"Ben needs to see it work before we spend more."', S["objection_q"]))
story.append(Paragraph("Phase 1 targets the highest-friction automation first, so there's a measurable time-savings number to show Ben before any Phase 2 ask.", S["objection_a"]))

story.append(Paragraph('"Don\'t we also need help with marketing?"', S["objection_q"]))
story.append(Paragraph("Real and documented (Sections 05–06) — but it's Phase 3. Fixing intake/case-prep capacity first means the firm can handle the volume marketing would generate.", S["objection_a"]))

story.append(Paragraph('"We don\'t have anyone in-house who understands AI tools."', S["objection_q"]))
story.append(Paragraph("That's what the Fractional CTO role solves — Hector said he doesn't want to manage this himself, exactly the Level 1 profile.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Legal AI Workforce — Fractional CTO Level 1</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Dedicated Fractional CTO; probate + after-hours + intake automation.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Law Firm AI Foundation Sprint (optional, one-time)</b>", S["price_main"]),
     Paragraph("$14,997 one-time", S["price_main"])],
    [Paragraph("Full build-out of Phase 1 automations; optional, not required to start.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$0/mo — not included", S["price_main"])],
    [Paragraph("Automation-only engagement; marketing scoped separately in Phase 3.", S["price_detail"]),
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
    "Total: $3,297/mo recurring (+ optional $14,997 one-time Foundation Sprint)  |  Save $500/mo by bundling  |  No ad spend this round — automation-only engagement",
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
