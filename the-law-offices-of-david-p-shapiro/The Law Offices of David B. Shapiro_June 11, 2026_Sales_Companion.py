"""
Sales Companion PDF — The Law Offices of David B. Shapiro
June 11, 2026 | Rep: Jacob Meissner
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

OUTPUT_PATH = "the-law-offices-of-david-p-shapiro/The_Law_Offices_of_David_B_Shapiro_06112026_Sales_Companion.pdf"


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
    """Dark bullet for transformation statements and what he wants."""
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

story.append(Paragraph("The Law Offices of David B. Shapiro", S["title"]))
story.append(Paragraph("Sales Companion  |  June 11, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("David B. Shapiro", S["snap_value"]),
     Paragraph("$15K–$70K/mo (lumpy)", S["snap_value"]),
     Paragraph("3–5 support", S["snap_value"]),
     Paragraph("Stage 3: Solo Practitioner", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Baltimore, MD", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM / TIME", S["section"]))
story.append(Paragraph("David wants to stop being the firm and start owning it — Maine summers, the restaurant, and showing up only when he chooses.", S["subsection"]))

story.append(quote_block("I'm getting calls at 2 in the morning."))
story.append(Spacer(1, 1))
story.append(quote_block("I have a C or D team. I need an A team."))
story.append(Spacer(1, 1))
story.append(quote_block("I need to be able to delegate about 80% of what I do."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Build an A-team.</b> 80% of his 60–70 hr/week is delegable — he needs people he can actually trust."))
story.append(bd("<b>Stop the 2 AM calls.</b> Late-night intake is time stolen from Maine, the restaurant, and working by choice."))
story.append(bd("<b>$100K/month.</b> The backlog is already there — he just needs team capacity to unlock it."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>C or D team.</b> No one he can fully delegate to — every important task still flows through David personally."))
story.append(b("<b>No intake system.</b> Personally handling all calls including 2 AM arrests — no backup, no after-hours coverage."))
story.append(b("<b>Broken website.</b> TLS cert error = security warning before prospects read a word; turns referrals into lost cases."))
story.append(b("<b>Zero digital presence.</b> 100% referral-dependent; LegalMatch contract is signed but never activated — $1,500/mo generating zero leads."))
story.append(b("<b>Backlog locked.</b> 150 PI cases ($3.75M+ potential) cannot resolve faster without team capacity."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Adds a digital pipeline alongside referrals — revenue continues even when David steps back."))
story.append(bd("Fixes the broken website so earned referrals convert instead of bouncing on a security warning."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("PI practice eliminates Essentials; Starter is the minimum qualifying tier."))
story.append(b("Revenue $400K–$1M → Starter tier. Baltimore = Tier 4 market."))
story.append(b("Includes website rebuild (TLS cert failure; site age; no mobile confirmation)."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the A-team structure — accountability, delegation framework, management layer so David stops doing the 80% he called delegable."))
story.append(bd("Replaces the 2 AM call habit with a documented intake process and after-hours coverage that runs without him."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M, team &lt;5, no dedicated ops → Elite Coach Plus is the correct tier."))
story.append(b("FCOO Advisor not yet appropriate — coaching builds the foundation first; upgrade once $75K+ months are consistent."))
story.append(b("Directly addresses David's three stated needs: team, intake, and financial predictability."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("David B. Shapiro — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("4–15 new PI and criminal defense cases/month from digital search, independent of David's personal activity."))
story.append(bd("LSA places firm at the very top of Google for the highest-intent Baltimore searches — pay-per-lead, not pay-per-click."))

story.append(Paragraph("<b>Ad Spend Range  |  Conservative: $7,500/mo  |  Aggressive: $25,000/mo</b>", S["subsection"]))
story.append(b("<b>Conservative ROI (est):</b> ~4 cases x $5,500 = $22,000/mo vs. $7,500 spend = ~3x return."))
story.append(b("<b>Aggressive ROI (est):</b> ~15 cases x $5,500 = $82,500/mo vs. $25,000 spend = ~3.3x return."))
story.append(b("<b>How conservative was calculated:</b> PI PPC $2,000 + Criminal PPC $2,500 + LSA $2,000 + Meta $1,000 = $7,500."))
story.append(b("<b>How aggressive was calculated:</b> $100K/mo goal x 20% = $20,000. Reverse math (121 leads x $240 CPL) = $29,040; rounded to $25,000. Note: exceeds Starter $8K cap — discuss Growth tier if committing to aggressive."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I just need to hire — marketing can wait."', S["objection_q"]))
story.append(Paragraph("Marketing funds the team. 4 extra PI cases/mo at $5,500 = $22K — covers full SMB investment and nets $14K. Revenue enables the hire.", S["objection_a"]))

story.append(Paragraph('"LegalMatch is already costing me $1,500/month."', S["objection_q"]))
story.append(Paragraph("That contract is signed and paid — but never activated. $0 incremental cost to turn it on. It is the only lead source David is paying for and not using.", S["objection_a"]))

story.append(Paragraph('"Revenue is too inconsistent for a monthly commitment."', S["objection_q"]))
story.append(Paragraph("The inconsistency is the symptom. 150 PI cases worth $3.75M+ are locked by team capacity — coaching unlocks that backlog, which dwarfs the monthly investment.", S["objection_a"]))

story.append(Paragraph('"Referrals have worked for 37 years."', S["objection_q"]))
story.append(Paragraph("Referrals stop when David steps back — the opposite of what he wants. Bob Katz (190+ reviews) and Seth Okin (212 reviews) are compounding digital advantages daily. Every month without digital presence makes this gap harder to close.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, SEO, Meta Ads, website rebuild — full digital lead gen system.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, intake build-out, A-team framework, profit plan, workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,500–$25,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $7,500–$25,000 ad spend  |  Save $1,147/mo by bundling  |  ~32.7%–69.6% of revenue (conservative end within 35% cap at $570K effective)",
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
