"""
Sales Companion PDF — Borinsky Law
Sales Rep: Dan Bryant  |  April 30, 2026
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

OUTPUT_PATH = "borinsky-law/BorinskyLaw_04302026_Sales_Companion.pdf"


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

story.append(Paragraph("Borinsky Law", S["title"]))
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
    [Paragraph("David Borinsky", S["snap_value"]),
     Paragraph("~$180K/yr ($15K/mo)", S["snap_value"]),
     Paragraph("2 (solo + admin)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("West Palm Beach, FL", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FINANCIAL STABILITY", S["section"]))
story.append(Paragraph(
    "David wants consistent, predictable income so he can stop worrying about money and practice the sophisticated law he loves.",
    S["subsection"]))

story.append(quote_block("Stop worrying about money."))
story.append(Spacer(1, 1))
story.append(quote_block("Three unfocused years."))
story.append(Spacer(1, 1))
story.append(quote_block("Income volatility."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable income.</b> Replace lumpy case flow with a steady pipeline he can plan around and use to pay down debt."))
story.append(bd("<b>Practice law, not chase leads.</b> Spend his days on sophisticated cross-border work, not business development."))
story.append(bd("<b>Market recognition.</b> Become the go-to international tax attorney for UHNW clients in West Palm Beach and Miami."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Zero digital presence.</b> No website, no GBP, no directory listings — invisible to every prospect searching online."))
story.append(b("<b>No intake system.</b> David handles every inquiry personally with no protocol, no follow-up, no delegation."))
story.append(b("<b>No paid lead generation.</b> Frost Law and TaxLawExpats collect every digital lead in his market."))
story.append(b("<b>Lumpy revenue + prior debt.</b> $180K/year but unpredictable; low six-figure liability adds urgency."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts David's Big Law credentials in front of UHNW prospects who are actively searching and ready to hire."))
story.append(bd("Builds the website, GBP, and Google Ads infrastructure that converts referrals and generates new leads consistently."))

story.append(Paragraph("<b>Full Service Marketing Essentials  |  $3,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$180K/year from zero digital presence — Essentials is the correct entry tier."))
story.append(b("No website exists — full-service package required; ads-only sub-package is ineligible without a landing page."))
story.append(b("West Palm Beach is Tier 4; Essentials $1,500 ad spend cap fits the initial budget constraint."))
story.append(b("<b>FLAG:</b> Revenue under $300K — scoping approval required before close. Confirm 4 months of fees available."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the intake protocol that converts paid leads into cases without David handling every call personally."))
story.append(bd("Provides external accountability for the business operations David finds uninteresting — so they get done, not deferred."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("David described limited interest in business ops — external accountability is essential, not optional."))
story.append(b("Admin/paralegal has no defined scope — coaching builds the intake framework before ads launch."))
story.append(b("Revenue goal of $500K (2.8x current) requires systematic execution, not just more ad spend."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Borinsky Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts Borinsky Law in front of international tax prospects in West Palm Beach and Miami at the exact moment they are ready to hire."))
story.append(bd("Converts David's rare expertise into a measurable lead pipeline so income growth is driven by a system, not by referral timing."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $1,500/mo — Business Law Google PPC minimum; no LSA (GBP required first), no Meta in initial phase."))
story.append(b("<b>Aggressive:</b> $1,500/mo — mgmt fees ($5,997) absorb client's $7K budget; use PPC floor. Confirm budget before close."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~1 case x $25,000 = $25,000/mo vs. $1,500 spend = ~16.7x return."))
story.append(b("<b>Aggressive:</b> ~1 case x $25,000 = $25,000/mo vs. $1,500 spend = ~16.7x return."))
story.append(Paragraph("<i>All figures are estimates based on $25,000 avg case value (stated) and 15% default close rate. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Business Law PPC minimum $1,500. LSA ineligible (no GBP yet). Meta deferred to Phase 2."))
story.append(b("<b>Aggressive:</b> $7K all-in minus $5,997 fees = $1,003 — below floor; use $1,500 minimum. Budget discussion required."))
story.append(b("<b>Cap note:</b> Mgmt fees ($5,997) alone = 40% of $15K/mo revenue. Above 35% cap — scoping approval required."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"Can Google Ads reach UHNW and international tax clients? That seems too niche."', S["objection_q"]))
story.append(Paragraph(
    "These are the highest-intent searchers online — a prospect searching 'expatriation attorney West Palm Beach' has a live tax problem and is ready to hire. "
    "Frost Law is already running multi-domain Google Ads on David's exact keywords. One conversion at $25K covers over a year of ad spend.",
    S["objection_a"]))

story.append(Paragraph('"This is a lot of money given my current income and debt."', S["objection_q"]))
story.append(Paragraph(
    "The debt is exactly why delay is expensive. One additional case/month at $25K covers the entire SMB investment. "
    "Without a lead system, income stays lumpy forever. Scoping approval process: confirm 4 months of fees available before close.",
    S["objection_a"]))

story.append(Paragraph('"What if ads work and I get more calls than I can handle?"', S["objection_q"]))
story.append(Paragraph(
    "The coaching engagement addresses this first — intake protocol and admin role scope are built before ads launch. "
    "The admin handles initial calls, not David. Phase 2 of the roadmap adds ops support when volume grows.",
    S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Essentials</b>", S["price_main"]),
     Paragraph("$3,397/mo", S["price_main"])],
    [Paragraph("Website build, GBP setup, Google Ads management, local SEO, reporting.", S["price_detail"]),
     Paragraph("N/A stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, practice area masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$1,500/mo (floor)", S["price_main"])],
    [Paragraph("Goes to Google and LSA — not to SMB Team.", S["price_detail"]),
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
    "Total mgmt fees: $5,997/mo + $1,500 ad spend  |  Save $897/mo by bundling  |  "
    "Mgmt fees = 40% of revenue — SCOPING APPROVAL REQUIRED before close",
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
