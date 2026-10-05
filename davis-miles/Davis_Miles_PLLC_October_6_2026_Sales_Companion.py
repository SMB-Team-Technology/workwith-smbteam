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
_FONT_DIR = os.path.join("Design Files", "fonts")
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
OUTPUT_PATH = "davis-miles/Davis_Miles_PLLC_October_6_2026_Sales_Companion.pdf"


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
story.append(Paragraph("Davis Miles PLLC", S["title"]))
# FILL: Sales Companion  |  [Month Day, Year]  |  Rep: [Rep Name]
story.append(Paragraph("Sales Companion  |  October 6, 2026  |  Rep: Michael Kopp", S["subtitle"]))
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
    [Paragraph("Not stated (contact: Kendyll Maughan)", S["snap_value"]),
     Paragraph("$785,161 (AZ family law, projected)", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("20%", S["snap_value"]),
     Paragraph("Tempe, Mesa, Glendale AZ", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE (inferred)", S["section"]))
# FILL: One sentence summarizing what the owner wants — plain language, connects to DBM
story.append(Paragraph("Hit a $1,000,000 Arizona family law year by closing a $215,000 gap and replacing an agency that stopped delivering.", S["subsection"]))

# FILL: 2-4 direct quotes from the transcript that reveal the DBM
# Use quote_block() for each. Separate with Spacer(1, 1).
story.append(quote_block("ineffective account management"))
story.append(Spacer(1, 1))
story.append(b("No personal motive was stated on this short vendor-evaluation call. Pull exact wording from the recording before the follow-up."))
story.append(Spacer(1, 2))

# FILL: "What she/he wants:" — 3-5 dark bullets (use bd())
# Each bullet: bold lead phrase + one short sentence. One idea per bullet.
story.append(Paragraph("<b>What the firm wants:</b>", S["subsection"]))
story.append(bd("<b>$1,000,000 year.</b> Close the gap from $785,161 in Arizona family law revenue."))
story.append(bd("<b>16 to 17 signed cases a month.</b> That is the lead math presented on the call at a $5,000 retainer."))
story.append(bd("<b>A better agency.</b> Faster communication and real progress than Elevato delivered."))
story.append(bd("<b>More than PPC.</b> Channels beyond Google search, as the firm already asked for."))

story.append(Spacer(1, 2))

# FILL: "What is stopping her/him:" — 3-5 gray bullets (use b())
# Each bullet: bold lead phrase + one short sentence. One idea per bullet.
story.append(Paragraph("<b>What is stopping them:</b>", S["subsection"]))
story.append(b("<b>Falling leads.</b> Leads have declined since March 2026 under Elevato."))
story.append(b("<b>Low show rate.</b> Fewer than half of free 15-minute consults are kept."))
story.append(b("<b>Shopper leads.</b> Unqualified shoppers and attorney approach drive no-shows."))
story.append(b("<b>Weak LSA management.</b> The firm called the LSA account poorly managed."))
story.append(b("<b>No ROI tracking.</b> Lawmatics is not connected to case management."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

# FILL: "What it does for her/him:" — 2-3 dark bullets (use bd())
# Transformation statements. What the package makes possible. Not deliverables.
story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Replaces a PPC-only vendor with Google, LSA, and Meta run as one system."))
story.append(bd("Gives monthly reporting by channel so every dollar is easy to judge."))
story.append(bd("Builds toward the 16 to 17 signed cases a month a $1M year needs."))

# FILL: "[Package Name]  |  $[bundled price]/mo bundled"
story.append(Paragraph("<b>Paid Ads Starter  |  $3,497/mo flat (no bundle discount)</b>", S["subsection"]))
# FILL: 3-4 gray bullets (use b()) — scoping rationale. One fact per bullet.
story.append(b("Revenue of $785,161 sits in the $500K to $1M Starter band; three offices rule out Essentials."))
story.append(b("Paid Ads Starter ad spend cap is $20,000/mo; the $3,500 to $16,000 range fits inside it."))
story.append(b("Firm already runs about $20K/mo in ads, so ads-only fits. PageSpeed was not obtained; confirm site."))
story.append(b("Ads-only normally pairs with coaching. Seller removed it (Slack, Sept 25, 2026). Confirm approval."))

story.append(thin_rule())

# ── Why No Coaching Package (Yet) ──
story.append(Paragraph("Why No Coaching Package (Yet)", S["section"]))

story.append(Paragraph("<b>What it keeps simple:</b>", S["subsection"]))
story.append(bd("One focused proposal that replaces Elevato, instead of a bigger ask on a vendor-switch call."))
story.append(bd("A clear next step later: fix the consult process once lead flow is steady."))

story.append(Paragraph("<b>Roadmap talking points (no coaching quoted today)  |  $0/mo</b>", S["subsection"]))
story.append(b("Seller dropped Elite Coach Plus per Slack override on Sept 25, 2026. Do not add it back unprompted."))
story.append(b("Phase 2: FCOO Advisor at $3,297/mo for a consistent consultation and follow-up process."))
story.append(b("Phase 3: FCFO Advisor at $3,297/mo for cost per case and profit visibility."))
story.append(b("Team size was not stated (pipeline defaulted to 3). Confirm before suggesting any coaching tier."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

# FILL: "[Firm Short Name] — Sales Companion (continued)"
story.append(Paragraph("Davis Miles — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

# FILL: "What it does for her/him:" — 2 dark bullets (use bd())
story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("Keeps the firm visible for family law searches in Tempe, Mesa, and Chandler."))
story.append(bd("Lets budget grow only as cost per signed case proves out."))

# FILL: Ad spend range — conservative (channel minimums) to aggressive (20% rule)
story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,500/mo — Google search minimum for family law."))
story.append(b("<b>Aggressive:</b> $16,000/mo — raised from $14,000 by seller override (Slack, Sept 25, 2026)."))

# FILL: ROI projection bullets for BOTH levels — all labeled as estimates
# Use data from Scoping Guide: CPL benchmarks, close rate, avg case value
story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 4.5 cases x $5K = $22.7K/mo vs. $3.5K spend = 6.5x return."))
story.append(b("<b>Aggressive:</b> 29 cases x $5K = $144.9K/mo vs. $16K spend = 9.1x return."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed. Used a 15.6% lead-to-case rate (16.5 cases from 106 leads on the call). At the stated 20% consult rate: 8.3x and 11.6x. Aggressive is above the 16.7 cases a month the goal needs; temper it.</i>", S["disclaimer"]))

# FILL: How both numbers were calculated — from Scoping Guide Steps 3-4
story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Family law Google PPC minimum $3,500. Blended CPL $100 x 1.2 cushion = $120, so 29 leads."))
story.append(b("<b>Aggressive:</b> $16,000 from the pipeline file. Channel mix weighted by channel minimums gives a $85.93 blended CPL, so 186 leads."))
story.append(b("Total at aggressive: $19,497/mo = 29.8% of $65,430 monthly revenue. Under the 35% cap ($22,900). The current ~$20K Google plus Meta plus fee would pass it."))

story.append(thin_rule())

# ── If She Pushes Back ──
# FILL: 2-4 objections anticipated from the transcript
# Each: red question (objection_q style) + gray response (objection_a style)
# Responses use specific data from the audit — competitor numbers, transcript quotes, etc.
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"We spend about $20,000 a month today. Why is your range lower?"', S["objection_q"]))
story.append(Paragraph("Leads have fallen since March 2026 at that spend, so more budget is not the fix. At $20K plus Meta plus our fee, spend would pass 35% of monthly revenue. Confirm what number was said on the call.", S["objection_a"]))

story.append(Paragraph('"Why switch agencies? We will lose momentum."', S["objection_q"]))
story.append(Paragraph("Momentum is already down: leads fell, LSA was poorly managed, and the agency stayed PPC-only. Davis Miles did not surface in Tempe, Mesa, or Chandler searches, but Arizona Law Group, Hildebrand Law, and Edwards &amp; Petersen did.", S["objection_a"]))

story.append(Paragraph('"Our real problem is consultation no-shows."', S["objection_q"]))
story.append(Paragraph("Agree. Fewer than half are kept, and at a 20% close rate each kept consult is worth about $1,000. Ads-side qualification helps now; the FCOO Advisor in Phase 2 fixes the process.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
# FILL: All pricing from the scoping calculation
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Paid Ads Starter</b>", S["price_main"]),
     Paragraph("$3,497/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, YouTube, Map Pack, and ChatGPT visibility.", S["price_detail"]),
     Paragraph("No bundle discount", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,500–$16,000/mo", S["price_main"])],
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
]))
story.append(pt)
# FILL: Total line — bundled total + ad spend range | savings | % of revenue at aggressive level
story.append(Paragraph(
    "Total: $3,497/mo + $3,500–$16,000 ad spend  |  No bundle savings (seller override)  |  10.7%–29.8% of revenue (under 35% cap)",
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
