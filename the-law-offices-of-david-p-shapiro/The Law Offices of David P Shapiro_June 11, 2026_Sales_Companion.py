"""
Sales Companion PDF — The Law Offices of David P. Shapiro
June 11, 2026 | Rep: Jacob Meissner
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

OUTPUT_PATH = "the-law-offices-of-david-p-shapiro/The Law Offices of David P Shapiro_June 11, 2026_Sales_Companion.pdf"


def add_page_elements(canvas, doc):
    canvas.saveState()
    width, height = letter
    canvas.setFont("Helvetica-Bold", 10)
    canvas.setFillColor(RED_WARNING)
    canvas.drawCentredString(width / 2, height - 0.38 * inch, "FOR INTERNAL USE ONLY; DO NOT SHARE.")
    canvas.setStrokeColor(RED_WARNING)
    canvas.setLineWidth(0.5)
    canvas.line(0.6 * inch, height - 0.44 * inch, width - 0.6 * inch, height - 0.44 * inch)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawCentredString(width / 2, 0.28 * inch, "SMB Team  |  Confidential  |  Internal Document")
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
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9, leading=11, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8.5, leading=11, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
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

story.append(Paragraph("The Law Offices of David P. Shapiro", S["title"]))
story.append(Paragraph("Sales Companion  |  June 11, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("David P. Shapiro", S["snap_value"]),
     Paragraph("~$500K+ est.", S["snap_value"]),
     Paragraph("7 (3 atty)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("San Diego, CA x2", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.1*inch, 0.85*inch, 0.7*inch, 0.8*inch, 1.1*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 3))

story.append(Paragraph("Dominant Buying Motive: SCALE AND DOMINATE", S["section"]))
story.append(Paragraph("Shapiro wants the firm recognized as the undisputed #1 criminal defense practice in San Diego County.", S["subsection"]))

story.append(quote_block("No transcript available. Observations from live research below."))
story.append(Spacer(1, 1))
story.append(quote_block("Firm markets itself as 'one of San Diego's largest criminal defense law firms' and sponsors Padres broadcasts on 97.3 The Fan — not a firm that avoids the spotlight."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Market dominance.</b> To be the first name every San Diego resident thinks of when they need a criminal defense attorney."))
story.append(bd("<b>Digital visibility to match his credentials.</b> AVVO 10.0 and 12 Super Lawyers listings that show up when prospects search Google, not just in directories."))
story.append(bd("<b>A firm that scales without him.</b> More revenue without more of his personal time — systems that run the firm, not just the owner."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No digital paid ads.</b> Radio builds awareness; it misses the midnight arrest search. No Google Ads, LSA, or Meta ads observed."))
story.append(b("<b>4:1 Google review gap.</b> Sevens Legal has 800+ reviews vs. this firm's ~204 — the primary local 3-pack ranking signal."))
story.append(b("<b>Website conversion gaps.</b> Buried contact form, no after-hours coverage — traffic does not convert as it should."))
story.append(b("<b>No financial tracking.</b> Revenue, margins, and owner compensation not confirmed — growth without visibility may not improve take-home."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts the firm's name on every San Diego criminal defense search — emergency calls this firm is currently missing go to them instead."))
story.append(bd("Closes the digital gap with Sevens Legal by competing on PPC, LSA, and Meta — the channels generating emergency retainers daily."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Criminal Defense + San Diego high-competitiveness: Essentials ineligible — Starter is minimum required tier."))
story.append(b("Practice areas (DUI, violent crimes, sex crimes, federal defense) require full-depth campaign coverage that Starter delivers."))
story.append(b("San Diego Tier 2 geo: $60–$150 CPC for criminal defense; Starter supports conservative launch at $5,500 ad spend."))
story.append(b("Saves $850/mo vs. stand-alone price of $5,697/mo."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds intake, team, and financial systems so the firm handles more volume without the owner becoming the bottleneck."))
story.append(bd("Creates the profit visibility to know whether growth is generating more take-home or just more overhead."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue band $400K–$1M: Elite Coach Plus is the appropriate tier."))
story.append(b("Intake specialist on staff but no documented process — coaching builds the intake system before scaling ad spend."))
story.append(b("7-person team, no confirmed management layer — coaching addresses the accountability gap directly."))
story.append(b("Saves $297/mo vs. stand-alone price of $3,497/mo."))


# PAGE 2
story.append(PageBreak())

story.append(Paragraph("David P. Shapiro — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Captures the midnight DUI arrest, the family member searching for a violent crimes attorney, the federal charge referral — the exact moment prospects are most willing to retain."))
story.append(bd("Conservative scenario: 2–3 new cases/month from digital alone. Aggressive: 12–13 cases/month. Both scenarios deliver strong ROI given this firm's case values."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,500/mo — channel minimums for criminal defense in San Diego."))
story.append(b("<b>Aggressive:</b> $22,000/mo — full coverage to compete with Sevens Legal. Note: exceeds Starter cap; Growth tier recommended at this level."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 18 leads x 15% close = 2–3 cases x $4K avg = ~$10K/mo vs. $5,500 spend = 1.8x return."))
story.append(b("<b>Aggressive:</b> 88 leads x 15% close = 12–13 cases x $4K avg = ~$52K/mo vs. $22K spend = 2.4x return."))
story.append(Paragraph("<i>Estimates only. Actual case values (felony/federal/sex crimes) likely $10K–$50K+ — true ROI substantially higher.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> PPC $2,500 + LSA $1,000 + Meta $2,000 = $5,500 (criminal defense minimums)."))
story.append(b("<b>Aggressive:</b> $1M goal x 20% / 12 x 1.3 (Tier 2) = $21,667; minus $4,847 fee = $16,820. Reverse math yields $34,675 — $22K is midpoint."))
story.append(b("$8,047 fees + $5,500 ad spend = $13,547 total (~32% of est. revenue). Within 35% cap at conservative level."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We already have radio and strong organic presence."', S["objection_q"]))
story.append(Paragraph("Radio misses the 2 a.m. arrest search. Sevens Legal has 800+ Google reviews and named SD's best DUI firm — they capture every digital emergency query this firm is not competing for.", S["objection_a"]))

story.append(Paragraph('"Our AVVO 10.0 and Super Lawyers already establish credibility."', S["objection_q"]))
story.append(Paragraph("Credibility is not the problem — visibility is. Those credentials do not appear on 'DUI lawyer San Diego' at midnight. Digital systems put credentials in front of prospects at the moment of need.", S["objection_a"]))

story.append(Paragraph('"We are not sure the timing is right for this investment."', S["objection_q"]))
story.append(Paragraph("Sevens Legal adds reviews every month — the 4:1 gap compounds over time. Every month without LSA and Google Ads is a month their local 3-pack dominance gets harder to challenge.", S["objection_a"]))

story.append(Paragraph('"How do we know the ROI will be there?"', S["objection_q"]))
story.append(Paragraph("LSA leads convert at 7x PPC. This firm's actual case values ($10K–$50K+ for felony/federal) make even 1–2 cases/month from a $5,500 ad spend a strong return. The market demand ($60–$150 CPC) confirms it.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, SEO, Meta Ads, website conversion optimization.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, intake optimization, team accountability, profit planning.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,500–$22,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $5,500–$22,000 ad spend  |  Save $1,147/mo by bundling  |  ~32–36% of estimated revenue",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
