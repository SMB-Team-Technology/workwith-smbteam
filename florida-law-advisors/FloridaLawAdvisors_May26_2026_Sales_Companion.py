"""
Sales Companion PDF — Florida Law Advisors
SMB Team  |  Rep: Jacob Meissner  |  May 26, 2026
Internal use only. Do not share with prospect.
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

OUTPUT_PATH = "florida-law-advisors/FloridaLawAdvisors_May26_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Florida Law Advisors", S["title"]))
story.append(Paragraph("Sales Companion  |  May 26, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Helbert Lopez, CEO", S["snap_value"]),
     Paragraph("Not confirmed (est. $400K–$1M)", S["snap_value"]),
     Paragraph("5 attorneys, 3 offices", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Tampa / Orlando / Dade City, FL", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM + SCALE", S["section"]))
story.append(Paragraph("Helbert wants a firm that runs itself — so he can pursue his outside business interests and build real wealth without the firm requiring his daily presence.", S["subsection"]))

# No transcript available — using inferred DBM from research
story.append(quote_block("No transcript available. DBM inferred from context: Helbert Lopez (CEO, Super Lawyers 2026) maintains a DC real estate investment email, signaling active outside ventures and a preference for a self-managing, scalable firm."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>A firm that grows without him.</b> Five attorneys and three offices should run without the CEO in every decision."))
story.append(bd("<b>Predictable paid lead flow.</b> A system that fills all three offices with qualified cases every month — no referral dependency."))
story.append(bd("<b>Freedom to invest elsewhere.</b> Real estate activity signals he is building wealth beyond the firm and needs it to fund itself."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No paid marketing.</b> Absent from Google Ads, LSA, and Meta — entire lead flow depends on organic and referrals."))
story.append(b("<b>3-pack invisibility.</b> Not in the local pack for family law, bankruptcy, or immigration in Tampa despite 100 reviews at 4.9 stars."))
story.append(b("<b>No management layer.</b> Three offices without accountability structure means owner dependency grows with the firm."))
story.append(b("<b>No profit visibility.</b> Revenue, margins, and cost per client are all unconfirmed."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds a multichannel lead flow — Google Ads, LSA, Meta — filling three offices without Helbert sourcing clients personally."))
story.append(bd("Activates the Spanish-language advantage already in the firm — 'Se Habla Espanol' and immigration become paid channels with lower CPL."))

story.append(Paragraph("<b>Full Service Marketing Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue est. $400K–$1M; Starter tier appropriate. Essentials hidden above $400K."))
story.append(b("2024 redesign is solid — CTA simplification and location pages needed, not full rebuild."))
story.append(b("Three GBP listings and review acquisition for Tampa, Orlando, and Dade City included."))
story.append(b("Spanish-language ad groups (family law + immigration) included — lower CPL, less competition."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Florida Law Advisors — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns a three-office firm from owner-managed to team-led — accountability structure, KPIs, and quarterly planning cadence."))
story.append(bd("Gives Helbert visibility into the firm without requiring his daily presence — the structure that makes his real estate focus possible."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Five attorneys and three offices — exactly the stage where coaching is the difference between scaling and fragmenting."))
story.append(b("No COO or management layer confirmed — coaching fills this gap with planning rhythm and accountability."))
story.append(b("Weekly coaching, practice area masterminds, quarterly workshops, and annual in-person summit included."))

story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Paid lead flow across family law, bankruptcy, and immigration — filling three offices without Helbert sourcing clients personally."))
story.append(bd("Gets into LSA and Google Ads before competitors further entrench quality score and review count advantages."))

story.append(Paragraph("<b>Range: $3,000–$5,000/mo  |  ROI estimates (defaults — no transcript):</b>", S["subsection"]))
story.append(b("<b>Conservative ($3,000):</b> ~10 leads x 15% = 1–2 cases x $3,500 = $3,500–$7,000/mo. ~2x return."))
story.append(b("<b>Aggressive ($5,000):</b> ~20 leads x 15% = 2–4 cases x $3,500 = $7,000–$14,000/mo. ~3x return."))
story.append(b("Conservative = PPC $1,500 + LSA $1,000 + Meta $500. Aggressive = Starter tier cap. Tampa Tier 2 (1.3x). Spanish 1.33x."))
story.append(Paragraph("<i>Estimates only. Actual results vary. Case values use practice area defaults — no transcript available.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We already have a website and referrals are working."', S["objection_q"]))
story.append(Paragraph("Referrals don't scale and don't fill three offices. All Family Law Group (155 reviews, ads + LSA) captures every Tampa search this firm misses. Referrals are a ceiling — not a growth strategy.", S["objection_a"]))

story.append(Paragraph('"I\'m not sure we\'re ready for paid ads."', S["objection_q"]))
story.append(Paragraph("Competitors holding Tampa's 3-pack and LSA slots — Gina Rosato (30 years), Robert Geller (7,000+ cases) — have entrenched quality score advantages. Every month of delay, they extend that lead. The window is open now.", S["objection_a"]))

story.append(Paragraph('"The budget feels large without knowing our revenue."', S["objection_q"]))
story.append(Paragraph("At est. $600K annual ($50K/mo), the $8,047 SMB fee is 16% of monthly revenue — well under 35%. Adding $3,000–$5,000 ad spend brings total to 22–26%. The math works even at conservative estimates.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, GBP optimization, website CTA optimization — 3 locations.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, masterminds, quarterly workshops, annual in-person summit.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000–$5,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $3,000–$5,000 ad spend  |  Save $1,147/mo by bundling  |  ~22–26% of est. monthly revenue (under 35% cap)",
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
