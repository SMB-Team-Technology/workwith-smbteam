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
_FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Design Files", "fonts")
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

# FILL: Output path — use format [FirmName]_[MMDDYYYY]_Sales_Companion.pdf
OUTPUT_PATH = "grano-law/Grano_Law_October_23_2026_Sales_Companion.pdf"


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

# FILL: Firm's full legal name
story.append(Paragraph("Grano Law", S["title"]))
# FILL: Sales Companion  |  [Month Day, Year]  |  Rep: [Rep Name]
story.append(Paragraph("Sales Companion  |  October 23, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    # FILL: All six snapshot values from Pass 1 research and transcript
    [Paragraph("Marc Grano", S["snap_value"]),
     Paragraph("$600K–$800K", S["snap_value"]),
     Paragraph("5", S["snap_value"]),
     Paragraph("4", S["snap_value"]),
     Paragraph("15% (est.)", S["snap_value"]),
     Paragraph("Las Vegas, NM", S["snap_value"])],
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
# FILL: "Dominant Buying Motive: [DBM KEYWORD IN CAPS]" — e.g. FREEDOM, SECURITY, LEGACY
story.append(Paragraph("Dominant Buying Motive: CONSISTENCY", S["section"]))
# FILL: One sentence summarizing what the owner wants — plain language, connects to DBM
story.append(Paragraph("Marc wants steady, quality DWI cases so he keeps the boutique firm he controls.", S["subsection"]))

# FILL: 2-4 direct quotes from the transcript that reveal the DBM
# Use quote_block() for each. Separate with Spacer(1, 1).
story.append(quote_block("I just want it to be a consistent stream with quality cases."))
story.append(Spacer(1, 1))
story.append(quote_block("All I'm concerned about is just opening up the spigot again."))
story.append(Spacer(1, 1))
story.append(quote_block("That way, there's margin for when we do have a trial, we can ramp up and it does, we flex, but we don't break."))
story.append(Spacer(1, 2))

# FILL: "What she/he wants:" — 3-5 dark bullets (use bd())
# Each bullet: bold lead phrase + one short sentence. One idea per bullet.
story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Open the spigot again.</b> DWI inquiries have trickled for about two months."))
story.append(bd("<b>Quality, not a flood.</b> A steady flow of cases he can give full attention."))
story.append(bd("<b>Stay a boutique.</b> He holds capacity at 60–70% so he can flex for trials."))
story.append(bd("<b>Be where the business is.</b> He wants Santa Fe and Rio Rancho cases."))

story.append(Spacer(1, 2))

# FILL: "What is stopping her/him:" — 3-5 gray bullets (use b())
# Each bullet: bold lead phrase + one short sentence. One idea per bullet.
story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Loyal but unhappy.</b> He pays two vendors and is “in an assessment period.”"))
story.append(b("<b>No visibility.</b> He opened the ad accounts but does not check them regularly."))
story.append(b("<b>Unwatched gaps.</b> LSA stops at 5 p.m., messages off, PPC not linked to GBP."))
story.append(b("<b>Price jump.</b> Rep-reported ad spend is about $3,000–$3,500/mo (unconfirmed)."))
story.append(b("<b>Soft on coaching.</b> He said it “may not be a bad idea”; he wants ads first."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

# FILL: "What it does for her/him:" — 2-3 dark bullets (use bd())
# Transformation statements. What the package makes possible. Not deliverables.
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Opens the spigot again with DWI demand from Santa Fe and Rio Rancho."))
story.append(bd("Replaces two vendors he has to chase with one team and one view of results."))
story.append(bd("Fixes the gaps found on the call: after-hours, GBP link, page titles."))

# FILL: "[Package Name]  |  $[bundled price]/mo bundled"
story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,997/mo bundled</b>", S["subsection"]))
# FILL: 3-4 gray bullets (use b()) — scoping rationale. One fact per bullet.
story.append(b("Starter fits ~$700K and two practice areas; Essentials is out."))
story.append(b("Starter ad cap is $25,000/mo; the recommended range sits well under it."))
story.append(b("No rebuild: PageSpeed 80 mobile, 97 desktop, modern and responsive."))
story.append(b("Vendor flag: he pays two vendors. Confirm the override call (see workings)."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

# FILL: "What it does for her/him:" — 2-3 dark bullets (use bd())
# Transformation statements. What the package makes possible. Not deliverables.
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives him a steady rhythm so a trial month does not derail the firm."))
story.append(bd("Puts him with peers who run firms like his."))
story.append(bd("Adds a weekly leads-and-cases check to catch slowdowns sooner."))

# FILL: "[Package Name]  |  $[bundled price]/mo bundled"
story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
# FILL: 3-4 gray bullets (use b()) — scoping rationale. One fact per bullet.
story.append(b("The $400K–$1M revenue band maps to Elite Coach Plus."))
story.append(b("Call said “Elite Coach”; the table gives Plus. Confirm with Dan."))
story.append(b("Master's Circle is out: under $1M and no dedicated ops lead."))
story.append(b("Coaching interest is soft. Lead with ads, then coaching."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

# FILL: "[Firm Short Name] — Sales Companion (continued)"
story.append(Paragraph("Grano Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

# FILL: "What it does for her/him:" — 2 dark bullets (use bd())
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts the firm in front of Santa Fe and Rio Rancho DWI searchers at a pace that fits his caseload."))
story.append(bd("Starting at the conservative level lets him test results before committing more."))

# FILL: Ad spend range — conservative (channel minimums) to aggressive (20% rule)
story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $7,500/mo — minimum viable spend across Google PPC and LSA."))
story.append(b("<b>Aggressive:</b> $12,000/mo — set by the 35% cap, not by a growth goal (he has none)."))

# FILL: ROI projection bullets for BOTH levels — all labeled as estimates
# Use data from Scoping Guide: CPL benchmarks, close rate, avg case value
story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~5 cases x $3K–$5K = $16K–$27K/mo vs. $7.5K spend = 2.1x–3.6x return."))
story.append(b("<b>Aggressive:</b> ~10 cases x $3K–$5K = $31K–$52K/mo vs. $12K spend = 2.6x–4.3x return."))
story.append(Paragraph("<i>All figures are estimates, not guaranteed. Case value ($3K–$5K) and 15% close rate are defaults; neither was stated.</i>", S["disclaimer"]))

# FILL: How both numbers were calculated — from Scoping Guide Steps 3-4
story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Criminal defense minimums: PPC $5,500 + LSA $2,000 = $7,500. No Meta, no PI ads."))
story.append(b("<b>Aggressive:</b> No goal stated; default $1.4M x 20% ÷ 12 = $23,333. Tier 4 (1.00x). Less $4,997 fee = $18,336, which breaks the cap, so it is held to $12,000."))
story.append(b("Total spend at aggressive: $20,197/mo = 34.6% of revenue. Under the 35% cap. (The decision file's $20,000 would be 48%.)"))

story.append(thin_rule())

# ── If He Pushes Back ──
# FILL: 2-4 objections anticipated from the transcript
# Each: red question (objection_q style) + gray response (objection_a style)
# Responses use specific data from the audit — competitor numbers, transcript quotes, etc.
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I already pay Jennifer and ConvertIt. Why add another vendor?"', S["objection_q"]))
story.append(Paragraph("He told us he is in an assessment period and leads have dried up. Nobody has to be fired: share the audit (LSA dark at 5 p.m., messages off, PPC unlinked) and let the results decide.", S["objection_a"]))

story.append(Paragraph('"That is a lot more than I spend now."', S["objection_q"]))
story.append(Paragraph("Start at the conservative $7,500: ~5 cases a month at $3K–$5K each is an estimated $16K–$27K. Bundling saves $997/mo.", S["objection_a"]))

story.append(Paragraph('"I do not want more volume. I do not want 40."', S["objection_q"]))
story.append(Paragraph("Agreed. Lead with the conservative range and show how to throttle spend. The goal is steady, not big, and caseload stays at 60–70%.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
# FILL: All pricing from the scoping calculation
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    # FILL: Marketing package name and bundled price
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    # FILL: One-line description and stand-alone price with strikethrough
    [Paragraph("Google profile, LSA, PPC, local SEO and Santa Fe / Rio Rancho pages.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    # FILL: Coaching package name and bundled price
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    # FILL: One-line description and stand-alone price with strikethrough
    [Paragraph("Weekly group coaching, masterminds, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    # FILL: Recommended ad spend range (conservative to aggressive)
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$7,500–$12,000/mo", S["price_main"])],
    [Paragraph("Goes to Google and LSA — not to SMB Team.", S["price_detail"]),
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
# FILL: Total line — bundled total + ad spend range | savings | % of revenue at aggressive level
story.append(Paragraph(
    "Total: $8,197/mo + $7,500–$12,000 ad spend  |  Save $997/mo by bundling  |  26.9%–34.6% of revenue (under 35% cap)",
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
