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

OUTPUT_PATH = "quesada/Quesada_Law_Firm_August_14_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Quesada Law Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  August 14, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Marco Quesada", S["snap_value"]),
     Paragraph("~$700K/yr", S["snap_value"]),
     Paragraph("3 total", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Miami, FL", S["snap_value"])],
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
story.append(Paragraph("Marco wants a firm that runs without him so he can reclaim personal time — and eventually transition out of law entirely.", S["subsection"]))

story.append(quote_block("Build a 'well-oiled machine' that can operate without the owner's daily involvement, enabling him to eventually transition out of law."))
story.append(Spacer(1, 1))
story.append(quote_block("Increase personal time and presence outside the firm."))
story.append(Spacer(1, 1))
story.append(quote_block("a plateau maintained for the last three years"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Time back.</b> A firm that runs without his daily presence."))
story.append(bd("<b>An eventual exit.</b> Long-term goal is to transition out of law."))
story.append(bd("<b>Predictable growth.</b> Break the plateau, hit $1,000,000."))
story.append(bd("<b>AI-led scale.</b> Automate rather than hire a large team."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>He is the intake system.</b> Every call runs through Marco."))
story.append(b("<b>Zero paid marketing history.</b> 100% referral acquisition."))
story.append(b("<b>Invisible in search.</b> Mirer (306) and Hernandez (203 reviews) dominate."))
story.append(b("<b>Solo-built automation.</b> No dedicated technical lead yet."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("First predictable lead source not dependent on referrals."))
story.append(bd("Closes the visibility gap against Mirer, Hernandez, Wichman."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("~$700K revenue + multiple practice areas both point to Starter; Essentials excluded on both grounds."))
story.append(b("Sequenced as Phase 2 — after intake capacity, matching Marco's own plan."))
story.append(b("Stand-alone $5,697/mo — bundling saves $700/mo."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Delegates intake off Marco's plate — his own stated Phase 1 priority."))
story.append(bd("Builds accountability structure before adding lead volume."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Corrected ~$700K revenue maps to Elite Coach Plus, not the $250K–$400K Elite Coach tier package_decision.json used."))
story.append(b("Includes weekly coaching, masterminds, quarterly workshops."))
story.append(b("Stand-alone $3,497/mo — bundling saves $297/mo."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Quesada Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns 20 years of credibility into inbound search traffic."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,500/mo — Google Search only, Criminal Defense PPC minimum."))
story.append(b("<b>Aggressive:</b> $20,000/mo — multi-channel, capped at Starter tier ceiling."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 3.8 cases x $4K = $15.3K/mo vs. $5.5K spend = 2.8x return."))
story.append(b("<b>Aggressive:</b> 20.5 cases x $4K = $82K/mo vs. $20K spend = 4.1x return."))
story.append(Paragraph("<i>Uses $4,000 default case value and 15% default close rate — neither stated on call. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("Conservative: PPC min $5,500 ÷ $216 blended CPL (with cushion) ≈ 25.5 leads."))
story.append(b("Aggressive: capped at Starter's $20K ceiling — $700K revenue is below the $1M Growth-tier floor needed to go higher (Boundary Rule)."))
story.append(b("Aggressive ~$82K/mo closely validates the reverse-math target for the client's $1M goal — a strong consistency signal."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We\'ve never needed to advertise — referrals work fine."', S["objection_q"]))
story.append(Paragraph("That's why revenue has plateaued at ~$700K for 3 years. Mirer (306) and Hernandez (203 reviews) dominate searches Quesada doesn't appear in at all.", S["objection_a"]))

story.append(Paragraph('"I want to automate with AI myself."', S["objection_q"]))
story.append(Paragraph("Marco is already building this solo alongside a full caseload. Fractional CTO L1 accelerates what he started — it doesn't replace it.", S["objection_a"]))

story.append(Paragraph('"Three packages feels like a lot at once."', S["objection_q"]))
story.append(Paragraph("Mirrors Marco's own 3-phase plan from the call: capacity, then leads, then automation — launched in that sequence, not all at once.", S["objection_a"]))

story.append(Paragraph('"Can ads alone hit $1,000,000?"', S["objection_q"]))
story.append(Paragraph("Not alone — flag for paid ads team review. Aggressive ads get to ~$984K/yr; referrals stay part of the mix to fully clear $1M.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("Google/Meta ads, LSA, GBP, website & local SEO.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, masterminds, intake framework.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Fractional CTO Level 1</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Dedicated CTO, Claude Enterprise, AI Skills.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,500–$20,000/mo", S["price_main"])],
    [Paragraph("Goes to Google, LSA, and Meta — not SMB Team.", S["price_detail"]),
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
    "Total: $11,494/mo + $5,500–$20,000 ad spend  |  Save $1,497/mo by bundling  |  2.4%–4.5% of revenue (under 35% cap)",
    S["savings"]))

# ── Internal Escalation Notes (sales visibility only — never client-facing) ──
story.append(Spacer(1, 2))
story.append(Paragraph("<i>Escalation flags: LAW package — confirm Fractional CTO delivery capacity. Criminal Defense in Miami (top-10 metro) — approval required. $1M goal likely exceeds ad-driven revenue alone — paid ads team review.</i>", S["disclaimer"]))

# ── Build ──
doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
