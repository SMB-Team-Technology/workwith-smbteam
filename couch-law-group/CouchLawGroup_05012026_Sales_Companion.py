"""
Sales Companion PDF — Couch Law Group
Generated: May 01, 2026  |  Rep: Randy Gold
Internal use only. Do not share with client.
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

OUTPUT_PATH = "couch-law-group/CouchLawGroup_05012026_Sales_Companion.pdf"


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

story.append(Paragraph("Couch Law Group", S["title"]))
story.append(Paragraph("Sales Companion  |  May 01, 2026  |  Rep: Randy Gold", S["subtitle"]))
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
    [Paragraph("Jordan Couch", S["snap_value"]),
     Paragraph("$20K / 3 wks", S["snap_value"]),
     Paragraph("3 (incl. Annie)", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("~80% qualified", S["snap_value"]),
     Paragraph("Cashiers, NC", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FREEDOM", S["section"]))
story.append(Paragraph("Jordan and Annie came home to Western NC to build a firm that earns at the highest level and still lets them live the life they chose — not to become the ceiling of everything they are building.", S["subsection"]))

story.append(quote_block("I want to work four days a week."))
story.append(Spacer(1, 1))
story.append(quote_block("We came home to be part of this community — that's why we moved back."))
story.append(Spacer(1, 1))
story.append(quote_block("I want to take home $250,000 to $300,000 a year."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>A four-day work week.</b> Jordan said it directly — he wants a firm that runs without him on day five."))
story.append(bd("<b>Predictable take-home income.</b> $250K–$300K/yr — not discovered at year-end, planned for from day one."))
story.append(bd("<b>Firm that owns the local market.</b> The only civil litigator in the five-county region serious about digital presence."))
story.append(bd("<b>A life in his community.</b> Jordan and Annie moved home — the firm should fund that life, not consume it."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Zero digital presence.</b> No GBP, no ads, no directory listings — the firm is invisible to every online search."))
story.append(b("<b>Jordan is the bottleneck.</b> Every intake, every case decision, every admin task runs through him personally."))
story.append(b("<b>No financial visibility.</b> No bookkeeper, no accountant — no way to know if the $300K goal is on track."))
story.append(b("<b>Intake has no system.</b> Manual phone-only follow-up means leads outside business hours are permanently lost."))
story.append(b("<b>Previous financial disruption.</b> Prior bookkeeper dropped under SEC investigation — books are in an unclear state."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts Couch Law Group on the map in Google, LSA, and directories before any local competitor claims that ground."))
story.append(bd("Generates qualified civil litigation and personal injury leads without Jordan personally working referral networks."))
story.append(bd("Builds the digital foundation — website, SEO, paid ads — that makes a four-day work week financially viable."))

story.append(Paragraph("<b>Full Service Marketing Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("PI practice area eliminates Essentials tier — Starter is the minimum eligible package for personal injury."))
story.append(b("Firm is three weeks old with no GBP, no indexed website, and no paid ads — needs full-service buildout, not a sub-package."))
story.append(b("Cashiers/Highlands market is Tier 5 rural — uncontested by local digital competitors, ideal conditions for Starter to dominate quickly."))
story.append(b("Website rebuild required: site returned 403 errors, not indexed, no practice area pages, no bios, no conversion path."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Jordan a structured framework to delegate intake and admin so he stops being the bottleneck at every step."))
story.append(bd("Defines Vanessa's role and Annie's role with scorecards — converting raw team capacity into actual operational leverage."))
story.append(bd("Builds the profit plan and financial clarity that makes $250K–$300K take-home a designed outcome, not a hope."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue under $500K — FCOO and FCFO products are not eligible; Elite Coach is the correct tier."))
story.append(b("Three-person team with no defined roles, no KPIs, and no accountability structure — coaching delivers the framework now."))
story.append(b("Firm is three weeks old — habits built in the first 90 days become the operating model for years; coaching shapes them early."))
story.append(b("Previous bookkeeper situation (SEC investigation) left financial records in disarray — coaching helps establish clean infrastructure."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Couch Law Group — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Activates a predictable lead pipeline in a market where no local competitor is currently running paid ads — first mover owns it."))
story.append(bd("Converts the wide-open Cashiers/Highlands digital landscape into paying civil litigation and injury cases before larger statewide firms claim the territory."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $2,400/mo — PI hard floor (low competitiveness, Tier 5 rural); Google PPC $1,500 + LSA $900."))
story.append(b("<b>Aggressive:</b> $4,000/mo — adds Meta retargeting; elevated to accelerate Y1 growth goals."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~3 cases x $5,000 avg = $15,000/mo revenue vs $2,400 spend = 6.3x return. (Est. only.)"))
story.append(b("<b>Aggressive:</b> ~5 cases x $5,000 avg = $25,000/mo revenue vs $4,000 spend = 6.3x return. (Est. only.)"))
story.append(Paragraph("<i>Case value uses practice area default ($5,000). Close rate 80% (prospect-stated). All figures are estimates. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> PI low-competitiveness channel minimums: Google PPC $1,500 + LSA $900 = $2,400."))
story.append(b("<b>Aggressive:</b> Reverse math: $300K goal ÷ 12 = $25K/mo target. 5 cases ÷ 80% = 6.25 leads. x $400 blended CPL (Tier 5) = $2,500. Elevated to $4,000 to fund Meta retargeting layer."))
story.append(b("<b>35% rule note:</b> At conservative, total SMB spend = $9,947/mo vs ~$26,667/mo run rate = 37.3%. Marginally over cap on a 3-week revenue sample — flag for scoping review; expect ratio to improve as revenue scales."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"The firm is only three weeks old — is this the right time to spend this much?"', S["objection_q"]))
story.append(Paragraph("The competitor building digital presence right now is Coward, Hicks & Siler — established since 1951 with GBP reviews and 3-pack positions across the five counties. Every week without a GBP is a week their lead stays permanent. The cheapest time to build is before a competitor accelerates.", S["objection_a"]))

story.append(Paragraph('"I\'m already billing everything I have — how do I add this to my plate?"', S["objection_q"]))
story.append(Paragraph("That's exactly the problem we're solving. The marketing and coaching run without Jordan's day-to-day involvement. The first 90 days include defining Vanessa's intake role specifically so Jordan stops being the one in every step — his plate gets lighter, not heavier.", S["objection_a"]))

story.append(Paragraph('"I don\'t have a GBP or a real website yet — can ads even work?"', S["objection_q"]))
story.append(Paragraph("GBP setup and website rebuild are included in Starter. We build the foundation first, then activate ads when the conversion infrastructure is ready. Nothing goes live until the site is optimized to capture the leads ads send.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website rebuild, Google Ads, LSA, local SEO, GBP management, Meta Ads.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, practice area masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$2,400–$4,000/mo", S["price_main"])],
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
    "Total: $7,447/mo + $2,400–$4,000 ad spend  |  Save $1,747/mo by bundling  |  35% rule: marginally over on 3-wk sample — flag for scoping review",
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
else:
    print("OK: exactly 2 pages.")
