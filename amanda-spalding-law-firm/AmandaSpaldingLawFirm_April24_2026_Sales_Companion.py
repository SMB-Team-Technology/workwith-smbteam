"""
Sales Companion PDF — Amanda M. Spalding Law Firm, P.S.C.
Sales Rep: Dan Bryant  |  Date: April 24, 2026
FOR INTERNAL USE ONLY. Do not share with the client.
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

OUTPUT_PATH = "amanda-spalding-law-firm/AmandaSpaldingLawFirm_April24_2026_Sales_Companion.pdf"


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

story.append(Paragraph("Amanda M. Spalding Law Firm, P.S.C.", S["title"]))
story.append(Paragraph("Sales Companion  |  April 24, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Amanda M. Spalding", S["snap_value"]),
     Paragraph("~$350K/yr", S["snap_value"]),
     Paragraph("2 (atty + paralegal)", S["snap_value"]),
     Paragraph("3 — Solo Practitioner", S["snap_value"]),
     Paragraph("15%", S["snap_value"]),
     Paragraph("Shepherdsville, KY", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: FUND THE CAMPAIGN. WIN THE JUDGESHIP.", S["section"]))
story.append(Paragraph("Maximize revenue over 6 months, fund the November judicial campaign, and close the firm with dignity and financial certainty.", S["subsection"]))

story.append(quote_block("I'm running for judge in November — I need to make sure I have enough to fund the campaign without it coming out of my own pocket."))
story.append(Spacer(1, 1))
story.append(quote_block("I want to finish strong. I don't want the last chapter of the firm to be a slow wind-down."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What she wants:</b>", S["subsection"]))
story.append(bd("<b>A fully funded campaign.</b> 6 months of strong case flow to build the war chest for November without personal savings."))
story.append(bd("<b>To finish strong.</b> Final months that reflect the firm's best — not a slow fade before the transition."))
story.append(bd("<b>Financial certainty for January.</b> Step into the judgeship knowing the transition is funded."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping her:</b>", S["subsection"]))
story.append(b("<b>No digital presence, ever.</b> Never activated LSA, paid search, or Meta — referrals alone won't hit 10–20 cases/month."))
story.append(b("<b>Website in maintenance mode.</b> Every online prospect hits a dead-end page with no form, no call button."))
story.append(b("<b>Amanda handles every intake call.</b> No delegation — firm stalls when she is in court or at a campaign event."))
story.append(b("<b>NAP inconsistency (2 phone numbers).</b> Actively suppressing local search rankings across all directories."))
story.append(b("<b>Paralegal time not billed.</b> ~$5K/month recoverable revenue left on the table every month."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Turns on predictable lead flow from Google — cases arriving from search, not just referrals."))
story.append(bd("Puts the firm in the top paid position before any competitor activates LSA — first-mover at the lowest CPL this market will ever see."))

story.append(Paragraph("<b>Essentials Full Service Marketing  |  $3,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue ~$350K/year places the firm in the Essentials tier ($250K–$400K)."))
story.append(b("No local competitor running LSA or paid search for estate planning/probate — window is open."))
story.append(b("22 Google reviews at ~4.1 stars meets LSA review threshold — no review phase required before activation."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Gives Amanda a 6-month sprint plan tied to the campaign funding target with monthly accountability."))
story.append(bd("Peer data from the mastermind for raising probate rates and implementing paralegal billing with confidence."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue under $400K qualifies for Elite Coach at the $250K–$400K non-marketing tier."))
story.append(b("Two margin leaks (no paralegal billing, $250/hr probate) — coaching delivers accountability to close both."))
story.append(b("Under $500K revenue — Fractional CFO/COO excluded by eligibility rules; Elite Coach is the correct tier."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Amanda M. Spalding Law Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for her:</b>", S["subsection"]))
story.append(bd("Generates estate planning and probate leads from Google while Amanda campaigns — cases arriving without her personal effort."))
story.append(bd("Every case that closes from a digital lead goes directly toward the November campaign fund and January cushion."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $900/mo — LSA only; minimum viable for rural KY estate planning; total all-in $6,897/mo."))
story.append(b("<b>Aggressive:</b> $1,500/mo — LSA + Google Search across Bullitt, Nelson, Spencer, and Hardin counties; total all-in $7,497/mo."))

story.append(Paragraph("<b>Estimated Return on Investment:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Est. 2–3 cases x $2,750 avg = $5,500–$8,250/mo vs. $900 spend = ~6.1x return (est.)."))
story.append(b("<b>Aggressive:</b> Est. 4–5 cases x $2,750 avg = $11,000–$13,750/mo vs. $1,500 spend = ~7.3x return (est.)."))
story.append(Paragraph("<i>Estimates based on rural KY market data and 15% close rate from the call. Case value ($2,750 avg) from transcript. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How the range was calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> Estate Planning LSA minimum $900 — LSA only. Total $5,997 management + $900 ads = $6,897/mo."))
story.append(b("<b>Aggressive:</b> $1,500 ads + $5,997 management = $7,497/mo total — 25.7% of monthly revenue."))
story.append(b("At aggressive: $7,497/mo = 25.7% of monthly revenue ($29,167). Under the 35% cap."))

story.append(thin_rule())

# ── If She Pushes Back ──
story.append(Paragraph("If She Pushes Back", S["section"]))

story.append(Paragraph('"I only have about $5,000 total to work with."', S["objection_q"]))
story.append(Paragraph("Full package is $5,997/mo management + $900–$1,500/mo ads = $6,897–$7,497/mo total. This exceeds the $5K stated budget — Dan needs to walk Amanda through the ROI case: every dollar into ads projects 5–7x return, and 6 months of results fund the campaign.", S["objection_a"]))

story.append(Paragraph('"Will clients still come to me if they know I\'m running for judge?"', S["objection_q"]))
story.append(Paragraph("Digital leads come from search intent, not community loyalty. No competitor is running paid ads in this market — the channel is wide open regardless.", S["objection_a"]))

story.append(Paragraph('"My website is a mess — I need to fix that before starting ads."', S["objection_q"]))
story.append(Paragraph("Essentials Full Service includes website restoration as a first-90-days deliverable. SMB Team handles it — the website fix and LSA enrollment happen simultaneously.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Essentials Full Service Marketing</b>", S["price_main"]),
     Paragraph("$3,397/mo", S["price_main"])],
    [Paragraph("GBP optimization, LSA, Google Ads, website restoration, directory cleanup.", S["price_detail"]),
     Paragraph("Bundled only", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Bi-weekly coaching, mastermind access, intake scripting, sprint revenue plan.", S["price_detail"]),
     Paragraph("Stand alone $3,497", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$900–$1,500/mo", S["price_main"])],
    [Paragraph("Goes to Google LSA and Google Ads — not to SMB Team.", S["price_detail"]),
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
    "Total: $5,997/mo management + $900–$1,500/mo ad spend  |  23.6%–25.7% of monthly revenue  |  Under 35% cap",
    S["savings"]))

# ── Build ──
doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

import re
with open(OUTPUT_PATH, 'rb') as f:
    content = f.read()
matches = re.findall(rb'/Count (\d+)', content)
page_count = int(matches[0]) if matches else 0
print(f"Page count: {page_count}")
if page_count != 2:
    print(f"WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
