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

OUTPUT_PATH = "the-law-offices-of-peter-paul-mendel/The Law Offices of Peter Paul Mendel_August 10, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("The Law Offices of Peter Paul Mendel", S["title"]))
story.append(Paragraph("Sales Companion  |  August 10, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Peter Paul Mendel", S["snap_value"]),
     Paragraph("~$3.5K/mo current (transcript); HubSpot est. $570K/yr conflicts — see notes", S["snap_value"]),
     Paragraph("1 (solo)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Long Beach, CA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE & SECURITY", S["section"]))
story.append(Paragraph("Peter wants to turn a solo mediation practice into a ~50-mediator platform — but only on a payment model that can never again leave him holding $500,000 in uncollected fees.", S["subsection"]))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>A 50-mediator platform.</b> ~50 mediators, each generating $20K-$40K/month long-term."))
story.append(bd("<b>Zero AR risk, permanently.</b> Upfront payment only, after $500K uncollected receivables sank his prior practice."))
story.append(bd("<b>A stronger referral engine.</b> Every engagement today comes from attorney referrals."))
story.append(bd("<b>3 mediations/week short-term.</b> $40K/month goal from volume."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No qualification filter.</b> Past paid leads were ~90% unqualified \"looky-loos.\""))
story.append(b("<b>Zero staff.</b> Peter personally handles intake, case files, and collections."))
story.append(b("<b>Fragmented directories.</b> 3 different NAP combos; Avvo/FindLaw still show his old general practice."))
story.append(b("<b>No mediation-specific revenue tracking.</b> ~$3,500/mo reported is legacy work, not mediation."))
story.append(b("<b>Won't pay retainer pricing without performance guarantees</b> — direct result of the looky-loo experience."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("No marketing package this round — the call was explicitly about coaching and systems, not paid lead volume."))
story.append(bd("A retainer-based package now risks repeating the ~90% looky-loo problem from his past paid lead gen."))
story.append(bd("Marketing gets revisited once referral/intake systems are proven and a pay-per-signed-case vendor is found."))

story.append(Paragraph("<b>No Marketing Package — Not Recommended This Round  |  $0/mo</b>", S["subsection"]))
story.append(b("Call-purpose override: transcript states this was explicitly NOT a standard marketing/intake growth call."))
story.append(b("Budget-reality override: Peter wants pay-per-signed-case pricing, not retainer/brand-awareness fees."))
story.append(b("Revenue mismatch: HubSpot estimate ($570K/yr) conflicts with transcript-stated revenue (~$42K/yr) — transcript is ground truth."))
story.append(b("Escalation flag (internal only): revenue under $300K — scoping approval required."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Turns his referral network into a repeatable, filtered pipeline instead of raw, unscreened inquiries."))
story.append(bd("Builds the billing/AR discipline that prevents a repeat of the $500K uncollected-receivables collapse."))
story.append(bd("Creates the hiring roadmap to move past a one-person ceiling toward the 50-mediator vision."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("package_decision.json defaulted to Elite Coach Plus ($3,200/mo) via the HubSpot-derived band — overridden for the lowest tier given his actual ~$42K/yr revenue."))
story.append(b("$2,600/mo clears the $2,497 minimum MRR floor; correct tier for the $250K-$400K band."))
story.append(b("Confirm Peter can sustain 4+ months of this investment given thin current cash flow (internal funds-check)."))
story.append(b("AI billing/AR tooling he asked about is included here, not sold separately — he's solo with no support staff, and standalone LAW requires 1-2 staff minimum."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Mendel — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("No ad spend recommended this round — see Marketing Package override notes on page 1."))
story.append(bd("Ad spend becomes viable once intake and referral systems are proven and a performance-based vendor is found."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>This Round:</b> $0/mo. <b>Future Phase:</b> revisit once systems are proven and a vendor is identified."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>This Round:</b> Not applicable. <b>Future Phase:</b> modeled once a channel/vendor and spend level are chosen."))
story.append(Paragraph("<i>All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("No calculation applies this round — see call-purpose and budget-reality overrides (Research Notes Step 9)."))
story.append(b("package_decision.json's ad spend figures ($3,500-$14,000) were not used, since no marketing package is sold in this proposal."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"Why isn\'t there a marketing package if you\'re supposed to help me grow?"', S["objection_q"]))
story.append(Paragraph("Paid marketing isn't the fix right now — his own past paid leads were ~90% \"looky-loos.\" Fixing referral and intake first means future ad spend actually converts.", S["objection_a"]))

story.append(Paragraph('"$2,600/month feels like a lot given I\'m only bringing in ~$3,500/month right now."', S["objection_q"]))
story.append(Paragraph("That's why this is flagged for an internal funds-check. It's the lowest coaching tier, clears the $2,497 MRR floor — Elite Coach Plus ($3,200) was intentionally not used.", S["objection_a"]))

story.append(Paragraph('"Can you guarantee I won\'t get more looky-loos?"', S["objection_q"]))
story.append(Paragraph("No guarantee, but the first-90-days plan builds a mediation-specific intake filter his past paid efforts never had.", S["objection_a"]))

story.append(Paragraph('"What happened to the AI billing/marketing tools I asked about?"', S["objection_q"]))
story.append(Paragraph("Included inside Elite Coach. Standalone Legal AI Workforce isn't sold separately — he's solo with no staff, and LAW requires 1-2 staff minimum.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>No Marketing Package (Not Recommended This Round)</b>", S["price_main"]),
     Paragraph("$0/mo", S["price_main"])],
    [Paragraph("Coaching-first per transcript override — see notes on page 1.", S["price_detail"]),
     Paragraph("", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly coaching, referral systems, intake qualification, AR/billing tools.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$0/mo — not this round", S["price_main"])],
    [Paragraph("Revisit once referral/intake systems are proven and a vendor is identified.", S["price_detail"]),
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
    "Total: $2,600/mo + $0 ad spend  |  Save $897/mo vs. Elite Coach stand-alone  |  0% of revenue at ad spend (none this round)",
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
