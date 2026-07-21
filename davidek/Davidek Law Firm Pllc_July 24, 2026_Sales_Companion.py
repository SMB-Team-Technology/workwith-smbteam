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

OUTPUT_PATH = "davidek/Davidek Law Firm Pllc_July 24, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Davidek Law Firm Pllc", S["title"]))
story.append(Paragraph("Sales Companion  |  July 24, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Dirk Davidek", S["snap_value"]),
     Paragraph("$2.7M", S["snap_value"]),
     Paragraph("3 of 5 attys", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("~80%", S["snap_value"]),
     Paragraph("New Braunfels, TX", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: ENTERPRISE VALUE (inferred — confirm on call)", S["section"]))
story.append(Paragraph("Dirk is not just chasing revenue — he's working with a fractional CFO and a time-tracking study toward $4M and a 20% margin, the profile of an owner building a firm to eventually sell.", S["subsection"]))

story.append(quote_block("lead gen is strong, with appointments booked into late August"))
story.append(Spacer(1, 1))
story.append(quote_block("Payroll costs exceed 50% of revenue (vs. a 25% goal), driving profit margins into the low single digits."))
story.append(Spacer(1, 1))
story.append(quote_block("85% estate planning; shifting to higher-net-worth clients while retaining the local market."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Hit $4M by end of 2027.</b> A stated revenue goal tied to a firm rebrand and Austin launch."))
story.append(bd("<b>Get payroll under control.</b> Bring payroll from 50%+ of revenue down to a 25-35% target."))
story.append(bd("<b>Hit a 20% profit margin.</b> A specific, stated number — not just \"more profit.\""))
story.append(bd("<b>Launch into Austin cleanly.</b> A January 2027 rebrand and market expansion, not a side project."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Two open attorney seats.</b> Staffed at 3 of 5 for over a year — a direct cap on case capacity."))
story.append(b("<b>Payroll already over 50% of revenue.</b> Well past the 25% target, with margins in the low single digits."))
story.append(b("<b>Ad spend he can't see into.</b> An outside agency manages all paid campaigns with no in-house visibility."))
story.append(b("<b>A live NAP problem.</b> Homepage lists (830) 515-5854; the Contact page lists (830) 217-1544."))
story.append(b("<b>Zero Austin digital presence.</b> No geo-pages exist yet for the planned 2027 launch market."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Replaces the agency's black-box ad management with visibility and reporting Dirk doesn't have today."))
story.append(bd("Protects and extends the organic advantage already built against J.M. Dickerson and Carroll Law Group."))
story.append(bd("Builds the Austin digital foundation before the January 2027 rebrand launches."))

story.append(Paragraph("<b>Full Service Marketing — Dominate  |  $10,497/mo bundled</b>", S["subsection"]))
story.append(b("Revenue of $2.7M places the firm in the $2M-$3M Dominate tier per the standard pricing table."))
story.append(b("Firm currently pays an outside agency for ad management — Dominate replaces that spend with in-house visibility."))
story.append(b("No geo-pages exist for the Austin expansion — Dominate tier includes full website and landing page build."))
story.append(b("Live NAP inconsistency (two different phone numbers) needs to be resolved as part of the website work."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts Dirk in a peer group of law firm owners solving the same staffing and margin problems."))
story.append(bd("Builds the accountability structure that turns the CFO's time-tracking study into an executed plan."))
story.append(bd("Adds a leadership layer the firm doesn't yet have beyond the newly-engaged fractional CFO."))

story.append(Paragraph("<b>Master's Circle  |  $4,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $2.7M and 5 attorney seats meet the $1M+ / 5+ team threshold for Master's Circle."))
story.append(b("CAUTION: team is currently staffed at only 3 of 5 seats with no dedicated ops/intake staff confirmed in the transcript — confirm ops capacity with Dirk before finalizing."))
story.append(b("Fractional CFO already engaged — Master's Circle coaching complements that work operationally."))
story.append(b("$4M revenue goal and 20% margin target require accountability structure, not just financial visibility."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Davidek — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Dirk visibility into paid lead performance he doesn't have with the current agency."))
story.append(bd("Builds a scalable ad engine ahead of the Austin launch instead of starting cold in 2027."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — Google Search only, the Estate Planning channel minimum."))
story.append(b("<b>Aggressive:</b> $14,000/mo — full spread across Google Search, LSA, Meta Retargeting, and Meta Cold."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~17 cases x $2.25K = ~$39K/mo vs. $3.5K spend = ~11.1x return."))
story.append(b("<b>Aggressive:</b> ~168 cases x $2.25K = ~$378K/mo vs. $14K spend = ~27x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Case value uses the Estate Planning default ($1.5K-$3K) — not stated in the transcript. The 80% close rate reflects current warm-lead intake performance, not a validated cold-ad-lead conversion rate — sanity-check the aggressive scenario with Dirk before presenting it.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Estate Planning Google Search minimum = $3,500."))
story.append(b("<b>Aggressive:</b> $3,500 each across Google Search, LSA, Meta Retargeting, Meta Cold = $14,000."))
story.append(b("Total spend at aggressive: $29,097/mo (bundled + ad spend) = 12.9% of $2.7M revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We already pay an agency for ads — why switch?"', S["objection_q"]))
story.append(Paragraph("No independent visibility into the current agency's performance could be confirmed this pass. Dominate replaces that black box with monthly reporting and moves toward the AI-driven cost reduction Dirk raised on the call.", S["objection_a"]))

story.append(Paragraph('"Payroll is already eating our margin — can we afford another line item?"', S["objection_q"]))
story.append(Paragraph("At $15,097/mo bundled, total investment plus even the aggressive ad spend is 12.9% of monthly revenue — under the 35% cap — and it directly targets the marketing visibility and coaching accountability needed to hit the stated 20% margin goal.", S["objection_a"]))

story.append(Paragraph('"We\'re not fully staffed — is now the right time to grow marketing?"', S["objection_q"]))
story.append(Paragraph("Appointments are already booked into late August — demand isn't the constraint. Fixing intake and marketing visibility protects revenue from leads already being generated while the attorney gap closes.", S["objection_a"]))

story.append(Paragraph('"We\'re planning Austin for 2027 — should we wait to invest?"', S["objection_q"]))
story.append(Paragraph("Building geo-landing pages and SEO now means Austin launches with digital infrastructure already in place instead of starting from zero in January 2027.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Dominate</b>", S["price_main"]),
     Paragraph("$10,497/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, website/geo-page management — replaces the agency.", S["price_detail"]),
     Paragraph("<strike>$12,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle</b>", S["price_main"]),
     Paragraph("$4,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, masterminds, quarterly workshops, annual in-person event.", S["price_detail"]),
     Paragraph("<strike>$4,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,500–$14,000/mo", S["price_main"])],
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
    "Total: $15,097/mo + $3,500–$14,000 ad spend  |  Save $2,397/mo by bundling  |  8.3%–12.9% of revenue (under 35% cap)",
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
