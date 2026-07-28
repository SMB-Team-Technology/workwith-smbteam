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

OUTPUT_PATH = "krause-kinsman/Krause & Kinsman Law Firm_August 4, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Krause & Kinsman Law Firm", S["title"]))
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
    [Paragraph("R. Kinsman & A. Krause", S["snap_value"]),
     Paragraph("Not stated (est. $3M+)", S["snap_value"]),
     Paragraph("2 partners +", S["snap_value"]),
     Paragraph("Stage 5", S["snap_value"]),
     Paragraph("Not stated (15% default)", S["snap_value"]),
     Paragraph("Kansas City, MO", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: PROTECTED BANDWIDTH", S["section"]))
story.append(Paragraph(
    "Robert and Adam want to launch and scale the IUL vertical without it consuming the personal time they've already built the mass tort practice to protect.",
    S["subsection"]))

# NOTE: No word-for-word transcript quotes were captured in the research notes
# (extraction was paraphrased) — omitting quote_block() rather than fabricating quotes.

story.append(Paragraph("<b>What they want:</b>", S["subsection"]))
story.append(bd("<b>Launch the IUL vertical fast.</b> ~100 cases in 60 days to validate before scaling to thousands."))
story.append(bd("<b>Protect partner time.</b> AI-avatar chosen because it replaces hours of filming with a 30-second approval."))
story.append(bd("<b>Cut inbound call volume.</b> Automate status updates to the 100,000+ existing mass tort client base."))
story.append(bd("<b>Beat competitors to market.</b> RP Legal LLC and Stoltmann Law are already building this exact content."))

story.append(Paragraph("<b>What is stopping them:</b>", S["subsection"]))
story.append(b("<b>Zero social presence.</b> No organic or paid social media exists today for either practice."))
story.append(b("<b>No dedicated content producer.</b> Content creation depends entirely on partner bandwidth."))
story.append(b("<b>No IUL landing page or intake path.</b> Nowhere for interested prospects to convert yet."))
story.append(b("<b>No connected profit benchmark.</b> The 100-case goal has no cost-per-case target attached."))

story.append(thin_rule())

# ── Why This Social & Content Package (replaces "Marketing Package" — see
#    Transcript-Stated Need Override in section_11_workings.txt: this is a
#    social/content engagement, not a local marketing engagement) ──
story.append(Paragraph("Why This Social & Content Package", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Builds paid + organic social distribution on the channels — TikTok, Instagram — where MLM-targeted IUL prospects already are."))
story.append(bd("Gives the firm a repeatable national content funnel instead of one-off posts with no promotion behind them."))

story.append(Paragraph("<b>OmniSocial AI 360 (Content + Ads Bundle)  |  $5,444/mo bundled</b>", S["subsection"]))
story.append(b("Ads – Platinum ($3,997/mo) matches the firm's stated $25K-$50K ad spend range."))
story.append(b("Content – Standard ($1,797/mo) covers the organic content calendar and publishing. Bundle saves $350/mo."))
story.append(b("Escalation: requires sales-ops approval (72-hour turnaround) — do not promise same-day terms."))

story.append(thin_rule())

# ── Why This Content Production Package (replaces "Coaching Package" — see
#    override note above; no coaching need was raised on this call) ──
story.append(Paragraph("Why This Content Production Package", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Produces IUL case-acquisition video and client status-update videos without Robert or Adam filming anything themselves."))
story.append(bd("Turns a 30-second approval into a monthly content pipeline — 1 long-form + 30 short-form videos — that targets the slow-communication complaint in the firm's own reviews."))

story.append(Paragraph("<b>AI Avatar Video Growth Add-On  |  $1,950/mo bundled + $2,997 one-time setup</b>", S["subsection"]))
story.append(b("Escalation: requires Alexis approval before finalizing the proposal."))
story.append(b("Standalone tier doesn't qualify yet (no paid-ads/organic-social history) — Add-On pairs with OmniSocial AI 360 instead. 12-month term, auto-renewal."))
story.append(b("Deliverables: 1 long-form + 30 short-form videos/mo, YouTube optimization, 5 scripts/quarter, quarterly strategy meetings."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Krause & Kinsman — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Establishes national paid social reach to compete for the IUL/MLM fraud audience before more competitors enter."))
story.append(bd("Funds the 100-case, 60-day validation window the firm itself proposed."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $25,000/mo — the firm's own stated starting number from the discovery call."))
story.append(b("<b>Aggressive:</b> $50,000/mo — the firm's own stated upper number from the discovery call."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~50 cases/mo (client's own 100-case/60-day goal) x case value not yet established = revenue TBD vs. $25K spend."))
story.append(b("<b>Aggressive:</b> Same case-acquisition target scaled faster x case value not yet established = revenue TBD vs. $50K spend."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. IUL/mass tort case value was not discussed on the call — confirm with the prospect before quoting a revenue figure.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("Both figures are the firm's own stated ad spend range from the discovery call, not a formula-derived estimate — no local PPC/LSA/Meta minimums apply, since this is a national social vertical, not a local practice area in the standard scoping tables."))
story.append(b("Total spend at aggressive ($50,000/mo) + package fees ($7,394/mo) = $57,394/mo. Cannot be benchmarked precisely as % of revenue since exact revenue was not stated — estimated at $3M+ for cap-check purposes only; confirm actual figure with sales before finalizing."))
story.append(b("Ad spend over $25,000/mo requires internal scoping approval."))

story.append(thin_rule())

# ── If They Push Back ──
story.append(Paragraph("If They Push Back", S["section"]))

story.append(Paragraph('"We don\'t want a 12-month commitment for something this experimental."', S["objection_q"]))
story.append(Paragraph("The Add-On video package validates within the same 60-day window the firm already set. If commitment length is the blocker, the One-Time AI Avatar package ($1,850, no recurring contract) is a lower-commitment starting point — flag with Alexis before offering.", S["objection_a"]))

story.append(Paragraph('"Why isn\'t this cheaper — we\'re not asking for local SEO or ads in Kansas City."', S["objection_q"]))
story.append(Paragraph("Correct — nothing in this proposal charges for the existing mass tort/local marketing, which already performs well (400-700+ reviews, ~4.7 stars). Every dollar here targets the IUL vertical gap identified on the call.", S["objection_a"]))

story.append(Paragraph('"How do we know this will actually produce 100 cases in 60 days?"', S["objection_q"]))
story.append(Paragraph("We don't have a stated case value or CPL benchmark for IUL specifically. Confirm expected case economics with the prospect directly, and frame the 60-day window as a validation period, not a guarantee.", S["objection_a"]))

story.append(Paragraph('"Can the AI avatar handle updates for something this sensitive (mass tort claims)?"', S["objection_q"]))
story.append(Paragraph("Yes — this is a scripted, recorded update format reviewed and approved by the firm before it's sent (the 30-second approval step), not a live or unscripted interaction.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>OmniSocial AI 360 (Content + Ads Bundle)</b>", S["price_main"]),
     Paragraph("$5,444/mo", S["price_main"])],
    [Paragraph("Paid + organic social distribution for the IUL vertical.", S["price_detail"]),
     Paragraph("<strike>$5,794</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>AI Avatar Video Growth Add-On</b>", S["price_main"]),
     Paragraph("$1,950/mo", S["price_main"])],
    [Paragraph("AI-avatar video production + client status updates. Flat rate, plus $2,997 one-time setup.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$25,000–$50,000/mo", S["price_main"])],
    [Paragraph("Goes to Meta and social ad platforms — not to SMB Team.", S["price_detail"]),
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
    "Total: $7,394/mo + $25,000–$50,000 ad spend  |  Save $350/mo by bundling  |  Revenue not confirmed (est. $3M+) — confirm with sales before quoting % of revenue",
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
