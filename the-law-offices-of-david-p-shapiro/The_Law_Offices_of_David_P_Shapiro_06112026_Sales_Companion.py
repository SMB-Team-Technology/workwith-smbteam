"""
Sales Companion PDF — The Law Offices of David P. Shapiro
SMB Team | June 11, 2026 | Rep: Jacob Meissner
FOR INTERNAL USE ONLY — DO NOT SHARE WITH CLIENT
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

OUTPUT_PATH = "the-law-offices-of-david-p-shapiro/The_Law_Offices_of_David_P_Shapiro_06112026_Sales_Companion.pdf"


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
S["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=9, leading=12, textColor=LIGHT_GRAY, spaceAfter=2)
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=ACCENT_GREEN, spaceBefore=5, spaceAfter=1)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=DARK_NAVY, spaceBefore=1, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=10, bulletIndent=0, spaceBefore=1, spaceAfter=0)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=10, bulletIndent=0, spaceBefore=1, spaceAfter=0)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9, leading=11, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=1)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8, leading=10, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=2)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=0)


def b(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY, spaceBefore=2, spaceAfter=2)

def quote_block(text):
    p = Paragraph(f'"{text}"', S["quote"])
    t = Table([[p]], colWidths=[6.5 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), QUOTE_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


# ══════════════════════════════════════════════════════════
# PAGE 1
# ══════════════════════════════════════════════════════════
story = []

story.append(Paragraph("The Law Offices of David P. Shapiro", S["title"]))
story.append(Paragraph("Sales Companion  |  June 11, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]), Paragraph("<b>Revenue</b>", S["snap_label"]), Paragraph("<b>Team</b>", S["snap_label"]), Paragraph("<b>Stage</b>", S["snap_label"]), Paragraph("<b>Close Rate</b>", S["snap_label"]), Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("David Shapiro", S["snap_value"]), Paragraph("$15K–$70K/mo", S["snap_value"]), Paragraph("Solo + C/D team", S["snap_value"]), Paragraph("Stage 3", S["snap_value"]), Paragraph("15% (default)", S["snap_value"]), Paragraph("Baltimore, MD", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.1*inch, 1.1*inch, 0.9*inch, 0.75*inch, 0.75*inch, 1.1*inch])
t1.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("TOPPADDING",(0,0),(-1,-1),1),("BOTTOMPADDING",(0,0),(-1,-1),1),("LEFTPADDING",(0,0),(-1,-1),0),("LINEBELOW",(0,1),(-1,1),0.5,RULE_GRAY)]))
story.append(t1)
story.append(Spacer(1, 3))

story.append(Paragraph("Dominant Buying Motive: FREEDOM", S["section"]))
story.append(Paragraph("Wants to stop being the Chief Everything Officer — Maine home, restaurant venture, and a firm that runs without him.", S["subsection"]))

story.append(quote_block("Highly variable — $15K–$70K/month currently"))
story.append(Spacer(1, 1))
story.append(quote_block("C or D team"))
story.append(Spacer(1, 1))
story.append(quote_block("disorganized intake missing weekend PI/criminal cases"))
story.append(Spacer(1, 1))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>A team to delegate to.</b> Estimates 80% of his work is delegable — has no one to delegate it to."))
story.append(bd("<b>Maine home + restaurant.</b> Specific personal goals that require time and bandwidth he does not have."))
story.append(bd("<b>$100K/month from the backlog.</b> 150 active PI cases are already in the pipeline — he wants to extract that revenue."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>C or D team.</b> His own words — staff cannot carry 150 PI cases plus criminal defense without him."))
story.append(b("<b>No intake process.</b> He handles every call personally including 2 a.m. — no protocol, no backup."))
story.append(b("<b>Revenue variability.</b> $55K monthly swing makes team investment and planning impossible."))
story.append(b("<b>Zero digital presence.</b> No ads, no LSA; website throws a security warning on HTTPS."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Fixes the website so every referral and paid click lands on a working site — not a security warning."))
story.append(bd("Google Ads and LSA put the firm in front of Baltimore PI and criminal defense leads 24/7."))
story.append(bd("Review generation closes the gap with Hassan/Tuchman (385) and Seth Okin (212) over time."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("PI is the primary practice area — PI requires minimum Starter; Essentials not available."))
story.append(b("Website rebuild required — expired TLS, outdated content, no above-the-fold CTA."))
story.append(b("Baltimore Tier 2 — PI CPCs $100–$250; criminal defense $75–$200; Starter covers both."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds delegation systems so David can stop carrying 80% of the firm's operational work personally."))
story.append(bd("Creates the management layer that lets the firm advance 150 PI cases without his daily involvement."))
story.append(bd("Turns the $100K/month goal from a wish into a plan with systems and accountability behind it."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue band $400K–$1M any team — Elite Coach Plus is the correct coaching tier."))
story.append(b("Primary problem is operational — coaching is the lead engagement; marketing is the accelerator."))
story.append(b("Revenue under $500K certainty — FCOO Advisor excluded; coaching-only is correct now."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("David P. Shapiro — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Generates measurable PI and criminal defense leads 24/7 — independent of whether someone knows David personally."))
story.append(bd("Replaces the $55K monthly revenue swing with a system that produces predictable lead volume."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,500/mo — PI Google Ads $3,500 + LSA $2,000 + Meta $1,200 + criminal defense $800."))
story.append(b("<b>Aggressive:</b> $25,000/mo — full $100K/month revenue goal pursuit; Growth tier upgrade discussion needed."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 25 leads x 15% close = ~3 cases x $6,500 = ~$23K/mo vs. $7,500 spend = 3.1x return."))
story.append(b("<b>Aggressive:</b> 100 leads x 15% close = 15 cases x $6,500 = ~$97K/mo vs. $25K spend = 3.9x return."))
story.append(Paragraph("Estimates only. PI cases often exceed $6,500 default — TBI and wrongful death resolve significantly higher.", S["disclaimer"]))

story.append(Paragraph("<b>Cap check:</b>", S["subsection"]))
story.append(b("At $70K/mo revenue: $8,047 + $25,000 = $33,047 = 47% — exceeds 35% cap. Confirm revenue before aggressive scenario."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I don\'t have the budget right now — revenue is too variable."', S["objection_q"]))
story.append(Paragraph("The variability IS the problem. Elite Coach Plus pays for itself if it advances one extra case per month from the 150 already in the pipeline. The 35% cap is fine at $8,047/mo alone (16.9% of $47K average).", S["objection_a"]))

story.append(Paragraph('"My main problem is the team, not marketing."', S["objection_q"]))
story.append(Paragraph("Agreed — that is why Elite Coach Plus is the primary engagement. Marketing is the infrastructure that will be ready when the team is. Starting both now eliminates the gap between readiness and launch.", S["objection_a"]))

story.append(Paragraph('"38 years and a Supreme Court victory — I already have credibility."', S["objection_q"]))
story.append(Paragraph("The credentials are real — they do not appear in Google results. Hassan/Tuchman: 385 reviews vs. 85. Seth Okin: AVVO 10.0 vs. 6.7. Every prospect who can't find a referral is choosing them — not because they are better, but because they show up first.", S["objection_a"]))

story.append(Paragraph('"I need to figure out the office manager situation first."', S["objection_q"]))
story.append(Paragraph("That situation is what coaching fixes — the whole firm depending on one admin is the problem coaching addresses first. Building backup coverage and documented processes starts in week one.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]), Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, Google Ads, LSA, GBP management, review generation.", S["price_detail"]), Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]), Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, practice area masterminds, quarterly workshops, annual in-person.", S["price_detail"]), Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]), Paragraph("$7,500–$25,000/mo", S["price_main"])],
    [Paragraph("Goes to Google, LSA, and Meta — not to SMB Team.", S["price_detail"]), Paragraph("", S["price_detail"])],
]
pt = Table(price_data, colWidths=[4.5 * inch, 1.7 * inch])
pt.setStyle(TableStyle([
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("LEFTPADDING",(0,0),(-1,-1),4),
    ("RIGHTPADDING",(0,0),(-1,-1),4),
    ("TOPPADDING",(0,0),(-1,-1),2),
    ("BOTTOMPADDING",(0,0),(-1,-1),1),
    ("LINEBELOW",(0,1),(-1,1),0.5,RULE_GRAY),
    ("LINEBELOW",(0,3),(-1,3),0.5,RULE_GRAY),
    ("LINEBELOW",(0,5),(-1,5),0.5,RULE_GRAY),
]))
story.append(pt)
story.append(Paragraph(
    "Total: $8,047/mo + $7,500–$25,000 ad spend  |  Save $1,147/mo by bundling  |  Confirm revenue before aggressive ad spend",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
