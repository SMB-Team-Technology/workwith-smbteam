"""
Sales Companion PDF — Just Jurist Law Firm, PLLC
Sales Rep: Dan Bryant
Date: May 12, 2026
FOR INTERNAL USE ONLY — DO NOT SHARE WITH CLIENT
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

OUTPUT_PATH = "just-jurist-law-firm/JustJuristLawFirm_May122026_Sales_Companion.pdf"


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


# ════════════════════════════════════════════════════════
# PAGE 1
# ════════════════════════════════════════════════════════
story = []

story.append(Paragraph("Just Jurist Law Firm, PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  May 12, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Pablo Gonzalez Zepeda", S["snap_value"]),
     Paragraph("~$400K-$600K est.", S["snap_value"]),
     Paragraph("3 (2 atty + 1 paralegal)", S["snap_value"]),
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
story.append(Paragraph("Pablo wants a firm that runs without him so he can stop working evenings and get his personal time back.", S["subsection"]))

story.append(quote_block("Build a self-managed, autonomous team to reduce reliance on Pablo for meetings and decisions."))
story.append(Spacer(1, 1))
story.append(quote_block("Runs profitably but hasn't scaled due to lifestyle/time priorities."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Evenings back.</b> Pablo attends all HOA board meetings personally — he wants a team that handles those without him."))
story.append(bd("<b>Autonomous firm.</b> Check in once a week and see the firm running, not be the reason it runs."))
story.append(bd("<b>A players.</b> Current team requires constant direction — he wants self-managing people."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Owner dependency.</b> Every board meeting and decision flows through Pablo personally."))
story.append(b("<b>Weak team.</b> Attorney and paralegal require hand-holding; no self-managing culture."))
story.append(b("<b>Zero digital presence.</b> No Google reviews, no local search, no ads — all growth is referral-dependent."))
story.append(b("<b>Hiring fear.</b> Afraid of training/losing associates; no ROI model to justify the hire."))
story.append(b("<b>No profit plan.</b> Revenue unknown at firm level; decisions made on gut, not data."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("New association clients find Just Jurist online and request a consult without Pablo's personal network being involved."))
story.append(bd("A predictable lead pipeline gives Pablo the revenue confidence to fund the team hires that create his freedom."))
story.append(bd("Claiming the GBP and building 20+ reviews immediately repositions Just Jurist above ALG's 2.9-star profile in search."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $2,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue est. $400K-$600K — Starter tier is the correct tier for this stage."))
story.append(b("Zero digital presence: no GBP reviews, no local pack, no paid ads — full foundation build required."))
story.append(b("Miami is Tier 2 market; HOA/condo law is B2B transactional; Google PPC and LSA are the primary channels."))
story.append(b("Ad spend cap at Starter tier: $5,000/mo; aggressive calculation (2x revenue goal) yields $18,820 — capped at tier limit."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Mastermind with HOA law firm owners who have already built autonomous firms — Pablo learns from peers who solved his exact problem."))
story.append(bd("Weekly coaching delivers the delegation frameworks and hiring protocols to build a team that runs without him."))

story.append(Paragraph("<b>Elite Coach Plus  |  $2,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K-$600K, team of 3: Elite Coach Plus is the correct tier."))
story.append(b("Master's Circle and FCOO excluded: team under 5, revenue under $1M."))
story.append(b("Pablo asked specifically about mastermind access — this is the right product."))
story.append(b("Primary need: team autonomy and delegation systems. Elite Coach Plus delivers both."))


# ════════════════════════════════════════════════════════
# PAGE 2
# ════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Just Jurist Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Inbound association leads arrive through Google — Pablo's personal network is no longer the only path to new clients."))
story.append(bd("At even conservative ROI (5x), a $2,500 ad spend generates ~$13,500/mo in new retainer value — funding his first team hire within months."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $2,500/mo — Google PPC $1,500 + LSA $1,000 (Business Law channel minimums as HOA/condo proxy)."))
story.append(b("<b>Aggressive:</b> $5,000/mo — Starter tier cap; 20% rule on $1M revenue goal yields $18,820 but is capped at tier maximum."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative ($2,500/mo):</b> ~10 leads x 15% close x $9K retainer value = ~$13,500/mo vs $2,500 spend = 5.4x return."))
story.append(b("<b>Aggressive ($5,000/mo):</b> ~25 leads x 15% close x $9K retainer value = ~$34,000/mo vs $5,000 spend = 6.8x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Case value = first-year HOA general counsel retainer ($750/mo x 12).</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> HOA/condo law (Business Law proxy): PPC $1,500 + LSA $1,000 = $2,500."))
story.append(b("<b>Aggressive:</b> $1.0M target x 20% / 12 = $16,667. Miami Tier 2 (1.3x) = $21,667. Minus $2,847 fee = $18,820. Capped at Starter tier limit of $5,000."))
story.append(b("Total SMB spend at conservative: ($5,047 + $2,500) / $41,667 = 18.1% of monthly revenue. Well under 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I\'ve seen peers spending $8,000/month on ads — that seems ridiculous."', S["objection_q"]))
story.append(Paragraph("The question is not the spend — it is the return. At $2,500/mo conservative, one new association retainer at $9,000/yr covers 3.6 months of ads. Most HOA associations stay for years. The math works at even modest volume.", S["objection_a"]))

story.append(Paragraph('"What if I train someone and they leave to compete with me?"', S["objection_q"]))
story.append(Paragraph("This fear is real but solvable. SMB Team's coaching includes hiring protocols that build loyalty, structured onboarding, and systems that make the firm's processes — not Pablo's relationships — the client retention engine. The risk of not hiring is worse: Pablo stays in every meeting indefinitely.", S["objection_a"]))

story.append(Paragraph('"I\'m not sure I can afford the investment right now."', S["objection_q"]))
story.append(Paragraph("At an estimated $400K-$600K gross with 40 association retainers, Just Jurist already generates predictable recurring revenue. The $5,047/mo management fee represents roughly 10-15% of estimated monthly gross. The first new association client from ads likely covers the management fee entirely.", S["objection_a"]))

story.append(Paragraph('"How hands-on is SMB Team — can you actually help me find and recruit a good HOA attorney?"', S["objection_q"]))
story.append(Paragraph("Pablo asked this directly on the call. Elite Coach Plus includes specific hiring frameworks, candidate sourcing guidance, and access to the SMB Team mastermind network — peers who have already recruited and retained A-player attorneys at similar HOA-focused firms.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$2,847/mo", S["price_main"])],
    [Paragraph("Google Ads, GBP, LSA, website CRO, review generation, monthly reporting.", S["price_detail"]),
     Paragraph("<strike>$4,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$2,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, HOA/probate mastermind, quarterly workshops, hiring frameworks.", S["price_detail"]),
     Paragraph("<strike>$2,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$2,500–$5,000/mo", S["price_main"])],
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
    "Total: $5,047/mo + $2,500–$5,000 ad spend  |  Save $2,147/mo by bundling  |  18.1%–24.1% of est. revenue (under 35% cap)",
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
