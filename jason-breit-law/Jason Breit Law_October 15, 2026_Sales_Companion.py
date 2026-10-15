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
_FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Design Files", "fonts")
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

OUTPUT_PATH = "jason-breit-law/Jason Breit Law_October 15, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Jason Breit Law", S["title"]))
story.append(Paragraph("Sales Companion  |  October 15, 2026  |  Rep: Nick Holderman", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Jason R. Breit, Esq.", S["snap_value"]),
     Paragraph("Not stated (HubSpot band $180K-$960K)", S["snap_value"]),
     Paragraph("Not stated (site lists 2)", S["snap_value"]),
     Paragraph("3 (prelim.)", S["snap_value"]),
     Paragraph("Not stated (15% default)", S["snap_value"]),
     Paragraph("Melville, NY", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: NOT YET KNOWN", S["section"]))
story.append(Paragraph("No discovery call was recorded, so there are no quotes and no stated goal. Learn his real motive on the proposal call.", S["subsection"]))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>Ask on the call:</b>", S["subsection"]))
story.append(bd("<b>What growth means to him.</b> More time, a firm he can sell, or a bigger footprint?"))
story.append(bd("<b>Where clients come from today.</b> Referrals, the website, past clients, or ads?"))
story.append(bd("<b>The numbers.</b> Annual revenue, average plan value, close rate, and team size."))
story.append(bd("<b>Current vendors.</b> Who built the landing page and writes the blog posts?"))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What may be stopping him (public research only):</b>", S["subsection"]))
story.append(b("<b>Slow mobile site.</b> Lighthouse scores 43 mobile and 89 desktop; the main content takes 7.4 seconds."))
story.append(b("<b>No paid channel seen.</b> Google, LSA, and Meta ads were not observed, but those tools could not be viewed."))
story.append(b("<b>Review gap unknown.</b> All review counts are unconfirmed; do not compare his count to anyone."))
story.append(b("<b>Thin local pages.</b> No pages for Garden City, Huntington, or Massapequa."))
story.append(b("<b>Brand built on Jason.</b> Name, bio, and consult offer all center on him."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts a measured, always-on channel in front of Nassau and Suffolk families searching for estate planning and elder law."))
story.append(bd("Shows which search or audience produces consultations, so he can decide where to invest next."))

story.append(Paragraph("<b>Paid Ads Essentials  |  $1,997/mo bundled</b>", S["subsection"]))
story.append(b("Seller-set package from the Slack request on 10/15; the proposal is locked."))
story.append(b("No stand-alone price exists, so there is no savings line in the report."))
story.append(b("Normally Essentials needs one practice area; this firm lists several."))
story.append(b("Mobile score under 50 normally means Full Service. Roadmap Phase 2 covers the upgrade."))

story.append(thin_rule())

story.append(Paragraph("Why No Coaching Package", S["section"]))

story.append(Paragraph("<b>What to tell him:</b>", S["subsection"]))
story.append(bd("Start with one clear channel, then add operations support when leads are steady."))
story.append(bd("Phase 2 adds Fractional COO support; Phase 3 adds Fractional CFO, bookkeeping, and AI Workforce."))

story.append(Paragraph("<b>Elite Coach Plus removed by the seller</b>", S["subsection"]))
story.append(b("The decision file first picked Elite Coach Plus ($3,200/mo bundled), then the seller dropped it."))
story.append(b("Default policy is marketing plus a non-marketing package; confirm this choice with sales-ops."))
story.append(b("Revenue and team size are HubSpot estimates ($570K, 3 people), not facts from Jason."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Jason Breit Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Buys enough Google and Meta traffic to learn what works in a crowded Long Island market."))
story.append(bd("Stays well inside the $7,500 Paid Ads Essentials cap, so there is room to scale."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $4,500/mo — Google $3,500 plus Meta retargeting $1,000."))
story.append(b("<b>Aggressive:</b> $6,000/mo — Google $4,000, Meta retargeting $1,000, Meta cold $1,000."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~5.6 cases x $1.5K-$3K = $8.4K-$16.9K/mo vs. $4.5K spend = 1.9x-3.7x return."))
story.append(b("<b>Aggressive:</b> ~10 cases x $1.5K-$3K = $15.0K-$30.1K/mo vs. $6.0K spend = 2.5x-5.0x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Case value and 15% close rate are defaults.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Range:</b> set by the seller ($4,500-$6,000). Estate planning CPL midpoints: Google $135, Meta retargeting $52.50, Meta cold $55."))
story.append(b("<b>Conservative leads:</b> 37.5 at a $120 blended CPL (20% cushion). <b>Aggressive:</b> 66.9 at $90."))
story.append(b("<b>Flag:</b> Below the estate planning channel minimums ($6,700 with LSA). Send to paid ads team for review."))
story.append(b("Total spend at aggressive: $7,997/mo = 16.8% of the $570K estimate. Under the 35% cap."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We get our clients from referrals and reviews. Why do we need ads?"', S["objection_q"]))
story.append(Paragraph("Referral mix is unknown, so ask. Competitors like Davidov and Ettinger promote large review totals, and ads add a channel with monthly reporting on leads and cost per lead.", S["objection_a"]))

story.append(Paragraph('"$2K in fees plus $4.5K-$6K in ads is a lot."', S["objection_q"]))
story.append(Paragraph("His site lists couples plans at $2,000-$10,000, so roughly 3-4 signed plans a month would cover $6.5K-$8K of total cost. That is an estimate; ask his real average.", S["objection_a"]))

story.append(Paragraph('"Shouldn\'t we fix the website first?"', S["objection_q"]))
story.append(Paragraph("He is right that mobile is 43/100. Paid Ads Essentials does not rebuild the site. Position the Phase 2 upgrade and ask who manages the site today.", S["objection_a"]))

story.append(Paragraph('"We already have someone handling our marketing."', S["objection_q"]))
story.append(Paragraph("A developer-hosted landing page and SEO-style blog titles hint at a vendor. If he just signed one, do not push marketing; reposition around coaching or operations.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Paid Ads Essentials</b>", S["price_main"]),
     Paragraph("$1,997/mo", S["price_main"])],
    [Paragraph("Managed Google and Meta campaigns with monthly reporting.", S["price_detail"]),
     Paragraph("No stand-alone price", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$4,500–$6,000/mo", S["price_main"])],
    [Paragraph("Goes to Google and Meta — not to SMB Team.", S["price_detail"]),
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
]))
story.append(pt)
story.append(Paragraph(
    "Total: $1,997/mo + $4,500–$6,000 ad spend  |  No bundling savings  |  13.7%–16.8% of revenue (est. $570K; under 35% cap)",
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
