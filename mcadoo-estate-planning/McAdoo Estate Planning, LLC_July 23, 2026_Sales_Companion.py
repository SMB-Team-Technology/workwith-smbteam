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

OUTPUT_PATH = "mcadoo-estate-planning/McAdoo Estate Planning, LLC_July 23, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("McAdoo Estate Planning, LLC", S["title"]))
story.append(Paragraph("Sales Companion  |  July 23, 2026 (re-trigger, 2nd pass)  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Kim McAdoo (attorney) / Scott Holt (ops)", S["snap_value"]),
     Paragraph("$3M+ (HubSpot est., re-confirmed this pass)", S["snap_value"]),
     Paragraph("~4 (under 5)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Jamaica, Queens NY", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM (Operational Relief)", S["section"]))
story.append(Paragraph("Scott wants the firm's marketing, intake, and vendor coordination to run without his constant manual intervention — freedom from being the fallback for every gap.", S["subsection"]))

story.append(quote_block("forced to DIY landing pages causing inconsistency and fatigue"))
story.append(Spacer(1, 1))
story.append(quote_block("crap"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Automatic intake.</b> Leads followed up and CRM data kept clean without him doing it by hand."))
story.append(bd("<b>After-hours coverage that just works.</b> No leads slipping through untracked outside business hours."))
story.append(bd("<b>A marketing system, not a manual patch job.</b> Landing pages and vendor coordination handled by a system, not by him."))
story.append(bd("<b>A website that matches the real focus.</b> Estate planning positioning finally leading over probate."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Generalist ad vendor.</b> Grow My Ads spend grew $6K→$8K/mo with no cost-per-case data."))
story.append(b("<b>No active web vendor.</b> Prior vendor was terminated — nobody maintains the site now."))
story.append(b("<b>NAP inconsistency is spreading.</b> 2 wrong addresses/phones across directories, now bleeding into Google's own review data."))
story.append(b("<b>No profit visibility.</b> Revenue and case-value figures weren't shared — spend decisions are blind."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Takes the generalist vendor relationship and DIY landing-page work off his plate."))
story.append(bd("Gets the firm's message to finally lead with estate planning instead of probate."))

story.append(Paragraph("<b>Full Service Marketing — Platinum  |  $15,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue is $3M+ (HubSpot-sourced estimate) — qualifies for Platinum."))
story.append(b("Platinum's $150,000/mo ad spend cap comfortably covers the $3,500–$14,000/mo recommended range."))
story.append(b("Two-location firm (Jamaica + Garden City) needs geo-coverage a lower tier wouldn't scope for."))
story.append(b("Grow My Ads covers PPC only, not the full gap — frame as transitioning that spend, not stacking new spend on top."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Kim and Scott coaching support to build the delegation structure currently missing."))
story.append(bd("Creates accountability for shifting the practice mix toward estate planning and away from probate."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Team is Kim, Scott, a receptionist, an office manager, plus sales staff — under the 5-person Master's Circle threshold. Confirm exact count live."))
story.append(b("No profitability complaints were raised on the call, so a Fractional CFO/COO add-on was not included — revisit if Kim raises profit visibility live."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("McAdoo Estate Planning — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns the firm's already-active $6K–$8K/mo spend into professionally tracked, cost-per-case-informed investment instead of a guess."))
story.append(bd("Opens Meta as a genuinely new channel with zero current investment or competing internal campaigns."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — matches the Estate Planning Google PPC channel minimum, a single-channel floor."))
story.append(b("<b>Aggressive:</b> $14,000/mo — scaled multi-channel budget (Google Search + LSA + Meta) sized to the firm's $3M+ revenue band."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~3 cases x $2.25K avg case value = ~$6.75K/mo vs. $3.5K spend = ~1.9x return."))
story.append(b("<b>Aggressive:</b> ~25 cases x $2.25K avg case value = ~$56.25K/mo vs. $14K spend = ~4.0x return."))
story.append(Paragraph("<i>All figures are estimates using an Estate Planning practice-area default case value (no firm-confirmed figure was available). Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Estate Planning Google PPC minimum = $3,500 (single active channel floor)."))
story.append(b("<b>Aggressive:</b> Blended CPL across Google Search ($135), LSA ($65), and Meta Cold ($55) midpoints, sized to a $14,000/mo multi-channel budget within Platinum's $150,000 cap."))
story.append(b("Total spend at aggressive: $19,197 (Platinum + Elite Coach Plus) + $14,000 ad spend = $33,197/mo ≈ 13.3% of the $250,000/mo revenue estimate ($3M/yr) — well under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We\'re already spending $6K-$8K a month with Grow My Ads — why pay more?"', S["objection_q"]))
story.append(Paragraph("Grow My Ads is a generalist vendor with no confirmed cost-per-case tracking, and it only covers PPC — the site, local SEO, directories, and social are still unaddressed. Platinum is a transition of that spend into legal-specific management plus the coverage Grow My Ads never touched, not an added cost on top.", S["objection_a"]))

story.append(Paragraph('"Our reviews already beat the competition — why do we need SEO work?"', S["objection_q"]))
story.append(Paragraph("True — 4.9 stars and 275 reviews beat every named competitor, including Morgan Legal Group's 157 — but at least two distinct wrong addresses/phone numbers across Avvo, Justia, and Yelp are now bleeding into Google's own review aggregation. That's an active, worsening leak in the trust signals already earned, not a one-time cleanup.", S["objection_a"]))

story.append(Paragraph('"Scott is already stretched thin — won\'t another vendor add more work?"', S["objection_q"]))
story.append(Paragraph("The opposite: Platinum replaces the DIY landing-page work and vendor coordination Scott already does by hand, and Elite Coach Plus adds coaching support to build the delegation structure that's missing.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Platinum</b>", S["price_main"]),
     Paragraph("$15,997/mo", S["price_main"])],
    [Paragraph("Legal-specific ads, local SEO/NAP cleanup, geo pages, Meta launch.", S["price_detail"]),
     Paragraph("<strike>$18,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, masterminds, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
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
    "Total: $19,197/mo + $3,500–$14,000 ad spend  |  Save $3,297/mo by bundling  |  9.1%–13.3% of revenue (under 35% cap)",
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
