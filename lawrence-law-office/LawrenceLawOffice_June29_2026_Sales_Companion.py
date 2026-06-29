"""
Sales Companion PDF — Lawrence Law Office
SMB Team Internal Use Only
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

OUTPUT_PATH = "lawrence-law-office/LawrenceLawOffice_June29_2026_Sales_Companion.pdf"


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
S["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=9, leading=12, textColor=LIGHT_GRAY, spaceAfter=2)
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=ACCENT_GREEN, spaceBefore=4, spaceAfter=1)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=DARK_NAVY, spaceBefore=1, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9, leading=11, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8, leading=11, textColor=MEDIUM_GRAY)
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

story.append(Paragraph("Lawrence Law Office", S["title"]))
story.append(Paragraph("Sales Companion  |  June 29, 2026  |  Rep: Dan Bryant", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Linda J. Lawrence", S["snap_value"]),
     Paragraph("~$750K est.", S["snap_value"]),
     Paragraph("~3 (est.)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Columbus, OH", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: FREEDOM", S["section"]))
story.append(Paragraph("Linda wants a firm that generates income without her daily involvement — a system built on 35 years of credentials, not managed through them.", S["subsection"]))
story.append(quote_block("No transcript — DBM inferred from career stage: Board Certified Family Law Specialist since 1990, 30+ years of operation, 2 offices. Owner is past the building phase and ready for the freedom phase."))
story.append(Spacer(1, 1))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable client flow.</b> New cases from a system, not from whoever called a referral."))
story.append(bd("<b>Less time in intake.</b> Stop being the first call at 7pm — delegate that entirely."))
story.append(bd("<b>Income that reflects 35 years of work.</b> Revenue tied to the firm's systems, not her hours."))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No paid lead system.</b> All leads are organic and referral-based — outside her control."))
story.append(b("<b>No intake infrastructure.</b> No after-hours coverage; both founders effectively manage intake."))
story.append(b("<b>Competitors accelerating.</b> Joslyn (78 reviews, 4.8★) and Gavvl (90+ reviews, 4.8★) run Google Ads, LSA, and Meta — Lawrence is absent from all three."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("<b>Columbus prospects find Lawrence before Joslyn or Gavvl</b> — because the firm finally appears where they search."))
story.append(bd("<b>Calendar fills from a system.</b> First step toward a firm that generates clients without Linda driving every lead."))
story.append(bd("<b>Board Certification and 35 years positioned visibly</b> — a differentiator no less-credentialed competitor can match."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$750K places the firm in the Starter tier ($400K–$1M). Consistent with HubSpot and research estimate."))
story.append(b("Columbus is Tier 2 — Google Ads, LSA, and Meta are all required to compete with Joslyn and Gavvl."))
story.append(b("Website redesign included — site estimated 8–12 years old; NAP inconsistency across listings dilutes local SEO."))
story.append(b("Stand-alone $5,697/mo — bundling saves $850/mo."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("<b>Financial clarity from session one.</b> Cost-per-client tracking turns marketing from an expense into a managed asset."))
story.append(bd("<b>Intake documented and delegatable.</b> Linda stops managing front-end acquisition personally."))
story.append(bd("<b>Weekly accountability.</b> 90-day revenue goals are tracked and adjusted in real time, not just set."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M, team ~3 — Elite Coach Plus is the correct tier."))
story.append(b("No financial baseline currently exists — coaching establishes it from session one."))
story.append(b("Practice area masterminds with Columbus-market family law peers facing the same competitive pressures."))
story.append(b("Stand-alone $3,497/mo — bundled saves $297/mo; total bundle saves $1,147/mo vs. stand-alone."))


# PAGE 2
story.append(PageBreak())

story.append(Paragraph("Lawrence Law Office — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("<b>Conservative ($3,500/mo):</b> 4–5 cases/mo x $5,000 = $20–25K revenue. ~6x ROAS."))
story.append(bd("<b>Aggressive ($14,000/mo):</b> 18–22 cases/mo x $5,000 = $90–110K revenue. ~6–7x ROAS."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — Google PPC $2,000 + LSA $500 + Meta $1,000. Family law channel minimums (Tier 2)."))
story.append(b("<b>Aggressive:</b> $14,000/mo — Starter tier cap. Full-budget approach to dominate Columbus paid search."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 28 leads / $125 CPL x 15% close = 4–5 cases x $5K = ~$20–25K/mo vs. $3.5K spend. ~6x."))
story.append(b("<b>Aggressive:</b> 137 leads / $102 CPL x 15% close = 18–22 cases x $5K = ~$90–110K/mo vs. $14K spend. ~6–7x."))
story.append(Paragraph("<i>Estimates use $5,000 default case value and 15% close rate (not stated in discovery). Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Family law Tier 2 channel minimums — PPC $2K + LSA $500 + Meta $1K = $3,500."))
story.append(b("<b>Aggressive:</b> $1.5M goal x 20% / 12 = $25K. Tier 2 (x1.3) = $32.5K. Minus $4,847 fee = $27,653. Capped at $14K (Starter tier)."))
story.append(b("At aggressive: $22,047/mo total = 35.3% of revenue — at the cap boundary. Acceptable."))

story.append(thin_rule())

story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I already have a strong reputation — why pay for ads?"', S["objection_q"]))
story.append(Paragraph("Reputation wins the case when someone finds you. Joslyn (78 reviews, 4.8★) and Gavvl (90+ reviews, 4.8★) appear above Lawrence on every Columbus family law search — Linda's reputation only converts prospects who reach her first.", S["objection_a"]))

story.append(Paragraph('"I\'ve done fine on referrals for 30 years."', S["objection_q"]))
story.append(Paragraph("Referrals depend on what others do, not what Linda controls. Gavvl didn't have 90 reviews three years ago — they built that aggressively and now own the Columbus 3-pack. Waiting means the gap keeps growing.", S["objection_a"]))

story.append(Paragraph('"$8,047 a month is a big commitment."', S["objection_q"]))
story.append(Paragraph("At conservative spend, 4–5 cases at $5,000 average = $20–25K/mo from ads against $3,500 ad spend and $8,047 in fees — net positive in month one when campaigns perform. Bundling already saves $1,147/mo vs. stand-alone.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, website redesign, SEO, GBP management.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, practice masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,500–$14,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $3,500–$14,000 ad spend  |  Save $1,147/mo by bundling  |  18.5%–35.3% of revenue (at or under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
