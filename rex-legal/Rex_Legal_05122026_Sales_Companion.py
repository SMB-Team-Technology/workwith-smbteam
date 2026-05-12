"""
Sales Companion PDF — Rex Legal
SMB Team Internal Document | May 12, 2026 | Rep: Jacob Meissner
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

OUTPUT_PATH = "/home/user/workwith-smbteam/rex-legal/Rex_Legal_05122026_Sales_Companion.pdf"


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
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=DARK_NAVY, spaceBefore=1, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=1)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8.5, leading=11, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=8.5, leading=12, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=2)
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
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


# ══════════════════════════════════════════════════════════
# PAGE 1
# ══════════════════════════════════════════════════════════
story = []

story.append(Paragraph("Rex Legal", S["title"]))
story.append(Paragraph("Sales Companion  |  May 12, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Michael Rex", S["snap_value"]),
     Paragraph("$370k (2025)", S["snap_value"]),
     Paragraph("Solo (1)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Denver, CO", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: FINANCIAL SECURITY", S["section"]))
story.append(Paragraph("Michael wants $500k in personal income — the number that means he is no longer stressed about money.", S["subsection"]))
story.append(quote_block("Reach $500k in personal income to feel financially secure."))
story.append(Spacer(1, 1))
story.append(quote_block("I spent $120k on LSA and made $160k — 25% margin. I need marketing that actually works."))
story.append(Spacer(1, 1))
story.append(quote_block("If I could get 1 to 2 quality cases consistently, I could hire an admin and scale to 50 cases."))
story.append(Spacer(1, 1))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Consistent injury cases.</b> 1–2 quality PI cases/month reliably — the trigger for his first admin hire."))
story.append(bd("<b>Admin hire at 25 cases.</b> The unlock that scales to 50+ cases and removes Michael as the bottleneck."))
story.append(bd("<b>$500k personal income.</b> Not revenue growth — the number that represents financial security."))
story.append(bd("<b>Injury cases only.</b> Prior campaign sent property damage calls, not injured clients."))
story.append(Spacer(1, 1))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No lead system.</b> Referrals only — caseload fell from ~30 to 15–20 when prior LSA campaign ended."))
story.append(b("<b>Skeptical of paid ads.</b> Prior $120k LSA spend → $160k revenue, 25% margin. Cautious to invest again."))
story.append(b("<b>No after-hours intake.</b> GBP shows closed weekends — Fri/Sat night accident leads go to competitors."))
story.append(b("<b>41 Google reviews.</b> Invisible in 3-pack vs. Denver PI firms with 407–1,926 reviews."))
story.append(b("<b>No profit plan.</b> Knows revenue but has no model mapping cases and margin to $500k personal income."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Delivers qualified injury cases — not property damage calls — through LSA with injury-specific categories."))
story.append(bd("Builds organic authority (GBP, SEO, content) that lowers cost per lead as the firm's visibility grows."))
story.append(bd("Fixes the intake gap — website rebuild and 24/7 coverage ensure ad spend generates answered contacts."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("PI practice area — Essentials tier eliminated; Starter is the mandatory minimum for PI firms."))
story.append(b("Revenue $370k is below the $400k next-tier threshold — Starter is the correct fit with a $5,000/mo ad cap."))
story.append(b("Website blocked automated crawlers, has no blog, no geo pages, URL typo — Full Service (not ads-only) required."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the profit model mapping cases and margin to $500k personal income — tracked monthly."))
story.append(bd("Creates the admin hire roadmap so the hire happens at 25 cases instead of being deferred indefinitely."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $370k falls in $250k–$400k band — Elite Coach is the correct non-marketing package."))
story.append(b("Solo firm (under 5 team members) and revenue under $500k — Master's Circle and fractional packages hidden."))
story.append(b("Clear profit gap ($370k revenue, well below $500k personal income target) — coaching directly addresses this."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Rex Legal — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Conservative ($6k/mo) already projects 3 cases/month — exceeds his stated goal of 1–2, positive ROI from month one."))
story.append(bd("Starting conservative and scaling on results directly addresses his bad prior experience. Data before commitment."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $6,000/mo — LSA $3,000 + Meta Retargeting $1,500 + Meta Lead Gen $1,500. Exceeds PI high-competition floor ($5,000). PPC added in Phase 2."))
story.append(b("<b>Aggressive:</b> $11,000/mo — $740k goal x 20% / 12 x 1.3 (Tier 2) - $4,847 management fee = $11,186."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative ($6k):</b> ~21 leads x 15% close = ~3 cases x $20,500 est. = ~$61,500/mo = ~10x return."))
story.append(b("<b>Aggressive ($11k):</b> ~39 leads x 15% close = ~5-6 cases x $20,500 est. = ~$112,750/mo = ~10x return."))
story.append(Paragraph("<i>Estimates only. Case value estimated (~$20,500 = $370k / 18 cases). Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>Calculation notes:</b>", S["subsection"]))
story.append(b("<b>FLAG:</b> Total spend at conservative ($13,447) = 43.6% of monthly revenue — exceeds 35% cap. Present as phased approach; scale as cases ramp and revenue grows."))
story.append(b("Denver = Tier 2 market (1.3x multiplier). Prior campaign failed at $8k/mo (insufficient) and broad targeting (property damage calls). Both correctable."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I tried ads before and they didn\'t work."', S["objection_q"]))
story.append(Paragraph("Correct diagnosis — wrong prescription. The prior campaign ran $4k/mo below Denver's market floor and used broad targeting that captured property damage calls. Injury-specific LSA categories and a properly funded campaign are structurally different — not incremental.", S["objection_a"]))

story.append(Paragraph('"$7,447 plus ad spend is a lot on $370k revenue."', S["objection_q"]))
story.append(Paragraph("At conservative ROI, 2 extra cases/month covers the entire SMB Team investment. Start at conservative ad spend and scale only when case volume justifies it. The admin hire — which unlocks 50 cases and $500k income — cannot happen without a reliable lead system.", S["objection_a"]))

story.append(Paragraph('"I just want 1-2 quality cases to start — not a big commitment."', S["objection_q"]))
story.append(Paragraph("Conservative scenario projects 3 cases/month — already above his goal. And 3 consistent cases/month gets Michael to the 25-case threshold in under a year, which triggers the admin hire that changes everything for his personal income.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, LSA, Google PPC, Meta Ads, local SEO, GBP optimization, monthly reporting.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, profit model, admin hire roadmap, quarterly accountability, annual workshop.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$6,000–$11,000/mo", S["price_main"])],
    [Paragraph("To Google LSA, Google PPC, and Meta — not to SMB Team. Start conservative; scale on results.", S["price_detail"]),
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
    "Total SMB Team: $7,447/mo + $6,000–$11,000/mo ad spend  |  Save $1,747/mo by bundling  |  43.6%–59.8% of revenue (FLAG: exceeds 35% cap — present as phased approach)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

import re
with open(OUTPUT_PATH, 'rb') as f:
    content = f.read()
pages = re.findall(rb'/Type\s*/Page\b', content)
print(f"Page count (approx): {len(pages)}")
if len(pages) != 2:
    print("WARNING: May not be exactly 2 pages — verify visually.")
