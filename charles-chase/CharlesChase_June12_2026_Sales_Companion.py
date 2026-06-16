"""
Sales Companion PDF — Charles Chase
SMB Team — Internal Use Only
Date: June 12, 2026
Rep: Randy Gold
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

OUTPUT_PATH = "charles-chase/CharlesChase_June12_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Charles Chase — Workers' Compensation Law", S["title"]))
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
    [Paragraph("Charles Chase", S["snap_value"]),
     Paragraph("~$0 current; $250K/yr goal", S["snap_value"]),
     Paragraph("Solo (1)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Fort Lauderdale, FL", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM / LIFESTYLE", S["section"]))
story.append(Paragraph("Build a firm generating $1M+ annual profit that runs without the owner's presence — funding a life in Portugal.", S["subsection"]))

story.append(quote_block("Relocating to Portugal — need firm to generate income without requiring my physical presence."))
story.append(Spacer(1, 1))
story.append(quote_block("12-month goal: $250,000 in revenue. Long-term: $1M+ annual profit."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Replace $400K+ combined income.</b> Firm revenue must fund the Portugal life without any other income source."))
story.append(bd("<b>A firm that runs without him.</b> Systems and staff handling cases and intake whether he is in Florida or overseas."))
story.append(bd("<b>$1M+ annual profit.</b> Long-term goal; not a lifestyle practice but a growth trajectory."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No digital infrastructure.</b> No owned website, no GBP, no directories — invisible in every channel."))
story.append(b("<b>Wasted ad spend.</b> Vendor targeted health insurance keywords — 200 visitors/day, zero case leads."))
story.append(b("<b>No intake system.</b> Zero inbound digital leads ever; no process ready when ads launch."))
story.append(b("<b>12-month runway.</b> Every month without a working system is runway burned without progress."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds a firm-owned website with workers' comp landing pages — an owned digital asset no vendor can take away."))
story.append(bd("Generates the first inbound case leads from Google Ads, breaking total dependence on referrals."))
story.append(bd("Resolves GBP and builds local SEO — unlocking local search, LSA, and review collection simultaneously."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("No owned website, no GBP — Full Service builds complete digital infrastructure from scratch."))
story.append(b("Workers' comp min ad spend (~$3,000–$4,000) exceeds Essentials cap ($1,500); Starter required per boundary rule."))
story.append(b("Fort Lauderdale Tier 2 market; competitors have 27–32 years of digital equity — Starter is the minimum competitive tier."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Provides weekly accountability toward the $250K goal — not just marketing, but strategic review of whether the firm is on track."))
story.append(bd("Connects with workers' comp attorneys in the SMB network who have already built past this stage."))
story.append(bd("Builds intake, hiring, and financial decision frameworks a solo startup needs — before expensive mistakes happen."))

story.append(Paragraph("<b>Elite Coach  |  $1,600/mo bundled</b>", S["subsection"]))
story.append(b("$250K revenue goal places firm in the $250K–$400K band — Elite Coach is the correct eligibility tier."))
story.append(b("Solo, no prior firm ownership — weekly coaching catches blind spots early."))
story.append(b("Includes weekly group coaching, practice area masterminds, quarterly virtual workshops, one annual in-person event."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Charles Chase — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Converts ad budget from health insurance keyword waste to injured workers with attorney-hire intent — fundamentally different audience."))
story.append(bd("Conservative $3,000/mo generates est. 3 cases/$7,500 revenue — 2.5x return from month one."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000/mo — Google Ads $2,000 + LSA $1,000; minimum viable for workers' comp in Fort Lauderdale."))
story.append(b("<b>Aggressive:</b> $10,000/mo — Google + LSA + Meta retargeting + Spanish campaign; Starter tier cap."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 22 leads x 15% close = 3 cases x $2,500 = $7,500 vs. $3,000 spend = 2.5x. (CPL $135 +20% cushion.)"))
story.append(b("<b>Aggressive:</b> 106 leads x 15% close = 15 cases x $2,500 = $37,500 vs. $10,000 = 3.75x. (Blended CPL $94.)"))
story.append(Paragraph("<i>Estimates only. Not guaranteed. Case value uses FL workers' comp fee default ($2,500 avg) — not stated in transcript.</i>", S["disclaimer"]))

story.append(Paragraph("<b>Calculation basis:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Accident/Injury General minimums: Google PPC $2,000 + LSA $1,000 = $3,000."))
story.append(b("<b>Aggressive:</b> $500K target x 20%/12 = $8,333. Tier 2 (1.3x) = $10,833. Spanish (1.33x) = $14,408. Cap at Starter $10,000."))
story.append(b("35% cap concern: $16,447 total vs. $20,833/mo goal = 79%. Discuss actual revenue trajectory with prospect."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I already spent money on ads and got zero results."', S["objection_q"]))
story.append(Paragraph("The vendor targeted health insurance keywords — people asking about coverage, not injured workers. That is a targeting failure, not a channel failure. SMB campaigns target 'workers comp attorney Fort Lauderdale' and high-intent terms. Completely different audience.", S["objection_a"]))

story.append(Paragraph('"The investment feels high for a startup."', S["objection_q"]))
story.append(Paragraph("Conservative: 3 cases/mo x $2,500 = $7,500 revenue vs. $3,000 ad spend = 2.5x. Plus referrals continue. The infrastructure is what makes the $250K goal achievable — waiting means more runway spent on referrals only.", S["objection_a"]))

story.append(Paragraph('"Can we start with just marketing and skip coaching?"', S["objection_q"]))
story.append(Paragraph("Bundle saves $2,747/mo vs. stand-alone. Coaching provides intake scripting, goal accountability, and weekly review — the difference between leads that sign and leads that go unanswered.", S["objection_a"]))

story.append(Paragraph('"I am worried about the 12-month runway."', S["objection_q"]))
story.append(Paragraph("The runway is exactly why starting now matters. At 3 cases/mo conservative, the firm generates $7,500/mo in new ad revenue by month 2. Waiting 3 months means 3 more months of referral-only dependence.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("New website, Google Ads (workers' comp keywords), GBP setup, local SEO, monthly reporting.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$1,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, practice area masterminds, quarterly virtual workshops, annual in-person event.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000–$10,000/mo", S["price_main"])],
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
    "Total: $6,447/mo + $3,000–$10,000 ad spend  |  Save $2,747/mo by bundling  |  35% cap concern noted — discuss revenue trajectory with prospect",
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
