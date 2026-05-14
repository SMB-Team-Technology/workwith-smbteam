"""
Sales Companion PDF — Law Offices of Mark Daniel Melnick
Generated: April 15, 2026 | Rep: Dan Bryant
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

OUTPUT_PATH = "/home/user/workwith-smbteam/melnick-defense/Law_Offices_of_Mark_Daniel_Melnick_04152026_Sales_Companion.pdf"


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
    textColor=ACCENT_GREEN, spaceBefore=4, spaceAfter=1)
S["subsection"] = ParagraphStyle(
    "subsection", fontName="Helvetica-Bold", fontSize=10, leading=13,
    textColor=DARK_NAVY, spaceBefore=1, spaceAfter=0)
S["bullet"] = ParagraphStyle(
    "bullet", fontName="Helvetica", fontSize=9.5, leading=12,
    textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0,
    spaceBefore=0, spaceAfter=0)
S["bullet_dark"] = ParagraphStyle(
    "bullet_dark", fontName="Helvetica", fontSize=9.5, leading=12,
    textColor=DARK_NAVY, leftIndent=12, bulletIndent=0,
    spaceBefore=0, spaceAfter=0)
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


# ── PAGE 1 ──
story = []

story.append(Paragraph("Law Offices of Mark Daniel Melnick", S["title"]))
story.append(Paragraph("Sales Companion  |  April 15, 2026  |  Rep: Dan Bryant", S["subtitle"]))
story.append(thin_rule())

# Prospect Snapshot
story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Dan Melnick", S["snap_value"]),
     Paragraph("Est. $200K–$400K", S["snap_value"]),
     Paragraph("Solo (1)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("~15% (default)", S["snap_value"]),
     Paragraph("Van Nuys, CA", S["snap_value"])],
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

# DBM
story.append(Paragraph("Dominant Buying Motive: AUTOPILOT AND PROFIT", S["section"]))
story.append(Paragraph(
    "Dan wants to build a firm that runs without him — hand it off to a younger attorney, collect passive income, and retire on his terms after 44 years of building it.",
    S["subsection"]))

story.append(quote_block("autopilot and profit"))
story.append(Spacer(1, 1))
story.append(quote_block("I want to stop taking long, complex trials. I want cases near San Fernando and Burbank — not Ventura."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Case mix shift.</b> Only misdemeanor and DUI near San Fernando/Burbank courts — no lengthy felony trials or distant venues."))
story.append(bd("<b>4-day work week.</b> Reduce personal involvement in the firm within 12 months of starting the build."))
story.append(bd("<b>An associate who runs the cases.</b> Hire a full-time attorney who takes full case responsibility so Dan can step back."))
story.append(bd("<b>Passive retirement income.</b> A firm that earns whether or not Dan is in the courtroom — and has transferable value he can eventually sell."))

story.append(Spacer(1, 1))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Ads currently dark.</b> Both channels paused since the malware incident; new campaign about to launch with Belugol (Anna)."))
story.append(b("<b>Legacy $300K Google Ads debt.</b> Nearly paid off but creates financial caution and limits immediate investment appetite."))
story.append(b("<b>Office + security disruption.</b> Building fire (March 2026), computer hack, and website malware (since cleared) all hit simultaneously."))
story.append(b("<b>\"Wait two weeks.\"</b> Wants to see Anna's ad results before committing to additional services."))

story.append(thin_rule())

# Marketing Package
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Rebuilds the lead engine with Burbank and San Fernando landing pages targeting exactly the misdemeanor and DUI case mix Dan wants."))
story.append(bd("Full attribution and budget controls from day one — prevents a repeat of the unmonitored campaign that accumulated the $300K debt."))
story.append(bd("NAP correction and local SEO means the firm appears for clients searching right now — not just the ones Dan personally reaches."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Criminal Defense + High market → Essentials tier eliminated; Starter is the minimum eligible tier."))
story.append(b("Website rebuild required: older WordPress build, malware long-tail suppression, no geo-landing pages — must use Full Service (not ads-only)."))
story.append(b("Starter ad spend cap: $3,000/mo — aligns exactly with Criminal Defense High market $3,000 minimum floor."))
story.append(b("Saves $850/mo vs. $5,697/mo stand-alone."))

story.append(thin_rule())

# Coaching Package
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns the \"autopilot and profit\" goal into a 12-to-18-month plan with accountable milestones — not a vague aspiration."))
story.append(bd("Group sessions with attorneys at similar stage provide peer accountability and real-world implementation models."))
story.append(bd("KPI framework defines exactly when the firm is ready to hire an associate and when Dan can step back."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue est. $200K–$400K → Elite Coach is the correct tier; Elite Coach Plus requires $400K+."))
story.append(b("Solo, no team → Master's Circle eliminated; no dedicated ops staff → Fractional COO not applicable."))
story.append(b("Saves $897/mo vs. $3,497/mo stand-alone."))


# ── PAGE 2 ──
story.append(PageBreak())

story.append(Paragraph("Melnick Defense — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# Ad Spend
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Generates the steady DUI and misdemeanor leads needed to build the case volume and team structure before Dan can step back."))
story.append(bd("Full tracking and attribution from day one — every dollar accountable; no campaigns running unchecked."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000/mo — at Starter tier cap; meets Criminal Defense High market minimum floor."))
story.append(b("<b>Aggressive:</b> $4,500/mo — Growth tier territory; requires upgrade or 10% overage fee above Starter cap."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~2 cases x $4,000 ACV = $8,000/mo vs. $3,000 spend = 2.7x return."))
story.append(b("<b>Aggressive:</b> ~4 cases x $4,000 ACV = $16,000/mo vs. $4,500 spend = 3.6x return."))
story.append(Paragraph("<i>ACV = $4,000 (DUI/misdemeanor LA default). Close rate = 15% (default). All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(b("<b>How calculated:</b> Criminal Defense High minimums: PPC $1,500 + LSA $900 + Meta $600 = $3,000 conservative. Aggressive: $600K goal x 20% ÷ 12 x Tier 1 (1.5x) − fee = $10,153; capped at $4,500."))
story.append(b("At $400K revenue: $7,447 + $3,000 = $10,447 = 31.3% of monthly revenue — within 35% cap. Verify actual revenue on April 29 call."))

story.append(thin_rule())

# Objections
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"Let\'s wait two weeks to see results from Anna\'s new campaign."', S["objection_q"]))
story.append(Paragraph(
    "SMB Team isn't competing with Anna. Two weeks of ad data won't fix the outdated NAP, the underperforming website, or the missing intake system. Leads are being lost right now. The coaching and website build can start in parallel today.",
    S["objection_a"]))

story.append(Paragraph('"I\'m cautious about spending after the $300K Google Ads debt."', S["objection_q"]))
story.append(Paragraph(
    "That debt came from campaigns running without oversight. Starter includes monthly reporting, budget controls, and attribution from day one. Elite Coach ($2,600/mo) is entirely separate from ad spend — the two don't conflict.",
    S["objection_a"]))


story.append(thin_rule())

# Investment
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild + Google Ads + LSA + local SEO + reporting.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching + masterminds + workshops + KPI accountability.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000–$4,500/mo", S["price_main"])],
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
    "Total management: $7,447/mo  |  Save $1,747/mo by bundling  |  +$3,000/mo ad spend = $10,447/mo total (31.3% of est. $400K revenue — within 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
