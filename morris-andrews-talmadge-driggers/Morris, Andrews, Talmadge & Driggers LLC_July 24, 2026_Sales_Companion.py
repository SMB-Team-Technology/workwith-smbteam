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

OUTPUT_PATH = "morris-andrews-talmadge-driggers/Morris, Andrews, Talmadge & Driggers LLC_July 24, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Morris, Andrews, Talmadge &amp; Driggers LLC", S["title"]))
story.append(Paragraph("Sales Companion  |  July 24, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("4 Partners (Joey Morris, contact)", S["snap_value"]),
     Paragraph("$4-6M/yr", S["snap_value"]),
     Paragraph("5 att. + 6.5 staff", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Dothan &amp; Mobile, AL", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.35*inch, 0.95*inch, 1.0*inch, 0.6*inch, 0.9*inch, 1.05*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 4))

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: SCALE &amp; DOMINATE", S["section"]))
story.append(Paragraph("The four partners want hard, call-tracked proof that a strategic growth investment can take them from $4-6M to $10M+ — without adding to what they already manage personally.", S["subsection"]))

story.append(quote_block("80% referral-based (former clients, other attorneys)"))
story.append(Spacer(1, 1))
story.append(quote_block("A fixed 35% of revenue is allocated to overhead, with the rest paid to attorneys"))
story.append(Spacer(1, 1))
story.append(quote_block("leaves little capital for growth investments"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What they want:</b>", S["subsection"]))
story.append(bd("<b>Scale to $10M+.</b> An extra $2M/year to prove the growth investment works to the other partners."))
story.append(bd("<b>Dominate the Black Belt market.</b> Become the top regional PI brand south of the Montgomery-Selma line, not just the oldest one."))
story.append(bd("<b>A dedicated operator, not a program.</b> Someone to build systems and hire an intake team without requiring partner time."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping them:</b>", S["subsection"]))
story.append(b("<b>Zero tracked marketing.</b> 80% referral-dependent, no digital lead gen system ever built."))
story.append(b("<b>Vacant intake role.</b> Paralegals absorb intake, delaying filed lawsuits and demands."))
story.append(b("<b>No unified operator.</b> Four partners run four practices with no one owning systems."))
story.append(b("<b>Fixed 35% overhead.</b> Growth investment competes with partner take-home pay."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Gives partners call-tracked, attributable proof of exactly which dollar generated which case."))
story.append(bd("Builds Black Belt visibility from near-zero to dominant, matching the scale of the $10M+ goal."))
story.append(bd("Fixes the broken mcatlaw.com domain and unverified Dothan GBP — both losing leads today."))

story.append(Paragraph("<b>Full Service Marketing — Platinum  |  $15,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue is $4-6M — the $3M+ Platinum band, with the only tier cap ($150K/mo) large enough for a $10M+ goal."))
story.append(b("Two offices and a broken primary domain require full-service scope, not an ads-only sub-package."))
story.append(b("Bundled $15,997/mo vs. $18,997/mo stand-alone — saves $3,000/mo."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Delivers exactly what partners asked for: a dedicated operator, not a coaching program requiring their time."))
story.append(bd("Ends the paralegal intake bottleneck by building a real, dedicated intake team."))
story.append(bd("Gives the \"four chiefs\" one point of operational accountability instead of four practices improvising separately."))

story.append(Paragraph("<b>FCOO Advisor  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Master's Circle is disqualified: no dedicated ops or intake staff exists (intake role is vacant)."))
story.append(b("Partners said group coaching is not preferred since they are unlikely to attend — FCOO fits their stated preference."))
story.append(b("Bundled $3,297/mo vs. $3,797/mo stand-alone — saves $500/mo. Includes group coaching deliverables."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("MCAT — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Gives partners a trackable cost-per-case read across Google and Meta — the data point they need to justify scaling further."))
story.append(bd("Converts 25 years of untapped brand trust into paid-channel volume for the first time."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $17,500/mo — MVA channel minimums across Google + Meta."))
story.append(b("<b>Aggressive:</b> $125,000/mo — capped by the 35%-of-revenue rule, not the Platinum tier's own $150K cap."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~5 cases x $7.5K = $37.5K/mo vs. $17.5K spend = 2.1x return."))
story.append(b("<b>Aggressive:</b> ~40 cases x $7.5K = $300K/mo vs. $125K spend = 2.4x return."))
story.append(Paragraph("<i>All figures are estimates using a 15% close rate and $7,500 avg case value default. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> MVA minimums: Google PPC $10,000 + Meta Retargeting $1,500 + Meta Lead Gen $6,000 = $17,500."))
story.append(b("<b>Aggressive:</b> $10M goal x 20% / 12 = $166,667. 35%-of-revenue cap (minus mgmt fees) is the binding limit at $125,000."))
story.append(b("Total spend at aggressive: $144,294/mo = 34.6% of revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If They Push Back ──
story.append(Paragraph("If They Push Back", S["section"]))

story.append(Paragraph('"We\'ve grown to $4-6M on referrals alone — why spend on ads now?"', S["objection_q"]))
story.append(Paragraph("Referrals got MCAT to $4-6M, but the firm's own goal is $10M+ — referrals alone add no lever for the extra $2M/year. Stokes Stemle (119 reviews, 4.9 stars) and The Cochran Firm are actively capturing the digital-search clients referrals never reach.", S["objection_a"]))

story.append(Paragraph('"We tried LSAs before and it didn\'t work."', S["objection_q"]))
story.append(Paragraph("The prior LSA campaign was never tracked — there is no data on what worked. This plan is built around call tracking on every lead, so partners finally get the attribution that was missing the first time.", S["objection_a"]))

story.append(Paragraph('"We don\'t want another coaching program — no partner has time to attend group sessions."', S["objection_q"]))
story.append(Paragraph("That is exactly why Master's Circle was not recommended. FCOO Advisor puts a dedicated operator on the ground building systems and hiring the intake team — no partner attendance required.", S["objection_a"]))

story.append(Paragraph('"$19,294/month plus ad spend is a lot for a firm that keeps overhead at 35%."', S["objection_q"]))
story.append(Paragraph("At the aggressive level, total spend is 34.6% of monthly revenue — under the firm's own 35% ceiling. The Phase 2 CFO Advisor is built specifically to fund this from new revenue, not partner take-home.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Platinum</b>", S["price_main"]),
     Paragraph("$15,997/mo", S["price_main"])],
    [Paragraph("Google + Meta, local SEO/GBP, website fixes, call tracking, NAP cleanup.", S["price_detail"]),
     Paragraph("<strike>$18,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>FCOO Advisor</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Dedicated fractional COO + intake team build-out, incl. group coaching.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$17,500–$125,000/mo", S["price_main"])],
    [Paragraph("Goes to Google and Meta — not to SMB Team.", S["price_detail"]),
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
    "Total: $19,294/mo + $17,500–$125,000 ad spend  |  Save $3,500/mo by bundling  |  8.8%–34.6% of revenue (under 35% cap)",
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
