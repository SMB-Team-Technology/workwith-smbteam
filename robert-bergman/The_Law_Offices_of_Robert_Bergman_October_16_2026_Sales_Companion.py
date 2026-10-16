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

OUTPUT_PATH = "robert-bergman/The_Law_Offices_of_Robert_Bergman_October_16_2026_Sales_Companion.pdf"


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

story.append(Paragraph("The Law Offices of Robert Bergman", S["title"]))
story.append(Paragraph("Sales Companion  |  October 16, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Robert P. Bergman", S["snap_value"]),
     Paragraph("Not stated (HubSpot $180K-$960K)", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("3 (prelim.)", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("San Jose, CA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: NOT YET STATED", S["section"]))
story.append(Paragraph("No discovery call exists, so Robert's own motive is unknown. Ask what a more successful practice would let him do.", S["subsection"]))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What we know he wants:</b>", S["subsection"]))
story.append(bd("<b>An AI-focused conversation.</b> Per the Slack request, this call is about Fractional CTO and AI Workforce Pro, not marketing."))
story.append(bd("<b>To keep the personal service.</b> His site stresses that he drafts documents himself, not paralegals."))
story.append(bd("<b>To protect a long reputation.</b> Practicing since 1981, State Bar Certified Specialist in Estate Planning, Trust and Probate."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What may be stopping him (confirm on the call):</b>", S["subsection"]))
story.append(b("<b>Team size unknown.</b> No staff are named on the site, and LAW needs 1-2 staff to engage with rollout."))
story.append(b("<b>Revenue unknown.</b> HubSpot band is $180K-$960K; Fractional CTO Level 1 needs $400K+."))
story.append(b("<b>Possible existing vendor.</b> About one blog post per day hints at a vendor or automated content tool."))
story.append(b("<b>Slow mobile site.</b> Mobile PageSpeed is 34 (LCP 11.6 s); desktop is 84."))
story.append(b("<b>Technology comfort unknown.</b> Openness to staff training and new tools is not yet confirmed."))

story.append(thin_rule())

# ── Why This Fractional CTO Package ──
story.append(Paragraph("Why This Fractional CTO Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("A named leader owns the AI rollout so Robert does not have to manage it."))
story.append(bd("Routine firm tasks move to AI skills and automations, freeing his hours for client counsel."))
story.append(bd("A monthly automation report shows what is being saved."))

story.append(Paragraph("<b>Fractional CTO Level 1  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Stand-alone is $3,797/mo, so bundling saves $500/mo. Setup fee is $0."))
story.append(b("Includes one monthly 1:1, up to 2 extra sessions, up to 2 skills deployed, and up to 1 custom automation per month."))
story.append(b("Requires $400K+ annual revenue. Confirm actual revenue before the proposal call."))
story.append(b("Set by the seller's Slack override. If revenue is under $400K, fall back to AI Workforce Pro – Starter alone."))

story.append(thin_rule())

# ── Why This AI Workforce Pro Package ──
story.append(Paragraph("Why This AI Workforce Pro Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Robert a law-firm-ready AI workspace he can start using right away."))
story.append(bd("A weekly implementation session keeps the tools from sitting unused."))

story.append(Paragraph("<b>AI Workforce Pro – Starter (1 user)  |  $350/mo</b>", S["subsection"]))
story.append(b("Seat count is inferred. Team size is not stated, so Starter with 1 user is the default."))
story.append(b("Month-to-month, 1M AI credits per user, overages $150/mo. No stand-alone price exists; never quote one."))
story.append(b("At 5+ users, AI Workforce Pro ($1,597/mo for 5 users) becomes the better fit."))
story.append(b("Confirm LAW delivery has launched and has capacity before sending the proposal."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Robert Bergman — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Marketing Package / Ad Spend ──
story.append(Paragraph("Why No Marketing Package Or Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Keeps this proposal focused on the AI engagement he was set up to discuss."))
story.append(bd("Avoids selling marketing to a firm that may already have a vendor."))

story.append(Paragraph("<b>No Marketing Package  |  $0/mo  |  No Ad Spend</b>", S["subsection"]))
story.append(b("The seller override on 2026-10-13 replaced Full Service Marketing and Elite Coach Plus with the LAW package."))
story.append(b("No ROI projection was built because no ads package is part of this recommendation."))
story.append(b("Google Search, Maps, LSA, and Meta results could not be viewed. Ad status is unknown, not absent."))
story.append(b("35% cap check: $3,647/mo is about 8% of the $47.5K/mo implied by $570K. About 24% at the $180K low end."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I draft everything myself. I don\'t want AI near my clients\' documents."', S["objection_q"]))
story.append(Paragraph("His personal drafting is the selling point. The goal is to move routine tasks off his desk so more time goes to the work only he does.", S["objection_a"]))

story.append(Paragraph('"I am a one-person practice. Who would run this?"', S["objection_q"]))
story.append(Paragraph("The Fractional CTO runs the rollout, and the weekly session supports him. If there is no staff at all, ask before quoting. LAW assumes 1-2 staff.", S["objection_a"]))

story.append(Paragraph('"My website and content are already handled."', S["objection_q"]))
story.append(Paragraph("Agree and ask who runs it. The audit still shows 34 mobile and one call to action. This proposal does not replace his vendor.", S["objection_a"]))

story.append(Paragraph('"That is a lot per month for something I have not tried."', S["objection_q"]))
story.append(Paragraph("Bundling saves $500/mo. The AI Workforce Pro seat is month-to-month. Ask first what a week of his time is worth.", S["objection_a"]))

story.append(thin_rule())

# ── Confirm On The Call ──
story.append(Paragraph("Confirm On The Call", S["section"]))
story.append(b("<b>Review data.</b> Counts are unconfirmed and are not printed in the report. Verify live before quoting any."))
story.append(b("<b>Basics.</b> Revenue, fee structure, team, close rate, goals, and DBM were all not stated."))
story.append(b("<b>Contact details.</b> Trigger phone and email differ from the website listing."))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Fractional CTO Level 1</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Monthly Fractional CTO leadership for the AI rollout.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>AI Workforce Pro – Starter (1 user)</b>", S["price_main"]),
     Paragraph("$350/mo", S["price_main"])],
    [Paragraph("Law-firm AI workspace and weekly implementation session.", S["price_detail"]),
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
]))
story.append(pt)
story.append(Paragraph(
    "Total: $3,647/mo  |  Save $500/mo by bundling  |  About 7.7% of estimated revenue (under 35% cap)",
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
