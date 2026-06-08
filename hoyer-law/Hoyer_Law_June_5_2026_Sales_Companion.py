"""
Sales Companion PDF — Hoyer Law
SMB Team  |  June 5, 2026  |  Rep: Randy Gold
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

OUTPUT_PATH = "hoyer-law/Hoyer_Law_06052026_Sales_Companion.pdf"


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

story.append(Paragraph("Hoyer Law (Hoyer Law Firm)", S["title"]))
story.append(Paragraph("Sales Companion  |  June 5, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Casey Hoyer", S["snap_value"]),
     Paragraph("~$600K est.", S["snap_value"]),
     Paragraph("10 (3 atty)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("Lehi + St. George, UT", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM", S["section"]))
story.append(Paragraph("Casey wants a firm that runs itself so he can practice law on his terms and stop managing every detail of the business.", S["subsection"]))

story.append(quote_block("No Fathom transcript available — DBM inferred from web research and firm profile."))
story.append(Spacer(1, 1))
story.append(quote_block("15+ years building a firm with a GM (wife Analia), 10 staff, and 2 locations — the infrastructure of freedom exists, but the growth engine to make it sustainable does not."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable client flow.</b> Stop relying on organic and referrals — build a paid pipeline that delivers family law clients every month."))
story.append(bd("<b>Operational freedom.</b> Let Analia and the team run day-to-day so he can focus on the cases he chooses."))
story.append(bd("<b>AI-powered leverage.</b> Multiply staff output on intake, drafting, and client updates without adding headcount."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No paid advertising.</b> CoilLaw (308 reviews) and Arnold Wadsworth are capturing every paid click while Hoyer Law relies entirely on organic."))
story.append(b("<b>No confirmed intake SOP.</b> Quality depends on which staff member picks up — not on a consistent system."))
story.append(b("<b>GM authority not formalized.</b> Analia is GM in title but operational decisions still route to Casey."))
story.append(b("<b>No AI infrastructure.</b> 10-person bilingual firm with a GM is AI-ready — no one is leading the rollout."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Converts 15 years of reputation and 139 reviews into a paid lead engine — entering Google, LSA, and Meta for the first time while competitors are already spending."))
story.append(bd("Spanish-language campaigns give Hoyer Law first-mover advantage in a bilingual market segment no competitor has claimed."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$600K–$1M places firm in Starter tier ($400K–$1M range)."))
story.append(b("Starter covers all channels: Google Ads, LSA, Meta, SEO, and Spanish-language campaigns."))
story.append(b("Starter ad spend cap $25,000/mo — well above $5,500–$14,000 recommended range."))
story.append(b("Stand-alone $5,697/mo — bundled saves $850/mo."))

story.append(thin_rule())

# ── Why This AI Package ──
story.append(Paragraph("Why This AI &amp; Growth Infrastructure Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("A Fractional CTO deploys Claude Enterprise and AI Skills for intake and drafting — without adding to Casey's management load."))
story.append(bd("Every staff member trained on AI tools relevant to their role — Analia, paralegals, receptionist all work faster on repeatable tasks."))

story.append(Paragraph("<b>Fractional CTO Level 1 (AI Accelerator L1)  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $600K+ clears $500K LAW minimum; 10-person team with bilingual GM — not solo."))
story.append(b("L1 done-with-you model selected: Casey lacks bandwidth to manage AI rollout independently."))
story.append(b("Includes Claude Enterprise, pre-built Law Firm AI Skills, monthly CTO strategy calls, full staff training."))
story.append(b("Stand-alone $3,797/mo — bundled saves $500/mo. AI Foundation Sprint $14,997 one-time available."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Hoyer Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("$5,500/mo conservative launches paid coverage on Google and LSA for the first time — capturing high-intent family law searches currently going to CoilLaw."))
story.append(bd("$14,000/mo aggressive adds Meta retargeting and cold audiences including Spanish-language targeting — no confirmed competitor is reaching this segment."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,500/mo — Google PPC $3,500 + LSA $2,000. Minimum viable coverage for Lehi family law."))
story.append(b("<b>Aggressive:</b> $14,000/mo — all four channels. 20% rule: $1.2M goal x 20% / 12 = $20K; minus $4,847 fee = $15K; using $14K."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative ($5,500/mo):</b> ~8 cases x $10K avg = ~$80K/mo vs. $5,500 spend = ~15x return (est.)."))
story.append(b("<b>Aggressive ($14,000/mo):</b> ~25 cases x $10K avg = ~$250K/mo vs. $14,000 spend = ~18x return (est.)."))
story.append(Paragraph("<i>All figures are estimates. Case value is practice area default ($10K) — confirm on call. Results not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Family Law minimums: Google PPC $3,500 + LSA $2,000 = $5,500."))
story.append(b("<b>Aggressive:</b> $1.2M target x 20% / 12 = $20K. Tier 4 (1.0x). Minus $4,847 fee = ~$15K; using $14,000."))
story.append(b("Total aggressive: $8,144 fees + $14,000 ads = $22,144. Flag revenue on call — if $840K+, within 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I\'m already getting leads from organic — why do I need paid?"', S["objection_q"]))
story.append(Paragraph("CoilLaw (308 reviews, 4.8 stars) and Arnold Wadsworth are both confirmed in paid results for 'divorce attorney Lehi Utah.' Every high-intent click on Google Ads and LSA goes to them. Organic works — paid defends the top of the page.", S["objection_a"]))

story.append(Paragraph('"I\'m not sure my team is ready for AI."', S["objection_q"]))
story.append(Paragraph("Level 1 is done-with-you — the Fractional CTO leads the entire rollout. Casey and Analia do not manage it. Bilingual GM + 7 support staff is exactly the human foundation AI implementation requires.", S["objection_a"]))

story.append(Paragraph('"Can we start with just the marketing?"', S["objection_q"]))
story.append(Paragraph("More leads without AI-powered intake just means more manual work for Casey and the team. The Fractional CTO converts the marketing investment into operational leverage — handling intake responses and drafting so the team can scale without adding headcount.", S["objection_a"]))

story.append(Paragraph('"What if the revenue estimate is wrong?"', S["objection_q"]))
story.append(Paragraph("Revenue was not confirmed — $600K is estimated from team size; ZoomInfo says ~$4M. Both Starter and FCTO Level 1 qualify at $500K–$1.5M either way. If revenue confirms higher on the call, Growth + Master's Circle may be appropriate — Randy to assess.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, SEO, Spanish-language campaigns, website optimization.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Fractional CTO Level 1</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Claude Enterprise, Law Firm AI Skills, done-with-you rollout, staff training. Foundation Sprint $14,997 one-time (optional).", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,500–$14,000/mo", S["price_main"])],
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
    "Total: $8,144/mo + $5,500–$14,000 ad spend  |  Save $1,350/mo by bundling  |  Confirm revenue on call",
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
