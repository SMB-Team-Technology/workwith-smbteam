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

OUTPUT_PATH = "lopez-teal/Lopez_Teal_September_8_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Lopez Teal Real Estate Law &amp; Title", S["title"]))
story.append(Paragraph("Sales Companion  |  September 8, 2026  |  Rep: Nick Holderman", S["subtitle"]))
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
    [Paragraph("Annette Lopez Teal", S["snap_value"]),
     Paragraph("~$1.3M (2026 proj.)", S["snap_value"]),
     Paragraph("5 + 1 PT atty", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("N/A (referral)", S["snap_value"]),
     Paragraph("Coral Gables, FL", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: EXIT / SELLABILITY", S["section"]))
story.append(Paragraph(
    "Annette wants to build a sellable asset within 5 years by reducing her own dependence on the firm and diversifying its revenue base.",
    S["subsection"]))

story.append(quote_block("Build a sellable asset within 5 years by reducing owner dependence and diversifying revenue."))
story.append(Spacer(1, 1))
story.append(quote_block("Annette is 'drowning'."))
story.append(Spacer(1, 1))
story.append(quote_block("Consultation on scaling a law firm for a future sale."))
story.append(Spacer(1, 1))
story.append(quote_block("The firm's luxury niche (Coral Gables, Coconut Grove) provides high-profit files ($15k vs. $2k), reducing the need for high-volume work."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>A sellable business, not just more revenue.</b> The goal is an exit within 5 years, not a bigger top line."))
story.append(bd("<b>A higher sale multiple.</b> Referral-only firms trade at 2-3x; diversified, institutional-client firms trade at 4-5x."))
story.append(bd("<b>Diversified clients.</b> She wants institutional clients (lenders, developers) alongside her realtor/broker referral base."))
story.append(bd("<b>Relief from being the sole rainmaker.</b> She's working 50-60+ hour weeks carrying every relationship personally."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Every client relationship runs through Annette.</b> No one else at the firm carries a file end-to-end."))
story.append(b("<b>No leadership layer.</b> Five staff plus a part-time attorney, but no one managing operations."))
story.append(b("<b>No intake process.</b> No CRM or tracking — referrals depend on her personal availability."))
story.append(b("<b>No firm-wide profit plan.</b> She tracks file-level profitability but not overall margin or enterprise value."))
story.append(b("<b>Directory/NAP issues.</b> Avvo, Yelp, Justia, FindLaw, and Martindale still list her prior firm name and address."))

story.append(thin_rule())

# ── Why This Package ──
story.append(Paragraph("Why This Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives her dedicated operational leadership instead of carrying every decision herself."))
story.append(bd("Builds the delegation plan that lets client relationships survive without her in the room."))
story.append(bd("Turns her file-level profitability insight into a trackable path toward a 4-5x sale multiple."))

story.append(Paragraph("<b>FCOO Advisor  |  $3,797/mo stand-alone</b>", S["subsection"]))
story.append(b("Sold stand-alone per Nick's locked decision — no marketing package attached this round."))
story.append(b("Revenue (~$1.3M) clears the $1M+ band and the $2,497/mo minimum MRR floor."))
story.append(b("At $3,797/mo, this is ~3.5% of monthly revenue — well under the 35% total-spend cap."))
story.append(b("Includes weekly group coaching, practice area masterminds, and quarterly plus annual workshops at no extra charge."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Lopez Teal — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Marketing Package (Yet) ──
story.append(Paragraph("Why No Marketing Package (Yet)", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Keeps the engagement focused on exactly what she asked about — scaling for a future sale, not lead volume."))
story.append(bd("Avoids adding spend she didn't ask for while the real blocker — owner dependence — gets fixed first."))

story.append(Paragraph("<b>Why this call is not a marketing engagement:</b>", S["subsection"]))
story.append(b("The call was explicitly framed as a consultation on scaling the firm for a future sale, not lead generation."))
story.append(b("Real lead-gen gaps exist (100% referral, no SEO, directory/NAP issues) but are Phase 3 roadmap work, not the immediate ask."))
story.append(b("Nick's locked decision: FCOO Advisor, stand-alone, no marketing bundle attached this round."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"Shouldn\'t we also be doing some marketing since referrals alone feel fragile?"', S["objection_q"]))
story.append(Paragraph("That's Phase 3, once delegation and a profit plan are in place. Adding lead generation before fixing owner-dependence would just add more work Annette has to personally carry.", S["objection_a"]))

story.append(Paragraph('"Why does this cost $3,797/mo if it\'s not bundled with anything?"', S["objection_q"]))
story.append(Paragraph("This is the stand-alone FCOO Advisor price. It already includes weekly group coaching, practice area masterminds, and quarterly plus annual workshops at no extra charge.", S["objection_a"]))

story.append(Paragraph('"How do we know this actually helps her sell the firm?"', S["objection_q"]))
story.append(Paragraph("Referral-only firms trade at a 2-3x revenue multiple versus 4-5x for diversified, institutional-client firms — Annette named that gap herself on the call. FCOO Advisor is what builds toward closing it.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>FCOO Advisor (stand-alone)</b>", S["price_main"]),
     Paragraph("$3,797/mo", S["price_main"])],
    [Paragraph("Dedicated operational leadership, plus included group coaching.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>Marketing Package</b>", S["price_main"]),
     Paragraph("Not included", S["price_main"])],
    [Paragraph("Not part of this engagement — flagged as Phase 3 roadmap work.", S["price_detail"]),
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
    "Total: $3,797/mo  |  No marketing package or ad spend included this round  |  ~3.5% of revenue (well under the 35% cap)",
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
