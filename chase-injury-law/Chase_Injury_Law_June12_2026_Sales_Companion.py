"""
Sales Companion PDF — Chase Injury Law
SMB Team Internal Document — DO NOT SHARE WITH CLIENT
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

OUTPUT_PATH = "chase-injury-law/Chase_Injury_Law_06122026_Sales_Companion.pdf"


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

story.append(Paragraph("Chase Injury Law", S["title"]))
story.append(Paragraph("Sales Companion  |  June 12, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Michelle Chase, Esq.", S["snap_value"]),
     Paragraph("Pre-revenue ($0–$180K est.)", S["snap_value"]),
     Paragraph("Solo (1)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Portugal (FL market)", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: LOCATION INDEPENDENCE UNDER DEADLINE", S["section"]))
story.append(Paragraph("Michelle relocated to Portugal and has a 12-month runway to replace $400K+ in combined income — this firm must become self-sustaining remotely, or the model fails.", S["subsection"]))

story.append(quote_block("The firm has a 12-month runway after relocating to Portugal. The goal is to replace a combined $400K+ annual income, targeting $1M+ annual profit."))
story.append(Spacer(1, 1))
story.append(quote_block("Become the experts in work comp in Florida."))
story.append(Spacer(1, 1))
story.append(quote_block("Only three cases coming from referrals."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Income from Portugal.</b> Replace $400K+ combined income within 12 months — remotely."))
story.append(bd("<b>A self-running firm.</b> Intake and operations handled without her being physically in Florida."))
story.append(bd("<b>Workers' comp market leadership.</b> Become the recognized Florida expert in work comp."))
story.append(bd("<b>A financial plan.</b> $250K year-one goal with real case targets and cost benchmarks."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>GBP stuck since April 2026.</b> No 3-pack, no LSA, no reviews — all blocked until verification."))
story.append(b("<b>Wrong Google Ads keywords.</b> Health insurance targeting: 200 daily visitors, zero leads."))
story.append(b("<b>Solo, 6-hour time zone gap.</b> No one in Florida for intake or time-sensitive needs."))
story.append(b("<b>No intake system.</b> Leads that miss Michelle go to whichever competitor answers first."))
story.append(b("<b>No financial model.</b> $250K goal with no break-even analysis or monthly case targets."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Rebuilds Google Ads with workers' comp keywords — same budget, right targeting, real leads."))
story.append(bd("Resolves GBP and launches LSA — Chase Injury Law appears above every competitor on Google."))
story.append(bd("Inbound lead flow that works from Portugal — no daily campaign management required."))

story.append(Paragraph("<b>Full Service Marketing — Essentials  |  $3,397/mo bundled</b>", S["subsection"]))
story.append(b("No lead gen infrastructure exists — full service required to build from zero."))
story.append(b("Essentials tier for pre-revenue firm; ad spend cap $7,500/mo."))
story.append(b("Workers' comp primary — no PI filter triggered; Essentials is eligible."))
story.append(b("Scoping: confirm client can cover 4 months ($23,988) before proceeding."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Builds the break-even model that turns $250K goal into tracked monthly case targets."))
story.append(bd("Designs the remote intake system so Florida leads don't fall through the time zone gap."))
story.append(bd("Accountability structure to ensure the 12-month runway produces results before it expires."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled  (saves $897/mo vs. $3,497 stand-alone)</b>", S["subsection"]))
story.append(b("Revenue under $250K: Elite Coach is the correct coaching tier."))
story.append(b("No financial model exists — break-even planning is immediate need #1."))
story.append(b("Remote intake design for Portugal ops is a direct coaching deliverable."))
story.append(b("Scoping: revenue under $250K requires scoping approval before proceeding."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Chase Injury Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Places Chase Injury Law in front of injured Florida workers the moment they search Google."))
story.append(bd("Generates the case volume needed to hit $250K year-one within the 12-month runway."))

story.append(Paragraph("<b>Recommended Range | Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative $3,000/mo:</b> ~6 leads x 15% = 1 case x $25K = $25K/mo est. revenue. ~8x ROAS."))
story.append(b("<b>Aggressive $7,500/mo:</b> ~18 leads x 15% = 3 cases x $25K = $75K/mo est. revenue. ~10x ROAS."))
story.append(Paragraph("<i>Estimates. ACV = FL workers' comp default ($25K). Settlements take 6–18 months. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How calculated:</b>", S["subsection"]))
story.append(b("Conservative: absolute minimum ($3K); LSA $2K + PPC $1K."))
story.append(b("Aggressive: $1M goal x 20%/12 x Tier 2 (1.3x) = $21,667; minus $3,397 fee = $18,270 — capped at $7,500."))
story.append(b("At aggressive: $13,497/mo total = 8.9% of $180K est. revenue. Under 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"My vendor tried Google Ads and it didn\'t work."', S["objection_q"]))
story.append(Paragraph("Keywords were wrong — health insurance, not workers' comp. Masnikoff (workerscompfl.net) runs the exact strategy SMB Team is proposing. Platform works; targeting was the problem.", S["objection_a"]))

story.append(Paragraph('"I\'m not sure I can afford this right now."', S["objection_q"]))
story.append(Paragraph("One workers' comp case ($25K ACV) covers 4+ months of SMB fees. Can the 12-month runway afford to wait? Anidjar &amp; Levine: 1,696 reviews. Masnikoff: running PPC today. Every month without a system widens the gap.", S["objection_a"]))

story.append(Paragraph('"I worry about managing this from Portugal."', S["objection_q"]))
story.append(Paragraph("SMB Team manages all campaigns — Michelle reviews a monthly report. Elite Coach builds the remote intake system. The entire package is engineered for location-independent ownership.", S["objection_a"]))

story.append(Paragraph('"What if GBP verification takes too long?"', S["objection_q"]))
story.append(Paragraph("Google Ads launch immediately while GBP is in process. LSA goes live the moment it resolves. The firm does not have to wait for GBP to start generating leads.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Essentials</b>", S["price_main"]),
     Paragraph("$3,397/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, local SEO, website optimization, monthly reporting.", S["price_detail"]),
     Paragraph("N/A stand-alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly coaching, intake system design, break-even modeling, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand-alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000–$7,500/mo", S["price_main"])],
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
    "Total SMB fees: $5,997/mo + $3,000–$7,500 ad spend  |  Save $897/mo by bundling  |  8.9% of revenue at aggressive (under 35% cap)",
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
