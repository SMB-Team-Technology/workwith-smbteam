"""
Sales Companion PDF — Adler Law Firm
SMB Team Internal Document — DO NOT SHARE WITH CLIENT
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

OUTPUT_PATH = "adler-law/Adler_Law_April_22_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Law Offices of Steven M. Adler, PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  April 22, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Steven Adler", S["snap_value"]),
     Paragraph("$1.4M/yr", S["snap_value"]),
     Paragraph("8 (4 att., 4 para.)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("60% (&#8595; 90%)", S["snap_value"]),
     Paragraph("Jericho, NY", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM &amp; SUCCESSION", S["section"]))
story.append(Paragraph("Steven wants to work 2.5 days per week and hand full day-to-day leadership to Marissa.", S["subsection"]))

story.append(quote_block("I want to get down to two and a half days a week. Marissa should be running this thing."))
story.append(Spacer(1, 1))
story.append(quote_block("My close rate has dropped from 90% to 60% — I know we're losing cases we already paid for."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>2.5-day work week.</b> Steven explicitly stated this as his primary personal goal."))
story.append(bd("<b>Marissa running the firm.</b> She is the identified successor — he wants to hand it off."))
story.append(bd("<b>Recover lost intake revenue.</b> He knows the 60% close rate is costing him real money."))
story.append(bd("<b>Financial clarity.</b> Broken Clio–QB sync means he cannot see true profit right now."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No intake follow-up system.</b> Non-retained consultations leave with no nurture sequence."))
story.append(b("<b>No team accountability.</b> No KPIs or scorecards — Steven monitors everything personally."))
story.append(b("<b>Financial blind spot.</b> Manual Excel + broken Clio–QB sync hide true profitability."))
story.append(b("<b>Waiting on hires.</b> Pending paralegal and Cashroom bookkeeper — wants Q3 start."))
story.append(b("<b>Scorpion lock-in.</b> Does not own his ad accounts or campaign data."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Adler Law owned campaign data — no more starting from zero if Scorpion leaves."))
story.append(bd("Adds LSA and Facebook retargeting: two channels Scorpion is not running."))
story.append(bd("Builds toward the dominant online presence Marissa needs to inherit a growing firm."))

story.append(Paragraph("<b>Dominate Full Service Marketing  |  $4,497/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1.4M (over $1M) — Dominate tier eligible; goals are aggressive ($1.8–$2M)."))
story.append(b("Scorpion generates 100+ leads/mo but firm does not own accounts or data — must rebuild ownership."))
story.append(b("Davidov Law Group has 250+ Google reviews vs. Adler's 82 — multi-channel approach required."))
story.append(b("Website geo-targeting strong — pairing owned ads with existing pages multiplies ROI."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching / Financial Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Marissa the structure to actually lead — not just work cases alongside Steven."))
story.append(bd("Builds the KPI scorecard that lets Steven stop monitoring and start stepping back."))
story.append(bd("Answers the financial question: can Steven sustain 2.5 days on current revenue?"))

story.append(Paragraph("<b>Elite Coach Plus + FCFO Advisor  |  $3,200 + $1,297 = $4,497/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1.4M, no dedicated ops/intake staff — Elite Coach Plus is the right tier."))
story.append(b("Broken Clio–QuickBooks sync + Excel tracking = no real-time profit visibility — FCFO warranted."))
story.append(b("60% close rate (down 30 pts) requires structured intake process coaching, not just hiring."))
story.append(b("Marissa's succession requires operational framework — trust alone is not a handoff plan."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Adler Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Adds independent lead flow that the firm owns — not dependent on Scorpion's platform."))
story.append(bd("Closes the Davidov review and visibility gap before it becomes permanent market dominance."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,000/mo — estate planning + probate channel minimums."))
story.append(b("<b>Aggressive:</b> $10,000/mo — Dominate tier cap; goal trajectory justifies full allocation."))

story.append(Paragraph("<b>Estimated Return on Investment (estimates — not guaranteed):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~7 cases x $6,000 = $42,000/mo vs. $5,000 spend = ~8x return."))
story.append(b("<b>Aggressive:</b> ~17 cases x $6,000 = $102,000/mo vs. $10,000 spend = ~10x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Estate Planning: PPC $1,500 + LSA $1,000 + Meta $700; Probate: PPC $1,500 + LSA $500 = ~$5,200 (rounded to $5,000)."))
story.append(b("<b>Aggressive:</b> $2M goal x 20% / 12 = $33,333; x Tier 2 (1.3x) = $43,333; minus $4,497 fee = $38,836; capped at $10,000 (Dominate tier cap)."))
story.append(b("At aggressive ($18,994 total): 16.3% of monthly revenue — well under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We\'re already paying $10K/month to Scorpion — I don\'t want to double my marketing spend."', S["objection_q"]))
story.append(Paragraph("Scorpion owns your ad accounts, data, and website. When that relationship ends, you start over. SMB Team builds infrastructure Adler Law owns. Also: the $10K/month Scorpion investment is generating leads at a 60% close rate — fixing that gap with a follow-up system recovers $6K–$30K/month without new ad spend.", S["objection_a"]))

story.append(Paragraph('"I need to wait until Cashroom gets the financials sorted — then we can talk."', S["objection_q"]))
story.append(Paragraph("The financial fix and the intake/marketing work run in parallel — one doesn't require the other. The conversion drop from 90% to 60% is happening right now; every week without a follow-up system is recoverable revenue walking out the door. The FCFO Advisor addresses the financial issue as part of the same engagement.", S["objection_a"]))

story.append(Paragraph('"Davidov has been around forever — I\'m not going to catch up in reviews."', S["objection_q"]))
story.append(Paragraph("Davidov has 250+ reviews; Adler has 82 — a 3-to-1 gap that feels large but closes faster than it looks. A post-matter review request to every closed client adds 5–10 reviews per month. At that rate, Adler reaches 200+ reviews in under 12 months. Every month without a request program is a month Davidov widens the gap.", S["objection_a"]))

story.append(Paragraph('"The close rate will fix itself once we hire the new paralegal."', S["objection_q"]))
story.append(Paragraph("The paralegal hire addresses capacity, not conversion. The 30-point drop is a process issue — consultation-to-signing — not a workload issue. More staff without a defined follow-up sequence will not recover the 40% of consultations currently leaving without retaining.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Dominate Full Service Marketing</b>", S["price_main"]),
     Paragraph("$4,497/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Facebook/Instagram ads, SEO, reporting.", S["price_detail"]),
     Paragraph("<strike>$5,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, KPI scorecard, intake process, delegation framework.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Fractional CFO Advisor</b>", S["price_main"]),
     Paragraph("$1,297/mo", S["price_main"])],
    [Paragraph("Monthly financial review, profit dashboard, owner comp modeling.", S["price_detail"]),
     Paragraph("<strike>$1,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,000–$10,000/mo", S["price_main"])],
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
    ("LINEBELOW", (0,7), (-1,7), 0.5, RULE_GRAY),
]))
story.append(pt)
story.append(Paragraph(
    "Total MRR: $8,994/mo + $5,000–$10,000 ad spend  |  Save $1,797/mo bundling  |  13.7%–16.3% of revenue (under 35% cap)",
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
