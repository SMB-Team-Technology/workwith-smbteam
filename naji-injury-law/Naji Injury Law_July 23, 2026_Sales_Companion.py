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

OUTPUT_PATH = "naji-injury-law/Naji Injury Law_July 23, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Naji Injury Law, LLC", S["title"]))
story.append(Paragraph("Sales Companion  |  July 23, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Jamil Naji", S["snap_value"]),
     Paragraph("~$1M now; $3M/$7M goals*", S["snap_value"]),
     Paragraph("6", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("88%**", S["snap_value"]),
     Paragraph("Clayton, MO", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.7*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Paragraph(
    "*Revenue: transcript states ~$1M current, $3M/$7M as goals (HubSpot showed $3M+ — confirm live). "
    "**Close rate is qualified-lead intake conversion, not case-settlement.", S["disclaimer"]))
story.append(Spacer(1, 3))

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: SCALE THROUGH SYSTEMS", S["section"]))
story.append(Paragraph("Stop renting growth from a failing lead vendor; build a firm on owned systems — scale to $3M, then $7M, without more of his own hours.", S["subsection"]))

story.append(quote_block("On track for $1M in fees. The goal is more return on hours, not fewer hours."))
story.append(Spacer(1, 1))
story.append(quote_block("High conversion rate (~88%) on qualified leads."))
story.append(Spacer(1, 1))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Own the pipeline, not rent it.</b> Stop paying a vendor for leads that build someone else's brand."))
story.append(bd("<b>More return on hours.</b> Scale revenue without adding to his workload."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Vendor has gone cold</b> — zero conversions since July 3."))
story.append(b("<b>Invisible in local search</b> vs. Brown & Crouppen, Schultz & Myers, Cofman Townsley."))
story.append(b("<b>No owned SEO/ad presence</b> — prior SEO and PPC/LSA tests both underperformed and were shut down."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Replaces the failing vendor with a lead engine Naji Injury Law owns outright."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $7,497/mo bundled</b>", S["subsection"]))
story.append(b("~$1M revenue qualifies for Growth, not Platinum — HubSpot's $3M+ reflects the goal, not current revenue; confirm live."))
story.append(b("$50,000/mo ad spend cap at this tier covers both scenarios below."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the delegation habits Jamil needs to move decisions off his own desk."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Team of 6 clears headcount for Master's Circle, but no dedicated ops/marketing/intake staff confirmed — verify live."))

story.append(thin_rule())

# ── Why This AI Automation Package ──
story.append(Paragraph("Why This AI Automation Package (Fractional CTO)", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Delivers exactly what he asked for — a dedicated CTO building custom automations into his existing Claude AI setup."))

story.append(Paragraph("<b>Fractional CTO — Level 1  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("~$1M revenue and 6 staff clear the LAW eligibility bar; firm already adopting AI on its own."))
story.append(b("Explicitly requested on this call alongside marketing — proposal must cover both."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Naji Injury Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Replaces ~60 rented leads/month that stopped converting with an owned pipeline feeding his 88%-converting intake team."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $15,000/mo — channel minimums across Google PPC, LSA, and Meta."))
story.append(b("<b>Aggressive:</b> $50,000/mo — Growth tier's ad spend cap, tied to the firm's stated $3M goal."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~5 cases x $6.5K = ~$32.5K/mo vs. $15K spend = ~2.2x return."))
story.append(b("<b>Aggressive:</b> ~20 cases x $6.5K = ~$130K/mo vs. $50K spend = ~2.6x return."))
story.append(Paragraph("<i>Estimates only; case value uses a PI-market default. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Cons.:</b> Accident/Injury (Gen.) mins: PPC $6,000 + LSA $2,000 + Meta $6,700 = $14,700 → $15,000."))
story.append(b("<b>Aggr.:</b> $3M goal x 20% ÷ 12 = $50,000 (Tier 4, 1.0x). Reverse math implies ~$100K but Growth tier caps at $50,000."))
story.append(b("At aggressive, total spend = 76.8% of CURRENT $1M revenue (exceeds 35% cap); 25.6% at the $3M goal — confirm framing before quoting."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We already pay for leads — why pay for marketing too?"', S["objection_q"]))
story.append(Paragraph("That vendor has zero conversions since July 3 — this replaces a failing rented pipeline with one you own.", S["objection_a"]))

story.append(Paragraph('"We tried SEO and PPC before and it didn\'t work."', S["objection_q"]))
story.append(Paragraph("Those were short, standalone tests (6-month SEO, 30-day PPC/LSA) — not a fully managed program across all channels.", S["objection_a"]))

story.append(Paragraph('"$50,000/mo in ad spend is a lot for a firm doing $1M today."', S["objection_q"]))
story.append(Paragraph("That's the aggressive ceiling tied to the firm's own $3M goal — the conservative plan starts at $15,000/mo.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$7,497/mo", S["price_main"])],
    [Paragraph("Replaces the failing third-party lead vendor.", S["price_detail"]),
     Paragraph("<strike>$8,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Builds delegation habits and profit visibility.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Fractional CTO — Level 1</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Custom AI automation, as explicitly requested on the call.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$15,000–$50,000/mo", S["price_main"])],
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
    ("LINEBELOW", (0,7), (-1,7), 0.5, RULE_GRAY),
]))
story.append(pt)
story.append(Paragraph(
    "Total: $13,994/mo + $15,000–$50,000 ad spend  |  Save $2,297/mo by bundling  |  "
    "34.8%–76.8% of current revenue (aggressive exceeds 35% cap — see note above)",
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
