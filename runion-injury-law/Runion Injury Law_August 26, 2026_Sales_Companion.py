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

NOTE ON THIS DEAL: This call was scoped as a Fractional COO engagement, not a
standard marketing/coaching growth deal (see research notes CRITICAL FLAG and
section_11_workings.txt). There is no marketing package, no coaching package, and no
ad spend in this proposal — a single standalone package (FCOO Director) is
recommended. The "Why This Coaching Package" and "Why This Ad Spend" sections have
been repurposed below to reflect that single-package reality while keeping the same
layout, styles, and page structure.
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

OUTPUT_PATH = "runion-injury-law/Runion Injury Law_August 26, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Runion Injury Law", S["title"]))
story.append(Paragraph("Sales Companion  |  August 26, 2026  |  Rep: Nick Holderman", S["subtitle"]))
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
    [Paragraph("Derick Runion", S["snap_value"]),
     Paragraph("Not stated on call", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Phoenix, AZ + Albuquerque, NM", S["snap_value"])],
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
story.append(Paragraph("Derick wants out of day-to-day litigation and into the operator seat, with enough structure in place to work remotely two weeks a month.", S["subsection"]))

# NOTE: Research notes are sourced from a Fathom AI call summary, not a raw
# verbatim transcript. The lines below are the closest-to-verbatim phrases the
# summary itself puts in quotation marks — key phrases for sales context, not
# confirmed word-for-word quotes.
story.append(quote_block("Supply-constrained — marketing is ineffective and Derick's time is consumed by litigation, preventing him from implementing his own operational playbook from Process Driven."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Exit litigation, gain freedom.</b> Work remotely two weeks a month."))
story.append(bd("<b>Get back to ops and marketing.</b> His passion — not “big lit.”"))
story.append(bd("<b>See his own plan actually run.</b> He has a playbook, no one to execute it."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No operational bandwidth.</b> Litigation consumes all of his time."))
story.append(b("<b>No dedicated operator or leadership.</b> Not stated on the call — likely nonexistent."))
story.append(b("<b>Underperforming marketing.</b> SEO vendor (CAMG) producing poor results."))
story.append(b("<b>No confirmed financials.</b> Revenue and margins were not discussed."))

story.append(thin_rule())

# ── Why This Package (single product — FCOO Director standalone) ──
story.append(Paragraph("Why This Package: FCOO Director", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts a dedicated operator in the seat Derick has been trying to fill himself."))
story.append(bd("Turns the Process Driven playbook from a stalled document into an actively executed plan."))
story.append(bd("Builds the operational structure he needs before he can responsibly step back into two weeks a month remote."))

story.append(Paragraph("<b>FCOO Director  |  $5,797/mo (standalone)</b>", S["subsection"]))
story.append(b("Priced as a true standalone engagement per seller instruction (Nick, Slack 8/25/2026) — not bundled with marketing or coaching."))
story.append(b("Matches the ~$4,000/mo Fractional COO engagement structure (5/9/17 hrs/month tiers) discussed on the discovery call."))
story.append(b("FCOO Director standalone normally requires $1M+ annual revenue — not confirmed on this call. Verify with client before signature."))
story.append(b("No marketing or ad spend is included. This call was scoped as an operational engagement, not a lead-gen engagement."))

story.append(thin_rule())

# ── Independent Audit Findings (context for a later phase — not part of this ask) ──
story.append(Paragraph("Independent Audit Findings (Not Part of This Proposal)", S["section"]))
story.append(Paragraph("Real lead-gen gaps surfaced in research — Phase 2 context, not today's ask.", S["subsection"]))
story.append(b("Runion did not surface in organic search across 6 sampled Phoenix PI terms; Phillips Law Group, Zanes Law, and Lamber Goodnow consistently did."))
story.append(b("Geo-pages already exist for Albuquerque and Scottsdale but receive no paid traffic — a fast win once marketing has budget and an owner again."))
story.append(Paragraph("<i>Hold for Phase 2, once FCOO Director has freed up bandwidth and revenue is confirmed.</i>", S["disclaimer"]))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Runion Injury Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We talked about $4,000/month, not $5,797."', S["objection_q"]))
story.append(Paragraph("$5,797/mo is the standalone rate because this is not bundled with marketing or coaching. It reflects the actual scope discussed (5–17 hrs/month of operational leadership) and was confirmed by Nick via Slack on 8/25.", S["objection_a"]))

story.append(Paragraph('"We do not know our revenue — are we even eligible?"', S["objection_q"]))
story.append(Paragraph("FCOO Director standalone normally requires $1M+ annual revenue. This needs to be confirmed with the client before signature — flagged internally in package_decision.json and section_11_workings.txt.", S["objection_a"]))

story.append(Paragraph('"The audit found real marketing gaps — why isn’t marketing part of this?"', S["objection_q"]))
story.append(Paragraph("The call was explicitly scoped as a Fractional COO conversation, not a marketing audit. Recommending marketing here would ignore what the client actually asked for. The lead-gen findings are documented for a Phase 2 conversation once Derick has bandwidth freed up.", S["objection_a"]))

story.append(Paragraph('"We already pay an SEO vendor (CAMG)."', S["objection_q"]))
story.append(Paragraph("Nothing in this proposal touches that vendor relationship. Once onboarded, the FCOO Director will actually be positioned to evaluate and manage that vendor — a value-add, not a redundant spend.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>FCOO Director (Standalone)</b>", S["price_main"]),
     Paragraph("$5,797/mo", S["price_main"])],
    [Paragraph("Dedicated Fractional COO leadership, SOPs, hiring support, group coaching and workshops included.", S["price_detail"]),
     Paragraph("No bundle discount — standalone rate", S["price_detail"])],
    [Paragraph("<b>Marketing / Ad Spend</b>", S["price_main"]),
     Paragraph("Not part of this proposal", S["price_main"])],
    [Paragraph("This call was scoped as an operational engagement, not a lead-gen engagement.", S["price_detail"]),
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
    "Total: $5,797/mo  |  No bundling discount applies (standalone engagement)  |  Revenue unconfirmed — verify the 35% spend cap before signature",
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
