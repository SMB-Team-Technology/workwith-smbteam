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

OUTPUT_PATH = "the-finn/The Finn Law Firm_July 27, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("The Finn Law Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  July 27, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Larry Finn", S["snap_value"]),
     Paragraph("$1M+", S["snap_value"]),
     Paragraph("Solo (1)", S["snap_value"]),
     Paragraph("3 — Solo", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Chicago, IL", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: STABILITY", S["section"]))
story.append(Paragraph("Larry wants to automate the firm's workflows — starting with the pre-intake bottleneck — to stabilize revenue before expanding the team.", S["subsection"]))

story.append(quote_block("Automate workflows to stabilize revenue and enable expansion, starting with the bottlenecked pre-intake evaluation process."))
story.append(Spacer(1, 1))
story.append(quote_block("High-value ($400k+), complex cases (med mal, nursing home abuse) create significant cash-flow volatility."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable revenue.</b> Stabilize cash flow instead of riding the volatility of slow-resolving, high-value cases."))
story.append(bd("<b>A pre-intake process that runs without him.</b> Named directly as the firm's top bottleneck."))
story.append(bd("<b>Fix systems before hiring.</b> Larry wants workflows and tech solid first, then expand the team."))
story.append(bd("<b>Time back for the cases that matter.</b> Less time spent personally triaging every lead."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Ads paused 6 months.</b> Google Ads — the firm's most direct lead channel — went dark and never restarted."))
story.append(b("<b>Zero organic visibility.</b> Did not appear in any of 9 local-visibility searches across all 3 practice areas."))
story.append(b("<b>No intake system.</b> Every case is evaluated personally by Larry — no delegation, no tracking."))
story.append(b("<b>No team.</b> No additional attorneys or staff to absorb any operational load."))
story.append(b("<b>Website mid-rebuild.</b> Outside $6K/mo agency rebuilding the site with no active SEO/content plan running alongside it."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns a paused, invisible lead system back into an active one across all three of his highest-value practice areas."))
story.append(bd("Rebuilds the local SEO visibility that Malman Law, Levin & Perconti, and Rosenfeld currently own outright."))
story.append(bd("Puts high-value abuse and neglect cases in front of prospects across Google, LSA, and Meta at once."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $7,497/mo bundled</b>", S["subsection"]))
story.append(b("Revenue is $1M–$2M, placing the firm squarely in the Growth tier."))
story.append(b("Ads were paused for lead volume, not poor performance — a faster, lower-risk relaunch than starting cold."))
story.append(b("Zero organic visibility across 3 practice areas rules out an ads-only add-on; full-service coverage is needed."))
story.append(b("Multiple practice areas rule out the Essentials tier regardless of revenue."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Larry direct guidance on automating the pre-intake bottleneck he named as the firm's top priority."))
story.append(bd("Builds the exact operational sequencing he already wants — fix workflows before hiring."))
story.append(bd("Creates a support structure so decisions no longer all depend on Larry alone."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue is $1M+ with a team under 5 — qualifies for Elite Coach Plus, not Master's Circle (requires 5+ team)."))
story.append(b("No dedicated ops, marketing, or intake staff — Master's Circle explicitly requires this and is not eligible."))
story.append(b("Firm's own stated plan to fix workflows before hiring matches Elite Coach Plus's operational focus."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("The Finn Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns the firm's own $400K+ case value into a predictable pipeline instead of one dependent on referrals alone."))
story.append(bd("Restarts a paused system with existing account history — lower risk than launching cold."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000/mo — minimum viable spend across recommended channels."))
story.append(b("<b>Aggressive:</b> $12,000/mo — full budget to hit growth goals."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~1 case x $400K = ~$400K/mo vs. $3K spend = ~133x return."))
story.append(b("<b>Aggressive:</b> ~4 cases x $400K = ~$1.6M/mo vs. $12K spend = ~133x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Case value reflects the transcript-stated $400K+ floor; actual monthly cash timing will vary given the firm's own long case-resolution cycles.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Absolute $3,000/mo floor applied — practice areas (med mal, nursing home abuse, sexual abuse) fall outside the standard PPC table's named categories."))
story.append(b("<b>Aggressive:</b> Scoped to $12,000/mo, within the Growth tier's $50,000 ad spend cap and the firm's stated cash-flow volatility."))
story.append(b("Total spend at aggressive: $22,697/mo (package + ad spend) = ~27.2% of monthly revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We tried digital marketing before and it was inconsistent."', S["objection_q"]))
story.append(Paragraph("Ads were paused for sufficient lead volume, not poor performance — relaunching starts from existing account history, and pairs with local SEO, LSA, and Meta to fix the inconsistency referrals alone never solved.", S["objection_a"]))

story.append(Paragraph('"I don’t have staff to manage all of this."', S["objection_q"]))
story.append(Paragraph("That is exactly why Elite Coach Plus — not a team-based Master's Circle tier — is the recommendation: it is built for solo firms fixing workflows before hiring, matching Larry's own stated sequencing.", S["objection_a"]))

story.append(Paragraph('"My cash flow is already unpredictable — can I afford this?"', S["objection_q"]))
story.append(Paragraph("At the aggressive ad spend level, total investment is ~27% of monthly revenue — under the 35% cap — while even a single $400K+ case covers the full monthly investment many times over.", S["objection_a"]))

story.append(Paragraph('"The website is already being rebuilt — isn’t that enough?"', S["objection_q"]))
story.append(Paragraph("The rebuild alone will not fix the 11-month-stale blog or the missing SEO and ad presence — Full Service Marketing pairs with the rebuild so the new site launches with an active lead system behind it.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$7,497/mo", S["price_main"])],
    [Paragraph("Google Ads, Local SEO, LSA, and Meta across all 3 practice areas.", S["price_detail"]),
     Paragraph("<strike>$8,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching focused on workflow and intake automation.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
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
    "Total: $10,697/mo + $3,000–$12,000 ad spend  |  Save $1,797/mo by bundling  |  16.4%–27.2% of revenue (under 35% cap)",
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
