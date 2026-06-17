"""
Sales Companion PDF — Farias Firm (David Farias)
SMB Team | Michael Kopp | June 17, 2026
FOR INTERNAL USE ONLY — DO NOT SHARE WITH PROSPECT
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

OUTPUT_PATH = "farias-firm-david-farias/FariasFirm_06172026_Sales_Companion.pdf"


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

story.append(Paragraph("Farias Firm (David Farias)", S["title"]))
story.append(Paragraph("Sales Companion  |  June 17, 2026  |  Rep: Michael Kopp", S["subtitle"]))
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
    [Paragraph("David Farias", S["snap_value"]),
     Paragraph("Est. &lt;$180K (HubSpot; not stated)", S["snap_value"]),
     Paragraph("Solo (1)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("San Antonio, TX", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: BECOME THE LITIGATOR / FIRM THAT RUNS ITSELF", S["section"]))
story.append(Paragraph("David wants a firm built on systems so he can pursue board certification, try cases, and build a Texas-wide reputation — without working 70-hour weeks managing operations.", S["subsection"]))

story.append(quote_block("60-70 hours/week including after-hours client calls"))
story.append(Spacer(1, 1))
story.append(quote_block("Taking cases from pre-litigation firms that lack the capacity for trial"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Board certification.</b> Building toward recognition as a certified PI trial specialist in Texas."))
story.append(bd("<b>Cases he chooses.</b> A pipeline beyond referrals so he can pick work that builds his reputation."))
story.append(bd("<b>Stop the 70-hour weeks.</b> Support staff so litigation gets his attention, not operations."))
story.append(bd("<b>Identity as a litigator.</b> Known as the trial attorney in Texas, not a PI intake shop."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No digital presence.</b> Coming Soon website, no GBP, zero reviews — invisible to non-TTLA prospects."))
story.append(b("<b>Solo with no support.</b> Intake, records, and admin all fall to David personally."))
story.append(b("<b>Settlement-dependent cash flow.</b> Self-funding litigation costs, no reserve if settlements delay."))
story.append(b("<b>No revenue goals.</b> Michael noted targets are a prerequisite for David's goals — none exist yet."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds digital foundation from scratch — website, GBP, ads — so leads arrive beyond referrals."))
story.append(bd("Activates the Spanish-language PI market at CPCs 50-70% below English — David's authentic edge."))
story.append(bd("Fully managed — David stays in court; SMB Team runs all marketing channels."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("PI practice requires minimum Starter — Essentials is excluded for personal injury."))
story.append(b("Coming Soon website needs full rebuild — included in Starter."))
story.append(b("All channels (GBP, LSA, Ads, Meta) start at zero — Starter covers all simultaneously."))
story.append(b("Stand-alone $5,697/mo — saves $850/mo bundled with Elite Coach."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Sets revenue goals and intake process so marketing leads become signed cases, not just clicks."))
story.append(bd("Provides accountability structure to build a firm that grows beyond David's personal hours."))
story.append(bd("PI attorney masterminds accelerate what individual coaching alone cannot."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue &lt;$250K — scoping approval required; confirm before presenting."))
story.append(b("Confirm David can cover 4 months of services ($29,788) before proceeding."))
story.append(b("No revenue target exists — coach builds this in Session 1."))
story.append(b("Stand-alone $3,497/mo — saves $897/mo bundled with Starter."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Farias Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Generates PI cases from paid channels independent of referrals — first paid case from ads validates the model."))
story.append(bd("Spanish-language PI campaign is an untapped channel competitors are not fully capitalizing on; first-mover advantage."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,500/mo — Google PPC $3,000 + LSA $2,000 + Meta $2,500 across PI keywords."))
story.append(b("<b>Aggressive:</b> $25,000/mo — Starter tier cap; full deployment across all channels including Spanish-language."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~6 cases x $8,000 = ~$48,000/mo vs. $7,500 spend = 6.4x estimated return."))
story.append(b("<b>Aggressive:</b> ~23 cases x $8,000 = ~$184,000/mo vs. $25,000 spend = 7.4x estimated return."))
story.append(Paragraph("<i>All figures are estimates based on PI benchmarks. Not guaranteed. Case value default $8K (PI Accident/Injury); close rate 15% default.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> PI minimums — PPC $3,000 + LSA $2,000 + Meta $2,500 = $7,500."))
story.append(b("<b>Aggressive:</b> 20% rule falls below conservative at est. revenue; using Starter tier cap $25,000."))
story.append(b("<b>Scoping flag:</b> Revenue est. &lt;$180K — 35% cap exceeded. Confirm revenue before presenting."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I\'m self-funding litigation costs — not sure I can afford this."', S["objection_q"]))
story.append(Paragraph("Conservative ROI: 6 cases x $8K = $48K/mo vs. $7,500 ad spend = 6.4x return. The spend pays back with one additional case.", S["objection_a"]))

story.append(Paragraph('"I get TTLA referrals — I don\'t need paid marketing yet."', S["objection_q"]))
story.append(Paragraph("Carabin & Shaw adds 15-20 reviews per month. The gap grows every week without a GBP. TTLA is a ceiling — digital assets compound over time.", S["objection_a"]))

story.append(Paragraph('"I\'m working 70 hours a week — no time to manage marketing."', S["objection_q"]))
story.append(Paragraph("SMB Team manages everything. David reviews monthly reports and attends coaching. The 70-hour weeks are the problem this solves, not a reason to wait.", S["objection_a"]))

story.append(Paragraph('"I\'ll wait until my website launches first."', S["objection_q"]))
story.append(Paragraph("Site has been Coming Soon since March 2026. Avvo still shows former employer (Sandoval & James). SMB Team's build is the fastest path to a live, optimized site.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website build, Google Ads (EN + ES), LSA, GBP, Meta, SEO, citations.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, PI masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,500–$25,000/mo", S["price_main"])],
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
    "Total: $7,447/mo + $7,500–$25,000 ad spend  |  Save $1,747/mo by bundling  |  SCOPING APPROVAL REQUIRED — confirm revenue before presenting",
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
