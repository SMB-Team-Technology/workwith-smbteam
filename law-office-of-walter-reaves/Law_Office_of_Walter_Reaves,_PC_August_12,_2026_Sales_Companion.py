"""
Sales Companion PDF — Law Office of Walter Reaves, PC
SMB Team Internal Document — DO NOT SHARE WITH CLIENT
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

_FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
pdfmetrics.registerFont(TTFont("Poppins", os.path.join(_FONT_DIR, "Poppins-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Bold", os.path.join(_FONT_DIR, "Poppins-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Italic", os.path.join(_FONT_DIR, "Poppins-Italic.ttf")))
pdfmetrics.registerFontFamily(
    "Poppins", normal="Poppins", bold="Poppins-Bold",
    italic="Poppins-Italic", boldItalic="Poppins-Bold",
)

DARK_NAVY = HexColor("#003A59")
SECTION_BLUE = HexColor("#0091C9")
ACCENT_GREEN = HexColor("#3B6D11")
MEDIUM_GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#888888")
RULE_GRAY = HexColor("#CCCCCC")
QUOTE_BG = HexColor("#F5F7F0")
WHITE = HexColor("#FFFFFF")
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "law-office-of-walter-reaves/Law_Office_of_Walter_Reaves,_PC_August_12,_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Law Office of Walter Reaves, PC", S["title"]))
story.append(Paragraph("Sales Companion  |  August 12, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Walter Reaves", S["snap_value"]),
     Paragraph("~$250K/yr", S["snap_value"]),
     Paragraph("2 (1 PT asst.)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Waco, TX", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: STABILIZATION &amp; SURVIVAL", S["section"]))
story.append(Paragraph("Walter wants to stop the revenue bleed from a failed merger and rebuild a practice that does not depend on him personally answering every call.", S["subsection"]))

story.append(quote_block("A failed merger cut firm revenue from ~$600k to ~$250k/year, creating a budget crisis."))
story.append(Spacer(1, 1))
story.append(quote_block("Cannot manage all incoming calls — describing the part-time legal assistant's intake capacity."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Stop the bleed.</b> Rebuild toward, and past, the pre-merger ~$600K run rate."))
story.append(bd("<b>Stop personally fielding every call.</b> He + one part-time assistant field 100% of intake."))
story.append(bd("<b>AI Workforce support.</b> His original ask — see why it's Phase 3, not Phase 1."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No intake backup.</b> ~5&ndash;6 cases/month (~$20K&ndash;$24K) lost to missed/unfollowed calls."))
story.append(b("<b>No follow-up sequence.</b> Leads who don't sign on the first call aren't contacted again."))
story.append(b("<b>Revenue floor.</b> Legal AI Workforce requires $500K+ revenue &mdash; not eligible yet."))

story.append(thin_rule())

# ── Why No Marketing Package (Yet) ──
story.append(Paragraph("Why No Marketing Package (Yet)", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Keeps spend inside what the firm can sustain during a stated budget crisis."))
story.append(bd("Avoids paying for ad-driven calls before intake can convert them."))

story.append(Paragraph("<b>No Marketing Package in Phase 1  |  Deferred to Phase 2</b>", S["subsection"]))
story.append(b("package_decision.json estimated revenue at $570K (HubSpot) — corrected to the transcript's ~$250K figure."))
story.append(b("Budget-Reality Override applies: explicit budget crisis, current spend ~$800/mo."))
story.append(b("Essentials ($3,497/mo) + ad floor ($3,000/mo min) would exceed the firm's 35% cap (~$7,292/mo at $250K/yr)."))
story.append(b("LSA reactivation queued for Phase 2, once intake can convert what it generates."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Walter and the assistant a defined follow-up process instead of losing cases to gaps."))
story.append(bd("Builds the financial visibility needed to rebuild deliberately, not just react to the merger."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$250K/yr places the firm in the $250K&ndash;$400K Elite Coach band (corrected from $570K estimate)."))
story.append(b("Team size is 2 &mdash; matches Elite Coach's \"any team size\" eligibility. Clears the $2,497 minimum MRR floor."))
story.append(b("Call-Purpose Override: the call was about AI Workforce, not marketing &mdash; coaching fits the actual need."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Walter Reaves — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Ad Spend (Yet) ──
story.append(Paragraph("Why No Ad Spend (Yet)", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Nothing is spent on ads in Phase 1 — every dollar goes toward stabilizing the practice first."))
story.append(bd("Protects the firm from committing marketing dollars before intake can convert the leads they'd generate."))

story.append(Paragraph("<b>Recommended Ad Spend Range (Phase 2, not a Phase 1 ask):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $2,000/mo — reactivating the Criminal Defense LSA minimum, a channel the firm already ran."))
story.append(b("<b>Aggressive:</b> $12,000/mo — full 20%-rule/reverse-math target against the $500K revenue goal."))

story.append(Paragraph("<b>Estimated Return on Investment (estimates — not guaranteed):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~1.6 cases x $4,000 = ~$6,250/mo vs. $2,000 spend = ~3.1x return."))
story.append(b("<b>Aggressive:</b> ~10.6 cases x $4,000 = ~$42,400/mo vs. $12,000 spend = ~3.5x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Criminal Defense LSA minimum $2,000; blended CPL ~$192 (20% cushion)."))
story.append(b("<b>Aggressive:</b> $500K goal x 20% / 12 = $8,333 (Tier 4); reverse math is higher at ~$11,800, rounded to $12,000."))
story.append(b("At the $500K goal, total ($14,600/mo) = 35% of goal revenue. Not viable at today's $250K (~70%) — a future target, not a Phase 1 spend."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I called about AI Workforce — why isn\'t that in this proposal?"', S["objection_q"]))
story.append(Paragraph("LAW requires $500K+ revenue; the firm is at ~$250K. Phase 3 adds AI Essentials once eligible — the fastest legitimate path back, not a no.", S["objection_a"]))

story.append(Paragraph('"$2,600/mo feels like a lot during a budget crisis."', S["objection_q"]))
story.append(Paragraph("It's our base coaching tier, just above the $2,497 floor. The 5&ndash;6 lost cases/month (~$20K&ndash;$24K) is nearly 10x the coaching cost.", S["objection_a"]))

story.append(Paragraph('"Why isn\'t marketing part of this if competitors are pulling ahead?"', S["objection_q"]))
story.append(Paragraph("A marketing tier now ($3,497/mo + $3,000+/mo ad floor) would blow past the firm's 35% cap at $250K/yr. Phase 2 reactivates LSAs once intake can convert the calls.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly coaching, practice masterminds, intake and financial-visibility focus.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend (Phase 2)</b>", S["price_main"]),
     Paragraph("$2,000&ndash;$5,000/mo", S["price_main"])],
    [Paragraph("Goes to Google/LSA — not to SMB Team. Deferred until intake is stable.", S["price_detail"]),
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
    "Total Phase 1 MRR: $2,600/mo (no ad spend yet)  |  Save $897/mo vs. stand-alone  |  12.5% of current $250K/yr revenue (well under 35% cap)",
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
