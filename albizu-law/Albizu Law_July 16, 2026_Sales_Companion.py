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

OUTPUT_PATH = "albizu-law/Albizu Law_July 16, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Albizu Law", S["title"]))
story.append(Paragraph("Sales Companion  |  July 16, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
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
    [Paragraph("Iris Albizu", S["snap_value"]),
     Paragraph("$1.8M ('25) / $2.0M proj.", S["snap_value"]),
     Paragraph("~3, lean", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Austin, TX", S["snap_value"])],
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
story.append(Paragraph("Iris wants to scale to $5M-$6M while cutting her hours from ~70/week down to a sustainable 40, so she has real time for her daughter before college.", S["subsection"]))

story.append(quote_block("The current pace is unsustainable and threatens burnout."))
story.append(Spacer(1, 1))
story.append(quote_block("Iris wants to regain time for family, especially a teenage daughter before she leaves for college."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>A sustainable 40-hour week.</b> Split 50/50 between case work and strategy, down from ~70 hours at 85% casework."))
story.append(bd("<b>Time with her daughter before college.</b> Her teenage daughter leaves for college soon — this is a closing window."))
story.append(bd("<b>Growth without more of her own hours.</b> Scale to $5M-$6M with only 4-5 planned hires, not by working harder."))
story.append(bd("<b>A team that runs cases without her.</b> Not just more staff — staff who can operate independently."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Owner-dependency.</b> Iris personally handles ~85% of casework — no delegation layer exists."))
story.append(b("<b>Zero local search visibility.</b> Firm did not appear in any of the 6 local-pack searches performed."))
story.append(b("<b>No intake process.</b> No CRM or follow-up sequence — referral leads can go uncontacted."))
story.append(b("<b>Bilingual hiring bottleneck.</b> The 4-5 hire plan (2-3 attorneys, 2 paralegals) has stalled on candidate availability."))
story.append(b("<b>No profit visibility.</b> Revenue has doubled in 2 years with no margin or cost-per-case tracking discussed."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Puts the firm in front of prospects currently finding Lincoln-Goldfinch, Kirker Davis, and Alonso & Alonso instead of her."))
story.append(bd("Turns the unused family law ad landing page into an active lead source with no new page build required."))
story.append(bd("Builds a visibility engine that does not depend on Iris's personal referral network."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $7,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue of $1.98M places the firm squarely in the $1M-$3M Growth tier band."))
story.append(b("Zero local-pack visibility across all 6 searches performed, spanning both practice areas."))
story.append(b("Existing family law landing page and 9 geo-targeted city pages are underused assets this package activates."))
story.append(b("LawInfo NAP conflict is actively suppressing local rankings and is corrected as part of this package."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives Iris a structured way to delegate instead of absorbing 85% of casework herself."))
story.append(bd("Turns the stalled 4-5 hire plan into an executable recruiting process."))
story.append(bd("Builds the leadership layer that lets the firm run without her in every case."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1M+ with team under 5 qualifies for Elite Coach Plus (Master's Circle requires 5+ dedicated staff)."))
story.append(b("No manager or delegated leadership layer currently exists at the firm."))
story.append(b("Owner-dependency is the single biggest blocker to the stated DBM of reclaiming personal time."))
story.append(b("Growth to $5M-$6M is explicitly tied to hiring in the transcript, not just lead volume."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Albizu Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Converts the firm's strong 4.7-star reputation into paid visibility instead of leaving it dormant."))
story.append(bd("Starts modest, in line with the transcript's caution against pushing volume the firm can't yet absorb."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — Family Law Google Search PPC minimum, reactivating the existing landing page."))
story.append(b("<b>Aggressive:</b> $14,000/mo — blended Google Search, LSA, and Meta across both practice areas."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~4 cases x $4K = ~$17.5K/mo vs. $3.5K spend = ~5.0x return."))
story.append(b("<b>Aggressive:</b> ~25 cases x $4.25K = ~$106K/mo vs. $14K spend = ~7.6x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Family Law channel minimum: Google PPC $3,500 (single channel, existing landing page)."))
story.append(b("<b>Aggressive:</b> Blended Google Search + LSA + Meta across both practice areas, held well under the Growth tier's $50,000 ad spend cap given the transcript's caution against pushing volume beyond current capacity."))
story.append(b("Total spend at aggressive: $14,000 ad spend + $10,597 bundled = $24,597/mo = ~14.9% of current monthly revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I don\'t have the bandwidth to handle more leads right now."', S["objection_q"]))
story.append(Paragraph("This is why coaching leads alongside marketing — Elite Coach Plus builds the team that can absorb new volume, and ad spend starts at $3,500/mo, not the $50K tier cap, so lead flow grows with capacity, not ahead of it.", S["objection_a"]))

story.append(Paragraph('"We\'ve grown fine on referrals alone — why fix what isn\'t broken?"', S["objection_q"]))
story.append(Paragraph("True, but every one of the 6 competitor searches performed put Lincoln-Goldfinch Law (1,523 reviews), Kirker Davis LLP (305 reviews), or Alonso & Alonso ahead of Albizu Law's ~40. Referrals got the firm to $1.8M; they will not get it to $5M-$6M against that visibility gap.", S["objection_a"]))

story.append(Paragraph('"Can we afford this on top of everything else?"', S["objection_q"]))
story.append(Paragraph("At $10,597/mo bundled plus $3,500-$14,000 ad spend, total spend runs ~8.5%-14.9% of current monthly revenue — well under the 35% cap SMB Team uses to keep spend sustainable.", S["objection_a"]))

story.append(Paragraph('"What about the immigration policy changes hurting our projections?"', S["objection_q"]))
story.append(Paragraph("That's a profit-visibility gap, not a marketing gap — Elite Coach Plus is scoped to build the cost-per-case tracking that shows whether the firm is more profitable, not just busier, as policy conditions shift.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("Google Ads, Local SEO, Meta ads, and website conversion work across both practice areas.", S["price_detail"]),
     Paragraph("<strike>$8,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, hiring plan support, practice-area masterminds.", S["price_detail"]),
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
    "Total: $10,597/mo + $3,500–$14,000 ad spend  |  Save $1,897/mo by bundling  |  8.5%–14.9% of revenue (under 35% cap)",
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
