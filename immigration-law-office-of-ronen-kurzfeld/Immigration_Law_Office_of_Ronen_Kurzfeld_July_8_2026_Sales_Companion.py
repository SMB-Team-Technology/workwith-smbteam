"""
Sales Companion PDF — Immigration Law Office of Ronen Kurzfeld
Sales Rep: Randy Gold | Date: July 8, 2026
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

OUTPUT_PATH = "immigration-law-office-of-ronen-kurzfeld/Immigration_Law_Office_of_Ronen_Kurzfeld_07082026_Sales_Companion.pdf"


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

story.append(Paragraph("Immigration Law Office of Ronen Kurzfeld", S["title"]))
story.append(Paragraph("Sales Companion  |  July 8, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Ronen Kurzfeld", S["snap_value"]),
     Paragraph("$2–3M CAD", S["snap_value"]),
     Paragraph("15 (7 atty + 8 offshore)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Toronto, ON", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 1.3*inch, 0.6*inch, 0.9*inch, 1.05*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 4))

# ── Dominant Buying Motive ──
story.append(Paragraph("Dominant Buying Motive: FREEDOM THROUGH DELEGATION", S["section"]))
story.append(Paragraph("Delegate intake and billing so the firm grows to $4–5M CAD without Ronen in the middle of every function.", S["subsection"]))

story.append(quote_block("Implement systems that enable delegation of intake and billing, which Ronen currently handles."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Intake off his plate.</b> His primary stated systems goal — lead with this."))
story.append(bd("<b>Billing off his plate.</b> He chases invoices personally; wants a system that replaces him here."))
story.append(bd("<b>Revenue to $4–5M CAD.</b> Stated goal; sees it as achievable with the right systems in place."))
story.append(bd("<b>A firm that runs without him.</b> Freedom is the destination — not just revenue growth."))

story.append(Spacer(1, 1))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Lead collapse.</b> Organic page 6+, Maps inconsistent, PPC ineffective — lead flow down ~50%."))
story.append(b("<b>No intake process.</b> Delegation without a documented process transfers chaos, not function."))
story.append(b("<b>Broken case management.</b> Monday.com failures: missed deadlines and lost leads."))
story.append(b("<b>Collections leaking.</b> Unpaid invoices and expired credit cards with no automated recovery."))
story.append(b("<b>AI risk exposure.</b> Unstructured AI use by lawyers creates fabricated citation liability."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Restores lead flow — without leads, there is nothing to delegate and no path to $4–5M CAD."))
story.append(bd("Builds a multi-channel system that runs without Ronen managing it daily."))
story.append(bd("Recovery plan while Mamann (783 reviews) and Matkowsky (600+ reviews) extend their digital lead."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $7,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $2–3M CAD confirmed on call — solidly Growth tier ($1M–$3M)."))
story.append(b("All three channels failed simultaneously; full-service coordinated approach required."))
story.append(b("Dual domains (immigrationway.com + kurzfeldlawfirm.com) split SEO authority; NAP inconsistencies suppress Maps."))
story.append(b("Growth tier ad cap ($12,000/mo) matches aggressive scenario; $3,000 conservative is viable start."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Ronen the framework to build delegation structures for intake and billing — the plan, not just the goal."))
story.append(bd("Connects him to immigration firm owners who have already solved his exact delegation challenge."))
story.append(bd("Accountability for the milestones that move him from intake bottleneck to firm owner."))

story.append(Paragraph("<b>Master's Circle  |  $4,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1M+ and 15-person team — eligible; verify dedicated ops capacity with Randy Gold before presenting."))
story.append(b("Stated goal is operational delegation — this package is built for owners at exactly this stage."))
story.append(b("Immigration law coaching specialists address his practice area and delegation context directly."))
story.append(b("Annual in-person workshop delivers the deep-dive needed to build the leadership layer he is missing."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Kurzfeld Immigration — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Restores paid lead flow immediately while organic and Maps recovery (months-long process) gets underway."))
story.append(bd("Builds PPC + LSA + Meta presence that Mamann and Matkowsky already hold — this firm does not."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000/mo — PPC + LSA + Meta retargeting minimums for Toronto immigration."))
story.append(b("<b>Aggressive:</b> $12,000/mo — Growth tier cap; full PPC + LSA + Meta lead gen with multilingual targeting."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~3 cases x $5K = $15,000/mo vs. $3,000 spend = 5x return (est.)."))
story.append(b("<b>Aggressive:</b> ~16 cases x $5K = $80,000/mo vs. $12,000 spend = 7x return (est.)."))
story.append(Paragraph("<i>Estimates only. Case value = practice area default ($5K USD, not stated on call). Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Immigration channel minimums: PPC $1K + LSA $1K + Meta $1.2K = ~$3,200 → $3,000."))
story.append(b("<b>Aggressive:</b> $4.5M CAD (~$3.29M USD) x 20% / 12 x 1.5 (Tier 1 Toronto) = $82K; Growth cap $12,000 applies."))
story.append(b("Total aggressive: $11,997 + $12,000 = $23,997/mo = ~15.8% of revenue — under 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"My PPC is already not working — why would more spend fix it?"', S["objection_q"]))
story.append(Paragraph("The problem is the infrastructure, not the spend. Broad 'immigration lawyer' terms pit this firm against Mamann (30-yr domain authority) and Matkowsky (confirmed remarketing). The fix: rebuild campaigns around practice-area keywords (Express Entry, spousal sponsorship) with dedicated landing pages. Same budget, 3–5x the conversion rate.", S["objection_a"]))

story.append(Paragraph('"I\'m not sure I need both packages."', S["objection_q"]))
story.append(Paragraph("The lead problem and delegation problem feed each other. More leads without intake delegation = Ronen handles more consultations personally. Delegation without leads = systematizing an empty pipeline. Both must be solved together. Bundle saves $1,997/month vs. buying separately.", S["objection_a"]))

story.append(Paragraph('"We have 371 reviews. Why aren\'t we ranking?"', S["objection_q"]))
story.append(Paragraph("The review count is strong (Bellissimo: 100, Guberman: 38). But three structural issues suppress it independent of reviews: (1) NAP inconsistencies — 3 phone numbers, 2 addresses across platforms; (2) dual domains splitting 20 years of link authority; (3) GBP posts not confirmed active. Fix structure first; then the 371 reviews do their full work.", S["objection_a"]))

story.append(Paragraph('"Can we start with just marketing and add coaching later?"', S["objection_q"]))
story.append(Paragraph("Workable, but flag: delegating intake and billing is a coaching outcome, not a marketing outcome. Marketing restores leads. Without Master's Circle, leads come back and Ronen handles them personally — same bottleneck. Bundle saves $1,997/mo vs. sequential purchase.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("Website rebuild, Local SEO, Google Ads, LSA, Meta — full multi-channel recovery.", S["price_detail"]),
     Paragraph("<strike>$8,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle</b>", S["price_main"]),
     Paragraph("$4,600/mo", S["price_main"])],
    [Paragraph("Weekly coaching, immigration masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("<strike>$4,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000–$12,000/mo", S["price_main"])],
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
    "Total: $11,997/mo + $3,000–$12,000 ad spend  |  Save $1,997/mo by bundling  |  ~15.8% of revenue at aggressive (under 35% cap)",
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
