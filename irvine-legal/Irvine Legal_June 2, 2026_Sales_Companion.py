"""
Sales Companion PDF — Irvine Legal
June 2, 2026 | Rep: Dan Bryant
Internal document — do not share with client.
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

OUTPUT_PATH = "irvine-legal/Irvine Legal_June 2, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Irvine Legal", S["title"]))
story.append(Paragraph("Sales Companion  |  June 2, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Joshua Irvine", S["snap_value"]),
     Paragraph("~$780K/yr", S["snap_value"]),
     Paragraph("8–9 staff", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("High (ref); 15% (ads)", S["snap_value"]),
     Paragraph("Layton, UT", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: TIME FREEDOM + MISSION", S["section"]))
story.append(Paragraph("Joshua wants a firm that runs without him so he can take a 6-week Himalaya trip and fully fund his nonprofit education work.", S["subsection"]))

story.append(quote_block("I want to take a 6-week Himalaya hiking trip when the firm is self-sustaining."))
story.append(Spacer(1, 1))
story.append(quote_block("The firm can run 1-2 weeks without me before things start to break — contract reviews pile up, litigation deadlines get close."))
story.append(Spacer(1, 1))
story.append(quote_block("I'm financially comfortable but not motivated purely by money — the revenue growth funds the nonprofit work."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Freedom from daily dependency.</b> Wants the firm to run 6+ weeks without him — not 1-2."))
story.append(bd("<b>A funded nonprofit mission.</b> Education Elevated and women's education initiative need predictable profit to operate."))
story.append(bd("<b>A scalable subscription model.</b> Wants to grow the outsourced general counsel business to $5M-$8M."))
story.append(bd("<b>Time with young kids.</b> Stated financial means exist but time freedom does not yet."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No digital lead system.</b> 100% referral-dependent — revenue is capped by referral volume."))
story.append(b("<b>Personal litigation bottleneck.</b> Handles all 20-25 active cases himself; no second attorney in place."))
story.append(b("<b>Zero Google reviews.</b> Completely invisible in local search — competitors with 8-22 reviews hold every map pack slot."))
story.append(b("<b>No operations playbook.</b> Firm knowledge lives in Joshua's head; delegation is limited by documentation gaps."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds a predictable subscription client pipeline independent of referrals — monthly revenue stops depending on word-of-mouth."))
story.append(bd("Captures the 'outsourced general counsel for contractors' keyword window before competitors figure it out."))

story.append(Paragraph("<b>Full Service Marketing Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $780K/yr: Starter tier ($400K-$1M). No PI restrictions; Tier 4 market (Layton/Davis County, UT)."))
story.append(b("Website rebuild required (5+ yr old design, no bio, no homepage form) — Full Service mandatory, not ads-only."))
story.append(b("NAP inconsistency (dual address), 0 Google reviews, no map pack visibility — all core deliverables address these."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the intake process for ad-generated leads and the profit tracking that shows what Joshua actually keeps."))
story.append(bd("Keeps the $100K/month goal on a structured timeline — not a vague aspiration."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K-$1M; Fractional COO hidden under $1M — add at Phase 2 when $100K/month is reached."))
story.append(b("Weekly coaching + practice area masterminds + quarterly workshops + 1 annual in-person; all included."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Irvine Legal — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Subscription LTV ($24K per client at $1K/mo x 24 months) makes standard CPL projections dramatically conservative."))
story.append(bd("First-mover on 'outsourced general counsel for contractors' — no competitor owns this keyword in Utah."))

story.append(Paragraph("<b>Ad Spend Range &amp; Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative $5,000/mo:</b> 42 leads x 15% = 6 cases x $5K = $30K revenue; 6x return. (Bus. Law minimums: PPC $3,500 + Meta $1,200.)"))
story.append(b("<b>Aggressive $14,500/mo:</b> 145 leads x 15% = 22 cases x $5K = $110K revenue; 7-8x return. ($1.2M goal x 20%/12 = $15,153; capped at $14,500 for 35% compliance.)"))
story.append(b("Total at aggressive: $8,047 + $14,500 = $22,547/mo = 34.7% of revenue — under 35% cap."))
story.append(Paragraph("<i>Estimates using $5K default case value. Subscription LTV is significantly higher. Not guaranteed.</i>", S["disclaimer"]))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I tried Google Ads before and it didn\'t work."', S["objection_q"]))
story.append(Paragraph("His $1,000 test had no strategy, no landing page, no follow-through — not a failed channel, a failed experiment. A managed campaign with keyword targeting and call tracking is categorically different.", S["objection_a"]))

story.append(Paragraph('"LSA was too expensive — $120/lead vs. $60 for PPC."', S["objection_q"]))
story.append(Paragraph("Correct call — with zero reviews, LSA is not competitive regardless of CPL. PPC first, build to 10+ reviews, then layer in LSA. Dan already aligned on this approach.", S["objection_a"]))

story.append(Paragraph('"What\'s the ROI on the subscription model specifically?"', S["objection_q"]))
story.append(Paragraph("At $1K/mo x 24 months = $24K LTV per subscription client. At 6 conservative clients/month, that is $144K in lifetime value from $5K in ad spend — 28x+ lifetime return.", S["objection_a"]))

story.append(Paragraph('"I\'m probably going to go with you guys — I just need to see the numbers."', S["objection_q"]))
story.append(Paragraph("Buying signal. Lead with subscription LTV math, not default case values. Anchor with the review gap (0 vs. SSHK's 22) and the zero-competition keyword window.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, Google Ads, Local SEO, Meta campaigns, monthly reporting.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, practice area masterminds, quarterly workshops, 1 annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,000–$14,500/mo", S["price_main"])],
    [Paragraph("Goes to Google and Meta directly — not to SMB Team.", S["price_detail"]),
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
    "Total SMB fees: $8,047/mo + $5,000–$14,500 ad spend  |  Save $1,147/mo by bundling  |  13.1%–22.7%+ of $65K revenue (under 35% cap)",
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
