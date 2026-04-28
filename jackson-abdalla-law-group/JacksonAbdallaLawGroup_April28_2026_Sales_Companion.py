"""
Sales Companion PDF — Jackson Abdalla Law Group
SMB Team  |  Internal Use Only  |  Do Not Share with Prospect
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

OUTPUT_PATH = "jackson-abdalla-law-group/JacksonAbdallaLawGroup_04282026_Sales_Companion.pdf"


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
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=ACCENT_GREEN, spaceBefore=5, spaceAfter=1)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.5, leading=12, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=0)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9.5, leading=12, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=0)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9.5, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9.5, leading=12, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
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


# PAGE 1
story = []

story.append(Paragraph("Jackson Abdalla Law Group", S["title"]))
story.append(Paragraph("Sales Companion  |  April 28, 2026  |  Rep: Randy Gold", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Julia Jackson", S["snap_value"]),
     Paragraph("~$200K/yr", S["snap_value"]),
     Paragraph("1 (Solo)", S["snap_value"]),
     Paragraph("3 — Solo", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Elgin, IL", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: TIME WITH FAMILY", S["section"]))
story.append(Paragraph("Julia wants a firm that runs without her so she can stop working 70–80 hours/week and be present for her family.", S["subsection"]))

story.append(quote_block("working 70–80 hours per week, creating burnout and impacting family time"))
story.append(Spacer(1, 1))
story.append(quote_block("sole income earner for a family — 40 stalled MetLife cases she cannot answer, delegate, or stop"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Her evenings back.</b> Stop fielding intake calls when she should be with her family."))
story.append(bd("<b>A firm that survives her absence.</b> One sick day currently shuts the whole practice down."))
story.append(bd("<b>Financial clarity.</b> Know what she takes home — not discover surprise $1,798/mo charges on a call."))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No intake system.</b> 20–30 MetLife leads/day; 2–3 day callbacks send cases to competitors."))
story.append(b("<b>Fear of hiring.</b> $26,000 upfront hire produced zero work — no processes, no structure."))
story.append(b("<b>Mixed finances.</b> Personal and business on one BofA debit card — true profit is unknown."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives Julia leads she owns — not leads that vanish if MetLife changes its criteria."))
story.append(bd("Makes the firm findable online so estate planning clients find Julia before Lauren Jackson Law."))

story.append(Paragraph("<b>Essentials Full Service Marketing  |  $3,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue at $200K is below Starter threshold; Essentials is the appropriate entry tier."))
story.append(b("Zero Google reviews and 3 indexed pages — foundation-building is the priority before scaling."))
story.append(b("Yelp miscategorized as 'Real Estate Law' — quick fix with outsized ranking impact for estate planning."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Builds the intake system that stops $34,000/month from walking out the door unanswered."))
story.append(bd("Creates documented processes so the next hire succeeds — unlike the $26,000 failure."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Solo practitioner with zero delegation needs structured accountability, not just marketing."))
story.append(b("Previous hire failed due to no systems — coaching builds intake scripts and KPIs first."))
story.append(b("Mixed accounts and unknown recurring charges require a financial OS — coaching installs it."))


# PAGE 2
story.append(PageBreak())

story.append(Paragraph("Jackson Abdalla Law Group — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Adds a lead channel Julia controls — when MetLife slows, the pipeline does not empty."))
story.append(bd("Estate planning clients from Google Ads arrive already searching and ready to hire."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $1,000/mo — estate planning Google PPC minimum for Elgin market."))
story.append(b("<b>Aggressive:</b> $1,500/mo — Essentials tier cap; full allocation at this package level."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~1–2 cases x $2,500 avg = $2,500–$3,750/mo vs. $1,000 spend = 2.5x–3.75x."))
story.append(b("<b>Aggressive:</b> ~2 cases x $2,500 avg = $5,000/mo vs. $1,500 spend = 3.3x return."))
story.append(Paragraph("<i>Estimates based on $100 blended CPL, 15% close rate default, $2,500 avg case value. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Estate planning Google PPC minimum $1,000/mo."))
story.append(b("<b>Aggressive:</b> $400K goal x 20% / 12 = $6,667. Tier 4 (1.0x). Minus $3,397 fee. Capped at Essentials $1,500 max."))
story.append(b("Total at aggressive: $7,497/mo ($5,997 management + $1,500 ad spend) = 45% of revenue."))

story.append(thin_rule())

story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I already paid $26,000 for someone who produced nothing."', S["objection_q"]))
story.append(Paragraph("That hire failed because there were no documented processes or KPIs — not a people problem. Elite Coach builds that structure before we recommend hiring anyone.", S["objection_a"]))

story.append(Paragraph('"I\'m already drowning. I don\'t have time for anything new."', S["objection_q"]))
story.append(Paragraph("The first 90 days are designed to reduce Julia's workload, not add to it. Intake coverage handles the MetLife calls she can't answer. The goal is fewer hours, not more tasks.", S["objection_a"]))

story.append(Paragraph('"I\'m not sure I can afford this right now."', S["objection_q"]))
story.append(Paragraph("The 40 stalled MetLife cases represent $34,000/month in identified missed revenue — more than 7x the total SMB investment. Fixing intake recovers money already at the door.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Essentials Full Service Marketing</b>", S["price_main"]),
     Paragraph("$3,397/mo", S["price_main"])],
    [Paragraph("Google Ads, GBP optimization, review generation, website conversion.", S["price_detail"]),
     Paragraph("<strike>$3,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Bi-weekly coaching, intake design, hiring framework, financial OS.", S["price_detail"]),
     Paragraph("<strike>$3,000</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$1,000–$1,500/mo", S["price_main"])],
    [Paragraph("Goes to Google — not to SMB Team.", S["price_detail"]),
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
    "Total: $5,997/mo + $1,000–$1,500 ad spend  |  Save $700/mo by bundling",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

import re
with open(OUTPUT_PATH, 'rb') as f:
    data = f.read()
counts = re.findall(rb'/Count (\d+)', data)
print(f"Page count: {counts[0].decode() if counts else 'unknown'}")
if counts and counts[0] != b'2':
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
