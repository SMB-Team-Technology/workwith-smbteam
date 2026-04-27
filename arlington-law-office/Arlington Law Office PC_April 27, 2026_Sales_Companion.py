"""
Sales Companion PDF — Arlington Law Office, PC
SMB Team  |  April 27, 2026  |  Rep: Randy Gold
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

OUTPUT_PATH = "arlington-law-office/Arlington Law Office PC_April 27, 2026_Sales_Companion.pdf"


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
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY,
                       spaceBefore=3, spaceAfter=3)

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

story.append(Paragraph("Arlington Law Office, PC", S["title"]))
story.append(Paragraph("Sales Companion  |  April 27, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Rose Bui", S["snap_value"]),
     Paragraph("~$600K/yr", S["snap_value"]),
     Paragraph("4 people", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("95%", S["snap_value"]),
     Paragraph("Garden Grove, CA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: PROOF", S["section"]))
story.append(Paragraph("Rose wants to prove a solo law firm can reach $1M+ without partners — on her own terms.", S["subsection"]))

story.append(quote_block("I want to reach $1 million — I've been told that's unprecedented outside of PI for a solo practitioner, but I want to prove it can be done."))
story.append(Spacer(1, 1))
story.append(quote_block("Rose closes 95% of qualified leads she meets with — the problem is the pipeline. We need more leads coming in."))
story.append(Spacer(1, 1))
story.append(quote_block("We're at 8 cases a month and the team can handle 16 — we just don't have the marketing to fill that capacity."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Prove the model.</b> $1M+ as a solo firm without partners — a milestone the industry says is impossible."))
story.append(bd("<b>A predictable pipeline.</b> Leads arriving from a system, not from whoever referred someone this week."))
story.append(bd("<b>A team that runs itself.</b> Firm operates without her in the room so she focuses on strategy, not operations."))

story.append(Spacer(1, 1))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No lead gen system.</b> 70% of clients are uncontrolled referrals — no system predicts or scales that flow."))
story.append(b("<b>Rose is the intake.</b> She screens every lead personally; volume increases risk overwhelming her."))
story.append(b("<b>No accountability layer.</b> The team runs through Rose and Ted with no structure for independent operation."))
story.append(b("<b>PPC skepticism.</b> Two years of below-10% conversion campaigns left her skeptical of paid advertising."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Fills her calendar from a system — not from whoever happened to refer someone this week."))
story.append(bd("Reaches Vietnamese- and Spanish-speaking communities that only Rose and her team can authentically serve."))

story.append(Paragraph("<b>Full Service Marketing — Growth Tier  |  $7,397/mo bundled</b>", S["subsection"]))
story.append(b("$1M+ goal and 7/10 Competitive Urgency Score exceed the Starter tier's scope and ad spend cap."))
story.append(b("Multilingual Vietnamese and Spanish campaigns require full-service execution, not an ads-only package."))
story.append(b("Prior PPC failed because of structure and landing pages — rebuilding correctly requires full-service support."))
story.append(b("Yekrangi has 114+ reviews and a Garden Grove landing page — catching up demands a coordinated multi-channel push."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Turns a 4-person team running on Rose's personal effort into a 4-person team running on systems."))
story.append(bd("Preserves the 95% close rate at higher volume by building an intake framework that works without Rose present."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Path to $1M+ is operational as much as it is marketing — the team has capacity but lacks structure."))
story.append(b("Transcript confirmed task assignments with deadlines as an improvement area — coaching addresses this directly."))
story.append(b("Weekly coaching cadence keeps the roadmap on track as lead volume increases and the team scales up."))
story.append(b("Adding marketing without adding structure at $600K risks burnout before reaching $1M+."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Arlington Law Office — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Fills unused team capacity — at 8 of 16 possible cases/month, every new case from ads is near-pure revenue upside."))
story.append(bd("At 95% close rate, every qualified lead that reaches Rose is almost a signed case — ad spend is the multiplier."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,000/mo — Google PPC + LSA minimums for immigration and estate planning in Garden Grove."))
story.append(b("<b>Aggressive:</b> $8,000/mo — adds Meta retargeting, Vietnamese/Spanish campaigns, and expanded geo-targeting."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~8–10 cases × $4,500 avg = ~$40,000/mo vs. $5,000 spend = ~8x return."))
story.append(b("<b>Aggressive:</b> ~12–15 cases × $4,500 avg = ~$60,000/mo vs. $8,000 spend = ~8x return."))
story.append(Paragraph("<i>Estimates based on OC immigration/estate planning CPL benchmarks and the firm's 95% close rate. Not guaranteed. EB-5 and business law cases may increase returns significantly.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Immigration PPC $3,000 + LSA $2,000 = $5,000 (channel minimums, Garden Grove market)."))
story.append(b("<b>Aggressive:</b> $1M goal × 20% ÷ 12 × 1.3 (Tier 2 OC) × 1.33 (Spanish) = $28,817 available; $8,000 is the recommended starting entry point."))
story.append(b("Total at aggressive: $8,000 + $10,597 = $18,597/mo = 37.2% of current revenue. Validated against $1M goal: 22.3% — well under cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"We tried PPC before and it didn\'t work."', S["objection_q"]))
story.append(Paragraph("Prior campaigns likely sent traffic to the homepage, not a dedicated landing page — that structural flaw explains the sub-10% conversion rate, not the channel. SMB Team builds conversion-optimized landing pages before the first dollar is spent.", S["objection_a"]))

story.append(Paragraph('"We\'re already at $600K on referrals — why change what\'s working?"', S["objection_q"]))
story.append(Paragraph("Rose is at 8 of 16 possible cases/month. Getting to $1M+ requires ~64 additional cases per year — referrals cannot reliably deliver that volume or be predicted, controlled, or scaled.", S["objection_a"]))

story.append(Paragraph('"The monthly investment feels high for where we are."', S["objection_q"]))
story.append(Paragraph("At conservative ad spend, total SMB cost is ~$15,597/mo vs. ~$40,000 projected new revenue — a net-positive position from month one at Rose's 95% close rate.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth Tier</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, landing pages, GBP, multilingual campaigns.", S["price_detail"]),
     Paragraph("<strike>$8,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, intake system design, team accountability framework.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,000–$8,000/mo", S["price_main"])],
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
    "Total: $10,597/mo + $5,000–$8,000 ad spend  |  Save $1,897/mo by bundling  |  31.2%–37.2% of current revenue",
    S["savings"]))

# ── Build ──
doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

import re
data = open(OUTPUT_PATH, 'rb').read()
pages = len(re.findall(b'/Type\\s*/Page[^s]', data))
print(f"Page count: {pages}")
if pages != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
else:
    print("OK: Exactly 2 pages confirmed.")
