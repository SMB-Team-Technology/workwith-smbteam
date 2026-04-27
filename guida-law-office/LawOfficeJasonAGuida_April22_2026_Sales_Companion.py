"""
Sales Companion PDF — Law Office of Jason A. Guida
Sales Rep: Randy Gold | April 22, 2026
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

OUTPUT_PATH = "guida-law-office/LawOfficeJasonAGuida_04222026_Sales_Companion.pdf"


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

story.append(Paragraph("Law Office of Jason A. Guida", S["title"]))
story.append(Paragraph("Sales Companion  |  April 22, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Jason Guida", S["snap_value"]),
     Paragraph("~$400K (inferred)", S["snap_value"]),
     Paragraph("2 (owner + asst)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Woburn, MA", S["snap_value"])],
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
story.append(Paragraph("Jason wants to stop being the firm and start owning it — fewer hours, chosen cases, eventually something he can sell.", S["subsection"]))

story.append(quote_block("working in the business, not on it"))
story.append(Spacer(1, 2))

story.append(bd("<b>Stop declining USCCA cases.</b> Court conflicts cost thousands each time — he needs an attorney covering appearances."))
story.append(bd("<b>Recover the 52 idle leads.</b> MyCase has had unworked leads since January; a system captures that revenue without him chasing it."))
story.append(bd("<b>Know the numbers before the next hire.</b> He wants strategic financial guidance, not just expense categorization."))
story.append(bd("<b>Build something sellable.</b> Exit value requires documented systems and predictable profit — neither exists today."))

story.append(Spacer(1, 1))

story.append(b("<b>Intake is broken.</b> Assistant ignores scripts, leaves data fields blank, does not follow up — revenue leaks on every lead."))
story.append(b("<b>No accountability structure.</b> No KPIs or scorecards; verbal feedback has not changed behavior."))
story.append(b("<b>No financial visibility.</b> No bookkeeping or projections — hiring decisions are made without data."))
story.append(b("<b>Zero paid marketing.</b> Every client depends on a referral; no Google Ads, LSA, or Meta."))
story.append(b("<b>Owner at capacity.</b> Jason handles all court appearances, blocking intake of additional high-value cases."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package  |  Full Service Starter  |  $4,847/mo", S["section"]))
story.append(bd("Builds Jason's first predictable inbound channel — paid search, LSA, and SEO targeting LTC, firearms, and self-defense intent in Massachusetts."))
story.append(bd("Puts his unique credentials (former FRB Director, USCCA referral attorney, only MA US LawShield attorney) in front of searchers his competitors can't match."))
story.append(bd("Closes the 66-review gap with Peterson (100+) and builds local authority that compounds."))
story.append(b("Criminal Defense + high-competitiveness → Essentials excluded; Starter is minimum eligible tier."))
story.append(b("Website rebuild included: no confirmed above-fold CTA, no geo landing pages, PageSpeed unverified."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package  |  Elite Coach Plus  |  $3,200/mo", S["section"]))
story.append(bd("Fixes intake in parallel with the marketing launch — so paid leads arrive into a working system, not a broken one."))
story.append(bd("Builds the accountability framework that turns verbal corrections into measurable performance standards."))
story.append(bd("Delivers the financial model Jason needs to hire safely — when to do it, what it does to take-home, how long to payback."))
story.append(b("Revenue ~$400K, team under 5 → Elite Coach Plus is correct tier; FCOO/FCFO excluded under $500K."))
story.append(b("MyCase already in place; coaching configures it for proper intake workflows and lead tracking."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Guida Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(bd("Converts high-intent MA LTC, license denial, and self-defense searchers — cases that never find Jason through referrals."))
story.append(bd("Conservative: 2 cases/month from $3,000 spend = $7,000 new monthly revenue (2.3x). Aggressive: 4 cases at $5,000 = $14,000 (2.8x)."))
story.append(b("<b>Conservative $3,000/mo:</b> Google Ads only; meets Criminal Defense (high comp) minimum. Within Starter cap and 35% revenue check (33.1%)."))
story.append(b("<b>Aggressive $5,000/mo:</b> Adds LSA ($1,000) + Meta retargeting ($1,000). Exceeds Starter cap — discuss 10% overage or upgrade."))
story.append(Paragraph("<i>Estimates only. Case value uses practice area default ($3,500); not confirmed on call.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I need to fix intake before I spend on marketing."', S["objection_q"]))
story.append(Paragraph("That is exactly the plan — coaching fixes intake in parallel. The 52 MyCase leads get reactivated in the first 30 days, before a single paid lead arrives.", S["objection_a"]))

story.append(Paragraph('"I cannot afford $8,000 a month right now."', S["objection_q"]))
story.append(Paragraph("The 52 unworked leads represent $50,000+ by Jason's own estimate. A 25% recovery — 13 cases at $3,500 — returns $45,500. That covers more than five months of the full investment without a single new marketing dollar.", S["objection_a"]))

story.append(Paragraph('"My referrals are steady — I do not need paid marketing."', S["objection_q"]))
story.append(Paragraph("Peterson has 100+ reviews, a Saugus landing page, and LTC keyword content — in Jason's own backyard. The window to be first in paid search is open now, but it will not stay that way.", S["objection_a"]))

story.append(Paragraph('"I need to hire an attorney first before I scale."', S["objection_q"]))
story.append(Paragraph("The attorney hire is Phase 2 — funded by Phase 1. Coaching builds the financial model that tells Jason exactly when the revenue threshold is right for that hire.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, local SEO, website CRO, Meta retargeting.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("1-on-1 coaching, intake rebuild, KPIs, hiring roadmap, group access.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000–$5,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $3,000–$5,000 ad spend  |  Save $1,147/mo by bundling  |  33.1%–39.1% of est. revenue (conservative within 35% cap)",
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
