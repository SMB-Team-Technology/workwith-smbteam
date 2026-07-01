"""
Sales Companion PDF — Umina Legal
SMB Team Internal Document — Do Not Share
Run 3 — Updated July 1, 2026: Full Service Marketing Growth + Elite Coach Plus
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
story.append(Paragraph("Sales Companion  |  June 30, 2026  |  Rep: Nick Holderman  |  Package: Growth Marketing + Elite Coach Plus", S["subtitle"]))
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
story.append(Paragraph("Ryan wants to scale to $1.5M-$2M while working ~30 hours a week — shifting from operator to owner without repeating a prior burnout.", S["subsection"]))

story.append(quote_block("I want to shift from operator to owner — the firm needs to run without me at the center of everything."))
story.append(Spacer(1, 1))
story.append(quote_block("Speed to lead is critical — I handle every call personally so we don't lose cases at first contact."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>$2M without more hours.</b> Scale revenue to the target without multiplying his personal workload."))
story.append(bd("<b>Burnout-proof systems.</b> The right infrastructure first — not more leads hitting a broken intake process."))
story.append(bd("<b>Operator-to-owner transition.</b> A trained team and delegated intake so the firm runs when he is not in it."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Single lead source.</b> One Google Ads campaign at $3K/mo — no organic floor, no LSA, no satellite market coverage."))
story.append(b("<b>Intake bottleneck.</b> Every call goes to Ryan personally — growth without delegation multiplies his load."))
story.append(b("<b>Empty review profile.</b> Slavey &amp; Shumaker has 101 Google reviews at 4.8 stars; Umina Legal has 0 confirmed."))
story.append(b("<b>No financial visibility.</b> Acknowledged bookkeeping gap, no monthly P&amp;L, no CRM tracking conversion data."))
story.append(b("<b>Burnout caution.</b> Prior scaling attempt failed — he needs structured growth, not just more ad spend."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why Full Service Marketing — Growth", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Takes marketing off Ryan's plate — professional management replaces the self-managed campaign he's running alone."))
story.append(bd("Adds satellite market campaigns for Parkersburg, Charleston, and Waynesburg — three offices, currently zero leads."))
story.append(bd("Builds the organic review infrastructure that creates a lead floor that survives when ads pause or bids increase."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $8,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1.2M ($1M-$3M range) → Growth tier. Starter was incorrect at this revenue level."))
story.append(b("PI listed on website (wrongful death, auto accidents) → minimum Starter tier; Growth exceeds requirement."))
story.append(b("Criminal Defense + high market competitiveness → Essentials tiers hidden; Growth is appropriate."))
story.append(b("Growth tier ad spend cap $15,000/mo. At aggressive $15K + $11,597 fees = 26.6% of revenue — under 35% cap."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why Elite Coach Plus", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Connects Ryan with criminal defense attorneys who have already made the operator-to-owner transition he described."))
story.append(bd("Provides weekly accountability for building the delegation and team structure that prevents the prior burnout from repeating."))
story.append(bd("Criminal defense mastermind access gives Ryan peers who understand his practice area and his exact growth challenge."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1M+ with team under 5 → Elite Coach Plus is the correct eligibility match."))
story.append(b("Master's Circle requires 5+ team members with dedicated staff — does not apply at 2-person firm."))
story.append(b("Burnout history makes coaching accountability structure critical — not optional — for safe growth."))
story.append(b("Retail stand-alone $3,497/mo — bundled saves $297/mo vs. stand-alone."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Umina Legal — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Converts existing satellite office presence into active lead pipelines — three markets, currently generating zero leads from paid search."))
story.append(bd("Builds LSA placement above paid ads — Google Screened review target makes Umina Legal the top result before competitors appear."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,500/mo — step-up from $3K adds satellite markets, LSA layer, and charge-type ad groups."))
story.append(b("<b>Aggressive:</b> $15,000/mo — Growth tier cap; full multi-channel coverage across all criminal defense search intent."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~56 leads x 15% close = 8 cases x $5K avg = $40K/mo vs. $7.5K spend = ~5x return (est.)."))
story.append(b("<b>Aggressive:</b> ~120 leads x 15% close = 18 cases x $7.5K avg = $135K/mo vs. $15K spend = ~9x return (est.)."))
story.append(Paragraph("<i>All figures are estimates using practice area defaults. Case value not stated on call. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Criminal Defense minimums: Google PPC $2,500 + LSA $1,000 + Meta Ret $1,200 + Meta Lead $1,500 = $6,200; step-up to $7,500 for satellite markets."))
story.append(b("<b>Aggressive:</b> $2M goal x 20% / 12 = $33,333. Tier 5 (0.85x) = $28,333. Minus $8,397 Growth fee = $19,936. Capped at Growth tier $15,000."))
story.append(b("Total at aggressive: $11,597 + $15,000 = $26,597/mo = 26.6% of revenue. Under the 35% cap. Clear."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"My Google Ads are already generating $100K/month. Why do I need SMB to manage them?"', S["objection_q"]))
story.append(Paragraph("Ryan's campaign is working at $3K/mo on one channel. The Growth package expands to charge-type ad groups, satellite markets (Parkersburg, Charleston, Waynesburg), LSA placement, and a website rebuild to capture organic traffic — reaching prospects the current setup misses entirely. Professional management also frees Ryan from monitoring campaigns personally.", S["objection_a"]))

story.append(Paragraph('"I burned out trying to grow before. How is this different?"', S["objection_q"]))
story.append(Paragraph("The prior burnout came from adding leads without adding systems. Elite Coach Plus builds the accountability structure and delegation framework before marketing adds more volume — coaching sets the delegation milestones, then marketing fills the pipeline that the intake coordinator handles.", S["objection_a"]))

story.append(Paragraph('"Slavey &amp; Shumaker has 101 reviews. Can we realistically catch up?"', S["objection_q"]))
story.append(Paragraph("Catching up on reviews does not require matching 101 — it requires crossing the Google Screened LSA threshold, typically 10-15 verified reviews. A systematic post-case review request program can hit that in 60-90 days, unlocking the LSA placement above Slavey & Shumaker's standard paid ads regardless of review count.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$8,397/mo", S["price_main"])],
    [Paragraph("Managed Google Ads, website rebuild, LSA launch, review gen, local SEO.", S["price_detail"]),
     Paragraph("<strike>$9,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, criminal defense mastermind, quarterly + annual workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,500–$15,000/mo", S["price_main"])],
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
    "Total: $11,597/mo + $7,500–$15,000 ad spend  |  Save $1,897/mo by bundling  |  19.1%–26.6% of revenue (under 35% cap)",
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
