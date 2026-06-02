"""
Sales Companion PDF — The Ebbert Law Firm
SMB Team | June 2, 2026 | Rep: Dan Bryant
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

OUTPUT_PATH = "the-ebbert/The_Ebbert_Law_Firm_06022026_Sales_Companion.pdf"


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
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=ACCENT_GREEN, spaceBefore=6, spaceAfter=2)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.5, leading=13, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9.5, leading=13, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9.5, leading=13, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9.5, leading=12, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9.5, leading=13, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
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

story.append(Paragraph("The Ebbert Law Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  June 2, 2026  |  Rep: Dan Bryant", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("L. Eric Ebbert", S["snap_value"]),
     Paragraph("Not stated; est. $500K+", S["snap_value"]),
     Paragraph("Solo — no staff", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Knoxville, TN", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: EFFICIENCY &amp; FREEDOM", S["section"]))
story.append(Paragraph("Eric wants a firm that works for him — not one he has to personally run every hour of the day.", S["subsection"]))

story.append(quote_block("137 Google reviews at 4.9 stars — strongest review position of any confirmed Knoxville competitor. Zero paid infrastructure to leverage it."))
story.append(Spacer(1, 1))
story.append(quote_block("Solo practitioner across 6 practice areas. Every lead, every intake call, every matter depends on Eric being available."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable pipeline.</b> Cases in consistently without depending on referrals or personal availability."))
story.append(bd("<b>Team layer.</b> Someone handling intake so he can focus on billable legal work."))
story.append(bd("<b>Financial clarity.</b> Know which of 6 practice areas drives the most profit per hour."))
story.append(bd("<b>Time back.</b> Step away without the firm stopping."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No paid marketing.</b> Zero Google Ads, LSA, or Meta — every competitor click is a case he didn't win."))
story.append(b("<b>Intake bottleneck.</b> No staff, no after-hours coverage — leads go unanswered when Eric is unavailable."))
story.append(b("<b>Solo ceiling.</b> Revenue capped by one person's billable hours with no path to scale."))
story.append(b("<b>Unused review equity.</b> 0 Avvo reviews despite 137 on Google; not in LSA at all."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gets the firm in front of qualified Knoxville prospects for employment, estate planning, and business law every day — without Eric doing anything."))
story.append(bd("Activates the 4.9/137 review profile in LSA — strongest in the market — so it generates cases, not just credibility."))
story.append(bd("Converts the website from brochure to lead engine with above-fold contact capture."))

story.append(Paragraph("<b>Full Service Marketing Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("No paid infrastructure exists — Starter covers Ads, LSA, SEO, and web optimization together."))
story.append(b("Revenue $400K–$1M range — Starter is the correct tier; Dominate/Platinum hidden."))
story.append(b("Multi-practice firm needs full-service; ads-only sub-package inappropriate without existing infrastructure."))
story.append(b("Burkhalter (95 reviews + active SEO) and Hodges (90+ years) require competitive budget."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Eric frameworks to build his first intake process and prepare for his first hire."))
story.append(bd("Weekly accountability keeps him building systems instead of staying in survival mode."))
story.append(bd("Peers who've solved the solo-to-firm-owner transition he is making right now."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M, no team — correct tier. Master's Circle requires 5+ staff."))
story.append(b("Solo managing everything — structured coaching fills operational gap until first hire."))
story.append(b("Fractional COO deferred to Phase 2 when team is being built."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("The Ebbert Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Converts 4.9/137 review equity into inbound cases — every dollar sends a high-credibility ad to active legal searchers in Knoxville."))
story.append(bd("Puts the firm above Burkhalter and HDC in paid and LSA positions where it currently has zero visibility."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,000/mo — PPC $2,500 + LSA $1,500 + Meta retargeting $1,000 (estate planning + business law)."))
story.append(b("<b>Aggressive:</b> $8,000/mo — expanded reach across all 5 areas; at or under 35% cap at estimated revenue."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative ($5K):</b> 40 leads x 15% close x $3K case value = $18K/mo vs. $5K spend = 3.6x return."))
story.append(b("<b>Aggressive ($8K):</b> 80 leads x 15% close x $3K case value = $36K/mo vs. $8K spend = 4.5x return."))
story.append(Paragraph("<i>All figures are estimates. Case value default — confirm on call. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Estate/business law minimums: PPC $2,500 + LSA $1,500 + Meta $1,000 = $5,000."))
story.append(b("<b>Aggressive:</b> $550K est. x 2 goal = $1.1M x 20% / 12 = $18,333. Tier 4 (1.0x). Minus $4,847 fee = $13,486. Capped at $8,000 for 35% compliance."))
story.append(b("At aggressive: $8,047 mgmt + $8,000 ads = $16,047. At $550K est. = 35% cap. Confirm revenue."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I get clients through referrals — I\'ve been fine for 30 years."', S["objection_q"]))
story.append(Paragraph("Referrals are not scalable and don't let you choose your cases. Burkhalter claims '#1 Knoxville Employment Attorney' online with active SEO. Every employment client who searches Google and clicks their result instead of yours is a case you didn't win. Your 4.9/137 review advantage needs a channel — and right now it doesn't have one.", S["objection_a"]))

story.append(Paragraph('"I don\'t know what my revenue is right now."', S["objection_q"]))
story.append(Paragraph("That's exactly what the coaching package addresses. Elite Coach Plus includes financial tracking frameworks to clarify revenue, margins, and profitability by practice area. We recommend starting marketing and coaching together — so growth is measured from day one.", S["objection_a"]))

story.append(Paragraph('"My website is working fine."', S["objection_q"]))
story.append(Paragraph("The design is solid and mobile responsive — that's working. The problem: contact form is on a separate page (not above-fold), no live chat, and GoDaddy limits landing page flexibility needed for paid campaigns. The Starter package includes conversion optimization — no full rebuild required.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, local SEO, website optimization, monthly strategy.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, masterminds, quarterly + annual workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,000–$8,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $5,000–$8,000 ad spend  |  Save $1,147/mo bundling  |  29%–35% of est. revenue (at/under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
