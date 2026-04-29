"""
Sales Companion PDF — Blancarte Law
SMB Team | April 29, 2026 | Rep: Randy Gold
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

OUTPUT_PATH = "blancarte-law/BlancarteLaw_April29_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Blancarte Law, APC", S["title"]))
story.append(Paragraph("Sales Companion  |  April 29, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Jesse &amp; James Blancarte (owners); Patricia Parker (ops)", S["snap_value"]),
     Paragraph("~$1M/yr", S["snap_value"]),
     Paragraph("2 attorneys + ops + paralegals", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Downtown LA, 90017", S["snap_value"])],
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
story.append(Paragraph("Jesse and James want a firm that runs without them — vacations without disruption, attorneys doing attorney work, and no bottlenecks.", S["subsection"]))

story.append(quote_block("Attorneys able to take vacations without disruption; clear delegation (paralegals do paralegal work), no bottlenecks."))
story.append(Spacer(1, 1))
story.append(quote_block("Focus on managing the business vs. working in it; better delegation; improved consistency."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What they want:</b>", S["subsection"]))
story.append(bd("<b>Time freedom.</b> Jesse and James want real vacations without the firm needing them."))
story.append(bd("<b>A self-managing team.</b> Paralegals do paralegal work; Patricia owns ops; attorneys own strategy."))
story.append(bd("<b>Predictable revenue.</b> James's target: $150K/month — tracked, not discovered at year end."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping them:</b>", S["subsection"]))
story.append(b("<b>Zero digital presence.</b> No ads, no reviews, no SEO — 100% dependent on one nonprofit referral source."))
story.append(b("<b>Intake leakage.</b> Current vendor in place but leads fall through after hours; no bilingual coverage."))
story.append(b("<b>No scorecards.</b> No KPIs for any role — Patricia cannot manage what is not measured."))
story.append(b("<b>No financial visibility.</b> James handles books manually; declining margins, no forward-looking dashboard."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>Full Service Marketing — Growth  |  $3,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$1M; Growth tier ($1M–$3M) is the correct tier."))
story.append(b("Website rebuild required — no practice area pages, no bios, no content; must use Full Service."))
story.append(b("LA is Tier 1 (mega market); immigration CPCs $15–$45+; competitive market requires full-stack approach."))
story.append(b("Spanish campaign needed for immigration firm in LA — bilingual capability is underutilized competitive edge."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>Elite Coach Plus  |  $2,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1M+, team under 5 operational threshold — Elite Coach Plus is the correct tier."))
story.append(b("Master's Circle hidden: team size and dedicated staff threshold not clearly met."))
story.append(b("Firm has profit visibility gap and declining margins — coaching cadence addresses both."))
story.append(b("FCOO Advisor ($1,297/mo) added at Phase 2 when firm reaches $120K/month consistently."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Blancarte Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>Recommended Range: $5,500 (conservative) – $8,000 (aggressive)/mo</b>", S["subsection"]))
story.append(b("<b>Conservative ($5,500):</b> Immigration minimums (PPC $2K + LSA $1K + Meta $2.2K) x 1.33 Spanish modifier = ~$5,500. Est. 7 cases x $4,500 = $31,500/mo — 5.7x return."))
story.append(b("<b>Aggressive ($8,000):</b> Growth tier cap. $1.8M goal x 20% / 12 x 1.5 (Tier 1 LA) x 1.33 (Spanish) = $59,850 — capped at $8,000. Est. 12 cases x $4,500 = $54,000/mo — 6.75x return."))
story.append(b("Total at aggressive: $5,597 + $8,000 = $13,597/mo = 16.3% of revenue. Well under the 35% cap."))
story.append(Paragraph("<i>All ROI figures are estimates. Case value uses immigration default ($4,500); none stated on call.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If They Push Back ──
story.append(Paragraph("If They Push Back", S["section"]))

story.append(Paragraph('"How is this different from our current intake vendor?"', S["objection_q"]))
story.append(Paragraph("Attorney Assistant gives Patricia real-time visibility — recorded calls, 24/7 bilingual coverage, direct CRM integration. Ask her: does your current vendor give you that visibility right now?", S["objection_a"]))

story.append(Paragraph('"We already have a CRM and an answering service."', S["objection_q"]))
story.append(Paragraph("Infrastructure that exists but is not optimized produces the same result as no infrastructure. The transcript confirmed leads are falling through. Answering calls is not the same as qualifying, following up, and converting.", S["objection_a"]))

story.append(Paragraph('"The market is competitive — will ads work for immigration in LA?"', S["objection_q"]))
story.append(Paragraph("Goldstein Immigration — 4 blocks away on Wilshire — doubled client intake via Google PPC. The market is competitive because demand is high. The question is not whether ads work. It is whether Blancarte Law will be in the auction.", S["objection_a"]))

story.append(Paragraph('"Profit is down — we\'re not sure we can afford this."', S["objection_q"]))
story.append(Paragraph("Profit is down because growth has been passive. At 7 additional cases/month from conservative ad spend, the plan generates ~$31,500 vs. $5,500 spent — paying for itself including management fees within the first quarter.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$3,397/mo", S["price_main"])],
    [Paragraph("Website rebuild + Google Ads + LSA + Meta (English &amp; Spanish) + review system + GBP.", S["price_detail"]),
     Paragraph("<strike>$4,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$2,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching + KPI scorecards + intake accountability + monthly financial review.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,500–$8,000/mo", S["price_main"])],
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
    "Total: $5,597/mo + $5,500–$8,000 ad spend  |  Save $2,897/mo by bundling  |  13.7%–16.4% of revenue (under 35% cap)",
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
