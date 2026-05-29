"""
Sales Companion PDF — Krause Law, PLLC
Internal use only — do not share with client.
Output: krause-law/Krause_Law_May_28_2026_Sales_Companion.pdf
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

OUTPUT_PATH = "krause-law/Krause_Law_May_28_2026_Sales_Companion.pdf"


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

S = {}
S["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=9.5, leading=13, textColor=LIGHT_GRAY, spaceAfter=3)
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=ACCENT_GREEN, spaceBefore=6, spaceAfter=2)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.5, leading=13, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9.5, leading=13, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9.5, leading=13, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9.5, leading=12, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9.5, leading=13, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8.5, leading=11, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


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

story.append(Paragraph("Krause Law, PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  May 28, 2026  |  Rep: Randy Gold", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Practice</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Benjamin Krause", S["snap_value"]),
     Paragraph("~$750K est.", S["snap_value"]),
     Paragraph("3–5 staff", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("VA Benefits", S["snap_value"]),
     Paragraph("Minneapolis (national)", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: MISSION &amp; SCALE", S["section"]))
story.append(Paragraph("Benjamin wants the most trusted veterans law brand in America — and a firm that serves thousands of veterans a year without him in every case.", S["subsection"]))

story.append(quote_block("I want to help as many veterans as possible get the benefits they've earned — that's why I do this."))
story.append(Spacer(1, 1))
story.append(quote_block("I've been thinking a lot about AI tools and how they could help us scale without just adding more staff."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Thousands of veteran clients served.</b> He built the authority — he needs the volume to match it."))
story.append(bd("<b>A firm that runs without him in every case.</b> AI and systems handle what he shouldn't be doing."))
story.append(bd("<b>DisabledVeterans.org converting to consultations.</b> A decade of content should flow into the firm pipeline."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Zero paid advertising.</b> All leads are organic — no engine captures the demand his content creates."))
story.append(b("<b>No intake automation.</b> National practice with no 24/7 coverage means veterans get competitors when he's unavailable."))
story.append(b("<b>Benjamin is the bottleneck.</b> He is brand, attorney, and content creator — his hours cap how many veterans he can serve."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns his decade of authority into a paid lead engine — veterans find Krause Law before CCK Law."))
story.append(bd("Puts Krause Law above every competitor in Google the moment Google Screened LSA goes live."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("National VA practice with zero paid presence — this is the entire conversion engine built from scratch."))
story.append(b("LSA and Google Ads capture veterans who have already decided they need an attorney right now."))
story.append(b("Meta retargeting on DisabledVeterans.org visitors converts warm audiences who already trust Benjamin."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Provides the accountability structure to transition from Stage 4 content-operator to Stage 6 law firm owner."))
story.append(bd("Builds the management layer so Benjamin can focus on strategy and advocacy instead of everything else."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Benjamin runs the brand, the firm, and the content simultaneously — coaching separates those roles."))
story.append(b("Stage 4→6 requires explicit milestone accountability; without it he stays operator-mode regardless of revenue."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Krause Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Creates the first external paid pipeline in the firm's history — veterans ready to hire find Krause Law before CCK Law."))
story.append(bd("Starting at $5K proves channel ROI before scaling; Benjamin will see attributable cases within 60 days."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,000/mo — PPC $3,000 + LSA $2,000; minimum viable to capture high-intent VA attorney searches."))
story.append(b("<b>Aggressive:</b> $9,000/mo — stays under 35% cap at $750K estimated revenue ($21,694/mo = 34.7% of revenue)."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 6 cases x $3,500 = $21,000/mo vs. $5,000 spend = 4.2x return."))
story.append(b("<b>Aggressive:</b> 14 cases x $3,500 = $49,000/mo vs. $9,000 spend = 5.4x return."))
story.append(Paragraph("<i>All figures are estimates. Krause Law's retroactive benefit award fees may significantly exceed $3,500/case.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("Conservative: Disability minimums PPC $3K + LSA $2K = $5,000. CPL blended ~$120. Close rate 15%."))
story.append(b("Aggressive: 35% cap at $750K = $21,875/mo max. Package MRR $12,694 leaves $9,181 for ads."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I already have a huge audience through DisabledVeterans.org."', S["objection_q"]))
story.append(Paragraph("Organic reach creates awareness — it does not capture the demand it creates. CCK Law and Berry Law are running paid ads targeting the exact veterans who read his content. He is educating them; they are converting them.", S["objection_a"]))

story.append(Paragraph('"$12,694 a month is a big commitment."', S["objection_q"]))
story.append(Paragraph("At $750K revenue, $12,694 is 20% of monthly revenue — under the 35% cap. A conservative paid ads return of $21,000/month covers the full investment. The math improves rapidly as revenue grows toward $1.5M.", S["objection_a"]))

story.append(Paragraph('"I haven\'t had time to figure out AI tools."', S["objection_q"]))
story.append(Paragraph("That is exactly what AI Accelerator Level 1 solves. The Fractional CTO handles strategy and implementation — Benjamin maps the first three automation priorities and month one builds begin. He does not have to figure it out himself.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website, Google Ads, LSA, Meta Ads, SEO, GBP.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly 1:1 coaching, KPI framework, Stage 4→6 roadmap.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>AI Avatar Virtual Video Growth Add-On</b>", S["price_main"]),
     Paragraph("$1,950/mo", S["price_main"])],
    [Paragraph("1 long-form + 30 short-form videos/mo; $2,997 setup.", S["price_detail"]),
     Paragraph("add-on rate", S["price_detail"])],
    [Paragraph("<b>AI Accelerator Level 1 — Legal AI Workforce</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Fractional CTO, monthly automation builds, 5 team members.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,000–$9,000/mo", S["price_main"])],
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
    ("LINEBELOW", (0,9), (-1,9), 0.5, RULE_GRAY),
]))
story.append(pt)
story.append(Paragraph(
    "Total: $12,694/mo + $5,000–$9,000 ad spend  |  Save $2,247/mo by bundling  |  28.3%–34.7% of revenue (under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

data = open(OUTPUT_PATH, 'rb').read()
pages = data.count(b'/Type /Page') - 1  # subtract /Type /Pages root
print(f"Page count (approx): {pages}")
if pages != 2:
    print("WARNING: Sales Companion must be exactly 2 pages.")
