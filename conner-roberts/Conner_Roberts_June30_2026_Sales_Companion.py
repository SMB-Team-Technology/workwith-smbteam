"""
Sales Companion PDF — Conner & Roberts, PLLC
SMB Team | Jonathan Farace | June 30, 2026
Internal document. Do not share with prospect.
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

DARK_NAVY = HexColor("#1a2332")
ACCENT_GREEN = HexColor("#3B6D11")
MEDIUM_GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#888888")
RULE_GRAY = HexColor("#CCCCCC")
QUOTE_BG = HexColor("#F5F7F0")
WHITE = HexColor("#FFFFFF")
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "conner-roberts/Conner_Roberts_06302026_Sales_Companion.pdf"


def add_page_elements(canvas, doc):
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

S = {}
S["title"] = ParagraphStyle(
    "title", fontName="Helvetica-Bold", fontSize=16, leading=20,
    textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle(
    "subtitle", fontName="Helvetica", fontSize=9.5, leading=13,
    textColor=LIGHT_GRAY, spaceAfter=3)
S["section"] = ParagraphStyle(
    "section", fontName="Helvetica-Bold", fontSize=11, leading=15,
    textColor=ACCENT_GREEN, spaceBefore=5, spaceAfter=1)
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

story.append(Paragraph("Conner &amp; Roberts, PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  June 30, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Amelia Roberts &amp; Lisa Conner", S["snap_value"]),
     Paragraph("$2M+ (2025); $3M+ (2026 est.)", S["snap_value"]),
     Paragraph("10 total", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Chattanooga, TN", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.7*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 3))

story.append(Paragraph("Dominant Buying Motive: SCALE AND SELL", S["section"]))
story.append(Paragraph("Build a firm that runs without them, grows predictably, and holds real value as a sellable asset over 10 years.", S["subsection"]))

story.append(quote_block("Build a scalable, sellable firm asset over 10 years, allowing partners to transition from practicing attorneys to business owners."))
story.append(Spacer(1, 1))
story.append(quote_block("Lisa is working 60+ hours a week — taking work home nightly — and spending 10-20 hours per week on manual retainer collection alone."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Freedom from the day-to-day.</b> Own a firm that runs without their constant presence."))
story.append(bd("<b>A sellable asset.</b> A 10-year exit with a firm a buyer pays a premium to acquire."))
story.append(bd("<b>Systems that replace partner time.</b> Collections, document review, and admin belong to AI — not the founders."))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No paid lead generation.</b> Zero Google Ads, LSA, or Meta — every paid lead goes to competitors."))
story.append(b("<b>Manual collections absorbing 10-20 hrs/week.</b> Highest-cost resource running a billing process AI can handle."))
story.append(b("<b>No operational leadership layer.</b> Both partners fill every management gap with no COO or manager in place."))
story.append(b("<b>NAP inconsistencies.</b> Three phone numbers and two addresses suppress local 3-pack rankings."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Turns organic-only case volume into a paid + organic engine — the predictable lead flow a sellable firm is built on."))
story.append(bd("Puts 102 Google reviews to work in LSA — placing the firm above every paid ad and organic result for family law searches."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $7,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $2M+ confirmed 2025; $3M+ projected 2026. Growth tier applies. Revisit Platinum at renewal if 2026 confirms $3M+."))
story.append(b("Family law, Chattanooga TN (Tier 4). No PI filter. Conservative ad spend $3,500/mo; aggressive cap $14,000/mo (Growth tier)."))
story.append(b("102 reviews at 4.7 stars = immediate LSA eligibility. Content strategy restarts blog inactive since January 2025."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Peer accountability from attorneys who have built what Amelia and Lisa are building — structure for the 10-year exit plan."))
story.append(bd("Embedded exit planning curriculum and KPI tracking to build financial visibility a buyer would pay to acquire."))

story.append(Paragraph("<b>Master's Circle  |  $4,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1M+, team 10 total. Verify at least one support staff in ops/intake role for eligibility confirmation."))
story.append(b("Firm deferred FCOO on call — partners handle ops once freed from caseload. No FCOO add-on required at this stage."))
story.append(b("Family law practice mastermind included; exit planning coaching embedded — directly supports 10-year sellable asset DBM."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Conner &amp; Roberts — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This AI Workforce Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("<b>Returns 10-20 hrs/week to Lisa</b> — manual collections automated; she stops taking work home."))
story.append(bd("<b>Eliminates partner document review</b> for uncontested divorce — AI handles screening, attorney signs off."))

story.append(Paragraph("<b>AI Accelerator L2 (Fractional CTO Level 2)  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("Agreed to on call at $5,799/mo (standalone). Bundled saves $800/mo. 12-month commitment confirmed."))
story.append(b("ESCALATION: Confirm LAW delivery launched and capacity available before July 10 proposal call."))
story.append(b("Scope: AI workflows for document generation, retainer invoicing, and client communications."))

story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Conservative $3,500/mo: est. 3 cases x $8,750 avg = $26,250/mo revenue. 7.5x return on ad spend."))
story.append(bd("Aggressive $14,000/mo: est. 17 cases x $8,750 avg = $148,750/mo revenue. 10x return on ad spend."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — PPC $1,500 + LSA $1,000 + Meta $1,000. Absolute minimum floor."))
story.append(b("<b>Aggressive:</b> $14,000/mo — Growth tier cap. $5M goal x 20% / 12 = $83,333; capped at $14,000."))
story.append(b("At aggressive: $30,994 total spend = 11.6% of monthly revenue. Well under 35% cap."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Close rate defaulted to 15% — not stated on call.</i>", S["disclaimer"]))

story.append(thin_rule())

story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"We already have 40-50 cases/month — do we really need ads?"', S["objection_q"]))
story.append(Paragraph("Every case you have came from organic — not a system you control. Horton Ballard Pemerton is in your paid search space. Ryan Hanzelik is building toward a perfect 5.0. One paid case per month more than covers the monthly marketing fee.", S["objection_a"]))

story.append(Paragraph('"We agreed to the Fractional CTO — why do we need marketing too?"', S["objection_q"]))
story.append(Paragraph("The CTO returns partner hours. Marketing controls how much volume comes in. Both serve the same goal — a firm that runs itself and grows predictably. Neither works as well without the other.", S["objection_a"]))

story.append(Paragraph('"The price is higher than we expected."', S["objection_q"]))
story.append(Paragraph("$16,994/mo in SMB fees is 6.4% of confirmed 2025 monthly revenue ($22,222). One additional Google Ads case per month — at $8,750 avg — offsets the full marketing fee. The 35% revenue cap allows up to $93,333/mo; you are at 6.4%.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, SEO, website optimization.", S["price_detail"]),
     Paragraph("<strike>$8,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle</b>", S["price_main"]),
     Paragraph("$4,600/mo", S["price_main"])],
    [Paragraph("Weekly coaching, masterminds, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$4,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>AI Accelerator L2 (Fractional CTO Level 2)</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("Collections, doc generation, client comms automation.", S["price_detail"]),
     Paragraph("<strike>$5,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,500–$14,000/mo", S["price_main"])],
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
    ("LINEBELOW", (0,7), (-1,7), 0.5, RULE_GRAY),
]))
story.append(pt)
story.append(Paragraph(
    "Total: $16,994/mo + $3,500–$14,000 ad spend  |  Save $2,797/mo by bundling  |  6.4%–11.6% of revenue (under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
