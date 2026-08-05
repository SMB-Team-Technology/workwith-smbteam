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

OUTPUT_PATH = "calderaro-law-group/Calderaro Law Group_August 11, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Calderaro Law Group", S["title"]))
story.append(Paragraph("Sales Companion  |  August 11, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Renata Calderaro", S["snap_value"]),
     Paragraph("~$1M/yr (plateaued)", S["snap_value"]),
     Paragraph("14", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("20% (goal 30%)", S["snap_value"]),
     Paragraph("Miami, FL", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE", S["section"]))
story.append(Paragraph("Break a revenue plateau and fill 30 open case slots with predictable lead flow instead of unpredictable referrals, targeting $3.6M by 2027.", S["subsection"]))

# No word-for-word transcript quotes were captured in Pass 1 research notes for this
# call — omitting quote_block() rather than paraphrasing into a quote box.
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Break the plateau.</b> Predictable growth toward a stated $3.6M target by 2027."))
story.append(bd("<b>Fill open capacity.</b> 30 unused case slots (90 of 120 filled) a steady lead flow could fill."))
story.append(bd("<b>Stop relying on referrals alone.</b> A cancelled sub-$500/mo Instagram test is her only paid-marketing history."))
story.append(bd("<b>Convert more of what's already coming in.</b> Stated goal: raise close rate from 20% to 30%."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Zero paid-channel history.</b> No Google Ads, LSA, SEO, or PPC has ever been run."))
story.append(b("<b>No visible trust signal.</b> No attorney bio, no visible review footprint, despite a real 90-95% approval rate."))
story.append(b("<b>Results-based pricing requirement.</b> Tied to recent slow sales — lead with the guarantee."))
story.append(b("<b>No stated case-value figure.</b> ROI math uses a $4,500 default — confirm before the call."))
story.append(b("<b>NAP inconsistency.</b> Conflicting directory addresses/phones could raise legitimacy concerns overseas."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Replaces referral dependency with channels she controls — PPC, LSA, and local SEO for E2/EB5/L/O terms."))
story.append(bd("Builds the trust signal (attorney bio, reviews, NAP fix) an overseas buyer needs before wiring a retainer."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $7,497/mo bundled</b>", S["subsection"]))
story.append(b("Revenue (~$1M) places this firm in the $1M-$2M Growth tier, not Dominate — HubSpot's $1M-$3M CRM range overstated this."))
story.append(b("Growth tier caps ad spend at $50,000/mo, well above the $5,000/mo conservative starting point."))
story.append(b("Website rebuild not required (recent, 2025 build) — budget goes to channels and trust-signal fixes."))
story.append(b("Bundled saves $1,500/mo vs. the $8,997/mo stand-alone price."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives Renata peer accountability from firm owners scaling past a revenue plateau."))
story.append(bd("Turns her existing 14-person team into a structured growth operation, not just headcount."))

story.append(Paragraph("<b>Master's Circle  |  $4,600/mo bundled</b>", S["subsection"]))
story.append(b("Team size (14) and two dedicated intake staff meet the 5+ dedicated-staff threshold."))
story.append(b("Revenue (~$1M) does not meet the $2M+ floor for + FCOO Director — plain Master's Circle is correct."))
story.append(b("No dedicated ops staff mentioned, so FCOO Advisor was not added — revisit at Phase 2."))
story.append(b("Bundled saves $397/mo vs. the $4,997/mo stand-alone price."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Calderaro — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("The conservative $5,000/mo entry point alone projects a 9.0x return."))
story.append(bd("Scaling toward the $50,000/mo ceiling is the path to the volume $3.6M requires — paced to the team's real capacity."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,000/mo — Google PPC ($3,000 min) + LSA ($2,000 min)."))
story.append(b("<b>Aggressive:</b> $50,000/mo — Growth tier ceiling (Dominate not eligible at ~$1M revenue)."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 10 cases x $4.5K = $45K/mo vs. $5K spend = 9.0x return."))
story.append(b("<b>Aggressive:</b> 126 cases x $4.5K = $567K/mo vs. $50K spend = 11.3x return. Flag: exceeds the 30-slot capacity gap — pace with Phase 2, not month one."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Immigration minimums: PPC $3,000 + LSA $2,000 = $5,000."))
story.append(b("<b>Aggressive:</b> $3.6M x 20% / 12 = $60,000. Tier 2 (1.3x) x Spanish (1.33x) = $103,740, minus $7,497 fee = $96,243 — capped at $50,000."))
story.append(b("At aggressive: $50,000 + $12,097 fees = ~74.5% of revenue — above the 35% cap. Start conservative (~20.5%) and scale in phases."))

story.append(thin_rule())

# ── If She Pushes Back ──
# FILL: 2-4 objections anticipated from the transcript
# Each: red question (objection_q style) + gray response (objection_a style)
# Responses use specific data from the audit — competitor numbers, transcript quotes, etc.
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"Why not just start with ads and skip coaching?"', S["objection_q"]))
story.append(Paragraph("With 14 staff in place, Master's Circle turns that headcount into a growth operation — skipping it often means the firm can't absorb new leads.", S["objection_a"]))

story.append(Paragraph('"We need results before a bigger spend."', S["objection_q"]))
story.append(Paragraph("That's why we start at $5,000/mo — a projected 9x return on her own 20% close rate — before scaling toward $50,000/mo.", S["objection_a"]))

story.append(Paragraph('"Our website is only a year old — why touch it?"', S["objection_q"]))
story.append(Paragraph("The site is a solid, recent build. The fix is an attorney bio and directory address/phone corrections — not a redesign.", S["objection_a"]))

story.append(Paragraph('"We need this results-based given recent slow sales."', S["objection_q"]))
story.append(Paragraph("Renata explicitly required performance pricing — SMB Team's double-your-investment 12-month guarantee is built for this. Lead with it.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
# FILL: All pricing from the scoping calculation
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$7,497/mo", S["price_main"])],
    [Paragraph("Google PPC, LSA, local SEO, and Meta ads targeting business immigration terms.", S["price_detail"]),
     Paragraph("<strike>$8,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle</b>", S["price_main"]),
     Paragraph("$4,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, practice-area masterminds, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$4,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,000–$50,000/mo", S["price_main"])],
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
    "Total: $12,097/mo + $5,000–$50,000 ad spend  |  Save $1,897/mo by bundling  |  ~20.5% of revenue at conservative (aggressive exceeds 35% cap — scale in phases)",
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
