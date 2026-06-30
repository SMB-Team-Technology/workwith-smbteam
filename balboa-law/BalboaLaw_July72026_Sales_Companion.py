"""
Sales Companion PDF — Balboa Law
SMB Team Internal Document — DO NOT SHARE WITH CLIENT
Sales Rep: Jonathan Farace | Date: July 7, 2026
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

OUTPUT_PATH = "balboa-law/BalboaLaw_07072026_Sales_Companion.pdf"


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
S["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=9.5, leading=13, textColor=LIGHT_GRAY, spaceAfter=3)
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=ACCENT_GREEN, spaceBefore=5, spaceAfter=1)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.5, leading=13, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9.5, leading=13, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8.5, leading=11, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


def b(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY, spaceBefore=3, spaceAfter=3)

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

story.append(Paragraph("Balboa Law", S["title"]))
story.append(Paragraph("Sales Companion  |  July 7, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Gerald Balboa", S["snap_value"]),
     Paragraph("$0 (pre-launch)", S["snap_value"]),
     Paragraph("2 (Gerald + wife)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Houston, TX", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: FINANCIAL FREEDOM", S["section"]))
story.append(Paragraph("Build a bilingual Houston PI firm that generates $300K–$1M/yr in profit without consuming Gerald or his wife's time.", S["subsection"]))
story.append(quote_block("Target a September 1 launch, with a first-year profit goal of $300K–$1M."))
story.append(Spacer(1, 1))
story.append(quote_block("Focus on marketing and intake for high-value cases — refer to trusted partners for a referral fee."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Income without daily involvement.</b> The referral model generates fees while automation handles intake."))
story.append(bd("<b>Minimal wife burden.</b> Her attorney role stays frictionless — the system does the work."))
story.append(bd("<b>The bilingual PI brand.</b> Balboa Law becomes Houston's go-to firm in English and Spanish."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Zero digital infrastructure.</b> No website, GBP, or reviews entering one of the most competitive PI markets in the US."))
story.append(b("<b>Physical office TBD.</b> Without a verified address, LSA and 3-Pack cannot be unlocked before September 1."))
story.append(b("<b>Intake not built yet.</b> Automation model doesn't exist — must be operational before ad spend begins."))
story.append(b("<b>Cash flow timing gap.</b> PI referral fees settle in 12–36 months; year-one profit goal requires a plan for the delay."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the entire digital infrastructure — website, GBP, ads, LSA, Meta — in English and Spanish before September 1."))
story.append(bd("Houston PI expertise: SMB's paid ads team knows which $170–$407/click keywords produce cases vs. burn budget."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("PI practice: Essentials tier hidden; Starter is the minimum qualifying tier."))
story.append(b("Custom bilingual website required — firm has no live site; 90-day SMB build targets September launch."))
story.append(b("Starter supports up to $40K/mo ad spend; well above the $10K–$25K recommended year-one range."))
story.append(b("Scoping approval required: revenue under $300K (pre-launch firm)."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Strategic guidance to build a referral-fee PI model correctly — Gerald has no prior law firm ownership experience."))
story.append(bd("Cash flow modeling for the 12–36 month referral settlement timeline turns the $300K–1M goal into an executable plan."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue under $400K: Elite Coach is the correct tier per eligibility rules."))
story.append(b("Scoping approval required: revenue under $250K; confirm 4 months of funds available before signing."))
story.append(b("Includes weekly group coaching, PI masterminds, quarterly workshops, annual in-person event."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Balboa Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Activates the lead flow engine the income goal depends on — in Houston PI, first-mover visibility wins cases."))
story.append(bd("Bilingual campaigns reach Spanish-speaking Houston PI prospects at lower CPCs with equivalent referral fee potential."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $10,000/mo — PI hard floor, high-competitiveness Houston. Mix: 65% Google, 25% LSA, 10% Meta."))
story.append(b("<b>Aggressive:</b> $25,000/mo — upper end of Gerald's $8,333–$16,667/mo budget; within Starter's $40K cap."))

story.append(Paragraph("<b>Estimated ROI (all figures estimates; referral fees paid at settlement):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 2–3 referrals/mo x $20K fee = $40K–$60K pipeline vs. $10K spend = 4–6x return."))
story.append(b("<b>Aggressive:</b> 5–7 referrals/mo x $25K fee = $125K–$175K pipeline vs. $25K spend = 5–7x return."))
story.append(b("<b>Calculation:</b> Blended CPL ~$125 conservative (20% cushion); ~$100 aggressive. 15% close rate. New firm discount applied."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"This is a lot of money for a firm that hasn\'t launched yet."', S["objection_q"]))
story.append(Paragraph("Pre-launch is the right time to invest — there are no active leads to lose while infrastructure is being built. Gerald's own estimate of $100K–$200K/year for marketing confirms the scale; SMB ensures that budget generates returns rather than being absorbed by $407/click PI keywords.", S["objection_a"]))

story.append(Paragraph('"I want to start small and see how ads perform first."', S["objection_q"]))
story.append(Paragraph("Houston PI CPCs run $170–$407/click. Below the $10K/mo PI hard floor, spend gets consumed before generating case volume. The conservative recommendation is already the minimum that can produce results — below it, results are statistically unlikely.", S["objection_a"]))

story.append(Paragraph('"My wife is skeptical and needs to see results before committing."', S["objection_q"]))
story.append(Paragraph("The system is designed so she doesn't have to be involved — automated intake and referral escalation handle everything. Results come fastest when infrastructure is built right before launch. Zehl has 1,262 reviews; Arnold &amp; Itkin has 1,346. Every month of delay widens that gap.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Bilingual website, Google Ads (EN+ES), LSA, Meta, GBP, local SEO, directories.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly coaching, PI masterminds, quarterly workshops, annual in-person, profit plan.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$10,000–$25,000/mo", S["price_main"])],
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
    "Total: $7,447/mo SMB fees + $10K–$25K ad spend  |  Save $1,747/mo by bundling  |  Scoping approval required (pre-launch revenue)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
