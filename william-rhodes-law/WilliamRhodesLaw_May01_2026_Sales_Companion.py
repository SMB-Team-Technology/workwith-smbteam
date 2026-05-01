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

OUTPUT_PATH = "william-rhodes-law/WilliamRhodesLaw_05012026_Sales_Companion.pdf"


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

story.append(Paragraph("William Rhodes Law Trial Attorneys", S["title"]))
story.append(Paragraph("Sales Companion  |  May 01, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Eric Rhodes", S["snap_value"]),
     Paragraph("$500K", S["snap_value"]),
     Paragraph("Solo", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15%", S["snap_value"]),
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
story.append(Spacer(1, 4))

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: FREEDOM + EXIT", S["section"]))
story.append(Paragraph("Eric wants fewer hours, more money, and a clean firm exit at $2M+ in 8–10 years.", S["subsection"]))

story.append(quote_block("Scale to $1M+ in 12–18 months to enable a sustainable lifestyle — fewer hours, more money — and a long-term exit."))
story.append(Spacer(1, 1))
story.append(quote_block("Transition to handling 2–3 cases at a time while generating $2M+ annually."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable leads.</b> End the referral dependency so revenue is reliable month to month."))
story.append(bd("<b>An A-player paralegal.</b> Hire support so he can focus on high-value trial work, not intake and discovery."))
story.append(bd("<b>A firm worth selling.</b> Clean financials, a self-running team, and an exit at $2M+ on his timeline."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No marketing system.</b> 26 years of referrals — no paid ads, no SEO, no GBP — revenue is unpredictable."))
story.append(b("<b>Houston PI is brutal.</b> Top competitors spend $15K–$50K/mo and hold every Maps and LSA spot he does not."))
story.append(b("<b>Salary gap blocks good hires.</b> $60–70K budget vs. $110–115K market rate for an experienced paralegal."))
story.append(b("<b>No intake system.</b> When marketing goes live, Eric will be overwhelmed with no process to convert the leads."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Replaces referral dependency with a predictable PI and commercial litigation lead flow every month."))
story.append(bd("Fixes the dual-domain split and rebuilds the website so paid traffic has a site that converts."))

story.append(Paragraph("<b>Full Service Marketing Growth  |  $6,397/mo bundled</b>", S["subsection"]))
story.append(b("PI + aggressive goals + $10K PI floor exceed Starter cap ($8K) — Growth tier required."))
story.append(b("Houston = Tier 1 market; PI CPCs exceed $100/click; Growth cap ($15K) covers full ad spend range."))
story.append(b("Website rebuild needed: site blocks crawlers, no bio or video, authority split across two domains."))
story.append(b("Stand-alone $7,997/mo — bundling saves $1,600/mo."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the intake script and SOP library so the next paralegal hire actually succeeds."))
story.append(bd("Coaches Eric from solo operator to firm manager — $500K to $1M is a systems gap, not a talent gap."))

story.append(Paragraph("<b>Elite Coach Plus  |  $2,200/mo bundled</b>", S["subsection"]))
story.append(b("$400K–$1M, solo, aggressive goals — maps directly to Elite Coach Plus."))
story.append(b("Previous hires failed without SOPs; coaching builds the infrastructure before the next hire."))
story.append(b("Includes weekly coaching, PI/commercial lit masterminds, quarterly workshops, and annual in-person."))
story.append(b("Stand-alone $3,497/mo — bundling saves $1,297/mo."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("William Rhodes Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Conservative: puts the firm on the map in Houston PI — est. 6 cases/month at 3.9x return."))
story.append(bd("Aggressive: targets the $1M goal — est. 11 cases/month at 4.8x return on ad spend."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $10,000/mo — PI high-competitiveness floor for Houston."))
story.append(b("<b>Aggressive:</b> $15,000/mo — Growth tier cap; full budget for the $1M goal."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~6 cases x $6,500 = ~$39,000/mo vs. $10,000 spend = 3.9x."))
story.append(b("<b>Aggressive:</b> ~11 cases x $6,500 = ~$71,500/mo vs. $15,000 spend = 4.8x."))
story.append(Paragraph("<i>Estimates only. 15% close rate, $6,500 Accident &amp; Injury default case value. Actual values may be higher.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Channel minimums sum to $6,700; PI Houston hard floor = $10,000."))
story.append(b("<b>Aggressive:</b> $1M x 20% / 12 = $16,667. Tier 1 (1.5x) = $25,000. Minus $6,397 fee = $18,603. Capped at $15,000 (Growth tier)."))
story.append(b("At aggressive: $21,397 / $83,333 goal revenue = 25.7% — under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"This is a big investment — I need to think about it."', S["objection_q"]))
story.append(Paragraph("Zehl (1,262 reviews), Arnold &amp; Itkin (1,186 reviews), and Brian White (1,000+ reviews) are already holding every Maps and LSA spot in Houston. Waiting one more month extends their lead. The cost of inaction is real.", S["objection_a"]))

story.append(Paragraph('"I\'m not sure I can handle more leads as a solo attorney."', S["objection_q"]))
story.append(Paragraph("Coaching starts with intake and SOPs first — before leads increase. The paralegal becomes affordable at $1M; the system that makes that hire succeed gets built now.", S["objection_a"]))

story.append(Paragraph('"What if ads don\'t work in Houston? It\'s too competitive."', S["objection_q"]))
story.append(Paragraph("The $10K conservative floor accounts for Houston pricing. Eric also has a first-mover advantage with Spanish-language PI campaigns — a channel most Houston competitors have not touched.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Growth</b>", S["price_main"]),
     Paragraph("$6,397/mo", S["price_main"])],
    [Paragraph("Website rebuild, SEO, Google Ads, LSA, Meta Ads — full managed service.", S["price_detail"]),
     Paragraph("<strike>$7,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$2,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, masterminds, workshops, SOPs, hiring roadmap, intake system.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$10,000–$15,000/mo", S["price_main"])],
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
    "Total: $8,597/mo + $10,000–$15,000 ad spend  |  Save $2,897/mo by bundling  |  25.7%–39.4% of revenue (under 35% cap at goal revenue)",
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
