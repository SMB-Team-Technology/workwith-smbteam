"""
Sales Companion PDF — Leibowitz Law Firm PLLC
SMB Team | Jonathan Farace | June 8, 2026
FOR INTERNAL USE ONLY — DO NOT SHARE WITH CLIENT
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

OUTPUT_PATH = "leibowitz-law-firm/Leibowitz_Law_Firm_PLLC_06082026_Sales_Companion.pdf"


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
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.5, leading=12, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9.5, leading=12, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9.5, leading=13, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9.5, leading=12, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9.5, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=1)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8.5, leading=11, textColor=MEDIUM_GRAY)
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

story.append(Paragraph("Leibowitz Law Firm PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  June 8, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Jake Leibowitz", S["snap_value"]),
     Paragraph("$300K–$750K est.", S["snap_value"]),
     Paragraph("Solo (1 atty)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("San Antonio, TX", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: FAMILY TIME + SCALE", S["section"]))
story.append(Paragraph("Jake wants consistent high-value truck and PI cases so he can build a firm that runs without him — and be present for his wife and two kids.", S["subsection"]))

story.append(quote_block("No transcript available. DBM inferred from Avvo profile: motivated by helping 'the underdog' and families standing up to corporations. Married with two children."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable truck and PI cases.</b> High-value cases from digital channels — not just referrals."))
story.append(bd("<b>Family time.</b> Two kids at home; wants to step back without the firm stalling."))
story.append(bd("<b>Dominant South Texas PI brand.</b> Bilingual + ATAA specialization = a market position nobody is occupying."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No digital presence.</b> Zero 3-pack, paid search, LSA, or Meta ads — competitors own every channel."))
story.append(b("<b>Under 10 Google reviews.</b> Competitors have 125–1,207; review gap is the primary blocker."))
story.append(b("<b>Three NAP inconsistencies.</b> Wrong address/phone on Yellow Pages, FindLaw, LawyerLegion."))
story.append(b("<b>Broken contact form.</b> Prospects can't submit inquiries; motivated leads are leaving the site."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the SEO and review foundation before paid ads — the right sequence for a firm starting from zero digital presence."))
story.append(bd("Bilingual practice area pages for San Antonio + three RGV counties unlock a market no competitor is serving digitally."))
story.append(bd("Review velocity toward 50+ enables LSA qualification and local 3-pack eligibility — unlocking the two highest-ROI channels."))

story.append(Paragraph("<b>Web &amp; SEO Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("PI high-competition market — foundation phase required before paid ads; no practice area pages or geo content currently exist."))
story.append(b("Review count is 10 vs. 125–1,207 for competitors; structured review program is prerequisite for everything else."))
story.append(b("Squarespace platform with no bilingual content for Edinburg, Brownsville, Laredo — unique competitive moat available."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Dedicated FCOO maps intake and builds delegation SOPs — team structure Jake needs to absorb the lead volume marketing creates."))
story.append(bd("Weekly coaching + mastermind keeps Jake building the business, not just practicing law — direct path to hiring first intake coordinator."))

story.append(Paragraph("<b>FCOO Advisor  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Solo with no team — FCOO builds the operational infrastructure before marketing scales beyond Jake's personal capacity."))
story.append(b("Includes Elite Coach group deliverables: weekly sessions, masterminds, quarterly and annual workshops."))
story.append(b("PACKAGE OVERRIDE from trigger file. Confirm firm revenue and readiness before proposal — 35% cap check required."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Leibowitz Law Firm PLLC — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend (Phase 2 Planning)", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Phase 2 paid ads launch once 50+ reviews achieved — Google Ads + LSA + Spanish Meta across San Antonio and South Texas."))
story.append(bd("Spanish-language campaigns in RGV markets Jake already serves but is currently invisible in digitally."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,500/mo — LSA-focused Phase 2 entry; below PI hard floor but appropriate for initial launch."))
story.append(b("<b>Aggressive:</b> $15,000/mo — multi-channel Google Ads + LSA + Spanish Meta targeting four-county South Texas footprint."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative ($7,500/mo):</b> ~11 leads x 15% = 2 cases x $25K = $50K/mo vs. $7.5K = 6.5x return (est.)."))
story.append(b("<b>Aggressive ($15,000/mo):</b> ~33 leads x 15% = 5 cases x $25K = $125K/mo vs. $15K = 8x return (est.)."))
story.append(Paragraph("<i>Estimates. $25K conservative default case value used — truck cases typically $75K–$200K+. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> PI high-competition entry. Blended CPL ~$677 (Google 70% + LSA 30% + 20% cushion)."))
story.append(b("<b>Aggressive:</b> $1M goal x 20% / 12 = $16,667. Tier 3 x 1.15 = $19,167. Spanish PI x 1.50 = $28,750. Minus fee = $23,903."))
story.append(b("At $500K rev: $8,144 + $15K = $23,144/mo = 55% of revenue — exceeds 35% cap. Confirm actual revenue before finalizing."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I get cases from referrals — why do I need digital?"', S["objection_q"]))
story.append(Paragraph("Referrals are finite. Carabin Shaw has 1,207 reviews and runs ads for Jake's exact keywords. Every referral he gets is a lead that found someone else first. Digital adds a second pipeline that does not depend on who Jake knows.", S["objection_a"]))

story.append(Paragraph('"My website is new — it should be fine."', S["objection_q"]))
story.append(Paragraph("Modern design but no practice area pages, no geo content for three of four counties served, and a contact form that did not render during testing. New websites that don't rank or convert are missed opportunities, not assets.", S["objection_a"]))

story.append(Paragraph('"I\'m a solo attorney — I can\'t afford $8K a month."', S["objection_q"]))
story.append(Paragraph("One truck accident case at $75K–$200K+ pays for over a year of SMB Team fees. The question is not whether Jake can afford it — it is whether he can afford watching competitors capture those cases while he waits for the next referral.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Web &amp; SEO Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Practice area pages, bilingual SEO, review program, directory cleanup, GBP management.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>FCOO Advisor</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Fractional COO + Elite Coach group deliverables (weekly sessions, masterminds, workshops).", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend (Phase 2)</b>", S["price_main"]),
     Paragraph("$7,500–$15,000/mo", S["price_main"])],
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
    "Total: $8,144/mo + $7,500–$15,000 ad spend  |  Save $1,350/mo by bundling  |  Confirm revenue (35% cap check required)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
