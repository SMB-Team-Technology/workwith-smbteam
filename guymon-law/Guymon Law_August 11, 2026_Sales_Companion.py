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

OUTPUT_PATH = "guymon-law/Guymon Law_August 11, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Guymon Law", S["title"]))
story.append(Paragraph("Sales Companion  |  August 11, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Amber L. Guymon", S["snap_value"]),
     Paragraph("~$570K (est.)", S["snap_value"]),
     Paragraph("4 attys + LP", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Chandler & Scottsdale, AZ", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: STAFF CAPACITY &amp; PAY", S["section"]))
story.append(Paragraph("Amber wants AI to increase her team's capacity so she can pay them more — without hiring anyone new.", S["subsection"]))

story.append(quote_block("use AI to increase staff capacity and pay raises, avoiding new hires"))
story.append(Spacer(1, 1))
story.append(quote_block("27 of 39 steps in a probate case were automated for one client"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>More capacity, not more headcount.</b> Get the current team doing more without hiring."))
story.append(bd("<b>Pay raises for her people.</b> Convert freed-up capacity directly into staff pay increases."))
story.append(bd("<b>Off her own plate.</b> Hand off sensitive tasks like performance reviews and tutorial videos to AI."))
story.append(bd("<b>A real system, not a hobby.</b> Scale beyond her own ad hoc Claude use into a firm-wide build."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Fragmented intake.</b> Intake and conflict-checking span 5+ disconnected systems."))
story.append(b("<b>Ad hoc AI use.</b> Claude is used personally today, not deployed as a firm-wide system."))
story.append(b("<b>No stated financial target.</b> No revenue goal or close rate exists to plan capacity gains against."))
story.append(b("<b>Thin local visibility.</b> Review/search footprint trails Scottsdale competitors — not why she called, but real."))

story.append(thin_rule())

# ── Why This AI Package (Primary — matches what the call was about) ──
story.append(Paragraph("Why This AI Package (Primary — Matches the Call)", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives her existing team the capacity to do more work without adding headcount."))
story.append(bd("Frees Amber from personally handling sensitive, repeatable tasks."))
story.append(bd("Turns individual, ad hoc AI use into a firm-wide system a dedicated Fractional CTO builds and runs."))

story.append(Paragraph("<b>Legal AI Workforce — Fractional CTO Level 1  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Revenue (~$570K est.) clears the $500K LAW minimum and fits the $500K–$1.5M L1 band."))
story.append(b("Firm has real support staff (4 attorneys, 1 LP, 16 total) — meets the LAW staffing minimum."))
story.append(b("Owner already uses Claude personally — strong AI-readiness, no adoption resistance to overcome."))
story.append(b("L1's dedicated Fractional CTO fits the call's emphasis on custom builds better than DIY AI Essentials."))
story.append(b("Staff outside Amber are hesitant to use AI themselves, per the call — L1 delivers automation without needing staff buy-in."))

story.append(thin_rule())

# ── Why This Marketing Package (Secondary opportunity, not the lead) ──
story.append(Paragraph("Why This Marketing Package (Secondary — Not the Lead)", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Closes the visibility gap with Arizona Law Group, Owens &amp; Perkins, and Genesis Family Law."))
story.append(bd("Builds a review and local SEO footprint that matches the credibility Amber has already earned."))
story.append(bd("Not what she called about — raise only as a second opportunity, after the AI conversation lands."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("Guymon Law did not surface in any of 3 local search tests run this session."))
story.append(b("Two office locations disqualify the lower-cost Essentials tier — Starter is the correct floor."))
story.append(b("Review footprint (Yelp 14, Avvo 13) trails named competitors' 190–400+ reviews by an order of magnitude."))
story.append(b("Do not lead with this — the transcript shows no marketing ask; position as optional add-on only."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Guymon Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend (Applies Only If Marketing Is Added)", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Converts local search visibility into signed cases, not just impressions."))
story.append(bd("Lets Guymon Law compete for the same searches Arizona Law Group and Owens & Perkins are winning."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — Google PPC only, the minimum viable single-channel spend for Family Law."))
story.append(b("<b>Aggressive:</b> $8,300/mo — capped below the raw 20%-rule figure ($19,700/mo) to stay under the 35% spend cap."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~4 cases x $4K = ~$17.5K/mo vs. $3.5K spend = ~5.0x return."))
story.append(b("<b>Aggressive:</b> ~14 cases x $4K = ~$57.2K/mo vs. $8.3K spend = ~6.9x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Uses default 15% close rate and default Family Law case value ($4K) since neither was stated on the call.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Family Law Google PPC minimum = $3,500 (firm has zero confirmed ad presence today)."))
story.append(b("<b>Aggressive:</b> $1.14M (2x current revenue, no goal stated) x 20% / 12 = $19,000. Tier 2 Phoenix multiplier (1.3x) = $24,700. Minus $4,997 marketing fee = $19,703 raw figure."))
story.append(b("Raw aggressive figure would put total spend at 57.5% of revenue — over the 35% cap — so ad spend was reduced to $8,300/mo, keeping total investment at ~34.9% of current monthly revenue."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"We came here to talk about AI, not marketing."', S["objection_q"]))
story.append(Paragraph("The AI package (Fractional CTO L1) is the lead recommendation and matches exactly what was discussed. Marketing is a secondary, optional opportunity from our own research — not a requirement.", S["objection_a"]))

story.append(Paragraph('"We don\'t know our exact revenue number."', S["objection_q"]))
story.append(Paragraph("The ~$570K estimate comes directly from the internal trigger record's monthly range ($15K–$80K), annualized — not a guess — and it puts the firm in the $500K–$1.5M band for Fractional CTO Level 1.", S["objection_a"]))

story.append(Paragraph('"We\'re already using Claude ourselves — why do we need this?"', S["objection_q"]))
story.append(Paragraph("That's exactly why L1 fits — it turns Amber's own ad hoc AI use into a structured, firm-wide system led by a dedicated Fractional CTO, instead of staying limited to what she personally has time to try.", S["objection_a"]))

story.append(Paragraph('"Is this going to require hiring more people to manage?"', S["objection_q"]))
story.append(Paragraph("No — the entire premise, per the call, is increasing capacity on the current team (4 attorneys, 1 LP, support staff) without adding headcount.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Legal AI Workforce — Fractional CTO L1</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Dedicated Fractional CTO leads AI rollout end-to-end.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("Closes the review/visibility gap identified in research (secondary).", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,500–$8,300/mo", S["price_main"])],
    [Paragraph("Goes to Google and LSA — not to SMB Team.", S["price_detail"]),
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
    "Total: $8,294/mo + $3,500–$8,300 ad spend  |  Save $1,200/mo by bundling  |  24.8%–34.9% of revenue (under 35% cap)",
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
