"""
Sales Companion PDF — Law Office of Steven Ellman
SMB Team | June 2, 2026 | Rep: Nick Holderman
Internal use only. Do not share with prospect.
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

OUTPUT_PATH = "law-office-of-steven-ellman/Law_Office_of_Steven_Ellman_06022026_Sales_Companion.pdf"


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

story.append(Paragraph("Law Office of Steven Ellman", S["title"]))
story.append(Paragraph("Sales Companion  |  June 2, 2026  |  Rep: Nick Holderman", S["subtitle"]))
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
    [Paragraph("Steven Ellman", S["snap_value"]),
     Paragraph("~$300K–$400K est. (unconfirmed)", S["snap_value"]),
     Paragraph("1 atty + 3 staff", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Medford &amp; Moorestown, NJ", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: PREDICTABLE CASE FLOW / FREEDOM TO PRACTICE", S["section"]))
story.append(Paragraph("Steven wants a machine that feeds cases predictably so he can focus on defending clients — not on marketing or business development.", S["subsection"]))

story.append(quote_block("No transcript — DBM inferred from 39-year solo DUI practice; attorney skilled at law but lacks a systematic lead generation engine."))
story.append(Spacer(1, 1))
story.append(quote_block("Confirm DBM, revenue, team size, and close rate on June 5, 2026 discovery call before finalizing proposal."))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Predictable case flow.</b> Cases that arrive without chasing — marketing works while he is in court."))
story.append(bd("<b>Freedom to practice law.</b> Time on client defense, not on marketing and operations."))
story.append(bd("<b>Financial visibility.</b> Knowing what he takes home — not discovering profit at year-end."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No paid lead generation.</b> Zero Google Ads, LSA, or Meta presence — entirely referral-dependent."))
story.append(b("<b>NAP inconsistency.</b> Address conflicts (715 vs. 617 Stokes Rd) suppress local pack rankings."))
story.append(b("<b>No intake process.</b> After-hours coverage and follow-up sequences not confirmed — DUI leads arrive at night."))
story.append(b("<b>Owner-dependency.</b> Solo attorney: the firm stops when he stops."))

story.append(thin_rule())

# ── Why This Marketing Package ──
story.append(Paragraph("Why This Marketing Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("<b>Cases come in while he is in court.</b> Google Ads and LSA generate leads without attorney involvement."))
story.append(bd("<b>Closes the paid channel gap.</b> Firm becomes visible where Baxter, Levow, and SRIS currently operate unopposed."))

story.append(Paragraph("<b>Full Service Marketing Essentials  |  $3,397/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $300K–$400K → Essentials tier ($250K–$400K band). DUI/DWI — Essentials not blocked."))
story.append(b("Website modern and mobile responsive — no forced rebuild. Essentials ad cap $7,500; both spend levels within cap."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("<b>Converts leads into cases.</b> Intake coaching maximizes conversion from every paid lead that comes in."))
story.append(bd("<b>Accountability structure.</b> Weekly coaching keeps growth on plan — results happen on purpose, not by chance."))

story.append(Paragraph("<b>Elite Coach  |  $2,600/mo bundled</b>", S["subsection"]))
story.append(b("Revenue $300K–$400K → Elite Coach is the recommended tier. Fractional COO/CFO not eligible under $500K."))
story.append(b("Intake gaps confirmed in research — after-hours protocol and follow-up sequence are day-one coaching priorities."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Law Office of Steven Ellman — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Ad Spend ──
story.append(Paragraph("Why This Ad Spend", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("<b>Creates the pipeline he has never had.</b> Paid leads arrive on schedule — not when referrals happen to come in."))
story.append(bd("<b>Closes the gap on Baxter and Levow.</b> Puts this firm in front of the same high-intent DUI prospects they capture now."))

story.append(Paragraph("<b>Recommended Ad Spend Range:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $4,000/mo — Google Ads intro level; within 35% cap at $350K est. revenue."))
story.append(b("<b>Aggressive:</b> $5,500/mo — criminal defense PPC minimum; requires revenue confirmed at $400K."))

story.append(Paragraph("<b>Estimated ROI:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> ~3 cases x $4,500 = ~$13,500/mo vs. $4,000 = ~3.4x return. (Est.)"))
story.append(b("<b>Aggressive:</b> ~5 cases x $4,500 = ~$22,500/mo vs. $5,500 = ~4.1x return. (Est.)"))
story.append(Paragraph("<i>Estimates. NJ DUI defaults: $4,000–$5,000 case value; 15% close rate. Not guaranteed.</i>", S["disclaimer"]))

story.append(Paragraph("<b>How calculated:</b>", S["subsection"]))
story.append(b("<b>Conservative:</b> $4,000 / ($180 CPL + 20% cushion = $216) = 18 leads x 15% = 3 cases."))
story.append(b("<b>Aggressive:</b> $5,500 / $180 CPL = 31 leads x 15% = 5 cases. Total $11,497 vs. $11,667 cap. ✓"))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I\'ve built this for 39 years without paid ads."', S["objection_q"]))
story.append(Paragraph("Baxter (144 reviews, former prosecutor) and Levow DWI Law (15 consecutive Best Law Firms) are running paid Burlington County campaigns now. Every month without ads, they convert prospects actively searching for you.", S["objection_a"]))

story.append(Paragraph('"I don\'t know my actual revenue."', S["objection_q"]))
story.append(Paragraph("Elite Coach kickoff establishes the baseline metrics Steven needs. The proposal uses conservative defaults ($300K–$400K) that work at the lower end of the range.", S["objection_a"]))

story.append(Paragraph('"Will Avvo hurt the ads?"', S["objection_q"]))
story.append(Paragraph("Google Ads and LSA are independent of Avvo. The 120 Google reviews at 4.9 stars are what Google uses — that profile is strong. Avvo management is a separate long-term item that does not block ads from launching.", S["objection_a"]))

story.append(Paragraph('"What if I can\'t handle more cases?"', S["objection_q"]))
story.append(Paragraph("Elite Coach addresses intake triage directly. Phase 2 builds the intake coordinator and operations layer that scales capacity alongside case volume.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Full Service Marketing Essentials</b>", S["price_main"]),
     Paragraph("$3,397/mo", S["price_main"])],
    [Paragraph("Google Ads, LSA, local SEO, website optimization, monthly reporting.", S["price_detail"]),
     Paragraph("Stand-alone N/A", S["price_detail"])],
    [Paragraph("<b>Elite Coach</b>", S["price_main"]),
     Paragraph("$2,600/mo", S["price_main"])],
    [Paragraph("Weekly group coaching, practice area masterminds, intake process guidance, quarterly and annual workshops.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("$4,000–$5,500/mo", S["price_main"])],
    [Paragraph("Goes to Google and LSA platforms — not to SMB Team.", S["price_detail"]),
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
    "Total: $5,997/mo + $4,000–$5,500 ad spend  |  Save $897/mo by bundling  |  34.4%–34.8% of revenue (under 35% cap at $400K est.)",
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
