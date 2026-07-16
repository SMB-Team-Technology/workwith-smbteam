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

OUTPUT_PATH = "grimmett-lawfirm/Grimmett_Law_Firm_07292026_Sales_Companion.pdf"


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

story.append(Paragraph("Grimmett Law Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  July 29, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("David Grimmett", S["snap_value"]),
     Paragraph("~$900K (on track)", S["snap_value"]),
     Paragraph("5 (incl. owner)", S["snap_value"]),
     Paragraph("3: Solo Practitioner", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Franklin, TN", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE AND DOMINATE (inferred)", S["section"]))
story.append(Paragraph("David wants to build a $10M, 10-lawyer firm — not just grow revenue, but dominate his market. Not stated in personal terms on the call; confirm directly on 7/29.", S["subsection"]))

# NOTE: No direct word-for-word transcript quotes about DBM were captured in research
# notes (explicitly flagged as inferred, not stated in personal terms). Using a factual
# snapshot table in place of fabricated quote blocks per the no-invented-quotes rule.
snap2 = [
    [Paragraph("<b>Revenue Goal</b>", S["snap_label"]), Paragraph("$10M within 3-5 years", S["snap_value"])],
    [Paragraph("<b>Team Goal</b>", S["snap_label"]), Paragraph("10 lawyers", S["snap_value"])],
    [Paragraph("<b>Margin Goal</b>", S["snap_label"]), Paragraph("15% profit margin", S["snap_value"])],
]
t2 = Table(snap2, colWidths=[1.6*inch, 4.9*inch])
t2.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
]))
story.append(t2)
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Build a $10M firm.</b> He has a concrete revenue target, not just \"more growth.\""))
story.append(bd("<b>Grow to 10 lawyers.</b> He wants a real firm with a real bench, not a one-attorney shop."))
story.append(bd("<b>Hit a 15% profit margin.</b> He wants growth that actually pays out, not just more cases."))
story.append(bd("<b>Own his market.</b> The transcript frames this as moving from skilled lawyer to business owner."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>One referral source.</b> Nearly all new clients come through \"Shannara\" in Alabama at a ~50% fee."))
story.append(b("<b>Negative-margin cases.</b> $2,500-$5,000 fees against $3,000-$4,000 referral costs on 80% of a 156-case load."))
story.append(b("<b>Missed calls.</b> ~20% of 260-300 weekly calls go unanswered."))
story.append(b("<b>Suppressed visibility.</b> GBP miscategorized as \"General Law,\" Yelp as \"Divorce & Family Law.\""))
story.append(b("<b>Thin team structure.</b> 5 people total; no leadership layer for a 10-lawyer future."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Replaces a single 50%-fee referral source with lead channels he owns outright."))
story.append(bd("Fixes GBP/Yelp category errors that are actively hiding him from PI searches."))
story.append(bd("Puts him in front of high-intent searches Griffith Law and The Williams Firm currently win."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$900K falls in the $400K-$1M Starter tier band."))
story.append(b("PI practice area requires minimum Starter tier — Essentials is not eligible."))
story.append(b("Ad spend cap for Starter ($8K) covers the $7,500 conservative recommendation."))
story.append(b("Bundled saves $850/mo vs. the $5,697/mo retail price."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the leadership structure he needs to grow from 5 people to 10 lawyers."))
story.append(bd("Builds a real profit plan so revenue growth turns into the 15% margin he wants."))
story.append(bd("Gives him a peer group of other growth-stage firm owners solving the same scaling problems."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$900K falls in the $400K-$1M Elite Coach Plus band."))
story.append(b("Coach Essentials/Essentials Plus are eliminated products — not eligible regardless of fit."))
story.append(b("Includes weekly group coaching, practice masterminds, quarterly workshops, one annual in-person event."))
story.append(b("Bundled saves $297/mo vs. the $3,497/mo retail price."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Grimmett Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Starts generating cases outside the Shannara referral relationship immediately."))
story.append(bd("Puts real numbers behind the $10M goal instead of hoping referrals keep pace."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,500/mo — minimum viable spend across Google, LSA, and Meta."))
story.append(b("<b>Aggressive:</b> $25,000/mo — scaled spend aligned to the $10M revenue goal."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~2-3 cases x $2.5K-$5K = ~$6K-$12K/mo vs. $7.5K spend = ~0.8x-1.6x return."))
story.append(b("<b>Aggressive:</b> ~9-10 cases x $2.5K-$5K = ~$24K-$48K/mo vs. $25K spend = ~1.0x-1.9x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Case cycles run longer than one month.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Accident & Injury channel minimums blended across Google, LSA, Meta = $7,500."))
story.append(b("<b>Aggressive:</b> $10M goal x 20% / 12 months scaled to Tier 3 (Nashville) market, minus mgmt fee = $25,000."))
story.append(b("Total spend at aggressive ($25K) + mgmt fees ($8,047) = ~$33K/mo = ~3.7% of the $900K current revenue base. Well under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We already get clients through Shannara — why do I need this?"', S["objection_q"]))
story.append(Paragraph("Referrals cost ~50% of the fee, and case economics are already thin ($2.5K-$5K fee vs. $3K-$4K referral cost on 80% of the caseload). Owned lead gen protects margin instead of giving half of it away.", S["objection_a"]))

story.append(Paragraph('"We don’t have time to manage new marketing on top of everything else."', S["objection_q"]))
story.append(Paragraph("Full Service Marketing is fully managed by SMB Team — David's team doesn't run campaigns, they run the firm. Elite Coach Plus adds the leadership support to make that sustainable.", S["objection_a"]))

story.append(Paragraph('"$8,047/mo plus ad spend feels like a lot right now."', S["objection_q"]))
story.append(Paragraph("At ~3.7% of current revenue even at the aggressive ad spend level, this is well under the 35% cap — and closing the 20% missed-call gap alone recovers value before a new ad dollar is spent.", S["objection_a"]))

story.append(Paragraph('"How do we know this will actually beat what Griffith Law and The Williams Firm are doing?"', S["objection_q"]))
story.append(Paragraph("Both carry stronger review counts (Griffith Law's established footprint, Williams' 81 reviews at 5.0) than Grimmett's ~27 — but neither has confirmed paid ad activity. This is a real window to move first.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Owned lead gen: Google Ads, local SEO, GBP/directory fixes.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Leadership + profit-plan coaching toward the 10-lawyer goal.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,500–$25,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $7,500–$25,000 ad spend  |  Save $1,147/mo by bundling  |  ~2.1%–3.7% of revenue (under 35% cap)",
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
