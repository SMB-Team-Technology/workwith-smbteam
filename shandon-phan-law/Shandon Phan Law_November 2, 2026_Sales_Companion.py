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
_FONT_DIR = "Design Files/fonts"
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

OUTPUT_PATH = "shandon-phan-law/Shandon Phan Law_November 2, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Shandon Phan Law", S["title"]))
story.append(Paragraph("Sales Companion  |  November 2, 2026  |  Rep: Michael Kopp", S["subtitle"]))
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
    [Paragraph("Shandon Phan", S["snap_value"]),
     Paragraph("~$400–500K this year (his words)", S["snap_value"]),
     Paragraph("3 people", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Houston, TX", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: A FIRM THAT LASTS", S["section"]))
story.append(Paragraph("He wants a firm that runs on systems and has value beyond his personal name. (Inferred; no personal-life motive was voiced.)", S["subsection"]))

story.append(quote_block("I should spend a lot of time on growing my business and building our system instead of just doing every low-level task myself."))
story.append(Spacer(1, 1))
story.append(quote_block("figure out how to build a system that can last."))
story.append(Spacer(1, 1))
story.append(quote_block("so that it would have institutional branding values beyond my personal name."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Systems, not tasks.</b> He wants to grow the business, not do every low-level job."))
story.append(bd("<b>A command center.</b> He wants SOPs so hired VAs know what to do."))
story.append(bd("<b>Better conversion.</b> He will raise the budget once intake is tuned."))
story.append(bd("<b>Fewer vendors.</b> He wants one simpler stack, not many tools."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>He is the only attorney.</b> Leads convert best when he handles them."))
story.append(b("<b>Training is slow.</b> A new hire takes six months to two years."))
story.append(b("<b>Few bilingual staff.</b> Vietnamese-speaking paralegals are scarce."))
story.append(b("<b>Tool sprawl.</b> Several vendors, and his automation is not yet functional."))
story.append(b("<b>Cautious budget.</b> He scaled the office down and wants low cost to start."))

story.append(thin_rule())

# ── Why This AI Workforce Package (replaces Marketing section: no marketing recommended) ──
story.append(Paragraph("Why This AI Workforce Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives him and one helper a working AI tool now, at the lowest cost to start."))
story.append(bd("Points the first skills at repeatable work like client asset inventories."))
story.append(bd("Adds a weekly session so the team learns while they build."))

story.append(Paragraph("<b>AI Workforce Pro – Starter (2 users)  |  $700/mo</b>", S["subsection"]))
story.append(b("$350 per user per month. No bundle applies and no stand-alone price exists. Never quote one."))
story.append(b("1M AI credits per user, month-to-month, plus a weekly implementation session."))
story.append(b("Seller set 2 seats in Slack on Nov 2. He never stated a seat count."))
story.append(b("Seller removed marketing and Elite Coach Plus. $700 is under the $2,497 minimum MRR."))

story.append(thin_rule())

# ── Why Fractional CTO Is Phase 2 (replaces Coaching section) ──
story.append(Paragraph("Why Fractional CTO Is Phase 2", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives him one person to lead the rollout once his team uses AI weekly."))
story.append(bd("Builds the custom workflows behind the CEO command center he described."))

story.append(Paragraph("<b>Fractional CTO Level 1  |  roadmap only, no price in the report</b>", S["subsection"]))
story.append(b("He discussed it on the call. The rep quoted about $3,800/mo; confirm before any quote."))
story.append(b("Level 1 needs $400K+ revenue. He is at or near that floor."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Shandon Phan Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Marketing or Ad Spend (replaces Ad Spend section) ──
story.append(Paragraph("Why No Marketing or Ad Spend", S["section"]))
story.append(bd("He said he is willing to raise the budget, but first needs to tune up intake."))
story.append(b("His Google Ads vendor is winding down by the end of this month or next."))
story.append(b("No ad spend, ROI table, or Block 4 in the report. Lead gen is a Phase 3 idea only."))
story.append(b("If marketing is added later: Essentials is hidden, Houston is a Tier 1 market, and a Vietnamese campaign is needed."))

story.append(thin_rule())

# ── Confirm Before The Call (internal flags) ──
story.append(Paragraph("Confirm Before The Call", S["section"]))
story.append(b("<b>Minimum MRR.</b> $700/mo is under $2,497. Seller locked it. Confirm with sales ops."))
story.append(b("<b>Seats.</b> Confirm who the two users are."))
story.append(b("<b>Delivery.</b> Confirm LAW delivery has launched and there is capacity."))
story.append(b("<b>Revenue.</b> HubSpot says $180K–$960K. He said $400K–$500K."))
story.append(b("<b>Missing data.</b> No PageSpeed, maps, ads, or live review data. Review counts unconfirmed; verify live before the call."))
story.append(b("<b>Live site.</b> A FAQ already exists, and bracketed placeholder text is still on it."))
story.append(b("<b>Names.</b> Katy Freeway vs Bellaire Blvd address, and several name and domain variants."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I already pay for too many tools."', S["objection_q"]))
story.append(Paragraph("This is month-to-month, so he can stop any time. It is the lowest-cost way to test AI on repeatable work, and about 2% of his stated revenue pace.", S["objection_a"]))

story.append(Paragraph('"I need leads, not AI."', S["objection_q"]))
story.append(Paragraph("He said intake must be tuned first. Lead gen is Phase 3, once intake converts closer to his own rate. That is his own condition.", S["objection_a"]))

story.append(Paragraph('"Why not the Fractional CTO now?"', S["objection_q"]))
story.append(Paragraph("Start small and see if the team uses AI weekly. The weekly session shows that, and the Fractional CTO is the natural Phase 2 step.", S["objection_a"]))

story.append(Paragraph('"The AI report did not reflect my firm."', S["objection_q"]))
story.append(Paragraph("He said it compared him to national firms. The report names only local Houston firms: David Nguyen, Tom Hoang, and Your Legacy Legal Care.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>AI Workforce Pro – Starter (2 users)</b>", S["price_main"]),
     Paragraph("$700/mo", S["price_main"])],
    [Paragraph("Two seats, pre-built skills, and a weekly implementation session.", S["price_detail"]),
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
]))
story.append(pt)
story.append(Paragraph(
    "Total: $700/mo  |  No bundle savings  |  1.7%–2.1% of stated revenue (under 35% cap)",
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
