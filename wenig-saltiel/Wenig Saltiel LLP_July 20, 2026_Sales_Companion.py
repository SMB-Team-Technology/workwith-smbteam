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

NOTE ON THIS INSTANCE: This deal is a Legal AI Workforce (LAW)-only engagement —
no marketing package, no coaching package, no ad spend. The "Why This Marketing
Package" section below has been adapted to "Why This Legal AI Workforce Package"
and the "Why This Coaching Package" section has been adapted to "Why This
Foundation Sprint (One-Time Onboarding)". The "Why This Ad Spend" section on
page 2 has been adapted to "Why This Investment Fits" (no ad spend exists for
this deal). Structure, styles, and layout are otherwise unmodified.
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

OUTPUT_PATH = "wenig-saltiel/Wenig Saltiel LLP_July 20, 2026_Sales_Companion.pdf"


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

story.append(Paragraph("Wenig Saltiel LLP", S["title"]))
story.append(Paragraph("Sales Companion  |  July 20, 2026  |  Rep: Jacob Meissner", S["subtitle"]))
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
    [Paragraph("Jeffrey L. Saltiel (semi-retired)", S["snap_value"]),
     Paragraph("~$1.98M (HubSpot est.)", S["snap_value"]),
     Paragraph("8 attorneys", S["snap_value"]),
     Paragraph("Stage 3", S["snap_value"]),
     Paragraph("N/A", S["snap_value"]),
     Paragraph("Manhattan / Staten Island", S["snap_value"])],
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
story.append(Paragraph("Dominant Buying Motive: TIME BACK", S["section"]))
story.append(Paragraph("Jeffrey wants his own hours back from manual pre-bill review and document work — not more revenue or lower costs.", S["subsection"]))

story.append(quote_block("3-hour, bi-weekly manual review of paper pre-bills"))
story.append(Spacer(1, 1))
story.append(quote_block("~1 hour"))
story.append(Spacer(1, 1))
story.append(quote_block("not necessarily to cut costs or grow revenue"))
story.append(Spacer(1, 2))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Cut the pre-bill review.</b> Reduce his 3-hour, bi-weekly manual review of a 3-inch paper stack to about 1 hour."))
story.append(bd("<b>End manual document assembly.</b> Stop building documents by hand, file by file."))
story.append(bd("<b>Modernize ProLaw billing.</b> Bring a modern workflow to the firm's legacy billing system."))
story.append(bd("<b>Get his time back.</b> Use semi-retirement for himself, not for paperwork."))

story.append(Spacer(1, 2))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No delegation exists.</b> Jeffrey is the entire pre-bill review system himself today."))
story.append(b("<b>No automation in place.</b> Document assembly and billing both remain fully manual."))
story.append(b("<b>Legacy ProLaw system.</b> Billing runs on an older platform with nothing modern layered on top."))
story.append(b("<b>Revenue is an estimate.</b> $1.98M is HubSpot-sourced, not transcript-confirmed — verify live on the call."))

story.append(thin_rule())

# ── Why This Legal AI Workforce Package ──
story.append(Paragraph("Why This Legal AI Workforce Package", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Cuts his bi-weekly pre-bill review from about 3 hours to about 1 hour."))
story.append(bd("Removes manual document assembly from his and his staff's workload."))
story.append(bd("Brings a modern workflow to ProLaw billing without forcing a system migration."))

story.append(Paragraph("<b>Legal AI Workforce — Fractional CTO L2  |  $4,997/mo bundled</b>", S["subsection"]))
story.append(b("Revenue estimate ($1.98M) fits L2's $1.5M-$3M target band, not L1's $500K-$1.5M band."))
story.append(b("Scope spans 3 distinct workflows (pre-bill, document assembly, ProLaw integration) — matches L2's multi-workflow build cadence."))
story.append(b("Bundled price sits mid-range in the informally discussed $3,800-$7,000/mo call range."))
story.append(b("L1 ($3,297/mo) is the fallback tier if the CTO scoping call finds lower complexity than currently scoped."))

story.append(thin_rule())

# ── Why This Foundation Sprint (One-Time Onboarding) ──
story.append(Paragraph("Why This Foundation Sprint (One-Time Onboarding)", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Covers the real integration lift of exporting and mapping legacy ProLaw billing data."))
story.append(bd("Gets the first pre-bill review and document assembly workflows built and tested."))
story.append(bd("Is a one-time cost, not an ongoing add to his monthly bill."))

story.append(Paragraph("<b>Law Firm AI Foundation Sprint  |  $14,997 one-time bundled</b>", S["subsection"]))
story.append(b("Paired price with Fractional CTO L2 saves $5,000 versus the $19,997 stand-alone price."))
story.append(b("Justified by the real ProLaw data export/import lift, not a generic onboarding fee."))
story.append(b("Separate from, and in addition to, the $4,997/mo recurring Fractional CTO L2 fee."))
story.append(b("No marketing or coaching package is included — this is a single-product LAW engagement."))


# ══════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════
story.append(PageBreak())

story.append(Paragraph("Wenig Saltiel — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

# ── Why This Investment Fits ──
story.append(Paragraph("Why This Investment Fits", S["section"]))

story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Gives Jeffrey back roughly 2 hours every pre-bill cycle without asking him to grow the firm."))
story.append(bd("Keeps every dollar of spend tied to time saved, not to leads or ad platforms — there is no ad spend in this deal."))

story.append(Paragraph("<b>Investment Structure:</b>", S["subsection"]))
story.append(b("<b>Recurring:</b> $4,997/mo — Legal AI Workforce, Fractional CTO L2."))
story.append(b("<b>One-time:</b> $14,997 — Law Firm AI Foundation Sprint, paired with L2."))

story.append(Paragraph("<b>Spend Cap Check:</b>", S["subsection"]))
story.append(b("$1.98M revenue ÷ 12 = ~$165,042/mo. 35% cap = ~$57,764/mo."))
story.append(b("$4,997/mo is far under the cap — no scoping approval issue on spend."))
story.append(Paragraph("<i>Revenue figure is an estimate. Confirm on the July 20 call.</i>", S["disclaimer"]))

story.append(Paragraph("<b>Escalation — confirm before proposing:</b>", S["subsection"]))
story.append(b("Confirm LAW delivery has launched and has capacity before finalizing this proposal."))
story.append(b("Confirm actual revenue and re-check L2 vs. L1 tier on the live CTO scoping call."))

story.append(thin_rule())

# ── If He Pushes Back ──
story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"Will AI replace attorney judgment / is it safe?"', S["objection_q"]))
story.append(Paragraph("All AI-generated output goes to a draft folder for human attorney review before anything is sent — direct from the call.", S["objection_a"]))

story.append(Paragraph('"How does this integrate with our legacy ProLaw system?"', S["objection_q"]))
story.append(Paragraph("Jeffrey exports data from ProLaw, and SMB Team builds the custom integration on top of it — direct from the call.", S["objection_a"]))

story.append(Paragraph('"Is $4,997/mo justified given no stated revenue?"', S["objection_q"]))
story.append(Paragraph("The informally discussed call range was $3,800-$7,000/mo; $4,997 sits mid-range, and the $1.98M revenue estimate (via HubSpot) comfortably supports it.", S["objection_a"]))

story.append(thin_rule())

# ── Investment At A Glance ──
story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>Legal AI Workforce — Fractional CTO L2</b>", S["price_main"]),
     Paragraph("$4,997/mo", S["price_main"])],
    [Paragraph("Pre-bill review, document assembly, and ProLaw billing automation.", S["price_detail"]),
     Paragraph("<strike>$5,797</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Law Firm AI Foundation Sprint (one-time)</b>", S["price_main"]),
     Paragraph("$14,997", S["price_main"])],
    [Paragraph("ProLaw data export/import and initial workflow build.", S["price_detail"]),
     Paragraph("<strike>$19,997</strike> stand alone", S["price_detail"])],
    [Paragraph("<b>Recommended Ad Spend</b>", S["price_main"]),
     Paragraph("None — not part of this deal", S["price_main"])],
    [Paragraph("This is a LAW-only engagement; no marketing package is proposed.", S["price_detail"]),
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
    "Total: $4,997/mo + $14,997 one-time  |  Save $800/mo + $5,000 one-time by bundling  |  ~3.0% of estimated monthly revenue (under 35% cap)",
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
