"""
Sales Companion PDF — Danton Legal
SMB Team Internal Document — Do Not Share
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

OUTPUT_PATH = "danton-legal/DantonLegal_06042026_Sales_Companion.pdf"


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
    """Dark bullet for transformation statements and what he wants."""
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

story.append(Paragraph("Danton Legal (Law Offices of M. Danton Richardson)", S["title"]))
story.append(Paragraph("Sales Companion  |  June 4, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("M. Danton Richardson", S["snap_value"]),
     Paragraph("~$500K est.", S["snap_value"]),
     Paragraph("Solo", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Pasadena, CA", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: INDEPENDENCE &amp; LEGACY", S["section"]))
story.append(Paragraph("Richardson is launching Danton Legal to build a practice under his own name after 39 years — he wants clients, income, and a reputation that belong entirely to him.", S["subsection"]))

story.append(quote_block("No Fathom transcript available. DBM inferred from research: 39-year IP veteran launching first solo brand. The drive is independence — a practice that generates under his name, not someone else's."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>His own firm.</b> Danton Legal is a new brand — findable, credible, generating clients under his name."))
story.append(bd("<b>Consistent client flow.</b> 39 years of referrals has value but not reliability — he wants a system, not a network."))
story.append(bd("<b>His track record visible.</b> HP, Sony Records, Victoria's Secret, Microsoft — none of this shows in Google today."))
story.append(bd("<b>Time leverage.</b> He wants a practice that doesn't require his personal involvement in every task."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No digital infrastructure.</b> dantonlegal.com is a blank placeholder — nothing to find."))
story.append(b("<b>No GBP or reviews.</b> Zero Google visibility — ineligible for local search and LSA."))
story.append(b("<b>NAP conflict.</b> Avvo lists old Soni address; State Bar lists current — suppresses local SEO."))
story.append(b("<b>Solo capacity ceiling.</b> No staff — intake, casework, and admin all compete for his time."))
story.append(b("<b>No transcript data.</b> Revenue and case value are inferred defaults — confirm on call."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Danton Legal goes from invisible to findable — IP prospects in Pasadena find the firm, read about Richardson's track record, and request consultations."))
story.append(bd("Website enables ads, ads drive traffic, SEO captures organic leads, GBP unlocks LSA — all four channels launch simultaneously."))
story.append(bd("Client inquiries come in through the system — not through Richardson's personal network."))

story.append(Paragraph("<b>Full Service Marketing Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("~$500K revenue places firm in $400K–$1M Starter tier. New brand requires full-service, not ads-only."))
story.append(b("Website build is mandatory — dantonlegal.com is a blank placeholder. Full Service required for any rebuild."))
story.append(b("Pasadena is Tier 2 (LA metro) — Cotman IP, Soni Law, and Mandour & Associates already running multi-channel campaigns."))
story.append(b("Ad spend at $6,000–$6,500/mo is cap-constrained at ~$500K revenue. Confirm actual revenue to unlock higher budget."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Peer access to firm owners at the same solo-to-scalable transition — avoiding mistakes they already made."))
story.append(bd("Builds intake process and financial baseline alongside the marketing launch — not after."))
story.append(bd("Monthly 1:1 calls keep growth on track and surface bottlenecks before they cost revenue."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("$400K–$1M revenue tier. FCOO excluded (under $500K threshold) — revisit at Phase 2 when revenue exceeds $750K."))
story.append(b("Weekly group sessions, monthly 1:1, masterminds, quarterly workshops, annual in-person event included."))
story.append(b("No transcript — position coaching around intake system build and financial tracking as immediate wins."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Danton Legal — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Paid ads put Danton Legal in front of high-intent IP and trademark prospects in Pasadena the moment the website goes live — before organic SEO has time to build."))
story.append(bd("At an estimated $7,500 average case value, even 3–4 signed clients per month from paid ads more than covers the total SMB Team investment."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $6,000/mo — Google PPC, LSA, Meta Retargeting, Meta Lead Gen across IP/trademark/entertainment keywords."))
story.append(b("<b>Aggressive:</b> $6,500/mo — full budget within 35% cap at estimated $500K revenue. Confirm revenue to unlock higher spend."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~7 cases x $7,500 = ~$52,500/mo vs. $6,000 spend = ~8.8x return."))
story.append(b("<b>Aggressive:</b> ~10 cases x $7,500 = ~$75,000/mo vs. $6,500 spend = ~11.5x return."))
story.append(Paragraph("<i>All figures are estimates. Case value of $7,500 is a conservative blend of transactional and litigation IP matters. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Business Law/IP minimums: PPC $3,500 + LSA $2,000 + Meta Ret $1,200 + Meta Lead $3,500 = $10,200 — cap-constrained to $6,000 at ~$500K revenue."))
story.append(b("<b>Aggressive:</b> $1M target x 20% / 12 = $16,667 x 1.3 (Tier 2) = $21,667 minus $4,847 fee = $16,820 — cap-constrained to $6,500 at ~$500K revenue."))
story.append(b("Total at aggressive: $8,047 + $6,500 = $14,547/mo = 34.9% of monthly revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I already get referrals — do I really need all of this?"', S["objection_q"]))
story.append(Paragraph("Referrals are not predictable or scalable. The Soni Law Firm is in the same Pasadena ZIP code with the same practice areas and is fully findable online. Every IP prospect searching right now who finds Soni instead of Richardson is a referral that never arrives.", S["objection_a"]))

story.append(Paragraph('"Can\'t I just build the website and GBP myself?"', S["objection_q"]))
story.append(Paragraph("An SEO-optimized, conversion-focused site integrated with Ads and GBP takes months solo. Cotman IP and Mandour & Associates already hold top paid and organic positions. Every month of slow launch is cases those firms sign instead.", S["objection_a"]))

story.append(Paragraph('"The ad spend feels low."', S["objection_q"]))
story.append(Paragraph("$6,000–$6,500 is constrained by the 35% cap at ~$500K estimated revenue. At $750K revenue the budget rises to ~$10,000/mo. Confirm actual revenue on the call — the right budget may be significantly higher.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website build, Google Ads, Local SEO, GBP, LSA, monthly reporting.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, monthly 1:1, masterminds, quarterly workshops, annual event.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$6,000–$6,500/mo", S["price_main"])],
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
    "Total: $8,047/mo + $6,000–$6,500 ad spend  |  Save $1,147/mo by bundling  |  33.7%–34.9% of est. revenue (under 35% cap)",
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
