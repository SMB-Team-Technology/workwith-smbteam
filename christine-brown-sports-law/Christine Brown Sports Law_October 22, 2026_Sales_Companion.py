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

OUTPUT_PATH = "christine-brown-sports-law/Christine Brown Sports Law_October 22, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Christine Brown Sports Law", S["title"]))
story.append(Paragraph("Sales Companion  |  October 22, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
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
    [Paragraph("Christine Brown", S["snap_value"]),
     Paragraph("Not stated ($180K–$960K HubSpot)", S["snap_value"]),
     Paragraph("~8 (website)", S["snap_value"]),
     Paragraph("4 (provisional)", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Old Greenwich, CT", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.0*inch, 1.45*inch, 0.85*inch, 0.8*inch, 0.7*inch, 1.2*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 4))

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: NOT STATED — CONFIRM ON THE CALL", S["section"]))
story.append(Paragraph("No discovery call exists, so the report assumes a firm that runs on its team and systems so Christine gets time back.", S["subsection"]))
story.append(b("No transcript quotes are available. Everything here comes from the website, a Lighthouse run, and the seller's Slack direction."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she may want (seller framing, unverified):</b>", S["subsection"]))
story.append(bd("<b>AI help for her team.</b> The seller scoped Fractional CTO Level 1 plus 12 AI Workforce Pro seats."))
story.append(bd("<b>Operational leadership.</b> The seller calls this an FCTO and FCOO deal."))
story.append(bd("<b>A firm that runs without her.</b> The team page already shows a COO, finance manager, and attorneys."))
story.append(bd("<b>Growth without more hours.</b> Her 30 years of expertise is the product, so her time is the limit."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What may be stopping her (public signals):</b>", S["subsection"]))
story.append(b("<b>Slow website.</b> Lighthouse mobile 28/100, desktop 53/100; LCP is 19.2 seconds on mobile."))
story.append(b("<b>Intake friction.</b> Clio Grow form is linked, not embedded, and no consultation button sits above the fold."))
story.append(b("<b>Unknown baseline.</b> Revenue, fees, close rate, and profit are all unconfirmed."))
story.append(b("<b>Founder reliance.</b> Whether the team runs without her is not yet known."))
story.append(b("<b>Listing mismatch.</b> Suite 210 vs 400 and Old Greenwich vs Shelton across sources."))

story.append(thin_rule())

# ── Why This AI Package ──
story.append(Paragraph("Why This AI Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Her team gets AI doing the first pass on drafting, research summaries, and intake notes."))
story.append(bd("A Fractional CTO leads the rollout, so she does not have to manage it herself."))
story.append(bd("All 12 seats get the tools, so the capacity gain reaches the whole firm."))

story.append(Paragraph("<b>Legal AI Workforce: Fractional CTO Level 1 + AI Workforce Pro (12 users)  |  $5,734/mo bundled</b>", S["subsection"]))
story.append(b("Fractional CTO Level 1 is $3,297/mo and needs $400K+ revenue; the $570K figure is a HubSpot estimate."))
story.append(b("AI Workforce Pro: $1,597 for 5 users plus 7 x $120 = $2,437/mo. Starter caps at 4 users."))
story.append(b("AI Workforce Pro is a yearly contract and has no stand-alone price, so never quote one."))
story.append(b("Escalation: confirm LAW delivery has launched and has capacity before sending."))

story.append(thin_rule())

# ── Why This Operational Package ──
story.append(Paragraph("Why This Operational Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Her COO and finance manager get a proven law-firm operating rhythm instead of building one alone."))
story.append(bd("Decisions stop routing back to her, which is what gives her time back."))

story.append(Paragraph("<b>FCOO Advisor  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Fractional ops products need $500K+ revenue, so confirm revenue before sending."))
story.append(b("Position it as support for her existing COO, not a replacement."))
story.append(b("Includes weekly group coaching, masterminds, virtual workshops, and one in-person workshop."))
story.append(b("Both levels were inferred as the lowest tiers; the seller should confirm."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Christine Brown — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Marketing Package or Ad Spend ──
story.append(Paragraph("Why No Marketing Package or Ad Spend", S["section"]))

story.append(Paragraph("<b>What this protects for her:</b>", S["subsection"]))
story.append(bd("The proposal stays matched to the seller's FCTO and FCOO scope, with no unrequested marketing bundle."))
story.append(bd("Marketing stays open as a Phase 2 step once the AI and operations base is running."))

story.append(Paragraph("<b>Why marketing was left out:</b>", S["subsection"]))
story.append(b("The seller override in package_decision.json removed marketing and ad spend; the proposal review is locked."))
story.append(b("The lead gen findings are real, but ads, LSA, and Meta were all not observed because Google and Meta were unreachable."))
story.append(b("Review counts are unconfirmed for her and every competitor. Verify live before the call; none appear in the report."))
story.append(Paragraph("<i>Report has no Block 4 (ad spend). Block 5 is \"What We Found\" (research findings, not her words), since no transcript exists.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"Do we really need 12 AI seats?"', S["objection_q"]))
story.append(Paragraph(
    "The seat count came from the seller's note, so confirm who the 12 users are. Each seat past 5 is $120/mo, "
    "so adding or removing a seat moves the price by $120.",
    S["objection_a"]))

story.append(Paragraph('"I already have a COO. Why add an FCOO?"', S["objection_q"]))
story.append(Paragraph(
    "The FCOO supports the COO with law-firm operating playbooks, KPIs, and weekly coaching. "
    "It adds experience and accountability around the role; it does not replace anyone.",
    S["objection_a"]))

story.append(Paragraph('"Is $9,031/mo right for a firm launched in 2025?"', S["objection_q"]))
story.append(Paragraph(
    "On the $570K working estimate this is 19.0% of revenue, well under the 35% cap, and bundling saves $1,000/mo. "
    "Revenue is unconfirmed, so ask her for the real figure before defending the number.",
    S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Legal AI Workforce: Fractional CTO Level 1</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Monthly 1:1 fCTO session, up to 2 skills, and up to 1 custom automation.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Legal AI Workforce: AI Workforce Pro (12 users)</b>", S["price_main"]),
     Paragraph("$2,437/mo", S["price_main"])],
    [Paragraph("5-user base plus 7 extra users; yearly contract; weekly implementation session.", S["price_detail"]),
     Paragraph("No stand-alone price", S["price_detail"])],
    [Paragraph("<b>FCOO Advisor</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Law-firm ops leadership plus bundled group coaching and workshops.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
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
    "Total: $9,031/mo  |  Save $1,000/mo by bundling  |  19.0% of working revenue estimate (under 35% cap)  |  No ad spend recommended",
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
