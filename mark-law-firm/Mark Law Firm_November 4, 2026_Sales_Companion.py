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

OUTPUT_PATH = "mark-law-firm/Mark Law Firm_November 4, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Mark Law Firm (Michael A. Mark Law Firm, LLC)", S["title"]))
story.append(Paragraph("Sales Companion  |  November 4, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Michael A. Mark, Esq.", S["snap_value"]),
     Paragraph("Not stated (HubSpot: $0–$250K)", S["snap_value"]),
     Paragraph("2 (solo + part-time helper)", S["snap_value"]),
     Paragraph("3: Solo", S["snap_value"]),
     Paragraph("Not stated (15% default)", S["snap_value"]),
     Paragraph("Ringwood, NJ (home office)", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: BEING PAID WHAT HIS EXPERIENCE IS WORTH", S["section"]))
story.append(Paragraph("He wants $2–4M a year and wants to stop doing $10-an-hour work himself.", S["subsection"]))

story.append(quote_block("I don't think it's unreasonable for me and my position with my experience to be making, you know, conservatively $2 to $4 million a year. (00:16:06)"))
story.append(Spacer(1, 1))
story.append(quote_block("When we hang up, I have to go make photocopies, and I have to stuff a couple of envelopes… $10 an hour… I shouldn't be doing that. (00:50:35)"))
story.append(Spacer(1, 1))
story.append(quote_block("I don't know how to get there, though, Jacob. (00:10:04)"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>$2–4M a year.</b> He calls it a reasonable goal for a 41-year trial attorney."))
story.append(bd("<b>Fewer low-value tasks.</b> He wants his time on work that bills at $500 an hour."))
story.append(bd("<b>More of the work he likes.</b> Municipal court and probate litigation close faster and pay sooner."))
story.append(bd("<b>A plan.</b> He is sure of the goal but not sure how to reach it."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>He is the whole team.</b> About 100 tasks sit on his calendar across roughly 20 files."))
story.append(b("<b>Calls go unanswered.</b> Six or seven silent voicemails in one week, and no intake process."))
story.append(b("<b>No marketing at all.</b> In his words: \"I don't do any marketing, none.\""))
story.append(b("<b>Very cost sensitive.</b> He hesitates on new subscriptions and walked away from a ~$7,000/mo pitch years ago."))
story.append(b("<b>Messy online footprint.</b> Mismatched addresses, two domains, and split review listings."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns his $2–4M goal into a plan with steps, so he is no longer guessing how to get there."))
story.append(bd("Shows him how to hand off the photocopies and envelopes, so his hours go to billable work."))
story.append(bd("Gives him a defined intake process so a $50–60K will contest is not lost to voicemail."))

story.append(Paragraph("<b>Elite Coach  |  $3,497/mo stand-alone</b>", S["subsection"]))
story.append(b("Seller override: marketing and AI Workforce Pro were dropped; Elite Coach alone."))
story.append(b("One product only, so no bundle. He pays the stand-alone price of $3,497, with no savings."))
story.append(b("Includes weekly group coaching, practice area masterminds, virtual quarterly workshops, one annual in-person workshop."))
story.append(b("Revenue is unverified (HubSpot band $0–$250K). Confirm he can fund 4 months of services."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Mark Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why No Marketing or Ad Spend Yet", S["section"]))
story.append(Paragraph("<b>What it means for him:</b>", S["subsection"]))
story.append(bd("Money goes first to catching the calls he already gets, before paying for more."))
story.append(bd("Marketing becomes a later step once coaching and intake are in place."))
story.append(Paragraph("<b>Why the report has no ad spend or ROI:</b>", S["subsection"]))
story.append(b("This was a coaching and operations call, not a marketing call, and the seller removed marketing."))
story.append(b("The lead-gen gap is real: no marketing, and he did not appear in the non-branded searches we ran."))
story.append(b("Ads would waste money while calls reach voicemail. Fix intake first, then revisit marketing."))
story.append(b("Later steps (FCOO, FCFO, bookkeeping, AI) depend on revenue reaching $500K+ and are not recommended now."))
story.append(Paragraph("<b>Check before the call:</b>", S["subsection"]))
story.append(b("<b>Review counts are unconfirmed.</b> The report has no review numbers. Do not quote any.")) 
story.append(b("<b>PageSpeed was not obtained.</b> Run it live if you want a score. None is in the report."))
story.append(b("<b>Under $300K needs scoping approval.</b> Revenue was never stated on the call."))
story.append(b("<b>AI Workforce Pro ($350/user/mo) was demoed.</b> It is not in this proposal. Be ready if he asks."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"You said around $2,500 a month. This is more."', S["objection_q"]))
story.append(Paragraph("You said smaller programs start \"right around $2,500\" (00:52:24). Elite Coach is $3,497 stand-alone. Coach Essentials Plus is $2,497 stand-alone if he needs a lower option. Confirm with the sales lead first.", S["objection_a"]))

story.append(Paragraph('"I\'m very, very cost sensitive."', S["objection_q"]))
story.append(Paragraph("At his own $500-an-hour rate, about 7 billable hours a month covers $3,497. He also said hiring means $50,000–$90,000 a year (00:09:12). This is an estimate, not a promise.", S["objection_a"]))

story.append(Paragraph('"Your pitch was close to $7,000 a month. That was a turnoff."', S["objection_q"]))
story.append(Paragraph("That was the old seminar-era program (00:03:47). You told him this plan is \"not $7,500 a month by any means\" (00:30:00). Today it is $3,497, about half.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$3,497/mo", S["price_main"])],
    [Paragraph("Coaching for a solo trial attorney. One product, so no bundle.", S["price_detail"]),
     Paragraph("stand-alone price", S["price_detail"])],
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
    "Total: $3,497/mo  |  No bundle savings  |  16.8% of $250K (top of HubSpot band; revenue unconfirmed), under 35% cap",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
