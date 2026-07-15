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

OUTPUT_PATH = "mcfall-legal/McFall Legal_July 24, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("McFall Legal (McFall Law, LLC)", S["title"]))
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
    [Paragraph("Alan McFall, Esq.", S["snap_value"]),
     Paragraph("~$180K (est., unconfirmed)", S["snap_value"]),
     Paragraph("2 attorneys", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Bangor, PA", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.7*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Paragraph(
    "<i>No discovery call transcript was available for this research pass. Revenue, team size, "
    "close rate, and DBM below are defaults/inferences from public site research — confirm on the "
    "proposal call before finalizing terms.</i>", S["disclaimer"]))
story.append(Spacer(1, 4))

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: LEGACY", S["section"]))
story.append(Paragraph(
    "Alan founded the solo practice in 2021 and brought son Jason on in 2023 — the inferred DBM "
    "is building a firm that runs itself and can be handed to Jason with real stability, not just a "
    "client list.", S["subsection"]))

story.append(Paragraph("<b>What he wants (inferred, unconfirmed on a call):</b>", S["subsection"]))
story.append(bd("<b>A firm Jason can inherit.</b> Not just casework, but a business with systems."))
story.append(bd("<b>Less personal dependency.</b> New clients should not depend entirely on Alan being reachable."))
story.append(bd("<b>Recognition to match reputation.</b> A 4.8-star, 21-review record that outperforms local competitors, but isn't yet reflected everywhere prospects look."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No lead system.</b> New clients depend on referrals, not a repeatable marketing engine."))
story.append(b("<b>No intake process.</b> A single consultation form with no confirmed follow-up behind it."))
story.append(b("<b>Directory drift.</b> Avvo, FindLaw, and Yellow Pages still show the pre-2021 legacy firm name."))
story.append(b("<b>No geo-landing pages.</b> Competitor Daly Law Offices has built exactly this, with fewer reviews."))
story.append(b("<b>No financial visibility.</b> No documented profit plan or known cost-per-acquisition."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Replaces referral-only growth with a repeatable lead system across both practice areas."))
story.append(bd("Closes the geo-landing-page gap against Daly Law Offices before it widens further."))
story.append(bd("Fixes the five-year-old NAP inconsistency across Avvo, FindLaw, and Yellow Pages."))

story.append(Paragraph("<b>Full Service Marketing — Essentials  |  $3,397/mo bundled</b>", S["subsection"]))
story.append(b("Estimated revenue (~$180K) places this firm in the entry Essentials tier — no lower Full Service tier exists."))
story.append(b("Firm currently has zero confirmed paid ads or geo-landing infrastructure — starting from the ground floor."))
story.append(b("Essentials tier ad spend cap is $7,500/mo, matching our aggressive ad spend recommendation exactly."))
story.append(b("Essentials has no stand-alone comparison price — it is the floor offering on the marketing ladder."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the defined intake and follow-up process this firm does not currently have."))
story.append(bd("Establishes cost-per-acquisition tracking and a documented profit plan for the first time."))
story.append(bd("Lays the operational groundwork before any FCOO/FCFO add-on would make sense."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Team of 2 attorneys plus unconfirmed support staff is well under the 5-person Master's Circle threshold."))
story.append(b("No dedicated ops, marketing, or intake staff exists yet — Elite Coach fits the current stage."))
story.append(b("Stand-alone price is $3,497/mo — bundled saves $897/mo against this package alone."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("McFall Legal — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns the firm's real 4.8-star, 21-review advantage into paid search visibility it does not currently use."))
story.append(bd("Captures Bangor/Northampton County estate planning and real estate searches before Daly or Ceraul do."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — Google PPC minimum for the estate planning practice area."))
story.append(b("<b>Aggressive:</b> $7,500/mo — the Essentials tier's ad spend cap (no stated revenue goal to run the 20% rule against)."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~3 cases x $3K avg case value = ~$9K/mo vs. $3.5K spend = ~2.6x return."))
story.append(b("<b>Aggressive:</b> ~11 cases x $3K avg case value = ~$33K/mo vs. $7.5K spend = ~4.4x return."))
story.append(Paragraph("<i>All figures are estimates based on documented CPL/case-value defaults, not firm-confirmed numbers. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Estate Planning Google Search CPL midpoint $135 + 20% cushion = ~$162 blended CPL. $3,500 / $162 = ~21 leads x 15% close = ~3 cases."))
story.append(b("<b>Aggressive:</b> Blended CPL across Google/LSA/Meta (~$98, weighted 50/30/20). $7,500 / $98 = ~76 leads x 15% close = ~11 cases."))
story.append(b("<b>SCOPING FLAG:</b> at the $180K revenue estimate ($15K/mo), fees + aggressive ad spend = $13,497/mo = ~90% of revenue — well over the 35% cap. Revenue is unconfirmed; verify with Alan directly before finalizing terms."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We already get plenty of clients from referrals."', S["objection_q"]))
story.append(Paragraph("Daly Law Offices has fewer reviews (13 vs. our 21) but has already built out geo-landing pages capturing search traffic referrals alone will never reach.", S["objection_a"]))

story.append(Paragraph('"Isn’t this a lot to spend for a firm our size?"', S["objection_q"]))
story.append(Paragraph("Our revenue figure is an estimate from HubSpot, not a confirmed number — let's verify actual revenue together so the investment is scoped to reality, not a guess.", S["objection_a"]))

story.append(Paragraph('"We don’t have staff to handle more leads."', S["objection_q"]))
story.append(Paragraph("That's exactly what Elite Coach coaching builds first — a defined intake process before lead volume increases.", S["objection_a"]))

story.append(Paragraph('"Our website already looks fine."', S["objection_q"]))
story.append(Paragraph("PageSpeed scores could not be verified this session and should be confirmed — but regardless of speed, the site has no geo-landing infrastructure competitors like Daly already have.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Essentials</b>", S["price_main"]),
     Paragraph("$3,397/mo", S["price_main"])],
    [Paragraph("Paid ads, local SEO, directory cleanup, geo-landing pages.", S["price_detail"]),
     Paragraph("Entry tier — no stand-alone price", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, masterminds, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,500–$7,500/mo", S["price_main"])],
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
    "Total: $5,997/mo + $3,500–$7,500 ad spend  |  Save $897/mo by bundling  |  "
    "~40.0%–90.0% of estimated $15K/mo revenue (exceeds 35% cap — confirm revenue, scoping approval required)",
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
