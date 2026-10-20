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
_FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "Design Files", "fonts")
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

OUTPUT_PATH = "morgan-law/Morgan Law_October 20, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Morgan Law", S["title"]))
story.append(Paragraph("Sales Companion  |  October 20, 2026  |  Rep: Daniel Lowe", S["subtitle"]))
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
    [Paragraph("David L. Morgan", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Idaho / Utah", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SECURITY", S["section"]))
story.append(Paragraph("He wants a firm that provides for his large family for the next 20 years.", S["subsection"]))

story.append(quote_block("Now that I have eight kids, you can see behind me on the wall, I've got a lot to take care of."))
story.append(Spacer(1, 1))
story.append(quote_block("I figured I might as well get moving for the next 20 years."))
story.append(Spacer(1, 1))
story.append(quote_block("I need to show up as the number one guy, because I think I can, especially since I've been here for so long."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>10 to 15 cases a month.</b> He gets about two to three today."))
story.append(bd("<b>To be first in new channels.</b> He wants ChatGPT Ads live before anyone else in Boise."))
story.append(bd("<b>To be the number one name locally.</b> Canyon County first, then Boise."))
story.append(bd("<b>Results he can see fast.</b> He likes PPC and does not trust organic SEO."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Referral dependence.</b> Almost every case comes from family, friends, and past clients."))
story.append(b("<b>ChatGPT Ads blocked.</b> OpenAI says the site blocks crawlers; cause unconfirmed."))
story.append(b("<b>Dated website.</b> Not updated since about 2019; no pages for his target markets."))
story.append(b("<b>Budget limits.</b> He wants about $1,000 per case; no money for organic."))
story.append(b("<b>Low reviews.</b> He says they are low; counts are unconfirmed."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Replaces referral luck with a steady flow of new cases from search and ads."))
story.append(bd("Fixes the site so ChatGPT Ads and AI search can finally read it."))
story.append(bd("Puts him in front of people searching in Canyon County, where he is based."))

story.append(Paragraph("<b>Full Service Marketing Essentials  |  $3,797/mo</b>", S["subsection"]))
story.append(b("Seller override (Oct 20): lowest full-service tier, no coaching, for budget."))
story.append(b("Essentials is normally hidden for PI and multi-office firms. Seller-approved exception."))
story.append(b("Revenue is a HubSpot estimate ($180K-$960K), not stated. Confirm it."))
story.append(b("ChatGPT Ads management is not a documented Essentials item. Confirm first."))

story.append(thin_rule())

# ── Why No Coaching Package ──
story.append(Paragraph("Why No Coaching Package", S["section"]))

story.append(Paragraph("<b>What this choice does for him:</b>", S["subsection"]))
story.append(bd("Keeps his monthly cost low while he proves the channels work."))
story.append(bd("Lets him judge SMB Team on lead flow before adding more."))

story.append(Paragraph("<b>No coaching package  |  $0/mo</b>", S["subsection"]))
story.append(b("Seller removed Elite Coach Plus ($3,200/mo) on Oct 20."))
story.append(b("He raised budget concerns twice on the call (00:10:22, 00:17:58)."))
story.append(b("Team size is unknown; intake and hiring needs come with volume."))
story.append(b("Phase 2 adds FCOO Advisor ($3,297/mo) at 8 to 10 cases a month."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Morgan Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns his budget into high-intent leads in Canyon County and Boise."))
story.append(bd("Caps spend at a level he can afford while he tests what works."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,500/mo — the Essentials cap (seller override)."))
story.append(b("<b>Aggressive:</b> $7,500/mo — same cap; only the lead-cost cushion differs."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 3.9 cases x $6.5K = $25.6K/mo vs. $7.5K spend = 3.4x return."))
story.append(b("<b>Aggressive:</b> 4.7 cases x $6.5K = $30.8K/mo vs. $7.5K spend = 4.1x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. $6.5K is the midpoint of the $5K-$8K practice-area default, not his stated figure.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Injury minimums are PPC $6,000 + LSA $2,000 = $8,000, so the $7,500 cap binds. Modeled 50% Google, 30% LSA, 20% Meta retargeting; $285 CPL with 20% cushion; 15% close rate."))
story.append(b("<b>Aggressive:</b> 2x est. revenue ($1.14M) x 20% ÷ 12 = $19,000. Tier 4 (1.00x). Minus $3,797 fee = $15,203, but Essentials caps ad spend at $7,500. $238 CPL, no cushion."))
story.append(b("Cost per case is about $1,584-$1,901, above his $1,000 target. Say so up front."))
story.append(b("Total spend: $11,297/mo = 23.8% of est. revenue ($47.5K/mo). Under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"It takes too much money."', S["objection_q"]))
story.append(Paragraph("Essentials is our lowest full-service tier at $3,797/mo, ad spend is capped at $7,500, and there is no coaching add-on. His past spend went mostly to organic; paid channels give the faster results he prefers. Be honest that modeled cost per case runs above his $1,000 target, and agree to track it by channel.", S["objection_a"]))

story.append(Paragraph('"I never really got any results from it." (organic SEO)', S["objection_q"]))
story.append(Paragraph("Frame the new site as the landing page for ChatGPT Ads, PPC, and LSAs, not as organic SEO. He said PPC produced cases, and OpenAI's crawler block shows the current site is holding him back.", S["objection_a"]))

story.append(Paragraph('"Morgan &amp; Morgan and all those big firms."', S["objection_q"]))
story.append(Paragraph("His market is local. The named rivals are Litster Frost, Hepworth Holzer, and Andrew Injury Law (Nampa). He was an early mover on PPC and LSAs and believes no one in Boise is on ChatGPT yet. Review counts and ad activity are unverified; check live before the call.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Essentials</b>", S["price_main"]),
     Paragraph("$3,797/mo", S["price_main"])],
    [Paragraph("Website, local SEO, Google profile, managed Google Search, LSA, and retargeting.", S["price_detail"]),
     Paragraph("No bundle discount", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,500/mo", S["price_main"])],
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
]))
story.append(pt)
story.append(Paragraph(
    "Total: $3,797/mo + $7,500 ad spend  |  No bundle savings  |  23.8% of est. revenue (under 35% cap)",
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
