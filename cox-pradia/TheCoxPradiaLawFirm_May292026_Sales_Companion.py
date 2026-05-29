"""
Sales Companion PDF — The Cox Pradia Law Firm
SMB Team | Nick Holderman | May 29, 2026
Internal use only — do not share with client.
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

OUTPUT_PATH = "cox-pradia/TheCoxPradiaLawFirm_May292026_Sales_Companion.pdf"


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
S["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=9, leading=12, textColor=LIGHT_GRAY, spaceAfter=2)
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=ACCENT_GREEN, spaceBefore=5, spaceAfter=2)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=10, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=10, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9, leading=11, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8.5, leading=11, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


def b(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY, spaceBefore=2, spaceAfter=2)


# ══════════════════════════════════════════════════════════
# PAGE 1
# ══════════════════════════════════════════════════════════
story = []

story.append(Paragraph("The Cox Pradia Law Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  May 29, 2026  |  Rep: Nick Holderman", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Cox &amp; Pradia", S["snap_value"]),
     Paragraph("Est. $500K–$1.5M (unconfirmed)", S["snap_value"]),
     Paragraph("10 staff", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("Houston, TX", S["snap_value"])],
]
t1 = Table(snap, colWidths=[0.95*inch, 1.3*inch, 0.75*inch, 0.65*inch, 0.85*inch, 1.05*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 3))

story.append(Paragraph("Dominant Buying Motive: LEGACY + FREEDOM", S["section"]))
story.append(Paragraph("Build a respected Houston PI firm that generates consistent cases from systems — freeing Cox and Pradia to focus on the high-value work without chasing every case. (No transcript available — confirm DBM on discovery call.)", S["subsection"]))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable lead flow.</b> A paid system generating PI cases every month — not referral dependency."))
story.append(bd("<b>Firm independence.</b> Operations that run without partner bottlenecks so Cox and Pradia choose their focus."))
story.append(bd("<b>Revenue that matches their reputation.</b> 40+ years and Top 50 Black Attorneys in Houston — the numbers should reflect it."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No paid ads active.</b> Invisible to high-intent PI searchers while competitors spend $250K–$900K+/year on Google alone."))
story.append(b("<b>3-pack absent for every term.</b> Zero local pack visibility — zero free leads from Google Maps for any PI search."))
story.append(b("<b>NAP inconsistency.</b> Two addresses + three phone numbers across directories actively suppressing local SEO."))
story.append(b("<b>Review gap is widening.</b> 51 reviews at 4.4 stars vs. Zehl at 1,262 reviews and 5.0 — gets harder every month."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Captures Houston PI searchers currently going to Zehl, Simmons, and Terry Bryant — puts Cox Pradia at the top of Google Ads and LSA."))
story.append(bd("Fixes NAP inconsistency, builds suburb landing pages, and activates review velocity — compounding local SEO gains every month."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("PI practice requires Starter minimum — Essentials not eligible."))
story.append(b("Google Ads + LSA + Meta + SEO + website optimization — coordinated, not siloed."))
story.append(b("Starter supports up to $25,000/mo ad spend — covers both conservative and aggressive scenarios."))
story.append(b("Saves $850/mo vs. stand-alone price of $5,697/mo."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Cox and Pradia the revenue targets, intake KPIs, and team accountability framework to scale — not just generate more leads."))
story.append(bd("Builds the management layer that allows the firm to operate without constant partner direction."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Appropriate for estimated $500K–$1M revenue range."))
story.append(b("Weekly coaching, masterminds, quarterly workshops, one annual in-person event."))
story.append(b("1:1 sessions for intake design, team KPIs, and case acquisition tracking setup."))
story.append(b("Saves $297/mo vs. stand-alone price of $3,497/mo."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Cox Pradia — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Generates 19–47 qualified PI leads/month from Google, LSA, and Meta — feeds the intake team already in place."))
story.append(bd("Conservative scenario projects $150,000/mo in case revenue against $13,200 ad spend — 11x return. (Est. only)"))

story.append(Paragraph("<b>Conservative: $13,200/mo  |  Aggressive: $22,000/mo</b>", S["subsection"]))
story.append(b("Conservative: PI hard floor PPC $10K + LSA $2K + Meta retargeting $1.2K = $13,200."))
story.append(b("Aggressive: $1.5M goal x 20% / 12 x 1.5 Tier-1 geo = $37,500. Capped at Starter limit: $22,000."))
story.append(b("ROI: Conservative 3 cases x $50K = $150K (11x). Aggressive 7 cases x $50K = $350K (16x). Estimates only."))
story.append(b("<b>35% cap:</b> $8,047 + $22K = $30,047/mo. Requires ~$86K/mo revenue (~$1.03M/yr). Confirm before presenting."))
story.append(Paragraph("<i>Avg. case value $50K is a practice area default — not stated. Houston truck/TBI cases often $150K–$2M+.</i>", S["disclaimer"]))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"Our cases come from referrals — we have never needed ads."', S["objection_q"]))
story.append(Paragraph("Zehl spends $913K/year on Google Ads and has 1,262 reviews. Simmons spends $384K/year and has 502. Both appear at the top of every search your prospects run. Referrals are not scalable — they are the result of relationships. The question is whether you close this gap before it gets wider.", S["objection_a"]))

story.append(Paragraph('"$8,047/month is a big number right now."', S["objection_q"]))
story.append(Paragraph("At conservative ad spend, the projected return is $150K/month in case revenue against $13.2K ad spend — an 11x return. A single additional truck accident case at $150K+ pays for the full program for the month. The cost of not acting is measured in leads Zehl captures while Cox Pradia waits.", S["objection_a"]))

story.append(Paragraph('"Houston PI is too competitive for us to win on ads."', S["objection_q"]))
story.append(Paragraph("Competitive means high volume — 70,000+ Harris County auto accidents per year. Your 40+ years of experience, structured team, and campaigns targeting TBI, truck accidents, and wrongful death can win cases in segments where even Zehl is not dominant. You do not need to beat everyone — you need to capture your share.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, SEO, website optimization — all PI practice areas.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, masterminds, workshops, 1:1 strategy sessions.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$13,200–$22,000/mo", S["price_main"])],
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
    "SMB Team total: $8,047/mo  |  Save $1,147/mo by bundling  |  Confirm revenue — 35% cap requires ~$1.03M+/yr",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
