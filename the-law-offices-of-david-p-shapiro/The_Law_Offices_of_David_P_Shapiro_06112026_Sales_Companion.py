"""
Sales Companion PDF — The Law Offices of David P. Shapiro
SMB Team | June 11, 2026 | Rep: Jacob Meissner
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

OUTPUT_PATH = "the-law-offices-of-david-p-shapiro/The_Law_Offices_of_David_P_Shapiro_06112026_Sales_Companion.pdf"


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

story.append(Paragraph("The Law Offices of David P. Shapiro", S["title"]))
story.append(Paragraph("Sales Companion  |  June 11, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("David P. Shapiro", S["snap_value"]),
     Paragraph("Est. $500K+ (unconfirmed)", S["snap_value"]),
     Paragraph("7 (3 atty + 4 staff)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("San Diego, CA (2 locations)", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE AND DOMINATE", S["section"]))
story.append(Paragraph("David wants to be recognized as the undisputed #1 criminal defense firm in San Diego County — and to build a firm that generates consistent revenue whether or not he is personally present.", S["subsection"]))

# No transcript — inferred signals from research
story.append(quote_block("Firm describes itself as 'one of San Diego's largest criminal defense law firms' — the ambition to dominate is built into the firm's public identity."))
story.append(Spacer(1, 1))
story.append(quote_block("12 consecutive Super Lawyers listings, BBB Torch Award for Ethics, 'San Diego's Most Influential People' 2022/2024/2025 — David is building a legacy brand, not just a practice."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Market dominance.</b> To be the recognized #1 criminal defense firm in San Diego County."))
story.append(bd("<b>Scalable revenue.</b> Consistent case flow that does not depend on David personally handling every decision."))
story.append(bd("<b>Legacy and freedom.</b> A documented, valuable firm he can scale, pass on, or sell on his terms."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No paid digital presence.</b> No Google Ads, LSA, or Meta Ads — competitors capture emergency searches while the firm relies on SEO and radio."))
story.append(b("<b>Review gap.</b> Sevens Legal: 800+ Google reviews vs. ~204 here — 4:1 gap suppressing local pack rankings."))
story.append(b("<b>Dead domain.</b> davidshapiro.com resolves to a 404 — all referrals to that URL are lost prospects."))
story.append(b("<b>Revenue unconfirmed.</b> No transcript — defaults applied. Confirm actual revenue on call to validate tier."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts the firm above Sevens Legal and Dod Law in Google at the moment of arrest — the highest-intent moment in criminal defense."))
story.append(bd("LSA Google Screened captures pay-per-lead calls above all paid ads and map pack results."))
story.append(bd("Retargeting keeps the firm visible to every prospect who visited the site but did not call."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("San Diego Tier 2 market — $60–$150 CPCs; minimum viable paid presence is $5,500/mo ad spend."))
story.append(b("Covers Google PPC, LSA, Meta Ads, SEO, and website CRO — all channels currently uncontested."))
story.append(b("Stand-alone $5,697/mo; bundled saves $850/mo. If revenue confirms $1M+, upgrade to Growth tier."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Converts more of the new leads the marketing generates — better intake, higher close rates, no extra ad spend."))
story.append(bd("Connects David with criminal defense attorneys who have scaled past this stage — peer learning from practitioners who solved these same problems."))
story.append(bd("Builds the management accountability frameworks so the firm operates without David in every decision."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M, 7-person team: Elite Coach Plus is correct tier per eligibility rules."))
story.append(b("Includes: weekly coaching, practice area masterminds, quarterly workshops, annual in-person event."))
story.append(b("Stand-alone $3,497/mo; bundled saves $297/mo. If revenue $1M+, escalate to Master's Circle ($4,600/mo)."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("David P. Shapiro — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("<b>Conservative $5,500/mo:</b> Activates Google PPC for criminal defense and DUI — captures highest-intent cases at the moment of arrest."))
story.append(bd("<b>Aggressive $22,000/mo:</b> Full-market presence across Google, LSA, and Meta — Sevens Legal-level digital investment."))

story.append(Paragraph("<b>Recommended Range + ROI (all estimates):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,500/mo → ~25 leads x 15% close = ~4 cases x $4K avg = $16K/mo revenue. 2.9x return."))
story.append(b("<b>Aggressive:</b> $22,000/mo → ~150 leads x 15% close = ~23 cases x $4K avg = $92K/mo revenue. 4.2x return."))
story.append(b("<b>Calculation:</b> $1M goal x 20% / 12 x 1.3 Tier 2 = $21,667. Reverse math ($144 blended CPL x 139 leads) = $20,042. Use $22,000."))
story.append(Paragraph("<i>Estimates only. $4,000 default case value (criminal defense midpoint). 15% default close rate. Not guaranteed.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We already do radio — why do we need digital ads too?"', S["objection_q"]))
story.append(Paragraph("Radio builds brand awareness for later; Google and LSA capture prospects at the moment of arrest. Someone arrested at 11pm searches on their phone — not a radio station. Both channels serve different moments.", S["objection_a"]))

story.append(Paragraph('"We have a great reputation — 4.9 stars, Super Lawyers. Why aren\'t we getting more clients?"', S["objection_q"]))
story.append(Paragraph("Reputation earns trust after the prospect finds you. With ~204 Google reviews vs. Sevens Legal's 800+, this firm is not in the local 3-pack. The reputation is real; the visibility system is not yet built.", S["objection_a"]))

story.append(Paragraph('"I\'m not sure about the investment level."', S["objection_q"]))
story.append(Paragraph("Conservative scenario: $13,547/mo total → ~4 cases/mo at $4,000 avg = $16,000 in projected revenue — 2.9x estimate. One retained felony at $15,000+ pays for a full month of both packages.", S["objection_a"]))


story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, Meta Ads, SEO, website CRO — full digital presence.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, practice area masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,500–$22,000/mo", S["price_main"])],
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
    "Total: $8,047/mo + $5,500–$22,000 ad spend  |  Save $1,147/mo bundled  |  Confirm revenue on call — conservative scenario (32.5%) under 35% cap at $500K estimate.",
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
