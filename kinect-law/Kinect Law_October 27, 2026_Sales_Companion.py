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
_FONT_DIR = "Design Files/fonts"
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

OUTPUT_PATH = "kinect-law/Kinect Law_October 27, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Kinect Law (Law Offices of Albert Wai-Kit Chan, PLLC)", S["title"]))
story.append(Paragraph("Sales Companion  |  October 27, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Robert D. Katz (partner contact)", S["snap_value"]),
     Paragraph("Not stated ($961K–$3M, HubSpot)", S["snap_value"]),
     Paragraph("4 partners", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("Not stated (15% default)", S["snap_value"]),
     Paragraph("Whitestone, NY", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SECURITY", S["section"]))
story.append(Paragraph("A predictable pipeline of high-value B2B clients so revenue stabilizes and the firm stops depending on referrals (inferred, not stated).", S["subsection"]))

story.append(quote_block("Fathom summary: The firm needs a predictable pipeline of high-value B2B clients (e.g., litigation, startups) to stabilize revenue."))
story.append(Spacer(1, 1))
story.append(quote_block("Fathom summary: Kinect Law's lead generation is inconsistent, relying on word-of-mouth."))
story.append(Spacer(1, 1))
story.append(quote_block("Fathom summary: Desired clients are high-value B2B work, not low-fee Amazon filings."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What they want:</b>", S["subsection"]))
story.append(bd("<b>Predictable pipeline.</b> New matters should not hinge on who refers the firm next."))
story.append(bd("<b>The right clients.</b> Biotech and pharma startups, trademark-heavy brands, and IP litigation."))
story.append(bd("<b>Wider reach.</b> Visibility in Manhattan, Westchester, Nassau, and Brooklyn, not just Whitestone."))
story.append(bd("<b>Stable cash flow.</b> Steadier revenue despite slow-paying clients."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping them:</b>", S["subsection"]))
story.append(b("<b>No marketing budget.</b> A $5-6K/mo spend is a \"big nut\" for the firm."))
story.append(b("<b>Partner alignment.</b> Partners must agree on the investment before committing."))
story.append(b("<b>Weak online footprint.</b> Old GBP name, no reviews or photos, no location pages."))
story.append(b("<b>No financial plan.</b> No formal budget or projections, and cash flow is tight."))
story.append(b("<b>Slow SEO payoff.</b> Results take 6-12 months."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Makes Kinect Law findable for the IP searches their ideal B2B clients run."))
story.append(bd("Replaces referral timing with an organic pipeline the partners control."))
story.append(bd("Builds trust for first-time searchers with a clean profile, reviews, and local pages."))

story.append(Paragraph("<b>Web + SEO Growth  |  $5,897/mo (stand-alone rate)</b>", S["subsection"]))
story.append(b("Call focus was long-term SEO and AEO: GBP cleanup, Areas We Serve pages, Q&amp;A content."))
story.append(b("Seller locked Web + SEO Growth, no coaching. Rulebook prefers a coaching pair; seller choice applied."))
story.append(b("Sits at the top of the $5-6K/mo budget the partners discussed. No ad spend."))

story.append(thin_rule())

# ── Why Not Coaching ──
story.append(Paragraph("Coaching Package: Not Included", S["section"]))

story.append(Paragraph("<b>Why it is out for now:</b>", S["subsection"]))
story.append(bd("One defined line item is easier for the partners to approve than a bundle."))
story.append(bd("Call was about marketing, not coaching or operations."))

story.append(Paragraph("<b>Elite Coach Plus was dropped at seller request (Slack, 10/27)</b>", S["subsection"]))
story.append(b("Roadmap Phase 2 adds an FCOO Advisor ($3,297/mo) once organic inquiries are steady."))
story.append(b("Rep mentioned fractional CFO for profit planning; it is a Phase 3 add, not priced here."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Kinect Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Ad Spend ──
story.append(Paragraph("Ad Spend: None Recommended", S["section"]))

story.append(Paragraph("<b>Why this keeps the plan simple:</b>", S["subsection"]))
story.append(bd("Web + SEO has no paid ads, so the partners only weigh one monthly figure."))
story.append(bd("Rep's view on the call: Google PPC is ineffective for B2B; organic search and social build the brand better."))

story.append(Paragraph("<b>What was not calculated:</b>", S["subsection"]))
story.append(b("<b>Ad spend range and ROI:</b> not projected. No paid package is in the proposal."))
story.append(b("<b>If ads come up later:</b> run channel minimums and the 20% rule with the paid ads team first."))
story.append(b("<b>Missing data:</b> revenue, case value, and close rate were not stated on the call."))
story.append(Paragraph("<i>No ROI figures are quoted to the prospect. Anything shared later must be labeled an estimate.</i>", S["disclaimer"]))

story.append(Paragraph("<b>Before the call:</b>", S["subsection"]))
story.append(b("<b>Review counts:</b> all competitor counts are unconfirmed. Verify live on Google before citing any."))
story.append(b("<b>PageSpeed:</b> 61 mobile / 94 desktop came from a local Lighthouse run. Re-run on pagespeed.web.dev."))
story.append(b("<b>Not observed:</b> 3-pack, Google Ads, LSA, and Meta data. Urgency score of 5 is provisional."))

story.append(thin_rule())

# ── If They Push Back ──
story.append(Paragraph("If They Push Back", S["section"]))

story.append(Paragraph('"$5,897 a month is a big nut with no marketing budget."', S["objection_q"]))
story.append(Paragraph("It is one line item with no ad spend and no coaching bundle. It sits inside the $5-6K range discussed on the call. Rep offered a recap the partners can use for their firm discussion.", S["objection_a"]))

story.append(Paragraph('"How long until we see results?"', S["objection_q"]))
story.append(Paragraph("SEO takes 6-12 months, as discussed on the call. Early steps are visible sooner: a corrected GBP, review requests going out, and new location pages going live. Do not promise lead counts.", S["objection_a"]))

story.append(Paragraph('"Referrals have worked for years. Why change?"', S["objection_q"]))
story.append(Paragraph("The summary says lead flow is inconsistent. Sisun Law, De Rose &amp; Surico, and Pollak &amp; Slepian already appear in trademark directory results where Kinect Law does not. Do not cite review counts until verified.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Web + SEO Growth</b>", S["price_main"]),
     Paragraph("$5,897/mo", S["price_main"])],
    [Paragraph("Website and SEO only: GBP, location pages, AEO content, reviews. No paid ads.", S["price_detail"]),
     Paragraph("stand-alone rate, no bundle", S["price_detail"])],
    [Paragraph("<b>Coaching Package</b>", S["price_main"]),
     Paragraph("Not included", S["price_main"])],
    [Paragraph("Elite Coach Plus dropped at seller request on 10/27.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("None", S["price_main"])],
    [Paragraph("Web + SEO includes no paid media. Revisit once organic is working.", S["price_detail"]),
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
    "Total: $5,897/mo  |  No bundle savings (stand-alone rate)  |  2.4%–7.4% of monthly revenue at the HubSpot band (under 35% cap)",
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
