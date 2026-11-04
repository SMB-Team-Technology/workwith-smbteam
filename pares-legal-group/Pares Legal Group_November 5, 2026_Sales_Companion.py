"""
Sales Companion PDF Template — SMB Team
========================================
This template generates the 2-page internal Sales Companion PDF for the sales rep.
It uses reportlab. Do not modify the layout, colors, fonts, styles, or structure.
Only replace the # FILL: placeholders with audit-specific content.

IMPORTANT: The final PDF must be exactly 2 pages. If content overflows to a third
page, shorten bullet text — do not remove sections.

All bullet text must be scannable: one idea per bullet, 8th-grade reading level.
Each "What it does for her/him:" bullet states the transformation, not the deliverable.
Each scoping rationale bullet states one fact with one conclusion.

Output filename: [FirmName]_[Date]_Sales_Companion.pdf
  - FirmName: spaces replaced with underscores
  - Date: MMDDYYYY format
  - Save to the root of the project folder (same location as the Growth Audit HTML)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Fonts — SMB Team brand font is Poppins. Embedded so it renders the
# same regardless of what's installed on the machine opening the PDF. ──
_FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "Design Files", "fonts")
pdfmetrics.registerFont(TTFont("Poppins", os.path.join(_FONT_DIR, "Poppins-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Bold", os.path.join(_FONT_DIR, "Poppins-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Italic", os.path.join(_FONT_DIR, "Poppins-Italic.ttf")))
pdfmetrics.registerFontFamily(
    "Poppins", normal="Poppins", bold="Poppins-Bold",
    italic="Poppins-Italic", boldItalic="Poppins-Bold",
)

# ── Colors — SMB Team brand colors (Deep Wood Blue, Ocean Blue) plus the
# existing semantic grays/reds/savings-green, which stay as they were. ──
DARK_NAVY = HexColor("#003A59")     # Deep Wood Blue — brand primary
SECTION_BLUE = HexColor("#0091C9")  # Ocean Blue — brand accent, section headers
ACCENT_GREEN = HexColor("#3B6D11")  # savings/positive-outcome green — matches the audit report
MEDIUM_GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#888888")
RULE_GRAY = HexColor("#CCCCCC")
QUOTE_BG = HexColor("#F5F7F0")
WHITE = HexColor("#FFFFFF")
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "pares-legal-group/Pares Legal Group_November 5, 2026_Sales_Companion.pdf"


def add_page_elements(canvas, doc):
    """Draws red warning header and confidential footer on every page. DO NOT MODIFY."""
    canvas.saveState()
    width, height = letter
    canvas.setFont("Poppins-Bold", 10)
    canvas.setFillColor(RED_WARNING)
    canvas.drawCentredString(width / 2, height - 0.38 * inch,
                             "FOR INTERNAL USE ONLY; DO NOT SHARE.")
    canvas.setStrokeColor(RED_WARNING)
    canvas.setLineWidth(0.5)
    canvas.line(0.6 * inch, height - 0.44 * inch,
                width - 0.6 * inch, height - 0.44 * inch)
    canvas.setFont("Poppins", 7)
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
    "title", fontName="Poppins-Bold", fontSize=16, leading=20,
    textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle(
    "subtitle", fontName="Poppins", fontSize=9.5, leading=13,
    textColor=LIGHT_GRAY, spaceAfter=3)
S["section"] = ParagraphStyle(
    "section", fontName="Poppins-Bold", fontSize=11, leading=15,
    textColor=SECTION_BLUE, spaceBefore=6, spaceAfter=2)
S["subsection"] = ParagraphStyle(
    "subsection", fontName="Poppins-Bold", fontSize=10, leading=13,
    textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle(
    "bullet", fontName="Poppins", fontSize=9.5, leading=13,
    textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0,
    spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle(
    "bullet_dark", fontName="Poppins", fontSize=9.5, leading=13,
    textColor=DARK_NAVY, leftIndent=12, bulletIndent=0,
    spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle(
    "quote", fontName="Poppins-Italic", fontSize=9.5, leading=13,
    textColor=DARK_NAVY, leftIndent=6, rightIndent=6,
    spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle(
    "snap_label", fontName="Poppins-Bold", fontSize=8.5, leading=11,
    textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle(
    "snap_value", fontName="Poppins", fontSize=9.5, leading=12,
    textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle(
    "objection_q", fontName="Poppins-Bold", fontSize=9.5, leading=13,
    textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle(
    "objection_a", fontName="Poppins", fontSize=9.5, leading=13,
    textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle(
    "price_main", fontName="Poppins-Bold", fontSize=9.5, leading=13,
    textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle(
    "price_detail", fontName="Poppins", fontSize=8.5, leading=12,
    textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle(
    "savings", fontName="Poppins-Bold", fontSize=9.5, leading=13,
    textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle(
    "disclaimer", fontName="Poppins-Italic", fontSize=8.5, leading=11,
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

story.append(Paragraph("Pares Legal Group", S["title"]))
story.append(Paragraph("Sales Companion  |  November 5, 2026  |  Rep: Daniel Lowe", S["subtitle"]))
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
    [Paragraph("Carlos Parés", S["snap_value"]),
     Paragraph("Not stated on call (HubSpot: $0&ndash;$180K)", S["snap_value"]),
     Paragraph("2&ndash;3", S["snap_value"]),
     Paragraph("3", S["snap_value"]),
     Paragraph("Not stated (15% default)", S["snap_value"]),
     Paragraph("Orlando, FL + Puerto Rico", S["snap_value"])],
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
story.append(Paragraph("Carlos wants to double his caseload without losing his relaxed, low-stress life.", S["subsection"]))

story.append(quote_block("I enjoy my relaxness."))
story.append(Spacer(1, 1))
story.append(quote_block("Instead of having five, maybe I can go to 10, 20, but never sacrificing my mental health."))
story.append(Spacer(1, 1))
story.append(quote_block("I'm the product. So I'm selling myself."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>A landing page and e-book.</b> A page in his brand colors that sells the e-book and books paid consults."))
story.append(bd("<b>AI inside the firm.</b> Automate intake and onboarding on one secure platform."))
story.append(bd("<b>More cases, same pace.</b> Four or five a month today, maybe 10 or 20."))
story.append(bd("<b>One clear decision.</b> Pick the path once and avoid a data mess."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No owned destination.</b> TV and social bring leads, but there is no landing page or e-book funnel."))
story.append(b("<b>Manual intake.</b> Intake and onboarding are hands-on for a team of two or three."))
story.append(b("<b>Informal AI use.</b> Personal Claude and ChatGPT in the office, no single platform."))
story.append(b("<b>Doubts about Google.</b> He said he does not need SEO or Ads and fears fake reviews."))
story.append(b("<b>Price-sensitive.</b> He is a &quot;numbered person&quot; and wants a &quot;very starter package.&quot;"))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives his TV and social attention a landing page that books paid consults."))
story.append(bd("Puts Spanish-language paid social behind the e-book without more of his time."))
story.append(bd("Monthly reporting shows cost per consult so he can set the pace."))

story.append(Paragraph("<b>Full Service Marketing Essentials  |  $3,797/mo (stand-alone price)</b>", S["subsection"]))
story.append(b("Seller override (Slack, 11/4). Rules would give Starter: 2 locations, several practice areas."))
story.append(b("Revenue is unverified. Under $250K: confirm 4 months of funds. Under $300K: scoping approval."))
story.append(b("He wants a &quot;very starter package&quot; and no Google, so lead with the landing page and Meta."))
story.append(b("Only one bundle-eligible product, so no bundle discount applies."))

story.append(thin_rule())

# ── Why This AI Workforce Package (replaces Coaching section: seller dropped coaching) ──
story.append(Paragraph("Why This AI Workforce Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Replaces ad hoc ChatGPT and Claude use with one managed AI workspace."))
story.append(bd("Starts with intake and onboarding, the first thing he wants automated."))
story.append(bd("A weekly session keeps the rollout moving without him leading it."))

story.append(Paragraph("<b>AI Workforce Pro &ndash; Starter (1 user)  |  $350/mo</b>", S["subsection"]))
story.append(b("Seats unconfirmed. Daniel quoted $350/seat and gave 3 seats as an example. Priced at 1."))
story.append(b("Starter covers 1&ndash;4 users; 5+ users moves to AI Workforce Pro at $1,597/mo. Month-to-month."))
story.append(b("Confirm LAW delivery has launched and has capacity before sending."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Pares Legal Group — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives his e-book and consult page paid reach in the Spanish-speaking audience he serves."))
story.append(bd("Sets a tested cost per consult before he commits to a bigger budget."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000/mo &mdash; the minimum for paid ads, on one Meta channel."))
story.append(b("<b>Aggressive:</b> $6,500/mo &mdash; 20% rule, under the $7,500 Essentials cap."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~5 cases x $4.5K = ~$22.5K/mo vs. $3K spend = 7.5x return."))
story.append(b("<b>Aggressive:</b> ~14 cases x $4.5K = ~$63K/mo vs. $6.5K spend = 9.7x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Case value ($4.5K, midpoint of the $3K&ndash;$6K immigration default) and 15% close rate were not confirmed on the call.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Immigration minimums are Google $3,000, Meta lead gen $3,000, LSA $2,000. One Meta channel at $3,000; cold CPL $75 + 20% cushion = $90, about 33 leads."))
story.append(b("<b>Aggressive:</b> $360K target (2x revenue, no goal stated) x 20% &divide; 12 = $6,000. Tier 2 Orlando (1.3x) = $7,800. Spanish x1.33 = $10,374. Minus $3,797 fee = $6,577, shown as $6,500. Reverse math gave about $3,100, so the 20% rule governs."))
story.append(b("The decision file's $12,000 aggressive figure broke the $7,500 cap, so it was recomputed."))
story.append(b("<b>Cap check:</b> total at conservative is $7,147/mo (47.6% of revenue). At aggressive it is $10,647/mo (71.0%). Both are over the 35% cap of $5,250 on $180K. Review with the rep."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I don\'t need Google SEO or Ads."', S["objection_q"]))
story.append(Paragraph("Agree. His leads come from TV and social, so lead with the landing page and Meta. Google stays optional.", S["objection_a"]))

story.append(Paragraph('"Competitors go to your Google reviews and start putting fake comments." [0:23:50]', S["objection_q"]))
story.append(Paragraph("Do not pitch review growth. Offer clean, consistent business details instead, since his name and address vary across sources.", S["objection_a"]))

story.append(Paragraph('"I\'m a numbered person at end of the day." [0:18:33]', S["objection_q"]))
story.append(Paragraph("Fees are $4,147/mo: $3,797 marketing plus $350 AI. Confirm revenue first, because fees are about 28% of $180K a year. Anchor on cost per booked consult.", S["objection_a"]))

story.append(Paragraph('"I want to make sure this is the pathway to go." [0:11:03]', S["objection_q"]))
story.append(Paragraph("He is open to Microsoft Copilot. Start with 1 seat, month-to-month, one platform, and a weekly session. Do not promise outcomes.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Essentials</b>", S["price_main"]),
     Paragraph("$3,797/mo", S["price_main"])],
    [Paragraph("Landing page, paid social, local SEO and reporting.", S["price_detail"]),
     Paragraph("$3,797 stand alone (no discount)", S["price_detail"])],
    [Paragraph("<b>AI Workforce Pro &ndash; Starter (1 user)</b>", S["price_main"]),
     Paragraph("$350/mo", S["price_main"])],
    [Paragraph("Managed AI workspace and weekly implementation session.", S["price_detail"]),
     Paragraph("No stand-alone price", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000&ndash;$6,500/mo", S["price_main"])],
    [Paragraph("Goes to Meta (Google and LSA only if he opts in) — not to SMB Team.", S["price_detail"]),
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
    "Total: $4,147/mo + $3,000&ndash;$6,500 ads  |  No bundle savings  |  47.6%&ndash;71.0% of revenue (over 35% cap)",
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
