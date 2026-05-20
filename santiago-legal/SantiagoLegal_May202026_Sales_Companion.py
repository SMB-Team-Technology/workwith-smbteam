"""
Sales Companion PDF — Santiago Legal LLC
Sales Rep: Randy Gold
Date: May 20, 2026
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

OUTPUT_PATH = "santiago-legal/SantiagoLegal_May202026_Sales_Companion.pdf"


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

story.append(Paragraph("Santiago Legal LLC", S["title"]))
story.append(Paragraph("Sales Companion  |  May 20, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Karla Santiago", S["snap_value"]),
     Paragraph("Not confirmed", S["snap_value"]),
     Paragraph("Solo (est.)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("Minnetonka, MN", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM + IMPACT", S["section"]))
story.append(Paragraph("Karla wants to serve more of Minnesota's Latino immigrant community without burning out — and build a firm that validates 16 years of bilingual legal practice.", S["subsection"]))

story.append(quote_block("No transcript available. DBM inferred from firm context and 16-year bilingual solo immigration profile. Verify on May 22 call."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>More clients, not more hours.</b> A system that brings the community to her, not the other way around."))
story.append(bd("<b>Market recognition.</b> Known as Minnesota's go-to Spanish-speaking immigration attorney."))
story.append(bd("<b>Time back.</b> A firm that runs when she's not in the room — no more single point of failure."))
story.append(bd("<b>Financial return.</b> Profit that grows independently of personal hours billed."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Zero reviews.</b> 0 verified reviews vs. 68–118 for top competitors — invisible in local search and LSA."))
story.append(b("<b>No paid ads.</b> All high-intent Google, LSA, and Meta traffic goes to competitors."))
story.append(b("<b>Solo intake.</b> Every inquiry routes to Karla personally — caps capacity at one attorney's hours."))
story.append(b("<b>Dual-domain issue.</b> santiagolegalservices.com vs. santiagolegalgroup.com actively suppresses local SEO."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Puts Santiago Legal in front of Spanish-speaking immigrants searching right now and finding competitors instead."))
story.append(bd("Closes the review gap with Capriotti (118) through systematic GBP optimization and review generation."))
story.append(bd("Activates 16 years of bilingual expertise at scale — community finds her, she doesn't have to find them."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("CD listed on Avvo; Minneapolis is high-competitiveness CD market → Essentials hidden; Starter is minimum eligible tier."))
story.append(b("Spanish-language campaigns are a structural differentiator no English-only competitor can replicate."))
story.append(b("GBP review generation is LSA prerequisite — without reviews, firm cannot appear above all organic results."))
story.append(b("Website rebuild required — no CTA above fold, dual-domain issue, no practice area pages → full service only."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Builds the intake process so Karla can handle marketing leads without burnout."))
story.append(bd("Dedicated growth coach to guide the solo-to-firm-leader transition."))
story.append(bd("Financial baselines and profit tracking that turn revenue growth into real income growth."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue estimated $400K–$1M for 16-year solo boutique — correct tier for this stage."))
story.append(b("Under $500K revenue means fractional COO/CFO products are hidden; Elite Coach Plus is the fit."))
story.append(b("Intake system design and first hire framework are immediate deliverables that unlock marketing ROI."))
story.append(b("Includes weekly group coaching, masterminds, quarterly workshops, one annual in-person workshop."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Santiago Legal LLC — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Activates the Spanish-language search market immediately — qualified immigration leads arriving within days of campaign launch."))
story.append(bd("Generates the review volume needed for LSA qualification, unlocking the highest-visibility ad position on Google over time."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $8,000/mo — minimum viable spend across Google PPC ($3,000), LSA ($2,000), and Meta Lead Gen ($3,000)."))
story.append(b("<b>Aggressive:</b> $15,000/mo — scaled bilingual campaigns across all channels; subject to revenue confirmation on proposal call."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 82 leads x 15% close = 12 cases x $3,750 avg = $45,000/mo vs. $8,000 spend = 5.6x return."))
story.append(b("<b>Aggressive:</b> 185 leads x 15% close = 28 cases x $3,750 avg = $105,000/mo vs. $15,000 spend = 7.0x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. ACV uses immigration practice area default ($3,000–$4,500) — confirm actual ACV on proposal call.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Immigration minimums: Google PPC $3,000 + LSA $2,000 + Meta Lead Gen $3,000 = $8,000."))
story.append(b("<b>Aggressive:</b> $800K goal x 20% / 12 = $13,333. Tier 2 (1.30x) = $17,333. Spanish (1.33x) = $23,053. Minus $4,847 fee = $18,206; presenting $15,000 pending revenue confirmation."))
story.append(b("35% cap check: confirm actual revenue on May 22 call before finalizing ad spend commitment."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I already get clients through word of mouth."', S["objection_q"]))
story.append(Paragraph("Referrals are a ceiling. Capriotti has 118 reviews; Dyan Williams runs bilingual podcasts targeting your exact audience. The community you want to serve is searching right now — the question is whose name they find.", S["objection_a"]))

story.append(Paragraph('"I\'m not sure I can afford this right now."', S["objection_q"]))
story.append(Paragraph("Conservative scenario: $8,000 ad spend → 12 cases x $3,750 = $45,000/mo revenue = 5.6x return on ad spend. The $8,047 SMB investment is the infrastructure that generates those returns.", S["objection_a"]))

story.append(Paragraph('"I don\'t have a team to handle more leads."', S["objection_q"]))
story.append(Paragraph("Elite Coach Plus solves exactly this in the first 90 days — intake system and first hire framework before the lead firehose turns on.", S["objection_a"]))

story.append(Paragraph('"My website is already bilingual."', S["objection_q"]))
story.append(Paragraph("The bilingual foundation is a real advantage — but no CTA above fold, no practice area pages, and the dual-domain NAP issue (santiagolegalservices.com vs. santiagolegalgroup.com) are actively suppressing SEO. The foundation is strong; the conversion layer is not built yet.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, bilingual Google Ads (EN + ES), GBP build, LSA setup, Meta campaigns.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Dedicated growth coach, intake system design, first hire framework, group coaching + workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$8,000–$15,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $8,000–$15,000 ad spend  |  Save $1,147/mo by bundling  |  Confirm % of revenue on May 22 call",
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
