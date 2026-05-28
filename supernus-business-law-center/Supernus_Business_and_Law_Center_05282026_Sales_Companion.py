"""
Sales Companion PDF — SMB Team
Supernus Business & Law Center | May 28, 2026 | Rep: Dan Bryant
FOR INTERNAL USE ONLY; DO NOT SHARE.
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

OUTPUT_PATH = "supernus-business-law-center/Supernus_Business_and_Law_Center_05282026_Sales_Companion.pdf"


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

story.append(Paragraph("Supernus Business &amp; Law Center", S["title"]))
story.append(Paragraph("Sales Companion  |  May 28, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Jedediah McClure", S["snap_value"]),
     Paragraph("Not confirmed (confirm on call)", S["snap_value"]),
     Paragraph("Solo — 1 atty", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Sycamore, IL", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: PROTECTION &amp; LEGACY", S["section"]))
story.append(Paragraph("Jedediah wants the firm to generate consistent income and protect his clients without requiring his constant personal involvement in every step.", S["subsection"]))

# No transcript available — use website-inferred signals instead of quote_block
story.append(quote_block("Protect What You Have Built. Plan for What Comes Next. (Website headline — reflects DBM directly)"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable clients.</b> A system bringing in business owners searching for asset protection — not whoever happens to refer next."))
story.append(bd("<b>Protected firm.</b> A practice that runs even when he is not present — consistent with succession planning he builds for clients."))
story.append(bd("<b>Ownership of his time.</b> Focus on high-value legal work rather than intake, scheduling, and admin tasks."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No paid digital presence.</b> No Google Ads, LSA, or Meta — zero paid visibility for any practice area."))
story.append(b("<b>Solo operation.</b> Every function flows through one person — no capacity to grow without growing personal hours."))
story.append(b("<b>No revenue baseline.</b> Revenue unconfirmed — cannot validate ad spend cap until confirmed on call."))
story.append(b("<b>NAP inconsistency.</b> Avvo shows 735 Independence Ave; all other platforms show 212 S Main St — suppresses local SEO."))
story.append(b("<b>Buried contact form.</b> Strategy session CTA on homepage but form requires multiple navigation clicks to reach."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts the firm at the top of Google for estate planning, asset protection, and business attorney searches in DeKalb/Kane County before any local competitor does."))
story.append(bd("Converts 239 five-star reviews into an LSA listing above all organic and paid results — pay per lead, not per click."))
story.append(bd("Reaches business owners on Facebook/Instagram at the exact life moments that trigger legal planning decisions."))

story.append(Paragraph("<b>Full Service Marketing Essentials  |  $3,397/mo bundled</b>", S["subsection"]))
story.append(b("Practice areas are estate planning, business law, asset protection — Essentials tier fully eligible (not PI or high-competition criminal)."))
story.append(b("No local competitor running paid search or LSA for any practice area — first-mover advantage available now."))
story.append(b("Revenue est. $250K–$400K (confirm on call); Essentials cap $7,500 covers recommended $6,500–$7,000. Revenue under $300K requires scoping approval."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the intake process, revenue baseline, and team foundation — turning incoming leads into a scalable practice, not just more personal work."))
story.append(bd("Connects him with attorneys at the same stage building the same systems — estate planning and business law solos moving from Stage 3 to Stage 4."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Solo practitioner — Elite Coach is appropriate tier; Master's Circle requires 5+ team members."))
story.append(b("Includes weekly coaching, practice area masterminds, quarterly workshops, annual in-person event."))
story.append(b("Saves $897/mo bundled vs. $3,497 stand-alone."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Supernus Business &amp; Law Center — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Places the firm at the top of search results for estate planning, asset protection, and business planning in DeKalb/Kane County — generating inbound leads from clients actively searching for what this firm does."))
story.append(bd("Turns the first-mover window in a quiet local market into a sustainable pipeline before any competitor claims those paid search positions."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $6,500/mo — Google PPC ($3,500) + LSA ($2,000) + Meta Retargeting ($1,200)."))
story.append(b("<b>Aggressive:</b> $7,000/mo — adds Meta lead gen; within Essentials $7,500 cap."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 7 cases x $5,000 = $35,000/mo vs. $6,500 spend = 5.4x. (Estimates — confirm case value on call.)"))
story.append(b("<b>Aggressive:</b> 10 cases x $5,000 = $50,000/mo vs. $7,000 spend = 7.1x. (Estimates — confirm case value on call.)"))

story.append(Paragraph("<b>How calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Estate Planning channel minimums: PPC $3,500 + LSA $2,000 + Meta Ret $1,200 = $6,700, rounded to $6,500."))
story.append(b("<b>Aggressive:</b> $600K goal x 20% / 12 = $10K. Tier 4 (1.0x). Minus $3,397 fee = $6,603; rounded to $7,000."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I get most of my clients from referrals — my reputation speaks for itself."', S["objection_q"]))
story.append(Paragraph("239 reviews at 5.0 stars confirm strong satisfaction. But referrals cannot be forecasted or scaled, and they do not reach business owners actively searching Google for an asset protection attorney in DeKalb County right now. Paid ads reach that audience.", S["objection_a"]))

story.append(Paragraph('"I\'m not sure I have the capacity to handle more clients right now."', S["objection_q"]))
story.append(Paragraph("Coaching is paired with marketing for exactly this reason. Elite Coach builds the intake process and delegation framework so capacity grows alongside lead volume — systems first, then spend accelerates.", S["objection_a"]))

story.append(Paragraph('"The market is small — will ads actually work in Sycamore?"', S["objection_q"]))
story.append(Paragraph("Small market means low CPCs and almost no competition. No local firm is running Google Ads or LSA for estate planning or asset protection. The firm that activates first owns those positions and will be very difficult to displace.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Essentials</b>", S["price_main"]),
     Paragraph("$3,397/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta Ads, website optimization, local SEO.", S["price_detail"]),
     Paragraph("No stand-alone price listed", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$6,500–$7,000/mo", S["price_main"])],
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
    "Total: $5,997/mo + $6,500–$7,000 ad spend  |  Save $897/mo by bundling  |  ~26%–39% of revenue (confirm revenue to validate cap)",
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
