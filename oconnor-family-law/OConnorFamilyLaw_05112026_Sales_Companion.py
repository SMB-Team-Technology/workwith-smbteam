"""
Sales Companion PDF — O'Connor Family Law
Sales Rep: Dan Bryant | Date: May 11, 2026
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

OUTPUT_PATH = "/home/user/workwith-smbteam/oconnor-family-law/OConnorFamilyLaw_05112026_Sales_Companion.pdf"

def add_page_elements(canvas, doc):
    canvas.saveState()
    width, height = letter
    canvas.setFont("Helvetica-Bold", 10)
    canvas.setFillColor(RED_WARNING)
    canvas.drawCentredString(width / 2, height - 0.38 * inch, "FOR INTERNAL USE ONLY; DO NOT SHARE.")
    canvas.setStrokeColor(RED_WARNING)
    canvas.setLineWidth(0.5)
    canvas.line(0.6 * inch, height - 0.44 * inch, width - 0.6 * inch, height - 0.44 * inch)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.drawCentredString(width / 2, 0.28 * inch, "SMB Team  |  Confidential  |  Internal Document")
    canvas.restoreState()

doc = SimpleDocTemplate(OUTPUT_PATH, pagesize=letter, topMargin=0.72*inch, bottomMargin=0.42*inch, leftMargin=0.6*inch, rightMargin=0.6*inch)

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

def b(text): return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])
def bd(text): return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])
def thin_rule(): return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY, spaceBefore=3, spaceAfter=3)
def quote_block(text):
    p = Paragraph(f'"{text}"', S["quote"])
    t = Table([[p]], colWidths=[6.5 * inch])
    t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), QUOTE_BG), ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8), ("TOPPADDING", (0,0), (-1,-1), 3), ("BOTTOMPADDING", (0,0), (-1,-1), 3)]))
    return t

story = []
story.append(Paragraph("O'Connor Family Law", S["title"]))
story.append(Paragraph("Sales Companion  |  May 11, 2026  |  Rep: Dan Bryant", S["subtitle"]))
story.append(thin_rule())
story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [[Paragraph("<b>Owner</b>", S["snap_label"]), Paragraph("<b>Revenue</b>", S["snap_label"]), Paragraph("<b>Team</b>", S["snap_label"]), Paragraph("<b>Stage</b>", S["snap_label"]), Paragraph("<b>Close Rate</b>", S["snap_label"]), Paragraph("<b>Location</b>", S["snap_label"])], [Paragraph("Heather O'Connor", S["snap_value"]), Paragraph("$4M+ (2025)", S["snap_value"]), Paragraph("25 / 13 atty", S["snap_value"]), Paragraph("Stage 5", S["snap_value"]), Paragraph("9% lead-to-signed", S["snap_value"]), Paragraph("Westborough &amp; Hanover, MA", S["snap_value"])]]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.7*inch, 1.15*inch])
t1.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1), ("LEFTPADDING", (0,0), (-1,-1), 0), ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY)]))
story.append(t1)
story.append(Spacer(1, 4))
story.append(Paragraph("Dominant Buying Motive: FREEDOM", S["section"]))
story.append(Paragraph("Heather wants a firm that runs without her — income not tied to her hours, Caitlyn leading forward, and the freedom she built this firm to create.", S["subsection"]))
story.append(quote_block("We provide signed, won, lost, and qualification data every month. We feel like they're not acting on it — no exclusions, no keyword pruning, nothing."))
story.append(Spacer(1, 1))
story.append(quote_block("2025 revenue just over $4 million. 2026 target is $5 to $7 million."))
story.append(Spacer(1, 2))
story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>Clean attribution.</b> She wants to know which dollars produce which signed cases — not raw call counts."))
story.append(bd("<b>Caitlyn's time back.</b> Her Director of Operations should lead growth, not audit reports the agency isn't acting on."))
story.append(bd("<b>A clear path to $7M.</b> She has the infrastructure — she needs the marketing system to match it."))
story.append(Spacer(1, 2))
story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No attribution.</b> $17-20k/month in ad spend with no signed-case reporting — she cannot tell what is working."))
story.append(b("<b>Wrong agency.</b> Empirical 360 has had 8-10 months of signed-case feedback and has not adjusted a single keyword or exclusion."))
story.append(b("<b>GBP and keyword errors.</b> Wrong primary category, wrong homepage framing, LSA-heavy budget that cannot filter junk by design."))
story.append(b("<b>No fractional CFO.</b> Growing to $7M without margin planning risks adding revenue without adding owner take-home."))
story.append(thin_rule())
story.append(Paragraph("Why This Marketing Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Replaces raw call count reporting with signed-case attribution — Caitlyn stops auditing reports and starts leading."))
story.append(bd("Rebalances PPC vs. LSA with income demographic layering and negative keywords — junk volume drops at the source."))
story.append(Paragraph("<b>Platinum Full-Service Marketing  |  $15,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue over $3M triggers Platinum tier — O'Connor at $4M+ qualifies; no lower tier applies."))
story.append(b("Two distinct markets (MetroWest + South Shore) require separate campaign structures and GBP strategies."))
story.append(b("$10k/month LSA with ~50% spam rate requires full restructure and systematic dispute process to recover credit."))
story.append(thin_rule())
story.append(Paragraph("Why This Coaching Package", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives Caitlyn an external FCOO partner to build the systems needed to reach $7M without expanding her hours."))
story.append(bd("Connects Heather to a Master's Circle cohort of owners at her revenue stage who have solved the $4M-to-$7M problem."))
story.append(Paragraph("<b>Master's Circle + FCOO Partner  |  $12,394/mo</b>", S["subsection"]))
story.append(b("25 employees + dedicated Director of Operations at $3M+ revenue triggers this tier."))
story.append(b("Caitlyn is carrying an agency management burden that belongs to the marketing partner — FCOO Partner resets this."))
story.append(b("No fractional CFO in current stack — growing to $7M without margin planning is the firm's central profit risk."))
story.append(PageBreak())
story.append(Paragraph("O'Connor Family Law — Sales Companion (continued)", S["title"]))
story.append(thin_rule())
story.append(Paragraph("Why This Ad Spend", S["section"]))
story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Every dollar of ad spend becomes attributable to a signed case — the guesswork about which channel is working ends permanently."))
story.append(bd("The intake engine already built for 40-50 new clients/month finally gets the clean, qualified pipeline it needs to operate at capacity."))
story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $15,000/mo — current spend level, rebalanced: LSA $7,500 + PPC $5,000 + Meta $2,500."))
story.append(b("<b>Aggressive:</b> $25,000/mo — full budget to accelerate to $5-7M with income demographic targeting in both markets."))
story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> 10-12 cases x $15,000 avg = $150,000-$180,000/mo vs. $15,000 spend = 10x-12x estimated return."))
story.append(b("<b>Aggressive:</b> 16-20 cases x $15,000 avg = $240,000-$300,000/mo vs. $25,000 spend = 9.6x-12x estimated return."))
story.append(Paragraph("<i>All figures are estimates based on industry averages. Not guaranteed.</i>", S["disclaimer"]))
story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Family law channel minimums: LSA $7,500 + PPC $5,000 + Meta $2,500 = $15,000/mo."))
story.append(b("<b>Aggressive:</b> $5M growth target x 20% / 12 = $83,333 theoretical max; capped at Platinum tier limit of $25,000/mo."))
story.append(b("Total spend at aggressive: $25,000/mo = ~6.25% of current $4M revenue. Well under the 35% cap."))
story.append(thin_rule())
story.append(Paragraph("If She Pushes Back", S["section"]))
story.append(Paragraph('"We had SMB Team before and left over slow web updates."', S["objection_q"]))
story.append(Paragraph("We take that history seriously — and the production workflow has changed. Web updates now carry a 48-hour SLA with dedicated production support. More importantly, what you need now is not faster updates; it is a marketing partner who optimizes to signed cases, which is exactly what Platinum delivers.", S["objection_a"]))
story.append(Paragraph('"We give them all this data and they just don\'t act on it."', S["objection_q"]))
story.append(Paragraph("That is the central problem. Empirical 360 has had 8-10 months of signed/won/lost feedback and has not adjusted a keyword or exclusion. SMB Team’s Platinum reporting is built specifically so that every optimization decision ties back to signed-case outcomes — not click volume.", S["objection_a"]))
story.append(Paragraph('"Half our LSA leads are spam. We\'re wasting money."', S["objection_q"]))
story.append(Paragraph("LSA cannot exclude 'cheap' or 'free' divorce intent by design — that is a platform limitation. The fix is to rebalance toward PPC where we layer household income top 30%, exclude junk terms, and dispute every unqualified LSA lead for credit. The current agency has not been doing any of this.", S["objection_a"]))
story.append(thin_rule())
story.append(Paragraph("Investment At A Glance", S["section"]))
price_data = [[Paragraph("<b>Platinum Full-Service Marketing</b>", S["price_main"]), Paragraph("$15,997/mo", S["price_main"])], [Paragraph("Website, SEO, PPC + LSA + Meta + GBP + signed-case attribution.", S["price_detail"]), Paragraph("<strike>$18,997</strike> stand alone", S["price_detail"])], [Paragraph("<b>Master's Circle + FCOO Partner</b>", S["price_main"]), Paragraph("$12,394/mo", S["price_main"])], [Paragraph("Elite Coach + High Level Mastermind + Team Training + FCOO Services.", S["price_detail"]), Paragraph("", S["price_detail"])], [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]), Paragraph("$15,000–$25,000/mo", S["price_main"])], [Paragraph("Goes to Google, LSA, and Meta — not to SMB Team.", S["price_detail"]), Paragraph("", S["price_detail"])]]
pt = Table(price_data, colWidths=[4.5*inch, 1.7*inch])
pt.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 4), ("RIGHTPADDING", (0,0), (-1,-1), 4), ("TOPPADDING", (0,0), (-1,-1), 2), ("BOTTOMPADDING", (0,0), (-1,-1), 1), ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY), ("LINEBELOW", (0,3), (-1,3), 0.5, RULE_GRAY), ("LINEBELOW", (0,5), (-1,5), 0.5, RULE_GRAY)]))
story.append(pt)
story.append(Paragraph("Total: $28,391/mo + $15,000–$25,000 ad spend  |  Save $3,000/mo by bundling Platinum  |  Ad spend = 6–10% of current revenue (under 35% cap)", S["savings"]))
doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")
