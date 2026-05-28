"""
Sales Companion PDF — Truman Law
SMB Team | May 28, 2026 | Rep: Randy Gold
Internal use only — do not share with client.
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

DARK_NAVY = HexColor("#1a2332")
ACCENT_GREEN = HexColor("#3B6D11")
MEDIUM_GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#888888")
RULE_GRAY = HexColor("#CCCCCC")
QUOTE_BG = HexColor("#F5F7F0")
WHITE = HexColor("#FFFFFF")
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "truman-law/TRUMAN_LAW_05282026_Sales_Companion.pdf"


def add_page_elements(canvas, doc):
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

S = {}
S["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=9.5, leading=13, textColor=LIGHT_GRAY, spaceAfter=3)
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=ACCENT_GREEN, spaceBefore=6, spaceAfter=2)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.5, leading=13, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9.5, leading=13, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9.5, leading=13, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9.5, leading=12, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9.5, leading=13, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=2)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8.5, leading=11, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


def b(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY, spaceBefore=3, spaceAfter=3)

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

story.append(Paragraph("Truman Law", S["title"]))
story.append(Paragraph("Sales Companion  |  May 28, 2026  |  Rep: Randy Gold", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Harkirat Singh Kang", S["snap_value"]),
     Paragraph("~$400K est.", S["snap_value"]),
     Paragraph("Solo est.", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("Surrey, BC", S["snap_value"])],
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

story.append(Paragraph("Dominant Buying Motive: COMMUNITY LEGACY &amp; SCALE", S["section"]))
story.append(Paragraph("Build Truman Law into the recognized name in Surrey's South Asian community — a firm that generates clients predictably without Harkirat bottlenecking every file.", S["subsection"]))

story.append(quote_block("Tagline: Clarity. Confidence. Completion. — signals intent to deliver at scale, not just solo."))
story.append(Spacer(1, 1))
story.append(quote_block("Founded 2020; expanded from litigation into real estate 2021 and into six more practice areas — consistent ambition to grow beyond initial scope."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Digital visibility.</b> Truman Law found on Google for real estate and business law before anyone calls a competitor."))
story.append(bd("<b>Scalable client flow.</b> New clients arriving through systems — not dependent on the next referral or personal connection."))
story.append(bd("<b>Firm ownership.</b> Step back from being the sole operator and run Truman Law as a business, not just a practice."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>Zero digital visibility.</b> Not in 3-pack for any practice area; ~20 reviews vs. 131 (Keystone), 100 (Walia); no ads running."))
story.append(b("<b>No intake system.</b> Solo attorney handles all contact; no after-hours capture; no documented follow-up process."))
story.append(b("<b>No team structure.</b> Cannot absorb marketing-generated volume without a first hire and documented intake process."))
story.append(b("<b>Revenue unconfirmed.</b> No transcript — confirm revenue, close rate, and avg case value on the call before finalizing."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts Truman Law on page one of Google for real estate and business law in Surrey — for the first time."))
story.append(bd("Builds 3-pack visibility and closes the review gap — making Truman Law the community's visible, credible default choice."))

story.append(Paragraph("<b>Full Service Marketing Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Practice areas (real estate, business law, private lending) not PI or high-comp criminal — Starter tier eligible."))
story.append(b("Estimated revenue ~$400K puts firm in $400K–$1M tier; Surrey (Greater Vancouver metro) is competitive enough for full service."))
story.append(b("Website has no geo-targeted pages, PageSpeed unverified — full service includes website optimization before ads launch."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the intake process and conversion habits that turn marketing leads into signed clients consistently."))
story.append(bd("Provides the peer group and accountability framework to make the first team hire and delegate successfully."))

story.append(Paragraph("<b>Elite Coach Plus  |  $2,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$400K, solo team — Elite Coach Plus is the correct tier; Master's Circle and fractional products are ineligible."))
story.append(b("No intake system currently exists — coaching builds the documented process needed before a support hire can work independently."))
story.append(b("Weekly peer group sessions provide accountability and real estate/business law growth strategies a solo practitioner cannot access alone."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Truman Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts Truman Law in front of Surrey residents actively searching for a real estate or business lawyer — highest-intent leads available."))
story.append(bd("Generates a consistent, measurable inquiry flow every month — turning firm growth from referral-dependent to system-driven."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $3,200/mo — Google PPC $1,500 + LSA $1,000 + Meta retargeting $200 + Meta cold $500."))
story.append(b("<b>Aggressive:</b> $5,000/mo — Starter tier cap; ~39 leads/month at blended $128 CPL (Business Law benchmarks)."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 3 cases x $2,500 avg = $7,500/mo vs. $3,200 spend = 2.3x return. (Estimates only.)"))
story.append(b("<b>Aggressive:</b> 6 cases x $2,500 avg = $15,000/mo vs. $5,000 spend = 3.0x return. (Estimates only.)"))
story.append(Paragraph("<i>All figures use 15% default close rate and practice area default case values. Confirm actuals on call.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Business Law channel minimums: PPC $1,500 + LSA $1,000 + Meta $700 = $3,200."))
story.append(b("<b>Aggressive:</b> $900K goal x 20% / 12 = $15,000. Tier 2 (1.3x) = $19,500. Minus $4,847 fee = $14,653. Capped at $5,000 Starter limit."))
story.append(b("Total at aggressive: $12,047/mo = ~32% of $450K revenue est. Under 35% cap at $430K+ annual revenue."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I get most clients through referrals — do I really need ads?"', S["objection_q"]))
story.append(Paragraph("Referrals are not scalable and they stop when networking stops. Keystone has 131 reviews and Walia has 100 — both capturing digital leads Truman Law cannot see. Every month without digital presence is another month they extend the gap.", S["objection_a"]))

story.append(Paragraph('"Is my revenue high enough to justify this?"', S["objection_q"]))
story.append(Paragraph("At estimated $400K–$450K, the $7,047 management fee is ~19% of revenue — well within the 35% total spend cap. Conservative ad projection shows $7,500/month in new estimated revenue. Confirm exact revenue on the call to finalize the numbers.", S["objection_a"]))

story.append(Paragraph('"I am worried the ads will not work."', S["objection_q"]))
story.append(Paragraph("The conservative projection uses 15% close rate and $2,500 avg case value — among the most conservative assumptions for a seven-practice-area firm. Even at 2.3x return, 3 cases from $3,200 spend pays for itself before management fees. Ask Harkirat for his actual close rate to show the real number.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Website, Google Ads, LSA, Local SEO, Meta retargeting, monthly reporting.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$2,200/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, practice masterminds, quarterly workshops, annual in-person.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$3,200–$5,000/mo", S["price_main"])],
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
    "Total: $7,047/mo + $3,200–$5,000 ad spend  |  Save $2,147/mo by bundling  |  ~32% of est. revenue (confirm on call)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
