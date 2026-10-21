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

# FILL: Output path — use format [FirmName]_[MMDDYYYY]_Sales_Companion.pdf
OUTPUT_PATH = "harold-rosbottom/Harold Rosbottom_October 28, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Harold Rosbottom", S["title"]))
story.append(Paragraph("Sales Companion  |  October 28, 2026  |  Rep: Daniel Lowe", S["subtitle"]))
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
    [Paragraph("Harold (role unconfirmed)", S["snap_value"]),
     Paragraph("$3M+ (HubSpot, not stated on call)", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Dallas, TX (PI)", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE WITHOUT OVERPAYING", S["section"]))
story.append(Paragraph("Harold wants to add paid channels to an organic-led firm without overpaying: start at a budget, then scale on results. (Inferred, low confidence. No personal motive was stated.)", S["subsection"]))

story.append(quote_block("Sure, as cheap as possible, Daniel. (00:11:04)"))
story.append(Spacer(1, 1))
story.append(quote_block("we probably would start at a budget. And if we have good success, then add to the budget. (00:14:38)"))
story.append(Spacer(1, 1))
story.append(quote_block("We don't understand or have any knowledge about the cost or how the system works, so we're looking for an expert to do that for us, and that's why I contacted you. (00:01:24)"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>ChatGPT ads from an expert.</b> His stated reason for the call: \"we're quite interested in that\" (00:01:08)."))
story.append(bd("<b>Paid ads only.</b> No web or SEO work in the package; he also named Meta and PPC (00:13:12)."))
story.append(bd("<b>A budget-first test.</b> Start modest and add budget only if the early results are good."))
story.append(bd("<b>Cost and yield data first.</b> He will not take platform steps until he sees the cost structure and likely yield (00:03:30)."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Cost caution.</b> \"As cheap as possible\" may clash with the $10,000 low end of the ad spend range."))
story.append(b("<b>ChatGPT availability.</b> Daniel still has to confirm if stand-alone ChatGPT ad management is offered."))
story.append(b("<b>Thin performance data.</b> ChatGPT ad results are a \"black box,\" so there is little proof to show."))
story.append(b("<b>Earlier timing.</b> He spoke to SMB Team months ago and it \"was still too early\" (00:01:36)."))
story.append(b("<b>Firm identity unconfirmed.</b> The trigger site belongs to The Law Firm of Aaron A. Herbert, P.C.; confirm it is Harold's firm."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("An expert runs Google, LSA and Meta, so he does not have to learn the platforms."))
story.append(bd("He starts at the low end and steps up only when the results support it."))
story.append(bd("He gets one fixed fee and a way to compare paid cost per case with his organic cost."))

story.append(Paragraph("<b>Paid Ads Starter  |  $3,497/mo (stand-alone price, no bundle discount)</b>", S["subsection"]))
story.append(b("Seller locked Paid Ads Starter stand-alone on 10/21: no coaching, no web, no other products."))
story.append(b("Priced at $3,497 stand-alone, not the $2,497 bundled rate. Savings are $0."))
story.append(b("Ad spend cap for this sub-package is $20,000/mo; the plan stays at or under it."))
story.append(b("Catalog pairs ads-only with coaching and wants Full Service if mobile speed is under 50 (it is 43). Seller chose ads-only."))
story.append(b("Revenue is from HubSpot, not the call. PI in Dallas needs approval. ChatGPT is shown only as a test where available."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Harold — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives paid channels enough budget to produce real data, not a token test."))
story.append(bd("Ties every increase to cost per signed case, which is how he wants to scale."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $10,000/mo, the PI floor for a high-competition market and the car accident Google minimum."))
story.append(b("<b>Aggressive:</b> $20,000/mo, capped at the Paid Ads Starter ad spend cap."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 2.9 cases x $5K-$8K = $14K-$23K/mo vs. $10K spend = 1.4x-2.3x return."))
story.append(b("<b>Aggressive:</b> 6.9 cases x $5K-$8K = $35K-$55K/mo vs. $20K spend = 1.7x-2.8x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Case value is the accident/injury default; he gave none. Close rate 15% is a default.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Car accident Google PPC minimum $10,000, which matches the PI high-competition floor of $10,000."))
story.append(b("<b>Aggressive:</b> No revenue goal was stated. 4x the floor is $40,000, capped at $20,000 for this sub-package."))
story.append(b("<b>ROI math:</b> 80% Google ($705 CPL) and 20% Meta cold ($170), blended $433; conservative adds 20% (CPL $519). ChatGPT excluded, no CPL data."))
story.append(b("Total spend at aggressive: $23,497/mo = 9.4% of $3M (HubSpot, unconfirmed). Conservative: $13,497 = 5.4%. Under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"Sure, as cheap as possible." Ten thousand a month is not cheap.', S["objection_q"]))
story.append(Paragraph("Daniel's $750 figure was only the ChatGPT minimum. Dallas PI Google leads run $630-$780 each, so a small test yields a handful of leads and no real data. Anything under the $10,000 PI floor needs paid ads team review.", S["objection_a"]))

story.append(Paragraph('"We have no interest in paying $3,000 per lead."', S["objection_q"]))
story.append(Paragraph("Estimated cost is about $2,900-$3,500 per signed case, not per lead. He said organic is \"well below that\" and paid \"costs a little more.\" Position paid as added volume, tracked by cost per signed case.", S["objection_a"]))

story.append(Paragraph('"Can you run ChatGPT ads on their own?"', S["objection_q"]))
story.append(Paragraph("Do not promise it. Daniel is confirming with the agency. Paid Ads Starter covers Google, LSA and Meta, with ChatGPT as a measured test where available. Rad Law Firm already runs Google ads on car accident searches.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Paid Ads Starter</b>", S["price_main"]),
     Paragraph("$3,497/mo", S["price_main"])],
    [Paragraph("Google, LSA and Meta management. No web or SEO.", S["price_detail"]),
     Paragraph("stand-alone price, no discount", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$10,000–$20,000/mo", S["price_main"])],
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
    "Total: $3,497/mo + $10,000–$20,000 ad spend  |  No bundle savings (stand-alone)  |  5.4%–9.4% of revenue (under 35% cap)",
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
