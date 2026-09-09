"""
Sales Companion PDF Template — SMB Team
========================================
This template generates the 2-page internal Sales Companion PDF for the sales rep.
It uses reportlab. Do not modify the layout, colors, fonts, styles, or structure.
Only replace the # FILL: placeholders with audit-specific content.

IMPORTANT: The final PDF must be exactly 2 pages. If content overflows to a third
page, shorten bullet text — do not remove sections.

Output filename: [FirmName]_[Date]_Sales_Companion.pdf
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

_FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "Design Files", "fonts")
pdfmetrics.registerFont(TTFont("Poppins", os.path.join(_FONT_DIR, "Poppins-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Bold", os.path.join(_FONT_DIR, "Poppins-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Italic", os.path.join(_FONT_DIR, "Poppins-Italic.ttf")))
pdfmetrics.registerFontFamily(
    "Poppins", normal="Poppins", bold="Poppins-Bold",
    italic="Poppins-Italic", boldItalic="Poppins-Bold",
)

DARK_NAVY = HexColor("#003A59")
SECTION_BLUE = HexColor("#0091C9")
ACCENT_GREEN = HexColor("#3B6D11")
MEDIUM_GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#888888")
RULE_GRAY = HexColor("#CCCCCC")
QUOTE_BG = HexColor("#F5F7F0")
WHITE = HexColor("#FFFFFF")
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "gourjian/Gourjian Law_September 8, 2026_Sales_Companion.pdf"


def add_page_elements(canvas, doc):
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


def b(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY,
                       spaceBefore=3, spaceAfter=3)

def quote_block(text):
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

story.append(Paragraph("Gourjian Law", S["title"]))
story.append(Paragraph("Sales Companion  |  September 8, 2026  |  Rep: Nick Holderman", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Varand Gourjian", S["snap_value"]),
     Paragraph("$3M+ gross, 60% margin", S["snap_value"]),
     Paragraph("8 attys / unclear staff", S["snap_value"]),
     Paragraph("3", S["snap_value"]),
     Paragraph("N/A (hourly GC)", S["snap_value"]),
     Paragraph("Glendale, CA", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: SCALE THE FIRM'S CAPACITY", S["section"]))
story.append(Paragraph("Varand wants to keep hiring attorneys who can each generate $650K-$700K, without the firm's growth staying permanently capped by his own personal referral network.", S["subsection"]))

story.append(quote_block("built entirely on referrals"))
story.append(Spacer(1, 1))
story.append(quote_block("60% profit margins"))
story.append(Spacer(1, 1))
story.append(quote_block("consistent 20%+ annual growth"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Keep hiring rainmaking attorneys.</b> Each new hire is expected to generate $650K-$700K."))
story.append(bd("<b>Build the &quot;branded play.&quot;</b> Content and authority marketing, not consumer-style PPC."))
story.append(bd("<b>Reduce referral dependence.</b> A visible market presence that works even when he's not the one introducing a client."))
story.append(bd("<b>Put profit to work.</b> Turn his stated ~20% reinvestment appetite into an actual plan."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Zero visibility.</b> The firm does not appear in organic or paid search for its own practice areas."))
story.append(b("<b>No content asset.</b> The site's &quot;News Feed&quot; is syndicated news, not firm-authored writing."))
story.append(b("<b>No intake system.</b> Every inquiry funnels through one email inbox with no tracking."))
story.append(b("<b>No ops layer.</b> A lean, top-heavy attorney team with nobody dedicated to growth operations."))
story.append(b("<b>Directory mismatch.</b> FindLaw/Martindale/Yelp still show the legacy &quot;Gourjian Law Group&quot; bankruptcy branding."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds real market authority instead of relying solely on personal relationships."))
story.append(bd("Gives his next attorney hires a firm with visible market presence behind them, not just a referral book."))
story.append(bd("Lets his 21-year reputation keep working for him even when he isn't the one making the introduction."))

story.append(Paragraph("<b>Full Service Marketing — Dominate  |  $12,497/mo</b>", S["subsection"]))
story.append(b("Revenue of $3M+ gross ties to the Dominate tier on SMB Team's marketing table."))
story.append(b("No coaching package is paired here, so this is priced at the $12,497/mo stand-alone rate, not the $10,497/mo bundled rate."))
story.append(b("Seller-reviewed override (Slack, 9/9/26): dropped the originally proposed Platinum + Elite Coach Plus bundle in favor of Dominate stand-alone."))
story.append(b("Scoped around content, local SEO, and directory cleanup — not a PPC-volume funnel — matching what was actually discussed on the call."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Gourjian Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Tests content distribution and visibility at low cost, without shifting into consumer-style PPC volume tactics."))
story.append(bd("Every dollar spent claims visibility no named competitor is currently paying for."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $4,500/mo — minimum viable spend to start testing content distribution."))
story.append(b("<b>Aggressive:</b> $18,000/mo — well under Dominate's $100,000 ad spend cap."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~5 inquiries x $5K = ~$25.5K/mo vs. $4.5K spend = ~5.7x return."))
story.append(b("<b>Aggressive:</b> ~25 inquiries x $5K = ~$122.7K/mo vs. $18K spend = ~6.8x return (mechanical ceiling only — see note)."))
story.append(Paragraph("<i>All figures are estimates using the Business Law CPL proxy (no CPL table exists for outside GC/B2B). This firm's real addressable search volume is lower than a consumer practice area, so treat the aggressive scenario as a ceiling, not a forecast. Do not quote lead counts to the client.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Business Law Google Search CPL $110 x 1.2 cushion = $132 blended. $4,500 / $132 = ~34 leads x 15% close = ~5 inquiries."))
story.append(b("<b>Aggressive:</b> Same $110 CPL, no cushion. $18,000 / $110 = ~164 leads x 15% = ~25 inquiries — not realistic for this niche B2B market; shown for protocol completeness only."))
story.append(b("Total spend at aggressive: $12,497 + $18,000 = $30,497/mo = ~12.2% of ~$250K monthly revenue. Under the 35% cap."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We\'ve never needed marketing before — why start now?"', S["objection_q"]))
story.append(Paragraph("Growth is capped by referrals alone, and Babachanian already outranks Gourjian Law for identical GC services — the market is starting to move even though the phone still rings today.", S["objection_a"]))

story.append(Paragraph('"Traditional legal marketing doesn\'t work for our clients."', S["objection_q"]))
story.append(Paragraph("Agreed — that's why this is scoped around content and authority (the &quot;branded play&quot; from the call), not a PPC-volume funnel. Ad spend here is modest and targeted, not a shift into consumer-style marketing.", S["objection_a"]))

story.append(Paragraph('"Is $12,497/month worth it for a firm already doing $3M?"', S["objection_q"]))
story.append(Paragraph("At ~$250K/month revenue, this is under 5% of monthly revenue on its own, well inside the 35% cap. Varand already said on the call he's open to reinvesting ~20% of revenue (~$600K/year) toward growth.", S["objection_a"]))

story.append(Paragraph('"We don\'t have anyone to manage this internally."', S["objection_q"]))
story.append(Paragraph("That's the point of Full Service Marketing — SMB Team runs the day-to-day so nobody on the lean, top-heavy attorney team has to own it.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Dominate</b>", S["price_main"]),
     Paragraph("$12,497/mo", S["price_main"])],
    [Paragraph("Content, local SEO, directory cleanup, and targeted paid presence.", S["price_detail"]),
     Paragraph("Stand-alone rate — no coaching bundled", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$4,500–$18,000/mo", S["price_main"])],
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
    "Total: $12,497/mo + $4,500–$18,000 ad spend  |  Single-service engagement — no bundling savings apply  |  6.8%–12.2% of revenue (under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
