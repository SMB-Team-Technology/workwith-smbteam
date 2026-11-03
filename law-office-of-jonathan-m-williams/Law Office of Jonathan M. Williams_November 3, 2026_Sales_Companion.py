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

OUTPUT_PATH = "law-office-of-jonathan-m-williams/Law Office of Jonathan M. Williams_November 3, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Law Office of Jonathan M. Williams", S["title"]))
story.append(Paragraph("Sales Companion  |  November 3, 2026  |  Rep: Cathy Tran", S["subtitle"]))
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
    [Paragraph("Jonathan M. Williams", S["snap_value"]),
     Paragraph("~$85K gross (est.)", S["snap_value"]),
     Paragraph("1 (solo)", S["snap_value"]),
     Paragraph("3", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("Harvey, LA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: A STEADY CASE FLOW", S["section"]))
story.append(Paragraph("Jonathan wants a constant flow of cases so he can stop relying on word of mouth and eventually hire help (inferred; no direct quote).", S["subsection"]))

story.append(quote_block("I know that I do need to do something different than just relying upon word of mouth."))
story.append(Spacer(1, 1))
story.append(quote_block("I would have to have a constant flow of cases."))
story.append(Spacer(1, 1))
story.append(quote_block("I would see improvement in my bottom line."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>More personal injury cases.</b> &ldquo;More cases, absolutely.&rdquo; He handles about two a month and could take five more."))
story.append(bd("<b>A source beyond referrals.</b> Word of mouth is the main source, and he cannot track it."))
story.append(bd("<b>Help, eventually.</b> He said &ldquo;Ultimately, yes&rdquo; to growing so he can hire."))
story.append(bd("<b>A better bottom line.</b> He has no revenue goal yet, only the wish to improve it."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No budget or goal.</b> &ldquo;I didn&rsquo;t consider a budget for it.&rdquo; No revenue target is set."))
story.append(b("<b>Small revenue.</b> About $85K gross. The package is about 61% of his monthly revenue."))
story.append(b("<b>He is alone.</b> No staff to run marketing, intake, or follow-up."))
story.append(b("<b>Past ads gave views.</b> His Facebook ads gave &ldquo;more views,&rdquo; and social is untracked."))
story.append(b("<b>Site built once.</b> A vendor built it and he adds no content."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Injury clients in Jefferson Parish can find his site and Google profile."))
story.append(bd("He gets a source of cases beyond people who already know him."))
story.append(bd("It builds the foundation first, with no ad spend at risk."))

story.append(Paragraph("<b>Web + SEO Starter  |  $3,997/mo stand-alone (no bundle discount)</b>", S["subsection"]))
story.append(b("Seller override (Slack, Nov 3): Web + SEO Starter, no coaching. Reps advised against paid ads."))
story.append(b("Starter is normally a $500K+ tier. He is near $85K gross, so expect a price conversation."))
story.append(b("The site is new (Lighthouse 65 mobile, 97 desktop). Scope is pages, content, and Google profile."))
story.append(b("Includes 10,000 words at launch, 6,000 a year after, and 30 minutes of edits a month."))

story.append(thin_rule())

# ── Why This AI Package ──
story.append(Paragraph("Why This AI Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Email, case notes, and scheduling start coming off his plate."))
story.append(bd("He tests AI month to month, with no long-term commitment."))

story.append(Paragraph("<b>AI Workforce Pro &ndash; Starter, 1 user  |  $350/mo</b>", S["subsection"]))
story.append(b("Reps raised it on the call. No tier or price was quoted to him."))
story.append(b("It does not count toward a bundle, so Web + SEO is charged at its stand-alone price."))
story.append(b("LAW normally excludes solo firms. Seller override. Confirm LAW delivery has launched."))
story.append(b("Fractional CTO needs $400K+ revenue, so it is not an option."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Williams Law &mdash; Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No Ad Spend ──
story.append(Paragraph("Why There Is No Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("No budget is tied up before he can see where cases come from."))
story.append(bd("It leaves room to add a paid channel once inquiries are tracked."))

story.append(Paragraph("<b>Ad spend status:</b>", S["subsection"]))
story.append(b("No ad spend is in the proposal. Web + SEO carries none."))
story.append(b("Reps advised against PPC, LSA, social ads, and lead buying at this revenue."))
story.append(b("Paid ads are a Phase 2 idea only, with no number set."))

story.append(Paragraph("<b>Estimated return (internal only):</b>", S["subsection"]))
story.append(b("None modeled. Do not quote leads or cases to him."))
story.append(Paragraph("<i>No ad spend is recommended, so there is no ROI projection.</i>", S["disclaimer"]))

story.append(Paragraph("<b>Spend and cap check:</b>", S["subsection"]))
story.append(b("$4,347/mo vs. about $7,083/mo revenue = 61%. The 35% cap is $2,479/mo. Over the cap."))
story.append(b("Under $250K revenue: confirm 4 months of funds ($17,388) and get scoping approval."))
story.append(b("Case value $5K&ndash;$8K is his number. The rep&rsquo;s $2,500 figure is not his. Net revenue is unconfirmed."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"That is a lot for what I make."', S["objection_q"]))
story.append(Paragraph("It is a real commitment: about $52K a year, or 7 to 10 cases at his $5K&ndash;$8K estimate. Ask what he can afford and flag it to Cathy.", S["objection_a"]))

story.append(Paragraph('"Why not just run ads like my competitors?"', S["objection_q"]))
story.append(Paragraph("He said they &ldquo;put a lot of dollars into marketing.&rdquo; Without tracking, ad dollars leak. His Facebook ads gave &ldquo;more views.&rdquo; Build the base first.", S["objection_a"]))

story.append(Paragraph('"I just got a new website."', S["objection_q"]))
story.append(Paragraph("Agree. It is clean and fast on desktop (97). It has no pages for his parishes and no content. That is what Web + SEO adds.", S["objection_a"]))

story.append(Paragraph('"Do you work with firms in my parishes?"', S["objection_q"]))
story.append(Paragraph("He asked on the call. Open item: check for existing clients in Jefferson and Orleans Parish before Nov 6.", S["objection_a"]))

story.append(thin_rule())

# ── Before The Call ──
story.append(Paragraph("Before The Call", S["section"]))
story.append(b("Review counts unconfirmed. Verify live before the call. None are printed in the report."))
story.append(b("Google profile, map results, and ads were not observed. Confirm live."))
story.append(b("Confirm collected (net) revenue and fee structure. Gross only was stated."))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Web + SEO Starter</b>", S["price_main"]),
     Paragraph("$3,997/mo", S["price_main"])],
    [Paragraph("Local pages, SEO content, Google profile, monthly edits.", S["price_detail"]),
     Paragraph("No bundle discount", S["price_detail"])],
    [Paragraph("<b>AI Workforce Pro &ndash; Starter (1 user)</b>", S["price_main"]),
     Paragraph("$350/mo", S["price_main"])],
    [Paragraph("Month to month. Managed AI workspace and weekly session.", S["price_detail"]),
     Paragraph("No stand-alone price", S["price_detail"])],
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
]))
story.append(pt)
story.append(Paragraph(
    "Total: $4,347/mo  |  No ad spend  |  No bundle savings  |  61% of revenue (OVER 35% cap)",
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
