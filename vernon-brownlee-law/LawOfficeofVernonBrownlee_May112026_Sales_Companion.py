"""\nSales Companion PDF — The Law Office of Vernon Brownlee\nSales Rep: Dan Bryant | Date: May 11, 2026\n"""

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

OUTPUT_PATH = "/home/user/workwith-smbteam/vernon-brownlee-law/LawOfficeofVernonBrownlee_05112026_Sales_Companion.pdf"


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
    topMargin=0.65 * inch, bottomMargin=0.42 * inch,
    leftMargin=0.6 * inch, rightMargin=0.6 * inch,
)

S = {}
S["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=9, leading=12, textColor=LIGHT_GRAY, spaceAfter=2)
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=ACCENT_GREEN, spaceBefore=5, spaceAfter=1)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=10, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=10, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=5, rightIndent=5, spaceBefore=1, spaceAfter=1)
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
        ("BACKGROUND", (0,0), (-1,-1), QUOTE_BG),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
    ]))
    return t


# ══════════════════════════════════════════════════════════
# PAGE 1
# ══════════════════════════════════════════════════════════
story = []

story.append(Paragraph("The Law Office of Vernon Brownlee", S["title"]))
story.append(Paragraph("Sales Companion  |  May 11, 2026  |  Rep: Dan Bryant", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Vernon Brownlee", S["snap_value"]),
     Paragraph("$600K–$720K", S["snap_value"]),
     Paragraph("Solo + 1 asst.", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("70% qual./able-to-pay", S["snap_value"]),
     Paragraph("Upper Marlboro, MD", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.0*inch, 0.85*inch, 0.65*inch, 1.2*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 3))

story.append(Paragraph("Dominant Buying Motive: REPUTATION &amp; FREEDOM", S["section"]))
story.append(Paragraph("Vernon wants to be PG County's go-to serious felony trial attorney — with a firm that runs without him so he can be fully present in the courtroom.", S["subsection"]))

story.append(quote_block("Ambition: build reputation on serious trials now; steady, controlled growth, not volume."))
story.append(Spacer(1, 1))
story.append(quote_block("Estimates losing 2–5 signed cases per month due to web and intake failures. Approximately 25% of qualified prospects can't afford fees — no financing option offered."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Serious felony reputation.</b> To be known as PG County's go-to murder and serious felony trial attorney."))
story.append(bd("<b>Firm that runs without him.</b> Walk into every trial knowing intake is covered and no case is lost while he's in the courtroom."))
story.append(bd("<b>Financial clarity.</b> Know what the firm earns — not discover profitability at year-end."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Broken mobile website.</b> Nav, phone, and CTAs disappear on mobile — ~50 qualified leads lost to broken contact form."))
story.append(b("<b>No after-hours coverage.</b> Criminal defense calls peak evenings/weekends; firm unreachable 16 hrs/day."))
story.append(b("<b>No paid advertising.</b> Google Ads, LSA, Meta all paused ~1 year ago; competitors capture every high-intent search."))
story.append(b("<b>Prior agency mistrust.</b> Two years at $2,000–$2,400/mo with no attribution — couldn't identify what worked."))

story.append(thin_rule())

story.append(Paragraph("Why These Packages", S["section"]))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(bd("Rebuilt mobile site stops the invisible 2–5 case/month bleed from broken UX and missing CTAs."))
story.append(bd("Google Ads + LSA puts Vernon's name at the top of 'murder attorney PG County' — currently goes to FrizWoods, Mooney, and Jezic &amp; Moyse exclusively."))
story.append(b("Starter tier: $600K–$720K revenue; serious felony + high competitiveness disqualifies Essentials; website rebuild requires Full Service."))
story.append(b("$5,000/mo ad spend meets Criminal Defense + High competitiveness hard floor exactly at Starter tier cap."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>Elite Coach Plus  |  $2,200/mo bundled</b>", S["subsection"]))
story.append(bd("Intake delegation framework lets Vernon be present in trial — new inquiries handled without him as single point of failure."))
story.append(bd("Monthly profit plan in Clio Manage turns $600K+ in revenue into planned income, not a year-end surprise."))
story.append(b("Under $1M revenue; mentions profit concern and no financial visibility — Elite Coach Plus use case; fractional packages not eligible."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Vernon Brownlee — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(bd("Paid ads capture 'murder attorney Prince George's County' — the searches that currently go exclusively to competitors."))
story.append(bd("LSA pay-per-call means the firm only pays when a qualified prospect calls directly — highest-intent leads in criminal defense."))
story.append(Paragraph("<b>Recommended: $5,000/mo</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Criminal Defense minimums — PPC $2,500 + LSA $1,000 + Meta $1,500 = $5,000. Meets hard floor."))
story.append(b("<b>Aggressive capped at Starter:</b> 20% rule yields $25K+ available but Starter cap = $5,000. Upgrade at $1M+ revenue."))
story.append(b("<b>Conservative ROI:</b> 5 cases x $5,000 = $25,000/mo vs. $5,000 spend = 5x return on ad spend."))
story.append(b("<b>Aggressive ROI:</b> 8 cases x $5,000 = $40,000/mo vs. $5,000 spend = 8x return on ad spend."))
story.append(Paragraph("<i>Estimates only. Not guaranteed. Results vary based on market conditions.</i>", S["disclaimer"]))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I\'ve already spent money on agencies and it didn\'t work."', S["objection_q"]))
story.append(Paragraph("No attribution framework meant there was no way to know what was working. SMB provides full lead-to-signed-case attribution. The agency gap was accountability, not marketing.", S["objection_a"]))

story.append(Paragraph('"I need 3–5x ROI to justify this."', S["objection_q"]))
story.append(Paragraph("Conservative scenario: 5 cases x $5K = $25K vs. $7,047 SMB fees = 3.5x on management fees. Aggressive = 5.7x. His own threshold is inside the conservative case.", S["objection_a"]))

story.append(Paragraph('"Can I afford this right now?"', S["objection_q"]))
story.append(Paragraph("$7,047/mo = 14.1% of ~$50K/mo revenue. The 35% cap allows up to $17,500/mo at this revenue level — he is at less than half the sustainable investment ceiling.", S["objection_a"]))

story.append(Paragraph('"The website and intake need to be fixed first before I invest in ads."', S["objection_q"]))
story.append(Paragraph("The Starter package fixes both simultaneously — ads launch in week 1 while the rebuild runs in parallel. Waiting means another month of high-intent searchers going to FrizWoods and Jezic &amp; Moyse.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, Google Ads, LSA, local SEO, Meta retargeting.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$2,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, intake framework, profit plan, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,000/mo", S["price_main"])],
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
    "Total: $7,047/mo SMB fees + $5,000/mo ad spend  |  Save $2,147/mo by bundling  |  24.1% of revenue (under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pdfrw import PdfReader
r = PdfReader(OUTPUT_PATH)
print(f"Page count: {len(r.pages)}")
if len(r.pages) != 2:
    print("WARNING: Must be exactly 2 pages.")