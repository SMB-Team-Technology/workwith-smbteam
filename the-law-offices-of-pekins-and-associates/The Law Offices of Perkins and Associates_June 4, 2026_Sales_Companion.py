"""
Sales Companion PDF — The Law Offices of Perkins and Associates, PLLC
June 4, 2026 | Rep: Randy Gold
PACKAGE: Full Service Marketing Starter + FCOO Advisor + Fractional CTO Level 1
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
WHITE = HexColor("#FFFFFF")
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "the-law-offices-of-pekins-and-associates/The_Law_Offices_of_Perkins_and_Associates_06042026_Sales_Companion.pdf"


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

story.append(Paragraph("The Law Offices of Perkins and Associates, PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  June 4, 2026  |  Rep: Randy Gold", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Trina Perkins-Mouton", S["snap_value"]),
     Paragraph("Est. $400K–$600K", S["snap_value"]),
     Paragraph("Solo (staff TBD)", S["snap_value"]),
     Paragraph("3 — Solo Prac.", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
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

story.append(Paragraph("Dominant Buying Motive: LEGACY &amp; COMMUNITY IMPACT", S["section"]))
story.append(Paragraph("29-year mission-driven practice — she wants financial stability and systems to serve Houston's community at scale without trading every personal hour.", S["subsection"]))
story.append(quote_block("No transcript. DBM inferred: brand identity ('The Queen of Justice'), community service messaging, Christian values — mission is primary; income stability enables the mission."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable cases.</b> A system that brings PI and criminal defense leads daily — not just referrals."))
story.append(bd("<b>A firm that runs without her personally.</b> 29 years solo; she needs leverage so growth doesn't just multiply her hours."))
story.append(bd("<b>Income that matches her reputation.</b> 5.0 stars and 29 years of experience should produce stable, predictable take-home."))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Expired SSL.</b> Every referral hits a browser security warning — the website is currently inaccessible."))
story.append(b("<b>Zero paid visibility.</b> No Google Ads, LSA, or Meta — invisible to thousands searching daily."))
story.append(b("<b>Review gap.</b> 30 Google reviews vs. 1,364 for Gonzalez Law Group — not appearing in any 3-pack result."))
story.append(b("<b>Solo bottleneck.</b> All intake and operations flow through the attorney; there is no leverage."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Fixes the broken infrastructure and turns on the channels — website, ads, LSA, SEO — that make the 29-year brand visible and searchable."))
story.append(bd("Positions her 5.0 stars and expungement expertise in front of Houston PI and criminal defense searchers for the first time."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("PI in Houston (top-40 metro) — Essentials tier ineligible; Starter is the minimum."))
story.append(b("Website rebuild required: SSL expired, site inaccessible, design 5–10+ years old."))
story.append(b("All channels needed: PPC for intent, LSA for top placement, Meta for retargeting, SEO for 3-pack."))

story.append(thin_rule())

story.append(Paragraph("Why These Operations &amp; AI Packages", S["section"]))
story.append(Paragraph("<b>What they do for her:</b>", S["subsection"]))
story.append(bd("FCOO Advisor builds the operational systems so incoming leads become retained clients — not more personal hours for the attorney."))
story.append(bd("Fractional CTO Level 1 deploys AI to handle repeatable intake and follow-up work so the firm scales without proportional headcount."))

story.append(Paragraph("<b>FCOO Advisor  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Solo with no ops infrastructure — every task routes through the attorney; FCOO is the structural fix."))
story.append(b("Includes group coaching, practice area masterminds, and quarterly workshops in the package."))

story.append(Paragraph("<b>Fractional CTO — Level 1  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Done-with-you AI — CTO builds and deploys tools, trains staff; attorney doesn't manage implementation."))
story.append(b("ESCALATION: Confirm with Randy Gold that LAW delivery is live and capacity available before closing."))
story.append(b("Foundation Sprint ($4,997 one-time at onboarding) — maps AI priorities across intake and case management."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Perkins and Associates — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Turns the rebuilt website and LSA listing into a real pipeline — qualified leads arriving weekly, not waiting on referrals."))
story.append(bd("Conservative scenario: 1–2 PI cases/mo at $8K avg covers the full three-package management fee."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $6,000/mo — Google PPC ($4K) + LSA ($2K); within 35% cap at ~$600K revenue."))
story.append(b("<b>Aggressive:</b> $10,000/mo — adds Meta retargeting/lead gen; fits 35% cap at ~$735K+ revenue."))

story.append(Paragraph("<b>Estimated ROI (not guaranteed — estimates based on market benchmarks):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~9 leads x 15% close = 1–2 cases x $8K avg = ~$12,000/mo vs. $6,000 spend = 2.0x."))
story.append(b("<b>Aggressive:</b> ~23 leads x 15% close = 3 cases x $8K avg = ~$24,000/mo vs. $10,000 spend = 2.4x."))
story.append(b("At aggressive: $11,441 fees + $10,000 ads = $21,441/mo — confirm at ~$735K annual revenue for 35% cap."))

story.append(thin_rule())

story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I\'ve built this on referrals for 29 years — why change now?"', S["objection_q"]))
story.append(Paragraph(
    "WestLoop Law is running PI ads one mile from her office. Gonzalez Law Group has 1,364 reviews vs. her 30 and markets across every practice area she handles. Referrals are the floor — but the market isn't standing still.",
    S["objection_a"]))

story.append(Paragraph('"The total monthly investment is a lot for a solo practice."', S["objection_q"]))
story.append(Paragraph(
    "Two additional PI cases at $8K each cover the full $11,441 management fee. At the conservative ad spend, the break-even is roughly 1.5 cases per month — a threshold a 29-year PI attorney with a rebuilt website and running ads should clear in the first quarter.",
    S["objection_a"]))

story.append(Paragraph('"I need to fix the website before I can run ads."', S["objection_q"]))
story.append(Paragraph(
    "The website rebuild is inside the marketing package. Ads can run to a landing page while the full rebuild is underway — waiting means another 90 days of zero paid visibility while Gonzalez and WestLoop keep running.",
    S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, Google Ads, LSA, Meta, local SEO.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>FCOO Advisor</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Fractional COO + group coaching, masterminds, intake system, first hire, workshops.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Fractional CTO — Level 1</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Done-with-you AI: Claude Enterprise, Law Firm AI Skills, custom agents. Foundation Sprint $4,997 one-time.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$6,000–$10,000/mo", S["price_main"])],
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
    ("LINEBELOW", (0,7), (-1,7), 0.5, RULE_GRAY),
]))
story.append(pt)
story.append(Paragraph(
    "Total: $11,441/mo + $6,000–$10,000 ad spend  |  Save $1,850/mo by bundling  |  Confirm 35% cap (~$735K revenue) at discovery",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
