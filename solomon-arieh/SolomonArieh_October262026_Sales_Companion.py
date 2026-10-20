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

OUTPUT_PATH = "solomon-arieh/SolomonArieh_October262026_Sales_Companion.pdf"


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

story.append(Paragraph("SOLOMON | ARIEH", S["title"]))
story.append(Paragraph("Sales Companion  |  October 26, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
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
    [Paragraph("David Keesling", S["snap_value"]),
     Paragraph("~$3M/yr (hourly)", S["snap_value"]),
     Paragraph("5 attys + ~5", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Tulsa, OK", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: LEADERSHIP", S["section"]))
story.append(Paragraph("He wants to lead on AI and get his own time back, not chase more revenue.", S["subsection"]))

story.append(quote_block("My personality is more tip of the spear, not the handle."))
story.append(Spacer(1, 1))
story.append(quote_block("If I can take overhead oversight from 20 hours a week to five hours a week because I can use efficiencies to AI, hell yes, I'm going to do that."))
story.append(Spacer(1, 1))
story.append(quote_block("To the extent that I can leave behind something better and do well for myself in the process, I'm willing to do that."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Time back.</b> Cut overhead oversight from 20 hours to 5 a week."))
story.append(bd("<b>Early-mover edge.</b> Be ahead of the game on AI, not behind it."))
story.append(bd("<b>Human-led AI.</b> Use it to supplement his people, not supplant them."))
story.append(bd("<b>Proof first.</b> Pilot in Tulsa and talk to five similar-size firms."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>AI is banned today.</b> At the firm, using it &quot;gets you fired day one.&quot;"))
story.append(b("<b>Vendor risk.</b> He asked who is behind the company and how secure it is."))
story.append(b("<b>Single point of failure.</b> He is wary of one vendor touching the financials."))
story.append(b("<b>Post-rollout value.</b> He asked what SMB Team does after implementation."))
story.append(b("<b>Pricing is unclear.</b> He said he needs to understand the pricing structure."))

story.append(thin_rule())

# ── Why This AI Implementation Package ──
story.append(Paragraph("Why This AI Implementation Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("A Fractional CTO leads the rollout, so it never lands on his desk."))
story.append(bd("His wish list of about 24 agent ideas becomes working automations, month by month."))
story.append(bd("Tulsa becomes a pilot he can judge for himself before going further."))

story.append(Paragraph("<b>Fractional CTO Level 2  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue of about $3M clears the $1M+ floor for Level 2."))
story.append(b("Level 3 needs $3M+. He said &quot;close to three,&quot; so that is unverified."))
story.append(b("Level 1 ($3,297) sits below the roughly $4,000+ range he heard on the call."))
story.append(b("Confirm the tier with Eli Gill, and confirm LAW delivery capacity first."))

story.append(thin_rule())

# ── Why No Marketing or Coaching Package ──
story.append(Paragraph("Why No Marketing or Coaching Package", S["section"]))

story.append(Paragraph("<b>What leaving them out does for him:</b>", S["subsection"]))
story.append(bd("The proposal stays on what he asked for, which builds trust."))
story.append(bd("We do not sell him a gap he told us he does not have."))

story.append(Paragraph("<b>Marketing + Coaching  |  Not recommended</b>", S["subsection"]))
story.append(b("The call was about AI. He said, &quot;I am not in need for something different. My life is good.&quot;"))
story.append(b("The pipeline picked Elite Coach Plus from a stale HubSpot band ($570K, team of 3)."))
story.append(b("The transcript shows about $3M and about 10 staff, and no coaching need."))
story.append(b("The 1-seat AI Workforce Pro Starter pick was also dropped. Seat count is unconfirmed."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("SOLOMON | ARIEH — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Ad Spend ──
story.append(Paragraph("Why No Ad Spend", S["section"]))

story.append(Paragraph("<b>What skipping it does for him:</b>", S["subsection"]))
story.append(bd("No ad budget to approve for a firm that is not asking for leads."))
story.append(bd("Every dollar goes to the AI work he came to talk about."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> n/a. No ads package is part of this recommendation."))
story.append(b("<b>Aggressive:</b> n/a. Lead generation was not discussed on the call."))

story.append(Paragraph("<b>Value in his own words:</b>", S["subsection"]))
story.append(b("<b>Time:</b> oversight from 20 to 5 hours a week is 15 hours back (his estimate)."))
story.append(b("<b>Vendors:</b> he named a $6,800/mo accounting cost he would like to reduce."))
story.append(b("Do not quote his rough savings guesses back to him. They were speculative."))
story.append(Paragraph("<i>All figures are his own rough estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the package was chosen:</b>", S["subsection"]))
story.append(b("<b>Call purpose:</b> Fractional CTO and AI, not marketing, so no marketing tier applies."))
story.append(b("<b>Pricing:</b> Level 2 is $4,997 bundled, $5,797 stand-alone, $0 setup."))
story.append(b("<b>Optional:</b> AI Foundation Sprint is $5,003 one-time with Level 2. Not in the report."))
story.append(b("<b>Cap check:</b> $4,997 is about 2.0% of roughly $250K monthly revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I need to know about pricing structure."', S["objection_q"]))
story.append(Paragraph("Walk through Level 2: $4,997/mo bundled, $5,797 stand-alone, no setup fee. Each month has set limits on sessions, skills and automations.", S["objection_a"]))

story.append(Paragraph('"What value does SMB have post-implementation?"', S["objection_q"]))
story.append(Paragraph("The Fractional CTO continues monthly: sessions, up to 4 skills, up to 2 automations. You said the first 12 months are heavier, then lighter. Define &quot;lighter&quot; before the call.", S["objection_a"]))

story.append(Paragraph('"I may just decide there are other vendors that are better."', S["objection_q"]))
story.append(Paragraph("He wants vendor longevity and proof at similar-size firms. Bring Eli Gill and line up references, but do not promise five until they are approved.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Fractional CTO Level 2</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("Dedicated Fractional CTO leading the Tulsa AI rollout.", S["price_detail"]),
     Paragraph("<strike>$5,797</strike> stand alone", S["price_detail"])],
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
    "Total: $4,997/mo  |  Save $800/mo by bundling  |  About 2.0% of monthly revenue (under 35% cap)",
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
