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

OUTPUT_PATH = "iridium-law/Iridium_Law_APC_August_11_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Iridium Law APC", S["title"]))
story.append(Paragraph("Sales Companion  |  August 11, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
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
    [Paragraph("Hadeel Abutouk", S["snap_value"]),
     Paragraph("~$390K (est.)", S["snap_value"]),
     Paragraph("2 (1 atty + 1 paralegal)", S["snap_value"]),
     Paragraph("Solo Practitioner", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Pleasant Hill, CA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM", S["section"]))
story.append(Paragraph("Hadeel wants a firm that runs without her personally carrying every case, so she can step back from being the workhorse and be present for her 13-year-old daughter.", S["subsection"]))

story.append(quote_block("a rollercoaster of revenue and stress"))
story.append(Spacer(1, 1))
story.append(quote_block("a well-oiled machine with predictable client flow"))
story.append(Spacer(1, 1))
story.append(quote_block("workhorse to owner/strategist"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable client flow.</b> An end to relying on word-of-mouth and discounted ARAG referrals."))
story.append(bd("<b>Owner, not workhorse.</b> Transition to strategist as the firm scales to 3 attorneys."))
story.append(bd("<b>Time with her daughter.</b> Presence for her 13-year-old, not just billable hours."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No verified GBP.</b> Co-work space hasn't approved address verification yet."))
story.append(b("<b>Zero paid marketing.</b> Everything today comes from referrals alone."))
story.append(b("<b>She is the only attorney.</b> Every case runs through her personally."))
story.append(b("<b>Fragmented directory footprint.</b> Her name still points to her prior SF firm in 3 cities."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Replaces discounted ARAG referrals with full-value clients found through her own local search presence."))
story.append(bd("Fixes the fragmented directory footprint currently sending prospects to her prior firm."))
story.append(bd("Gives her a paid channel that isn't dependent on who happens to refer someone this month."))

story.append(Paragraph("<b>Full Service Marketing Essentials  |  $3,497/mo bundled</b>", S["subsection"]))
story.append(b("Single practice area + single location qualifies for Essentials — Starter would over-scope a 6-month-old, ~$390K firm."))
story.append(b("GBP verification, directory NAP cleanup, and PPC + Meta Retargeting launch are all included at this tier."))
story.append(b("Ad spend cap for Essentials is $5,000/mo — matches the range recommended below."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Builds the accountability and delegation systems needed before she can hire her first associate."))
story.append(bd("Documents the intake and case-handling processes she currently carries entirely alone."))
story.append(bd("Keeps her moving toward the 3-attorney structure without losing momentum to day-to-day casework."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue estimate (~$390K) falls in the $250K–$400K band — Elite Coach, not Elite Coach Plus ($400K–$1M)."))
story.append(b("Team today is just Hadeel + 1 paralegal — no dedicated ops/marketing staff yet, so Master's Circle and FCOO tiers aren't eligible."))
story.append(b("FCOO Advisor is a Phase 2 roadmap add-on once revenue clears $500K."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Iridium Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Even the conservative end of this range is projected to clear her own stated target of 4–5 new clients/month."))
story.append(bd("Every dollar goes directly to Google and Meta — not to SMB Team — and stops the moment it isn't working."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $4,700/mo — PPC ($3,500) + Meta Retargeting ($1,200), the channel mix that fits inside the Essentials $5,000 ad spend cap."))
story.append(b("<b>Aggressive:</b> $5,000/mo — the max the Essentials tier supports. The $1.5M goal implies ~$29,000/mo under the 20% rule, but that's a Phase 2/4 tier-upgrade ask, not Phase 1 for a 2-person firm."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~44 leads x 15% close rate = ~6-7 cases x $37.5K avg case value = ~$225K/mo vs. $4.7K spend = ~48x return."))
story.append(b("<b>Aggressive:</b> ~56 leads x 15% close rate = ~8 cases x $37.5K avg case value = ~$300K/mo vs. $5K spend = ~60x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Family Law minimums: PPC $3,500 + Meta Retargeting $1,200 = $4,700 (LSA's $2,000 min would push PPC+LSA to $5,500, over the Essentials cap)."))
story.append(b("<b>Aggressive:</b> $1.5M goal x 20% / 12 = $25,000. Tier 2 (SF Bay Area, 1.3x) = $32,500. Minus $3,497 fee = ~$29,003 implied — capped at the Essentials tier's $5,000 max for this phase."))
story.append(b("Total spend at aggressive: $6,097 fees + $5,000 ad spend = $11,097/mo = ~34.1% of ~$32,500/mo estimated current revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"Why not the higher marketing tier if my goal is $1.5M?"', S["objection_q"]))
story.append(Paragraph("Her current revenue (~$390K est.) and 2-person team qualify for Essentials today. Phase 2 upgrades the tier once revenue crosses $500K and ad spend needs grow past the $5,000 Essentials cap — this avoids over-scoping a 6-month-old firm.", S["objection_a"]))

story.append(Paragraph('"Can we skip GBP and go straight to ads?"', S["objection_q"]))
story.append(Paragraph("LSA eligibility requires a verified GBP, and PPC/Meta traffic converts better once the directory and NAP fragmentation across Avvo, Martindale, Super Lawyers, and Lawyers.com is fixed — GBP verification is the first 30-day priority for exactly this reason.", S["objection_a"]))

story.append(Paragraph('"I don\'t have time to manage coaching on top of casework."', S["objection_q"]))
story.append(Paragraph("Elite Coach is built around a weekly accountability rhythm, not more work for Hadeel — its purpose is documenting the processes she currently carries alone so she can eventually hand them off.", S["objection_a"]))

story.append(Paragraph('"Is $6,097/month affordable at my revenue?"', S["objection_q"]))
story.append(Paragraph("At an estimated $32,500/mo in current revenue, $6,097 in fees plus up to $5,000 in ad spend totals ~34% of revenue — under the 35% cap SMB Team never exceeds.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Essentials</b>", S["price_main"]),
     Paragraph("$3,497/mo", S["price_main"])],
    [Paragraph("GBP verification, PPC + Meta Retargeting, directory cleanup, website review.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly accountability, SOP documentation, hiring/delegation groundwork.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$4,700–$5,000/mo", S["price_main"])],
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
    "Total: $6,097/mo + $4,700–$5,000 ad spend  |  Save $1,197/mo by bundling  |  33.2%–34.1% of revenue (under 35% cap)",
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
