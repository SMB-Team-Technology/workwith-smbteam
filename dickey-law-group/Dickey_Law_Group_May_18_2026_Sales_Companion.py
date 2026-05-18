"""
Sales Companion PDF — Dickey Law Group PLLC
SMB Team Internal Document — Do Not Share with Client
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

OUTPUT_PATH = "dickey-law-group/Dickey_Law_Group_05182026_Sales_Companion.pdf"


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

story.append(Paragraph("Dickey Law Group PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  May 18, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
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
    [Paragraph("James &amp; Mireya Dickey", S["snap_value"]),
     Paragraph("~$400K–$600K est.", S["snap_value"]),
     Paragraph("2 attorneys", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("The Woodlands, TX", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM + LEGACY", S["section"]))
story.append(Paragraph("Build a bilingual firm that serves the community and creates financial independence — without requiring both founders at every step.", S["subsection"]))

story.append(Paragraph("<i>No transcript — DBM inferred from public data. Validate on proposal call May 22, 2026.</i>", S["disclaimer"]))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What they want:</b>", S["subsection"]))
story.append(bd("<b>Predictable client flow.</b> 100% organic today — they want a system, not a dependency on referrals and rankings."))
story.append(bd("<b>Time back.</b> A firm that doesn't require both founders at every intake call, every evening, every weekend."))
story.append(bd("<b>To serve their bilingual community.</b> Mireya's Spanish fluency and Hispanic Chamber membership are more than credentials — they are a market advantage."))
story.append(bd("<b>Financial clarity.</b> Revenue they actually keep — profit planned, not discovered."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping them:</b>", S["subsection"]))
story.append(b("<b>No paid lead generation.</b> 100% organic — client volume is unpredictable and capped by search rankings they don't control."))
story.append(b("<b>No support staff.</b> Everything runs through two attorneys — no path to stepping back without hiring and systems first."))
story.append(b("<b>Revenue not confirmed.</b> Estimated $300K–$600K; confirm actual figure before finalizing ad spend."))
story.append(b("<b>No transcript.</b> DBM inferred — validate all assumptions on proposal call May 22, 2026."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Turns their bilingual website and strong review base into a lead generation machine — consultations come in while they are doing casework."))
story.append(bd("Puts Dickey Law Group at the top of Google for estate planning and probate searches in The Woodlands — a position no organic-only strategy can reliably hold."))
story.append(bd("Opens the Spanish-language paid search channel — a wide-open market where no competitor currently has a credible presence."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue tier: $400K–$1M → Starter. Essentials ineligible above $400K."))
story.append(b("Estate planning: no PI minimum tier restriction. No website rebuild needed — modern bilingual site."))
story.append(b("Spanish campaign: YES — bilingual site + Hispanic Chamber = confirmed priority."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Gives James and Mireya an accountability structure and strategic advisor as the firm scales — so growth does not just mean more work."))
story.append(bd("Connects them to a peer community of estate planning attorneys at similar stages — actionable strategies, not theory."))
story.append(bd("Builds the operational and business development habits that create a self-managing firm — the foundation of the freedom they are after."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue tier: $400K–$1M, any team → Elite Coach Plus. FCOO ineligible under $500K."))
story.append(b("Includes: weekly group coaching, practice area masterminds, quarterly virtual workshops, one annual in-person."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Dickey Law Group — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Brings estate planning and probate prospects directly to the firm at the moment they are ready to hire — not waiting to be found organically."))
story.append(bd("The Spanish-language campaign captures a market segment that almost no competitor is currently paying to reach."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,500/mo — Google PPC $3,500 + LSA $2,000. Minimum viable paid search footprint."))
story.append(b("<b>Aggressive:</b> $15,000/mo — adds Meta retargeting, Spanish-language campaigns, and expanded keyword coverage."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~42 leads x 15% close x $3,500 avg case = ~$21,000/mo vs. $5,500 spend = 3.8x return (est.)"))
story.append(b("<b>Aggressive:</b> ~172 leads x 15% close x $3,500 avg case = ~$91,000/mo vs. $15,000 spend = 6.1x return (est.)"))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Case value of $3,500 is estate planning industry default — not confirmed with firm.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Estate planning channel minimums — Google PPC $3,500 + LSA $2,000 = $5,500."))
story.append(b("<b>Aggressive:</b> $900K goal x 20% / 12 x 1.33 Spanish = $19,950 minus $4,847 fee = $15,103. Rounded to $15,000."))
story.append(b("35% cap: $8,047 + $5,500 = $13,547 = 32.5% at $500K. Confirm revenue before aggressive spend."))

story.append(thin_rule())

# ── If They Push Back ──
story.append(Paragraph("If They Push Back", S["section"]))

story.append(Paragraph('"We already get clients from Google organically — why pay for ads?"', S["objection_q"]))
story.append(Paragraph("Organic gets people who searched for you specifically. Ads get people who found a competitor first — the larger share. With 1,300 monthly visitors and 0% paid traffic, most high-intent estate planning searches in The Woodlands are landing on other firms.", S["objection_a"]))

story.append(Paragraph('"We do not have a big budget right now."', S["objection_q"]))
story.append(Paragraph("Conservative spend ($5,500/mo) projects ~6 cases/month at $3,500 avg = ~$21,000 revenue. The investment is under 25% of estimated monthly revenue at the $400K floor. First two clients cover the management fee.", S["objection_a"]))

story.append(Paragraph('"We are just two people — can we handle more clients?"', S["objection_q"]))
story.append(Paragraph("That is exactly why coaching runs alongside marketing. Elite Coach Plus builds the intake, delegation, and operations systems that absorb volume without adding attorney hours — infrastructure grows with the pipeline.", S["objection_a"]))

story.append(Paragraph('"We have never advertised — how do we know it works?"', S["objection_q"]))
story.append(Paragraph("Estate planning performs strongly in paid search: high case values, motivated clients, and clear intent keywords. The firm has 32 five-star reviews and a bilingual site that is already conversion-ready — the traffic is the only missing piece.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, SEO, website optimization, reporting.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("1-on-1 coaching, group sessions, masterminds, workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,500–$15,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $5,500–$15,000 ad spend  |  Save $1,147/mo by bundling  |  32.5%–61% of est. revenue (confirm revenue before aggressive launch)",
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
