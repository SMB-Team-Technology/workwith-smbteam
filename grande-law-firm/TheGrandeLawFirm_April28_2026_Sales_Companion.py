"""
Sales Companion PDF — SMB Team
The Grande Law Firm | April 28, 2026 | Rep: Dan Bryant
Internal use only. Do not share with client.
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

OUTPUT_PATH = "grande-law-firm/TheGrandeLawFirm_April28_2026_Sales_Companion.pdf"


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

story.append(Paragraph("The Grande Law Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  April 28, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Cynthia Grande", S["snap_value"]),
     Paragraph("~$1.08M (2025)", S["snap_value"]),
     Paragraph("5+ members", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("20% avg; lead rep 58%; legacy rep 22%; newer hire matches/exceeds lead rep", S["snap_value"]),
     Paragraph("Torrance + San Bruno, CA", S["snap_value"])],
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

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: OPERATIONAL FREEDOM", S["section"]))
story.append(Paragraph("Cynthia wants a firm that keeps growing whether she is in the office or not.", S["subsection"]))

story.append(quote_block("About five months ago our leads started declining — we were at a similar run rate to last year and that worries me for 2026."))
story.append(Spacer(1, 1))
story.append(quote_block("My lead intake rep converts around 58% but one of my other reps is around 22%. I know that gap is costing us."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Lead predictability.</b> A system generating immigration cases monthly — not dependent on her network."))
story.append(bd("<b>CEO freedom.</b> Months away (new baby, parents' Europe trip) without the firm missing a beat."))
story.append(bd("<b>$5–6M by year three</b> at 30% net — as true CEO with an ops director, not as a managing attorney."))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No paid ads ever.</b> All leads from referrals or organic — volume declining five months running."))
story.append(b("<b>Intake gap.</b> Legacy rep at 22% vs. 58% standard — no script or accountability structure in place."))
story.append(b("<b>Current coaching overlap.</b> Committed to HTM through August; cautious about stacking commitments."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Replaces referral dependency with paid channels — leads arrive whether or not Cynthia is networking."))
story.append(bd("First dedicated Spanish campaign in Compton, South Gate, Huntington Park — no competitor is running this yet."))

story.append(Paragraph("<b>Full Service Growth Marketing — Growth Tier  |  $7,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1.08M — Growth tier ($1M–$3M) is the correct match; Essentials excluded at $1M+."))
story.append(b("Spanish campaign required — ICP is Spanish-speaking working-class families; English-only misses them."))
story.append(b("No website rebuild needed — newly redesigned site; optimization only (header CTA, footer NAP, H1)."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Closes the 36-point intake gap — script and training that brings all three reps to the 58% standard."))
story.append(bd("Builds the accountability layer that lets Cynthia step back without being the fallback during disruptions."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Cynthia is already CEO — she needs systems coaching, not delegation coaching."))
story.append(b("Lawmatics + CallRail already in place — coaching can use live data from day one."))
story.append(b("Intake conversion fix is six-figure annual ROI at zero additional marketing spend."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("The Grande Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Conservative ($7K): ~14 cases/mo at ~$3,500–$5,000 = $49K–$70K revenue vs. $7K spend (~7–10x)."))
story.append(bd("Aggressive ($14K): ~28–34 cases/mo at ~$3,500–$5,000 = $98K–$119K revenue vs. $14K spend (~7–9x)."))

story.append(Paragraph("<b>Recommended Ad Spend Range ($7,000–$14,000/mo):</b>", S["subsection"]))
story.append(b("<b>Conservative $7,000/mo:</b> LSA $900 + Spanish PPC $3,000 + English PPC $2,000 + Meta retargeting $1,100."))
story.append(b("<b>Aggressive $14,000/mo:</b> LSA $2,000 + Spanish PPC $5,000 + English PPC $4,000 + Meta lead gen $3,000."))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Confirmed on April 29 call:</b> Cynthia's target is $7K–$14K/mo to add ~14 cases/month."))
story.append(b("CPL benchmarks confirmed: LSA ~$55; PPC English ~$100; PPC Spanish ~$100–$125; social ~$50."))
story.append(b("At aggressive: $10,597 fee + $14,000 ads = $24,597/mo = 27.3% of revenue. Under 35% cap."))
story.append(Paragraph("<i>All projections are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"We got to a million without ads — why spend now?"', S["objection_q"]))
story.append(Paragraph("Lead volume has been declining for five months. To hit $1.5M (39% growth) referrals alone will not close the gap. Sharon Abaud has 187 reviews and a Spanish-language brand — she is capturing the same families right now.", S["objection_a"]))

story.append(Paragraph('"What if advertising does not work for immigration?"', S["objection_q"]))
story.append(Paragraph("LSA for immigration pays only when a prospect calls — approximately $55/lead in this market. Spanish-language PPC in Compton and South Gate is underpriced because competitors are not running it. The question is who moves first.", S["objection_a"]))

story.append(Paragraph('"I already have a coaching commitment through August — I don\'t want to overlap."', S["objection_q"]))
story.append(Paragraph("Marketing launches now regardless — the firm cannot afford five more months of declining leads. Coaching can be structured to align with August completion or begin immediately on operational accountability only. These are separate tracks.", S["objection_a"]))

story.append(Paragraph('"I\'ve heard horror stories about auto-renew billing and not owning the assets."', S["objection_q"]))
story.append(Paragraph("SMB Team does not auto-renew. Clients sign and renew intentionally. All ad accounts, website assets, and data belong to the firm — not to us. We confirmed this directly on the April 29 call; Cynthia left satisfied on asset ownership.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Growth Marketing</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("LSA + Google PPC (English &amp; Spanish) + Meta + website optimization.", S["price_detail"]),
     Paragraph("<strike>$7,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, intake scripting + training, KPI dashboards, ops design.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,000–$14,000/mo", S["price_main"])],
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
    "Total: $10,597/mo + $7,000–$14,000 ad spend  |  Save $897/mo by bundling  |  19.6%–27.3% of revenue (under 35% cap)",
    S["savings"]))

# ── Build ──
doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

# Page count check via raw PDF
with open(OUTPUT_PATH, 'rb') as f:
    content = f.read().decode('latin-1')
import re
counts = re.findall(r'/Count\s+(\d+)', content)
print(f"PDF /Count values: {counts}")
# Count actual page objects
page_objs = len(re.findall(r'/Type\s*/Page[^s]', content))
print(f"Page objects: {page_objs}")
