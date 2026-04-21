"""
Sales Companion PDF — Law Office of Lorena Ibarra
Internal use only. Do not share with prospect.
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

OUTPUT_PATH = "lorena-ibarra-law/LawOfficeLorenaIbarra_April20_2026_Sales_Companion.pdf"


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


# ══════════════════════════════════════════
# PAGE 1
# ══════════════════════════════════════════
story = []

story.append(Paragraph("Law Office of Lorena Ibarra", S["title"]))
story.append(Paragraph("Sales Companion  |  April 20, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Lorena Ibarra", S["snap_value"]),
     Paragraph("$1.3M–$1.5M", S["snap_value"]),
     Paragraph("7 (incl. owner)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("~15% (default)", S["snap_value"]),
     Paragraph("Hoover, AL", S["snap_value"])],
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
story.append(Paragraph("She wants a firm that runs itself so she can be the attorney again — not the manager, HR department, and operations director.", S["subsection"]))

story.append(quote_block("I'm the chief everything officer. I have to be here for everything."))
story.append(Spacer(1, 1))
story.append(quote_block("I can't even take a vacation. If I leave, everything falls apart."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>A self-running firm.</b> Walk in Monday and the team is already moving — no fires, no decisions waiting on her."))
story.append(bd("<b>To practice law again.</b> Built this firm to serve immigrants; wants to do that work, not manage staff."))
story.append(bd("<b>Predictable growth.</b> Revenue that comes from systems, not from her working harder."))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No management layer.</b> All 6 staff report through Lorena — every decision lands on her."))
story.append(b("<b>No intake system.</b> $360K/year in missed cases tied directly to this operational gap."))
story.append(b("<b>Two recent bad hires.</b> No hiring or onboarding system; performance problems are recurring."))
story.append(b("<b>No financial visibility.</b> No cost-per-case data, no profit plan — growth is unpredictable."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Creates a predictable client flow that does not require Lorena to personally chase leads."))
story.append(bd("Spanish-first brand + immigrant story = a paid ad advantage competitors cannot replicate."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $4,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue of $1.3M–$1.5M places her in the Growth tier ($1M–$3M)."))
story.append(b("Abogados Centro Legal has 397 reviews; Solano Law Firm has 229+. Firm has no paid presence."))
story.append(b("Website needs inline intake form and city landing pages — full service handles both."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Puts an operations leader in place so the firm stops requiring Lorena for day-to-day decisions."))
story.append(bd("Builds the hiring, KPI, and accountability systems her current program promised but never delivered."))

story.append(Paragraph("<b>FCOO Advisor  |  $2,297/mo bundled</b>", S["subsection"]))
story.append(b("Self-described 'chief everything officer' — this is an ops crisis, not a coaching gap."))
story.append(b("Current coaching (6 months remaining) gave strategy without execution support."))
story.append(b("At $1.3M with no management layer, an FCOO is the minimum viable structural fix."))


# ══════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Law Office of Lorena Ibarra — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Places the firm at the top of Google for immigration searches in Hoover and Birmingham."))
story.append(bd("Spanish-language campaigns convert higher and cost less than English-only — a structural advantage."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,000/mo — immigration channel minimums with Spanish campaign factor."))
story.append(b("<b>Aggressive:</b> $10,000/mo — Growth tier cap; 20% rule produces ~$44K but is capped here."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative ($7,000):</b> ~9–10 cases x $4,500 avg = ~$42,750/mo vs. $7K spend = ~6x return."))
story.append(b("<b>Aggressive ($10,000):</b> ~15–18 cases x $4,500 avg = ~$67,500–$81,000/mo vs. $10K = ~7–8x return."))
story.append(Paragraph("<i>Estimates based on immigration CPL benchmarks and 15% default close rate. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Immigration minimums PPC $2K + LSA $1K + Meta $1.2K = $4.2K x 1.33 Spanish = $5.6K; floored at $7K."))
story.append(b("<b>Aggressive:</b> $2.6M goal x 20% / 12 = $43K. Tier 5 (0.85x) = $36.8K. Spanish (1.33x) = $48.9K. Capped at $10K tier max."))
story.append(b("Total at aggressive: $14,397 mgmt + $10K ad spend = $24,397/mo = 18.7% of revenue. Under 35% cap."))

story.append(thin_rule())

story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I still have 6 months left on my coaching contract."', S["objection_q"]))
story.append(Paragraph("That program recommended KPIs but gave no implementation support. The $360K/year gap is an execution problem — every month without systems in place is another month of that loss.", S["objection_a"]))

story.append(Paragraph('"I\'ve never run paid ads — what if it doesn\'t work?"', S["objection_q"]))
story.append(Paragraph("Abogados Centro Legal (1.5 miles away) has 397 Google reviews vs. her 42. They are capturing the immigration searches this firm should own. Spanish-language ads have lower CPL and higher conversion than English-only.", S["objection_a"]))

story.append(Paragraph('"I\'m already doing $1.3M — do I really need this?"', S["objection_q"]))
story.append(Paragraph("$1.3M with no intake system and no management layer means her ceiling is her personal bandwidth. Without a change, $2M means twice the work, not twice the freedom.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))
price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$4,397/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, SEO, Spanish campaigns, website optimization.", S["price_detail"]),
     Paragraph("<strike>$4,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>FCOO Advisor</b>", S["price_main"]),
     Paragraph("$2,297/mo", S["price_main"])],
    [Paragraph("Fractional COO builds management layer, hiring systems, KPIs, accountability.", S["price_detail"]),
     Paragraph("<strike>$2,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,000–$10,000/mo", S["price_main"])],
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
    "Total: $6,694/mo + $7,000–$10,000 ad spend  |  Save $1,100/mo by bundling  |  14.7%–18.7% of revenue (under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

import re
with open(OUTPUT_PATH, 'rb') as f:
    content = f.read()
pages = len(re.findall(b'/Type\s*/Page[^s]', content))
print(f"Page count: {pages}")
if pages != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
