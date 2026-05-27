"""
Sales Companion PDF — Law Office of Drake Spears
SMB Team | May 27, 2026 | Rep: Jacob Meissner
Internal use only. Do not share with prospect.
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

OUTPUT_PATH = "law-office-of-drake-spears/Law_Office_of_Drake_Spears_05272026_Sales_Companion.pdf"


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

story.append(Paragraph("Law Office of Drake Spears", S["title"]))
story.append(Paragraph("Sales Companion  |  May 27, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Drake Spears", S["snap_value"]),
     Paragraph("~$250K est.*", S["snap_value"]),
     Paragraph("Solo (1)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Plainfield, IN", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.7*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Paragraph("*No transcript available. Revenue estimated from market context. Confirm on call. ESCALATION: Revenue under $300K requires scoping approval.", S["disclaimer"]))
story.append(Spacer(1, 3))

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: INDEPENDENCE", S["section"]))
story.append(Paragraph("Drake left Banks &amp; Brower — one of Indianapolis's largest firms — to build a practice entirely his own.", S["subsection"]))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>His own client base.</b> Cases that came to him, not through a former employer's network."))
story.append(bd("<b>Market recognition.</b> His name first on Google when Hendricks County families search for a family lawyer."))
story.append(bd("<b>Case selection.</b> The freedom to choose which matters to take on, not just take what comes in."))
story.append(bd("<b>A firm that grows without him doing everything.</b> Systems and eventually a team — not just a job he owns."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No digital presence.</b> Zero paid ads, zero local pack visibility, estimated 0–3 Google reviews."))
story.append(b("<b>Solo capacity ceiling.</b> Every function — intake, casework, admin — runs through Drake personally."))
story.append(b("<b>No intake system.</b> All inquiries managed manually; no after-hours coverage; no follow-up protocol."))
story.append(b("<b>Review gap.</b> O'Dell has 16 reviews, Renner has 23, Banks &amp; Brower has 893 — Drake has almost none."))
story.append(b("<b>Brand-new firm.</b> No market recognition in Plainfield or Hendricks County under his own name."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("His name appears above O'Dell and Renner in search results — for the first time."))
story.append(bd("Cases start arriving from strangers who found him online and chose him — not from people who already know him."))
story.append(bd("He builds an independent client base that exists whether or not Banks &amp; Brower keeps referring to him."))

story.append(Paragraph("<b>Full Service Marketing Essentials  |  $3,397/mo bundled</b>", S["subsection"]))
story.append(b("Family law in an Indianapolis suburb requires PPC + LSA to compete — both channels confirmed as priority by competitive research."))
story.append(b("Website content and PageSpeed unverified — optimization included to ensure ads convert the traffic they bring in."))
story.append(b("Essentials tier is correct for this revenue range ($250K–$400K); ad spend cap $7,500/mo gives room to grow."))
story.append(b("Includes LSA setup and Google Screened verification — positions Drake above every other ad format on Google."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("He gets the business-owner framework he never needed inside Banks &amp; Brower but now needs to build alone."))
story.append(bd("Intake protocol, pricing, and financial tracking get built from day one — not after problems accumulate."))
story.append(bd("Accountability and peer benchmarks from a community of law firm owners replace the isolation of going solo."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Solo attorney, Stage 3, no prior business-owner experience — Elite Coach provides essential structure at the right price."))
story.append(b("Under $400K revenue: Elite Coach is the correct tier; Master's Circle requires $1M+ and 5+ dedicated staff."))
story.append(b("Weekly group coaching directly addresses Drake's three critical gaps: intake, team-building, and profit planning."))
story.append(b("Peer community replaces the mentorship and accountability he had inside a large firm — without the ceiling."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Law Office of Drake Spears — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns his digital investment into a lead engine — cases come in even when Drake is in court or with a client."))
story.append(bd("Ends dependence on referrals from people who know him from his prior employer."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,500/mo — Family Law channel minimums: PPC $3,500 + LSA $2,000."))
story.append(b("<b>Aggressive:</b> $6,500/mo — adds Meta lead gen $1,000; targets 2x revenue goal."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~8 cases x $4K avg = ~$30K/mo vs. $5.5K spend = 5.5x return. (Avg case value est.; confirm on call.)"))
story.append(b("<b>Aggressive:</b> ~11 cases x $4K avg = ~$42K/mo vs. $6.5K spend = 6.5x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Avg case value unconfirmed — default used.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Family Law minimums: PPC $3,500 + LSA $2,000 = $5,500. Within Essentials $7,500 cap."))
story.append(b("<b>Aggressive:</b> $500K goal x 20% / 12 = $8,333. Tier 3 (1.15x) = $9,583. Minus $3,397 fee = $6,186. Use $6,500."))
story.append(b("<b>35% cap check:</b> Confirm actual revenue on call before presenting ad spend. At $250K rev, combined fees + ads exceed cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I\'m not sure I\'m ready to spend this much on marketing."', S["objection_q"]))
story.append(Paragraph("Urgency score is 7/10. O'Dell (16 reviews), Renner (23 reviews), and Banks &amp; Brower (893 reviews) are all running in Drake's exact market right now. Every month without a counter-presence is a month they extend their lead.", S["objection_a"]))

story.append(Paragraph('"I\'m still new — I want to build gradually."', S["objection_q"]))
story.append(Paragraph("Being new is the advantage. No legacy campaigns to unwind, no bad reviews to overcome — just a clean slate to build the right digital presence from day one, before competitors lock up the local pack permanently.", S["objection_a"]))

story.append(Paragraph('"I don\'t know my numbers well enough yet."', S["objection_q"]))
story.append(Paragraph("That is exactly what Elite Coach's month-one financial tracking and retainer pricing framework is built to fix. The goal is to know those numbers before the decisions need to be made — not after.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Essentials</b>", S["price_main"]),
     Paragraph("$3,397/mo", S["price_main"])],
    [Paragraph("Website, Google Ads, LSA, local SEO — all channels for Hendricks County.", S["price_detail"]),
     Paragraph("No stand-alone price", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Group coaching, masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,500–$6,500/mo", S["price_main"])],
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
    "Total: $5,997/mo + $5,500–$6,500 ad spend  |  Save $897/mo by bundling  |  CONFIRM REVENUE ON CALL before presenting ad spend (35% cap applies)",
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
