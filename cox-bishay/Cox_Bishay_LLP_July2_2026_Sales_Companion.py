"""
Sales Companion PDF — Cox & Bishay, LLP
July 2, 2026 | Rep: Randy Gold
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

DARK_NAVY = HexColor("#1a2332")
ACCENT_GREEN = HexColor("#3B6D11")
MEDIUM_GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#888888")
RULE_GRAY = HexColor("#CCCCCC")
QUOTE_BG = HexColor("#F5F7F0")
WHITE = HexColor("#FFFFFF")
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "cox-bishay/Cox_Bishay_LLP_07022026_Sales_Companion.pdf"


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
S["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=9, leading=12, textColor=LIGHT_GRAY, spaceAfter=2)
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=ACCENT_GREEN, spaceBefore=4, spaceAfter=1)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9, leading=11, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8.5, leading=11, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=2)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


def b(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY, spaceBefore=2, spaceAfter=2)

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


# PAGE 1
story = []

story.append(Paragraph("Cox &amp; Bishay, LLP", S["title"]))
story.append(Paragraph("Sales Companion  |  July 2, 2026  |  Rep: Randy Gold", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Rami Bishay &amp; Kimberly Cox", S["snap_value"]),
     Paragraph("~$500K (est.)", S["snap_value"]),
     Paragraph("3 (2 partners + paralegal)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("West Chester, PA", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.15*inch, 0.9*inch, 0.65*inch, 0.7*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 3))

story.append(Paragraph("Dominant Buying Motive: LEGACY + GROWTH ON THEIR TERMS", S["section"]))
story.append(Paragraph("Grow their 35-year boutique practice — attract the right cases, build systems, and grow without becoming a volume firm.", S["subsection"]))
story.append(quote_block("No transcript. DBM inferred: 35-year family law boutique, Super Lawyers + Avvo 9.6, zero paid marketing — signals quality-focused growth, not volume."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What they want:</b>", S["subsection"]))
story.append(bd("<b>More of the right clients.</b> Selective firm — they want qualified Chester County families, not volume."))
story.append(bd("<b>Digital visibility that matches their reputation.</b> 35 years of peer awards; zero first-page presence."))
story.append(bd("<b>Freedom from doing everything personally.</b> Partners handle all intake and operations — no systems yet."))

story.append(Paragraph("<b>What is stopping them:</b>", S["subsection"]))
story.append(b("<b>Zero digital lead gen.</b> No ads, no 3-pack rankings, no contact form, no online lead capture."))
story.append(b("<b>3 active NAP errors.</b> Wrong address on Yelp, wrong city on Lawful.com, wrong name on Martindale."))
story.append(b("<b>No intake system.</b> Partners handle all first contact; no after-hours path; no follow-up process."))
story.append(b("<b>Revenue unconfirmed (~$500K est.).</b> Verify before finalizing; 35% cap check required."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("<b>First-page visibility.</b> Makes Cox &amp; Bishay findable for every Chester County family law search."))
story.append(bd("<b>Rebuilt website that converts.</b> Current site has no form; paid ads need a working landing page."))
story.append(bd("<b>Predictable client flow.</b> Moves the firm off referral dependency onto a system it controls."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$400K–$800K — Starter tier correct. Upgrade to Growth when revenue crosses $1M."))
story.append(b("Website rebuild required: no contact form, no CTAs, no geo pages — site blocks ad ROI without rebuild."))
story.append(b("NAP cleanup in onboarding: 3 citation errors must be fixed before SEO investment gains traction."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("<b>Operational framework before the leads arrive.</b> Intake process, role clarity, and KPIs set up first."))
story.append(bd("<b>Peer learning with family law owners at the same stage.</b> Masterminds specific to their practice area."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Team of 3 (under 5) — Master's Circle hidden; Elite Coach Plus is the correct tier."))
story.append(b("No transcript: coaching need inferred from Stage 3 profile and all-partner bottleneck on intake and operations."))
story.append(b("Adding marketing without coaching creates capacity chaos — coaching builds the system to absorb the growth."))


# PAGE 2
story.append(PageBreak())

story.append(Paragraph("Cox &amp; Bishay, LLP — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("<b>Reaches Chester County families at peak search intent.</b> Divorce, custody, and support searches — captured before competitors get them."))
story.append(bd("<b>Conservative level proves the model fast.</b> Aggressive level competes meaningfully against Ciccarelli, McCallin, and Petrelli Previtera."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — PPC $1,500 + LSA $1,000 + Meta Retargeting $1,000."))
story.append(b("<b>Aggressive:</b> $8,000/mo — Starter tier cap; full PPC + LSA + Meta deployment."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~22 leads x 15% = 3–4 cases x $10K = ~$35K/mo vs. $3,500 spend = ~10x return."))
story.append(b("<b>Aggressive:</b> ~68 leads x 15% = 10–11 cases x $10K = ~$110K/mo vs. $8,000 spend = ~14x return."))
story.append(Paragraph("<i>Estimates only. $10K avg case value is a default for Chester County family law — verify with firm. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Family Law channel minimums — PPC $1,500 + LSA $1,000 + Meta $1,000 = $3,500."))
story.append(b("<b>Aggressive:</b> $1M goal x 20% / 12 = $16,667. Tier 4 (1.0x). Minus $4,847 fee = $11,820. Capped at Starter max $8,000."))
story.append(b("35% cap: $8,047 + $8,000 = $16,047. Passes at ~$550K+ revenue. Confirm actual revenue before finalizing."))

story.append(thin_rule())

story.append(Paragraph("If They Push Back", S["section"]))

story.append(Paragraph('"We built on referrals for 35 years — why change now?"', S["objection_q"]))
story.append(Paragraph("Referrals cap at your network size. Ciccarelli has 618 reviews and runs paid ads. Petrelli Previtera built West Chester landing pages from Philadelphia. Every Chester County family searching online finds them — not Cox &amp; Bishay.", S["objection_a"]))

story.append(Paragraph('"We don\'t know our revenue — how do we know we can afford this?"', S["objection_q"]))
story.append(Paragraph("Conservative: $3,500 ad spend + $8,047 fees = $11,547/mo. Three additional cases at $10K covers it. Conservative projection shows 3–4 cases/mo. The math works — just confirm actual revenue to finalize scope.", S["objection_a"]))

story.append(Paragraph('"We\'re only two attorneys. We can\'t handle more volume."', S["objection_q"]))
story.append(Paragraph("Coaching kickoff includes intake process audit and team structure review before lead volume increases. First 90 days builds the capacity infrastructure — not the volume. We never flood a firm before it is ready.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, local SEO, Google Ads, LSA, Meta — full digital stack.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, family law masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,500–$8,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $3,500–$8,000 ad spend  |  Save $1,147/mo by bundling  |  ~28%–38% of est. revenue (verify at ~$550K+ for 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
