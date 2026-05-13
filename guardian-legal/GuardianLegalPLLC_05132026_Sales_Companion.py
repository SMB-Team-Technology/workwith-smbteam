"""
Sales Companion PDF — Guardian Legal PLLC
Sales Rep: Jacob Meissner | Date: May 13, 2026
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

OUTPUT_PATH = "/home/user/workwith-smbteam/guardian-legal/GuardianLegal_05132026_Sales_Companion.pdf"


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
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=ACCENT_GREEN, spaceBefore=4, spaceAfter=1)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9, leading=11, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8.5, leading=11, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


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

story.append(Paragraph("Guardian Legal PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  May 13, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Mariano Rodriguez", S["snap_value"]),
     Paragraph("Pre-settlement; $20–25K/mo spend", S["snap_value"]),
     Paragraph("4 (incl. owner)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Phoenix, AZ / Fort Lauderdale, FL", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.3*inch, 0.8*inch, 0.65*inch, 0.7*inch, 1.1*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 3))

story.append(Paragraph("Dominant Buying Motive: AUTOMATION &amp; FREEDOM", S["section"]))
story.append(Paragraph("Mariano wants an automated, self-running PI firm — owned marketing, 25 cases/month, and systems that let him step back.", S["subsection"]))

story.append(quote_block("I want to get to about 20 to 25 cases per month... I'd like to see about 3.36 million dollars a year."))
story.append(Spacer(1, 1))
story.append(quote_block("I want to be able to step back... kind of have an automated, system-driven firm."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Own marketing system.</b> Replace $2,000 purchased retainers with an owned engine that builds equity and drops cost-per-case over time."))
story.append(bd("<b>25 cases/month.</b> The specific milestone ($3.36M/year) he stated on the call — built on owned leads, not vendor dependency."))
story.append(bd("<b>Automated firm.</b> Documented workflows, a hiring plan, and financial visibility so he can step back from day-to-day decisions."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Zero online presence.</b> No GBP, no reviews, no ads — while Phillips Law Group (2,500+ reviews), Lamber Goodnow, and Lerner &amp; Rowe dominate every Phoenix PI channel."))
story.append(b("<b>Pre-settlement, no financial visibility.</b> $20–25K/mo funding leads with no cost-per-case tracking and no profit plan before first settlements arrive."))
story.append(b("<b>Intake gap.</b> 24/7 advertised, hourly intake staffed — every after-hours missed call is a $2,000 loss; ad spend multiplies the problem."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Replaces vendor dependency with owned Google Ads, LSA, and Meta campaigns that build the firm's audience and compound every month."))
story.append(bd("Gets Guardian Legal into the Phoenix local 3-pack and above paid ads via Google Screened — positions currently owned by Phillips and Lamber Goodnow."))

story.append(Paragraph("<b>Full Service Marketing Growth  |  $3,397/mo bundled</b>", S["subsection"]))
story.append(b("PI practice area requires minimum Starter; aggressive $3.36M goal triggers boundary rule — Growth tier with $15K ad spend cap is correct for Phoenix high-competition PI."))
story.append(b("Full service (not ads-only) required: site has unverified PageSpeed, broken 24/7 intake promise, and no trust signals — website optimization is a prerequisite for ad ROI."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the workflow documentation, hiring plan, and profit framework Mariano explicitly requested — the operating infrastructure behind the automated firm he described."))

story.append(Paragraph("<b>Elite Coach  |  $1,600/mo bundled</b>", S["subsection"]))
story.append(b("Pre-settlement revenue places firm under $250K — Elite Coach is correct tier. FCOO/CFO hidden under $500K; Master's Circle hidden under $1M and requires 5+ members."))
story.append(b("Note: bundled price ($1,600) is $103 above stand-alone ($1,497); offset by $600 savings on Growth marketing — net $497/mo saved overall."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Guardian Legal — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Replaces $2,000 purchased retainers with owned campaigns at $75–$300/lead — builds a compounding asset, not a recurring vendor cost."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative $10,000/mo:</b> PI hard floor (high competition Phoenix). Allocation: PPC $3,500 + LSA $2,500 + Meta RT $1,500 + Meta LG $2,500."))
story.append(b("<b>Aggressive $15,000/mo:</b> Growth tier cap. 20% rule ($56K) and reverse math ($33K) both exceed cap — $15K is the practical ceiling until revenue justifies tier upgrade."))

story.append(Paragraph("<b>Estimated ROI (not guaranteed):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~7–8 cases x $10,000 avg = $75,000/mo vs. $10,000 spend = ~7.5x return."))
story.append(b("<b>Aggressive:</b> ~14 cases x $10,000 avg = $140,000/mo vs. $15,000 spend = ~9.3x return."))
story.append(b("Blended CPL: PPC $200 | LSA $150 | Meta RT $100 | Meta LG $175. Close rate 15% (default). Case value $10,000 (stated on call)."))
story.append(b("Spend check: $15,000 ad + $4,997 mgmt = $19,997 = 7.1% of revenue goal ($280K/mo). Under 35% cap."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I\'m already spending $20–25K/mo on leads. I can\'t add more."', S["objection_q"]))
story.append(Paragraph("That spend builds nothing — it funds the vendor's asset. SMB Team ad spend builds a GBP with map pack authority, an LSA profile accumulating reviews, and a retargeting audience the firm owns. Purchased leads reset every month; owned marketing compounds.", S["objection_a"]))

story.append(Paragraph('"I\'m pre-settlement — the timing might not be right."', S["objection_q"]))
story.append(Paragraph("The 3–6 month ramp to owned marketing ROI means starting now puts first owned leads arriving as settlements close. Every quarter of delay is another quarter at $2,000/retainer with no asset built.", S["objection_a"]))

story.append(Paragraph('"Can we actually compete with Phillips Law Group and Lamber Goodnow?"', S["objection_q"]))
story.append(Paragraph("Yes — through LSAs (pay per verified call, ranked on review velocity not budget) and suburban targeting. Scottsdale, Mesa, Tempe, and Gilbert have lower CPCs than the city core and reach the same qualified PI audience. These are the entry points before competing head-to-head on 'car accident lawyer Phoenix.'", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Growth</b>", S["price_main"]),
     Paragraph("$3,397/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, website optimization, SEO — Phoenix AZ + Fort Lauderdale FL.", S["price_detail"]),
     Paragraph("<strike>$3,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$1,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, practice area masterminds, hiring guidance, workflow docs, profit plan.", S["price_detail"]),
     Paragraph("<strike>$1,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$10,000–$15,000/mo", S["price_main"])],
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
    "Total: $4,997/mo management + $10,000–$15,000 ad spend  |  Save $497/mo by bundling  |  7.1%–8.9% of revenue goal (under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

import re
with open(OUTPUT_PATH, 'rb') as f:
    content = f.read().decode('latin-1')
pages = len(re.findall(r'/Type\s*/Page\b', content))
print(f"Page count: {pages}")
if pages != 2:
    print("WARNING: Must be exactly 2 pages. Shorten bullet text to fit.")
