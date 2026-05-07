"""
Sales Companion PDF — Shingleton Law, PLLC
Sales Rep: Jacob Meissner | Date: May 07, 2026
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

OUTPUT_PATH = "shingleton-law/ShingletonLaw_05072026_Sales_Companion.pdf"


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
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


# ══════════════════════════════════════════════════════════
# PAGE 1
# ══════════════════════════════════════════════════════════
story = []

story.append(Paragraph("Shingleton Law, PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  May 07, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]), Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]), Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]), Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Adam Shingleton", S["snap_value"]), Paragraph("~$125K/yr", S["snap_value"]),
     Paragraph("Solo + tech co-founder", S["snap_value"]), Paragraph("Stage 3", S["snap_value"]),
     Paragraph("~90%", S["snap_value"]), Paragraph("Hampstead, NC", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: FREEDOM + SCALE", S["section"]))
story.append(Paragraph("Adam wants a self-managing statewide firm that generates cases and serves clients without him being in every room.", S["subsection"]))
story.append(quote_block("Time cut from ~5 hours to 30-45 mins on the application. From 3-7 hours to 15-20 mins on the final account."))
story.append(Spacer(1, 1))
story.append(quote_block("Goal: statewide NC expansion within one year and a long-term revenue target of $10M."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Cases without his sourcing.</b> He handles every consult now — he wants the pipeline to fill without him generating it."))
story.append(bd("<b>Statewide scale without personal involvement.</b> NC expansion is the 12-month goal — impossible if he drives every market launch himself."))
story.append(bd("<b>The tech advantage to pay off.</b> Zach built a platform that cuts probate admin from hours to minutes — Adam wants that to translate into market share."))

story.append(Spacer(1, 1))
story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Zero paid advertising.</b> No Google Ads, no LSA, no Meta — every case today is organic or referral."))
story.append(b("<b>GBP unoptimized.</b> Under 12 months old, near-zero reviews, not in the 3-pack for any probate keyword."))
story.append(b("<b>Intake bottleneck.</b> Adam handles every initial consult — statewide scale requires intake to work without him."))
story.append(b("<b>Revenue under $250K.</b> Confirm funds for 4 months of services before proceeding."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Paid leads come in from LSA and PPC while Adam focuses on consults — the pipeline fills without him sourcing every case."))
story.append(bd("GBP, landing page, and SEO compound over 6-12 months to generate free organic cases in parallel with paid."))

story.append(Paragraph("<b>Full Service Marketing Essentials  |  $3,397/mo bundled</b>", S["subsection"]))
story.append(b("At $125K/yr ($10,417/mo), Essentials is the correct tier. Stand-alone: N/A — this is the entry bundled offering."))
story.append(b("Includes GBP optimization, probate landing page, SEO, FAQ schema, blog, reporting, and LSA/PPC setup for Phase 2 activation."))
story.append(b("35% cap: $3,397 = 32.6% of $10,417 — within cap. Remaining $248/mo is below min ad spend; paid ads launch in Phase 2."))

story.append(thin_rule())

story.append(Paragraph("Elite Coach — Phase 2 Add (triggers at $250K revenue)", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Teaches Adam to delegate the initial consultation — the change that unlocks every growth milestone above $250K."))
story.append(bd("Builds the leadership structure (SOPs, hiring playbook, accountability) needed for multi-market expansion."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled (Phase 2 only)</b>", S["subsection"]))
story.append(b("Excluded from Phase 1: $3,397 + $2,600 = $5,997 = 57.6% of $10,417 — far over 35% cap."))
story.append(b("At $250K revenue ($20,833/mo): $5,997 = 28.8% — within cap. Saves $897/mo vs. $3,497 stand-alone."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Shingleton Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend (Phase 2 — launches at $250K revenue)", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("<b>Conservative $1,000/mo:</b> 4-5 probate cases at $5K avg = ~$20K/mo revenue — 20x return. Total Phase 2 spend = 33.6% of $20,833 — within cap."))
story.append(bd("<b>Aggressive $1,200/mo:</b> 8-9 cases = ~$40K/mo revenue — 33x return. Total Phase 2 spend = 34.6% of $20,833 — within cap."))

story.append(Paragraph("<b>How it was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Estate planning blended CPL $175 + 20% cushion = $200. $1K / $200 = 5 leads x 90% close = 4-5 cases."))
story.append(b("<b>Aggressive:</b> ($75 + $175) / 2 = $125 blended. $1.2K / $125 = 9-10 leads x 90% close = 8 cases."))
story.append(b("Practice area minimums exceed budget ($3,200 total) — LSA-first prioritization required; flag for paid ads team."))
story.append(b("Phase 1 cap: $3,397 mgmt = 32.6% of $10,417 — within cap. $248 remaining is below $1K min; ads launch Phase 2."))
story.append(Paragraph("<i>All ROI figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We are just getting started — maybe we should wait."', S["objection_q"]))
story.append(Paragraph("At $125K, the firm generates 7 cases/month with zero paid ads. Adding 4-5 cases at $5K from a $1K ad spend = $20K-$25K additional revenue monthly. Blackburn & Ording has 26 reviews and 35 years of presence. Every month without action is another month they extend their lead while Shingleton Law's GBP stays unoptimized.", S["objection_a"]))

story.append(Paragraph('"My close rate is 90% — isn\'t that enough?"', S["objection_q"]))
story.append(Paragraph("A 90% close rate is the firm's strongest asset and the audit confirms it. The gap is not the close — it is the leads. Shingleton Law does not appear in the local 3-pack for any probate keyword and runs no paid ads. Barrington Law (5.0 stars / 32 Avvo reviews) and Bespoke Estate Law (geo-targeted Hampstead landing pages) are already taking the cases Adam never hears about.", S["objection_a"]))

story.append(Paragraph('"The budget feels tight with the 35% cap."', S["objection_q"]))
story.append(Paragraph("Essentials at $3,397 = 32.6% of $10,417/mo — within cap as a management fee. The remaining $248/mo is below the ad spend minimum, so paid ads launch in Phase 2 at $250K revenue. At that point $5,997 management fees = 28.8% of $20,833, and the 35% cap allows $1,000-$1,294 for ads alongside both packages.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))
price_data = [
    [Paragraph("<b>Full Service Marketing Essentials</b>", S["price_main"]),
     Paragraph("$3,397/mo", S["price_main"])],
    [Paragraph("GBP, SEO, probate landing page, FAQ schema, blog, reporting, LSA/PPC setup.", S["price_detail"]),
     Paragraph("Stand-alone: N/A", S["price_detail"])],
    [Paragraph("<b>Elite Coach (Phase 2 — unlocks at $250K/yr)</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly coaching, practice area masterminds, quarterly workshops, annual in-person event.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand-alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$1,000–$1,200/mo", S["price_main"])],
    [Paragraph("Goes to Google LSA, PPC — not to SMB Team. LSA-first recommended.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
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
    "Phase 1: $3,397/mo management only (32.6% of revenue — no ad spend within Phase 1 cap)  |  Phase 2 adds Elite Coach ($2,600) + ads $1,000-$1,200  |  Elite Coach saves $897/mo bundled",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

import re
data = open(OUTPUT_PATH, 'rb').read()
count = len(re.findall(b'/Type\s*/Page[^s]', data))
print(f"Page count: {count}")
if count != 2:
    print("WARNING: Must be exactly 2 pages. Shorten bullet text.")
else:
    print("OK: Exactly 2 pages.")
