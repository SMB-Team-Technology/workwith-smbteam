"""
Sales Companion PDF — SMB Team
Gilley Law (Chris Gilley) | June 18, 2026 | Rep: Nick Holderman
FOR INTERNAL USE ONLY; DO NOT SHARE.
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

OUTPUT_PATH = "gilley-law/GilleyLaw_06182026_Sales_Companion.pdf"


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

story.append(Paragraph("Gilley Law (Chris Gilley)", S["title"]))
story.append(Paragraph("Sales Companion  |  June 18, 2026  |  Rep: Nick Holderman", S["subtitle"]))
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
    [Paragraph("Chris Gilley", S["snap_value"]),
     Paragraph("$730K goal; ~$1M annualized pace", S["snap_value"]),
     Paragraph("1 (solo)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("Anderson, IN", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: TIME FREEDOM / AUTONOMY", S["section"]))
story.append(Paragraph("Chris launched Gilley Law to build a firm that runs without him — specifically to escape the 10-11 PM workdays at his previous practice.", S["subsection"]))

story.append(quote_block("A basic landing page, not built for SEO."))
story.append(Spacer(1, 1))
story.append(quote_block("Chris expressed interest in the Done For You model because he does not have bandwidth to execute marketing himself."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Autonomous firm.</b> Left his last job to build a practice that runs without him."))
story.append(bd("<b>Time back.</b> No 10-11 PM nights — non-negotiable after the previous firm."))
story.append(bd("<b>Done-For-You execution.</b> Lacks bandwidth to manage marketing; wants a team to own it."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Solo operation.</b> Only person in the firm — every intake call and case runs through him."))
story.append(b("<b>One paid channel.</b> LSAs at $6K/month alone cannot hold against multi-channel competitors."))
story.append(b("<b>No organic presence.</b> Landing page cannot rank; 100% of traffic is paid or direct."))
story.append(b("<b>Intake bottleneck.</b> Missed after-hours calls = paid LSA leads lost before any conversation."))
story.append(b("<b>7 NAP errors.</b> Yellow Pages links to old firm; suppressing GBP trust signals."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Takes all marketing off his plate — website, PPC, LSA, Meta — Done For You as requested."))
story.append(bd("Builds an SEO website that generates organic leads while Chris is in court, not at a desk."))
story.append(bd("Adds PPC and Meta to counter Eskew Law and Banks &amp; Brower, bidding for his keywords unopposed."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("$730K stated goal sits in $400K-$1M Starter range; $1M annualized pace is 2.5 weeks of data."))
story.append(b("Website rebuild required: current landing page has zero organic search capability."))
story.append(b("Both practice areas (criminal 40%, family 60%) need PPC, LSA, and Meta coverage."))
story.append(b("Starter cap $8,000/mo covers full multi-channel deployment for both practice areas."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Designs intake so paid leads convert without Chris answering every call personally."))
story.append(bd("Builds financial tracking (P&amp;L, cost per case, $730K goal) so revenue becomes real wealth."))
story.append(bd("Provides accountability structure to move Gilley Law from solo practice to self-managing firm."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K-$1M, solo team: Elite Coach Plus is the correct tier per eligibility rules."))
story.append(b("New firm needs intake design, team-building roadmap, and financial baseline from day one."))
story.append(b("Group coaching gives Chris peer exposure at criminal defense and family law growth stages."))
story.append(b("No FCOO/FCFO: team size is 1; fractional ops not appropriate until team grows."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Gilley Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Creates a managed, multi-channel lead flow so new cases arrive without Chris making calls or attending events."))
story.append(bd("Optimizes the $6K/mo already spent on self-managed LSAs — adds PPC and Meta to produce more cases per dollar."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,500/mo — criminal defense PPC $1,500 + LSA $1,000; family law PPC $1,500 + LSA $1,000; Meta retargeting $500."))
story.append(b("<b>Aggressive:</b> $8,000/mo — Starter tier cap; adds Meta lead gen and expanded 5-county geographic targeting."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~6 cases x $2,200 blended = ~$13,200/mo vs. $5,500 spend = 2.4x return. (Estimate only.)"))
story.append(b("<b>Aggressive:</b> ~11 cases x $2,200 blended = ~$24,200/mo vs. $8,000 spend = 3.0x return. (Estimate only.)"))
story.append(Paragraph("<i>All figures are estimates based on 15% default close rate and blended criminal/family case values. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Channel minimums — criminal PPC $1,500 + LSA $1,000 + family PPC $1,500 + LSA $1,000 + Meta $500 = $5,500."))
story.append(b("<b>Aggressive:</b> $730K goal x 20% / 12 = $12,167; minus $4,847 fee = $7,320; rounded to Starter cap $8,000."))
story.append(b("At aggressive: $8,047 + $8,000 = $16,047/mo = 26.4% of $60,833 monthly revenue. Under 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I\'m already spending $6,000/month on LSAs — why spend more?"', S["objection_q"]))
story.append(Paragraph("The $6K is LSA-only and self-managed with no PPC, no Meta, and no SEO. Eskew Law built a dedicated Anderson page and is actively bidding for his criminal defense keywords. Every month without a counter-campaign those Indianapolis firms pick off Anderson cases that belong to the local attorney.", S["objection_a"]))

story.append(Paragraph('"The website is brand new — do I really need to rebuild it?"', S["objection_q"]))
story.append(Paragraph("Chris described it himself as 'a basic landing page, not built for SEO.' Zaki Ali Trial Lawyers has 462 reviews and years of indexed content. The current site generates zero organic leads — 100% of traffic is paid or direct. A rebuild is not optional for an organic strategy.", S["objection_a"]))

story.append(Paragraph('"I just launched — this feels like a lot."', S["objection_q"]))
story.append(Paragraph("He generated $60K in 2.5 weeks. The demand is real. The problem is those leads all run through Chris personally 24/7 — the exact pattern he left his previous firm to escape. Building systems now is what prevents the 10-11 PM nights from returning at Gilley Law.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, Google PPC + LSA, Meta ads, SEO, reporting.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("1:1 coaching, group sessions, intake design, financial tracking.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,500–$8,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $5,500–$8,000 ad spend  |  Save $1,147/mo by bundling  |  22.3%–26.4% of revenue (under 35% cap)",
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
