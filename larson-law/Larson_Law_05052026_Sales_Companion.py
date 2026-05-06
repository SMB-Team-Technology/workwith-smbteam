"""
Sales Companion PDF — Larson Law
Generated: May 05, 2026
Sales Rep: Jonathan Farace
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

OUTPUT_PATH = "larson-law/Larson_Law_05052026_Sales_Companion.pdf"


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
    topMargin=0.68 * inch, bottomMargin=0.42 * inch,
    leftMargin=0.6 * inch, rightMargin=0.6 * inch,
)

S = {}
S["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=9, leading=12, textColor=LIGHT_GRAY, spaceAfter=2)
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=ACCENT_GREEN, spaceBefore=4, spaceAfter=1)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=DARK_NAVY, spaceBefore=1, spaceAfter=0)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=0, spaceAfter=0)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=0, spaceAfter=0)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9, leading=11, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=1)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8, leading=11, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=2)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=LIGHT_GRAY, spaceBefore=0, spaceAfter=0)


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
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


# PAGE 1
story = []

story.append(Paragraph("Larson Law", S["title"]))
story.append(Paragraph("Sales Companion  |  May 05, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Adam Larson", S["snap_value"]),
     Paragraph("~$1.1M/yr", S["snap_value"]),
     Paragraph("&lt;5", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("South Jordan, UT", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: FREEDOM &amp; FINANCIAL SECURITY", S["section"]))
story.append(Paragraph("Adam wants to step out of the day-to-day, operate as CEO, and build a firm that generates real financial security — income not tied to his personal hours.", S["subsection"]))
story.append(Spacer(1, 2))

story.append(quote_block("I don't want to be an employee of my own business — I want to own it. Revenue has been flat for five years and I just took full ownership from my dad."))
story.append(Spacer(1, 1))
story.append(quote_block("95 to 98 percent of my cases come from referrals. I want to double revenue to $2.2M and have time for my family."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>CEO role.</b> Step back from operations; firm runs without him signing every case."))
story.append(bd("<b>Predictable income.</b> Revenue not tied to referrals or personal availability."))
story.append(bd("<b>Double revenue.</b> $1.1M to $2.2M with a controlled marketing system."))
story.append(bd("<b>Financial security.</b> Long-term wealth for family — retirement, stability, options."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No Google presence.</b> Near-zero reviews; not in 3-pack; competitors own every PI keyword."))
story.append(b("<b>Intake bottleneck.</b> Utah Bar requires Adam to personally sign every client; no after-hours coverage."))
story.append(b("<b>Referral dependency.</b> 95–98% referral-based; no marketing system; revenue flat 5 years."))
story.append(b("<b>No second attorney.</b> Hard cap on case volume; cannot step back from signing."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Replaces referral dependency with controlled lead flow — signed cases every month, not just when referrals come in."))
story.append(bd("Builds the Google presence (reviews, 3-pack, LSA) that competitors use to dominate every online PI search."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $7,397/mo bundled</b>", S["subsection"]))
story.append(b("PI firm: Essentials eliminated. $1M+ revenue: Growth band ($1M–$3M) is correct tier."))
story.append(b("Aggressive 2x revenue goal with line-of-credit funding — Growth more responsible than Dominate as entry."))
story.append(b("Path to Dominate upgrade at $1.5M+ when ad spend justifies the tier move."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("CEO transition framework — not just more leads, but a plan for stepping back from operations."))
story.append(bd("Intake systems, second attorney hire roadmap, and profit planning built alongside marketing."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1M+, team under 5: Elite Coach Plus is correct tier. Master's Circle requires 5+ dedicated staff."))
story.append(b("Full ownership transition just occurred — CEO coaching is highest-leverage use right now."))
story.append(b("FCOO Advisor added Phase 2 at 10+ signed cases/month; FCFO Advisor added Phase 3 at $1.5M+."))


# PAGE 2
story.append(PageBreak())

story.append(Paragraph("Larson Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Activates Google, LSA, and Meta simultaneously — Larson Law visible wherever PI prospects search."))
story.append(bd("At Adam's own $2,500 CAC target, $12K/mo = ~5 signed cases = ~$55K expected revenue per month."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $12,000/mo — channel minimums for PI/MVA high-competitiveness market."))
story.append(b("<b>Aggressive:</b> $20,000/mo — Growth tier cap; upgrade to Dominate at $1.5M+ for higher budget."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~6 cases x $11K = $66K/mo revenue vs. $12K spend = ~5.5x return."))
story.append(b("<b>Aggressive:</b> ~9 cases x $11K = $99K/mo revenue vs. $20K spend = ~5x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> PI/MVA high-comp minimums: PPC $5K + LSA $2K + Meta Retargeting $1.5K + Meta Cold $3.5K = $12K."))
story.append(b("<b>Aggressive:</b> $2.2M goal x 20% / 12 = $36,667. Tier 3 (x1.15) = $42,167. Minus $7,397 fee = $34,770. Capped at $20K."))
story.append(b("Total at aggressive: $30,597/mo = ~33.4% of $1.1M revenue. Under the 35% cap."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"Referrals have always come in — I\'m not sure I need ads right now."', S["objection_q"]))
story.append(Paragraph("Revenue flat 5 years on referrals. Kramer Law Group: 300+ Google reviews, active PPC — capturing every online PI case in Adam's market daily. Referrals cannot double revenue. A system can.", S["objection_a"]))

story.append(Paragraph('"I don\'t have budget — I might need a line of credit."', S["objection_q"]))
story.append(Paragraph("$12K/mo in ads = ~$55K expected revenue at Adam's own $2,500 CAC target. A line of credit to fund a 5x return is a business decision. The investment services itself within the first settlement cycle.", S["objection_a"]))

story.append(Paragraph('"I\'m the only attorney — I can only sign so many cases."', S["objection_q"]))
story.append(Paragraph("That's why coaching runs alongside marketing. Elite Coach Plus builds intake systems and a second attorney hire roadmap. Marketing creates the case volume that justifies and funds the hire.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta Ads, GBP optimization, review campaign, city landing pages.", S["price_detail"]),
     Paragraph("<strike>$7,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, masterminds, CEO transition plan, quarterly + annual workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$12,000–$20,000/mo", S["price_main"])],
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
    "Total: $10,597/mo + $12,000–$20,000 ad spend  |  Save $897/mo by bundling  |  24.6%–33.4% of revenue (under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

# Page count check without pypdf
with open(OUTPUT_PATH, 'rb') as f:
    content = f.read()
pages = content.count(b'/Type /Page\n') + content.count(b'/Type /Page ')
print(f"Page count (approximate): {pages}")
if pages != 2:
    print("WARNING: Sales Companion must be exactly 2 pages.")
