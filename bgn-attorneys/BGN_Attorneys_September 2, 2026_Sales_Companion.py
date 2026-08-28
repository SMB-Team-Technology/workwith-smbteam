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
_FONT_DIR = os.path.join("Design Files", "fonts")
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

OUTPUT_PATH = "bgn-attorneys/BGN_Attorneys_September 2, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("BGN Attorneys", S["title"]))
story.append(Paragraph("Sales Companion  |  September 2, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("3 partners (Boyce, Goss, Neal)", S["snap_value"]),
     Paragraph("N/A on call", S["snap_value"]),
     Paragraph("~10 total", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Kent, WA", S["snap_value"])],
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
story.append(Paragraph("The partners want a self-managing firm that hits real personal income targets without repeating the high-churn, high-volume model they left behind.", S["subsection"]))

story.append(quote_block("not a settlement mill / churn and burn"))
story.append(Spacer(1, 1))
story.append(quote_block("100% retention so far; no employee churn to date"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What they want:</b>", S["subsection"]))
story.append(bd("<b>A firm that runs itself.</b> Operations continue without partners trapped in daily case administration."))
story.append(bd("<b>Predictable personal income.</b> $350-400K comp in year two, $500K within three years."))
story.append(bd("<b>To protect case quality at scale.</b> Explicitly rejects the high-volume settlement-mill model."))
story.append(bd("<b>A documented hiring sequence.</b> Add roles ahead of growth, not react to it."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping them:</b>", S["subsection"]))
story.append(b("<b>All three partners are hands-on.</b> Litigation, HR/IT, and intake/ops each run through one partner, no manager layer."))
story.append(b("<b>No profit plan exists.</b> Case volume/value never translated into a take-home target."))
story.append(b("<b>Growth is outpacing structure.</b> Volume is climbing toward 40-50/month faster than hiring."))
story.append(b("<b>No revenue data was tracked.</b> The call surfaced volume goals, not financial ones."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("No Marketing Package In This Proposal", S["section"]))

story.append(Paragraph("<b>What this means for them:</b>", S["subsection"]))
story.append(bd("No marketing or ad spend is included — the firm explicitly deferred that conversation to January 2027."))
story.append(bd("This keeps the engagement scoped exactly to what was discussed on the call: coaching and capacity, not lead generation."))
story.append(bd("The existing LSA agency relationship stays untouched — nothing here creates channel overlap."))

story.append(Paragraph("<b>No Marketing Package  |  Not included in this engagement</b>", S["subsection"]))
story.append(b("Call-Purpose Override applies — this was a coaching/ops call, not a marketing discovery call."))
story.append(b("Seller confirmed via Slack (2026-08-26): drop marketing, propose Elite Coach Plus only."))
story.append(b("Existing LSA agency relationship is under review; revisit marketing in Phase 3 (see roadmap)."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Gives the partners a documented hiring sequence built around the 40-50 cases/month target."))
story.append(bd("Builds a profit plan connecting case volume and case value to the $350-400K and $500K comp targets."))
story.append(bd("Creates the manager layer that finally lets Scott, Tyson, and Dan step back from daily case administration."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,497/mo standalone</b>", S["subsection"]))
story.append(b("Standalone pricing — no marketing package attached, so no bundle discount applies."))
story.append(b("~10 total headcount would normally route to Master's Circle, but the seller overrode to Elite Coach Plus standalone via Slack."))
story.append(b("Minimum revenue threshold met — HubSpot lists $3,000,000+ annual revenue."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("BGN Attorneys — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("No Ad Spend In This Proposal", S["section"]))

story.append(Paragraph("<b>What this means for them:</b>", S["subsection"]))
story.append(bd("No ad spend is recommended — marketing was intentionally excluded from this engagement per the September 2 call."))
story.append(bd("Every dollar in this proposal goes to coaching, not media spend."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Not applicable — no marketing package is included in this proposal."))
story.append(b("<b>Aggressive:</b> Not applicable — the firm has deferred the marketing conversation to January 2027."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Not applicable — no ad spend recommended in this engagement."))
story.append(b("<b>Aggressive:</b> Not applicable — no ad spend recommended in this engagement."))
story.append(Paragraph("<i>Ad spend and ROI projections do not apply to this proposal.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Not calculated — this proposal contains no marketing or ad spend line item."))
story.append(b("<b>Aggressive:</b> Not calculated — marketing was intentionally excluded per the Call-Purpose Override (see workings file)."))
story.append(b("Total spend at aggressive: N/A — 0% of revenue, since no ad spend is included."))

story.append(thin_rule())

# ── If They Push Back ──
story.append(Paragraph("If They Push Back", S["section"]))

story.append(Paragraph('"We already pay an agency for LSAs — why pay for something else?"', S["objection_q"]))
story.append(Paragraph("This proposal includes zero marketing or ad spend — it doesn't touch or duplicate the existing LSA relationship in any way. It's priced and scoped purely as coaching.", S["objection_a"]))

story.append(Paragraph('"We\'re worried about over-hiring hurting our take-home pay."', S["objection_q"]))
story.append(Paragraph("That's exactly the guardrail Elite Coach Plus is built to solve — a documented hiring sequence and profit plan turn “how many people can we afford” into a number instead of a guess.", S["objection_a"]))

story.append(Paragraph('"Marketing isn\'t something we want to talk about until 2027."', S["objection_q"]))
story.append(Paragraph("Agreed — this proposal contains no marketing or ad spend recommendation. It's scoped exactly to the coaching and capacity work discussed on this call.", S["objection_a"]))

story.append(Paragraph('"Is $3,497/month worth it without a marketing bundle?"', S["objection_q"]))
story.append(Paragraph("Because no marketing package is attached, this is the standard standalone coaching rate — there's no bundle discount to lose on a single-service engagement, and it directly funds the hiring sequence and profit plan the firm asked for.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Elite Coach Plus (Standalone)</b>", S["price_main"]),
     Paragraph("$3,497/mo", S["price_main"])],
    [Paragraph("Documented hiring sequence, capacity plan, and profit plan.", S["price_detail"]),
     Paragraph("standalone — no bundle discount", S["price_detail"])],
    [Paragraph("<b>No Marketing Package</b>", S["price_main"]),
     Paragraph("Not included", S["price_main"])],
    [Paragraph("Excluded per Call-Purpose Override — marketing deferred to Jan 2027.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("Not applicable", S["price_main"])],
    [Paragraph("Marketing intentionally excluded from this engagement.", S["price_detail"]),
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
    "Total: $3,497/mo  |  No marketing or ad spend included  |  Standalone pricing — no bundle discount applies",
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
