"""
Sales Companion PDF — Saltiel Law Group
Generated: May 7, 2026 | Rep: Dan Bryant
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

OUTPUT_PATH = "/home/user/workwith-smbteam/saltiel-law-group/SaltielLawGroup_05072026_Sales_Companion.pdf"


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
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY,
                       spaceBefore=3, spaceAfter=3)

def quote_block(text):
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

story.append(Paragraph("Saltiel Law Group", S["title"]))
story.append(Paragraph("Sales Companion  |  May 7, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Moises Saltiel", S["snap_value"]),
     Paragraph("$3–5M", S["snap_value"]),
     Paragraph("4–5 people", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("11%", S["snap_value"]),
     Paragraph("Coral Gables, FL", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: SCALE WITHOUT THE CEILING", S["section"]))
story.append(Paragraph("Moises wants to build a firm that reaches $6M and runs on systems — not on him personally closing every client.", S["subsection"]))

story.append(quote_block("We have 83 leads and we're getting 9 clients... our close rate is probably around 11%... we know there's a problem there."))
story.append(Spacer(1, 1))
story.append(quote_block("Moises is the one doing all the consultations... he's the one closing every client."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Revenue to $6M.</b> Specific goal, current gap — actively tracking it."))
story.append(bd("<b>Intake without him.</b> Can't scale past his personal hours closing every client."))
story.append(bd("<b>Bilingual paid lead gen.</b> Organic is vulnerable; needs a reliable bilingual system."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No paid infrastructure.</b> Never run ads — zero data, no campaigns while competitors spend monthly."))
story.append(b("<b>11% conversion.</b> 74 leads/month walking out; faster ROI than any new marketing spend."))
story.append(b("<b>No delegation.</b> Close process lives in Moises's head — undocumented, untrainable."))
story.append(b("<b>Competitors ahead.</b> Trembly confirmed on Google Ads; EPGD has 342+ reviews and content authority."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts Saltiel at the top of Google in English and Spanish — capturing clients competitors can't reach."))
story.append(bd("Builds bilingual paid lead flow for the first time — predictable, not algorithm-dependent."))

story.append(Paragraph("<b>Full Service Marketing — Platinum  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("$3–5M revenue, $6M goal, bilingual Miami market — Platinum is the correct tier."))
story.append(b("First-time advertiser: full EN+ES infrastructure needed from scratch; lower tiers are underpowered."))
story.append(b("Miami = Tier 2 (1.3×); Spanish multiplier (1.33×); conservative spend lands at $5,000/mo within cap."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Removes Moises as the bottleneck — delegation frameworks, documented close process, team accountability."))
story.append(bd("Installs financial visibility: CAC tracking, margin analysis, profit planning toward $6M."))

story.append(Paragraph("<b>Master's Circle + FCOO Director  |  $4,394/mo bundled</b>", S["subsection"]))
story.append(b("$3–5M revenue, 5+ defined-role team — Master's Circle + FCOO Director row applies."))
story.append(b("Moises is sole closer; FCOO Director builds the infrastructure to delegate that role."))
story.append(b("No CAC or profit plan exists; peer group has already solved the problems he faces now."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Saltiel Law Group — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("First paid system in firm history — EN+ES search and LSA generating ~22–44 leads/mo on top of organic."))

story.append(Paragraph("<b>Range: $5,000–$10,000/mo (estimates — not guaranteed)</b>", S["subsection"]))
story.append(b("<b>Conservative $5K:</b> 4–5 cases × $10K = ~$45K/mo | ~9× ROAS | ~3× total SMB investment."))
story.append(b("<b>Aggressive $10K:</b> 8–9 cases × $10K = ~$85K/mo | ~8.5× ROAS | ~4× total SMB investment."))
story.append(b("<b>Calc:</b> Biz Law minimums × 1.33 bilingual = $5K conservative. $6M×20%÷12 = $100K → capped at $10K."))
story.append(b("Total at aggressive: $19,391/mo = 7.8% of revenue — well under 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We\'ve always been organic-first — never run paid ads."', S["objection_q"]))
story.append(Paragraph("Trembly is confirmed running Google Ads for your exact keywords right now — showing above your organic listings. Every month without paid extends their lead. Organic rankings are also not protected from algorithm changes.", S["objection_a"]))

story.append(Paragraph('"The fees feel like a lot before ad spend."', S["objection_q"]))
story.append(Paragraph("At 11% conversion the firm is leaving ~$740K/mo in potential revenue unconverted from leads it already has. Activating Clio Grow alone is projected to add 7–8 clients/month at zero additional ad cost. The math justifies the investment.", S["objection_a"]))

story.append(Paragraph('"We have Clio Grow — isn\'t intake handled?"', S["objection_q"]))
story.append(Paragraph("Clio Grow is installed but automation is not activated. 83 leads/month at 11% close means the tool exists but is not doing the work. This engagement turns it on and adds structure on top.", S["objection_a"]))

story.append(Paragraph('"Can we do marketing only and skip coaching?"', S["objection_q"]))
story.append(Paragraph("More leads into a broken intake system won't produce the expected results — Moises is already the bottleneck at 11% on 83 existing leads. Marketing fills the funnel; coaching and FCOO fixes what happens after the lead arrives.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Platinum</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("Bilingual paid search (EN+ES), LSA, Meta Ads, SEO, landing pages, reporting.", S["price_detail"]),
     Paragraph("<strike>$7,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Master's Circle + FCOO Director</b>", S["price_main"]),
     Paragraph("$4,394/mo", S["price_main"])],
    [Paragraph("Fractional COO Director, group coaching, masterminds, quarterly workshops, 1 annual in-person.", S["price_detail"]),
     Paragraph("<strike>$7,794</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$5,000–$10,000/mo", S["price_main"])],
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
    "Total: $9,391/mo + $5,000–$10,000 ad spend  |  Save $6,400/mo by bundling  |  1.2%–7.8% of revenue (well under 35% cap)",
    S["savings"]))

# ── Build ──
doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

try:
    from pypdf import PdfReader
    r = PdfReader(OUTPUT_PATH)
    page_count = len(r.pages)
    print(f"Page count: {page_count}")
    if page_count != 2:
        print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
except ImportError:
    print("pypdf not available for page count check.")
