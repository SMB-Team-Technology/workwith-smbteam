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
story.append(Spacer(1, 1))
story.append(quote_block("78% of our clientele is Latin or Spanish-speaking... we have a bilingual website, English and Spanish."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Revenue to $6M.</b> He has a specific goal and a current gap — this is a number he is actively tracking."))
story.append(bd("<b>Intake that runs without him.</b> He cannot scale past his personal hours if he closes every client personally."))
story.append(bd("<b>Paid lead gen in both languages.</b> Organic is working but vulnerable — he wants a system that generates bilingual leads reliably."))
story.append(bd("<b>A firm that doesn't need him at the center.</b> The goal is ownership, not just employment."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No paid infrastructure.</b> The firm has never run ads — zero paid data, no benchmarks, no campaigns running while competitors spend monthly."))
story.append(b("<b>11% intake conversion.</b> 74 leads per month are walking out the door; fixing this is faster ROI than any marketing spend."))
story.append(b("<b>No closing delegation.</b> The consultation and close process lives in Moises's head — undocumented, undelegatable."))
story.append(b("<b>No acquisition cost data.</b> Cannot make confident scaling decisions without knowing what each new client costs to acquire."))
story.append(b("<b>Competitors moving fast.</b> Trembly confirmed running Google Ads; EPGD has 342+ reviews and dominant content authority."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts Saltiel at the top of Google in English and Spanish — above organic, above the map pack — capturing the exact clients competitors are missing."))
story.append(bd("Generates bilingual paid leads on a consistent, predictable cadence for the first time in the firm's history."))
story.append(bd("Builds the review and LSA presence needed to compete with EPGD and Trembly on every Google surface."))

story.append(Paragraph("<b>Full Service Marketing — Platinum  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $3–5M with a $6M goal and aggressive bilingual market — Platinum is the correct tier."))
story.append(b("First-time advertiser: needs full infrastructure built from scratch in both English and Spanish simultaneously."))
story.append(b("Spanish campaign multiplier (1.33x) brings conservative ad spend to $5,000/mo — within Platinum cap."))
story.append(b("Miami is Tier 2 geo market (1.3x multiplier) — Starter or Growth tiers would be underpowered for this market."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Moises the peer group, accountability, and fractional COO support needed to delegate intake and stop being the firm's revenue ceiling."))
story.append(bd("Builds the operational structure — documented processes, team accountability, hiring frameworks — that makes scaling to $6M possible without adding chaos."))
story.append(bd("Provides financial operations oversight so Moises knows his acquisition costs, margins, and take-home as he scales — not after the fact."))

story.append(Paragraph("<b>Master's Circle + FCOO Director  |  $4,394/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $3–5M, 5+ team members with defined roles — Master's Circle + FCOO Director row applies."))
story.append(b("Moises is the sole closer — FCOO Director builds the delegation infrastructure and closes that gap."))
story.append(b("No profit plan or CAC tracking exists — FCOO Director installs financial visibility immediately."))
story.append(b("Master's Circle peer group gives Moises access to owners who have already solved the exact problems he is facing."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Saltiel Law Group — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Creates the first paid lead generation system in the firm's history — English and Spanish, paid search and LSA, running 24/7 without Hector manually driving each lead."))
story.append(bd("Generates an estimated 22–44 additional qualified leads per month, layered on top of existing organic volume."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $5,000/mo — minimum viable bilingual paid presence across Google Search, LSA, and Meta retargeting."))
story.append(b("<b>Aggressive:</b> $10,000/mo — full bilingual paid lead generation at Platinum tier cap."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 4–5 cases x $10K avg value = ~$45K/mo vs. $5K spend = ~9x ROAS (~3x on total SMB investment)."))
story.append(b("<b>Aggressive:</b> 8–9 cases x $10K avg value = ~$85K/mo vs. $10K spend = ~8.5x ROAS (~4x on total SMB investment)."))
story.append(Paragraph("<i>All figures are estimates based on industry averages. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Business Law minimums: PPC $1,500 + LSA $1,000 + Meta $700 = $3,200 x 1.33 bilingual = $4,256 → $5,000."))
story.append(b("<b>Aggressive:</b> $6M goal x 20% / 12 = $100K budget. Minus $4,997 fee = $95K available — exceeds Platinum cap of $15K. Capped at $10,000."))
story.append(b("Total spend at aggressive: $9,391 + $10,000 = $19,391/mo = 7.8% of current revenue — well under 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"We\'ve always been organic-first — we\'ve never run paid ads."', S["objection_q"]))
story.append(Paragraph("Organic built the firm to $3–5M, which is a real achievement. But Trembly is confirmed running Google Ads for your exact keywords right now, and they are showing up above your organic listings. Every month without paid is a month they extend that lead — and your organic rankings are not protected from algorithm changes.", S["objection_a"]))

story.append(Paragraph('"The budget feels like a lot — almost $10K in management fees before ad spend."', S["objection_q"]))
story.append(Paragraph("At 11% conversion, the firm is leaving roughly $740K/mo in potential revenue unconverted from leads it already has. The intake work alone — activating Clio Grow automation and adding scheduling — is expected to add 7–8 clients/month without any new ad spend. The question is not whether the investment is large; it is whether the return justifies it — and the math says it does.", S["objection_a"]))

story.append(Paragraph('"We already have Clio Grow — isn\'t our intake fine?"', S["objection_q"]))
story.append(Paragraph("Clio Grow is in place but the automation features are not activated. The firm is at 11% conversion with 83 leads/month — the tool exists, but it is not doing the work. This engagement activates what is already paid for and layers a structured follow-up system on top of it.", S["objection_a"]))

story.append(Paragraph('"Can we just start with marketing and skip the coaching package?"', S["objection_q"]))
story.append(Paragraph("Marketing will generate more leads — but Moises is already the bottleneck on converting the 83 leads he has at 11%. More leads into a broken intake system will not produce the results he is expecting. The two packages are designed to work together: marketing fills the top of the funnel, coaching and FCOO fixes conversion and operations below it.", S["objection_a"]))

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
