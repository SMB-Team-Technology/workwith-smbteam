"""
Sales Companion PDF Template — SMB Team
========================================
This template generates the 2-page internal Sales Companion PDF for the sales rep.
It uses reportlab. Do not modify the layout, colors, fonts, styles, or structure.
Only replace the # FILL: placeholders with audit-specific content.

IMPORTANT: The final PDF must be exactly 2 pages. If content overflows to a third
page, shorten bullet text — do not remove sections.

All bullet text must be scannable: one idea per bullet, 8th-grade reading level.
Each "What it does for her/him:" bullet states the transformation, not the deliverable.
Each scoping rationale bullet states one fact with one conclusion.

Output filename: [FirmName]_[Date]_Sales_Companion.pdf
  - FirmName: spaces replaced with underscores
  - Date: MMDDYYYY format
  - Save to the root of the project folder (same location as the Growth Audit HTML)
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

OUTPUT_PATH = "the-ladd-firm/The Ladd Firm, LLC_July 27, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("The Ladd Firm, LLC", S["title"]))
story.append(Paragraph("Sales Companion  |  July 27, 2026  |  Rep: Dan Bryant", S["subtitle"]))
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
    [Paragraph("Banks Ladd", S["snap_value"]),
     Paragraph("~$800K pace (~$600K prior yr)", S["snap_value"]),
     Paragraph("4 + contractor", S["snap_value"]),
     Paragraph("Stage 4", S["snap_value"]),
     Paragraph("15% (default)", S["snap_value"]),
     Paragraph("Mobile, AL (1 loc.)", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: TIME FREEDOM", S["section"]))
story.append(Paragraph("Banks wants the firm to grow without it consuming more of his personal time — he still needs roughly five hours a day for production work and worries about being overloaded by new initiatives.", S["subsection"]))

story.append(quote_block("~10% ad cost to revenue last month, approx $60K revenue on $6K spend"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>A Fractional CTO, not a DIY project.</b> Someone else leading AI rollout — he lacks bandwidth to run it himself."))
story.append(bd("<b>Real delegation.</b> Coaching that makes intake follow-up and team accountability stick."))
story.append(bd("<b>No overlap with Colin.</b> No marketing pitch that steps on his current contractor's scope."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No bandwidth for AI himself.</b> Trialing AI Workforce Pro but needs a CTO leading it."))
story.append(b("<b>No defined intake process.</b> Meetings capped near 5/week despite active ad spend."))
story.append(b("<b>Below-market case value.</b> $4,000 average vs. ~$5,000 locally."))

story.append(thin_rule())

# ── Why This AI Enablement Package ──
story.append(Paragraph("Why This AI Enablement Package (Not Marketing)", S["section"]))

story.append(Paragraph("<b>IMPORTANT — read before the call:</b>", S["subsection"]))
story.append(b("This call was about AI enablement and coaching, not marketing — Banks reserved that for a later call to avoid overlapping with Colin."))
story.append(b("Per SMB Team's override rules, Full Service Marketing is excluded entirely this cycle. Do not lead with a marketing pitch."))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Puts a dedicated Fractional CTO in charge of the AI rollout Banks already started trialing."))
story.append(bd("Turns MyCase and repeatable intake/follow-up tasks into automations that run without his time."))

story.append(Paragraph("<b>Legal AI Workforce — Fractional CTO L1  |  $3,297/mo bundled</b>", S["subsection"]))
story.append(b("Revenue (~$800K) is in the $500K-$1.5M target band for AI Accelerator L1."))
story.append(b("Banks wants a Fractional CTO leading automation — L1 fits better than AI Essentials' DIY model."))
story.append(b("Foundation Sprint paired with L1 is $14,997 one-time (vs. $19,997 standalone) — a separate, one-time cost."))

story.append(thin_rule())

# ── Why This Coaching Package ──
story.append(Paragraph("Why This Coaching Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Banks a structured way to delegate intake and follow-up instead of personally overseeing it."))
story.append(bd("Builds team accountability around Summer, Leo, and the growing attorney bench."))
story.append(bd("Turns a rough ad-cost-to-revenue ratio into an actual profit plan."))

story.append(Paragraph("<b>Elite Coach Plus  |  $3,200/mo bundled</b>", S["subsection"]))
story.append(b("Revenue in the $400K-$1M band places Elite Coach Plus as the standard non-marketing recommendation."))
story.append(b("Note: transcript references \"Elite Coach\" by name — confirm Elite Coach Plus (correct tier for this band) is what's proposed."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("The Ladd Firm — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why No New Ad Spend This Cycle ──
story.append(Paragraph("Why No New Ad Spend This Cycle", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Keeps this proposal focused on what Banks actually asked about, building trust instead of overreaching."))
story.append(bd("Leaves the door open for a separate, dedicated marketing conversation once the AI and coaching foundation is underway."))

story.append(Paragraph("<b>Existing ad spend (for context only — not part of this proposal):</b>", S["subsection"]))
story.append(b("The firm's ~$6,000/mo Google PPC + LSA spend continues via Colin Bulger, outside SMB Team's scope this cycle."))
story.append(b("Per the transcript, that spend generated ~$60,000 in revenue last month — roughly a 10x return the firm is already seeing on its own."))
story.append(b("Do not present a Conservative/Aggressive SMB ad-spend table on this call — it would misrepresent what's being proposed."))

story.append(Paragraph("<b>35% cap check (for scoping, not client-facing):</b>", S["subsection"]))
story.append(b("New monthly commitment: $3,297 (LAW) + $3,200 (Coaching) = $6,497/mo = 9.7% of $66,667/mo revenue — well under the 35% cap."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"What happened to the marketing proposal we talked about before?"', S["objection_q"]))
story.append(Paragraph("That conversation is still on the table — Banks asked to keep it separate from today's AI and coaching discussion so it doesn't step on Colin's current scope. We'll revisit it on its own once this foundation is running.", S["objection_a"]))

story.append(Paragraph('"Can I really manage AI adoption without more of my own time?"', S["objection_q"]))
story.append(Paragraph("That's exactly what the Fractional CTO role is for — Level 1 puts someone else driving the rollout, with the Foundation Sprint handling initial setup so it isn't Banks's project to run.", S["objection_a"]))

story.append(Paragraph('"I want to sleep on it before signing anything."', S["objection_q"]))
story.append(Paragraph("Reasonable — the numbers here are estimates Banks can verify against his own ad account and GBP data before committing. Nothing about this recommendation requires a same-day decision.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Legal AI Workforce — Fractional CTO L1</b>", S["price_main"]),
     Paragraph("$3,297/mo", S["price_main"])],
    [Paragraph("Dedicated CTO, Claude Enterprise workspace, AI Skills, MyCase workflows.", S["price_detail"]),
     Paragraph("<strike>$3,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Elite Coach Plus</b>", S["price_main"]),
     Paragraph("$3,200/mo", S["price_main"])],
    [Paragraph("Delegation coaching, intake build-out, team accountability.", S["price_detail"]),
     Paragraph("<strike>$3,497</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Foundation Sprint (one-time, paired w/ L1)</b>", S["price_main"]),
     Paragraph("$14,997", S["price_main"])],
    [Paragraph("Onboarding only — not a recurring monthly cost.", S["price_detail"]),
     Paragraph("<strike>$19,997</strike> stand alone", S["price_detail"])],
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
    "Total: $6,497/mo + $14,997 one-time onboarding  |  Save $797/mo + $5,000 one-time by bundling  |  9.7% of revenue (well under 35% cap)",
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
