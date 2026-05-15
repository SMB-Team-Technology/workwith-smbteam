"""
Sales Companion PDF — Conroy Scott LLP
SMB Team | May 15, 2026 | Rep: Jacob Meissner
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

OUTPUT_PATH = "conroy-scott/ConroyScottLLP_05152026_Sales_Companion.pdf"


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

story.append(Paragraph("Conroy Scott LLP", S["title"]))
story.append(Paragraph("Sales Companion  |  May 15, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Adam Castonguay", S["snap_value"]),
     Paragraph("$1.25M CAD", S["snap_value"]),
     Paragraph("13 (5L+8S)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Sudbury, ON", S["snap_value"])],
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
story.append(Paragraph("Adam wants to stop being the firm's single point of failure and build the business that runs without him.", S["subsection"]))

story.append(quote_block("Wills and Estates is at full capacity — we are no longer marketing this practice area."))
story.append(Spacer(1, 1))
story.append(quote_block("We can onboard approximately 200 new corporate general counsel clients quickly."))
story.append(Spacer(1, 1))
story.append(quote_block("Maximum revenue at our current team capacity is approximately $2.5M CAD."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Corporate and Real Estate growth.</b> Both are declared priorities with zero paid digital lead generation today."))
story.append(bd("<b>Intake that works without him.</b> A consultant has been hired — he knows it is broken and is ready to fix it."))
story.append(bd("<b>A firm that runs without him.</b> He wants to step back from operational control, not just hire more people."))
story.append(bd("<b>Predictable revenue to $2.5M.</b> Knows the capacity ceiling; wants a plan to reach it without burning out."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Misaligned ad spend.</b> $30/day generates W&amp;E leads he cannot use; corporate and real estate get nothing."))
story.append(b("<b>Intake not fixed yet.</b> Consultant engaged but process not in place — scaling ads now amplifies the loss."))
story.append(b("<b>No ops layer.</b> Adam makes every operational decision; no accountability structure between him and the team."))
story.append(b("<b>Talent scarcity.</b> Qualified lawyers are hard to find in Sudbury — limits delegation of casework."))
story.append(b("<b>Prior pricing concern.</b> Last SMB Team proposal was $10K USD/month, which equaled his entire profit margin at the time."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the corporate and real estate lead pipeline from zero — so Adam is no longer the source of new business."))
story.append(bd("Replaces the misaligned W&amp;E ad spend with campaigns targeting the firm's actual growth practice areas on Day 1."))
story.append(bd("Website rebuild makes every future ad dollar more efficient — conversion-optimized landing pages for each target area."))

story.append(Paragraph("<b>Full Service Marketing Growth  |  $7,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1.25M CAD → $1M–$3M bracket → Growth tier is the correct fit."))
story.append(b("Website rebuild needed: no practice area landing pages, hidden contact form, no above-fold consultation CTA."))
story.append(b("Growth tier ad spend cap ($50,000/mo) far exceeds the recommended range — room to scale as pipeline grows."))
story.append(b("Full service (not ads-only) required because the website rebuild is essential to campaign performance."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Growth Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the org layer Adam needs to stop making every decision — FCOO Advisor designs the ops structure."))
story.append(bd("Connects Adam with law firm owners at exactly his stage navigating the same owner-dependency challenge."))
story.append(bd("Provides the financial and operational infrastructure to scale confidently to $2.5M and know what he keeps."))

story.append(Paragraph("<b>Master's Circle + FCOO Advisor  |  $6,694/mo bundled</b>", S["subsection"]))
story.append(b("13-person team (5 lawyers + 8 support) with dedicated staff qualifies for Master's Circle."))
story.append(b("Adam handles 50%+ of revenue AND all ops — FCOO Advisor is the correct tool to build the delegation layer."))
story.append(b("Fractional package includes weekly group coaching, practice area masterminds, quarterly workshops, and annual in-person."))
story.append(b("Under $2M revenue → Master's Circle + FCOO Advisor is correct; Director and Partner tiers apply at $2M+."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Conroy Scott LLP — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Generates qualified corporate and real estate leads without Adam personally doing business development."))
story.append(bd("At conservative spend, 13 estimated cases/month — enough to hit real estate transaction target and begin corporate pipeline."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $10,200/mo — Business Law channel minimums; aligned to current team intake capacity."))
story.append(b("<b>Aggressive:</b> $22,000/mo — 35% cap-constrained ceiling; full multi-channel push for both practice areas."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 13 cases x $2,000 avg = $26,000/mo vs. $10,200 spend = 2.5x return (estimated)."))
story.append(b("<b>Aggressive:</b> 33 cases x $2,000 avg = $66,000/mo vs. $22,000 spend = 3.0x return (estimated)."))
story.append(Paragraph("<i>All figures are estimates using default case values. Corporate retainer pricing TBD. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Business Law minimums: PPC $3,500 + LSA $2,000 + Meta Retargeting $1,200 + Meta Lead Gen $3,500 = $10,200."))
story.append(b("<b>Aggressive:</b> $2.5M goal x 20% / 12 = $41,667. Tier 4 (1.0x) = $41,667. 35% cap binds: $36,458 - $14,091 fees = $22,367. Round to $22,000."))
story.append(b("Total at aggressive: $36,091/mo = 34.7% of $104,167 monthly revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"The last time you quoted us it was $10,000 USD a month and that equaled our entire profit margin."', S["objection_q"]))
story.append(Paragraph("The firm is now at $1.25M revenue — materially stronger than the prior conversation. Total bundled investment is $14,091 USD/month (approx. $19,400 CAD), not $10K USD on one product. The bundled savings of $3,700/month means Adam is getting the full-service package at a significant discount. Jacob should walk through the CAD equivalents line by line.", S["objection_a"]))

story.append(Paragraph('"We can\'t handle the intake volume — that was the problem last time."', S["objection_q"]))
story.append(Paragraph("This time, the FCOO Advisor is explicitly in the package to build the intake system before the fire hose opens. First 90 days includes intake process documentation and coordinator training. We do not scale ads before the plumbing is working — that is the whole point of the phased approach.", S["objection_a"]))

story.append(Paragraph('"If we grow leads, who handles the additional work? Lawyers are hard to find in Sudbury."', S["objection_q"]))
story.append(Paragraph("Corporate GC is a retainer model with lower per-matter intensity — 200 new clients does not mean 200 new heavy files. Real estate at 20 transactions/month is achievable at current team size (12-13 already; target is 20). The $2.5M capacity ceiling is the firm's own stated maximum — we are targeting $2M, not beyond it.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Growth</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("Website rebuild + Google Ads + LSA + Meta Ads + Local SEO.", S["price_detail"]),
     Paragraph("<strike>$8,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle + FCOO Advisor</b>", S["price_main"]),
     Paragraph("$6,694/mo", S["price_main"])],
    [Paragraph("Group coaching, masterminds, FCOO ops support, workshops.", S["price_detail"]),
     Paragraph("<strike>$8,794</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$10,200–$22,000/mo", S["price_main"])],
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
    "Total: $14,091/mo + $10,200–$22,000 ad spend  |  Save $3,700/mo by bundling  |  23.3%–34.7% of revenue (under 35% cap)",
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
