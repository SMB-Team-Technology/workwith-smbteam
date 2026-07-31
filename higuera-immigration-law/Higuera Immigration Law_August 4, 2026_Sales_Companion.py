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

OUTPUT_PATH = "higuera-immigration-law/Higuera Immigration Law_August 4, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Higuera Immigration Law", S["title"]))
story.append(Paragraph("Sales Companion  |  August 4, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Danja Higuera", S["snap_value"]),
     Paragraph("~$100K-$150K/yr", S["snap_value"]),
     Paragraph("Solo + ICs", S["snap_value"]),
     Paragraph("3 - Solo", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Weston, FL", S["snap_value"])],
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
story.append(Paragraph("Danja wants a firm that runs without her so she can work fewer than 30 hours a week and be present for her two young kids.", S["subsection"]))

story.append(quote_block("What do you offer to help me make the jump to a self-managing team?"))
story.append(Spacer(1, 1))
story.append(quote_block("solid but unpredictable"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>A self-managing team.</b> Delegation so the firm stops depending entirely on her."))
story.append(bd("<b>Predictable lead flow.</b> A funded channel to plan hiring around, not a guess."))
story.append(bd("<b>Fewer hours, not just more revenue.</b> Growth means time back, not just top-line."))
story.append(bd("<b>A trustworthy next hire.</b> Already vetting an IC attorney for removal/defense."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No delegated team.</b> Only ICs \"as needed\" — no fixed staff, no org structure."))
story.append(b("<b>Zero paid lead generation.</b> No Google Ads, LSA, or Meta found for either practice area."))
story.append(b("<b>Invisible in local search.</b> Did not surface in any of six search terms tested."))
story.append(b("<b>Explicit budget sensitivity.</b> ~$100-150K revenue; pricing deliberately deferred."))
story.append(b("<b>No CRM or follow-up process.</b> Every intake call runs through her personally."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Lead-Gen Add-On (NOT a Full Marketing Package)", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives her a funded lead channel without a full marketing program she can't yet afford."))
story.append(bd("Creates the case-volume data she needs to plan her next hire with confidence."))
story.append(bd("Puts her above the competitors in her own office building the moment a call comes in."))

story.append(Paragraph("<b>LSA Management Add-On  |  $900/mo bundled</b>", S["subsection"]))
story.append(b("Revenue (~$100-150K/yr) is well under $250K — this is the entry-point combo for this revenue band, NOT the Starter tier from package_decision.json."))
story.append(b("Matches what Dan already discussed: a $500/week LSA starting point, funded through cash flow first."))
story.append(b("Pay-per-lead, not pay-per-click — spend only converts when a real prospect calls."))
story.append(b("Deliberately the smallest paid lead-gen entry point — do not upsell to Starter marketing this call."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives her the org design and delegation sequencing she asked about directly on the call."))
story.append(bd("Builds the KPI/accountability structure that makes hiring her next team member low-risk."))
story.append(bd("Connects every session to the real goal: fewer personal hours, not just more revenue."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue under $250K places this firm in the Elite Coach tier — confirm 4 months of funds before proceeding."))
story.append(b("Includes weekly group coaching, masterminds, quarterly workshops, one annual in-person workshop."))
story.append(b("Coaching-led deal per the transcript, not a marketing-discovery lead — lead with this package."))
story.append(b("Elite Coach Plus and higher tiers are not eligible yet at this revenue level."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Higuera Immigration Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Turns \"referrals are unpredictable\" into a real, trackable number she can plan hiring around."))
story.append(bd("Tests lead-gen at the smallest responsible spend level before asking her to commit to more."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000/mo — the documented absolute minimum for any paid ads program, close to the $500/week starting point already discussed on the call."))
story.append(b("<b>Aggressive:</b> $5,400/mo — 20% of a 2x revenue goal (~$250K/yr), adjusted for the Miami-metro (Tier 2) market."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~6 cases x $4.5K = ~$26K/mo vs. $3.0K spend = ~8.7x return."))
story.append(b("<b>Aggressive:</b> ~13 cases x $4.5K = ~$56K/mo vs. $5.4K spend = ~10.4x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Average case value and close rate are practice-area defaults — not stated on the call.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Immigration LSA-only minimum ($2,000) is below the platform-wide absolute minimum, so the $3,000 floor applies."))
story.append(b("<b>Aggressive:</b> $250K goal x 20% / 12 = $4,167/mo. Miami-metro market (Tier 2, 1.3x) = $5,417/mo, rounded to $5,400."))
story.append(b("35% cap check: the $3,500/mo management fee alone is ~34% of current monthly revenue — within cap. Adding ad spend pushes total above 35% at today's revenue and even at the $250K goal (~43%). Flag the aggressive ad number as a stretch scenario, not a Phase 1 commitment."))

story.append(thin_rule())

# ── If She Pushes Back ──
# FILL: 2-4 objections anticipated from the transcript
# Each: red question (objection_q style) + gray response (objection_a style)
# Responses use specific data from the audit — competitor numbers, transcript quotes, etc.
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"This still feels like a lot for where I am right now."', S["objection_q"]))
story.append(Paragraph("The $3,500/mo management fee is the smallest funded combination SMB Team offers, and it's ~34% of current monthly revenue on its own — the documented entry point for firms under $250K, not the Starter marketing tier.", S["objection_a"]))

story.append(Paragraph('"I don\'t want to commit to full-service marketing yet."', S["objection_q"]))
story.append(Paragraph("This isn't full-service — it's Elite Coach paired with a $900/mo LSA management add-on, the exact combination discussed on the call, with ad spend starting at just $3,000/mo.", S["objection_a"]))

story.append(Paragraph('"How do I know this will actually help me build a team?"', S["objection_q"]))
story.append(Paragraph("The coaching program is built specifically around the org design, KPI, and delegation sequencing she asked about directly on the call — that's the literal starting point of the engagement.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
# FILL: All pricing from the scoping calculation
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, masterminds, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>LSA Management Add-On</b>", S["price_main"]),
     Paragraph("$900/mo", S["price_main"])],
    [Paragraph("Pay-per-lead Local Service Ads management — no stand-alone tier.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000–$5,400/mo", S["price_main"])],
    [Paragraph("Goes to Google/LSA — not to SMB Team.", S["price_detail"]),
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
    "Total: $3,500/mo mgmt + $3,000-$5,400 ad spend  |  Save $897/mo by bundling  |  Mgmt fee alone = ~34% of revenue (under cap); full total exceeds 35% at current revenue",
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
