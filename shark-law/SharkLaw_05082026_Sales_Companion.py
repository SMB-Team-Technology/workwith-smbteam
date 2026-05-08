"""
Sales Companion PDF — Shark Law (Herzner Law, LLC)
Sales Rep: Dan Bryant
Date: May 08, 2026
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

OUTPUT_PATH = "shark-law/SharkLaw_05082026_Sales_Companion.pdf"


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

story.append(Paragraph("Shark Law (Herzner Law, LLC)", S["title"]))
story.append(Paragraph("Sales Companion  |  May 08, 2026  |  Rep: Dan Bryant", S["subtitle"]))
story.append(thin_rule())

# ── Prospect Snapshot ──
story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Avg Case Value</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Shane Herzner", S["snap_value"]),
     Paragraph("$800K pace", S["snap_value"]),
     Paragraph("4 people", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("$6,500 blended", S["snap_value"]),
     Paragraph("Cincinnati, OH", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.9*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 4))

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: FREEDOM &amp; SELECTIVITY", S["section"]))
story.append(Paragraph("Shane wants to stop doing every intake call personally and take only the DUI jury trials he wants to try.", S["subsection"]))

story.append(quote_block("Shane splits time roughly 50% admin and 50% court. He does all intakes and closing. He prefers trials but wants to choose cases and reduce routine court."))
story.append(Spacer(1, 1))
story.append(quote_block("About $700K last year. Pacing about $800K this year. Goal to surpass $1M and keep growing."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>DUI jury trials only.</b> Take only felony OVIs and high-stakes cases — not every case that calls."))
story.append(bd("<b>Remove himself from intake.</b> A firm that closes cases without him at every step."))
story.append(bd("<b>Market dominance.</b> Shark Law shows up first when Cincinnati prospects search for a DUI attorney."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Local search invisibility.</b> Shark Law ~11% of Google Maps DUI searches vs. Suhre ~96%."))
story.append(b("<b>Intake bottleneck.</b> Shane handles every consultation and every close — no delegation, no scale."))
story.append(b("<b>Speed-to-lead gap.</b> 15–20 min Scorpion notification lag; DUI clients decide in under 30 minutes."))
story.append(b("<b>NAP fragmentation.</b> Three phone numbers across directories suppress GBP authority and LSA placement."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("DUI clients searching Google find Shark Law first — closing the 89% of searches the firm is currently invisible in."))
story.append(bd("A consistent multi-channel pipeline means Shane's calendar fills with inbound DUI leads, not just whoever called a referral source this month."))
story.append(bd("Full attribution reporting ties every marketing dollar to signed cases — so Shane can make confident budget decisions based on evidence, not instinct."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $5,397/mo bundled</b>", S["subsection"]))
story.append(b("Criminal Defense in a high-competitiveness market — Essentials tier excluded; Growth required."))
story.append(b("Aggressive $1M+ goal: 20% rule yields $11,270 ad spend — exceeds Starter $5,000 cap; Growth tier required."))
story.append(b("Growth tier provides $10,000 ad spend capacity to run Google Ads, LSA, and Meta simultaneously across Cincinnati metro."))
story.append(b("Website rebuild scope needed: PageSpeed not confirmed but Scorpion sites commonly score 45–65 mobile; suburb landing pages absent."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Shane builds the intake delegation structure that removes him as the bottleneck."))
story.append(bd("Criminal defense mastermind with attorneys making the same owner-operator to firm CEO transition."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M — Elite Coach Plus is the standard recommendation at this stage."))
story.append(b("Under $1M — Master's Circle and FCOO Advisor both excluded."))
story.append(b("Shane does all intake personally — coaching framework needed to build delegation systems."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Shark Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Consistent Google Ads and LSA intake means Shane's trial calendar fills with high-value DUI cases — not whatever referrals happen to come in that month."))
story.append(bd("Meta retargeting captures website visitors who researched Shark Law and didn't call — converting warm prospects before they hire a competitor."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $4,000/mo — Criminal Defense high-competitiveness minimum across Google PPC, LSA, and Meta."))
story.append(b("<b>Aggressive:</b> $10,000/mo — Growth tier cap; full budget to compete head-to-head with Suhre across all channels."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~2 cases x $6,500 = $13,000/mo vs. $4,000 spend = 3.3x return."))
story.append(b("<b>Aggressive:</b> ~6 cases x $6,500 = $39,000/mo vs. $10,000 spend = 3.9x return."))
story.append(Paragraph("<i>All figures are estimates based on industry CPL benchmarks and 15% close rate. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Criminal Defense minimums: PPC $2,000 + LSA $1,000 + Meta Retargeting $700 + Meta Lead Gen $300 = $4,000."))
story.append(b("<b>Aggressive:</b> $1M target x 20% ÷ 12 = $16,667. Tier 4 (1.0x) = $16,667. Minus $5,397 fee = $11,270. Capped at Growth tier $10,000."))
story.append(b("Total at aggressive: $5,397 + $3,200 + $10,000 = $18,597/mo = 27.9% of revenue. Under 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I\'m already with Scorpion and it\'s been steady lately."', S["objection_q"]))
story.append(Paragraph("Suhre appears in 96% of DUI searches; Shark Law appears in 11%. \"Steady\" is not winning. Scorpion's incentive is retention — SMB Team tracks every dollar to signed cases.", S["objection_a"]))

story.append(Paragraph('"I don\'t know if the timing is right."', S["objection_q"]))
story.append(Paragraph("One additional DUI case per month covers the full SMB Team investment. The real cost is invisibility — every month Suhre widens the gap.", S["objection_a"]))

story.append(Paragraph('"I don\'t have time to manage another vendor."', S["objection_q"]))
story.append(Paragraph("Phase 1 is designed to run without Shane's time. Kickoff call plus monthly review — that is all that is required from him.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$5,397/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, website, local SEO, Meta Ads, reporting.", S["price_detail"]),
     Paragraph("<strike>$5,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, criminal defense mastermind, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$4,000–$10,000/mo", S["price_main"])],
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
    "Total: $8,597/mo + $4,000–$10,000 ad spend  |  Save $897/mo by bundling  |  12.8%–27.9% of revenue (under 35% cap)",
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
