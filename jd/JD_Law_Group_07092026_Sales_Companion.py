"""
Sales Companion PDF — JD Law Group
SMB Team Internal Document — DO NOT SHARE
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

OUTPUT_PATH = "jd/JD_Law_Group_07092026_Sales_Companion.pdf"


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
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=ACCENT_GREEN, spaceBefore=6, spaceAfter=2)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.5, leading=13, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9.5, leading=13, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9.5, leading=13, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9.5, leading=12, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9.5, leading=13, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8.5, leading=11, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


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

story.append(Paragraph("JD Law Group", S["title"]))
story.append(Paragraph("Sales Companion  |  July 9, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Doug Chanco", S["snap_value"]),
     Paragraph("$2.5M (2025)", S["snap_value"]),
     Paragraph("3 (2 atty+para)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("65% hist./down", S["snap_value"]),
     Paragraph("Roswell, GA", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: WORK IN THE BUSINESS", S["section"]))
story.append(Paragraph("Doug wants to practice law — solve legal puzzles — not manage the business behind it.", S["subsection"]))

story.append(quote_block("Doug prefers 'working in' the business (solving legal puzzles) over 'working on' it."))
story.append(Spacer(1, 1))
story.append(quote_block("Getting our lunch handed to us — 2026 case volume is a fraction of what it was in 2025."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Back to practicing law.</b> Off the operational treadmill; focused on cases."))
story.append(bd("<b>Systems that generate leads without him.</b> No managing marketing or intake personally."))
story.append(bd("<b>Revenue recovery.</b> Recover to $2.5M, then 20% annual growth."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Triple website crisis.</b> chancoschiffer.com indexed + roswelllegal.com has zero indexed pages — organic destroyed."))
story.append(b("<b>No paid ads running.</b> PPC and LSA stopped; poor ROI was likely a landing page problem, not a market problem."))
story.append(b("<b>88%/82% case volume collapse.</b> 2026 YTD: 35 criminal + 10 PI vs. 300 + 55 in full-year 2025."))
story.append(b("<b>No intake role or protocol.</b> Both attorneys absorb operational tasks; no defined digital follow-up process."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Rebuilds the digital foundation — one domain, LSAs live, GBP optimized — so leads come in without Doug managing it."))
story.append(bd("Replaces the broken organic-only model with a paid engine that competes in the channels The Ford Law Firm and Hammers already own."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $7,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $2.5M: Growth tier. PI practice area: minimum Starter, satisfied. "))
story.append(b("Website rebuild required: roswelllegal.com zero-indexed; three-domain authority split must be resolved."))
story.append(b("Conservative total SMB spend: $18,097/mo = 8.7% of 2025 revenue — well under 35% cap."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Provides profit plan framework so revenue recovery translates into actual take-home, not just higher case volume."))
story.append(bd("Builds the intake protocol and operational structure that removes Doug from business management — his stated goal."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1M+, team under 5: Elite Coach Plus. Master's Circle requires 5+ team — ineligible."))
story.append(b("Weekly group sessions + practice area masterminds address criminal defense and PI recovery challenges."))
story.append(b("Saves $297/mo vs. stand-alone $3,497/mo."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("JD Law Group — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Activates LSAs using the firm's existing 117 reviews / 4.7 stars — fastest path to pay-per-lead top-of-Google visibility."))
story.append(bd("Turns paid advertising into a reliable case engine that replaces the organic model that collapsed."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,500/mo — Criminal PPC $2,500 + LSA $1,000 + PI PPC $2,500 + LSA $1,500."))
story.append(b("<b>Aggressive:</b> $30,000/mo — full Roswell metro + Alpharetta, Sandy Springs, Marietta, Cumming."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 8-10 cases x $6,500 avg = ~$58,500/mo vs. $7,500 = ~7.8x return (est.)."))
story.append(b("<b>Aggressive:</b> 44-46 cases x $6,500 avg = ~$299,000/mo vs. $30,000 = ~10x return (est.)."))
story.append(Paragraph("<i>Estimates only. PI case value uses practice area default — not stated on call. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Channel minimums — criminal + PI PPC and LSA floors sum to $7,500."))
story.append(b("<b>Aggressive:</b> $3.0M goal x 20% / 12 = $50K; Tier 2 Atlanta (1.3x) = $65K; capped at $30K per Growth tier."))
story.append(b("At aggressive: $40,597 total SMB spend = 19.5% of 2025 revenue. Under 35% cap."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We tried ads before and they didn\'t work."', S["objection_q"]))
story.append(Paragraph("Prior campaigns ran to a non-indexed domain with a buried contact form — a landing page problem, not a market problem. The Ford Law Firm and Hammers prove ads work in Roswell; the fix is a proper conversion-optimized page on one authoritative domain.", S["objection_a"]))

story.append(Paragraph('"We can\'t afford to invest right now with revenue down."', S["objection_q"]))
story.append(Paragraph("At current 2026 pace, the firm is projecting roughly $630K-$900K — a $1.5M+ annual deficit vs. 2025. Conservative SMB investment ($18,097/mo) is 8.7% of prior revenue. The cost of inaction compounds every month competitors extend their lead.", S["objection_a"]))

story.append(Paragraph('"I don\'t want to manage more people or grow a big firm."', S["objection_q"]))
story.append(Paragraph("The pitch is not a bigger firm — it's one intake coordinator who removes Doug from the operational treadmill entirely. Every intake and follow-up task Doug currently handles goes to that role. Team stays small; Doug's workload gets lighter.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("Website rebuild, Google Ads, LSAs, Local SEO, GBP — both practice areas.", S["price_detail"]),
     Paragraph("<strike>$8,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,500–$30,000/mo", S["price_main"])],
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
    "Total: $10,597/mo + $7,500–$30,000 ad spend  |  Save $1,897/mo by bundling  |  8.7%–19.5% of revenue (under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
