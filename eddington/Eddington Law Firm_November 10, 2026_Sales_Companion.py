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

OUTPUT_PATH = "eddington/Eddington Law Firm_November 10, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Eddington Law Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  November 10, 2026  |  Rep: Daniel Lowe", S["subtitle"]))
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
    [Paragraph("Wes Eddington and Adam Gleason", S["snap_value"]),
     Paragraph("~$1.98M (est.)", S["snap_value"]),
     Paragraph("~7", S["snap_value"]),
     Paragraph("4", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Denver, CO", S["snap_value"])],
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
story.append(Paragraph("A firm that runs itself so Wes and Adam can focus on growing and be away without it crumbling.", S["subsection"]))

story.append(quote_block("a perfect world and growing, we could bring in staff and at least have the faith to know that, hey, things are going to be running smoothly … if we're both not here, … the whole place isn't going to go crumbling"))
story.append(Spacer(1, 1))
story.append(quote_block("I work on vacation."))
story.append(Spacer(1, 1))
story.append(quote_block("Wes and I are doing everything."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What they want:</b>", S["subsection"]))
story.append(bd("<b>Daily fires off their plates.</b> Someone to hand tech and staff issues to."))
story.append(bd("<b>Onboarding that is streamlined.</b> The office manager will handle hiring, firing, and SOPs."))
story.append(bd("<b>A roadmap.</b> Wes: “Just a roadmap or something.”"))
story.append(bd("<b>Formal accountability.</b> Objective weekly check-ins on what is being done."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping them:</b>", S["subsection"]))
story.append(b("<b>They are in every case.</b> Both attorneys touch daily work and tech problems."))
story.append(b("<b>Tech switch in motion.</b> Moving from Clio to EVE OS. Integrations are a high priority."))
story.append(b("<b>A fresh bad experience.</b> They ended their prior part-time COO just before the call. Access has not been handed over."))
story.append(b("<b>Trial in about four weeks.</b> Wes is in trial prep. Adam is the lead contact."))
story.append(b("<b>Marketing vendor is active.</b> A rebrand and new site launch in a month or two."))

story.append(thin_rule())

# ── Why This FCOO Package (replaces Marketing section: no marketing recommended) ──
story.append(Paragraph("Why This FCOO Package", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Gives them one accountable owner for daily operations and tech issues."))
story.append(bd("Builds hiring, onboarding, and SOPs before the associates arrive."))
story.append(bd("Adds the objective weekly rhythm Adam asked for."))

story.append(Paragraph("<b>FCOO Director  |  $5,797/mo stand-alone price</b>", S["subsection"]))
story.append(b("Seller switched FCOO Advisor to FCOO Director in Slack on 11/5. The seller choice stands."))
story.append(b("Only one bundle-eligible product, so the stand-alone price applies. No bundle savings."))
story.append(b("Includes weekly group coaching, masterminds, quarterly workshops, and one annual in-person workshop."))
story.append(b("Revenue is the HubSpot range midpoint ($961K–$3M), seller-confirmed. Not stated on the call."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Eddington Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Marketing or Ad Spend (replaces Ad Spend section) ──
story.append(Paragraph("Why No Marketing or Ad Spend", S["section"]))
story.append(bd("The call was about operations. They just hired a marketing agency for a rebrand and new site."))
story.append(bd("Adam wants to stop “getting bogged down in the marketing and the daily operations.”"))
story.append(b("No ad spend, ROI table, or Block 4 in the report. No marketing package is proposed."))
story.append(b("If marketing comes up later, Denver personal injury needs approval. Marketing waits until the agency work is done."))

story.append(thin_rule())

# ── Confirm Before The Call (internal flags) ──
story.append(Paragraph("Confirm Before The Call", S["section"]))
story.append(b("<b>Revenue.</b> Never stated. $1.98M is the HubSpot midpoint. Ask for the real number."))
story.append(b("<b>Reviews.</b> All review counts and ratings are unconfirmed. Verify live before the call."))
story.append(b("<b>Missing data.</b> No PageSpeed, 3-pack, Google Ads, LSA, or Meta data was observed. Re-run for figures."))
story.append(b("<b>Site claims.</b> Site says four states, since 1984. They called themselves a small two-attorney firm. Ask."))
story.append(b("<b>FCOO or CTO.</b> You said COO first, maybe technical later. A CTO or LAW package needs delivery confirmed."))
story.append(b("<b>Handover.</b> Put access and credentials from the prior COO on the Phase 1 agenda. Keep it gentle."))
story.append(b("<b>Who joins.</b> Adam leads. The office manager should join the check-ins."))

story.append(thin_rule())

# ── If They Push Back ──
story.append(Paragraph("If They Push Back", S["section"]))

story.append(Paragraph('"Is $5,797 a month too much?"', S["objection_q"]))
story.append(Paragraph("About 3.5% of estimated monthly revenue, far under the 35% cap. Adam said “we have the capital to market,” and Wes wants to put money to work by year end.", S["objection_a"]))

story.append(Paragraph('"We tried a fractional COO. It was an endless hamster wheel."', S["objection_q"]))
story.append(Paragraph("That was part-time and not tied to deliverables. Adam said they should have kept closer tabs. This gives a roadmap and the objective weekly check-ins he asked for.", S["objection_a"]))

story.append(Paragraph('"Will you handle our tech and the EVE OS integration?"', S["objection_q"]))
story.append(Paragraph("Wes called integrations a high priority. Start with the COO owning issues. Move to a technical arrangement only if coding is needed.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>FCOO Director</b>", S["price_main"]),
     Paragraph("$5,797/mo", S["price_main"])],
    [Paragraph("Fractional COO leadership plus group coaching and workshops.", S["price_detail"]),
     Paragraph("Stand-alone price", S["price_detail"])],
]
pt = Table(price_data, colWidths=[4.5 * inch, 1.7 * inch])
pt.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 4),
    ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ("TOPPADDING", (0,0), (-1,-1), 2),
    ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(pt)
story.append(Paragraph(
    "Total: $5,797/mo  |  No bundle savings (stand-alone price)  |  3.5% of estimated revenue (under 35% cap)",
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
