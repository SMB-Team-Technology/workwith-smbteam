"""
Sales Companion PDF — Umina Legal
SMB Team Internal Document — Do Not Share
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

OUTPUT_PATH = "umina-legal/UminaLegal_06302026_Sales_Companion.pdf"


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

story.append(Paragraph("Umina Legal PLLC — Ryan Umina", S["title"]))
story.append(Paragraph("Sales Companion  |  June 30, 2026  |  Rep: Nick Holderman", S["subtitle"]))
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
    [Paragraph("Ryan Umina", S["snap_value"]),
     Paragraph("~$1.2M/yr", S["snap_value"]),
     Paragraph("2 people", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("~15% (est.)", S["snap_value"]),
     Paragraph("Morgantown, WV", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM WITHOUT BURNOUT", S["section"]))
story.append(Paragraph("Ryan wants to scale to $1.5M–$2M while working ~30 hours a week — shifting from operator to owner without repeating a prior burnout.", S["subsection"]))

story.append(quote_block("I want to shift from operator to owner — the firm needs to run without me handling everything."))
story.append(Spacer(1, 1))
story.append(quote_block("Speed to lead is critical — I handle every call personally so we don't lose cases at first contact."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>$2M without more hours.</b> Scale revenue without scaling his personal workload."))
story.append(bd("<b>Delegation that preserves quality.</b> Move intake off his plate without losing his standards."))
story.append(bd("<b>Burnout-proof growth.</b> Systems that protect him the way the prior attempt didn't."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Intake bottleneck.</b> Every call goes to Ryan personally — growth multiplies his load."))
story.append(b("<b>Single lead channel.</b> Google Ads only; no organic, LSA, or Meta presence."))
story.append(b("<b>No CRM.</b> Practice Panther is unusable — no pipeline or conversion visibility."))
story.append(b("<b>Weak bookkeeping.</b> Ryan can't measure real margins or ad ROI."))
story.append(b("<b>Burnout caution.</b> Prior experience makes him risk-averse — needs a plan, not just spend."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns a single $3K/mo self-managed campaign into a professionally managed multi-channel engine — more leads, less Ryan managing it."))
story.append(bd("Adds satellite market campaigns for Parkersburg, Waynesburg, and Charleston — offices he has but isn't generating leads from."))
story.append(bd("Builds the organic and LSA presence that lets him own the top of Google, not just the paid slots."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $6,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$1.2M/yr (stated on call) — falls in $1M–$3M band; Growth tier is the correct match."))
story.append(b("Criminal defense + PI practice mix; Starter is the floor for PI — Growth is the correct tier."))
story.append(b("Retail stand-alone is $6,997/mo — bundled saves $600/mo vs. stand-alone."))
story.append(b("At $25K aggressive ad spend: $6,397 + $25,000 = $31,397 = 31.4% of revenue, under the 35% cap."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Ryan the delegation framework to move intake off his plate without losing the quality he values."))
story.append(bd("Connects him with criminal defense peers who have already solved the operator-to-owner transition."))
story.append(bd("Builds the accountability and team structure that protects him from repeating the prior burnout."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M+ with team under 5 members — Elite Coach Plus is the standard recommendation."))
story.append(b("Ryan's stated goal (operator to owner) is precisely what this program is built to deliver."))
story.append(b("Retail stand-alone is $3,497/mo — bundled saves $297/mo vs. stand-alone."))
story.append(b("Includes weekly group coaching, practice area masterminds, quarterly workshops, and one annual in-person event."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Umina Legal — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("More spend with professional management converts existing market demand into cases Ryan doesn't have to personally chase."))
story.append(bd("Satellite market campaigns turn three offices with no leads into active revenue streams — no new headcount needed."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,500/mo — meaningful step up from current $3K, adds satellite markets and LSA setup."))
story.append(b("<b>Aggressive:</b> $25,000/mo — full multi-channel build across Morgantown and all satellite markets."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~16 leads x 15% close = 2–3 cases x $7K avg = ~$17,500/mo vs. $7,500 spend = ~2x return."))
story.append(b("<b>Aggressive:</b> ~62 leads x 15% close = 9–10 cases x $7K avg = ~$63,000/mo vs. $25,000 spend = ~2.5x return."))
story.append(Paragraph("<i>All figures are estimates using practice area defaults. Case value not stated on call. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Criminal Defense minimums: PPC $2,500 + LSA $1,000 + Meta $1,200 + Lead Gen $500 = $5,200 floor; $7,500 chosen to cover satellite market launch."))
story.append(b("<b>Aggressive:</b> $2M target x 20% / 12 = $33,333. Tier 4 (1.0x) = $33,333. Minus $6,397 fee = $26,936; rounded to $25,000."))
story.append(b("Total at aggressive: $9,597 + $25,000 = $34,597/mo = 34.6% of revenue — just within 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"My Google Ads are already working — why change anything?"', S["objection_q"]))
story.append(Paragraph("They work, but $3K/mo is his entire lead gen budget for a $1.2M firm. Slavey & Shumaker (10.0 Avvo, 21 reviews) holds organic and LSA slots above his paid ads. Growth tier adds multi-channel coverage and satellite market campaigns he isn't running.", S["objection_a"]))

story.append(Paragraph('"I don\'t want to grow too fast — I burned out before."', S["objection_q"]))
story.append(Paragraph("The burnout was caused by growth without systems — not by growth itself. Elite Coach Plus delivers the intake delegation framework and team structure that lets leads convert without adding to his hours. That's the structural fix he described needing.", S["objection_a"]))

story.append(Paragraph('"I\'m not sure I can trust someone else to handle intake."', S["objection_q"]))
story.append(Paragraph("That instinct is right — which is why coaching starts with building the intake coordinator role to his standards. He sets the bar; we help train someone to meet it. Every court day where no one answers the phone is a case going to Slavey & Shumaker.", S["objection_a"]))

story.append(Paragraph('"The investment feels like a lot."', S["objection_q"]))
story.append(Paragraph("At $9,597/mo, he needs 1–2 additional criminal defense cases per month to break even — realistic at conservative ad spend given his close rate. Every month without action extends competitors' directory and LSA leads.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$6,397/mo", S["price_main"])],
    [Paragraph("Google Ads, website, local SEO, LSA, Meta retargeting — all markets.", S["price_detail"]),
     Paragraph("<strike>$6,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, masterminds, intake framework, workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,500–$25,000/mo", S["price_main"])],
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
    "Total: $9,597/mo + $7,500–$25,000 ad spend  |  Save $897/mo by bundling  |  17.1%–34.6% of revenue (under 35% cap)",
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
