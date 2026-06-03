"""
Sales Companion PDF — Lasser Law Group
Sales Rep: Randy Gold | Audit Date: June 2, 2026
FOR INTERNAL USE ONLY. DO NOT SHARE WITH CLIENT.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
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
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "lasser-law-group/LasserLawGroup_June2_2026_Sales_Companion.pdf"


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


doc = SimpleDocTemplate(OUTPUT_PATH, pagesize=letter,
    topMargin=0.65 * inch, bottomMargin=0.42 * inch,
    leftMargin=0.6 * inch, rightMargin=0.6 * inch)

S = {}
S["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=9, leading=12, textColor=LIGHT_GRAY, spaceAfter=2)
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=10.5, leading=14, textColor=ACCENT_GREEN, spaceBefore=4, spaceAfter=1)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=0)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=0)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9, leading=11, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=1)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8, leading=11, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=2)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=0)


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
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


# PAGE 1
story = []

story.append(Paragraph("Lasser Law Group PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  June 2, 2026  |  Rep: Randy Gold", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]), Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]), Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]), Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("S. Lasser", S["snap_value"]), Paragraph("~$1M est.", S["snap_value"]),
     Paragraph("12 (9 atty)", S["snap_value"]), Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]), Paragraph("NYC, 3 offices", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.7*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 2))

story.append(Paragraph("Dominant Buying Motive: SCALE AND DOMINATE", S["section"]))
story.append(Paragraph("Stephen wants Lasser Law Group to be the recognized first-call firm for real estate and commercial litigation in New York.", S["subsection"]))
story.append(quote_block("No transcript available — DBM inferred from 20+ year history, multi-office expansion, video podcast investment, and 'large law firm experience with personal service' positioning."))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Market Visibility.</b> The firm's expertise findable by clients searching online — not just referral sources."))
story.append(bd("<b>Predictable Case Flow.</b> A reliable pipeline independent of who happens to make a referral call."))
story.append(bd("<b>Systems-Driven Growth.</b> A firm where nine attorneys operate efficiently without the managing partner in every decision."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No Digital Presence.</b> Zero paid ads, no LSA, not in the 3-pack — all online traffic goes to competitors."))
story.append(b("<b>Reputation Risk.</b> 3.6 stars / 24 reviews; recent reviews negative. Goldberg &amp; Lindenberg: 57 reviews at 4.2★."))
story.append(b("<b>Weak Intake.</b> Contact form buried, no live chat — any new marketing will under-convert."))
story.append(b("<b>Revenue Unconfirmed.</b> $1M is a third-party estimate only — qualify actual figure early in the call."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts the firm at the top of every Manhattan real estate attorney search — converting 20 years of expertise into steady inbound cases."))
story.append(bd("LSA enrollment and GBP recovery give the Google Screened badge and rebuild trust signals above the 4.0-star threshold."))

story.append(Paragraph("<b>Full Service Marketing Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("NYC Tier 1, high-CPL legal market — requires full-service management across Google Ads, LSA, local SEO, and Meta."))
story.append(b("Website rebuild needed: contact form buried, blog stalled 12+ months, mobile performance unconfirmed."))
story.append(b("Conservative $10K ad spend: est. 13 cases x $9K avg = $117K/mo, ~11.7x return. All figures are estimates."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the intake system and KPI framework that turns new lead flow into signed cases at a predictable conversion rate."))
story.append(bd("Structured path from Stage 4 (owner-operator) to Stage 5 (CEO) — gives Stephen his time back without a new full-time hire."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("~$1M revenue, 12-person team, three offices — weekly group coaching and masterminds for Stage 4 to 5 transition."))
story.append(b("No confirmed intake process or KPI framework — coaching addresses both. Stand-alone $3,497; bundle saves $297/mo."))


# PAGE 2
story.append(PageBreak())

story.append(Paragraph("Lasser Law Group — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Captures landlord, property manager, and board member intent traffic currently going to Goldberg &amp; Lindenberg and Belkin Burden Goldman."))
story.append(bd("One signed commercial litigation matter at $10K–$30K recovers a full month of ad spend — making this the highest-leverage investment available."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $10,000/mo — PPC $3,500 + LSA $2,000 + Meta Ret $1,200 + Meta Lead $3,500 = $10,200."))
story.append(b("<b>Aggressive:</b> $25,000/mo — Starter tier cap. Scaling beyond $25K requires Growth tier ($7,397/mo fee)."))

story.append(Paragraph("<b>Estimated ROI (estimates only, not guaranteed):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 85 leads x 15% = 13 cases x $9,000 = $117,000/mo vs. $10,000 = 11.7x return."))
story.append(b("<b>Aggressive:</b> 255 leads x 15% = 38 cases x $9,000 = $342,000/mo vs. $25,000 = 13.7x return."))
story.append(Paragraph("<i>Business Law CPL benchmarks, NYC Tier 1. Blended case value — commercial litigation averages higher. No transcript to confirm close rate.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the numbers were built:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Channel minimums. PPC $3,500 + LSA $2,000 + Meta $2,700 = $10,200 rounded to $10,000."))
story.append(b("<b>Aggressive:</b> $2M goal x 20% / 12 x 1.5 (Tier 1) = $50,000 — capped at Starter limit of $25,000."))
story.append(b("$8,047 + $10,000 = $18,047/mo = ~1.8% of revenue. Aggressive $33,047 = ~3.3%. Both under the 35% cap."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We get enough work from referrals."', S["objection_q"]))
story.append(Paragraph("Referrals have a ceiling. Goldberg & Lindenberg has 57 Google reviews at 4.2 stars and appears in every Manhattan landlord-tenant search. That gap grows every month without action.", S["objection_a"]))

story.append(Paragraph('"Our Google rating has some issues."', S["objection_q"]))
story.append(Paragraph("3.6 stars / 24 reviews with a May 2026 critical review is the first thing a new prospect sees. Systematic review generation can recover above 4.0 in 60–90 days — but only if it starts now.", S["objection_a"]))

story.append(Paragraph('"Is the timing right? We\'re busy managing three offices."', S["objection_q"]))
story.append(Paragraph("Urgency score: 7/10. Belkin Burden Goldman (60 attorneys, Chambers-ranked) and Gallet Dreyer & Berkey (50+ years in condo/co-op) are not waiting. Every month extends their lead.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Starter</b>", S["price_main"]), Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, website rebuild, local SEO, Meta ads, monthly reporting.", S["price_detail"]), Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]), Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, masterminds, intake optimization, KPI framework, workshops.", S["price_detail"]), Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]), Paragraph("$10,000–$25,000/mo", S["price_main"])],
    [Paragraph("Goes to Google, LSA, and Meta — not to SMB Team.", S["price_detail"]), Paragraph("", S["price_detail"])],
]
pt = Table(price_data, colWidths=[4.5 * inch, 1.7 * inch])
pt.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 4), ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ("TOPPADDING", (0,0), (-1,-1), 2), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
    ("LINEBELOW", (0,3), (-1,3), 0.5, RULE_GRAY),
    ("LINEBELOW", (0,5), (-1,5), 0.5, RULE_GRAY),
]))
story.append(pt)
story.append(Paragraph(
    "Total: $8,047/mo + $10,000–$25,000 ad spend  |  Save $1,147/mo by bundling  |  1.8%–3.3% of revenue (under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
