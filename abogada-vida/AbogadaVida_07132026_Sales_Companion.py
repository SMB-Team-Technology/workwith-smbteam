"""
Sales Companion PDF — Abogada Vida PLLC
Generated: July 13, 2026 | Sales Rep: Dan Bryant
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

OUTPUT_PATH = "abogada-vida/AbogadaVida_07132026_Sales_Companion.pdf"


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

story.append(Paragraph("Abogada Vida PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  July 13, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Mahsa Mohkamkar", S["snap_value"]),
     Paragraph("~$600K est.", S["snap_value"]),
     Paragraph("9 people", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("40.7%", S["snap_value"]),
     Paragraph("Schnecksville, PA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE AND DOMINATE", S["section"]))
story.append(Paragraph("Vivid Vision: $1M Year 1, $3M Year 2, $7M Year 3 — build a multi-attorney firm that runs itself.", S["subsection"]))

story.append(quote_block("Marketing budget was decreased for case types that are referred out"))
story.append(Spacer(1, 1))
story.append(quote_block("~30% of leads (removal/detainee) are referred out — no attorney with that specialty"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Hit $1M in Year 1.</b> Explicit three-year targets: $1M, $3M, $7M — not aspirations."))
story.append(bd("<b>Stop giving away 30% of leads.</b> Hire a removal defense attorney, capture that revenue in-house."))
story.append(bd("<b>Freedom from operations.</b> Hasn't opened client emails in 3 months — wants same at the attorney level."))
story.append(bd("<b>Bilingual market dominance.</b> Serve the Lehigh Valley's Spanish-speaking immigrant community better than any English-only competitor."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No paid lead system.</b> Firm not appearing in local search or paid ads for Allentown immigration searches."))
story.append(b("<b>Geographic gap.</b> Schnecksville is 15 miles from Allentown; no city landing pages = underperforming paid and organic."))
story.append(b("<b>NAP inconsistency.</b> Two phone numbers across directories suppressing local pack ranking despite 96 reviews."))
story.append(b("<b>Intake gap.</b> Karen books 66%; Gabby books 26.7% — 40-point gap on the same leads."))
story.append(b("<b>Solo attorney bottleneck.</b> Revenue ceiling = Mahsa's personal bandwidth until second hire."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Places Abogada Vida in front of Allentown's Spanish-speaking community in English and Spanish — on Google, LSA, and Meta — before they call a competitor."))
story.append(bd("City-specific landing pages close the Schnecksville/Allentown geo gap; LSA enrollment activates the 96-review advantage at the top of Google."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("~$600K revenue places firm in $400K–$1M band — Starter tier correct."))
story.append(b("Website rebuild needed: 14-sec load, no city pages, no above-fold form."))
story.append(b("Spanish multiplier (1.33x) applied — bilingual campaigns required for $1M goal."))
story.append(b("Stand-alone $5,697/mo — saves $850/mo bundled."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Weekly accountability to the $1M target — intake coaching, KPIs, and a structured attorney hiring plan."))
story.append(bd("Closes the Karen/Gabby 40-point booking gap through call review and structured performance coaching."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("$400K–$1M revenue band — Elite Coach Plus is the correct tier."))
story.append(b("Weekly group coaching, masterminds, quarterly workshops, annual in-person."))
story.append(b("Stand-alone $3,497/mo — saves $297/mo bundled."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Abogada Vida PLLC — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Generates estimated 32–90 immigration leads per month from paid channels alone — adding pipeline on top of the organic and referral base that already exists."))
story.append(bd("At 40.7% close rate and ~$5,250 avg case value, conservative spend alone projects ~$68K/mo in new revenue — more than the firm's best month on record."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $4,000/mo — immigration channel minimums x 1.33 Spanish multiplier."))
story.append(b("<b>Aggressive:</b> $9,000/mo — at Starter tier cap; Growth tier upgrade needed to scale further toward $1M goal."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative ($4K/mo):</b> ~32 leads x 40.7% = ~13 cases x $5,250 = ~$68K/mo | ~17x ROAS."))
story.append(b("<b>Aggressive ($9K/mo):</b> ~90 leads x 40.7% = ~37 cases x $5,250 = ~$194K/mo | ~22x ROAS."))
story.append(Paragraph("<i>Estimates based on industry CPL averages and firm-stated close rate. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Immigration channel mins ($3,200) x 1.33 Spanish multiplier = $4,256 rounded to $4,000."))
story.append(b("<b>Aggressive:</b> $1M x 20% / 12 x Tier 4 x 1.33 Spanish = $22,167 minus $4,847 fee = $17,320; capped at Starter $9,000."))
story.append(b("Total at aggressive: $17,047/mo = 34.1% of revenue — under 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I already have systems — why do I need coaching?"', S["objection_q"]))
story.append(Paragraph("Case delivery works. Growth does not. Intake has a 40-point booking gap (Karen 66%, Gabby 26.7%), revenue swings $36K–$66K monthly, and no $1M plan exists. Elite Coach Plus fixes all three.", S["objection_a"]))

story.append(Paragraph('"Can ads work from Schnecksville for Allentown searches?"', S["objection_q"]))
story.append(Paragraph("Yes. Lehigh Valley Immigration Law LLC (2025, fewer reviews) already ranks and runs bilingual Allentown ads. City-specific landing pages and NAP fix close the geo gap. The 96-review advantage just needs to be activated.", S["objection_a"]))

story.append(Paragraph('"$8,047/month is a lot before the second attorney is hired."', S["objection_q"]))
story.append(Paragraph("Conservative ads project ~$68K/mo in new revenue. Total with $4K ads: ~$12K/mo = 24% of revenue — under the 35% cap. Marketing generates the revenue that justifies the hire, not the other way around.", S["objection_a"]))

story.append(Paragraph('"We can\'t serve removal cases yet — why market them?"', S["objection_q"]))
story.append(Paragraph("Family immigration and humanitarian campaigns launch first. Removal ads are added once the second attorney is hired — part of the coaching plan. Marketing funds the hire; the hire unlocks the next ad category.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, bilingual Google Ads, Local SEO, LSA, Meta Ads.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$4,000–$9,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $4,000–$9,000 ad spend  |  Save $1,147/mo by bundling  |  24.1%–34.1% of revenue (under 35% cap)",
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
