"""
Sales Companion PDF — Scott Levine Law
SMB Team Internal Document — Do Not Share
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

OUTPUT_PATH = "scott-levine-law/ScottLevineLaw_June262026_Sales_Companion.pdf"


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

story.append(Paragraph("Scott Levine Law (Scott D. Levine, APC)", S["title"]))
story.append(Paragraph("Sales Companion  |  June 26, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Scott D. Levine", S["snap_value"]),
     Paragraph("~$2M est.", S["snap_value"]),
     Paragraph("Solo (1)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("Solana Beach, CA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: CONSISTENT CASES &amp; FREEDOM FROM REFERRAL DEPENDENCY", S["section"]))
story.append(Paragraph("Scott wants qualified construction defect clients to find him consistently — so he can focus on complex litigation, not case sourcing.", S["subsection"]))

story.append(quote_block("No transcript provided. DBM inferred: solo practice profile, 'select few clients at a time' website copy, SB800 legislative credential."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Consistent inbound.</b> Qualified cases arriving without depending on who happens to refer to him."))
story.append(bd("<b>Digital authority.</b> SB800 credential and 35-year reputation visible online, not just known by peers."))
story.append(bd("<b>Intake off his plate.</b> First-contact handled by someone else so he stays in complex litigation."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No digital presence.</b> Zero paid ads, 1 confirmed review, no geo pages — invisible online despite extraordinary credentials."))
story.append(b("<b>404 errors on key pages.</b> Practice area and contact pages broken — Google cannot index them."))
story.append(b("<b>Solo operation.</b> Every inquiry runs through Scott personally; no intake staff or delegation."))
story.append(b("<b>Revenue unconfirmed.</b> Estimated $2M from HubSpot profile — verify on June 26 call."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("SB800 co-authorship becomes a live ad asset — 'I wrote the law' headline no competitor can use."))
story.append(bd("San Diego homeowners and HOA boards find Scott before Artemis Law Group (89 reviews, 2 miles away)."))
story.append(bd("1,000+ past clients contacted for Google reviews unlocks LSA eligibility rapidly."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $7,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1M–$3M est.: Growth tier. Essentials hidden at $1M+; Platinum requires $3M+."))
story.append(b("Website rebuild required: 404 errors on key pages, no geo landing pages, 5–8 year old design."))
story.append(b("Stand-alone $8,997/mo; bundled saves $1,600/mo."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Peer accountability to make intake, staffing, and financial decisions as inbound leads start flowing."))
story.append(bd("Connects Scott with solo-to-CEO attorneys navigating the same transition he is about to make."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Solo, team under 5: Elite Coach Plus. Master's Circle requires 5+ dedicated staff."))
story.append(b("Revenue $1M+: Elite Coach Plus is the correct tier; Elite Coach is for sub-$400K."))
story.append(b("Stand-alone $3,497/mo; bundled saves $297/mo."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Scott Levine Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("2 cases/month at $50K avg from $3K conservative spend = ~$100K revenue, ~33x return."))
story.append(bd("9–10 cases/month at $50K avg from $12K aggressive spend = ~$500K revenue, ~42x return."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000/mo — channel minimums for construction defect in San Diego."))
story.append(b("<b>Aggressive:</b> $12,000/mo — Growth tier cap; full budget to saturate San Diego construction defect searches."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 2–3 cases x $50K avg = ~$100K–$150K/mo vs. $3K spend = ~33–50x return (estimated)."))
story.append(b("<b>Aggressive:</b> 9–10 cases x $50K avg = ~$450K–$500K/mo vs. $12K spend = ~38–42x return (estimated)."))
story.append(Paragraph("<i>All figures are estimates. Average case value estimated from $50M+ career results / 1,000+ clients. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Business Law minimums: PPC $1,500 + LSA $1,000 + Meta Retargeting $200 + Lead Gen $500 = $3,200 (rounded to $3,000)."))
story.append(b("<b>Aggressive:</b> $4M goal x 20% / 12 = $66,667. Tier 2 SD (1.3x) = $86,667. Growth cap = $12,000."))
story.append(b("Total at aggressive: $10,597 fees + $12,000 ads = $22,597/mo = 13.6% of $2M revenue. Under 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I get all my cases through referrals — I don\'t need marketing."', S["objection_q"]))
story.append(Paragraph("Artemis Law Group is 2 miles away with 89 reviews and dedicated geo pages. Every homeowner Googling 'construction defect attorney Solana Beach' who doesn't find Scott goes to them — today.", S["objection_a"]))

story.append(Paragraph('"I\'m a solo — I can only take so many cases anyway."', S["objection_q"]))
story.append(Paragraph("With consistent inbound, Scott chooses which cases to take. The first hire follows lead volume — the first 90 days build toward that transition.", S["objection_a"]))

story.append(Paragraph('"The price seems high for my size of firm."', S["objection_q"]))
story.append(Paragraph("$10,597/mo = 8% of a $2M revenue estimate — under the 35% cap. Two construction defect cases from paid marketing covers the full year of fees. Bundling saves $1,897/mo vs. standalone.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("Website rebuild, Google Ads, LSA, local SEO, Meta ads, monthly reporting.", S["price_detail"]),
     Paragraph("<strike>$8,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, practice area masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000–$12,000/mo", S["price_main"])],
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
    "Total: $10,597/mo + $3,000–$12,000 ad spend  |  Save $1,897/mo by bundling  |  8%–13.6% of revenue (under 35% cap)",
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
