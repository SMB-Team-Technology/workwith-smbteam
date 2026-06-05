"""
Sales Companion PDF — Indiana Immigration Attorneys
Internal use only. Do not share with prospect.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)

# ── Colors — DO NOT MODIFY ──
DARK_NAVY = HexColor("#1a2332")
ACCENT_GREEN = HexColor("#3B6D11")
MEDIUM_GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#888888")
RULE_GRAY = HexColor("#CCCCCC")
QUOTE_BG = HexColor("#F5F7F0")
WHITE = HexColor("#FFFFFF")
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "indiana-immigration-attorneys/IndianaImmigrationAttorneys_June5_2026_Sales_Companion.pdf"


def add_page_elements(canvas, doc):
    """Draws red warning header and confidential footer on every page. DO NOT MODIFY."""
    canvas.saveState()
    width, height = letter
    canvas.setFont("Helvetica-Bold", 10)
    canvas.setFillColor(RED_WARNING)
    canvas.drawCentredString(width / 2, height - 0.38 * inch,
                             "FOR INTERNAL USE ONLY; DO NOT SHARE.")
    canvas.setStrokeColor(RED_WARNING)
    canvas.setLineWidth(0.5)
    canvas.line(0.6 * inch, height - 0.44 * inch,
                width - 0.6 * inch, height - 0.44 * inch)
    canvas.setFont("Helvetica", 7)
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
    "title", fontName="Helvetica-Bold", fontSize=16, leading=20,
    textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle(
    "subtitle", fontName="Helvetica", fontSize=9.5, leading=13,
    textColor=LIGHT_GRAY, spaceAfter=3)
S["section"] = ParagraphStyle(
    "section", fontName="Helvetica-Bold", fontSize=11, leading=15,
    textColor=ACCENT_GREEN, spaceBefore=6, spaceAfter=2)
S["subsection"] = ParagraphStyle(
    "subsection", fontName="Helvetica-Bold", fontSize=10, leading=13,
    textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle(
    "bullet", fontName="Helvetica", fontSize=9.5, leading=13,
    textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0,
    spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle(
    "bullet_dark", fontName="Helvetica", fontSize=9.5, leading=13,
    textColor=DARK_NAVY, leftIndent=12, bulletIndent=0,
    spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle(
    "quote", fontName="Helvetica-Oblique", fontSize=9.5, leading=13,
    textColor=DARK_NAVY, leftIndent=6, rightIndent=6,
    spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle(
    "snap_label", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
    textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle(
    "snap_value", fontName="Helvetica", fontSize=9.5, leading=12,
    textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle(
    "objection_q", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
    textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle(
    "objection_a", fontName="Helvetica", fontSize=9.5, leading=13,
    textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle(
    "price_main", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
    textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle(
    "price_detail", fontName="Helvetica", fontSize=8.5, leading=12,
    textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle(
    "savings", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
    textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle(
    "disclaimer", fontName="Helvetica-Oblique", fontSize=8.5, leading=11,
    textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


# ── Helpers — DO NOT MODIFY ──
def b(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY,
                       spaceBefore=3, spaceAfter=3)

def quote_block(text):
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

story.append(Paragraph("Indiana Immigration Attorneys", S["title"]))
story.append(Paragraph("Sales Companion  |  June 5, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Libby Nelson", S["snap_value"]),
     Paragraph("Est. $150K–$350K (verify)", S["snap_value"]),
     Paragraph("2 (atty + interpreter)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Logansport, IN", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: MISSION &amp; SUSTAINABILITY", S["section"]))
story.append(Paragraph("Libby came back to Logansport to serve her community — she wants a firm that makes that mission financially sustainable for decades.", S["subsection"]))

# No direct transcript quotes available — noting research-based signals instead
story.append(quote_block("I truly believe I was given these gifts or talents and the best way to use them is to help others."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Community trust.</b> To be the go-to immigration attorney for north Indiana — the name families say without hesitation."))
story.append(bd("<b>Sustainable mission.</b> A firm generating reliable income so she can serve her community for decades, not just years."))
story.append(bd("<b>Time back.</b> Stop handling every intake call personally — focus on the legal work that actually needs her."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No paid lead generation.</b> Relies on Facebook and word-of-mouth — no predictable system."))
story.append(b("<b>Invisible online.</b> 16 reviews vs. 105–792 for Indianapolis competitors — losing the search battle."))
story.append(b("<b>No intake structure.</b> 2-person team; Libby handles all consultations — bottleneck grows with lead volume."))
story.append(b("<b>Revenue not confirmed.</b> No transcript — verify revenue, close rate, and avg case value on the call."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Turns the vacant north Indiana paid search market into a predictable lead flow — stops depending on who Libby knows."))
story.append(bd("Spanish-language campaigns reach the bilingual community she built the firm to serve — near-zero local ad competition."))

story.append(Paragraph("<b>Full Service Marketing — Essentials  |  $2,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue est. $150K–$350K — Essentials appropriate; upgrade to Starter if Jacob confirms $400K+."))
story.append(b("35% cap: $6,997 total at $3K ad spend = 33.6% of $250K annual revenue — within cap."))
story.append(b("Near-zero local paid competition — lower CPL than most immigration markets in Indiana."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Intake systems and accountability to stop being the bottleneck to every client's first experience with the firm."))
story.append(bd("Peer community of attorneys navigating Stage 3-to-6 — she is not building this alone."))

story.append(Paragraph("<b>Elite Coach  |  $1,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $250K–$400K — Elite Coach is the correct tier. Stand-alone $2,497/mo; saves $897/mo bundled."))
story.append(b("No FCOO/FCFO at this revenue level (under $500K). Phase 2 adds FCOO once firm hits $500K."))
story.append(b("Focus: intake protocols, hiring readiness, financial visibility — the Stage 3 priorities."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Indiana Immigration Attorneys — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("IIA is the only local firm showing up in paid search — every dollar faces near-zero local competition, meaning lower CPL than a metro market."))
story.append(bd("Spanish-language ads reach the Hispanic manufacturing community no competitor is targeting today."))

story.append(Paragraph("<b>Recommended Range &amp; ROI (estimates — verify case value on call):</b>", S["subsection"]))
story.append(b("<b>Conservative $3,000/mo:</b> ~4 cases x $3,500 = ~$14,000 revenue. ~4.7x return. Within Essentials $3,500 cap."))
story.append(b("<b>Aggressive $7,000/mo:</b> ~10 cases x $3,500 = ~$35,000 revenue. ~5x return. Above cap — discuss Starter upgrade or 10% overage."))
story.append(b("<b>How calculated:</b> Conservative = immigration minimums x 1.33 Spanish. Aggressive = 2x rev goal x 20% / 12 x Tier 4 geo x 1.33 Spanish minus fee."))
story.append(Paragraph("<i>Estimates only. Not guaranteed.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"Am I too early — only 13 months old?"', S["objection_q"]))
story.append(Paragraph("Flora Legal Group already has 406 reviews and geo-targeted Indiana pages. The question is whether IIA claims north Indiana first or plays catch-up after a competitor does.", S["objection_a"]))

story.append(Paragraph('"I don\'t know my revenue — how do I know I can afford this?"', S["objection_q"]))
story.append(Paragraph("Essentials at $3,997/mo meets the 35% cap at $250K annual revenue. Conservative ad ROI covers the investment in 1-2 cases per month.", S["objection_a"]))

story.append(Paragraph('"I can\'t handle more leads — I\'m the only attorney."', S["objection_q"]))
story.append(Paragraph("That is the intake problem, not a marketing problem. Elite Coach establishes intake protocols first so lead volume is captured by a system, not Libby personally.", S["objection_a"]))

story.append(Paragraph('"No local competitors — why the urgency?"', S["objection_q"]))
story.append(Paragraph("Flora Legal (406 reviews), Banks &amp; Brower (792), and Carolyn Grimes (105) are virtual competitors winning north Indiana searches today. IIA has 16 reviews and no ads.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Essentials</b>", S["price_main"]),
     Paragraph("$2,397/mo", S["price_main"])],
    [Paragraph("Paid Google Search, GBP, Spanish-language Facebook/Instagram, LSA, website optimization.", S["price_detail"]),
     Paragraph("Stand-alone: N/A", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$1,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, immigration mastermind, quarterly workshops, annual in-person event.", S["price_detail"]),
     Paragraph("<strike>$2,497</strike> stand-alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000–$7,000/mo", S["price_main"])],
    [Paragraph("Goes to Google, LSA, and Meta — not to SMB Team.", S["price_detail"]),
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
    "Total SMB fees: $3,997/mo + $3,000–$7,000 ad spend  |  Save $897/mo by bundling  |  33.6% of revenue at $250K (within 35% cap)",
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
