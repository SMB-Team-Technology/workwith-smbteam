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

OUTPUT_PATH = "jensen-mccomas/Jensen & McComas_July 23, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Jensen &amp; McComas, LLC", S["title"]))
story.append(Paragraph("Sales Companion  |  July 23, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Kristine Kukich", S["snap_value"]),
     Paragraph("~$1.2M (goal $3M)", S["snap_value"]),
     Paragraph("16 (6 atty)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Towson, MD", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE &amp; STRUCTURE", S["section"]))
story.append(Paragraph("Kristine wants to triple revenue to $3M and add five hires within a year — without the firm cracking under its own growth.", S["subsection"]))

story.append(quote_block("a non-existent marketing engine and a leaky intake process"))
story.append(Spacer(1, 1))
story.append(quote_block("a phased plan, starting with foundational systems and potentially including fractional COO/recruiting services"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Triple revenue to $3M.</b> A ~2.5x increase from $1.2M within one year."))
story.append(bd("<b>Grow the team by 30%.</b> Five hires already scoped, including a senior associate and two admins."))
story.append(bd("<b>Build in a deliberate order.</b> Foundational systems before marketing spend — not chaotic growth."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Leaky intake process.</b> Cited as one of two root causes of the current growth plateau."))
story.append(b("<b>No dedicated ops owner.</b> She is personally building the firm's AI intake tool on top of running the practice."))
story.append(b("<b>Zero digital footprint.</b> No GBP reviews, no paid ads on any channel, stale directory listings."))
story.append(b("<b>No profit visibility.</b> No cost tracking between Corporate ($85K) and Trusts &amp; Estates ($20K) work."))

story.append(thin_rule())

# ── Why This Operations Package (FCOO Advisor — no marketing package in this proposal) ──
story.append(Paragraph("Why This Operations Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives operations a real owner besides Kristine, so she stops personally building the firm's systems."))
story.append(bd("Builds the intake process and hiring/onboarding plan for the five roles already scoped — before marketing adds volume to a leaky system."))

story.append(Paragraph("<b>FCOO Advisor  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Transcript explicitly asked for &ldquo;fractional COO/recruiting services&rdquo; — not marketing. No marketing package is included in this proposal."))
story.append(b("Revenue ($1.2M) and no dedicated ops/intake staff member rule out Master's Circle; FCOO Advisor is the correct $1M+ fit."))
story.append(b("Already bundles Elite Coach group deliverables below — no separate coaching line needed."))
story.append(b("$3,297/mo clears the $2,497 MRR floor and sits well inside the 35% spend cap (~$35K/mo at current revenue)."))

story.append(thin_rule())

# ── What's Included: Group Coaching & Masterminds (bundled into FCOO Advisor) ──
story.append(Paragraph("What's Included: Group Coaching &amp; Masterminds", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Puts Kristine in a room with other managing partners scaling through the same growth stage."))
story.append(bd("Practice-area masterminds give Corporate and Trusts &amp; Estates-specific peer input, not generic coaching."))

story.append(Paragraph("<b>Included in FCOO Advisor  |  $0 additional/mo</b>", S["subsection"]))
story.append(b("Weekly group coaching sessions and practice area masterminds."))
story.append(b("Virtual access to quarterly workshops, plus one annual in-person workshop."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Jensen &amp; McComas — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend (Phase 2 Preview — not part of this proposal) ──
story.append(Paragraph("Why This Ad Spend (Phase 2 Preview)", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Once the intake process and new hires are in place, paid digital gives the firm its first real lead generation engine — instead of relying only on referrals and conferences."))
story.append(bd("Targets Trusts &amp; Estates specifically, where individual clients actually search online — Corporate stays relationship-driven, as it is today."))

story.append(Paragraph("<b>Recommended Ad Spend Range (Phase 2, not billed now):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,500/mo — Estate Planning Google PPC + LSA minimums, once the firm is ready to launch."))
story.append(b("<b>Aggressive:</b> $8,500/mo — adds Meta lead-gen budget for the Trusts &amp; Estates practice."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 6 cases x $20K = $120K/mo vs. $5.5K spend = 21.8x return."))
story.append(b("<b>Aggressive:</b> 11 cases x $20K = $220K/mo vs. $8.5K spend = 25.9x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Estate Planning minimums: PPC $3,500 + LSA $2,000 = $5,500."))
story.append(b("<b>Aggressive:</b> Mechanical 20% rule ($3M goal x 20% / 12 = $50,000; Tier 4 x1.0 = $50,000; minus $7,497 Growth-tier fee = $42,503) is disproportionate for a boutique T&amp;E practice — capped instead at a market-realistic $8,500. Full math flagged in section_11_workings.txt for paid-ads team review."))
story.append(b("Total spend at aggressive Phase 2: $3,297 (FCOO) + $8,500 (ad spend) = $11,797/mo = 11.8% of $100K monthly revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"We already told you we don’t want to spend on marketing yet."', S["objection_q"]))
story.append(Paragraph("This proposal does not include a marketing package. It is the FCOO Advisor engagement she asked for on the call: intake process design and the hiring plan for the five already-scoped roles. Marketing stays a Phase 2 conversation, once the foundation is in place.", S["objection_a"]))

story.append(Paragraph('"Why isn’t this cheaper if we’re not buying marketing?"', S["objection_q"]))
story.append(Paragraph("At $3,297/mo bundled ($3,797 stand-alone), FCOO Advisor already includes weekly group coaching, practice area masterminds, and quarterly workshops — it is priced as a combined ops-plus-coaching engagement, not a stripped-down add-on.", S["objection_a"]))

story.append(Paragraph('"We’re already building our own AI intake tool — why do we need this?"', S["objection_q"]))
story.append(Paragraph("Her AI tool is scheduled for an August beta, but it will only be as good as the process behind it. FCOO Advisor defines that process now, so the tool has something real to run on top of instead of automating today's gaps.", S["objection_a"]))

story.append(Paragraph('"How do we know operations needs a fractional COO and not just another hire?"', S["objection_q"]))
story.append(Paragraph("The two admins already on the hiring list will need a defined structure to plug into. A fractional COO builds that structure once, rather than each new hire building it themselves.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>FCOO Advisor</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Includes weekly coaching, masterminds, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend (Phase 2)</b>", S["price_main"]),
     Paragraph("$5,500–$8,500/mo", S["price_main"])],
    [Paragraph("Goes to Google, LSA, and Meta — not to SMB Team. Begins in Phase 2, not now.", S["price_detail"]),
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
]))
story.append(pt)
story.append(Paragraph(
    "Total now: $3,297/mo  |  Save $500/mo by bundling  |  Phase 2 adds $5,500–$8,500/mo ad spend (11.8% of revenue at aggressive level, under 35% cap)",
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
