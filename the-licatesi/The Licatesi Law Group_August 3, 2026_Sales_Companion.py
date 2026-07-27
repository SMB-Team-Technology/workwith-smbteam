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

OUTPUT_PATH = "the-licatesi/The Licatesi Law Group_August 3, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("The Licatesi Law Group, LLP", S["title"]))
story.append(Paragraph("Sales Companion  |  August 3, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Michael Licatesi", S["snap_value"]),
     Paragraph("~$720K/yr (~$60K/mo, transcript)", S["snap_value"]),
     Paragraph("Michael + Brianna named", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Uniondale, NY (HQ)", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM (HANDS-OFF)", S["section"]))
story.append(Paragraph("Michael wants a marketing partner that runs on its own, so he and Brianna get their time back.", S["subsection"]))

story.append(quote_block("A hands-off marketing solution to free up his and Brianna's time."))
story.append(Spacer(1, 1))
story.append(quote_block("Requires constant prompting from Brianna."))
story.append(Spacer(1, 1))
story.append(quote_block("He will proceed only if the cost is financially viable and the risk is low, given past negative experiences."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Hands-off marketing.</b> A partner who reports results instead of needing to be chased for them."))
story.append(bd("<b>Predictable case flow.</b> Clear, reconciled numbers on spend, cases, and case value."))
story.append(bd("<b>Low risk.</b> A guaranteed acquisition-cost framework after being burned by an underpriced vendor job."))
story.append(bd("<b>Brand clarity.</b> One consolidated site and brand instead of a fragmented rebrand in progress."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Vendor dependency.</b> Current marketing vendor needs constant prompting and shows no clear ROI."))
story.append(b("<b>Fragmented brand.</b> tllgllp.com placeholder, legacy Rubin & Licatesi brand, and NAP inconsistencies split visibility."))
story.append(b("<b>Organic invisibility.</b> Firm does not surface in top results for its own core local searches."))
story.append(b("<b>Unreconciled numbers.</b> Lead-gen spend vs. case volume vs. case value don't add up cleanly yet."))
story.append(b("<b>Risk aversion.</b> Past vendor experience (underpriced $1,000 job) makes him cautious on new spend."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Replaces the vendor relationship that requires constant prompting with managed reporting."))
story.append(bd("Consolidates the fragmented rebrand (NAP, legacy brand, placeholder domain) into one clean presence."))
story.append(bd("Puts the firm's own name back in front of Nassau County searchers instead of named competitors."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ($624.5K-$720K) fits the $500K-$1M Starter band; Essentials is excluded (PI hides Essentials, and firm has 3 locations)."))
story.append(b("Ad spend cap at this tier is $20,000/mo — matches our recommended aggressive spend exactly."))
story.append(b("Stand-alone price is $5,697/mo — bundling saves $700/mo."))
story.append(b("Covers website/local SEO, Google Search, LSA, and Meta management in one package."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Michael a framework to reconcile lead-gen spend, case volume, and case value."))
story.append(bd("Builds the financial visibility he currently lacks beyond the ~$1,800/case acquisition cost."))
story.append(bd("Supports stepping back from day-to-day oversight with confidence, not guesswork."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue band ($400K-$1M) and no dedicated ops leadership fit Elite Coach Plus exactly."))
story.append(b("Stand-alone price is $3,497/mo — bundling saves $297/mo."))
story.append(b("Includes weekly group coaching, practice area masterminds, and quarterly workshops."))
story.append(b("FCOO Advisor was considered per package_decision.json notes but held for Phase 2 — no dedicated ops staff yet."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Licatesi Law Group — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Replaces $100K/month flowing to a third-party lead-gen agency with spend the firm can see and control."))
story.append(bd("Builds toward the $100K/month revenue goal with a reconciled, trackable acquisition cost."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $10,000/mo — clears Google PPC MVA minimum ($10,000) and PI medium-competitiveness floor ($7,500)."))
story.append(b("<b>Aggressive:</b> $20,000/mo — capped at the Starter tier's ad-spend ceiling (see calculation below)."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 13.3 leads x 15% = ~2.0 cases x $7.5K = $15K/mo vs. $10K spend = 1.5x return."))
story.append(b("<b>Aggressive:</b> 31.9 leads x 15% = ~5 cases x $7.5K = $37.5K/mo vs. $20K spend = 1.9x return."))
story.append(Paragraph("<i>All figures are estimates. Average case value ($7,500) is an MVA default, not transcript-stated. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> MVA channel minimums: Google PPC $10,000 clears the medium-competitiveness PI floor ($7,500)."))
story.append(b("<b>Aggressive:</b> $1.2M goal x 20% / 12 = $20,000. Tier 1 NYC multiplier (1.5x) = $30,000, minus $4,997 fee = ~$25,000 available — capped at the Starter tier's $20,000 ceiling since revenue does not meet the Growth tier's $1M floor."))
story.append(b("Total spend at aggressive: $20,000/mo + $8,197 bundled = $28,197/mo = ~47% of $720K/12 monthly revenue if annualized run-rate is used flatly; scoping team should confirm this against actual monthly cash flow before finalizing, given the cap is near the practical ceiling for this revenue band."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"Our current vendor already handles this — why switch?"', S["objection_q"]))
story.append(Paragraph("The current vendor requires constant prompting from Brianna and shows no clear ROI — plus underpriced a $1,000 job that should have cost $4,500, raising stability concerns.", S["objection_a"]))

story.append(Paragraph('"How do I know this budget is safe given past bad experiences?"', S["objection_q"]))
story.append(Paragraph("SMB Team's proposed guaranteed acquisition-cost range ($2,500-$4,000/case) is a direct, structured answer to the risk-aversion Michael raised on the call.", S["objection_a"]))

story.append(Paragraph('"We are already 291 reviews at 4.8 stars — is SEO really the gap?"', S["objection_q"]))
story.append(Paragraph("Yes — despite that review base, the firm does not surface in top organic results for its own core searches, while Palermo Law (400+ reviews) and Raphaelson & Levine (700+ reviews) do.", S["objection_a"]))

story.append(Paragraph('"Why does the aggressive ad spend stop at $20,000 instead of scaling to the $100K/month revenue goal?"', S["objection_q"]))
story.append(Paragraph("The 20% rule and geo multiplier point to ~$25,000 available, but current revenue doesn't yet meet the $1M floor required to move to a higher tier — so spend is capped at the Starter tier's $20,000 ceiling rather than over-extending the firm.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("Website/SEO, Google Search, LSA, and Meta management.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, masterminds, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$10,000-$20,000/mo", S["price_main"])],
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
    "Total: $8,197/mo + $10,000-$20,000 ad spend  |  Save $997/mo by bundling  |  Confirm % of revenue with scoping before final signature",
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
