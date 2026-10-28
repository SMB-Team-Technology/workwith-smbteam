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

OUTPUT_PATH = "blackheath-partners/Blackheath Partners_October 29, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Blackheath Partners", S["title"]))
story.append(Paragraph("Sales Companion  |  October 29, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Matt Eller", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("4 field, 2 internal", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("Not stated", S["snap_value"]),
     Paragraph("Dorado, PR", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE", S["section"]))
story.append(Paragraph("He wants to build Blackheath's regional offices into a known national brand so his salespeople, not only he, bring in the right advisors.", S["subsection"]))

story.append(quote_block("what I'm trying to do is build up the franchises."))
story.append(Spacer(1, 1))
story.append(quote_block("I need my salespeople carrying me because people come to me because they want to work with me."))
story.append(Spacer(1, 1))
story.append(quote_block("I need&hellip; some brand awareness and ramp it up."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>New high-net-worth advisors.</b> His goal is 100 to 200 new advisors, not lower-tier insurance agents."))
story.append(bd("<b>Proof of concept first.</b> He said he wants to start with a test before committing."))
story.append(bd("<b>Brand awareness.</b> Warmer calls so his salespeople can carry more conversations."))
story.append(bd("<b>Growth in the regional offices.</b> He calls them franchises and is building more."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Almost no marketing history.</b> Growth is referrals, reputation and one broker-dealer contact."))
story.append(b("<b>A bad last vendor result.</b> Prior funnel brought calls from the wrong kind of lead."))
story.append(b("<b>No tracking.</b> We verified no Meta pixel, Analytics or Tag Manager on the site."))
story.append(b("<b>He is the final call.</b> Larger relationships still need him."))
story.append(b("<b>No clear next step.</b> Site has no form, content has no call to action, no formal referral system."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts Blackheath in front of wealth advisors he has never met."))
story.append(bd("Shows what works before he commits to a bigger budget."))
story.append(bd("Builds brand awareness so his team's calls start warmer."))

story.append(Paragraph("<b>Paid Ads &mdash; Starter  |  $3,497/mo stand-alone</b>", S["subsection"]))
story.append(b("Seller override (Slack, Oct 28): Starter stand-alone. Platinum and Elite Coach Plus were removed."))
story.append(b("Catalog says ads-only is normally paired with coaching. You told Matt you need approval to scope it."))
story.append(b("Catalog lists no deliverables for this tier. The proposal lists the scope you described on the call."))
story.append(b("Matt gave no revenue. HubSpot shows $5MM+ and was used for tiering only."))

story.append(thin_rule())

# ── Approvals and Open Items (replaces Coaching section) ──
story.append(Paragraph("Approvals and Open Items", S["section"]))
story.append(b("<b>Scoping answer.</b> You promised Matt an answer by end of day October 29."))
story.append(b("<b>OmniSocial AI 360 and avatar video.</b> Both came up; neither is in the proposal. Needs sales-ops (72 hours) and Alexis."))
story.append(b("<b>AI Workforce Pro.</b> It is in roadmap Phase 3. Confirm delivery has launched before discussing it."))
story.append(b("<b>Reviews.</b> No Google listing or review count could be confirmed. Verify live before the call."))
story.append(b("<b>Follow-ups.</b> Text the Marco Island workshop (Dec 3-5) and estate-planning mastermind info."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Blackheath &mdash; Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Funds a measured test on Meta, LinkedIn, YouTube and Google Display aimed at advisors."))
story.append(bd("Lets him scale only the channels that bring in the right kind of advisor."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,000/mo &mdash; the minimum for any paid ads package."))
story.append(b("<b>Aggressive:</b> $12,000/mo &mdash; four times the floor. A default, not a validated number."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Not projected.</b> Matt gave no case value, close rate or revenue."))
story.append(b("Our CPL and case-value tables are for law practice areas and do not fit advisor recruiting."))
story.append(b("Set return targets with Matt after the proof of concept shows cost per qualified advisor."))
story.append(Paragraph("<i>Do not quote return numbers on the call. Any figure would be a guess.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> No practice-area minimum table fits. The default $3,000 floor applies."))
story.append(b("<b>Aggressive:</b> Decision file scaled the floor 4x. The 20% rule was not used because no revenue goal was stated."))
story.append(b("Both are inside the $20,000 Paid Ads Starter cap. The $25,000/mo you mentioned was pitch math, not Matt's budget."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"My last people made the phone ring, and the leads were wrong."', S["objection_q"]))
story.append(Paragraph("Agree. He said they were \"lower tiered insurance people, not financial advisors.\" This plan aims at advisors with custom and lookalike audiences from advisor lists, and it starts as a small test.", S["objection_a"]))

story.append(Paragraph('"I am talking to two other marketers."', S["objection_q"]))
story.append(Paragraph("Fine. He cancelled his last vendor last Monday and has no contract. Ask how they would track results. His site has no pixel or analytics today, and fixing that comes first with us.", S["objection_a"]))

story.append(Paragraph('"I can make the content myself. It is about distribution."', S["objection_q"]))
story.append(Paragraph("Agree. He records and his team edits. We handle audiences, placement and a clear call to action, which people have told him his content lacks.", S["objection_a"]))

story.append(Paragraph('"How much will this cost me in ad spend?"', S["objection_q"]))
story.append(Paragraph("You told him a proof of concept is \"in the thousands.\" The range is $3,000 to $12,000 a month, and he starts at the low end.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Paid Ads &mdash; Starter</b>", S["price_main"]),
     Paragraph("$3,497/mo", S["price_main"])],
    [Paragraph("Ads-only: tracking, remarketing and advisor audiences across Meta, LinkedIn, YouTube and Display.", S["price_detail"]),
     Paragraph("stand-alone, no bundle", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,000&ndash;$12,000/mo", S["price_main"])],
    [Paragraph("Goes to Meta, LinkedIn, YouTube and Google Display &mdash; not to SMB Team.", S["price_detail"]),
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
story.append(Paragraph(
    "Total: $3,497/mo + $3,000&ndash;$12,000 ad spend  |  No bundle savings  |  35% cap not tested (revenue not stated)",
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
