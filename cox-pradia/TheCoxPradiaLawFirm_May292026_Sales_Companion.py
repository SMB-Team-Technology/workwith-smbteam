"""
Sales Companion PDF — The Cox Pradia Law Firm
SMB Team | Nick Holderman | May 29, 2026
Internal use only — do not share with client.
Package: Full Service Marketing — Dominate + Master's Circle
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
     Paragraph("Not stated — confirm", S["snap_value"]),
     Paragraph("10 staff", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("Houston, TX", S["snap_value"])],
]
t1 = Table(snap, colWidths=[0.95*inch, 1.2*inch, 0.75*inch, 0.65*inch, 0.85*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 3))

story.append(Paragraph("Dominant Buying Motive: LEGACY + FREEDOM", S["section"]))
story.append(Paragraph("Build a firm that generates consistent cases from systems — freeing Cox and Pradia to focus on high-value work without chasing every case. (No transcript — confirm DBM on call.)", S["subsection"]))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable case flow.</b> A paid system delivering PI leads every month — not referral dependency."))
story.append(bd("<b>Firm independence.</b> Operations that run without partner bottlenecks so they choose their focus."))
story.append(bd("<b>Revenue reflecting their reputation.</b> 40+ years and Top 50 Black Attorneys in Houston — the financials should match."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No paid ads active.</b> Invisible while Zehl ($913K/yr), Simmons ($384K/yr), Terry Bryant ($272K/yr) dominate."))
story.append(b("<b>3-pack absent.</b> Zero local pack visibility for every primary PI term in Houston."))
story.append(b("<b>NAP inconsistency.</b> Two addresses + three phone numbers fragmenting local SEO authority."))
story.append(b("<b>Review gap widening.</b> 51 reviews vs. Zehl's 1,262 — compounds every month without action."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Establishes Cox Pradia across Google Ads, LSA, Meta, and SEO at a budget that actually competes in Houston's PI market."))
story.append(bd("Closes the visibility gap against Zehl and Simmons — at the Dominate level, the firm is finally in the same league as its top competitors."))
story.append(bd("Builds the lead generation engine that lets the intake team already in place actually run at capacity."))

story.append(Paragraph("<b>Full Service Marketing — Dominate  |  $10,497/mo bundled</b>", S["subsection"]))
story.append(b("PI practice in Houston's most competitive market requires Dominate-level investment to compete — Essentials and Starter are outgunned."))
story.append(b("Dominate includes up to $75,000/mo ad spend capacity — covers full aggressive scenario as firm scales."))
story.append(b("Saves $2,000/mo vs. stand-alone price of $12,497/mo."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Cox and Pradia peer accountability with other $1M+ firm owners — shared tactics, real benchmarks, faster decisions."))
story.append(bd("Builds the management layer and leadership framework that allows the firm to scale without partner bottlenecks."))

story.append(Paragraph("<b>Master's Circle  |  $4,600/mo bundled</b>", S["subsection"]))
story.append(b("Appropriate for a 10-person established firm with structured roles and $1M+ revenue trajectory."))
story.append(b("Weekly group coaching, PI masterminds, quarterly workshops, one annual in-person event, 1:1 strategy sessions."))
story.append(b("Saves $397/mo vs. stand-alone price of $4,997/mo."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Cox Pradia — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Conservative ($20K) projects 6 PI cases/mo at $50K avg = $300K/mo in case revenue vs. $20K spend — 15x return. (Estimates only.)"))
story.append(bd("Aggressive ($60K) projects 20 PI cases/mo = $1,000,000/mo in case revenue vs. $60K spend — 17x return. (Estimates only.)"))

story.append(Paragraph("<b>Recommended range: $20,000–$60,000/mo</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> PI hard floor $10K PPC + LSA $2K + Meta retargeting $1.5K + Meta lead gen $6.5K = $20,000."))
story.append(b("<b>Aggressive:</b> $2.5M goal x 20% / 12 x 1.5 Tier-1 = $75K. Capped at Dominate practical level: $60,000."))
story.append(b("<b>35% cap check:</b> Conservative $35,097 total requires $1.2M+/yr revenue. Aggressive $75,097 requires $2.6M+/yr. Confirm on call."))
story.append(Paragraph("<i>Avg. case value $50K is practice area default — not stated by firm. Houston truck/TBI/wrongful death cases often $100K–$2M+.</i>", S["disclaimer"]))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"Our referrals have worked fine for 27 years."', S["objection_q"]))
story.append(Paragraph("Referrals are relationship-based and capped by the partners' personal network. Zehl has 1,262 Google reviews and an estimated $913K/yr ad budget — they are capturing the cases no one refers to Cox Pradia. Referrals won't close that gap.", S["objection_a"]))

story.append(Paragraph('"$15,097/month is a lot before we know if ads will work."', S["objection_q"]))
story.append(Paragraph("At conservative ad spend, the projected return is 15x — one additional truck accident case at $150K pays for the full program. The question is not whether Houston PI ads work; it is who captures the leads while Cox Pradia waits.", S["objection_a"]))

story.append(Paragraph('"Houston PI is too competitive — we can\'t beat Zehl."', S["objection_q"]))
story.append(Paragraph("You don't need to. Harris County sees 70,000+ auto accidents per year. Targeting TBI, wrongful death, nursing home negligence, and truck accidents in suburbs (Katy, Sugar Land, The Woodlands) where Zehl's presence is thinner puts the firm in front of cases it can win.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Dominate</b>", S["price_main"]),
     Paragraph("$10,497/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, full SEO, website — all PI practice areas in Houston.", S["price_detail"]),
     Paragraph("<strike>$12,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle</b>", S["price_main"]),
     Paragraph("$4,600/mo", S["price_main"])],
    [Paragraph("Weekly coaching, PI masterminds, quarterly workshops, annual in-person event.", S["price_detail"]),
     Paragraph("<strike>$4,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$20,000–$60,000/mo", S["price_main"])],
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
    "SMB Team total: $15,097/mo  |  Save $2,397/mo by bundling  |  35% cap: confirm revenue ($1.2M+ conservative, $2.6M+ aggressive)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
