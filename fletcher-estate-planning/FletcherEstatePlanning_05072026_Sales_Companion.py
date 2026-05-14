"""
Sales Companion PDF — Fletcher Estate Planning
SMB Team | May 07, 2026 | Rep: Michael Kopp
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

OUTPUT_PATH = "fletcher-estate-planning/FletcherEstatePlanning_05072026_Sales_Companion.pdf"


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

story.append(Paragraph("Fletcher Estate Planning", S["title"]))
story.append(Paragraph("Sales Companion  |  May 07, 2026  |  Rep: Michael Kopp", S["subtitle"]))
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
    [Paragraph("Jim Fletcher", S["snap_value"]),
     Paragraph("~$420K/yr", S["snap_value"]),
     Paragraph("3 (family)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("79%", S["snap_value"]),
     Paragraph("Sandy Springs, GA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM", S["section"]))
story.append(Paragraph("Jim wants $840,000 in revenue and a firm that generates income without requiring his constant personal presence.", S["subsection"]))

story.append(quote_block("I want to get to $840,000 — that's the goal I've set for myself."))
story.append(Spacer(1, 1))
story.append(quote_block("I'm considering charging a fee — maybe $99 — to get people to commit so they don't no-show."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>$840K revenue.</b> A clear numerical goal — double his current run rate — set before this call."))
story.append(bd("<b>Predictable leads.</b> Referrals are fragile; he wants a system that produces consistently every month."))
story.append(bd("<b>Time freedom.</b> He handles every consultation personally and wants a firm that can run without him."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No paid lead system.</b> Zero advertising history — all $420K comes from referrals and directory listings."))
story.append(b("<b>Competitive pressure.</b> Perigon (58 reviews, active PPC) and Slowik (Harvard Law, opened Sandy Springs April 2026) are advancing fast."))
story.append(b("<b>Intake gap.</b> No-shows confirmed; after-hours calls go to voicemail with no follow-up process in place."))
story.append(b("<b>Dual domain split.</b> fletcherestateplanning.com and jimfletcherlaw.com divide Google's link authority."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>Full Service Marketing Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$420K sits in the $400K–$1M Starter tier; full service (not ads-only) because website conversion optimization is needed before paid traffic scales."))
story.append(b("Estate planning Google Ads + LSA + Meta covers all three high-intent channels; LSA places Jim above the map pack for zero wasted impressions."))
story.append(b("Atlanta is a Tier 1 geo market — full service management ensures campaigns are optimized for a competitive metro environment."))
story.append(b("No paid advertising history means the firm needs campaign buildout from scratch; ads-only sub-packages require existing infrastructure."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>Elite Coach Plus  |  $2,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M with a growing but thin team maps directly to Elite Coach Plus tier."))
story.append(b("Jim explicitly needs intake systems, no-show reduction, and profit visibility — all core Elite Coach Plus deliverables."))
story.append(b("No dedicated ops function yet — Elite Coach Plus builds the business operating framework before fractional roles are needed."))
story.append(b("Profit blind spots noted (no dashboard, new ad cost category coming) — coaching cadence addresses both immediately."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Fletcher Estate Planning — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>Recommended Range: $2,500 (conservative) – $5,000 (aggressive)/mo</b>", S["subsection"]))
story.append(b("<b>Conservative ($2,500):</b> Estate Planning minimums — PPC $1,500 + LSA $1,000. Est. 7 cases x $3,000 = $21,000/mo — 8.4x return."))
story.append(b("<b>Aggressive ($5,000):</b> Starter tier cap. $840K goal x 20% / 12 x 1.5 (Tier 1 Atlanta) = $21,000 — capped at $5,000. Est. 18 cases x $3,000 = $54,000/mo — 10.8x return."))
story.append(b("Total at aggressive: $7,047 + $5,000 = $12,047/mo = 17.2% of $840K goal revenue. Well under 35% cap."))
story.append(Paragraph("<i>All ROI figures are estimates based on industry averages. Not guaranteed.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"Referrals have gotten me to $420K — why change what\'s working?"', S["objection_q"]))
story.append(Paragraph("To reach $840K, Jim needs roughly 280 clients/year at $3K avg. Referrals alone have never consistently produced that volume — and with Slowik now in Sandy Springs deploying SEO content immediately, the referral environment will get more competitive, not less.", S["objection_a"]))

story.append(Paragraph('"I\'m not sure I\'m ready to spend on advertising."', S["objection_q"]))
story.append(Paragraph("At 79% close rate and $3,000/case, one new client from ads covers an entire month of conservative ad spend. Perigon is running active PPC. Slowik entered the market in April 2026. Every month of delay is a month they build paid visibility Jim cannot easily overcome later.", S["objection_a"]))

story.append(Paragraph('"The total investment feels high right now."', S["objection_q"]))
story.append(Paragraph("At conservative ad spend, total SMB cost is $9,547/mo — 27% of current monthly revenue. The first 3–4 new clients from ads typically offset management fees within 30 days at Jim's case value and close rate.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads + LSA + Local SEO + Meta Ads — full management included.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$2,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching + masterminds + quarterly workshops + intake systems.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$2,500–$5,000/mo", S["price_main"])],
    [Paragraph("Goes directly to Google, LSA, and Meta — not to SMB Team.", S["price_detail"]),
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
    "Total: $7,047/mo + $2,500–$5,000 ad spend  |  Save $2,147/mo by bundling  |  27%–34% of revenue (under 35% cap)",
    S["savings"]))

# ── Build ──
doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

import re
with open(OUTPUT_PATH, 'rb') as f:
    content = f.read()
counts = re.findall(b'/Count\\s+(\\d+)', content)
print(f'Page count: {counts}')
