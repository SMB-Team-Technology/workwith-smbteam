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

OUTPUT_PATH = "bw-law/BW Law, PLLC_August 14, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("BW Law, PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  August 14, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Sarah (Yunjuan) Bai", S["snap_value"]),
     Paragraph("~$200K (2025); goal $500K", S["snap_value"]),
     Paragraph("1 PT assistant + contractors", S["snap_value"]),
     Paragraph("4: Small Biz Mgr", S["snap_value"]),
     Paragraph("Not stated (15% default)", S["snap_value"]),
     Paragraph("Gainesville, FL", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM FROM \"CHIEF EVERYTHING OFFICER\"", S["section"]))
story.append(Paragraph("Sarah wants to stop personally reviewing every contractor's work and build a team she trusts, so she can spend her time on business development and networking instead.", S["subsection"]))

story.append(quote_block("Chief everything officer"))
story.append(Spacer(1, 1))
story.append(quote_block("Build a trusted team to delegate work and reduce personal stress"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Hit $500K without burning out.</b> Scale from ~$200K without just working more hours."))
story.append(bd("<b>Delegate real work.</b> A team she trusts enough to stop reviewing every file herself."))
story.append(bd("<b>Get her time back.</b> Room for business development and networking, not just oversight."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No hiring system.</b> Every hire depends entirely on her personal time to train and review."))
story.append(b("<b>Thin team.</b> One part-time assistant plus contractors — no one owns ops or QA."))
story.append(b("<b>No capacity plan behind $500K.</b> The revenue target exists; the team plan does not."))
story.append(b("<b>Single lead channel.</b> GBP, referrals, and networking work, but nothing adds volume on top."))

story.append(thin_rule())

# ── Why This Coaching Package (single recommended package — see note below) ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives her a structured hiring and delegation framework instead of winging it."))
story.append(bd("Group coaching with owners solving the same Stage 4 to 6 problem."))

story.append(Paragraph("<b>Coach Essentials Plus  |  $2,497/mo stand-alone</b>", S["subsection"]))
story.append(b("Revenue is under $250K on both the HubSpot estimate ($180K) and the transcript figure (~$200K) — Elite Coach's floor is $250K+, so it does not qualify. Coach Essentials Plus is the correct tier (fund verification required)."))
story.append(b("Closely matches what was proposed on the call: coaching on hiring/systems at ~$2,000/mo, which Sarah confirmed as realistic."))
story.append(b("Priced stand-alone — no marketing package is bundled in, so there is no bundled discount to show."))
story.append(b("No marketing package included: GBP/referrals/networking already work and there is no paid history to fix. Single-product by design."))

story.append(Paragraph("<b>AI Workforce Pro &ndash; Starter (1 user)  |  $350/mo</b>", S["subsection"]))
story.append(b("The exact 'AI Workforce' platform discussed on the call, sized to a single user — no revenue floor on this seat tier, unlike the 5-user AI Essentials tier."))
story.append(b("Automates intake qualification, case-update communication, and email drafting — freeing Sarah's time for hiring and business development."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("BW Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why We're Not Recommending Ads Yet ──
story.append(Paragraph("Why We're Not Recommending Ads Yet", S["section"]))

story.append(Paragraph("<b>Randy's call:</b>", S["subsection"]))
story.append(bd("BW Law is budget-conscious and is prioritizing the hiring/operations fix first — do not lead with or push ad spend on this proposal."))
story.append(bd("Revisit paid visibility in Phase 2, once hiring and delegation systems free up bandwidth to handle added lead flow."))

story.append(Paragraph("<b>Reference math only (not part of this proposal):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000/mo — Immigration Google PPC minimum, which also matches the platform's absolute floor for any paid ads."))
story.append(b("<b>Aggressive:</b> $8,300/mo — full budget aligned to the $500K revenue goal."))

story.append(Paragraph("<b>Estimated Return, if pursued later:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~3.8 cases x $4.5K avg case value = ~$17.3K/mo vs. $3.0K spend = ~5.8x return."))
story.append(b("<b>Aggressive:</b> ~12.8 cases x $4.5K avg case value = ~$57.6K/mo vs. $8.3K spend = ~6.9x return."))
story.append(Paragraph("<i>All figures are estimates using an Immigration default case value ($4,500) and 15% default close rate — neither was stated on the call. Not guaranteed, and not currently recommended.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"Why isn\'t there a marketing package here?"', S["objection_q"]))
story.append(Paragraph("She said GBP, referrals, and networking are working, and she's never run paid marketing. The call was about hiring, not lead gen. Ad spend is reference-only for a later phase, not part of this proposal.", S["objection_a"]))

story.append(Paragraph('"Is $2,497/mo really enough for the coaching?"', S["objection_q"]))
story.append(Paragraph("She independently confirmed ~$2,000/mo as realistic before we quoted a price — $2,497/mo stand-alone is close to what she already told us she's comfortable with.", S["objection_a"]))

story.append(Paragraph('"Can we do LSA/PPC too?"', S["objection_q"]))
story.append(Paragraph("Randy has committed to including LSA/PPC at no additional service fee whenever she opts in down the road — flag this as a rep concession, not a standard catalog term (standard add-on is $900/mo), so it's tracked if she takes him up on it.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Coach Essentials Plus</b>", S["price_main"]),
     Paragraph("$2,497/mo", S["price_main"])],
    [Paragraph("Coaching on hiring, systems, and workflow — the exact category discussed on the call. Stand-alone (no marketing bundle).", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>AI Workforce Pro &ndash; Starter (1 user)</b>", S["price_main"]),
     Paragraph("$350/mo", S["price_main"])],
    [Paragraph("Intake qualification, case updates, email drafting.", S["price_detail"]),
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
    "Total: $2,847/mo  |  Stand-alone pricing, no marketing bundle  |  1.4% of stated $500K goal (well under 35% cap)  |  LSA/PPC comped by Randy whenever she opts in — not shown above",
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
