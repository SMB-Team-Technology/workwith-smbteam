"""
Sales Companion PDF — Jeff Anderson Family Law, PLLC
SMB Team Internal — Do Not Share
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

OUTPUT_PATH = "onda-family-law/JeffAndersonFamilyLaw_06182026_Sales_Companion.pdf"


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
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=ACCENT_GREEN, spaceBefore=5, spaceAfter=2)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9, leading=11, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
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

story.append(Paragraph("Jeff Anderson Family Law, PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  June 18, 2026  |  Rep: Dan Bryant", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Jeff Anderson", S["snap_value"]),
     Paragraph("~$500K est.", S["snap_value"]),
     Paragraph("3 est.", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("Frisco/Dallas/San Antonio TX", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.1*inch, 1.1*inch, 0.8*inch, 0.7*inch, 0.85*inch, 1.65*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 3))

story.append(Paragraph("Dominant Buying Motive: SCALE AND DOMINATE", S["section"]))
story.append(Paragraph("Jeff wants a competent partner to fix his digital foundation so he can scale into the dominant practice his 30-year Board Certified credentials have already earned.", S["subsection"]))

story.append(quote_block("primarily divorce; second most child custody modifications; also enforcements and protective orders"))
story.append(Spacer(1, 1))
story.append(quote_block("firm expanding space and headcount in approximately six months; wants +20% lead growth now, more later"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Digital presence matching his credentials.</b> Board Certified, Top 100 TX, 30 years — but invisible in Maps and absent from every paid channel."))
story.append(bd("<b>+20% leads now with a clear expansion path.</b> Explicit near-term goal tied to planned space and staff additions in 6 months."))
story.append(bd("<b>A partner who does not make technical mistakes.</b> Vendor failures (malware, errors, wrong numbers) created deep frustration; he wants competence."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Vendor failures.</b> Malware, content errors, wrong phone numbers, cross-contaminated location pages — technical debt never resolved."))
story.append(b("<b>Review gap.</b> 22 Google reviews vs. Pfister 240+, Ramage 317+ — structurally invisible in the 3-pack until this closes."))
story.append(b("<b>No call tracking.</b> Cannot attribute which sources generate calls; every marketing decision is a guess."))
story.append(b("<b>Bad LSA experience.</b> Prior LSAs produced unqualified leads — makes him cautious about paid channel investment."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Paid visibility in the high-intent divorce and custody searches Jeff is currently absent from — from day one."))
story.append(bd("Full attribution via CallRail — every call tracked, every dollar accounted for, investment decisions data-driven."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Organic traffic declining 2.5+ years; zero paid channels running while competitors buy every relevant search position."))
story.append(b("Website has malware history, content errors, NAP inconsistencies — full service rebuild required before ads launch."))
story.append(b("3 locations plus expansion require full scope: website, GBP, PPC, local SEO, and citations across all markets."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Planned expansion — new space, staff, Dallas and San Antonio — happens with structure and accountability rather than instinct."))
story.append(bd("Expert guidance on every growth decision so Jeff is not navigating team-building and ops expansion alone."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$400K–$1M — Elite Coach Plus is the correct tier; Master's Circle requires $1M+ and 5+ dedicated staff."))
story.append(b("Staff expansion planned in 6 months — needs coaching framework before adding headcount to avoid unstructured growth."))
story.append(b("Hunter referral with record SMB profit months is the proof point; Jeff wants the same results from the same model."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Jeff Anderson Family Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Paid visibility in Frisco and Dallas searches Jeff is invisible in — converting high-intent prospects searching right now."))
story.append(bd("Measurable return on tracked investment with CallRail; CPL and ROI visible from day one."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative $3,500/mo:</b> Google PPC + Meta for Frisco/Dallas; minimum viable for meaningful paid visibility."))
story.append(b("<b>Aggressive $7,000/mo:</b> Starter tier cap; 4–6 cases/month at projected ROI."))
story.append(b("<b>Conservative ROI:</b> ~2–3 cases x $20K avg = $40K–$60K/mo vs. $3,500 spend = ~11–17x (est.)."))
story.append(b("<b>Aggressive ROI:</b> ~4–6 cases x $20K avg = $80K–$120K/mo vs. $7,000 spend = ~12–17x (est.)."))
story.append(Paragraph("<i>Estimates only. Default case value $20,000 — confirm with Jeff before proposal.</i>", S["disclaimer"]))
story.append(b("35% cap: $8,047 + $3,500 = $11,547 = 27.7% of $500K revenue — within cap at conservative. Flag aggressive with Dan."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We tried LSAs and the leads were terrible — low income, unqualified."', S["objection_q"]))
story.append(Paragraph("LSA issue was broad targeting with no filters — not a platform problem. Recommended path is smart PPC with CallRail, Board Certified and high-net-worth keyword targeting, and negative keyword exclusions. Pfister (240+ reviews) and Ramage (317+) are in those LSA spots now.", S["objection_a"]))

story.append(Paragraph('"The website was just redesigned — why rebuild it again?"', S["objection_q"]))
story.append(Paragraph("The current vendor introduced malware, typos, wrong phone numbers, and cross-contaminated city content. PageSpeed expected below 50 mobile. These inflate Google Ads CPCs and suppress local rankings. Rebuilding on a clean foundation costs less than paying premium CPCs on a broken one.", S["objection_a"]))

story.append(Paragraph('"$8,000 a month feels like a lot right now."', S["objection_q"]))
story.append(Paragraph("At $3,500 conservative ad spend, total is $11,547/mo. Projected return at 2–3 cases x $20K avg = $40K–$60K/mo revenue. That is a 3.5–5x return on total spend — and the competitor gap (Pfister: 240 reviews, Jeff: 22) widens every month without action.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, GBP management, Google PPC with CallRail, local SEO, citation management.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, family law masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,500–$7,000/mo", S["price_main"])],
    [Paragraph("Goes to Google and Meta — not to SMB Team.", S["price_detail"]),
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
    "Total: $8,047/mo + $3,500–$7,000 ad spend  |  Save $1,147/mo by bundling  |  27.7%–36.1% of revenue",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
