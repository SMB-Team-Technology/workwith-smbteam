"""
Sales Companion PDF Template — SMB Team
========================================
This template generates the 2-page internal Sales Companion PDF for the sales rep.
It uses reportlab. Do not modify the layout, colors, fonts, styles, or structure.
Only replace the # FILL: placeholders with audit-specific content.

IMPORTANT: The final PDF must be exactly 2 pages. If content overflows to a third
page, shorten bullet text — do not remove sections.

All bullet text must be scannable: one idea per bullet, 8th-grade reading level.
Each "What it does for her/him:" bullet states the transformation, not the deliverable.
Each scoping rationale bullet states one fact with one conclusion.

Output filename: [FirmName]_[Date]_Sales_Companion.pdf
  - FirmName: spaces replaced with underscores
  - Date: MMDDYYYY format
  - Save to the root of the project folder (same location as the Growth Audit HTML)
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

OUTPUT_PATH = "john-stevens-law/JohnStevensLaw_04302026_Sales_Companion.pdf"


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

story.append(Paragraph("John Stevens Law", S["title"]))
story.append(Paragraph("Sales Companion  |  April 30, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("John H. Stevens", S["snap_value"]),
     Paragraph("~$1M/year", S["snap_value"]),
     Paragraph("5 + John", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Jackson, MS", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FINANCIAL FREEDOM", S["section"]))
story.append(Paragraph("John wants to pay off $2M in debt and retire debt-free in 10 years — with a firm that earns income without him.", S["subsection"]))

story.append(quote_block("I want to generate about 10 more cases a month and increase my personal income by around $200,000 a year."))
story.append(Spacer(1, 1))
story.append(quote_block("I have about $2 million in personal and business real estate debt I need to pay down before I can retire."))
story.append(Spacer(1, 1))
story.append(quote_block("I want to get to a point where the firm is on autopilot — where it's working for me instead of me working for it."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Debt paid off on a schedule.</b> A clear monthly plan — not a hope — to eliminate $2M before retirement."))
story.append(bd("<b>10 more cases every month.</b> Consistent, predictable volume not dependent on who refers him next."))
story.append(bd("<b>A firm that runs without him.</b> Step back from daily ops so the firm earns whether he shows up or not."))
story.append(bd("<b>Retire on his terms in 10 years.</b> Walk away from the grind debt-free — or keep going because he chooses to."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Online invisibility.</b> 18 Google reviews vs. 4,077 for the top competitor — he cannot be found by prospects searching online."))
story.append(b("<b>No paid lead generation.</b> Every high-intent search goes to competitors; no ads observed across PI, WC, or SSDI."))
story.append(b("<b>Intake not built to scale.</b> No formal process or after-hours coverage — marketing-generated leads will fall through."))
story.append(b("<b>No financial model.</b> The 10-year retirement goal has no math behind it — no paydown schedule, no cost-per-case tracking."))
story.append(b("<b>Owner-dependent operations.</b> Every new case adds pressure on John; the team cannot absorb growth without structure."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts John in front of 10+ PI and WC prospects per month searching online in Jackson — replacing referral dependency with a reliable pipeline."))
story.append(bd("Builds the review volume and geo-targeting presence that transforms the firm from invisible to discoverable over 12–18 months."))
story.append(bd("Creates the predictable new-case math that makes the $2M debt paydown plan something John can track monthly."))

story.append(Paragraph("<b>Full Service Marketing Growth  |  $5,397/mo bundled</b>", S["subsection"]))
story.append(b("PI practice area requires minimum Growth tier — Essentials is not eligible for personal injury."))
story.append(b("At ~$1M revenue with aggressive 10-year retirement goals, Growth tier provides the channel depth the plan requires."))
story.append(b("Website relaunched in late 2025 but needs content, geo-targeting, and local SEO build — all included in Full Service."))
story.append(b("NAP inconsistency (two phone numbers across directories) suppresses local pack rankings; audit and cleanup is a Growth deliverable."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives John the structure to delegate operations — so growth stops meaning more personal workload and starts meaning more freedom."))
story.append(bd("Creates monthly accountability around cases, revenue, and debt paydown — turning a 10-year hope into a tracked plan."))
story.append(bd("Connects John to a peer group of law firm owners who have already solved the delegation and scaling problems he is facing."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("At $1M revenue with a 5-person team, Elite Coach Plus is the correct tier — built for firms transitioning from owner-driven to team-driven."))
story.append(b("John described feeling overwhelmed by daily ops; coaching provides the accountability framework to change that, not just more revenue."))
story.append(b("No practice manager or ops lead in place — coaching delivers the process guidance to build that accountability layer."))
story.append(b("$500k personal profit confirms capacity to invest; ROI is measured in operational leverage and owner stress reduction, not just new cases."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("John Stevens Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Converts marketing investment into signed cases every month — giving the $2M debt paydown plan real numbers to run on."))
story.append(bd("Puts John in front of high-intent Jackson and Metro suburbs prospects before they call Richard Schwartz or Morgan &amp; Morgan."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,000/mo — minimum viable spend across Google Ads, LSA enrollment, and Meta retargeting."))
story.append(b("<b>Aggressive:</b> $10,000/mo — full channel coverage to reach the 10-case/month target; Growth tier cap is $7,000; Dominate tier ($7,497/mo) unlocks $10K+ spend."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 2–3 cases x $7,500 avg = ~$18,750/mo vs. $5,000 spend = ~3.75x return."))
story.append(b("<b>Aggressive:</b> 7–8 cases x $7,500 avg = ~$56,250/mo vs. $10,000 spend = ~5.6x return."))
story.append(Paragraph("<i>All figures are estimates based on 15% close rate and $7,500 avg case value. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> PI/WC channel minimums: Google Ads $3,000 + LSA $900 + Meta retargeting $1,000 = $4,900."))
story.append(b("<b>Aggressive:</b> $1.2M revenue target x 20% ÷ 12 = $20,000. Tier 4 market (1.0x) = $20,000. Growth cap at $7,000; Dominate tier needed for $10K."))
story.append(b("Total at aggressive: $7,597 fees + $10,000 ad spend = $17,597/mo = 17.6% of revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I already get steady referrals — why do I need to spend on marketing now?"', S["objection_q"]))
story.append(Paragraph("Referrals reflect past relationships — they do not scale to 10 new cases per month. To add $200k/year in personal income and pay down $2M in debt on a 10-year schedule, the firm needs a lead generation system that works independently of who happens to refer next.", S["objection_a"]))

story.append(Paragraph('"I\'m not sure this is the right time with everything going on."', S["objection_q"]))
story.append(Paragraph("The gap is not waiting. Richard Schwartz has 4,077 Google reviews; John has 18. Every month without a review generation campaign widens the gap that drives local pack and LSA rankings. The best time to start was 12 months ago — the second-best time is today.", S["objection_a"]))

story.append(Paragraph('"How do I know this will actually work for PI in Mississippi?"', S["objection_q"]))
story.append(Paragraph("The market is competitive because PI prospects are making decisions online — they search, compare, and call. A targeted paid search and LSA strategy puts John in front of the same prospects currently calling Schwartz first. A local specialist with 35 years of roots in Jackson can out-trust any national firm — he just needs to be visible.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Growth</b>", S["price_main"]),
     Paragraph("$5,397/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, local SEO, content, and website optimization — fully managed.", S["price_detail"]),
     Paragraph("<strike>$5,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, practice area masterminds, quarterly workshops, annual in-person event.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,000–$10,000/mo", S["price_main"])],
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
    "Total: $8,597/mo + $4,900–$10,000 ad spend  |  Save $897/mo by bundling  |  13.5%–18.6% of revenue (under 35% cap)",
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
