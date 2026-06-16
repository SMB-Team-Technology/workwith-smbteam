"""
Sales Companion PDF — The Eichholz Law Firm
Sales Rep: Michael Kopp
Proposal Call: June 19, 2026
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

OUTPUT_PATH = "the-eichholz/TheEichholzLawFirm_June19_2026_Sales_Companion.pdf"


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


# ══════════════════════════════════════════════════════════
# PAGE 1
# ══════════════════════════════════════════════════════════
story = []

story.append(Paragraph("The Eichholz Law Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  June 19, 2026  |  Rep: Michael Kopp", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("David Eichholz", S["snap_value"]),
     Paragraph("$5.2M/yr", S["snap_value"]),
     Paragraph("3+ staff", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (est.)", S["snap_value"]),
     Paragraph("Savannah, GA", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.1*inch, 0.8*inch, 0.7*inch, 0.8*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 3))

story.append(Paragraph("Dominant Buying Motive: VINDICATION &amp; DOMINATION", S["section"]))
story.append(Paragraph("David wants to prove the growth path was right and restore the firm to its $13M peak — with someone who believes that is achievable.", S["subsection"]))

story.append(quote_block("The firm is unprofitable — projecting a -$130k net loss on $5.2M revenue."))
story.append(Spacer(1, 1))
story.append(quote_block("A healthy PI firm should target 23-31% net profit. David's firm has never achieved this."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Return to $13M.</b> His stated goal — not incremental recovery, full market dominance."))
story.append(bd("<b>Prove the vision was right.</b> The decline is personal; he needs a partner who believes growth, not contraction."))
story.append(bd("<b>Handle the 2027 balloon from strength.</b> $2.1M due end of 2027 — needs a growing pipeline now."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Unprofitable cost structure.</b> Payroll rose from 25% to 42% of revenue as the firm contracted."))
story.append(b("<b>Advertising paused.</b> Casino (1,057 reviews) and Hostilo (628 reviews) are buying every PI keyword while Eichholz is absent."))
story.append(b("<b>COO-owner stalemate.</b> No governance framework — every decision requires David personally."))
story.append(b("<b>Pipeline gap risk.</b> Cutting ads now means 2027 revenue arrives at its thinnest when the balloon is due."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts Eichholz back in the Savannah PI auction — where it historically dominated — while Casino and Hostilo are actively buying."))
story.append(bd("Builds the case pipeline through 2026 so the 2027 balloon arrives with growing revenue, not a depleted docket."))

story.append(Paragraph("<b>Full Service Marketing — Platinum  |  $15,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $5.2M ($3M+): Platinum tier. All Essentials tiers hidden for PI firm."))
story.append(b("Platinum ad spend cap $40,000/mo — matches aggressive market recovery scenario."))
story.append(b("Stand-alone $18,997/mo. Bundled with coaching saves $3,000/mo on this package."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Establishes profit targets and a monthly review cadence — making profitability an operational output, not a year-end surprise."))
story.append(bd("Provides the leadership alignment framework to let David execute his direction without COO-level stalemates blocking every move."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1M+, team under 5: Elite Coach Plus selected (Master's Circle requires 5+ team)."))
story.append(b("Weekly group coaching + PI masterminds + quarterly workshops + annual in-person."))
story.append(b("Stand-alone $3,497/mo. Bundled with marketing saves $297/mo."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Eichholz Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Re-enters the Google Ads auction immediately — where the firm was the dominant buyer at $80-$90 CPC before the pullback."))
story.append(bd("Generates measurable, tracked leads so ROI is visible at the case level — unlike the prior $3.5M in untracked TV/radio spend."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $10,000/mo — Google Ads $6K + LSA $3K + Meta retargeting $1K."))
story.append(b("<b>Aggressive:</b> $40,000/mo — full Platinum tier capacity across Savannah + Atlanta markets."))

story.append(Paragraph("<b>Estimated ROI (estimates only — not guaranteed):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~12 cases x $15,000 avg = ~$180,000/mo from $10,000 spend = ~18x return."))
story.append(b("<b>Aggressive:</b> ~56 cases x $15,000 avg = ~$840,000/mo from $40,000 spend = ~21x return."))
story.append(Paragraph("<i>Case value $15K is conservative floor. Firm documents $100K-$400K settlements. 15% close rate (default). Results vary.</i>", S["disclaimer"]))
story.append(b("Total aggressive SMB spend: $19,197 + $40,000 = $59,197/mo = 13.7% of revenue. Under 35% cap."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We are losing money — adding $19K/mo makes it worse."', S["objection_q"]))
story.append(Paragraph("The prior spend ($3.5M-$4.5M/yr) was untracked TV and radio with no case-level ROI. SMB Team at $15,997/mo is managed and measured — every dollar tied to CPL and case value data. The problem was not advertising; it was unmanaged advertising with a broken cost structure.", S["objection_a"]))

story.append(Paragraph('"The COO wants to cut back, not grow — I cannot get alignment."', S["objection_q"]))
story.append(Paragraph("The Elite Coach Plus coaching relationship is specifically designed to resolve leadership alignment. Starting coaching now — not after the stalemate self-resolves — gives David an external framework to make the growth decision with accountability behind it.", S["objection_a"]))

story.append(Paragraph('"Can we start smaller and scale up later?"', S["objection_q"]))
story.append(Paragraph("With a 2027 balloon approaching and Casino actively buying every PI keyword in Savannah, a conservative start risks arriving at the deadline with a thin pipeline. Platinum is the minimum tier for a $5.2M PI firm pursuing market recovery — starting below it concedes the market while getting up to speed.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Platinum</b>", S["price_main"]),
     Paragraph("$15,997/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, local SEO, website optimization.", S["price_detail"]),
     Paragraph("<strike>$18,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, PI masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$10,000–$40,000/mo", S["price_main"])],
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
    "Total: $19,197/mo + $10,000–$40,000 ad spend  |  Save $3,297/mo by bundling  |  6.7%–13.7% of revenue (under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
