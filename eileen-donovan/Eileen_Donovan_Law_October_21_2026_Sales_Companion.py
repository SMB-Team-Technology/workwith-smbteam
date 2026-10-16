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
_FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Design Files", "fonts")
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

OUTPUT_PATH = "eileen-donovan/Eileen_Donovan_Law_October_21_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Eileen Donovan Law", S["title"]))
story.append(Paragraph("Sales Companion  |  October 21, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Eileen Donovan, Esq.", S["snap_value"]),
     Paragraph("~$360K gross (approx.)", S["snap_value"]),
     Paragraph("2 + drafter", S["snap_value"]),
     Paragraph("3", S["snap_value"]),
     Paragraph("Near 100%", S["snap_value"]),
     Paragraph("Scarsdale, NY", S["snap_value"])],
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
story.append(Paragraph("Eileen wants her time back and a firm she can scale and run differently, not just more cases.", S["subsection"]))

story.append(quote_block("I've spent the money to get my time back and I don't have it back."))
story.append(Spacer(1, 1))
story.append(quote_block("So I want to scale and operate differently."))
story.append(Spacer(1, 1))
story.append(quote_block("&hellip;have the remote person do more of that, and have AI do what can be done."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Her time back.</b> She has a team and still absorbs the overflow."))
story.append(bd("<b>A source beyond referrals.</b> She wants to go from six or eight a month to &ldquo;some ad spend.&rdquo;"))
story.append(bd("<b>Proof first.</b> She asked for the process, the initial outlay, and the ROI."))
story.append(bd("<b>No tire kickers.</b> She has not bought paid leads and says she hates them."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>NLBM is in the picture.</b> She pays about $1,000/mo, will not leave, and is weighing their new Westchester ad zone."))
story.append(b("<b>Fear of double paying.</b> Coaching was set aside for that reason."))
story.append(b("<b>Unsure where to start.</b> No ad history and no clear first channel."))
story.append(b("<b>Website vendor.</b> She wants out but has not made the move."))
story.append(b("<b>Thin bandwidth.</b> No receptionist, and her client services director is stretched."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Families in Westchester can finally find, trust, and call her."))
story.append(bd("She gets a first paid channel that rings her phone, without a big bet."))
story.append(bd("New clients stop depending on who happens to refer her."))

story.append(Paragraph("<b>Web + SEO Essentials ($1,997) + LSA Management Add-On ($900)  |  $2,897/mo bundled</b>", S["subsection"]))
story.append(b("Seller override (Dan, Oct 16): Essentials despite three related practice areas. One office, under $750K."))
story.append(b("Site needs a rebuild. Mobile score is 63/100, no address or phone, 4 of 5 logos broken."))
story.append(b("LSA is a lower-risk start than Google Ads. Full Service is the Phase 2 upgrade."))
story.append(b("Includes 5,000 words of content. Dan floated 10,000; extra is $0.22/word. Confirm."))

story.append(thin_rule())

# ── Why This AI Package ──
story.append(Paragraph("Why This AI Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Repeat phone and admin work starts coming off her team's plate."))
story.append(bd("She tests AI month to month, with no long-term commitment."))

story.append(Paragraph("<b>AI Workforce Pro &ndash; Starter, 1 user  |  $350/mo bundled</b>", S["subsection"]))
story.append(b("She asked for AI to &ldquo;do what can be done.&rdquo; Coaching was not asked for."))
story.append(b("1M credits per user and a weekly implementation session. Her team does the setup work."))
story.append(b("Confirm LAW delivery has launched and has capacity before sending."))
story.append(b("Fractional CTO needs $400K+ revenue. She is about $40K short today."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Donovan Law &mdash; Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This LSA Budget ──
story.append(Paragraph("Why This LSA Budget (Not Set Yet)", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("A small, controlled test of paid leads before any bigger commitment."))
story.append(bd("Real lead and cost data answers her ROI question with numbers."))

story.append(Paragraph("<b>Budget status:</b>", S["subsection"]))
story.append(b("No ad spend is in the client report. The add-on is a management fee, not media."))
story.append(b("Estate planning LSA minimum is $2,000/mo. The paid-ads floor is $3,000/mo."))
story.append(b("Suggested starting point: $3,000/mo, paid to Google. Agree the number with her."))

story.append(Paragraph("<b>Estimated return (internal only):</b>", S["subsection"]))
story.append(b("At $3,000/mo: about 38 leads x 15% close = about 6 cases x $5K = about $29K, or 9.6x."))
story.append(Paragraph("<i>Estimate only. Cold-lead close rate is untested. Do not quote this number.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How it was calculated:</b>", S["subsection"]))
story.append(b("LSA cost per lead $55&ndash;$75, midpoint $65, plus 20% cushion = $78. $3,000 / $78 = about 38 leads."))
story.append(b("Close rate 15% default. Her &ldquo;shy of 100%&rdquo; is referral-only. Case value $5,000 is her number."))
story.append(b("Aggressive case not modeled: she gave no dollar revenue goal. Essentials ad cap is $7,500."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I already pay NLBM about $1,000 a month. I don\'t want to double pay."', S["objection_q"]))
story.append(Paragraph("There is no coaching here. You told us NLBM does not do &ldquo;the Google Ads piece&rdquo; or &ldquo;the AI piece.&rdquo; This adds only what they do not.", S["objection_a"]))

story.append(Paragraph('"I hate tire kickers. What are the promises and the ROI?"', S["objection_q"]))
story.append(Paragraph("No promises. LSAs charge per lead, and you set the budget. Start small and look at 30 days of real calls and cost.", S["objection_a"]))

story.append(Paragraph('"NLBM\'s new Westchester ad zone might do the same thing."', S["objection_q"]))
story.append(Paragraph("It is offered, not signed, and she said &ldquo;they're building it as they're going.&rdquo; A fast site and a live Google profile help any channel she picks.", S["objection_a"]))

story.append(thin_rule())

# ── Before The Call ──
story.append(Paragraph("Before The Call", S["section"]))
story.append(b("Review counts unconfirmed. Verify live before the call. None are printed in the report."))
story.append(b("Her Google profile status is rep-reported. Confirm it. Also confirm the Scarsdale address (two on file)."))
story.append(b("Re-check the broken logos on her site. The vendor may fix them."))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Web + SEO Essentials</b>", S["price_main"]),
     Paragraph("$1,997/mo", S["price_main"])],
    [Paragraph("Rebuilt site, Google profile, SEO content. Add-on: Local Service Ads Management, $900/mo.", S["price_detail"]),
     Paragraph("No stand-alone discount", S["price_detail"])],
    [Paragraph("<b>Local Service Ads Management Add-On</b>", S["price_main"]),
     Paragraph("$900/mo", S["price_main"])],
    [Paragraph("Setup, Google Screened verification, ongoing lead-quality management.", S["price_detail"]),
     Paragraph("No stand-alone discount", S["price_detail"])],
    [Paragraph("<b>AI Workforce Pro &ndash; Starter (1 user)</b>", S["price_main"]),
     Paragraph("$350/mo", S["price_main"])],
    [Paragraph("Month to month. LSA media spend goes to Google, not to SMB Team.", S["price_detail"]),
     Paragraph("No stand-alone price", S["price_detail"])],
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
    "Total: $3,247/mo + LSA ad spend TBD (about $3,000 ref.)  |  No bundle savings  |  10.8%&ndash;20.8% of revenue (under 35% cap)",
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
