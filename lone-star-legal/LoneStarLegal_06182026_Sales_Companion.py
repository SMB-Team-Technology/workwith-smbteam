"""
Sales Companion PDF — Lone Star Legal
SMB Team Internal Document — DO NOT SHARE
Sales Rep: Nick Holderman | Date: June 18, 2026
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

OUTPUT_PATH = "lone-star-legal/LoneStarLegal_06182026_Sales_Companion.pdf"


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

story.append(Paragraph("Lone Star Legal (Kelly Law Firm, P.C.)", S["title"]))
story.append(Paragraph("Sales Companion  |  June 18, 2026  |  Rep: Nick Holderman", S["subtitle"]))
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
    [Paragraph("Robbye Kelly", S["snap_value"]),
     Paragraph("~$570K est.", S["snap_value"]),
     Paragraph("9 staff", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("Georgetown, TX", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SYSTEMS &amp; MARKET DOMINANCE", S["section"]))
story.append(Paragraph("Robbye wants predictable case flow and a firm that runs itself — before regional firms fully capture Georgetown.", S["subsection"]))
story.append(quote_block("No discovery transcript provided. DBM inferred: Board Certified PI firm with 9 staff, Georgetown market, and no digital marketing = owner who wants visibility and systems, not more referral-dependent growth."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable leads.</b> Know how many cases are coming in next month before the month starts."))
story.append(bd("<b>Market position.</b> Be the first result Georgetown accident victims see — not Angel Reyes or Carlson Law."))
story.append(bd("<b>Operational independence.</b> Team and CEO manage day-to-day; partners focus on cases and strategy."))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No paid advertising.</b> Invisible on Google Ads, LSA, and Meta while competitors with 400–790+ reviews dominate."))
story.append(b("<b>Review gap.</b> Angel Reyes: 790+ reviews; Carlson: 408. Lone Star Legal's count unconfirmed but appears far lower."))
story.append(b("<b>NAP inconsistency.</b> FindLaw shows old address; dual business names suppress local rankings."))
story.append(b("<b>Revenue unconfirmed.</b> HubSpot range $180K–$960K — confirm on call to validate tier and ad spend scale."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("<b>Top of Google.</b> Puts LSL above Angel Reyes and Carlson for Georgetown PI searches via Ads + LSA."))
story.append(bd("<b>Compounds over time.</b> NAP fix + review velocity + GBP optimization widen the local SEO gap vs. competitors."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("PI practice requires minimum Starter tier — Essentials ineligible for personal injury firms."))
story.append(b("Georgetown is high-competition PI market (urgency 7/10); Starter + $10K–$25K ad spend is correct entry."))
story.append(b("Stand-alone: $5,697/mo. Bundle saves $850/mo vs. stand-alone."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("<b>Accountability.</b> Weekly targets for cases, intake conversion, and team performance — not set-and-forget."))
story.append(bd("<b>Peer network.</b> PI firm owners at the same stage sharing what is working in their markets right now."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M, 9 staff — Elite Coach Plus correct tier. FCOO Advisor available in Phase 2."))
story.append(b("Includes weekly group coaching, PI mastermind, quarterly workshops, annual in-person event."))
story.append(b("Stand-alone: $3,497/mo. Bundle saves $297/mo. No transcript — lead with market urgency and competitor review gap."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Lone Star Legal — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("<b>Immediate lead flow.</b> Ads generate qualified PI leads from Georgetown searches within 30 days of launch."))
story.append(bd("<b>3–11 cases/month.</b> Conservative scenario: 3 cases x $7,500 = $22,500 revenue vs. $10K spend = 2.3x return."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $10,000/mo — PI high-competition hard floor; Google Ads + LSA only."))
story.append(b("<b>Aggressive:</b> $25,000/mo — Starter tier cap; adds Meta retargeting and cold audiences."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~19 leads x 15% = 3 cases x $7,500 = $22,500/mo. Return: 2.3x. (Estimates only.)"))
story.append(b("<b>Aggressive:</b> ~72 leads x 15% = 11 cases x $7,500 = $82,500/mo. Return: 3.3x. (Estimates only.)"))
story.append(Paragraph("<i>Default case value $7,500 (PI/MVA). LSL catastrophic/offshore cases may be significantly higher. All figures estimates.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> PI high-competition floor $10K. Google $7K ($846 CPL +20%) + LSA $3K ($282 CPL +20%) = 19 leads."))
story.append(b("<b>Aggressive:</b> 2x revenue goal ($1.14M) x 20% / 12 x 1.15 geo = $21,850. Minus fee = $17K. Reverse math $47K (cap). Capped at $25K."))
story.append(b("Conservative total SMB spend: $18,047/mo. Confirm revenue — at $700K+ this is under 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"We already have a strong reputation — why do we need to spend on ads?"', S["objection_q"]))
story.append(Paragraph("Angel Reyes has 790+ reviews and a Georgetown landing page; Carlson Law has 408 reviews and is 8 miles away. LSL is not appearing in the local 3-pack for Georgetown PI searches despite having a Board Certified attorney on staff. The reputation exists — the visibility does not.", S["objection_a"]))

story.append(Paragraph('"We are not sure the budget works right now."', S["objection_q"]))
story.append(Paragraph("Conservative model: 3 cases/month at $7,500 avg = $22,500 new revenue covers the full $18,047 investment (fees + ad spend) in month one. One catastrophic or offshore case changes the math entirely — those settle for $100K–$500K+.", S["objection_a"]))

story.append(Paragraph('"We need to confirm our revenue number first."', S["objection_q"]))
story.append(Paragraph("Confirm on the call. HubSpot shows $180K–$960K. With 9 staff and a Board Certified PI attorney, revenue is almost certainly above $400K and the Starter tier stands. If confirmed at $700K+, conservative ad spend ($10K) is comfortably under the 35% cap.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, local SEO, Meta, website management.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, PI mastermind, quarterly + annual workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$10,000–$25,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $10,000–$25,000 ad spend  |  Save $1,147/mo by bundling  |  Confirm revenue on call — at $700K+ conservative spend is under 35% cap",
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
