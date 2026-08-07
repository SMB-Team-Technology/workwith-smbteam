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

OUTPUT_PATH = "zimmer-rens/Zimmer & Rens LLC_August 7, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Zimmer &amp; Rens LLC", S["title"]))
story.append(Paragraph("Sales Companion  |  August 7, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Paul Zimmer / Taylor Rens", S["snap_value"]),
     Paragraph("~$1.8M (est., not stated)", S["snap_value"]),
     Paragraph("16 (9 attys)", S["snap_value"]),
     Paragraph("4 - SBM", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Brookfield WI +La Crosse", S["snap_value"])],
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
story.append(Paragraph(
    "<i>Revenue not stated on the call — no package_decision.json or HubSpot lookup available. "
    "Confirm actual revenue with Taylor before finalizing pricing tier.</i>", S["disclaimer"]))

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: SCALE", S["section"]))
story.append(Paragraph(
    "Paul and Taylor are building a multi-office, multi-practice-area firm — not stated as a "
    "personal-freedom quote on this call, so confirm directly, but the expansion pattern (4 new "
    "practice areas + a 2nd office) points to scale/dominate.", S["subsection"]))

story.append(quote_block("The firm's fractional CFO confirms marketing spend is significantly below the industry benchmark of ~20% of revenue."))
story.append(Spacer(1, 1))
story.append(quote_block("A prior quote from a non-specialist consultant for $100k was deemed too high."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What they want:</b>", S["subsection"]))
story.append(bd("<b>Four new practice areas funded properly</b> — estate planning, criminal defense, PI, first-party bad faith."))
story.append(bd("<b>A second office that opens strong</b> — not from a standing start in La Crosse."))
story.append(bd("<b>Right-sized AI automation</b> — not a $100K generalist consultant."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping them:</b>", S["subsection"]))
story.append(b("<b>No after-hours intake.</b> Most CD/PI leads come in outside 9-5 — direct revenue leak."))
story.append(b("<b>Zero paid presence.</b> No ads in criminal defense or estate planning yet, the 2 priority areas."))
story.append(b("<b>Revenue not confirmed.</b> No number stated on the call — treat all tier/pricing math below as an estimate pending confirmation."))
story.append(b("<b>Marketing spend below benchmark.</b> Firm's own CFO already flagged this — an easy internal 'yes, we know' on the call."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Gives estate planning and criminal defense their own lead flow instead of leftover real estate referrals."))
story.append(bd("Directly closes the CFO-flagged marketing-spend-below-benchmark gap."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("Quoted at Starter per Jacob's package instruction for this call — note the $1.8M revenue estimate would otherwise place the firm in the Growth tier; confirm with Taylor whether Starter or Growth is the right fit."))
story.append(b("FLAG: Starter's ad cap is $20K/mo — below the $23.4K-$37.1K/mo range this proposal recommends. Confirm with Jacob whether to cap ad spend to $20K or upgrade the marketing tier before presenting."))

story.append(thin_rule())

# ── Why This AI Package ──
story.append(Paragraph("Why This AI Package", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Fractional CTO L1 delivers the operational AI automation the firm explicitly asked for — without the $100K generalist price tag."))

story.append(Paragraph("<b>Fractional CTO L1 $3,297/mo bundled</b>", S["subsection"]))
story.append(b("16-person team with dedicated ops/intake staff (office manager, paralegals) gives the firm the bandwidth to engage with a done-with-you AI rollout."))
story.append(b("CTO L1 chosen over L2 — transcript describes a modest initial need (email/scheduling), and the firm already balked at a $100K quote."))
story.append(b("Escalation flag: confirm LAW delivery capacity with sales rep before this proposal is finalized."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Zimmer &amp; Rens — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Funds Estate Planning and Criminal Defense only — the two areas explicitly prioritized on the call."))
story.append(bd("Stays under the 35%-of-revenue cap even at the aggressive end, so it doesn't compete with the CTO/coaching spend."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $23,400/mo — channel minimums for Estate Planning ($10,200) + Criminal Defense ($13,200)."))
story.append(b("<b>Aggressive:</b> $37,100/mo — under the 35% total-spend rule, but exceeds the Starter tier's $20K ad cap (see flag above)."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~27 cases/mo x ~$3.1K avg = ~$83K/mo vs. $23.4K spend = ~3.5x return."))
story.append(b("<b>Aggressive:</b> ~52 cases/mo x ~$3K avg = ~$158K/mo vs. $37.1K spend = ~4.3x return."))
story.append(Paragraph("<i>All figures are estimates using published CPL ranges and practice-area default case values. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> EP: PPC $3,500 + LSA $2,000 + Meta $4,700 = $10,200. CD: PPC $5,500 + LSA $2,000 + Meta $5,700 = $13,200."))
story.append(b("<b>Aggressive:</b> $3.6M (2x revenue est.) x 20% / 12 = $60,000. Tier 3 (1.15x) = $69,000. Minus $8,294 mgmt fee = $60,706 theoretical."))
story.append(b("35% cap ($150K est. monthly revenue): $52,500 total - $8,294 fees = $44,206 ad spend room — but Starter's own $20K tier cap now binds tighter than either figure (see flag above)."))

story.append(thin_rule())

# ── If They Push Back ──
story.append(Paragraph("If They Push Back", S["section"]))

story.append(Paragraph('"We don\'t know our exact revenue number off the top of our heads."', S["objection_q"]))
story.append(Paragraph("That's fine — this proposal is built on a conservative $1.8M estimate based on team size. If actual revenue is higher, the tier and ad spend ceiling both move up in your favor, not down.", S["objection_a"]))

story.append(Paragraph('"We already tried a $100K AI consultant quote and passed."', S["objection_q"]))
story.append(Paragraph("This is a different scope and a different price point — Fractional CTO Level 1 starts at $3,297/mo focused specifically on email and scheduling automation, led by a law-firm-only CTO, not a generalist $100K engagement.", S["objection_a"]))

story.append(Paragraph('"Why not put all the marketing budget toward real estate — that\'s our proven practice?"', S["objection_q"]))
story.append(Paragraph("Real estate already has referral flow working for it. Estate planning and criminal defense have zero paid presence and named local competitors (Grieve Law, Margerie Law) already dominating those searches — that's where new dollars generate new revenue fastest.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("Dedicated lead gen for Estate Planning &amp; Criminal Defense.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Fractional CTO L1</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("AI automation for email/scheduling.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$23,400–$37,100/mo", S["price_main"])],
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
    "Total: $8,294/mo + $23,400–$37,100 ad spend  |  Save $1,200/mo by bundling  |  "
    "21.1%–30.3% of est. revenue (confirm actual revenue before close — aggressive ad spend exceeds Starter's $20K tier cap, see flag above)",
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
