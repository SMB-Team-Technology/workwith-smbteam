"""
Sales Companion PDF — Keeling Gutierrez Debt Relief Attorneys
Sales Rep: Randy Gold  |  May 05, 2026
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

OUTPUT_PATH = "/home/user/workwith-smbteam/keeling-gutierrez/KeelingGutierrezDebtRelief_05052026_Sales_Companion.pdf"


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

story.append(Paragraph("Keeling Gutierrez Debt Relief Attorneys", S["title"]))
story.append(Paragraph("Sales Companion  |  May 05, 2026  |  Rep: Randy Gold", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Gutierrez &amp; Keeling", S["snap_value"]),
     Paragraph("~$3M/yr (flat)", S["snap_value"]),
     Paragraph("7 attorneys", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("43%", S["snap_value"]),
     Paragraph("Houston, TX", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: LEGACY PROTECTION", S["section"]))
story.append(Paragraph("Protect a 40-year firm from a fast-moving competitor and grow to $6M before the window closes.", S["subsection"]))

story.append(quote_block("Allmand is filing doubled monthly — 30, then 60, then 90 cases in 3 months."))
story.append(Spacer(1, 1))
story.append(quote_block("13 specific clients from our direct mail were lost to Allmand Law."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Stop losing ground.</b> Allmand entered 6 months ago — she wants to compete on every channel before the gap widens further."))
story.append(bd("<b>Double revenue to $6M.</b> Stated directly — the firm has been flat at $3M and she knows why."))
story.append(bd("<b>Attribution on ad spend.</b> $6–7k/month with zero tracking is a known pain point; she wants data."))
story.append(bd("<b>Firm that runs without her.</b> Partners handling after-hours and intake gaps is not sustainable at scale."))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>5x review gap.</b> Allmand has 586 Google reviews vs. 120 — every LSA dollar returns less than theirs."))
story.append(b("<b>40 lost leads/month.</b> Warm consultations leaving with no follow-up = $120k/month unconverted."))
story.append(b("<b>Competitor has an exclusive agency.</b> TSG Logic runs both Allmand and Southward — coordinated, data-driven."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("<b>Full attribution.</b> She will know cost per case by channel within 30 days — for the first time."))
story.append(bd("<b>Closes the review gap.</b> Managed review generation closes 466-review deficit with Allmand, month by month."))
story.append(bd("<b>Spanish-language campaigns.</b> Two bilingual attorneys + Houston 45% Hispanic = virtually uncontested segment."))

story.append(Paragraph("<b>Full Service Marketing — Platinum  |  $5,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $3M+ → Platinum tier; Houston = Tier 1 requiring full-spectrum approach."))
story.append(b("Includes PPC, LSA, Meta, review generation, Spanish campaigns, and citation cleanup."))
story.append(b("Retail $9,997/mo; bundled at $5,997 = $4,000/mo savings."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("<b>Fixes intake.</b> Script + 3-touch follow-up for the 40 monthly non-converters = $30–45k/mo in recovered revenue."))
story.append(bd("<b>Removes the partners as bottleneck.</b> FCOO Director builds the ops layer so the firm runs without them."))
story.append(bd("<b>KPI accountability.</b> Monthly targets and tracking for cost per case and consultation-to-signing rate."))

story.append(Paragraph("<b>Master's Circle + FCOO Director  |  $8,394/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $2M+ with 5+ team → Master's Circle + FCOO Director eligible."))
story.append(b("No dedicated intake, ops, or marketing function — FCOO Director fills that gap directly."))
story.append(b("Bundle includes Elite Coach deliverables: weekly coaching, masterminds, quarterly + annual workshops."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Keeling Gutierrez — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("<b>Replaces blind spend.</b> Current $6–7k has no attribution — this budget is tracked from day one."))
story.append(bd("<b>Spanish-language channel.</b> Funds campaigns targeting Houston's most underserved bankruptcy segment."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $10,000/mo — minimum viable across all recommended channels."))
story.append(b("<b>Aggressive:</b> $20,000/mo — full budget aligned to the $6M goal."))

story.append(Paragraph("<b>Estimated ROI (not guaranteed):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~40 cases x $3,000 = ~$120,000/mo vs. $10,000 spend = ~12x return."))
story.append(b("<b>Aggressive:</b> ~100 cases x $3,000 = ~$300,000/mo vs. $20,000 spend = ~15x return."))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Bankruptcy minimums — PPC $4,500 + LSA $3,000 + Meta $500 + Spanish Meta $2,000 = $10,000."))
story.append(b("<b>Aggressive:</b> $6M x 20% ÷ 12 = $100k. Houston Tier 1 (x1.5) + Spanish (x1.33) = $199,500. Capped at $20,000 practical start."))
story.append(b("Total at aggressive: $34,391/mo = 13.8% of revenue. Under 35% cap."))

story.append(thin_rule())

story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"We\'re already spending $6–7k — why more?"', S["objection_q"]))
story.append(Paragraph("Your current spend has zero attribution — you can't tell if it's working. We rebuild it with full tracking so you see cost per case by channel within 30 days. Then you scale what works.", S["objection_a"]))

story.append(Paragraph('"Allmand has a head start — can we catch up?"', S["objection_q"]))
story.append(Paragraph("They've been in Houston 6 months. You've been here 40 years. You have board certification and a bilingual team they can't replicate. The gap is in marketing infrastructure — not credibility. We build the infrastructure.", S["objection_a"]))

story.append(Paragraph('"$14k/month is a lot."', S["objection_q"]))
story.append(Paragraph("At conservative ($10k ad spend), the model projects $105–120k/month in revenue. Total engagement = $24,391/mo = 9.8% of monthly revenue. Well under the 35% cap.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Platinum</b>", S["price_main"]),
     Paragraph("$5,997/mo", S["price_main"])],
    [Paragraph("PPC, LSA, Meta, review generation, Spanish campaigns, attribution.", S["price_detail"]),
     Paragraph("<strike>$9,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle + FCOO Director</b>", S["price_main"]),
     Paragraph("$8,394/mo", S["price_main"])],
    [Paragraph("Intake script, KPI accountability, ops leadership, coaching + workshops.", S["price_detail"]),
     Paragraph("Bundle incl. Elite Coach", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$10,000–$20,000/mo", S["price_main"])],
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
    "Total: $14,391/mo + $10,000–$20,000 ad spend  |  Save $4,000/mo by bundling  |  9.8%–13.8% of revenue (under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

import re
with open(OUTPUT_PATH, 'rb') as f:
    content = f.read().decode('latin-1')
pages = len(re.findall(r'/Type\s*/Page[^s]', content))
print(f"Page count: {pages}")
if pages != 2:
    print("WARNING: Must be exactly 2 pages.")
else:
    print("OK: Exactly 2 pages.")
