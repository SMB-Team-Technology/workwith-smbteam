"""
Sales Companion PDF Template — SMB Team
========================================
This template generates the 2-page internal Sales Companion PDF for the sales rep.
It uses reportlab. Do not modify the layout, colors, fonts, styles, or structure.
Only replace the # FILL: placeholders with audit-specific content.

IMPORTANT: The final PDF must be exactly 2 pages. If content overflows to a third
page, shorten bullet text — do not remove sections.

All bullet text must be scannable: one idea per bullet, 8th-grade reading level.
Each "What it does for her/him:" bullet states the transformation, not the deliverable.
Each scoping rationale bullet states one fact with one conclusion.

Output filename: [FirmName]_[Date]_Sales_Companion.pdf
  - FirmName: spaces replaced with underscores
  - Date: MMDDYYYY format
  - Save to the root of the project folder (same location as the Growth Audit HTML)
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

# ── Colors — DO NOT MODIFY ──
DARK_NAVY = HexColor("#1a2332")
ACCENT_GREEN = HexColor("#3B6D11")
MEDIUM_GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#888888")
RULE_GRAY = HexColor("#CCCCCC")
QUOTE_BG = HexColor("#F5F7F0")
WHITE = HexColor("#FFFFFF")
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "aero-law-center/Aero_Law_Center_July 24, 2026_Sales_Companion.pdf"


def add_page_elements(canvas, doc):
    """Draws red warning header and confidential footer on every page. DO NOT MODIFY."""
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

# ── Styles — DO NOT MODIFY ──
S = {}
S["title"] = ParagraphStyle(
    "title", fontName="Helvetica-Bold", fontSize=16, leading=20,
    textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle(
    "subtitle", fontName="Helvetica", fontSize=9.5, leading=13,
    textColor=LIGHT_GRAY, spaceAfter=3)
S["section"] = ParagraphStyle(
    "section", fontName="Helvetica-Bold", fontSize=11, leading=15,
    textColor=ACCENT_GREEN, spaceBefore=6, spaceAfter=2)
S["subsection"] = ParagraphStyle(
    "subsection", fontName="Helvetica-Bold", fontSize=10, leading=13,
    textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle(
    "bullet", fontName="Helvetica", fontSize=9.5, leading=13,
    textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0,
    spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle(
    "bullet_dark", fontName="Helvetica", fontSize=9.5, leading=13,
    textColor=DARK_NAVY, leftIndent=12, bulletIndent=0,
    spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle(
    "quote", fontName="Helvetica-Oblique", fontSize=9.5, leading=13,
    textColor=DARK_NAVY, leftIndent=6, rightIndent=6,
    spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle(
    "snap_label", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
    textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle(
    "snap_value", fontName="Helvetica", fontSize=9.5, leading=12,
    textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle(
    "objection_q", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
    textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle(
    "objection_a", fontName="Helvetica", fontSize=9.5, leading=13,
    textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle(
    "price_main", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
    textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle(
    "price_detail", fontName="Helvetica", fontSize=8.5, leading=12,
    textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle(
    "savings", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
    textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle(
    "disclaimer", fontName="Helvetica-Oblique", fontSize=8.5, leading=11,
    textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


# ── Helpers — DO NOT MODIFY ──
def b(text):
    """Gray bullet for scoping rationale, obstacles, and technical details."""
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    """Dark bullet for transformation statements and what she/he wants."""
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY,
                       spaceBefore=3, spaceAfter=3)

def quote_block(text):
    """Quote block with subtle background for prospect's own words."""
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

story.append(Paragraph("Aero Law Center", S["title"]))
story.append(Paragraph("Sales Companion  |  July 24, 2026  |  Rep: Dan Bryant", S["subtitle"]))
story.append(thin_rule())

# ── Prospect Snapshot ──
story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("John Ewing (not on call)", S["snap_value"]),
     Paragraph("~$3M; goal $5-7M", S["snap_value"]),
     Paragraph("13 staff", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% default*", S["snap_value"]),
     Paragraph("Fort Lauderdale, FL", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.7*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 4))

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: SCALE AND DOMINATE (inferred)", S["section"]))
story.append(Paragraph("John wants Aero Law Center to become the largest aviation law firm in the country — John was not on this call, so confirm this directly with him.", S["subsection"]))

story.append(quote_block("Relationships, referrals, conferences, PR, and AeroShield webinars are our lead sources today"))
story.append(Spacer(1, 1))
story.append(quote_block("One month of PPC got us about 140 leads, but 75% were junk and only 12-15 were retained"))
story.append(Spacer(1, 1))
story.append(quote_block("We ended the SEO retainer at the new year — we were paying for 6 articles a month and barely got 5 all year"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>National category dominance.</b> The firm already brands itself the largest aviation law firm in the US."))
story.append(bd("<b>$10M long term.</b> This year's goal is $5-7M, up from about $3M last year."))
story.append(bd("<b>A team that runs without him.</b> He was not even on this discovery call."))
story.append(bd("<b>Proof that paid marketing can work.</b> Past PPC and SEO spend left a bad taste."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Google Ads is paused.</b> A payment issue, not a strategy choice, has the account off right now."))
story.append(b("<b>SEO just ended.</b> The $8,600/mo Hennessey Digital retainer stopped at the new year over ROI."))
story.append(b("<b>Two priority cities have no page.</b> Orlando and Atlanta were named on the call but don't exist on the site."))
story.append(b("<b>Intake leaks leads.</b> Historical PPC leads converted at only 9-11% lead-to-retained."))
story.append(b("<b>John is still the bottleneck.</b> GBP access sits on his personal Gmail; he wasn't on this call."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns the Google Ads account back on and adds LSA and Meta to fill the gap left by the ended SEO retainer."))
story.append(bd("Builds the Aircraft Lien, Orlando, and Atlanta pages the firm itself flagged as missing."))
story.append(bd("Gives the national platform a paid engine that matches its brand claim."))

story.append(Paragraph("<b>Full Service Marketing — Platinum  |  $15,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue (~$3M) sits at the $3M+ Platinum threshold in our pricing table."))
story.append(b("The 20% rule aggressive ad spend (~$105,600/mo) exceeds Dominate's $75K cap, so Platinum's $150K cap is needed."))
story.append(b("Active national expansion (7 states, 4 cities live) needs full-service scope, not an ads-only add-on."))
story.append(b("Saves $3,000/mo vs. the $18,997/mo stand-alone price."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds an operations layer so decisions stop routing through John's calendar alone."))
story.append(bd("Puts a dedicated FCOO Director on fixing the intake gaps costing retained cases."))
story.append(bd("Group coaching connects the firm to peers who have made this exact jump in scale."))

story.append(Paragraph("<b>Master's Circle + FCOO Director  |  $8,394/mo bundled</b>", S["subsection"]))
story.append(b("Revenue (~$3M) and team size (13 staff + dedicated Finance/Revenue Manager) hit the $2M+ / 5+ dedicated staff row."))
story.append(b("FCOO Partner tier was ruled out — no stand-alone price exists for that combo in our tables."))
story.append(b("Includes weekly group coaching, masterminds, and workshop access at no extra charge."))
story.append(b("Saves $2,400/mo vs. the $10,794/mo stand-alone price."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Aero Law Center — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Restarts a paid engine that has been sitting idle, not underperforming, since the payment issue and the SEO exit."))
story.append(bd("Gives a real number to test against the $5-7M goal, instead of another single-month verdict."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $6,700/mo — Business Law channel minimums (closest analog; no Aviation Law row exists in our tables)."))
story.append(b("<b>Aggressive:</b> $105,000/mo — 20% rule against the $5-7M goal, Tier 2 Miami-metro multiplier, minus management fees."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~8 cases x $9K blended value = ~$70K/mo vs. $6.7K spend = ~10.5x return."))
story.append(b("<b>Aggressive:</b> ~147 cases x $9K blended value = ~$1.32M/mo vs. $105K spend = ~12.6x return."))
story.append(Paragraph("<i>All figures are estimates using a $9K blended case value, not the $18-20K overall average. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Business Law minimums: PPC $3,500 + LSA $2,000 + Meta Retargeting $1,200 = $6,700."))
story.append(b("<b>Aggressive:</b> $6M goal midpoint x 20% / 12 = $100,000. Tier 2 (1.3x) = $130,000. Minus $24,391 fees = ~$105,600, rounded to $105,000."))
story.append(b("At aggressive spend, total is ~25.9% of the $6M goal's monthly revenue and ~51.8% of current revenue — flag for paid ads review before scoping."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We already tried PPC and it did not work — 140 leads and only 12-15 retained."', S["objection_q"]))
story.append(Paragraph("That is a 9-11% lead-to-retained rate on a channel with no dedicated after-hours intake and a buried contact form. The lead volume was real — the leak was on our side of the handoff, not the channel.", S["objection_a"]))

story.append(Paragraph('"We just paid $8,600/mo for SEO for a year and it did not deliver."', S["objection_q"]))
story.append(Paragraph("Confirmed — only about 5 of a promised 6 articles/month were ever indexed. That is a vendor execution failure, not proof SEO does not work for this firm.", S["objection_a"]))

story.append(Paragraph('"Our average case is $18-20K — why are you projecting only $9K per case?"', S["objection_q"]))
story.append(Paragraph("That $18-20K is the firm-wide average, but the transcript shows many prior PPC leads converted into $2-5K demand-letter matters. We used a $9K blended estimate so the ROI numbers reflect the real historical lead mix, not the best-case average.", S["objection_a"]))

story.append(Paragraph('"$105,000/mo in ad spend sounds like a lot."', S["objection_q"]))
story.append(Paragraph("It is scaled to your own stated $5-7M goal, not current revenue — at that goal it is under 26% of monthly revenue, inside our 35% cap. It also requires sales leadership scoping approval before it goes in a final proposal.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
# FILL: All pricing from the scoping calculation
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Platinum</b>", S["price_main"]),
     Paragraph("$15,997/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, website rebuild, local SEO.", S["price_detail"]),
     Paragraph("<strike>$18,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle + FCOO Director</b>", S["price_main"]),
     Paragraph("$8,394/mo", S["price_main"])],
    [Paragraph("Group coaching plus dedicated Fractional COO Director.", S["price_detail"]),
     Paragraph("<strike>$10,794</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$6,700–$105,000/mo", S["price_main"])],
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
    "Total: $24,391/mo + $6,700-$105,000 ad spend  |  Save $5,400/mo by bundling  |  12.4%-25.9% of goal revenue (aggressive scenario needs scoping approval)",
    S["savings"]))

# ── Build ──
doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
