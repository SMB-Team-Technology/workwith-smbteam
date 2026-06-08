"""
Sales Companion PDF — Maiden Law Firm
SMB Team | June 5, 2026 | Rep: Randy Gold
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

OUTPUT_PATH = "maiden-law-firm/Maiden Law Firm_June 5, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Maiden Law Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  June 5, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Brooke Maiden, Esq.", S["snap_value"]),
     Paragraph("~$500K (est.)", S["snap_value"]),
     Paragraph("~3 (est.)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Mt. Pleasant, SC", S["snap_value"])],
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
story.append(Paragraph("No transcript — DBM inferred. Boutique PI firm, founder-run, 4.5 stars, zero paid marketing. Wants cases without personally chasing them.", S["subsection"]))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable case flow.</b> A system that brings in qualified PI leads so she isn't relying on referrals."))
story.append(bd("<b>Intake that runs without her.</b> Someone else qualifying and booking consultations."))
story.append(bd("<b>Planned owner compensation.</b> A financial framework — not whatever happens to settle."))
story.append(bd("<b>Time and choice.</b> Ability to take a week off without cases falling through the cracks."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No paid advertising on any channel.</b> Google, LSA, and Meta all untouched while competitors spend heavily."))
story.append(b("<b>31 reviews vs. 730 (Drennan) and 2,260+ (Joye).</b> Not appearing in 3-pack for any competitive keyword."))
story.append(b("<b>No intake specialist or after-hours coverage.</b> Attorney likely handles every inquiry personally."))
story.append(b("<b>Revenue unconfirmed (est. $500K, low confidence).</b> Confirm before finalizing — 35% cap requires ~$640K+ at $10K ad spend."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Maiden Law Firm appears in Google for 'car accident lawyer Charleston SC' — searches going entirely to competitors today."))
story.append(bd("LSA places the firm above paid ads and the map pack; charges per qualified lead, not per click."))
story.append(bd("Review strategy begins closing the 699-review gap with Drennan Law Firm."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("PI practice — Essentials not eligible; Starter is the minimum tier for personal injury."))
story.append(b("Revenue $400K–$1M estimated — Starter is the correct revenue-band match."))
story.append(b("No paid ads on any channel — full service needed, not ads-only sub-package."))
story.append(b("Site missing attorney bio, practice area pages, geo-targeting — rebuild required."))

story.append(thin_rule())

# ── Phase 2 Note ──
story.append(Paragraph("Phase 2 Note (For Randy Gold)", S["section"]))
story.append(Paragraph("<b>Coaching is not included in Phase 1 per sales rep directive.</b>", S["subsection"]))
story.append(b("Phase 1 = Full Service Marketing — Starter only. Do not present coaching as part of this proposal."))
story.append(b("Phase 2 recommendation: Add Elite Coach Plus ($3,200/mo bundled) once marketing launches and Brooke sees lead volume growing — frame as the system that converts more leads into signed cases without her personally running intake."))
story.append(b("Natural trigger: After first 60–90 days when she's asking 'how do I handle all these leads?' — that is the coaching conversation."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Maiden Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("PI leads arrive from Google and LSA within 90 days — without Brooke personally sourcing them."))
story.append(bd("Conservative spend projects ~5–6 cases/mo ($41K revenue) vs. $10K spend — a ~4x return (est.)."))

story.append(Paragraph("<b>Ad Spend Range &amp; ROI (estimates — confirm case value and close rate):</b>", S["subsection"]))
story.append(b("<b>Conservative $10K/mo:</b> ~37 leads x 15% close x $7,500 = ~$41,000 revenue. ~4x return. PPC $5K + LSA $3K + Meta $2K."))
story.append(b("<b>Aggressive $20K/mo:</b> ~89 leads x 15% close x $7,500 = ~$100,000 revenue. ~5x return. Exceeds Starter cap — Growth tier upgrade or 10% overage required."))
story.append(b("<b>35% cap:</b> $4,847 fees + $10K ads = $14,847 / est. $41,667 mo rev = 36%. Near cap — confirm revenue is at least ~$510K annually. If revenue is lower, reduce ad spend first."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I\'m not sure I have the budget for this right now."', S["objection_q"]))
story.append(Paragraph("Joye Law Firm (2,260+ reviews) and Drennan Law Firm (730 reviews) are spending now to own the searches Maiden Law Firm isn't appearing in. Conservative scenario: ~$41K estimated monthly revenue vs. $10K ad spend — designed to be self-funding.", S["objection_a"]))

story.append(Paragraph('"How do I know this will generate cases in my market?"', S["objection_q"]))
story.append(Paragraph("The market is generating the cases — Joye Law Firm proves it. They didn't invent demand; they built systems to capture it. Maiden Law Firm has a 4.5-star reputation and real client testimonials. The quality is there. The system to get in front of searchers is what's missing.", S["objection_a"]))

story.append(Paragraph('"I need to think about it."', S["objection_q"]))
story.append(Paragraph("Every month is a month Drennan Law Firm (699 more reviews) and Joye Law Firm (advertising on every channel) extend their lead. Urgency score 8/10 — this is not a future problem. The audit gives Graham and Brooke everything they need to make the decision.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, Google Ads, LSA, local SEO, Facebook/Instagram ads.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$10,000–$20,000/mo", S["price_main"])],
    [Paragraph("Goes to Google, LSA, and Meta — not to SMB Team. Confirm tier/overage for $20K.", S["price_detail"]),
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
]))
story.append(pt)
story.append(Paragraph(
    "Total SMB fees: $4,847/mo + $10K–$20K ad spend  |  Save $850/mo vs. stand-alone  |  Phase 1: marketing only per sales rep directive",
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
