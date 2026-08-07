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

NOTE ON THIS INSTANCE: This deal is a Coaching + Legal AI Workforce (LAW)
engagement — no marketing package, no ad spend in Phase 1 (marketing is
deliberately deferred per the transcript's own stated call-purpose override;
see section_11_workings.txt). The "Why This Marketing Package" section below
has been adapted to "Why This Coaching Package", and the "Why This Coaching
Package" section has been adapted to "Why This Legal AI Workforce Package".
The "Why This Ad Spend" section on page 2 has been adapted to "Why Marketing
Comes Later" (no ad spend exists for this Phase 1 deal). Structure, styles,
and layout are otherwise unmodified.
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

OUTPUT_PATH = "salam-associates/Salam_Associates_August 10, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Salam & Associates, P.C.", S["title"]))
story.append(Paragraph("Sales Companion  |  August 10, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Fatima Salam", S["snap_value"]),
     Paragraph("$4M hist. / ~$2M proj.", S["snap_value"]),
     Paragraph("Small, underperf.", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("N/A (15% default)", S["snap_value"]),
     Paragraph("Richardson, TX", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FIRM AUTONOMY / RETIREMENT", S["section"]))
story.append(Paragraph("Fatima wants the firm to run itself so she can retire from daily operations and run a new NGO.", S["subsection"]))

story.append(quote_block("Make the firm self-managing so Fatima Salam can retire from daily operations and run a new NGO."))
story.append(Spacer(1, 1))
story.append(quote_block("Team coaching and custom AI automation to fix operations before investing in marketing."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Step back from daily operations.</b> Stop catching every mistake on every file herself."))
story.append(bd("<b>Fix operations before marketing.</b> Coaching and AI automation first, ad spend later."))
story.append(bd("<b>Automate the repetitive work.</b> Fatima GPT, case notes, and a retention drip campaign."))
story.append(bd("<b>Eventually retire and run her NGO.</b> The end goal behind this proposal."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>She does ~75% of the work herself.</b> No accountability structure exists behind her."))
story.append(b("<b>Intake is losing ~5 cases/month (~$600K/year).</b> Slow follow-up, no after-hours coverage."))
story.append(b("<b>Revenue is in freefall.</b> $4M -> ~$2M projected, case volume ~400/yr -> ~175/yr."))
story.append(b("<b>Past marketing failed.</b> Walker, Geyser, and old Google/Facebook ads underperformed."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Builds the accountability structure the team has never had, led by Peter Schultz."))
story.append(bd("Directly matches what she asked for on the call — not a substituted product."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1M+ (current effective ~$2M) with a team under 5 matches this tier exactly."))
story.append(b("Stand-alone price is $3,497/mo — bundled saves $297/mo."))
story.append(b("Master's Circle not used: requires 5+ team with dedicated staff, which this firm lacks."))

story.append(thin_rule())

# ── Why This Legal AI Workforce Package ──
story.append(Paragraph("Why This Legal AI Workforce Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Builds the custom 'Fatima GPT' SOP assistant she asked about on the call."))
story.append(bd("Automates case notes, document tracking, and catching gaps like missing radiology bills."))

story.append(Paragraph("<b>Legal AI Workforce — Fractional CTO L2  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue band $1.5M-$3M fits current effective revenue (~$2M) and the growth goal (~$2.4M)."))
story.append(b("Multiple concurrent builds (Fatima GPT, case/doc tracking, drip campaign) match L2's cadence, not L1."))
story.append(b("Fatima has ~zero spare bandwidth — a dedicated Fractional CTO fits better than a DIY tier."))
story.append(b("Paired with the Foundation Sprint ($14,997 one-time, saves $5,000 vs. $19,997 stand-alone)."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Salam & Associates — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why Marketing Comes Later ──
story.append(Paragraph("Why Marketing Comes Later", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Protects future ad spend from leaking into the follow-up process losing ~5 cases/month today."))
story.append(bd("Matches what she asked for on the call — operations and coaching first, marketing second."))

story.append(Paragraph("<b>No Ad Spend in Phase 1:</b>", S["subsection"]))
story.append(b("$0 ad spend recommended now — marketing is a Phase 2 roadmap item, not a Phase 1 line item."))
story.append(b("Full Service Marketing — Growth ($7,497/mo) is the next tier once intake/coaching are proven."))

story.append(Paragraph("<b>Phase 2/3 Planning Reference (internal only):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $10K/mo -> ~1.8 cases/mo -> ~$13.3K/mo = 1.33x return."))
story.append(b("<b>Aggressive:</b> $50K/mo (Growth tier cap) -> ~16.6 cases/mo -> ~$124.9K/mo = 2.50x return."))
story.append(Paragraph("<i>Estimates use default close rate (15%) and case value ($7,500) — not stated on call.</i>", S["disclaimer"]))

story.append(Paragraph("<b>Escalation — confirm before proposing:</b>", S["subsection"]))
story.append(b("Confirm LAW delivery has launched and has capacity before finalizing Fractional CTO L2."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"Why coaching and AI before marketing when case volume is declining?"', S["objection_q"]))
story.append(Paragraph("Slow follow-up is already losing ~5 cases/month (~$600K/year) from leads the firm already has — new marketing spend on top of that leak would be wasted before intake is fixed.", S["objection_a"]))

story.append(Paragraph('"We tried paid ads and vendors before and they failed."', S["objection_q"]))
story.append(Paragraph("Walker, Geyser, and the 3-4-year-old Google/Facebook campaigns likely failed in part because there was no reliable intake process to convert what they generated — the same gap this proposal fixes first.", S["objection_a"]))

story.append(Paragraph('"Is $8,197/mo affordable given revenue is falling?"', S["objection_q"]))
story.append(Paragraph("$8,197/mo is about 4.9% of current effective monthly revenue (~$166,667/mo at ~$2M/yr) — well under the 35% cap even at the lower, declining revenue figure.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Full-team coaching led by Peter Schultz.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Legal AI Workforce — Fractional CTO L2</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("Fatima GPT, case/doc tracking automation, drip campaign.", S["price_detail"]),
     Paragraph("<strike>$5,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("None — deferred to Phase 2", S["price_main"])],
    [Paragraph("Marketing is a future roadmap phase, not part of this Phase 1 deal.", S["price_detail"]),
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
    "Total: $8,197/mo + $14,997 one-time  |  Save $1,097/mo + $5,000 one-time by bundling  |  ~4.9% of current monthly revenue (under 35% cap)",
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
