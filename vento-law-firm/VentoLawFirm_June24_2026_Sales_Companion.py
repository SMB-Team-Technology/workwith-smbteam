"""
Sales Companion PDF — SMB Team
Vento Law Firm | June 24, 2026 | Rep: Nick Holderman
FOR INTERNAL USE ONLY; DO NOT SHARE.
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

OUTPUT_PATH = "vento-law-firm/VentoLawFirm_06242026_Sales_Companion.pdf"


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
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=ACCENT_GREEN, spaceBefore=5, spaceAfter=1)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=DARK_NAVY, spaceBefore=1, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.5, leading=13, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=0, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9.5, leading=13, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=0, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9.5, leading=13, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9.5, leading=12, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9.5, leading=13, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=1)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8.5, leading=11, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


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

story.append(Paragraph("Vento Law Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  June 24, 2026  |  Rep: Nick Holderman", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Idalis Vento, Esq.", S["snap_value"]),
     Paragraph("~$180K/yr", S["snap_value"]),
     Paragraph("Solo, 0 staff", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (est.)", S["snap_value"]),
     Paragraph("Tampa, FL", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: SUSTAINABLE INDEPENDENCE", S["section"]))
story.append(Paragraph("She wants a firm that runs on systems, not fear — so she stops taking cases out of desperation.", S["subsection"]))

story.append(quote_block("Case volume dropped from ~25 to 10 active matters since April — financially unsustainable."))
story.append(Spacer(1, 1))
story.append(quote_block("Vision: hire full-time assistant and intake staff, purchase an office building. Two-year goal."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable case flow.</b> Stop wondering if the phone will ring; plan from a real pipeline."))
story.append(bd("<b>A team so she can step back.</b> Intake coordinator and assistant — once revenue is stable."))
story.append(bd("<b>The building.</b> Office purchase requires consistent, forecastable profit — not referral luck."))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No lead system.</b> 100% referrals; zero paid ads ever run; invisible in local search at 32 reviews."))
story.append(b("<b>No intake infrastructure.</b> Handles every call herself; no after-hours coverage; form below fold."))
story.append(b("<b>Revenue in contraction.</b> Down 60% from peak; unsustainable by her own description."))
story.append(b("<b>Scoping flag: Revenue under $250K — scoping approval required before contract.</b>"))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Paid calls from people searching for a criminal defense attorney — starting week one."))
story.append(bd("Website converts crisis visitors; review campaign builds toward LSA threshold."))

story.append(Paragraph("<b>Full Service Marketing — Essentials  |  $3,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $180K is under $400K — Essentials is correct tier; no stand-alone retail price."))
story.append(b("Tampa paid search underdeveloped: only Fernandez confirmed running ads. Open market."))
story.append(b("Website rebuild needed (no above-fold CTA, no urgency language) — Full Service required."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Intake scripts and qualification process so paid leads convert — not just more calls."))
story.append(bd("Hiring roadmap and accountability to bring on intake coordinator in the right sequence."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled (saves $897 vs. $3,497 stand-alone)</b>", S["subsection"]))
story.append(b("Revenue under $400K — Elite Coach is correct tier per eligibility table."))
story.append(b("Docket Flow: 8 leads, 0 clients. Intake problem, not a lead volume problem. Coaching fixes this."))
story.append(b("Bundling saves $897/mo vs. purchasing Elite Coach separately."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Vento Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Conservative $5,500/mo: ~24 leads, ~4 cases, ~$14,000/mo new revenue. Est. 2.5x return."))
story.append(bd("Aggressive $7,500/mo: ~39 leads, ~6 cases, ~$24,000/mo new revenue. Est. 3.1x return."))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Criminal Defense minimums: PPC $1,500 + LSA $1,000 + Meta $700 + Spanish uplift = $5,500."))
story.append(b("<b>Aggressive:</b> $360K goal x 20% / 12 = $6,000. Reverse math: 33 leads x $190 CPL = $6,270 -> $7,500."))
story.append(b("CPL: $190/call (Tampa criminal defense LSA). Close rate: 15% est. Avg case: $4,000 est. Confirm on call."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Confirm average case value June 24.</i>", S["disclaimer"]))

story.append(thin_rule())

story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"The monthly fee is too high right now."', S["objection_q"]))
story.append(Paragraph("Conservative $5,500 ad spend yields est. 3–4 cases/mo at $4,000 avg = $12,000–$16,000 new revenue. Two additional cases/mo covers both packages. Staying at 10 cases means revenue keeps declining.", S["objection_a"]))

story.append(Paragraph('"I tried paid leads with Docket Flow — got nothing."', S["objection_q"]))
story.append(Paragraph("Docket Flow sends arrest-record leads who didn't search for an attorney. SMB Team targets people who type 'criminal defense attorney Tampa' after an arrest. High intent vs. cold outreach — completely different conversion profile.", S["objection_a"]))

story.append(Paragraph('"My reviews are only at 32 — will ads even work?"', S["objection_q"]))
story.append(Paragraph("Google Ads run independent of review count — page 1 visibility starts day one. LSA performance improves as the review campaign builds toward 75+. We run both simultaneously. Sammis (161 reviews) and Hanlon Law (61 reviews) started somewhere too.", S["objection_a"]))

story.append(Paragraph('"Can we skip coaching and just do marketing?"', S["objection_q"]))
story.append(Paragraph("8 leads and 0 clients on Docket Flow confirms an intake problem. More ads without an intake process repeats that result. Coaching delivers the qualification scripts and follow-up system that turns calls into signed cases.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Essentials</b>", S["price_main"]),
     Paragraph("$3,397/mo", S["price_main"])],
    [Paragraph("Website, Google Ads, LSA, SEO/AEO, GBP, review campaign, directories.", S["price_detail"]),
     Paragraph("No stand-alone retail", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly coaching, intake development, hiring roadmap, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,500–$7,500/mo", S["price_main"])],
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
    "Total: $5,997/mo + $5,500–$7,500 ad spend  |  Save $897/mo by bundling  |  Scoping approval required (revenue under $250K)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
