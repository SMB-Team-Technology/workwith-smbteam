"""
Sales Companion PDF — The Law Offices of Justin R. Payne, PA
SMB Team | Dan Bryant | April 28, 2026
FOR INTERNAL USE ONLY — DO NOT SHARE WITH CLIENT
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

OUTPUT_PATH = "justin-payne-law/JustinPayneLaw_April282026_Sales_Companion.pdf"


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

story.append(Paragraph("The Law Offices of Justin R. Payne, PA", S["title"]))
story.append(Paragraph("Sales Companion  |  April 28, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Justin R. Payne", S["snap_value"]),
     Paragraph("~$350K/yr", S["snap_value"]),
     Paragraph("1 atty + 1 asst", S["snap_value"]),
     Paragraph("3 — Solo", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Cocoa, FL", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM + EXIT", S["section"]))
story.append(Paragraph("Justin wants to step into a supervisory wizard role, build a sellable firm, and reclaim his personal time.", S["subsection"]))

story.append(quote_block("Build it up and eventually sell; retirement goal, timeline several years."))
story.append(Spacer(1, 1))
story.append(quote_block("What would success look like in 12 months? More automation; supervisory role; win more cases — emulate 'wizard' model."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Supervisory role.</b> Staff prepares files; he argues cases — no more daily admin."))
story.append(bd("<b>Scalable case flow.</b> Predictable leads from digital channels, not just referrals."))
story.append(bd("<b>A sellable firm.</b> Documented systems and financials that have real market value."))
story.append(bd("<b>Personal freedom.</b> Time that is his — not consumed by non-legal tasks."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No digital presence.</b> Referral-only firm, no ads, no GBP reviews, outdated website."))
story.append(b("<b>Admin bottleneck.</b> Spends 10-20 hrs/week on non-legal tasks with no delegation system."))
story.append(b("<b>Undecided pivot.</b> Probate vs. criminal defense choice is delaying hiring and marketing decisions."))
story.append(b("<b>No financial visibility.</b> Revenue known; margins, cost-per-case, and acquisition cost are not tracked."))
story.append(b("<b>Intake gaps.</b> Phone-only, business-hours-only — no after-hours capture, no follow-up process."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Generates a steady flow of real estate and civil litigation cases without Justin personally generating each one."))
story.append(bd("Fixes the credibility gap — rebuilt website, corrected headline, contact form, and GBP reviews in place."))
story.append(bd("Creates the measurable case pipeline that makes hiring the next team member financially safe."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $3,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$350K with aggressive 2x goal — boundary rule justifies Starter tier over Essentials."))
story.append(b("Website rebuild needed: outdated design, misspelled headline, no contact form, likely below PageSpeed benchmarks."))
story.append(b("No named local competitor dominates paid search — first-mover advantage is available now."))
story.append(b("LSA Google Screened: clean Florida Bar record (admitted 2003, no discipline) — qualifies immediately."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the intake system that converts more cases without Justin answering every call himself."))
story.append(bd("Defines the assistant role fully so the admin hours get off Justin's plate within 30 days."))
story.append(bd("Provides a framework to evaluate the practice pivot — numbers-first, not gut-first."))

story.append(Paragraph("<b>Elite Coach  |  $1,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $250K-$400K — Elite Coach is the appropriate tier; revenue upgrade path clear at $50K+/mo."))
story.append(b("Intake is RED: no process, no after-hours coverage, no follow-up cadence — immediate coaching priority."))
story.append(b("Assistant is undefined — role documentation is the first 30-day deliverable that frees admin hours."))
story.append(b("Pivot decision (probate vs. criminal) needs financial modeling; coaching provides the evaluation framework."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Justin Payne — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Creates a case pipeline independent of referrals — the foundation for hiring, delegation, and eventual exit."))
story.append(bd("Positions Justin as the visible local option for Brevard County civil litigation before competitors claim those spots."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $2,400/mo — Google PPC $1,500 + LSA $900. First-mover positioning established."))
story.append(b("<b>Aggressive:</b> $4,500/mo — expanded PPC + LSA + Meta retargeting. Total SMB spend = 34.1% of revenue (under 35% cap)."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~2-3 cases x $8,500 = ~$21K-$25K/mo vs. $2,400 spend = ~8-10x return (est.)."))
story.append(b("<b>Aggressive:</b> ~5-6 cases x $8,500 = ~$42K-$51K/mo vs. $4,500 spend = ~9-11x return (est.)."))
story.append(Paragraph("<i>All figures are estimates. Average case value is a default (not stated by prospect). Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Business/civil litigation minimums: PPC $1,500 + LSA $900 = $2,400."))
story.append(b("<b>Aggressive:</b> $700K goal x 20% / 12 = $11,667. Tier 4 (1.0x) = $11,667. Minus $3,847 fee = $7,820 > cap; capped at $4,500 to stay under 35% revenue limit."))
story.append(b("Total at aggressive: $5,447 fees + $4,500 ads = $9,947/mo = 34.1% of monthly revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I get most of my business from referrals — why do I need ads?"', S["objection_q"]))
story.append(Paragraph("Referrals are great but they are not scalable or predictable. He cannot hire a paralegal, expand into probate, or plan a future sale on referral income that fluctuates. Goldman Monaghan — in his own building — has a multi-attorney team because they did not wait for referrals to fund growth.", S["objection_a"]))

story.append(Paragraph('"I am still deciding between probate and criminal defense — should I wait?"', S["objection_q"]))
story.append(Paragraph("Waiting delays the one thing he said he wants most: the supervisory wizard practice. Marketing for real estate and civil litigation can launch now regardless of the pivot. The ads test demand; the coaching helps him make the pivot decision with financial data. Every month of inaction is a month Goldman Monaghan and Brink Law extend their head start.", S["objection_a"]))

story.append(Paragraph('"$5,447 a month is a big number for where I am right now."', S["objection_q"]))
story.append(Paragraph("Conservative scenario projects 2-3 additional cases per month at ~$8,500 each — that is $17K-$25K in monthly revenue from ads alone. The management fees are $5,447. Even at conservative estimates, the math is strongly positive. And he is already losing cases every month to after-hours calls he never answers.", S["objection_a"]))

story.append(Paragraph('"My website has been fine — I am not sure I need to rebuild it."', S["objection_q"]))
story.append(Paragraph("The homepage headline misspells 'Commitment.' Title companies and commercial clients evaluating a litigator who cannot catch a spelling error on his own website may reconsider. The site also has no contact form, no mobile-optimized design confirmed, and a second domain (jrpaynelaw.com) pointing nowhere. It is not fine — it is costing him cases.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$3,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, Google PPC, LSA, local SEO, review generation, monthly reporting.", S["price_detail"]),
     Paragraph("<strike>$4,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$1,600/mo", S["price_main"])],
    [Paragraph("Bi-weekly coaching, intake design, team structure, KPI tracking, pivot evaluation.", S["price_detail"]),
     Paragraph("<strike>$2,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$2,400–$4,500/mo", S["price_main"])],
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
    "Total: $5,447/mo + $2,400–$4,500 ad spend  |  Save $1,747/mo by bundling  |  26.8%–34.1% of revenue (under 35% cap)",
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
