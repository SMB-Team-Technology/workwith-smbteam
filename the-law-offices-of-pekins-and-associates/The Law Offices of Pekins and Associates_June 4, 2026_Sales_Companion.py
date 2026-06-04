"""
Sales Companion PDF — The Law Offices of Pekins and Associates, PLLC
June 4, 2026 | Rep: Randy Gold
FOR INTERNAL USE ONLY. DO NOT SHARE WITH CLIENT.
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
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "the-law-offices-of-pekins-and-associates/The_Law_Offices_of_Pekins_and_Associates_06042026_Sales_Companion.pdf"


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
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.5, leading=12, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=0, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9.5, leading=12, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=0, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9.5, leading=13, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9.5, leading=12, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9.5, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=1)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8.5, leading=11, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


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
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


# ══════════════════════════════════════════════════════════
# PAGE 1
# ══════════════════════════════════════════════════════════
story = []

story.append(Paragraph("The Law Offices of Pekins and Associates, PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  June 4, 2026  |  Rep: Randy Gold", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]), Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]), Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]), Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Trina Perkins-Mouton", S["snap_value"]), Paragraph("~$400K–$600K est.", S["snap_value"]),
     Paragraph("Solo (1 atty)", S["snap_value"]), Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]), Paragraph("Houston, TX", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: LEGACY &amp; COMMUNITY MISSION", S["section"]))
story.append(Paragraph("She wants a firm that carries her values forward — serving Houston at scale — with financial stability freeing her from trading every hour for dollars.", S["subsection"]))

story.append(quote_block("DBM inferred from research (no transcript): 29-year brand identity ('The Queen of Justice'), client testimonials citing Christian values, documented specialty in expungements/non-disclosures for Houston's underserved community."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Community reach at scale.</b> Systems that serve more Houston clients without requiring her personal presence for every matter."))
story.append(bd("<b>Predictable income.</b> Referral-only revenue is unpredictable — she wants consistent case flow she can plan around."))
story.append(bd("<b>Freedom to focus on legal work.</b> Intake and operations should not require the attorney."))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Broken website.</b> Expired SSL triggers browser security warnings — every referral sent to the site hits this first."))
story.append(b("<b>Zero paid visibility.</b> No Google Ads, LSA, or Meta — invisible to every prospect actively searching in Houston."))
story.append(b("<b>Review gap.</b> 30 Google reviews vs. 1,364 for The Gonzalez Law Group — invisible in 3-pack for every competitive keyword."))
story.append(b("<b>Solo bottleneck.</b> All intake flows through her personally — growth increases workload with no leverage."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Puts a rebuilt, SSL-secured website and active ads in front of Houston PI and criminal defense prospects — the phone rings with new clients."))
story.append(bd("LSA enrollment places her 5.0-star rating above WestLoop Law and Gonzalez — at pay-per-lead, not pay-per-click."))
story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("PI in Houston (top-40 metro) requires minimum Starter — Essentials is ineligible for personal injury practices."))
story.append(b("Website rebuild required: SSL expired, site 5–10 years old — Full Service (not ads-only) is required."))
story.append(b("Stand-alone retail $5,697/mo — bundled saves $850/mo."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Builds the intake system and profit-tracking that converts increased lead flow into retained clients — not more noise hitting a broken process."))
story.append(bd("Weekly coaching and practice area masterminds give a 29-year solo practitioner accountability and a peer group she has never had."))
story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$600K = Elite Coach Plus tier ($400K–$1M range). Fractional COO/CFO ineligible under $500K. Master's Circle ineligible: fewer than 5 staff."))
story.append(b("Stand-alone retail $3,497/mo — bundled saves $297/mo."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Perkins &amp; Associates — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Puts the firm at the top of Google for PI and criminal defense — capturing clients currently finding WestLoop Law and Gonzalez instead."))
story.append(bd("The expungement/non-disclosure niche is high-demand in Houston; her 29-year track record is a moat no generalist competitor can match."))
story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $6,000/mo — Google Ads + LSA for PI and criminal defense. Within 35% cap at $500K+ estimated revenue."))
story.append(b("<b>Aggressive:</b> $10,000/mo — adds Meta retargeting and lead gen. Scale as confirmed revenue grows above $600K."))
story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative ($6,000/mo):</b> ~9 leads x 15% close x $8,000 avg PI case = ~$12,000/mo; ~2.0x return. (Estimates; default case value.)"))
story.append(b("<b>Aggressive ($10,000/mo):</b> ~23 leads x 15% close x $8,000 avg PI case = ~$24,000/mo; ~2.4x return. (Estimates; default case value.)"))
story.append(Paragraph("<i>All figures are estimates based on industry benchmarks. Not guaranteed.</i>", S["disclaimer"]))

story.append(thin_rule())

story.append(Paragraph("If She Pushes Back", S["section"]))
story.append(Paragraph('"I\'ve built this for 29 years without paid ads."', S["objection_q"]))
story.append(Paragraph("WestLoop Law is less than a mile away running PI campaigns in the same corridor. The Gonzalez Law Group has 1,364 reviews across your same practice areas. The referral model worked when competitors were not doing this — they are doing it now.", S["objection_a"]))

story.append(Paragraph('"My website needs to be fixed before I advertise."', S["objection_q"]))
story.append(Paragraph("Correct — the Starter package includes the full website rebuild. We launch ads to a temporary landing page while the rebuild runs so the firm does not lose a month of lead capture.", S["objection_a"]))

story.append(Paragraph('"I can\'t handle more cases by myself."', S["objection_q"]))
story.append(Paragraph("Elite Coach Plus builds the intake system first. Leads are handled by a process — not by the attorney — before ad volume scales. That is the design, not an afterthought.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]), Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, Google Ads, LSA, Meta, local SEO, reporting.", S["price_detail"]), Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]), Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, intake build, profit planning, first hire guidance, workshops.", S["price_detail"]), Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]), Paragraph("$6,000–$10,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $6,000–$10,000 ad spend  |  Save $1,147/mo by bundling  |  ~33–36% of est. revenue (under 35% cap at $600K+ confirmed rev)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
