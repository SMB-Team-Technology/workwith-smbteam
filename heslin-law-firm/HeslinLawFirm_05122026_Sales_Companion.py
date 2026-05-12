"""
Sales Companion PDF — The Heslin Law Firm
May 12, 2026 | Rep: Jonathan Farace
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

OUTPUT_PATH = "heslin-law-firm/HeslinLawFirm_05122026_Sales_Companion.pdf"


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
S["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=9.5, leading=13, textColor=LIGHT_GRAY, spaceAfter=3)
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=ACCENT_GREEN, spaceBefore=5, spaceAfter=2)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9, leading=11, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8, leading=11, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


def b(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY, spaceBefore=3, spaceAfter=3)

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

story.append(Paragraph("The Heslin Law Firm", S["title"]))
story.append(Paragraph("Sales Companion  |  May 12, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Gary Heslin", S["snap_value"]),
     Paragraph("$700K–$800K", S["snap_value"]),
     Paragraph("Gary + staff; Brian Nov 2026", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("~80–90%+", S["snap_value"]),
     Paragraph("NE Philadelphia, PA", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: LEGACY &amp; FREEDOM", S["section"]))
story.append(Paragraph("Gary wants to hand the firm to Brian Emhof in November 2026 — not just as an employee, but as the attorney who carries the practice forward.", S["subsection"]))

story.append(quote_block("I need to get to 12 cases a month before Brian starts — the revenue needs to be there to support the hire."))
story.append(Spacer(1, 1))
story.append(quote_block("I've spent 30 years building this firm. The goal is to get to a point where it runs without me having to be there every day."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Brian to succeed from day one.</b> Firm at 12 cases/mo so revenue supports the full-time hire the moment he walks in."))
story.append(bd("<b>A firm that runs without him.</b> Step back from the lead attorney role — hand off the identity, not just the caseload."))
story.append(bd("<b>The November transition to actually happen.</b> Not get pushed back or stall because revenue wasn't there."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No lead engine.</b> 2-year SEO pause has taken the firm off the 3-pack for NE Philadelphia PI searches — cases not coming in at the rate needed."))
story.append(b("<b>Platform lock-in.</b> Foster Web Marketing .cfm CMS blocks all outside SEO agencies — WordPress rebuild is required before any SEO work can start."))
story.append(b("<b>No transition playbook.</b> Brian has no onboarding structure; the planning cannot be rushed in the final 60 days before his start date."))
story.append(b("<b>Competitors filling the vacuum.</b> Kalikhman &amp; Rayz (250+ reviews in 9 months), Cousin Benny (85–113 reviews), Pearce Law (114+) are building while Heslin is offline."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Restores 3-pack visibility in 19124 and NE Philadelphia — putting the firm back in front of prospects actively searching for a PI attorney in Gary's market."))
story.append(bd("WordPress rebuild removes the 2-year platform barrier that has blocked every SEO agency from working with the site."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("PI in Philadelphia (Tier 1) — minimum Starter tier; Essentials is ineligible for personal injury."))
story.append(b("Website rebuild required: Foster Web blocks all SEO agency access — WordPress is the prerequisite for every other growth action."))
story.append(b("Revenue $700K–$800K maps to Starter band ($400K–$1M); Growth tier available at $1M+."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Heslin Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the transition playbook that gives Gary confidence to step back and gives Brian a documented path to the lead attorney role."))
story.append(bd("Provides weekly accountability during the 12 months that determine whether November 2026 becomes a real handoff or a moving target."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $700K–$800K maps to Elite Coach Plus ($400K–$1M); Master's Circle requires $1M+."))
story.append(b("High-stakes transition with defined November deadline — weekly coaching cadence provides the structure the handoff requires."))
story.append(b("Includes: weekly group coaching, PI masterminds, quarterly workshops (virtual), one annual in-person workshop."))

story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Generates qualified PI leads in NE Philadelphia during the 6-month SEO ramp-up — so the firm doesn't wait for organic rankings to reach 12 cases/mo."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative: $5,000/mo</b> — PI high-competition hard floor; equals the Starter tier cap. ~3 cases x $8K = $24K/mo = 4.8x return on ad spend."))
story.append(b("<b>Aggressive: $13,000/mo</b> — capped at 33.7% of revenue (under 35% ceiling). ~4 cases x $8K = $32K/mo = 2.5x return on ad spend."))
story.append(Paragraph("<i>All figures are estimates based on Philadelphia PI market benchmarks. Not guaranteed.</i>", S["disclaimer"]))
story.append(b("<b>How calculated:</b> Revenue goal ($1.15M) x 20% / 12 x Tier 1 (1.5x) = $28,800; capped at 35% rule: $21,875 total minus $8,047 fee = $13,828 max ad spend."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I want to compare this with the 10 Golden Rules offer first."', S["objection_q"]))
story.append(Paragraph("The comparison worth making: which offer has the fastest path to 12 cases/month before November 2026? The WordPress rebuild and NE Philadelphia SEO restoration are the specific plan — ask the other offer to show the same.", S["objection_a"]))

story.append(Paragraph('"I\'m not sure I\'m ready to commit to 12 months."', S["objection_q"]))
story.append(Paragraph("SEO ramp-up takes 6 months alone. A shorter commitment means starting a campaign he can't see results from before it ends. November is 6 months away — the commitment has to match the timeline Gary is already on.", S["objection_a"]))

story.append(Paragraph('"We still get referrals — the firm isn\'t dead, it\'s just slower."', S["objection_q"]))
story.append(Paragraph("Referrals are keeping the firm at 8 cases/month. The goal is 12. That gap won't close on referrals alone — and while Heslin waits, Kalikhman &amp; Rayz is adding 250+ reviews in 9 months inside 19124.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("WordPress rebuild, NE Philadelphia local SEO, GBP optimization, monthly lead tracking.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, PI masterminds, quarterly workshops (virtual), one annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,000–$13,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $5,000–$13,000 ad spend  |  Save $1,147/mo by bundling  |  20.9%–33.7% of revenue (under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

import re
with open(OUTPUT_PATH, 'rb') as f:
    content = f.read()
m = re.search(rb'/Count (\d+)', content)
if m:
    print(f"Page count: {m.group(1).decode()}")
