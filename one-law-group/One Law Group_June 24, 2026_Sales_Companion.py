"""
Sales Companion PDF — One Law Group
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

OUTPUT_PATH = "one-law-group/One_Law_Group_06242026_Sales_Companion.pdf"


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

story.append(Paragraph("One Law Group", S["title"]))
story.append(Paragraph("Sales Companion  |  June 24, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
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
    [Paragraph("Emanuel Abrishami", S["snap_value"]),
     Paragraph("$2.4M (2025)", S["snap_value"]),
     Paragraph("4–5 people", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (est.)", S["snap_value"]),
     Paragraph("Beverly Hills, CA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM &amp; LEGACY", S["section"]))
story.append(Paragraph("Emanuel wants to stop managing the office and return to rainmaking and litigation — building the $10M firm his reputation already warrants.", S["subsection"]))

story.append(quote_block("Growth is organic, driven by client referrals from successful litigation."))
story.append(Spacer(1, 1))
story.append(quote_block("$10M annually within 3 to 5 years — that is the goal."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Be the attorney again.</b> Rainmaking and litigation — not payroll and HR."))
story.append(bd("<b>$10M in 3–5 years.</b> Explicit goal; needs a system, not more personal effort."))
story.append(bd("<b>Cases that come to him.</b> Firm generates leads without every case needing a personal referral."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No paid marketing.</b> 100% referral-only; no digital presence; no scalable lead channel."))
story.append(b("<b>Owner runs operations.</b> Payroll, accounting, HR, admin — 50–70 hrs/week; 5 hrs left for rainmaking."))
story.append(b("<b>3-pack invisible.</b> ~120 reviews vs. Omega Law Group's 641 — not appearing for Beverly Hills PI searches."))
story.append(b("<b>No intake protocol.</b> No after-hours coverage; fast competitors sign cases Emanuel could have won."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Generates PI leads from Beverly Hills searches without depending on Emanuel's personal relationships."))
story.append(bd("Puts One Law Group in front of accident victims before they call Omega Law Group or The Dominguez Firm."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $7,397/mo bundled</b>", S["subsection"]))
story.append(b("PI requires minimum Starter tier; Growth is appropriate at $2.4M revenue."))
story.append(b("Beverly Hills Tier 1 market — competitors spending $40K–$150K/mo; Growth supports up to $40K ad spend."))
story.append(b("No existing digital infrastructure — website, Google Ads, LSA, Meta, and SEO all needed from scratch."))
story.append(b("Spanish-language campaign matches Emanuel's bilingual staff and LA market footprint."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the intake and team systems that free Emanuel from day-to-day operational management."))
story.append(bd("Moves One Law Group from Stage 4 to Stage 5 — firm grows without Emanuel doing everything himself."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1M+, team under 5: Master's Circle requires 5+ dedicated staff — Elite Coach Plus is correct tier."))
story.append(b("Weekly coaching + PI mastermind addresses intake gaps, team delegation, and profit planning in parallel."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("One Law Group — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Generates qualified Beverly Hills PI leads at a predictable cost — turning a referral-only firm into a marketing-driven one."))
story.append(bd("Conservative: est. 3 cases/mo x $50K avg fee = $150K revenue vs. $10K spend = ~15x return (estimate)."))

story.append(Paragraph("<b>Recommended Ad Spend:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $10,000/mo — Google Ads $7K + LSA $1.5K + Meta $1.5K (Tier 1 PI minimums)."))
story.append(b("<b>Aggressive:</b> $40,000/mo — $2.4M x 20% / 12 = $40K; at Growth tier cap."))
story.append(b("<b>Aggressive ROI est.:</b> ~15 cases x $50K = $750K/mo vs. $40K spend = ~19x return (estimate)."))
story.append(b("Total aggressive SMB spend: $50,597/mo = 25.3% of monthly revenue — under 35% cap."))
story.append(Paragraph("<i>All projections are estimates. Not guaranteed. Case value = estimated PI contingency fee.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We have grown to $2.4M without advertising — why change now?"', S["objection_q"]))
story.append(Paragraph("That growth is capped at Emanuel's personal capacity. Omega has 641 reviews and full digital coverage for the same searches. The $10M goal requires a system — referrals alone cannot get there.", S["objection_a"]))

story.append(Paragraph('"I do not have time to manage a marketing program."', S["objection_q"]))
story.append(Paragraph("SMB Team manages everything. Emanuel does not run the campaigns. The coaching program is specifically designed to reduce his operational load, not add to it.", S["objection_a"]))

story.append(Paragraph('"What if the leads are not quality PI cases?"', S["objection_q"]))
story.append(Paragraph("LSA pays per qualified lead from people actively searching for a PI attorney. Emanuel's 5.0 stars and Super Lawyers credentials qualify him for top LSA placement — targeting high-value terms like wrongful death and motorcycle accidents.", S["objection_a"]))

story.append(Paragraph('"The investment is significant."', S["objection_q"]))
story.append(Paragraph("One additional PI case per month at $50K avg fee more than covers the full $10,597/mo management cost. Conservative ad spend projection is ~$150K/mo in revenue on $10K spend.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, local SEO, website optimization.", S["price_detail"]),
     Paragraph("<strike>$8,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, PI mastermind, quarterly + annual workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$10,000–$40,000/mo", S["price_main"])],
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
    "Total: $10,597/mo + $10,000–$40,000 ad spend  |  Save $1,897/mo by bundling  |  25.3% of revenue at aggressive (under 35% cap)",
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
