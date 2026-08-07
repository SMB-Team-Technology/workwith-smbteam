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
_FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "Design Files", "fonts")
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

OUTPUT_PATH = "law-offices-of-ricky-malik/Law_Offices_of_Ricky_Malik_August_11_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Law Offices of Ricky Malik, P.C.", S["title"]))
story.append(Paragraph("Sales Companion  |  August 11, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Ricky Malik", S["snap_value"]),
     Paragraph("Est. $500K–$1M*", S["snap_value"]),
     Paragraph("8", S["snap_value"]),
     Paragraph("4 (SBM)", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Manassas, VA", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.7*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Paragraph("*Transcript says \"sub-$1M plateau for years\" — overrides HubSpot's $1.98M estimate. See workings file.", S["disclaimer"]))
story.append(Spacer(1, 4))

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: FREEDOM", S["section"]))
story.append(Paragraph("Ricky wants the firm to run without him personally enforcing every SOP, so he can focus on business-level work instead of daily firefighting.", S["subsection"]))

story.append(quote_block("Ricky is the firm's bottleneck, pulled into daily minutiae by staff who fail to follow documented SOPs."))
story.append(Spacer(1, 1))
story.append(quote_block("Only 2 of 8 staff are considered 'A-players.'"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Step back from firefighting.</b> SOPs followed without him enforcing them personally."))
story.append(bd("<b>Make the associate hire count.</b> Freed-up time shouldn't get absorbed by the next fire."))
story.append(bd("<b>Grow without more chaos.</b> 15–16 to 30 retainers/mo should mean freedom, not more fires."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>SOPs exist but aren't followed.</b> Sign-offs happen; deadlines still get missed."))
story.append(b("<b>Only 2 of 8 staff are A-players.</b> High turnover from an unmet quality bar."))
story.append(b("<b>Spanish-accent intake bias.</b> Non-Hispanic callers disengage before reaching intake."))
story.append(b("<b>Zero financial visibility.</b> Can't confirm growth converts to profit."))

story.append(thin_rule())

# ── Why This Operations Package ──
story.append(Paragraph("Why This Operations Package (Not Marketing)", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts a Fractional COO in place to enforce the SOPs Ricky already wrote."))
story.append(bd("Coaching builds the 6 non-A-players into a team he can depend on."))
story.append(bd("Matches what Ricky asked about on the call — coaching + FCOO, not marketing."))

story.append(Paragraph("<b>Elite Coach Plus + FCOO Advisor  |  $5,694/mo bundled</b>", S["subsection"]))
story.append(b("Revenue overridden to est. $500K–$1M per transcript ('sub-$1M plateau') — not the $1.98M HubSpot figure."))
story.append(b("Under $1M revenue rules out Master's Circle by the eligibility table — this tier is correct."))
story.append(b("Existing SEO/Smith.ai vendor (~$5K/mo) triggers the existing-vendor override — do NOT pitch marketing."))
story.append(b("Team of 8 with only 2 A-players and a stated FCOO ask make this a genuine fit."))

story.append(thin_rule())

# ── Why This AI / Automation Package ──
story.append(Paragraph("Why This AI / Automation Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the \"Ricky GPT\" SOP-enforcement tool he already floated — without him managing the build."))
story.append(bd("A dedicated Fractional CTO leads it done-with-you, matching an owner with zero spare bandwidth."))

story.append(Paragraph("<b>Fractional CTO Level 1 (LAW)  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Revenue band ($500K–$1.5M) and 8-person staff meet LAW eligibility; owner already showed AI openness."))
story.append(b("L1 preferred over AI Essentials — Ricky has no bandwidth to manage a DIY rollout himself."))
story.append(b("Foundation Sprint paired rate ($14,997 one-time) should be scoped into kickoff now."))
story.append(b("ESCALATION: confirm LAW delivery capacity with ops before finalizing dates."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Ricky Malik — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend (Phase 2 — Not Part of This Proposal)", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Converts the firm's strongest asset — trust in the Hispanic market — into volume once the team can handle it."))
story.append(bd("Gives Ricky a lower-risk way to re-test paid channels after past PPC produced \"worthless leads.\""))

story.append(Paragraph("<b>Recommended Ad Spend Range (Phase 2):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $8,000/mo — sum of immigration channel minimums across recommended channels."))
story.append(b("<b>Aggressive:</b> $15,000/mo — roughly 3x current combined marketing spend, not a full 20%-rule scale-up."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 12 cases x $4.5K = $54K/mo vs. $8K spend = 6.8x return."))
story.append(b("<b>Aggressive:</b> 28 cases x $4.5K = $126K/mo vs. $15K spend = 8.4x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Immigration minimums: PPC $3,000 + LSA $2,000 + Meta $3,000 = $8,000."))
story.append(b("<b>Aggressive:</b> Straight 20%-rule math on a doubled revenue goal produced ~$43K/mo and 80+ cases — unrealistic for an 8-person team, so this was scaled to ~3x current spend instead."))
story.append(b("This spend is deferred to Phase 2, once coaching/FCOO has SOP compliance in place — it is not part of the Phase 1 total below."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We already tried paid ads and they didn\'t work."', S["objection_q"]))
story.append(Paragraph("Past PPC produced \"worthless leads\" per Ricky himself — an execution/targeting problem, not proof paid channels can't work. It's also moot here: no ad spend is included in this proposal.", S["objection_a"]))

story.append(Paragraph('"We already pay for SEO and Smith.ai — why do we need more?"', S["objection_q"]))
story.append(Paragraph("This proposal doesn't add another marketing vendor. It's coaching, a Fractional COO, and a Fractional CTO — the SEO/Smith.ai relationship stays untouched.", S["objection_a"]))

story.append(Paragraph('"$8,991/month feels like a lot for something that isn\'t even marketing."', S["objection_q"]))
story.append(Paragraph("At an estimated $500K–$1M revenue, that's roughly 9%–18% of monthly revenue — well under the 35% cap — aimed directly at the bottleneck Ricky named himself.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Elite Coach Plus + FCOO Advisor</b>", S["price_main"]),
     Paragraph("$5,694/mo", S["price_main"])],
    [Paragraph("Coaching + operational leadership to enforce SOPs.", S["price_detail"]),
     Paragraph("<strike>$7,294</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Fractional CTO Level 1 (LAW)</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("AI/automation to build the SOP-enforcement tool.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend (Phase 2, not now)</b>", S["price_main"]),
     Paragraph("$8,000–$15,000/mo", S["price_main"])],
    [Paragraph("Goes to Google, LSA, and Meta — deferred until Phase 2.", S["price_detail"]),
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
    "Phase 1 Total: $8,991/mo  |  Save $2,100/mo by bundling  |  ~9%–18% of estimated revenue (under 35% cap). Ad spend is a Phase 2 addition, not included above.",
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
