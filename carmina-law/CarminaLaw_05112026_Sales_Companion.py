"""
Sales Companion PDF — Law Offices of Carmina Fernandes
SMB Team | May 11, 2026 | Rep: Dan Bryant
Internal use only. Do not share with prospect.
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

OUTPUT_PATH = "carmina-law/CarminaLaw_05112026_Sales_Companion.pdf"


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


# ════════════════════════════════════════════════════════
# PAGE 1
# ════════════════════════════════════════════════════════
story = []

story.append(Paragraph("Law Offices of Carmina Fernandes", S["title"]))
story.append(Paragraph("Sales Companion  |  May 11, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Carmina Fernandes", S["snap_value"]),
     Paragraph("$325K–$350K/yr", S["snap_value"]),
     Paragraph("Solo + staff", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("~15% (est.)", S["snap_value"]),
     Paragraph("Ludlow, MA", S["snap_value"])],
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
story.append(Paragraph("She needs a firm that runs without her — not as a goal, but as a medical necessity.", S["subsection"]))

story.append(quote_block("Operations/processes are the constraint; not client demand."))
story.append(Spacer(1, 1))
story.append(quote_block("Needs delegation, reliable processes, and A-players while managing medical travel."))
story.append(Spacer(1, 1))
story.append(quote_block("Booked this call due to interest in AI to solve operational bottlenecks."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>A firm that runs while she's away.</b> She travels to Brazil regularly for medical treatment — the firm cannot require her physical presence to function."))
story.append(bd("<b>Predictable immigration revenue.</b> Family petitions at $3K and removal defense at $6K–$7K are the cases she wants — not $950 estate plans that drain time."))
story.append(bd("<b>Bilingual systems that work 24/7.</b> Spanish and Portuguese-speaking immigrant families call after hours — she wants those leads captured and booked automatically."))
story.append(bd("<b>A path to $1M.</b> She set a clear goal: $500K–$600K this year, $1M next year — and she wants a roadmap, not just ambition."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No marketing infrastructure.</b> Website not indexed by Google; GBP misconfigured; zero paid advertising ever run."))
story.append(b("<b>Broken intake.</b> No dedicated receptionist, no after-hours coverage, no call tracking — leads are leaking before anyone talks to them."))
story.append(b("<b>No team accountability.</b> Staff operates without KPIs; contractors fire without communication standards; owner is the default for every escalation."))
story.append(b("<b>Practice mix friction.</b> Low-fee estate plans ($950) consume attorney time that $3K–$7K immigration cases could fill."))
story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>Full Service Marketing Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $325K–$350K; aggressive goals ($1M by next year) exceed Essentials ad spend cap of $1,500 — Starter required."))
story.append(b("Spanish campaign needed (confirmed on call) — adds 1.33x modifier to ad spend calculation."))
story.append(b("Website crawl issue and GBP misconfiguration require full-service rebuild, not ads-only package."))
story.append(b("Starter includes LSA enrollment — places firm above every other result for immigration attorney searches."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $325K–$350K falls in the $250K–$400K range — Elite Coach is the correct tier."))
story.append(b("Under $500K — FCOO and FCFO products are not eligible yet; Elite Coach is the right starting point."))
story.append(b("Immigration Mastermind (scheduled Thu 5/14) is included — she expressed specific interest in this group."))
story.append(b("SMB differentiator vs. HTM: done-for-you marketing, practice-area masterminds, flexible pivots — not coaching-only."))


# ════════════════════════════════════════════════════════
# PAGE 2
# ════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Carmina Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Generates 6–9 signed immigration cases per month — family petitions and removal defense — without Carmina personally chasing leads."))
story.append(bd("Spanish-language campaigns reach immigrant families searching in their native language, where CPC is lower and Carmina's fluency is an unmatched conversion advantage."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $4,100/mo — Google PPC $2,000 + LSA $900 + Meta Lead Gen $1,000 + Meta Retargeting $200."))
story.append(b("<b>Aggressive:</b> $5,000/mo — Starter cap; Spanish modifier drives need for full budget allocation."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative ($4,100/mo):</b> ~41 leads x 15% close = 6 cases x $3,000 = $18,000/mo vs. $4,100 spend = 4.4x return."))
story.append(b("<b>Aggressive ($5,000/mo):</b> ~61 leads x 15% close = 9 cases x $3,000 = $27,000/mo vs. $5,000 spend = 5.4x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I\'m worried about the cost stacking — answering service, drafting software, CRM on top of your fees."', S["objection_q"]))
story.append(Paragraph("Address the phased approach: answering service (~$300/mo) is the only immediate add-on. CallRail is minimal. CRM evaluation happens after intake foundation is in place. The $18K–$27K/mo in projected ad revenue self-funds everything within the first 30–60 days of ads running.", S["objection_a"]))

story.append(Paragraph('"I\'m going back to HTM. How is this different from what they do?"', S["objection_q"]))
story.append(Paragraph("SMB Team does done-for-you digital marketing (GBP, website rebuild, Google Ads, LSA, Meta) — HTM does not. Practice-area masterminds are monthly and active; her Immigration group meets Thu 5/14. SMB has flexible program pivots and a future fractional CTO for AI implementation. These are complementary services, not competing ones.", S["objection_a"]))

story.append(Paragraph('"What if I can\'t handle the increased call volume?"', S["objection_q"]))
story.append(Paragraph("The bilingual answering service handles volume increase — it answers, qualifies, and books consultations 24/7 with no attorney involvement. First hire is a bilingual intake VA (~$12.50/hr) through SMB’s sister company once volume justifies it. The ads ramp gradually — volume does not spike overnight.", S["objection_a"]))

story.append(Paragraph('"I\'ve been burned by unreliable contractors before."', S["objection_q"]))
story.append(Paragraph("The real estate paralegal fire during the call is the exact problem Elite Coach addresses: proven hiring frameworks, KPI scorecards, and communication standards so contractors operate with accountability — not just on goodwill. The 90-day roadmap prioritizes intake and hiring infrastructure before adding volume.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, GBP optimization, Google Ads (EN/ES), LSA, Meta ads, CallRail, monthly reporting.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly coaching, Immigration Mastermind, hiring templates, KPI frameworks, 90-day roadmap, annual workshop.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$4,100–$5,000/mo", S["price_main"])],
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
    "Total: $7,447/mo + $4,100–$5,000 ad spend  |  Save $1,747/mo by bundling  |  27.2% of goal revenue (under 35% cap)",
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
