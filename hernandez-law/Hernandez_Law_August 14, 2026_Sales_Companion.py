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

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Fonts — SMB Team brand font is Poppins. Embedded so it renders the
# same regardless of what's installed on the machine opening the PDF. ──
_FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
pdfmetrics.registerFont(TTFont("Poppins", os.path.join(_FONT_DIR, "Poppins-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Bold", os.path.join(_FONT_DIR, "Poppins-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Italic", os.path.join(_FONT_DIR, "Poppins-Italic.ttf")))
pdfmetrics.registerFontFamily(
    "Poppins", normal="Poppins", bold="Poppins-Bold",
    italic="Poppins-Italic", boldItalic="Poppins-Bold",
)

# ── Colors — SMB Team brand colors (Deep Wood Blue, Ocean Blue) plus the
# existing semantic grays/reds/savings-green, which stay as they were. ──
DARK_NAVY = HexColor("#003A59")     # Deep Wood Blue — brand primary
SECTION_BLUE = HexColor("#0091C9")  # Ocean Blue — brand accent, section headers
ACCENT_GREEN = HexColor("#3B6D11")  # savings/positive-outcome green — matches the audit report
MEDIUM_GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#888888")
RULE_GRAY = HexColor("#CCCCCC")
QUOTE_BG = HexColor("#F5F7F0")
WHITE = HexColor("#FFFFFF")
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

# FILL: Output path — use format [FirmName]_[MMDDYYYY]_Sales_Companion.pdf
OUTPUT_PATH = "hernandez-law/Hernandez_Law_August 14, 2026_Sales_Companion.pdf"


def add_page_elements(canvas, doc):
    """Draws red warning header and confidential footer on every page. DO NOT MODIFY."""
    canvas.saveState()
    width, height = letter
    canvas.setFont("Poppins-Bold", 10)
    canvas.setFillColor(RED_WARNING)
    canvas.drawCentredString(width / 2, height - 0.38 * inch,
                             "FOR INTERNAL USE ONLY; DO NOT SHARE.")
    canvas.setStrokeColor(RED_WARNING)
    canvas.setLineWidth(0.5)
    canvas.line(0.6 * inch, height - 0.44 * inch,
                width - 0.6 * inch, height - 0.44 * inch)
    canvas.setFont("Poppins", 7)
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
    "title", fontName="Poppins-Bold", fontSize=16, leading=20,
    textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle(
    "subtitle", fontName="Poppins", fontSize=9.5, leading=13,
    textColor=LIGHT_GRAY, spaceAfter=3)
S["section"] = ParagraphStyle(
    "section", fontName="Poppins-Bold", fontSize=11, leading=15,
    textColor=SECTION_BLUE, spaceBefore=6, spaceAfter=2)
S["subsection"] = ParagraphStyle(
    "subsection", fontName="Poppins-Bold", fontSize=10, leading=13,
    textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle(
    "bullet", fontName="Poppins", fontSize=9.5, leading=13,
    textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0,
    spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle(
    "bullet_dark", fontName="Poppins", fontSize=9.5, leading=13,
    textColor=DARK_NAVY, leftIndent=12, bulletIndent=0,
    spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle(
    "quote", fontName="Poppins-Italic", fontSize=9.5, leading=13,
    textColor=DARK_NAVY, leftIndent=6, rightIndent=6,
    spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle(
    "snap_label", fontName="Poppins-Bold", fontSize=8.5, leading=11,
    textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle(
    "snap_value", fontName="Poppins", fontSize=9.5, leading=12,
    textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle(
    "objection_q", fontName="Poppins-Bold", fontSize=9.5, leading=13,
    textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle(
    "objection_a", fontName="Poppins", fontSize=9.5, leading=13,
    textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle(
    "price_main", fontName="Poppins-Bold", fontSize=9.5, leading=13,
    textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle(
    "price_detail", fontName="Poppins", fontSize=8.5, leading=12,
    textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle(
    "savings", fontName="Poppins-Bold", fontSize=9.5, leading=13,
    textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle(
    "disclaimer", fontName="Poppins-Italic", fontSize=8.5, leading=11,
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

story.append(Paragraph("Hernandez Law (Law Offices of Tatiana Hernandez)", S["title"]))
story.append(Paragraph("Sales Companion  |  August 14, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Tatiana Hernandez", S["snap_value"]),
     Paragraph("~$500K (2026 pace)", S["snap_value"]),
     Paragraph("Owner + 3", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Beverly Hills, CA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM / BANDWIDTH", S["section"]))
story.append(Paragraph("Tatiana wants a firm that generates and converts cases without every decision routing through her personally, especially during discovery-heavy litigation weeks.", S["subsection"]))

story.append(quote_block("Everything routes through her, causing delays and missed opportunities."))
story.append(Spacer(1, 1))
story.append(quote_block("Acknowledged SMB Team will be higher ($3-4k) but includes foundational organic/GBP/site work and long-term asset building."))
story.append(Spacer(1, 1))
story.append(quote_block("Prospect is open to the $2,000-$4,000/month range, most likely to land at $3,000-$4,000/month."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>More bandwidth back.</b> She is exploring AI tools to reduce her discovery burden."))
story.append(bd("<b>Consistent case volume.</b> Target is 5+ qualified cases/month, up from 1-2, at $30K-$50K+ per case."))
story.append(bd("<b>A firm that runs without her micromanaging intake.</b> She wants delays and missed opportunities to stop."))
story.append(bd("<b>Reasonable, phased investment.</b> She is comfortable in the $3K-$4K/month range."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Referral slowdown.</b> Referring attorneys keeping cases in-house pulled 2026 revenue pace to ~$500K from ~$1M."))
story.append(b("<b>No organic/local presence.</b> GBP is misconfigured (wrong category, old LA address) and zero reviews exist on Facebook/Avvo."))
story.append(b("<b>Declining paid ad quality.</b> The existing Spanish Google Ads campaign (~$5K/mo + ~$1.2K fee) is producing misqualified leads."))
story.append(b("<b>Split bilingual web presence.</b> hernandezlawca.com and justicieralegal.com are separate domains."))
story.append(b("<b>She personally bottlenecks intake.</b> No delegated process exists, especially during heavy litigation weeks."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Builds a real local and organic presence so new cases stop depending only on a slowing referral network."))
story.append(bd("Fixes the GBP and review gap that is actively costing visibility against named local competitors."))
story.append(bd("Adds Spanish PPC/social ads and bilingual site work as a long-term asset, not just a recurring ad expense."))

story.append(Paragraph("<b>Full Service Marketing — Essentials  |  $3,497/mo bundled</b>", S["subsection"]))
story.append(b("Revenue (~$500K) is under the $750K Essentials ceiling."))
story.append(b("Single location (1 Beverly Hills office) and single practice area (Employment Law) — both required for Essentials eligibility."))
story.append(b("Bundled price saves $300/mo versus the $3,797/mo stand-alone rate."))
story.append(b("Fits within her stated $3,000-$4,000/month comfort range from the call."))

story.append(thin_rule())

# ── Why No Coaching Package (override note, not a template section swap) ──
story.append(Paragraph("Why No Coaching Package Is Included", S["section"]))

story.append(Paragraph("<b>Budget-reality override applied (full detail in workings file):</b>", S["subsection"]))
story.append(b("Revenue table implies Starter + Elite Coach Plus = $8,197/mo — never discussed on the call."))
story.append(b("$8,197/mo is roughly double her stated $3,000-$4,000/month comfort range."))
story.append(b("Recommendation: Essentials only ($3,497/mo) — lowest-cost fit for her stated need."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Hernandez Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Replaces declining-quality Spanish-only ads with a bilingual, better-targeted campaign."))
story.append(bd("Keeps total spend inside both her stated budget and the Essentials tier's ad spend cap."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000/mo — the table's absolute minimum for any paid ads (no Employment Law row exists)."))
story.append(b("<b>Aggressive:</b> $5,000/mo — capped at the Essentials tier's ad spend ceiling, not a 20%-rule output (see workings file)."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~3 cases x $40K = $120K/mo vs. $3,000 spend = ~40x return."))
story.append(b("<b>Aggressive:</b> ~7 cases x $40K = $272K/mo vs. $5,000 spend = ~54x return."))
story.append(Paragraph("<i>All figures are estimates using a disclosed Business Law CPL proxy (no Employment Law row exists) and a 15% default close rate. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Absolute minimum ($3,000) x 20% cushion CPL ($132, Business Law proxy) = ~23 leads x 15% close = ~3 cases."))
story.append(b("<b>Aggressive:</b> Capped at tier ad spend ceiling ($5,000), not the 20%-rule formula — full 20%-rule math was intentionally skipped per the budget-reality override."))
story.append(b("Total spend at aggressive: $8,497/mo (mgmt fee + ad spend) = ~20.4% of ~$500K revenue. Well under the 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"Why isn\'t coaching included if we talked about scaling?"', S["objection_q"]))
story.append(Paragraph("Coaching was never discussed on the call — needs were GBP, site, SEO, reviews, and Spanish ads. We scoped to her stated budget, not the full revenue-implied bundle.", S["objection_a"]))

story.append(Paragraph('"$3,497/mo feels like a lot on top of existing ad spend."', S["objection_q"]))
story.append(Paragraph("Her current agency fee alone is ~$1,200/mo for declining-quality leads. This replaces it with compounding assets (GBP, SEO, reviews) she has never had.", S["objection_a"]))

story.append(Paragraph('"How do we know this reverses the revenue decline?"', S["objection_q"]))
story.append(Paragraph("Zero reviews and a broken GBP mean she is invisible where Setareh (17), Matern (19), and Blady (17) all rank. Closing that gap is the highest-leverage fix available.", S["objection_a"]))

story.append(Paragraph('"What about the AI/discovery tool interest she mentioned?"', S["objection_q"]))
story.append(Paragraph("Flagged as a minor secondary interest, not the call's focus. Positioned as a Phase 3 roadmap item once the marketing foundation is in place — not a Phase 1 add that exceeds her budget.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Essentials</b>", S["price_main"]),
     Paragraph("$3,497/mo", S["price_main"])],
    [Paragraph("GBP remediation, EN/ES site consolidation, SEO, reviews, Spanish PPC/social ads.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Coaching Package</b>", S["price_main"]),
     Paragraph("None", S["price_main"])],
    [Paragraph("Not recommended — never requested on the call; budget-reality override applied.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000-$5,000/mo", S["price_main"])],
    [Paragraph("Goes to Google Ads — not to SMB Team.", S["price_detail"]),
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
    "Total: $3,497/mo + $3,000-$5,000 ad spend  |  Save $300/mo by bundling  |  15.6%-20.4% of revenue (under 35% cap)",
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
