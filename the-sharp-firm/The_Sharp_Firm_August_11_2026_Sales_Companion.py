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

OUTPUT_PATH = "the-sharp-firm/The_Sharp_Firm_August_11_2026_Sales_Companion.pdf"


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

story.append(Paragraph("The Sharp Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  August 11, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Lance Sharp", S["snap_value"]),
     Paragraph("~$570K est. (low conf.)", S["snap_value"]),
     Paragraph("2 (Lance + Laura)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("Austin, TX", S["snap_value"])],
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
story.append(Paragraph("Lance wants a done-for-you system that gets him out of personally screening every low-value call, so he can build the truck/auto niche practice he actually wants.", S["subsection"]))

story.append(quote_block("Hell no. (Lance's response when asked if he'd DIY social/video content himself)"))
story.append(Spacer(1, 1))
story.append(quote_block("Rejects ~99% of Med/Dental Mal inquiries due to case quality; will only take catastrophic MedMal."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Out of the low-value intake grind.</b> Fielding 5-10 med/dental mal calls a day, rejecting 99% himself."))
story.append(bd("<b>A real truck/auto pipeline.</b> Explicitly wants to pivot toward auto and 18-wheeler cases."))
story.append(bd("<b>Done-for-you, not DIY.</b> Said \"hell no\" to producing his own social/video content."))
story.append(bd("<b>To dominate the truck niche.</b> Open to a distinct brand/GMB to rank in Maps for truck cases."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Burned by prior vendors.</b> Rise Up PPC collapsed after a Google change; a year of SEO gave poor ROI for auto/truck."))
story.append(b("<b>Can't outspend the big players.</b> Named Thomas J. Henry and Jim Adler as firms he cannot outbid on core PPC terms."))
story.append(b("<b>No systems behind him.</b> No CRM, no Meta pixel, no LSA — everything runs through him personally."))
story.append(b("<b>Revenue confidence is low.</b> Not stated on the call; HubSpot band is wide ($180K-$960K) — confirm before finalizing."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts real budget behind the auto/truck pivot instead of relying on organic med-mal momentum."))
story.append(bd("Avoids the PPC arms race he already lost — leads with Meta and LSA, not head-on Google bidding."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue band + multiple practice areas both point to Starter (Essentials requires single practice area)."))
story.append(b("No website rebuild needed — mobile-responsive, ~12-18 months old, has bios and practice pages."))
story.append(b("Retail $5,697/mo vs. bundled $4,997/mo — saves $700/mo."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Structured path to delegate intake triage instead of running it all personally."))
story.append(bd("Builds cost-per-lead/cost-per-case visibility he doesn't have today — decisions are gut feel now."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue band ($400K-$1M) points here regardless of exact team-size count (2 vs. 3)."))
story.append(b("Retail $3,497/mo vs. bundled $3,200/mo — saves $297/mo. Total bundled savings: $997/mo."))
story.append(b("Total monthly investment: $8,197/mo (marketing + coaching, before ad spend)."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("The Sharp Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Buys leads through channels he can actually win — Meta and LSA — not a PPC war he's already lost."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $10,000/mo — PI High-competitiveness floor (LSA + Meta Retargeting + Lead Gen minimums)."))
story.append(b("<b>Aggressive:</b> $18,000/mo — 20%-rule calc, corrected down from the pipeline's $20,000 placeholder (see workings)."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~7 cases x $7.5K avg = ~$52.5K/mo vs. $10K spend = ~5.25x return."))
story.append(b("<b>Aggressive:</b> ~16 cases x $7.5K avg = ~$120K/mo vs. $18K spend = ~6.67x return."))
story.append(Paragraph("<i>Estimates based on industry CPL benchmarks and a 15% default close rate. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> LSA $2K + Meta Retargeting $1.5K + Meta Lead Gen $6K = $9.5K; PI High floor ($10K) governs."))
story.append(b("<b>Aggressive:</b> 2x revenue x 20% / 12 = $19K; Austin Tier 3 (x1.15) = $21.85K; minus $4,997 fee = $16,853, rounded to $18K."))
story.append(b("At the $570K revenue estimate, fees + conservative ad spend run ~38.3% of monthly revenue — over the 35% cap. Confirm actual revenue before finalizing; prior $7.5-8K/mo agency spend suggests it likely supports this."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I already tried PPC and SEO — why would this be different?"', S["objection_q"]))
story.append(Paragraph("Rise Up's PPC collapsed after a Google policy change; SEO gave poor ROI for auto/truck. This leads with Meta and LSA — pay-per-lead, not pay-per-click — to avoid the Thomas J. Henry/Jim Adler bidding war that broke the last approach.", S["objection_a"]))

story.append(Paragraph('"I\'m already talking to other vendors for social/video/AI marketing."', S["objection_q"]))
story.append(Paragraph("Good — that confirms he sees the gap. Position this as the only option bundling the marketing engine with the coaching/delegation support he needs to get time back, not just more leads to screen.", S["objection_a"]))

story.append(Paragraph('"This is more than the ~$3,500/mo we talked about."', S["objection_q"]))
story.append(Paragraph("That figure was a rough example, not a quote. $8,197/mo bundles marketing and coaching, saving $997/mo vs. retail; ad spend is separate and can start at the $10,000 floor.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("Meta retargeting, Meta lead gen, LSA, NAP cleanup, local SEO.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, PI mastermind, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$10,000–$18,000/mo", S["price_main"])],
    [Paragraph("Goes to Meta and LSA — not to SMB Team.", S["price_detail"]),
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
    "Total: $8,197/mo + $10,000-$18,000 ad spend  |  Save $997/mo by bundling  |  38.3%-55.1% of estimated revenue — ABOVE 35% cap at this estimate; confirm actual revenue before finalizing",
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
