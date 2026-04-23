"""
Sales Companion PDF — Ammeen & Associates LLC
SMB Team  |  April 22, 2026  |  Rep: Randy Gold
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

OUTPUT_PATH = "ammeen-associates/Ammeen_Associates_April22_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Ammeen &amp; Associates LLC", S["title"]))
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
    [Paragraph("James Ammeen Jr.", S["snap_value"]),
     Paragraph("~$550K combined", S["snap_value"]),
     Paragraph("2 attorneys", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Indianapolis, IN", S["snap_value"])],
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
story.append(Paragraph("James wants a firm that runs without him — so he can take the golf trips and travel he's been putting off for years.", S["subsection"]))

story.append(quote_block("I want to be able to take a week off and not have everything fall apart."))
story.append(Spacer(1, 1))
story.append(quote_block("Slow lead response due to my workload is a known problem."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Intake off his plate.</b> Wants Gene handling leads when James is in court — no leads lost to slow response."))
story.append(bd("<b>Digital pipeline.</b> Signed 12 clients last year with capacity for 5 more/month — needs a system to fill the gap."))
story.append(bd("<b>$1M milestone.</b> James at $500K, Gene partner at $300K, new associate at $200K, firm runs without him."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No intake system.</b> Losing 2–3 leads/month = $8K–$12K in missed revenue; no script, no follow-up, no delegation."))
story.append(b("<b>Zero digital visibility.</b> Not in Google 3-pack or paid results for commercial litigation, estate planning, or creditor bankruptcy."))
story.append(b("<b>Gene has no path.</b> No partnership track = no BD accountability; James stays the only rainmaker."))
story.append(b("<b>Marketing blind.</b> LegalMatch $570/mo since Feb 2025, never tracked in Clio; unknown if it generates a single client."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Clients start finding James on Google instead of only through referrals — building an inbound pipeline that makes the associate hire possible."))
story.append(bd("Firm becomes visible for the three searches that matter: commercial litigation, estate planning, and creditor bankruptcy in Indianapolis."))
story.append(bd("Every marketing dollar tracked — ends the guesswork on LegalMatch and every future channel."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$550K places firm in Starter tier; Google Ads + LSA + Meta cover all three practice areas."))
story.append(b("Website rebuild required: avalawin.com 4–6 years old, no practice-area pages, three firm names hurting local SEO."))
story.append(b("Ad cap $3,000/mo appropriate now; tier upgrade planned at $800K+."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gene gets a defined role and partnership path — giving James someone who can run the firm when he's traveling."))
story.append(bd("Billing and revenue tracking surface unbilled hours already being worked — recovering revenue before a single new client signs."))
story.append(bd("Structured accountability turns James's $1M goal into a sequenced plan, not a wish."))

story.append(Paragraph("<b>Elite Coach Plus  |  $1,200/mo bundled</b>", S["subsection"]))
story.append(b("2 attorneys, no ops staff, owner hands-on — correct fit for Starter tier coaching."))
story.append(b("Builds execution plan for $1M goal, intake delegation, Gene's partnership path."))
story.append(b("FCOO Advisor added at $700K–$750K milestone as complexity grows."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Ammeen &amp; Associates — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Paid search reaches business owners and families actively searching for a commercial litigation or estate planning attorney tonight — not waiting on a referral."))
story.append(bd("At 2 cases/month from ads, revenue return covers the full SMB investment — a compounding asset, not an ongoing expense."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $2,500/mo — commercial litigation Google PPC $1,500 + estate planning LSA $500 + Meta retargeting $500."))
story.append(b("<b>Aggressive:</b> $3,000/mo — Starter tier cap; full roadmap targets tier upgrade as revenue grows toward $1M."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 2 cases x $4,000 = $8,000/mo vs. $2,500 spend = 3.2x return (est.)."))
story.append(b("<b>Aggressive:</b> 3 cases x $4,000 = $12,000/mo vs. $3,000 spend = 4.0x return (est.)."))
story.append(Paragraph("<i>Case value is a blended estimate ($4,000) using practice area defaults; close rate default 15%. All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Channel minimums — commercial litigation PPC $1,500 + estate planning LSA $500 + meta retargeting $500 = $2,500."))
story.append(b("<b>Aggressive:</b> $1M goal x 20% / 12 = $16,667; Tier 3 Indianapolis x 1.15 = $19,167; minus $4,847 mgmt fee = $14,320; capped at Starter tier maximum $3,000."))
story.append(b("At $3,000 ad spend + $6,047 management fees: total SMB spend $9,047 = ~19.7% of current monthly revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I already tried marketing — LegalMatch isn\'t working."', S["objection_q"]))
story.append(Paragraph("LegalMatch has never been tracked in Clio — no data proves it isn't working, only silence. That's a measurement failure. We build tracking first so every dollar is accountable.", S["objection_a"]))

story.append(Paragraph('"I don\'t have capacity for more clients right now."', S["objection_q"]))
story.append(Paragraph("James signs 1 client/month with capacity for 5 more. The constraint is leads and intake, not capacity. Fixing intake alone could close the gap without a single new marketing dollar.", S["objection_a"]))

story.append(Paragraph('"I need to fix intake before I spend money on marketing."', S["objection_q"]))
story.append(Paragraph("Intake and marketing launch together — the script, cadence, and Gene's role are built in the first 90 days of coaching before ads ramp up.", S["objection_a"]))

story.append(Paragraph('"This seems expensive for a firm our size."', S["objection_q"]))
story.append(Paragraph("$6,047/month in management fees is ~13% of current monthly revenue — well under the 35% threshold. At 2 new cases/month at $4K, ad revenue alone covers the full SMB investment.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, Google Ads, LSA, Meta retargeting — all three practice areas.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$1,200/mo", S["price_main"])],
    [Paragraph("Coaching, accountability, Gene's partnership path, intake system, revenue dashboard.", S["price_detail"]),
     Paragraph("<strike>$2,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$2,500–$3,000/mo", S["price_main"])],
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
    "Total: $6,047/mo + $2,500–$3,000 ad spend  |  Save $2,147/mo by bundling  |  18.5%–19.7% of revenue (under 35% cap)",
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
