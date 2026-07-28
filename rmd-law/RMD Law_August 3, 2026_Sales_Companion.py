"""
Sales Companion PDF — RMD Law
Generated per SMB Team Sales Companion template. Do not modify layout/styles.
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

OUTPUT_PATH = "rmd-law/RMD Law_August 3, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("RMD Law", S["title"]))
story.append(Paragraph("Sales Companion  |  August 3, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Michael Schulz", S["snap_value"]),
     Paragraph("Est. $2M-$3M*", S["snap_value"]),
     Paragraph("6 atty + CMO", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% def.", S["snap_value"]),
     Paragraph("Irvine, CA +8", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.7*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Paragraph("*Re-estimated from $80K/mo ad spend + firm scale — confirm before finalizing.", S["disclaimer"]))
story.append(Spacer(1, 4))

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: SCALE & DOMINATE (inferred)", S["section"]))
story.append(Paragraph("Michael is pushing RMD Law into new states and a new practice area — success means dominating every market the firm enters, not just holding steady in Irvine.", S["subsection"]))
story.append(Paragraph("No verbatim quotes available (Fathom call summary) — DBM inferred, confirm with Michael next call.", S["disclaimer"]))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Regain the case pace.</b> Get back to 50+ signings/month after slipping to 30."))
story.append(bd("<b>Win new markets outright.</b> Dominate Austin, Seattle, Dallas, and Houston the way RMD Law already leads in Irvine."))
story.append(bd("<b>Launch employment law cleanly.</b> Resolve the site-structure decision and get the new practice generating cases."))
story.append(bd("<b>Make the $80K/month prove itself.</b> Know which channels are actually producing signed cases."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Budget concentration risk.</b> $50K of the $80K/month budget rides on one volatile channel (Yelp Ads)."))
story.append(b("<b>Aged LSA account.</b> Underperforming due to poor ranking, in the firm's own words."))
story.append(b("<b>Zero 3-pack visibility in 4 of 5 priority markets.</b> Sacramento, San Diego, San Bernardino, Austin."))
story.append(b("<b>No profit visibility.</b> No revenue or margin figure discussed despite the spend level."))
story.append(b("<b>Decisions still route through Michael.</b> Channel mix and new-practice structure sit with ownership, not a team."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns the existing $80,000/month budget into one coordinated system across all five priority markets instead of one volatile channel."))
story.append(bd("Builds the local SEO and review foundation Austin, Seattle, Dallas, and Houston will need before RMD Law's name means anything there."))
story.append(bd("Gives Michael one accountable team for channel mix, instead of him reallocating budget himself."))

story.append(Paragraph("<b>Full Service Marketing — Dominate  |  $10,497/mo bundled</b>", S["subsection"]))
story.append(b("Revenue re-estimated at $2M-$3M from $80K/mo sustained spend + firm scale — HubSpot's raw $1.98M midpoint undersells it."))
story.append(b("Multiple locations and practice areas already disqualify Essentials regardless of revenue."))
story.append(b("Dominate's $100,000 ad cap comfortably covers the firm's current $80,000/month budget."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Michael a structured way to delegate channel-mix and new-market decisions instead of owning every one personally."))
story.append(bd("Builds the operational leadership layer needed to launch employment law and enter Seattle, Dallas, and Houston without adding to his own workload."))
story.append(bd("Master's Circle connects Michael with peer firm owners navigating the same multi-market scale-up."))

story.append(Paragraph("<b>Master's Circle + FCOO Director  |  $8,394/mo bundled</b>", S["subsection"]))
story.append(b("Team confirmed 5+ with dedicated marketing staff (CMO, Marketing Director) — qualifies for Master's Circle."))
story.append(b("Revenue estimate of $2M-$3M meets the FCOO Director tier's $2M+ threshold."))
story.append(b("Price includes Elite Coach group deliverables (coaching, masterminds, workshops) — no separate charge."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("RMD Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Converts the ad budget from a black box into tracked channels with a known cost per case."))
story.append(bd("Gives Michael a floor (conservative) and a ceiling (aggressive) to plan expansion budget against, both under the firm's 35% total-spend guardrail."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $19,500/mo — minimum viable spend across recommended channels."))
story.append(b("<b>Aggressive:</b> $54,000/mo — capped by the 35% total-spend guardrail, not the tier's $100,000 ad cap."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~5 cases x $6.5K = $32.5K/mo vs. $19.5K spend = 1.7x return."))
story.append(b("<b>Aggressive:</b> ~18 cases x $6.5K = $117K/mo vs. $54K spend = 2.2x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> MVA minimums: PPC $10,000 + LSA $2,000 + Meta Retargeting $1,500 + Meta Lead Gen $6,000 = $19,500."))
story.append(b("<b>Aggressive:</b> 20%-rule and reverse-math both exceeded the tier cap; capped by the firm's 35% total-spend rule instead."))
story.append(b("Total at aggressive: $18,891 fees + $54,000 ads = $72,891/mo = ~35.0% of est. monthly revenue — at the cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We\'re already spending $80K/month — why spend more?"', S["objection_q"]))
story.append(Paragraph("You don't need to — this redirects the existing $80,000/month. $50,000 rides on one volatile channel (Yelp Ads, 5-20 signups/mo) today; Dominate coordinates it across five markets instead.", S["objection_a"]))

story.append(Paragraph('"Our Neil Patel contract doesn\'t end until August — why now?"', S["objection_q"]))
story.append(Paragraph("That's exactly why now matters — RMD Law has zero strategic marketing partner starting September without a transition plan in place first.", S["objection_a"]))

story.append(Paragraph('"We don\'t know our exact revenue — is this the right tier?"', S["objection_q"]))
story.append(Paragraph("HubSpot's $1.98M estimate undersells the firm — $960K/yr in ad spend alone implies revenue well above $2M. Confirm against financials before signing (workings file).", S["objection_a"]))

story.append(Paragraph('"Why add coaching/ops on top of marketing?"', S["objection_q"]))
story.append(Paragraph("Every new market — Austin already, Seattle/Dallas/Houston next — routes through Michael personally today. FCOO Director support is what lets that stop.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Dominate</b>", S["price_main"]),
     Paragraph("$10,497/mo", S["price_main"])],
    [Paragraph("Coordinated SEO, Google Ads, LSA rebuild, and Meta across all 5 markets.", S["price_detail"]),
     Paragraph("<strike>$12,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle + FCOO Director</b>", S["price_main"]),
     Paragraph("$8,394/mo", S["price_main"])],
    [Paragraph("Group coaching + dedicated ops leadership for multi-market delegation.", S["price_detail"]),
     Paragraph("<strike>$10,794</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$19,500-$54,000/mo", S["price_main"])],
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
    "Total: $18,891/mo + $19,500-$54,000 ad spend  |  Save $4,400/mo by bundling  |  18.4%-35.0% of revenue (under 35% cap)",
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
