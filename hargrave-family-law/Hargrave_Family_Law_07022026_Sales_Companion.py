"""
Sales Companion PDF — Hargrave Family Law
=========================================
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

DARK_NAVY = HexColor("#1a2332")
ACCENT_GREEN = HexColor("#3B6D11")
MEDIUM_GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#888888")
RULE_GRAY = HexColor("#CCCCCC")
QUOTE_BG = HexColor("#F5F7F0")
WHITE = HexColor("#FFFFFF")
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "hargrave-family-law/Hargrave_Family_Law_07022026_Sales_Companion.pdf"


def add_page_elements(canvas, doc):
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

S = {}
S["title"] = ParagraphStyle(
    "title", fontName="Helvetica-Bold", fontSize=16, leading=20,
    textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle(
    "subtitle", fontName="Helvetica", fontSize=9.5, leading=13,
    textColor=LIGHT_GRAY, spaceAfter=3)
S["section"] = ParagraphStyle(
    "section", fontName="Helvetica-Bold", fontSize=11, leading=15,
    textColor=ACCENT_GREEN, spaceBefore=5, spaceAfter=1)
S["subsection"] = ParagraphStyle(
    "subsection", fontName="Helvetica-Bold", fontSize=10, leading=13,
    textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle(
    "bullet", fontName="Helvetica", fontSize=9, leading=12,
    textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0,
    spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle(
    "bullet_dark", fontName="Helvetica", fontSize=9, leading=12,
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
    "snap_value", fontName="Helvetica", fontSize=9, leading=12,
    textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle(
    "objection_q", fontName="Helvetica-Bold", fontSize=9, leading=12,
    textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle(
    "objection_a", fontName="Helvetica", fontSize=9, leading=12,
    textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=1)
S["price_main"] = ParagraphStyle(
    "price_main", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
    textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle(
    "price_detail", fontName="Helvetica", fontSize=8.5, leading=12,
    textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle(
    "savings", fontName="Helvetica-Bold", fontSize=9, leading=12,
    textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=2)
S["disclaimer"] = ParagraphStyle(
    "disclaimer", fontName="Helvetica-Oblique", fontSize=8, leading=10,
    textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


def b(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY,
                       spaceBefore=3, spaceAfter=3)


# PAGE 1
story = []

story.append(Paragraph("Hargrave Family Law", S["title"]))
story.append(Paragraph("Sales Companion  |  July 2, 2026  |  Rep: Dan Bryant", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Jennifer Hargrave", S["snap_value"]),
     Paragraph("Unknown — est. $500K+ (verify)", S["snap_value"]),
     Paragraph("7 attorneys, 2 offices", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("Dallas &amp; McKinney, TX", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.7*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 3))

story.append(Paragraph("Dominant Buying Motive: INSTITUTION / LEGACY", S["section"]))
story.append(Paragraph("Jennifer wants Hargrave Family Law to operate as an institution — generating income and freedom without requiring her presence in every decision.", S["subsection"]))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she likely wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable pipeline.</b> A client flow that does not depend on referrals this week."))
story.append(bd("<b>Firm that runs without her.</b> Two offices and seven attorneys should enable this."))
story.append(bd("<b>Income that grows with the firm.</b> Inc. 5000 growth without a profit plan often produces bigger overhead, not bigger distributions."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is likely stopping her:</b>", S["subsection"]))
story.append(b("<b>No paid lead gen.</b> No ads observed on Google, LSA, or Meta — organic carries everything."))
story.append(b("<b>NAP inconsistency.</b> FindLaw phone (469) 423-9607 vs. website (214) 416-9433 — suppressing local rankings."))
story.append(b("<b>No transcript.</b> Revenue and goals unconfirmed — verify before finalizing package tier."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Turns 211 five-star reviews into top-of-page visibility — LSA, Google Search, and Meta launching simultaneously."))
story.append(bd("Owns the 'collaborative divorce' keyword category before competitors recognize it."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue est. $400K–$1M — Starter tier; upgrade to Growth ($6,397) if revenue confirms at $1M+."))
story.append(b("No paid ads on any channel — all four need to launch together."))
story.append(b("Website conversion gaps require website work; full service is required."))
story.append(b("Starter ad spend cap is $6,000/mo; aggressive $12,000 scenario requires tier upgrade discussion."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Builds intake protocols so increased lead volume converts — not just arrives."))
story.append(bd("Gives Jennifer a management framework to lead both offices strategically, not operationally."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Standard coaching selection for $400K–$1M revenue band."))
story.append(b("No intake process verifiable from public data — audit is day-one priority."))
story.append(b("If revenue confirms at $1M+ with 5+ dedicated staff, consider Master's Circle upgrade."))


# PAGE 2
story.append(PageBreak())

story.append(Paragraph("Hargrave Family Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Puts Hargrave at the top of Google for Dallas family law searches on every paid channel — ending organic-only dependence."))
story.append(bd("Conservative: est. 4 cases/mo. Aggressive: est. 20 cases/mo — using 211-review strength as a conversion asset."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000/mo — Family Law minimums: Google PPC $1,500 + LSA $1,000 + Meta $500."))
story.append(b("<b>Aggressive:</b> $12,000/mo — requires Growth tier upgrade (Starter cap is $6,000/mo)."))

story.append(Paragraph("<b>ROI Estimates (not guaranteed):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 25 leads / 15% close = 4 cases x $6,000 avg = $24,000/mo vs. $3,000 = 8x return."))
story.append(b("<b>Aggressive:</b> 130 leads / 15% close = 20 cases x $6,000 avg = $120,000/mo vs. $12,000 = 10x return."))
story.append(b("<b>Cap check:</b> At $500K revenue, $12K ad + $8K fees = $20K/mo = 48% (over 35% cap). At $1M it is 24% (within cap). Verify revenue."))
story.append(Paragraph("<i>CPL benchmarks: Family Law Google $75–$150, LSA $50–$100, Meta $25–$100. Case value default $6,000.</i>", S["disclaimer"]))

story.append(thin_rule())

story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"We already get referrals — why pay for ads?"', S["objection_q"]))
story.append(Paragraph("Referrals are not a system. Powell Law Offices is running paid ads for the same search terms right now. Goranson Bain Ausley has 26+ attorneys and 7 offices holding paid positions. Her 211 reviews are the asset — paid ads are how she activates it.", S["objection_a"]))

story.append(Paragraph('"How do I know the ROI estimates are realistic?"', S["objection_q"]))
story.append(Paragraph("The CPL benchmarks are SMB Team's live family law data. $6,000 avg case value is conservative for a board-certified Dallas boutique. Even at half the projected leads, conservative spend returns 4x. Results are estimates — not guarantees — built on market data.", S["objection_a"]))

story.append(Paragraph('"We don\'t have capacity for more leads right now."', S["objection_q"]))
story.append(Paragraph("Coaching fixes intake before lead volume increases. Seven attorneys across two offices is real capacity — the gap is almost always the intake process, not attorney availability. The first 90 days build the system before scaling the spend.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Search, LSA, Meta Ads, Local SEO, website optimization.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, masterminds, quarterly workshops, intake audit.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000–$12,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $3,000–$12,000 ad spend  |  Save $1,147/mo by bundling  |  VERIFY REVENUE before aggressive scenario",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
