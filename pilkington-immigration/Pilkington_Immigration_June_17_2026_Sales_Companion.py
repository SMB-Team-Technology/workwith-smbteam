"""
Sales Companion PDF — Pilkington Immigration
Sales Rep: Jonathan Farace
Date: June 17, 2026
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

OUTPUT_PATH = "pilkington-immigration/Pilkington_Immigration_06172026_Sales_Companion.pdf"


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

story.append(Paragraph("Pilkington Immigration", S["title"]))
story.append(Paragraph("Sales Companion  |  June 17, 2026  |  Rep: Jonathan Farace", S["subtitle"]))
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
    [Paragraph("Andrew Maloney", S["snap_value"]),
     Paragraph("~$3M USD/yr", S["snap_value"]),
     Paragraph("30 (8–9 atty)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("~15% (est.)", S["snap_value"]),
     Paragraph("Guelph ON (HQ) +4", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM — CEO TRANSITION", S["section"]))
story.append(Paragraph("Andrew wants to stop running the day-to-day and become a true owner — the firm should grow without requiring his personal presence in every decision.", S["subsection"]))

story.append(quote_block("Still heavily in-the-business day-to-day; wants to move toward more of an owner/CEO role."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Fixed marketing engine.</b> Google Ads was generating 1.5:1 ROI a year ago — now below 0.5:1. This is his primary ask."))
story.append(bd("<b>New lead channels.</b> LSA and paid social are both untouched; he wants diversification, not just a patched single source."))
story.append(bd("<b>Geographic expansion.</b> London ON, Edmonton, Ottawa, Calgary — specific markets named on the call."))
story.append(bd("<b>CEO role transition.</b> 30 employees, 5 offices, a U.S. acquisition — the firm has outgrown being run by one person."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Broken paid channel.</b> $10K/month at sub-0.5:1 ROI — losing money on the primary growth engine since summer 2024."))
story.append(b("<b>No management layer.</b> All decisions route through Andrew — nothing runs without him because nothing is delegated."))
story.append(b("<b>No intake team.</b> Attorneys handle consultations at uneven close rates — conversion is person-dependent, not process-driven."))
story.append(b("<b>No outside accountability.</b> First-time coaching client — will need trust established before fully leaning into coaching."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Stops the bleeding first — rebuilt Google Ads account ends the $5K+/month losses and targets positive ROI within 90 days."))
story.append(bd("Opens two new channels (LSA + Meta) so the firm is never again dependent on one broken source."))
story.append(bd("Puts Pilkington's brand in 8 Ontario expansion markets ahead of competitors at a fraction of Google PPC cost."))

story.append(Paragraph("<b>Full Service Marketing — Platinum  |  $15,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $3M USD = Platinum tier ($3M+ threshold); aggressive goals (2x = $6M) confirm higher tier."))
story.append(b("Website rebuild needed: no attorney bios, no video, no inline form, 55-site PageSpeed unverified."))
story.append(b("Multi-location, multi-practice firm requires full-service — not an ads-only sub-package."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the management layer — a Fractional COO Director creates the structure that lets Andrew step back from daily decisions."))
story.append(bd("Integrates Orlando — unified systems across Canadian and U.S. practices so one person is not running two separate firms."))
story.append(bd("Master's Circle peer group delivers the accountability and law firm playbooks he has been building without for 10+ years."))

story.append(Paragraph("<b>Master's Circle + FCOO Director  |  $8,394/mo bundled</b>", S["subsection"]))
story.append(b("$3M revenue + 30-person team + dedicated staff (Brian Gill) = Master's Circle eligible."))
story.append(b("DBM is CEO transition — FCOO Director builds exactly the operational framework Andrew needs."))
story.append(b("First-time coaching client: Director is right entry point; FCOO Partner is the Phase 2-3 upgrade. Saves $2,400/mo vs. standalone."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Pilkington Immigration — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Conservative ($10K/mo) optimizes what he is already spending — same budget, rebuilt structure, estimated 6.8:1 return vs. current sub-0.5:1 loss."))
story.append(bd("Aggressive ($50K/mo) opens the geographic expansion he described — 90 cases/month estimated, $405K/month revenue from ads at 8.1:1 return."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $10,000/mo — matches current spend; optimized structure across Google PPC + new LSA + Meta retargeting."))
story.append(b("<b>Aggressive:</b> $50,000/mo — scales to priority expansion markets; within 35% revenue cap at current $250K/mo revenue."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 15 cases x $4,500 avg = $67,500/mo vs. $10,000 spend = 6.8x return (est.)."))
story.append(b("<b>Aggressive:</b> 90 cases x $4,500 avg = $405,000/mo vs. $50,000 spend = 8.1x return (est.)."))
story.append(Paragraph("<i>All figures are estimates based on immigration CPL benchmarks and 15% default close rate. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Immigration channel minimums: Google PPC $3,000 + LSA $2,000 + Meta retargeting $1,200 + Meta lead gen $3,000 = $9,200; rounded to $10,000."))
story.append(b("<b>Aggressive:</b> $6M goal x 20% / 12 = $100K. Tier 3 blended geo (1.15x) = $115K. Minus $15,997 fee = $99K; capped at $50K by 35% rule."))
story.append(b("Total at aggressive: $24,391 fees + $50,000 ads = $74,391/mo = 29.8% of revenue. Under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"Why would more spend fix what isn\'t working on Google Ads?"', S["objection_q"]))
story.append(Paragraph("It is not about more spend — it is a structural account problem from the 2024 algorithm update. We rebuild first; spend does not increase until ROI is positive. Same $10K/month in a rebuilt account projects at 6.8x vs. current sub-0.5:1.", S["objection_a"]))

story.append(Paragraph('"I\'ve never worked with a coach — I\'m not sure I need that."', S["objection_q"]))
story.append(Paragraph("Growing to $3M alone is what is now limiting the firm. A 30-person firm cannot scale with one person making all decisions. FCOO Director builds the management layer — Andrew gets to lead, not operate.", S["objection_a"]))

story.append(Paragraph('"$24K/month is significant — what if it doesn\'t work?"', S["objection_q"]))
story.append(Paragraph("$24,391 is 9.8% of monthly revenue — well under the 35% benchmark. Conservative ad projection is $67,500/month at 6.8x. The bigger risk: losing $5,000+/month on a broken ad account with no plan to fix it.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Platinum</b>", S["price_main"]),
     Paragraph("$15,997/mo", S["price_main"])],
    [Paragraph("Google Ads rebuild, LSA, Meta ads, website/SEO across 5 offices.", S["price_detail"]),
     Paragraph("<strike>$18,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle + FCOO Director</b>", S["price_main"]),
     Paragraph("$8,394/mo", S["price_main"])],
    [Paragraph("Fractional COO Director, Master's Circle peer group, weekly coaching.", S["price_detail"]),
     Paragraph("<strike>$10,794</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$10,000–$50,000/mo", S["price_main"])],
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
    "Total: $24,391/mo + $10,000–$50,000 ad spend  |  Save $5,400/mo by bundling  |  13.8%–29.8% of revenue (under 35% cap)",
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
