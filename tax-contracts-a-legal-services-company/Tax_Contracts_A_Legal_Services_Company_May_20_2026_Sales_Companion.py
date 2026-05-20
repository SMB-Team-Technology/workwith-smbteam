"""
Sales Companion PDF — Tax & Contracts, A Legal Services Company
Sales Rep: Randy Gold | May 20, 2026
Internal document. Do not share with prospect.
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

OUTPUT_PATH = "tax-contracts-a-legal-services-company/Tax_Contracts_A_Legal_Services_Company_May_20_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Tax &amp; Contracts, A Legal Services Company", S["title"]))
story.append(Paragraph("Sales Companion  |  May 20, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Chrystan Carlton", S["snap_value"]),
     Paragraph("~$500K–$1M est.", S["snap_value"]),
     Paragraph("4 FT + 1 PT", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("80% webinar; ~1.75% paid ads", S["snap_value"]),
     Paragraph("Chicago, IL", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 1.2*inch, 0.65*inch])
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
story.append(Paragraph("Chrystan wants a firm that generates $6M without requiring 70-hour weeks — she wants her time back.", S["subsection"]))

story.append(quote_block("My goal is to reach $6 million in revenue within three years."))
story.append(Spacer(1, 1))
story.append(quote_block("We want to return to our peak of 8 to 10 new clients per month."))
story.append(Spacer(1, 1))
story.append(quote_block("One of our agencies provided 57 leads that yielded only one booking."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Fewer hours.</b> Working 60–70+ hours per week; evenings consumed by legal work."))
story.append(bd("<b>Reliable lead flow.</b> Webinars close at 80% but are not built for scale; needs a predictable pipeline."))
story.append(bd("<b>A firm that runs itself.</b> 3–6 year goal: step back and trust the firm operates without her."))
story.append(bd("<b>Clear marketing ROI.</b> Paying 3–4 agencies with no visibility into what is working."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Sole attorney bottleneck.</b> Only she can generate legal revenue — every matter flows through her personally."))
story.append(b("<b>Broken intake.</b> 57 leads produced 1 booking (1.75%) — no structured follow-up system exists for paid leads."))
story.append(b("<b>No attribution.</b> Multiple agencies active, no unified tracking — cannot identify what is working."))
story.append(b("<b>GBP under legacy name.</b> Profile listed as 'Carlton Law, Ltd.' — the Tax &amp; Contracts brand is invisible in local search."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Replaces 3–4 unaccountable agencies with one integrated team tracking every dollar to a cost-per-client outcome."))
story.append(bd("Puts the firm in front of high-intent prospects searching for federal tax and business law attorneys in Chicago."))
story.append(bd("Rebuilds the website into a conversion asset that works with paid traffic — not just a digital brochure."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M bracket; Starter correct tier (Essentials excluded for business/tax practice areas)."))
story.append(b("Website rebuild needed: Wix limits technical SEO, broken nav link, no blog, PageSpeed unconfirmed."))
story.append(b("Spanish campaign: bilingual ops coordinator in place; social enterprise consulting serves Spanish-speaking clients."))
story.append(b("Urgency 7/10: Gordon Law Group (200+ reviews) and The Tax Defenders (280 reviews) dominate every target keyword."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Turns the $6M goal from aspiration into a tracked, milestone-driven plan with weekly accountability."))
story.append(bd("Builds intake process, delegation framework, and team systems that marketing alone cannot create."))

story.append(Paragraph("<b>Elite Coach Plus  |  $2,200/mo bundled</b>", S["subsection"]))
story.append(b("Team under 5 FT staff — Master's Circle excluded; Elite Coach Plus is the correct fit."))
story.append(b("Stage 4 owner with ambitious goals and no coaching accountability — structural match for Elite Coach Plus."))
story.append(b("Intake crisis (1.75% conversion) and team capacity gaps require coaching-level systems work alongside marketing."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Tax &amp; Contracts — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Creates a measurable, attributed paid lead channel that replaces the current unaccountable agency spend with transparent ROI."))
story.append(bd("At conservative spend, projects 2–3 new cases per month from ads — a meaningful revenue addition without requiring more attorney hours."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,200/mo — channel minimums for Business Law (Google PPC $1,500 + LSA $1,000 + Meta $700)."))
story.append(b("<b>Aggressive:</b> $6,000/mo — Starter tier cap; 20% of $6M goal exceeds cap, cap applies."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~3 cases x $5,000 = $15,000/mo revenue vs. $3,200 spend = 4.7x return. (Estimates; not guaranteed.)"))
story.append(b("<b>Aggressive:</b> ~5–6 cases x $5,000 = $27,500/mo revenue vs. $6,000 spend = 4.6x return. (Estimates; not guaranteed.)"))
story.append(Paragraph("<i>Default case value of $5,000 used — not confirmed on call. Results will vary.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Business Law minimums: PPC $1,500 + LSA $1,000 + Meta Retargeting $200 + Meta Lead Gen $500 = $3,200."))
story.append(b("<b>Aggressive:</b> $6M goal x 20% / 12 = $100K. Chicago Tier 2 (1.3x) and Spanish (1.33x) exceed Starter cap of $6,000."))
story.append(b("At $6,000 ad spend + $4,847 fee = $10,847/mo total; at est. $700K revenue ($58K/mo) = 18.7% — under 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"We are already working with multiple agencies."', S["objection_q"]))
story.append(Paragraph("57 leads from one agency produced 1 booking — 1.75% conversion. Gordon Law Group built 200+ reviews with one integrated strategy. Multiple uncoordinated agencies cannot build that compounding advantage.", S["objection_a"]))

story.append(Paragraph('"Marketing has not worked for us before."', S["objection_q"]))
story.append(Paragraph("The 57-to-1 result is a lead quality AND intake problem. SMB Team manages both: rebuilt website, tracked leads, and a follow-up process that gives paid traffic a system to land in — none of which previous agencies provided.", S["objection_a"]))

story.append(Paragraph('"I am not sure about this level of investment."', S["objection_q"]))
story.append(Paragraph("Conservative scenario: 2–3 cases/mo at $5,000 each = $10K–$15K monthly revenue. That covers the fee with a return. Staying the course means paying 3–4 agencies for another quarter of 57-to-1 results.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, SEO, website rebuild, review acquisition, monthly reporting.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$2,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, practice area masterminds, quarterly and annual workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,200–$6,000/mo", S["price_main"])],
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
    "Total SMB fees: $7,047/mo + $3,200–$6,000 ad spend  |  Save $2,147/mo by bundling  |  Est. 18–28% of revenue (under 35% cap)",
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
