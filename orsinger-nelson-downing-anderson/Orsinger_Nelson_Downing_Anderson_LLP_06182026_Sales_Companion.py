"""
Sales Companion PDF — SMB Team
Firm: Orsinger, Nelson, Downing & Anderson, LLP (Jeff Anderson individual practice)
Date: June 18, 2026
Rep: Dan Bryant
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

OUTPUT_PATH = "orsinger-nelson-downing-anderson/Orsinger_Nelson_Downing_Anderson_LLP_06182026_Sales_Companion.pdf"


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

story.append(Paragraph("Orsinger, Nelson, Downing &amp; Anderson, LLP", S["title"]))
story.append(Paragraph("Sales Companion  |  June 18, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Jeff Anderson", S["snap_value"]),
     Paragraph("Est. $1M–$2M (not disclosed)", S["snap_value"]),
     Paragraph("2 (Jeff + Alicia)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Frisco + Dallas, TX", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE &amp; DOMINATE", S["section"]))
story.append(Paragraph("Jeff wants his individual practice to recover and expand its market position so he can practice law at the highest level without managing vendor failures or being his own marketing department.", S["subsection"]))

story.append(quote_block("LSA generated many low-quality, broke leads — that's why we discontinued it."))
story.append(Spacer(1, 1))
story.append(quote_block("I want about 20% more leads right now, and higher volume in about 6 months when I expand my space and add headcount."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Quality leads, not volume.</b> Wants high-net-worth divorce clients — not the price-sensitive inquiries LSA produced."))
story.append(bd("<b>Proven results, not reports.</b> 2.5 years of organic decline with no fix has made him skeptical of vendors."))
story.append(bd("<b>Marketing that scales with him.</b> Planning physical expansion in 6 months — needs a system that grows without adding to his workload."))
story.append(bd("<b>Visibility that matches his credentials.</b> 30 years, board certified, 19x D Magazine — he deserves digital presence that reflects that."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Prior bad LSA experience.</b> Broad targeting produced poor leads — created skepticism about paid ads as a category."))
story.append(b("<b>Investment sensitivity.</b> Revenue not disclosed; needs a clear ROI case before committing."))
story.append(b("<b>22 reviews vs. 226 (Coker Robb).</b> May not know that review volume drives map pack rank more than rating."))
story.append(b("<b>Vendor trust deficit.</b> 2.5 years of decline with no recovery explanation has eroded confidence in digital marketing."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Qualified divorce and custody inquiries from targeted paid and organic channels — without him managing a vendor."))
story.append(bd("Review generation closes the Coker Robb gap (22 vs. 226) and restores map pack visibility in Frisco."))
story.append(bd("PPC filtered for high-net-worth keywords means leads match the complex cases he specializes in."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $11,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue est. $1M–$2M individual practice (HubSpot $5M+ is firm-wide for 21 attorneys)."))
story.append(b("Growth tier: Dallas Tier 1 market; $7,000/mo ad spend cap fits initial 20% more leads goal."))
story.append(b("NAP fix, GBP category update, review generation — the specific issues Jeff raised on the call."))
story.append(b("SEO recovery addresses the 2.5-year visibility decline the previous vendor never fixed."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Org design, role definitions, and intake framework built before the 6-month expansion — not scrambled together after."))
story.append(bd("Weekly coaching keeps operational build on track alongside the marketing ramp-up."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Team under 5: Master's Circle not eligible; Elite Coach Plus is correct tier."))
story.append(b("6-month expansion planned — coaching now prevents hiring before structure is in place."))
story.append(b("No dedicated intake role identified; Coach Plus provides the system design to define it correctly."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("ONDA / Jeff Anderson — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Paid search fills the gap that declining organic and discontinued LSA created — producing a consistent flow of high-intent divorce inquiries while SEO recovers."))
story.append(bd("Conservative spend starts small and proves the model — giving Jeff the ROI data he needs to feel confident before scaling to the aggressive level."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — minimum viable Google Search + Meta retargeting for Frisco/Dallas family law."))
story.append(b("<b>Aggressive:</b> $7,000/mo — Growth tier cap; full Frisco/Dallas paid presence for divorce, custody, and protective orders."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 2–3 cases x $15,000 = $37,500/mo vs. $3,500 spend = 10.7x return (estimated)."))
story.append(b("<b>Aggressive:</b> 6–7 cases x $15,000 = $97,500/mo vs. $7,000 spend = 13.9x return (estimated)."))
story.append(Paragraph("<i>Case value estimated at $15,000 — board-certified complex divorce profile; not transcript-confirmed. All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Family law minimums: Google PPC $1,500 + LSA $1,000 + Meta $1,000 = $3,500."))
story.append(b("<b>Aggressive:</b> 2x $1.5M goal x 20% / 12 = $50K; minus $11,397 fee = $38,603 available — capped at Growth tier limit of $7,000."))
story.append(b("Total at aggressive: $11,397 + $3,200 + $7,000 = $21,597/mo = ~17.3% of $125K/mo revenue estimate. Well under 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I tried paid ads before and they just brought in low-quality leads."', S["objection_q"]))
story.append(Paragraph("The LSA experience was a broad pay-per-lead format — not a targeted PPC campaign. Our Google Search approach uses board-certified divorce attorney keywords and strong negative keyword filtering to attract the high-net-worth clients you specialize in. The targeting is fundamentally different from what you ran before.", S["objection_a"]))

story.append(Paragraph('"I\'m not sure I can afford this right now."', S["objection_q"]))
story.append(Paragraph("Conservative scenario at $3,500 ad spend: 2–3 cases per month at $15,000 = $37,500 in estimated revenue vs. $14,597 in total SMB fees. That is a 2.6x return on total investment in month one — before compounding SEO and review gains. The cost of not acting is the continued decline that has been happening for 2.5 years.", S["objection_a"]))

story.append(Paragraph('"My organic rankings are declining — can you actually fix that?"', S["objection_q"]))
story.append(Paragraph("The NAP inconsistency (Suite 210 vs. Suite 200 across your sites), the outdated primary GBP category, and the 22-review gap vs. 226 for Coker Robb are all identifiable, fixable signals. We address all three in the first 90 days — and unlike the previous vendor, we have a documented recovery playbook specific to the DFW family law market.", S["objection_a"]))

story.append(Paragraph('"Why do I need coaching if I already have marketing?"', S["objection_q"]))
story.append(Paragraph("You're planning a physical expansion in 6 months — more space, more headcount. The coaching builds the org structure and intake system before you hire, so the expansion creates efficiency rather than overhead. Marketing brings leads; coaching ensures the team converts them and the practice scales without adding to your personal workload.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$11,397/mo", S["price_main"])],
    [Paragraph("Google PPC, GBP optimization, review generation, SEO recovery, Meta retargeting.", S["price_detail"]),
     Paragraph("<strike>$11,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, practice area masterminds, quarterly workshops, annual in-person event.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,500–$7,000/mo", S["price_main"])],
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
    "Total: $14,597/mo + $3,500–$7,000 ad spend  |  Save $897/mo by bundling  |  ~17%–21% of revenue (under 35% cap)",
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
