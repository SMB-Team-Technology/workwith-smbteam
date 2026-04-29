"""
Sales Companion PDF — The Kaiser Law Group
SMB Team Internal Document — DO NOT SHARE WITH CLIENT
Sales Rep: Dan Bryant | April 28, 2026
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

OUTPUT_PATH = "kaiser-law-group/TheKaiserLawGroup_04282026_Sales_Companion.pdf"


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
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=ACCENT_GREEN, spaceBefore=5, spaceAfter=2)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=1)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9, leading=11, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=1)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8.5, leading=12, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=3)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=1)


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


# PAGE 1
story = []

story.append(Paragraph("The Kaiser Law Group", S["title"]))
story.append(Paragraph("Sales Companion  |  April 28, 2026  |  Rep: Dan Bryant", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]),
     Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]),
     Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Close Rate</b>", S["snap_label"]),
     Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("Dan Kaiser", S["snap_value"]),
     Paragraph("$600K–$1.2M", S["snap_value"]),
     Paragraph("4 (+1 atty fall)", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% default", S["snap_value"]),
     Paragraph("Flagstaff, AZ", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.85*inch, 0.7*inch, 0.75*inch, 1.05*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 3))

story.append(Paragraph("Dominant Buying Motive: LEGACY + FREEDOM", S["section"]))
story.append(Paragraph("Work 20 hrs/week, mentor his daughter at the firm, build a business that earns without him.", S["subsection"]))

story.append(quote_block("In about 3 years: 3 attorneys total, about 4 support staff, Dan at about 20 hours a week."))
story.append(Spacer(1, 1))
story.append(quote_block("Need 5 incremental criminal cases per month — DUI, drugs, DV — at about $5K average to cover daughter's comp."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Case flow by September.</b> Daughter joins fall 2026; needs $25K/mo incremental to fund hire without personal savings."))
story.append(bd("<b>The firm answers when he doesn't.</b> Currently fields after-hours calls personally; wants a system that covers 24/7."))
story.append(bd("<b>Predictable revenue.</b> 2024 was a net loss; revenue swings $600K wide; wants to know what he earns before year-end."))

story.append(Spacer(1, 1))
story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No paid ads.</b> LSAs were stopped; poor targeting burned his confidence; no PPC or LSA running today."))
story.append(b("<b>Review gap.</b> ~27 reviews vs. Griffen &amp; Stevens at 294 — suppresses Map Pack for every DUI and drug crime search."))
story.append(b("<b>Intake is Dan-dependent.</b> No after-hours coverage, no script, no financing option — qualified leads walk to whoever answers first."))

story.append(thin_rule())

story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Delivers the 5 criminal defense cases per month Dan needs before September — targeted by case type, filtered by intent."))
story.append(bd("Rebuilds confidence in paid channels with the exact fix he asked for: segmentation, negative keywords, dayparting."))

story.append(Paragraph("<b>Full Service Marketing — Starter  |  $4,847/mo bundled</b>", S["subsection"]))
story.append(b("Criminal Defense + High Competitiveness rules out Essentials; Starter correct at $600K–$1.2M revenue."))
story.append(b("Google PPC and LSA first; Meta retargeting via Dan's FAQ video content added once live."))
story.append(b("Stand-alone $5,697/mo; bundled saves $850/month. Growth tier path at $1M+ documented in roadmap."))

story.append(thin_rule())

story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds intake system and daughter's onboarding framework before September — she joins with a process, not just a mentor."))
story.append(bd("Monthly financial reporting gives Dan the visibility to commit to her salary with data, not hope."))

story.append(Paragraph("<b>Elite Coach Plus  |  $2,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $400K–$1M, growing team — Elite Coach Plus is the correct tier."))
story.append(b("FCOO Advisor available Phase 2 once revenue crosses $900K and daughter is fully integrated."))
story.append(b("Stand-alone $3,497/mo; bundled saves $1,297/month. Combined bundle savings: $2,147/month."))


# PAGE 2
story.append(PageBreak())

story.append(Paragraph("The Kaiser Law Group — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Conservative ($4,500/mo): 3–5 cases/month approaches the 5-case target without personal savings."))
story.append(bd("Aggressive ($6,500/mo): 7–9 cases/month exceeds the target, funds a support hire, accelerates path to $1M."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $4,500/mo — Google PPC $2,500 + LSA $2,000. Criminal defense only."))
story.append(b("<b>Aggressive:</b> $6,500/mo — Google PPC + LSA + Meta retargeting + PI targeting."))

story.append(Paragraph("<b>Estimated ROI (estimates only — not guaranteed):</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~28 leads x 15% = 4 cases x $5K = ~$20K/mo vs. $4,500 spend = ~4x."))
story.append(b("<b>Aggressive:</b> ~55 leads x 15% = 8 cases x $5K = ~$40K/mo vs. $6,500 spend = ~6x."))
story.append(Paragraph("<i>Avg case value $5,000 per Dan Kaiser. Close rate 15% (default). All projections are estimates.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Criminal Defense channel minimums: PPC $2,500 + LSA $2,000. Note: slightly above $4,000 Starter cap; discuss Growth tier or 10% overage at May 13."))
story.append(b("<b>Aggressive:</b> $3M goal x 20% ÷ 12 x 0.85 (Tier 5) = $42,500. Capped at $6,500 for current revenue stage."))
story.append(b("Total aggressive: $7,047 fees + $6,500 ads = $13,547/mo = ~17% of $800K planning revenue. Under 35% cap."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"LSAs burned me before — expensive with no quality cases."', S["objection_q"]))
story.append(Paragraph("The previous LSAs had no case-type filtering or negative keywords — paying $137+/call for unqualified leads is the expected outcome without segmentation. This is DUI-only and drug-only targeting with 'free lawyer' and 'public defender' exclusions. Flagstaff Tier 5 means lower CPLs than his metro experience.", S["objection_a"]))

story.append(Paragraph('"Many leads can\'t afford counsel."', S["objection_q"]))
story.append(Paragraph("Income-signal targeting and negative keywords filter low-budget queries at the front end. For qualified but cash-constrained prospects, third-party financing (LawPay, CallPay) converts the case without collection risk — Dan identified this gap himself on the call.", S["objection_a"]))

story.append(Paragraph('"AI is taking over search — will this even work?"', S["objection_q"]))
story.append(Paragraph("LSAs appear above AI Overviews — they hold the top position. FAQ schema content makes the firm AI-visible in summaries. Firms with 50+ reviews and schema markup are cited in AI Overviews; priority now is review velocity to cross that threshold.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing — Starter</b>", S["price_main"]),
     Paragraph("$4,847/mo", S["price_main"])],
    [Paragraph("Google PPC + LSA + Meta + SEO alignment + GBP optimization.", S["price_detail"]),
     Paragraph("<strike>$5,697</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$2,200/mo", S["price_main"])],
    [Paragraph("Weekly coaching, intake system, onboarding framework, financial reporting.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$4,500–$6,500/mo", S["price_main"])],
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
    "Total: $7,047/mo (fees) + $4,500–$6,500/mo ad spend  |  Save $2,147/mo by bundling  |  ~14–17% of revenue (under 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

import re
with open(OUTPUT_PATH, 'rb') as f:
    content = f.read().decode('latin-1')
pages = len(re.findall(r'/Type\s*/Page\b', content))
print(f"Page count: {pages}")
if pages != 2:
    print("WARNING: Must be exactly 2 pages. Shorten bullet text.")
