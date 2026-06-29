"""
Sales Companion PDF — Santoni, Vocci & Ortega LLC
SMB Team | Jacob Meissner | July 6, 2026
Internal use only — do not share with prospect.
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

OUTPUT_PATH = "santoni-vocci-ortega/Santoni_Vocci_Ortega_LLC_07062026_Sales_Companion.pdf"


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

story.append(Paragraph("Santoni, Vocci &amp; Ortega LLC", S["title"]))
story.append(Paragraph("Sales Companion  |  July 6, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Matthew Vocci (contact)", S["snap_value"]),
     Paragraph("~$1.2M est.", S["snap_value"]),
     Paragraph("5 (3 partners, 2 staff)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Towson &amp; Timonium, MD", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: MISSION SCALE + PARTNER FREEDOM", S["section"]))
story.append(Paragraph("No transcript — DBM inferred. Confirm on the call with Matthew Vocci.", S["subsection"]))

story.append(quote_block("Firm profile signals: Law Firm of the Year (MD Volunteer Lawyers Service); Jane Santoni practicing since 1988; Matthew Vocci bio emphasizes high-quality representation for clients who need it. Mission-driven, not revenue-first."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What they want:</b>", S["subsection"]))
story.append(bd("<b>Cases from systems, not hustle.</b> Inbound flow that doesn't require each partner's personal network."))
story.append(bd("<b>Mission at scale.</b> Serve more Baltimore-area clients who need PI and consumer rights help."))
story.append(bd("<b>Partner freedom.</b> Any partner can step away without the firm stalling."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping them:</b>", S["subsection"]))
story.append(b("<b>No paid lead gen.</b> All clients come from referrals and organic — nothing runs without the partners."))
story.append(b("<b>No LSA.</b> Competitors hold the top Google position for PI searches; SVO is absent from that slot."))
story.append(b("<b>Review gap.</b> Leppler Injury Law: 407 reviews at 5.0 vs. SVO's 102 — keeps SVO out of the PI 3-pack."))
story.append(b("<b>No intake system.</b> No after-hours coverage; ads will generate leads the firm can't reliably convert."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("<b>Turns on inbound.</b> Delivers cases through paid systems so partners stop being the only lead source."))
story.append(bd("<b>Captures the PI searches they're missing.</b> Leppler and Portner &amp; Shure own those clicks today; Growth tier takes them back."))
story.append(bd("<b>Rebuilds the website to convert traffic.</b> PageSpeed ~38–52 mobile means ads land on a page that loses leads — the rebuild fixes that."))

story.append(Paragraph("<b>Full Service Marketing — Growth  |  $7,397/mo bundled</b>", S["subsection"]))
story.append(b("$1.2M est. revenue — Growth tier ($1M–$3M) is correct; Starter undersizes it and caps ad spend at $10K."))
story.append(b("PI practice: minimum Starter required; Growth unlocks LSA + PI + consumer rights campaigns simultaneously."))
story.append(b("Growth ad spend cap: $15,000/mo. Upgrade to Dominate ($8,497/mo) if aggressive goals confirmed on call."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("<b>Intake before ads go live.</b> Builds the follow-up system so paid leads convert instead of falling through."))
story.append(bd("<b>Profit plan.</b> Makes partner distributions predictable; contingency revenue stops arriving as surprises."))
story.append(bd("<b>Team structure.</b> Defines what only a partner must do vs. what a trained staff member can handle."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $1M+, 5-person team — Elite Coach Plus is the right fit before adding a formal ops layer."))
story.append(b("No transcript: dedicated intake/ops role unconfirmed. If confirmed on call, revisit Master's Circle ($6,600/mo)."))
story.append(b("Includes: weekly group coaching, mastermind, quarterly workshops, one annual in-person workshop."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Santoni, Vocci &amp; Ortega LLC — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for them:</b>", S["subsection"]))
story.append(bd("<b>Measurable inbound.</b> Every case from a paid campaign is tracked, costed, and optimizable from day one."))
story.append(bd("<b>Fills the paid channels.</b> Google Search, LSA, and Meta put the firm in front of high-intent PI and consumer rights prospects now."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $10,000/mo — PI hard floor for competitive Baltimore County; covers Google, LSA, Meta retargeting."))
story.append(b("<b>Aggressive:</b> $15,000/mo — Growth tier cap; full coverage across PI, consumer rights, and Meta lead gen simultaneously."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative ($10K):</b> ~6 cases x $25K avg = ~$150K/mo revenue vs. $10K spend = ~15x return."))
story.append(b("<b>Aggressive ($15K):</b> ~11 cases x $25K avg = ~$275K/mo revenue vs. $15K spend = ~18x return."))
story.append(b("<b>Calculation:</b> Conservative = PI channel minimums ($10K floor). Aggressive = 2x rev ($2.4M) x 20% / 12 x 1.3 geo = $52K, capped at Growth tier max $15K."))
story.append(b("Total aggressive: $10,597 fees + $15,000 ads = $25,597/mo = 25.6% of revenue. Under 35% cap."))
story.append(Paragraph("<i>Estimates only. Case value $25K is default — confirm with Matthew Vocci. Not guaranteed.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If They Push Back ──
story.append(Paragraph("If They Push Back", S["section"]))

story.append(Paragraph('"We already have a good reputation — do we really need to advertise?"', S["objection_q"]))
story.append(Paragraph("Leppler Injury Law (407 reviews, 5.0 stars) is running active campaigns on every PI search SVO doesn't appear on. Reputation makes ads convert — but only if the firm is in the auction. SVO's Super Lawyers credentials and 102 reviews make it a credible advertiser the moment it enters.", S["objection_a"]))

story.append(Paragraph('"We don\'t have budget for $10K+ in ad spend."', S["objection_q"]))
story.append(Paragraph("$10,000 ad spend at 15x projected return = ~$150K/mo in case revenue for ~$20,597 total (fees + ads). That's a 7x+ return on total investment. Paid ads add measurable incremental volume at known cost — not a leap of faith.", S["objection_a"]))

story.append(Paragraph('"Is the Growth tier really necessary — can we start with Starter?"', S["objection_q"]))
story.append(Paragraph("Starter ($4,847/mo) is for firms under $1M with a $10K ad spend cap. At $1.2M estimated revenue with a PI practice, SVO outgrows Starter from day one. Growth adds the website rebuild, LSA, and multi-practice campaign capacity the firm needs to make the spend work.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Growth</b>", S["price_main"]),
     Paragraph("$7,397/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta, SEO, website rebuild. Full service across all channels.", S["price_detail"]),
     Paragraph("<strike>$7,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, intake design, profit plan, team structure, quarterly workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$10,000–$15,000/mo", S["price_main"])],
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
    "Total: $10,597/mo + $10,000–$15,000 ad spend  |  Save $897/mo by bundling  |  20.6%–25.6% of revenue (under 35% cap)",
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
