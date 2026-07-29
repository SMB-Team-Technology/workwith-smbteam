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

OUTPUT_PATH = "davlatov/Davlatov Law Firm, P.C._August 4, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Davlatov Law Firm, P.C.", S["title"]))
story.append(Paragraph("Sales Companion  |  August 4, 2026  |  Rep: Nick Holderman", S["subtitle"]))
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
    [Paragraph("Mustafo Davlatov", S["snap_value"]),
     Paragraph("~$50K/mo (~$600K/yr)", S["snap_value"]),
     Paragraph("Not stated (~3 est.)", S["snap_value"]),
     Paragraph("Stage 3: Solo", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Brooklyn, NY", S["snap_value"])],
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
story.append(Paragraph("Mustafo wants the firm to run without his personal hours behind every case, so he finally gets real time back.", S["subsection"]))

story.append(quote_block("The firm cannot take extended time off without revenue dipping."))
story.append(Spacer(1, 1))
story.append(quote_block("Missed calls are a major issue, causing lost leads and wasted marketing spend."))
story.append(Spacer(1, 1))
story.append(quote_block("Revenue now only covers expenses."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Real time off.</b> Today the firm cannot survive him stepping away, even briefly."))
story.append(bd("<b>Diversified revenue.</b> A pivot into Personal Injury and Family Law to offset a shrinking immigration docket."))
story.append(bd("<b>Actual profit.</b> Not just revenue that covers expenses — money he can keep."))
story.append(bd("<b>A team that runs without him.</b> So new practice areas add revenue, not just more hours."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Immigration is shrinking.</b> A government crackdown has cut case volume and win rates."))
story.append(b("<b>Zero pivot visibility.</b> No search or directory presence in PI or Family Law despite live service pages."))
story.append(b("<b>Missed calls.</b> Marketing spend is being wasted on leads that never get answered."))
story.append(b("<b>No delegation structure.</b> 12-hour days, total owner dependency, no manager in place."))
story.append(b("<b>$1M in uncollected receivables.</b> A real, active cash-flow crunch on top of breakeven revenue."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Personal Injury and Family Law a real shot at generating cases instead of staying invisible."))
story.append(bd("Reduces reliance on a shrinking immigration docket as the firm's only growth engine."))
story.append(bd("Builds local search authority that compounds, instead of depending on referrals alone."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("Multiple practice areas (Immigration, PI, Family Law) rule out Essentials — Starter is the minimum eligible tier."))
story.append(b("Revenue run rate (~$600K/yr) falls squarely in the $500K–$1M Starter band."))
story.append(b("$20,000/mo ad spend cap on Starter matches the aggressive scenario ceiling — no tier upgrade needed yet."))
story.append(b("Covers Google Ads, Local SEO, LSA enrollment, and Meta across all three practice areas."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the firm's first real delegation layer, so Mustafo is not the only one who can run a case."))
story.append(bd("Gives him outside accountability and a peer group he does not have today."))
story.append(bd("Turns growth in new practice areas into less personal workload, not more."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Team size not stated on call (defaulted to 3) — confirm actual headcount."))
story.append(b("<b>Tier note:</b> ~$600K/yr revenue implies Elite Coach Plus, but breakeven cash position + $1M uncollected receivables make Elite Coach the responsible call now (see section_11_workings.txt)."))
story.append(b("Confirm client can sustain the full $7,597/mo before finalizing."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Davlatov — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Even the conservative scenario is projected to generate ~8 cases/mo across all three practice areas — enough to prove out the pivot without overcommitting cash."))
story.append(bd("The aggressive scenario matches the firm's defaulted growth goal, but should be phased in only once cash flow stabilizes."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,500/mo — minimum viable spend across Google, LSA, and Meta for Immigration, PI, and Family Law."))
story.append(b("<b>Aggressive:</b> $20,000/mo — matches the Starter tier's ad spend cap and the firm's defaulted 2x revenue goal."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~8 cases x ~$4.4K = ~$35.2K/mo vs. $7.5K spend = ~4.7x return."))
story.append(b("<b>Aggressive:</b> ~25 cases x ~$4.4K = ~$110K/mo vs. $20K spend = ~5.5x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Blended channel minimums (Google Search, LSA, Meta) across Immigration, PI, and Family Law."))
story.append(b("<b>Aggressive:</b> Defaulted 2x revenue goal (~$1.2M/yr, not stated on call) x 20% / 12 = $20,000/mo — at Starter's cap."))
story.append(b("<b>FLAG:</b> $7,597 mgmt + $20,000 aggressive ad spend = $27,597/mo = 55.2% of TODAY'S $50K/mo revenue — exceeds the 35% cap against current revenue. It only clears the cap (27.6%) against the defaulted $100K/mo goal. Lead with conservative; treat aggressive as a future target, not a day-one ask."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I can\'t take on $27,597 a month on top of everything else."', S["objection_q"]))
story.append(Paragraph("Start at the conservative $7,500/mo ad spend — total commitment of $15,097/mo, or 30.2% of current revenue, under the 35% cap. Aggressive is a future target, not a day-one requirement.", S["objection_a"]))

story.append(Paragraph('"We already tried marketing and it didn\'t work — calls kept getting missed."', S["objection_q"]))
story.append(Paragraph("That is exactly why Elite Coach and the missed-call fix are built into Phase 1 alongside marketing. Gursoy Law Firm (5.0 stars, 270+ reviews) is already capturing the calls this gap is losing.", S["objection_a"]))

story.append(Paragraph('"Immigration is our whole business — why spend on Personal Injury and Family Law?"', S["objection_q"]))
story.append(Paragraph("A government crackdown has already cut immigration case volume and win rates. Karasik Law Group and The Louis Law Firm are already established in PI and Family Law — every month without a presence there is a month further behind.", S["objection_a"]))

story.append(Paragraph('"We have $1M in uncollected receivables — shouldn\'t we fix that first?"', S["objection_q"]))
story.append(Paragraph("Recovering receivables and launching marketing are not mutually exclusive. Phase 1 pairs a collections push with the lowest-cost coaching tier, keeping total spend to 30.2% of current revenue.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("Google Ads, Local SEO, LSA, Meta across Immigration, PI & Family Law.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, delegation-building, group accountability.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,500–$20,000/mo", S["price_main"])],
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
    "Total: $7,597/mo + $7,500–$20,000 ad spend  |  Save $1,597/mo by bundling  |  30.2% of revenue at conservative (aggressive exceeds 35% cap at today's revenue)",
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
