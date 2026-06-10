"""
Sales Companion PDF — Granados Law Group, PLLC
SMB Team | Jacob Meissner | June 11, 2026
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

OUTPUT_PATH = "granados/GranadosLawGroup_June112026_Sales_Companion.pdf"


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

story.append(Paragraph("Granados Law Group, PLLC", S["title"]))
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
    [Paragraph("Lindsey Granados", S["snap_value"]),
     Paragraph("~$750K/yr", S["snap_value"]),
     Paragraph("6 total", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("~80%", S["snap_value"]),
     Paragraph("Cary, NC", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM + SECURITY", S["section"]))
story.append(Paragraph("Lindsey wants the firm to run without her so she can take a real vacation and fund college and retirement on a plan — not a hope.", S["subsection"]))

story.append(quote_block("I work 11-12 hours/day and fear revenue will stop during my upcoming 2-week vacation."))
story.append(Spacer(1, 1))
story.append(quote_block("I need to rebuild a stable team so the firm can run without me."))
story.append(Spacer(1, 1))
story.append(quote_block("We're in the black."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Vacation without fear.</b> Take 2 weeks off and come back to a firm that ran itself."))
story.append(bd("<b>Return to $1.25M.</b> Prior peak before her partner ran for Congress — she knows it is possible."))
story.append(bd("<b>Financial clarity.</b> College and retirement funded by a plan, not by logging more hours."))
story.append(bd("<b>Team she can trust.</b> Stable, sales-minded people who handle operations without her."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>Owner dependency.</b> Every high-value felony intake runs through Lindsey personally."))
story.append(b("<b>No after-hours coverage.</b> DWI arrests happen Friday nights — the firm is dark."))
story.append(b("<b>No financial visibility.</b> 'We're in the black' is the full extent of financial planning."))
story.append(b("<b>Marketing ROI unknown.</b> Paying Rise Up Marketing with no measured return."))
story.append(b("<b>No documented processes.</b> Team runs on Lindsey's knowledge, not on systems."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Puts the firm's ads on 24/7 — capturing DWI and criminal arrests that currently go to Saad Law after hours."))
story.append(bd("Gives Lindsey real ROI numbers — she will finally know what each case costs to acquire."))
story.append(bd("Closes the review gap with competitors — systematic review generation improves local pack rankings without additional spend."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Personal injury practice area — minimum Starter tier per eligibility rules."))
story.append(b("Revenue $750K in $400K–$1M band — Starter is the correct tier."))
story.append(b("Criminal defense + DWI in Raleigh Tier 3 market — competitive enough to warrant full-service."))
story.append(b("Saves $850/mo vs. stand-alone rate of $5,697/mo."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Builds the team systems and delegation framework — the structural fix for owner dependency."))
story.append(bd("Weekly coaching with attorneys facing the same rebuild challenges — she is not doing this alone."))
story.append(bd("Creates the documented playbooks that let the team handle operations when Lindsey is on vacation."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M — Elite Coach Plus is the standard recommendation."))
story.append(b("Team is stable 3–4 months but has no documented processes — exactly what coaching addresses."))
story.append(b("Saves $297/mo vs. stand-alone rate of $3,497/mo."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Granados Law Group — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Generates consistent criminal defense and DWI cases from paid search — measured, not hoped for."))
story.append(bd("Funds the return to $1.25M by adding 5–10 signed cases per month from ad-generated leads."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,500/mo — covers Google PPC, LSA, and Meta retargeting 24/7."))
story.append(b("<b>Aggressive:</b> $13,500/mo — expands felony-specific campaigns; stays under 35% revenue cap."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~31 leads x 15% close = ~5 cases x $8K = ~$40K/mo vs. $7.5K spend = ~5x return."))
story.append(b("<b>Aggressive:</b> ~67 leads x 15% close = ~10 cases x $8K = ~$80K/mo vs. $13.5K spend = ~6x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Case value blended from transcript ($4K–$50K).</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Criminal defense PPC $4,000 + LSA $2,000 + Meta $1,000 + Meta lead gen $500 = $7,500."))
story.append(b("<b>Aggressive:</b> 35% cap at $750K rev = $21,875 total max. Minus $8,047 fees = $13,828 max ad spend."))
story.append(b("Total spend at aggressive: $21,547/mo = 34.5% of revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I already have a marketing company — Rise Up Marketing is handling it."', S["objection_q"]))
story.append(Paragraph("Lindsey said on the call she doesn't know if Rise Up's ads are performing. We track every dollar to signed cases and send a monthly report. If Rise Up is delivering, you'll see it. If not, you'll stop funding campaigns that aren't working.", S["objection_a"]))

story.append(Paragraph('"The ads run at night and that\'s fine — we answer calls during business hours."', S["objection_q"]))
story.append(Paragraph("DWI arrests peak Friday–Saturday 10pm–3am. Those families search for an attorney that same night. Saad Law (275 reviews, former DA) answers. Kurtz & Blum (290 reviews) answers. Granados Law Group does not. At $7,500+ per DWI case, one recovered after-hours case per week is $30K/month.", S["objection_a"]))

story.append(Paragraph('"$8,000 a month is a lot — I don\'t know if we can afford it."', S["objection_q"]))
story.append(Paragraph("Conservative ad scenario alone projects ~$40K/month in new case revenue on $7.5K ad spend — a 5x return. The management fee pays for itself if one additional case per month is signed. At her current 80% close rate, that is very achievable.", S["objection_a"]))

story.append(Paragraph('"We just stabilized the team — I\'m not sure this is the right time."', S["objection_q"]))
story.append(Paragraph("The stabilization is exactly why this is the right time. The team is sales-minded and coachable — Lindsey said so herself. Waiting another 6 months means Saad Law and Amy Whinery Osborne (208 reviews in Cary) extend their lead while the firm holds steady. The window to close the gap is open now.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, SEO, website CRO, reporting.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, masterminds, team systems, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,500–$13,500/mo", S["price_main"])],
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
    "Total: $8,047/mo + $7,500–$13,500 ad spend  |  Save $1,147/mo by bundling  |  24.9%–34.5% of revenue (under 35% cap)",
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
