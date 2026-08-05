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

OUTPUT_PATH = "dhanani-law/Dhanani_Law_August_6_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Dhanani Law Firm, LLC", S["title"]))
story.append(Paragraph("Sales Companion  |  August 6, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Rahim Dhanani", S["snap_value"]),
     Paragraph("~$150K-$200K/yr", S["snap_value"]),
     Paragraph("Solo (1)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Atlanta, GA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM / SELLABLE FIRM", S["section"]))
story.append(Paragraph("Rahim wants a systematized firm that runs without him, so he can work on the business as CEO — not just survive as its only attorney.", S["subsection"]))

story.append(quote_block("Build a systematized, sellable firm that runs without his constant presence, enabling him to work on the business as a true CEO."))
story.append(Spacer(1, 1))
story.append(quote_block("Gain personal freedom, reduce stress, and build a lasting legacy by helping clients start new lives."))
story.append(Spacer(1, 1))
story.append(quote_block("Open to SMB Team's $2,500/mo minimum package (12-month commitment)."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Step back from the day-to-day</b> so the firm runs without his constant presence."))
story.append(bd("<b>Break the chicken-and-egg cycle</b> — a system to hire and delegate, not just more leads."))
story.append(bd("<b>Build something sellable,</b> not just a practice tied to his own involvement."))
story.append(bd("<b>Hit $500K gross / $250K net,</b> stretch target $1.2M+ within the year."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Sole bottleneck.</b> Every case and intake call runs through him personally."))
story.append(b("<b>Past freelance hires failed</b> on quality — hesitant to try again."))
story.append(b("<b>No consistent lead channel.</b> Referral-only; a past PPC campaign failed."))
story.append(b("<b>No financial visibility</b> beyond top-line revenue."))
story.append(b("<b>Under $250K revenue</b> — confirm he can cover 4 months of service before signing."))

story.append(thin_rule())

# ── Why No Marketing Package (Phase 1) ──
story.append(Paragraph("Why No Marketing Package in Phase 1", S["section"]))

story.append(Paragraph("<b>What this protects for him:</b>", S["subsection"]))
story.append(bd("Prevents pushing lead volume at a solo attorney with no team to handle it."))
story.append(bd("Keeps monthly investment inside the 35% of revenue cap, instead of overshooting before ad spend starts."))

story.append(Paragraph("<b>Scoping rationale — departure from the revenue-based recommendation:</b>", S["subsection"]))
story.append(b("35% cap at ~$15K/mo revenue is ~$5,250/mo. Starter + Elite Coach bundled = $7,597/mo, over by $2,300+ before ad spend."))
story.append(b("Essentials tier unavailable — multiple practice areas (family + business immigration) require single-practice-area Essentials."))
story.append(b("Rahim's $2,500/mo comfort level assumed a bundle partner. Sold alone, Elite Coach is $3,497/mo — flag this gap for Jacob."))
story.append(b("Marketing deferred to Phase 2 — documented as intentional, not an oversight."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives him a real hiring/training/delegation system, not a repeat of the failed freelance hire."))
story.append(bd("Builds the team capacity that must exist before more leads would help him."))

story.append(Paragraph("<b>Elite Coach  |  $3,497/mo</b>", S["subsection"]))
story.append(b("Stand-alone rate. Bundled $2,600/mo only applies with a second package — see objection below."))
story.append(b("Includes weekly coaching, masterminds, quarterly workshops, one annual in-person workshop."))
story.append(b("Sole Phase 1 recommendation — fits the call's explicit coaching/systems focus."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Dhanani Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend (Phase 2 Target) ──
story.append(Paragraph("Why This Ad Spend (Phase 2 Target, Not Phase 1)", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns the $500K-$1.2M revenue goal into a concrete media plan once the team is ready."))
story.append(bd("Fixes the past PPC failure right this time, with a landing page and real keyword targeting."))

story.append(Paragraph("<b>Recommended Ad Spend Range (Phase 2):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000/mo — Google Search only, Immigration category minimum."))
story.append(b("<b>Aggressive:</b> $12,000/mo — 20% rule on the $500K goal, Tier 1 Atlanta multiplier."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~3-4 cases x $4.5K avg = ~$13.5K-$18K/mo vs. $3K spend = ~5-6x return."))
story.append(b("<b>Aggressive:</b> ~24-25 cases x $4.5K avg = ~$108K-$112.5K/mo vs. $12K spend = ~9x return."))
story.append(Paragraph("<i>Estimates use the Immigration default case value ($3K-$6K). Not guaranteed.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I thought we were going to start running ads right away."', S["objection_q"]))
story.append(Paragraph("More leads without a team just recreates the bottleneck you described. Elite Coach builds the team first — marketing launches in Phase 2.", S["objection_a"]))

story.append(Paragraph('"You said $2,500 a month — this is $3,497."', S["objection_q"]))
story.append(Paragraph("$2,500 assumed a bundle with marketing. Sold alone in Phase 1, Elite Coach is priced at its standard $3,497/mo rate. Bundling returns in Phase 2.", S["objection_a"]))

story.append(Paragraph('"Why not just do the $4,997/mo Starter marketing package now?"', S["objection_q"]))
story.append(Paragraph("At your revenue, Starter alone is already ~33% of monthly revenue — no room left for ad spend under the 35% cap.", S["objection_a"]))

story.append(Paragraph('"What about the AI Workforce Pro tool we talked about?"', S["objection_q"]))
story.append(Paragraph("A great fit down the road — it needs $500K+ revenue and 1-2 support staff. Elite Coach gets you there; revisit in Phase 3.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$3,497/mo", S["price_main"])],
    [Paragraph("Weekly coaching on systems, hiring, and delegation. Stand-alone rate — no bundle partner yet.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>Marketing</b>", S["price_main"]),
     Paragraph("Deferred to Phase 2", S["price_main"])],
    [Paragraph("Launches once coaching builds a team. Bundling then drops Elite Coach to $2,600/mo.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend (Phase 2)</b>", S["price_main"]),
     Paragraph("$3,000–$12,000/mo", S["price_main"])],
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
    "Total Phase 1: $3,497/mo (stand-alone, no bundle partner yet)  |  Phase 2 ad spend adds $3,000-$12,000/mo on top",
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
