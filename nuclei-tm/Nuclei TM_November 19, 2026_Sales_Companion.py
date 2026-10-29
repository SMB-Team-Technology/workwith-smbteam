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

OUTPUT_PATH = "nuclei-tm/Nuclei TM_November 19, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Nuclei TM", S["title"]))
story.append(Paragraph("Sales Companion  |  November 19, 2026  |  Rep: Daniel Lowe", S["subtitle"]))
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
    [Paragraph("Ashley Gomes", S["snap_value"]),
     Paragraph("$200K (seller-set)", S["snap_value"]),
     Paragraph("2", S["snap_value"]),
     Paragraph("3", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("St. Augustine, FL", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: TIME BACK", S["section"]))
story.append(Paragraph("She wants the administrative work off her plate so she can grow without being the bottleneck.", S["subsection"]))

story.append(quote_block("somewhere I can take some of the administrative duties off of me"))
story.append(Spacer(1, 1))
story.append(quote_block("that is where I am looking for some escape"))
story.append(Spacer(1, 1))
story.append(quote_block("if I get more clients, I don't have enough bandwidth to address those clients"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Admin off her desk.</b> Invoicing, scanning, email, and calendar work should run without her."))
story.append(bd("<b>Room to grow.</b> She wants to serve more clients without adding her own hours."))
story.append(bd("<b>Knowledge kept in-house.</b> She wants to keep the data her contractor uses if he leaves."))
story.append(bd("<b>A low-risk start.</b> She called $350 &quot;really, really cost effective&quot; and wants a demo first."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>One-person show.</b> She has one contractor co-writer and plans to hire two more."))
story.append(b("<b>Manual billing.</b> Every invoice is built, attached, and emailed by hand."))
story.append(b("<b>Budget priorities.</b> A past marketing quote (about $3,000/mo) did not fit her financial priorities."))
story.append(b("<b>Tool fatigue.</b> She tried Claude, Gemini, and Copilot earlier and was unimpressed."))
story.append(b("<b>Fit question.</b> She is not barred in the U.S. and runs a professional services company, not a law firm."))

story.append(thin_rule())

# ── Why This AI Package ──
story.append(Paragraph("Why This AI Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Takes repeat admin work off her desk so her hours go back to petitions."))
story.append(bd("Puts her and her contractor in one shared setup, so the knowledge stays in the business."))
story.append(bd("Builds the habit of delegating to AI before she hires two more people."))

story.append(Paragraph("<b>AI Workforce Pro &ndash; Starter  |  $700/mo (2 users x $350/user)</b>", S["subsection"]))
story.append(b("The call was about AI, not marketing, and she put lead gen behind automating operations."))
story.append(b("Starter is month-to-month with 1M AI credits per user and a weekly AI Implementation Session."))
story.append(b("Rep quoted one license on the call. She floated two so her contractor can link in. Confirm seats."))
story.append(b("$700/mo is under the $2,497 minimum. The seller locked the package in Slack."))

story.append(thin_rule())

# ── What We Left Out ──
story.append(Paragraph("What We Left Out, and Why", S["section"]))
story.append(b("<b>Marketing:</b> She is short on capacity, not leads. Revisit in Phase 2 once admin is automated."))
story.append(b("<b>Coaching:</b> It was not discussed on the call. Add it only if the seller wants it."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Nuclei TM — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Ad Spend ──
story.append(Paragraph("Why No Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Frees capacity first, so the next lead is a client she can actually serve."))
story.append(bd("Keeps her spend small while she tests whether AI fits her daily work."))

story.append(Paragraph("<b>Recommended Ad Spend:</b>", S["subsection"]))
story.append(b("<b>None.</b> No marketing package is in this proposal, so there is no ad spend or ROI projection."))
story.append(b("<b>Phase 2 trigger:</b> Once admin runs on automation, she said she would like to run lead gen in parallel."))
story.append(Paragraph("<i>No projections are shown because no ads are recommended.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── Before The Call ──
story.append(Paragraph("Before The Call", S["section"]))
story.append(b("<b>Seats:</b> Confirm one or two users with Ashley before quoting $350 or $700."))
story.append(b("<b>Fit:</b> Confirm AI Workforce Pro has no limit for a non-law-firm professional services company."))
story.append(b("<b>Delivery:</b> Confirm the AI package is live and has capacity before sending."))
story.append(b("<b>Wording:</b> Do not say &quot;enterprise&quot; or &quot;enterprise-grade.&quot; The rep prefers not to."))
story.append(b("<b>Research gaps:</b> PageSpeed, Google profile, ad, and review data were not obtained. Check them live."))
story.append(b("<b>Revenue:</b> Not stated on the call. $200K is seller-set. Confirm she can fund 4 months ($2,800)."))
story.append(b("<b>Next steps she asked for:</b> a demo account, the agent-building workshop recording, and an implementation specialist on the call."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"The marketing price did not make sense for us before."', S["objection_q"]))
story.append(Paragraph("This is not that. It is $700/mo for two users, month-to-month. She called the $350 price &quot;really, really cost effective.&quot; Marketing is a later phase.", S["objection_a"]))

story.append(Paragraph('"I tried Claude, Gemini, and Copilot and was not impressed."', S["objection_q"]))
story.append(Paragraph("The weekly implementation session builds the workflows with her. She can start with a demo account and stay month-to-month.", S["objection_a"]))

story.append(Paragraph('"Does this work for a company that is not a law firm?"', S["objection_q"]))
story.append(Paragraph("The rep did not believe there is a limit but said he would confirm (00:18:23, 00:21:20). Confirm first. Do not promise it before then.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>AI Workforce Pro &ndash; Starter</b>", S["price_main"]),
     Paragraph("$700/mo", S["price_main"])],
    [Paragraph("Two users at $350/user/mo. No stand-alone price and no bundle savings apply.", S["price_detail"]),
     Paragraph("Month-to-month", S["price_detail"])],
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
    "Total: $700/mo  |  No ad spend  |  No bundle savings (single product)  |  4.2% of revenue (under 35% cap)",
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
