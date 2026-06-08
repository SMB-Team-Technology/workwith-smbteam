"""
Sales Companion PDF — Lasser Law Group
Sales Rep: Randy Gold | Audit Date: June 2, 2026
FOR INTERNAL USE ONLY. DO NOT SHARE WITH CLIENT.
PACKAGE: FCOO Advisor ONLY — Coaching and Operations Proposal
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
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
RED_WARNING = HexColor("#CC0000")
RED_ACCENT = HexColor("#C0392B")

OUTPUT_PATH = "lasser-law-group/LasserLawGroup_June2_2026_Sales_Companion.pdf"


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


doc = SimpleDocTemplate(OUTPUT_PATH, pagesize=letter,
    topMargin=0.65 * inch, bottomMargin=0.42 * inch,
    leftMargin=0.6 * inch, rightMargin=0.6 * inch)

S = {}
S["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=DARK_NAVY, spaceAfter=1)
S["subtitle"] = ParagraphStyle("subtitle", fontName="Helvetica", fontSize=9, leading=12, textColor=LIGHT_GRAY, spaceAfter=2)
S["section"] = ParagraphStyle("section", fontName="Helvetica-Bold", fontSize=10.5, leading=14, textColor=ACCENT_GREEN, spaceBefore=4, spaceAfter=1)
S["subsection"] = ParagraphStyle("subsection", fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=DARK_NAVY, spaceBefore=2, spaceAfter=1)
S["bullet"] = ParagraphStyle("bullet", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=0)
S["bullet_dark"] = ParagraphStyle("bullet_dark", fontName="Helvetica", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=12, bulletIndent=0, spaceBefore=1, spaceAfter=0)
S["quote"] = ParagraphStyle("quote", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=DARK_NAVY, leftIndent=6, rightIndent=6, spaceBefore=1, spaceAfter=1)
S["snap_label"] = ParagraphStyle("snap_label", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=LIGHT_GRAY)
S["snap_value"] = ParagraphStyle("snap_value", fontName="Helvetica", fontSize=9, leading=11, textColor=DARK_NAVY)
S["objection_q"] = ParagraphStyle("objection_q", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=RED_ACCENT, spaceBefore=2, spaceAfter=0)
S["objection_a"] = ParagraphStyle("objection_a", fontName="Helvetica", fontSize=9, leading=12, textColor=MEDIUM_GRAY, leftIndent=8, spaceAfter=1)
S["price_main"] = ParagraphStyle("price_main", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=DARK_NAVY)
S["price_detail"] = ParagraphStyle("price_detail", fontName="Helvetica", fontSize=8, leading=11, textColor=MEDIUM_GRAY)
S["savings"] = ParagraphStyle("savings", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceBefore=2)
S["disclaimer"] = ParagraphStyle("disclaimer", fontName="Helvetica-Oblique", fontSize=8, leading=10, textColor=LIGHT_GRAY, spaceBefore=1, spaceAfter=0)


def b(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet"])

def bd(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", S["bullet_dark"])

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5, color=RULE_GRAY, spaceBefore=2, spaceAfter=2)

def quote_block(text):
    p = Paragraph(f'"{text}"', S["quote"])
    t = Table([[p]], colWidths=[6.5 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), QUOTE_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


# PAGE 1
story = []

story.append(Paragraph("Lasser Law Group PLLC", S["title"]))
story.append(Paragraph("Sales Companion  |  June 2, 2026  |  Rep: Randy Gold  |  FCOO Advisor Proposal", S["subtitle"]))
story.append(thin_rule())

story.append(Paragraph("Prospect Snapshot", S["section"]))
snap = [
    [Paragraph("<b>Owner</b>", S["snap_label"]), Paragraph("<b>Revenue</b>", S["snap_label"]),
     Paragraph("<b>Team</b>", S["snap_label"]), Paragraph("<b>Stage</b>", S["snap_label"]),
     Paragraph("<b>Urgency</b>", S["snap_label"]), Paragraph("<b>Location</b>", S["snap_label"])],
    [Paragraph("S. Lasser", S["snap_value"]), Paragraph("~$1M est.", S["snap_value"]),
     Paragraph("12 (9 atty)", S["snap_value"]), Paragraph("Stage 4", S["snap_value"]),
     Paragraph("7 / 10", S["snap_value"]), Paragraph("NYC, 3 offices", S["snap_value"])],
]
t1 = Table(snap, colWidths=[1.15*inch, 1.2*inch, 0.8*inch, 0.7*inch, 0.7*inch, 1.15*inch])
t1.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 1), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(t1)
story.append(Spacer(1, 2))

story.append(Paragraph("Dominant Buying Motive: SCALE AND DOMINATE", S["section"]))
story.append(Paragraph("Stephen wants Lasser Law Group to be the recognized first-call firm for real estate and commercial litigation in New York.", S["subsection"]))
story.append(quote_block("No transcript available — DBM inferred from 20+ year history, multi-office expansion, video podcast investment, and 'large law firm experience with personal service' positioning."))

story.append(Paragraph("<b>What he wants:</b>", S["subsection"]))
story.append(bd("<b>Systems-Driven Growth.</b> A firm where nine attorneys operate efficiently across three offices without the managing partner in every decision."))
story.append(bd("<b>Predictable Case Flow.</b> A reliable pipeline built on a solid operational foundation — not just referrals."))
story.append(bd("<b>Market Domination.</b> The Lasser name as the first call for any property owner, landlord, or developer who needs legal representation in New York."))

story.append(Paragraph("<b>What is stopping him:</b>", S["subsection"]))
story.append(b("<b>No Operations Layer.</b> Nine attorneys and three offices with no confirmed COO or ops staff — everything flows through the managing partner."))
story.append(b("<b>Intake Gap.</b> Contact form buried, no systematic intake process — growth marketing will under-convert without this fixed first."))
story.append(b("<b>Reputation Risk.</b> 3.6 stars / 24 reviews; recent reviews negative. Goldberg &amp; Lindenberg: 57 reviews at 4.2★."))
story.append(b("<b>Revenue Unconfirmed.</b> $1M is a third-party estimate only — qualify actual figure early in the call."))

story.append(thin_rule())

story.append(Paragraph("Why FCOO Advisor Is the Right Starting Point", S["section"]))
story.append(Paragraph("<b>What it does for him:</b>", S["subsection"]))
story.append(bd("Builds the operational infrastructure — intake systems, team accountability, management structure — so nine attorneys across three offices run consistently without Stephen as the decision-maker for every question."))
story.append(bd("Dedicated Fractional COO with law firm operations expertise, plus Elite Coach group deliverables included: weekly coaching, practice area masterminds, quarterly workshops, and annual in-person event."))
story.append(bd("Review generation system and GBP optimization as 90-day quick wins — immediate visibility improvement without any ad spend."))

story.append(Paragraph("<b>FCOO Advisor  |  $2,297/mo</b>", S["subsection"]))
story.append(b("~$1M revenue, 12-person team, 3 offices with no confirmed ops layer — operations foundation must be built before marketing investment is maximized."))
story.append(b("Fractional COO assesses all three offices within first 30 days; 90-day operational roadmap tailored to a multi-office real estate litigation practice."))
story.append(b("Stand-alone price $2,797/mo — bundled rate saves $500/mo through the SMB Team relationship."))


# PAGE 2
story.append(PageBreak())

story.append(Paragraph("Lasser Law Group — Sales Companion (continued)", S["title"]))
story.append(thin_rule())

story.append(Paragraph("What the First 90 Days Look Like", S["section"]))
story.append(Paragraph("<b>Operational actions (FCOO Advisor):</b>", S["subsection"]))
story.append(bd("FCOO Advisor kickoff: full operations assessment across all three offices — identify most urgent bottlenecks in intake, matter management, and team accountability."))
story.append(bd("Define role clarity and documented intake process — establish who owns first contact, follow-up, and conversion across Manhattan, Westchester, and Long Island."))
story.append(bd("Monthly coaching cadence and case targets established — accountability checkpoints for managing partner and team from day one."))

story.append(Paragraph("<b>Fast digital wins (no ad spend required):</b>", S["subsection"]))
story.append(b("Begin review generation process targeting satisfied clients — target: recover Google rating above 4.0 stars within 60–90 days."))
story.append(b("Optimize Google Business Profile with Super Lawyers credentials; correct FindLaw and Yelp NAP inconsistencies."))

story.append(thin_rule())

story.append(Paragraph("If He Pushes Back", S["section"]))

story.append(Paragraph('"I\'m not sure I need an operations person — I need more clients."', S["objection_q"]))
story.append(Paragraph("Marketing without operations is like turning up the water pressure before fixing the leaky pipes. Nine attorneys, three offices, no documented intake process — every new lead that comes in without a system hits a bottleneck. Fix the operations first; then every marketing dollar converts at a higher rate.", S["objection_a"]))

story.append(Paragraph('"We get enough work from referrals."', S["objection_q"]))
story.append(Paragraph("Referrals have a ceiling. Goldberg & Lindenberg has 57 Google reviews at 4.2 stars and appears in every Manhattan landlord-tenant search. Belkin Burden Goldman has 60 attorneys and is Chambers-ranked. That gap grows every month without action. The operational foundation you build today is what makes marketing investment pay off tomorrow.", S["objection_a"]))

story.append(Paragraph('"Is $2,297/mo worth it for coaching?"', S["objection_q"]))
story.append(Paragraph("This is not coaching in the abstract — it is a dedicated Fractional COO with law firm operations expertise assessing all three offices and building the management structure that makes every attorney hour more productive. One additional case per month from improved intake conversion more than covers the investment.", S["objection_a"]))

story.append(Paragraph('"We\'re busy managing three offices already."', S["objection_q"]))
story.append(Paragraph("Urgency score: 7/10. Competitors are dominating multiple channels in this market right now. The three-office structure you are managing manually today is the exact problem FCOO Advisor solves — so the managing partner can lead the firm rather than run it.", S["objection_a"]))

story.append(thin_rule())

story.append(Paragraph("Investment At A Glance", S["section"]))

price_data = [
    [Paragraph("<b>FCOO Advisor</b>", S["price_main"]), Paragraph("$2,297/mo", S["price_main"])],
    [Paragraph("Fractional COO, operations assessment, intake systems, team accountability, coaching sessions, masterminds, workshops.", S["price_detail"]), Paragraph("<strike>$2,797</strike> stand alone", S["price_detail"])],
]
pt = Table(price_data, colWidths=[4.5 * inch, 1.7 * inch])
pt.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 4), ("RIGHTPADDING", (0,0), (-1,-1), 4),
    ("TOPPADDING", (0,0), (-1,-1), 2), ("BOTTOMPADDING", (0,0), (-1,-1), 1),
    ("LINEBELOW", (0,1), (-1,1), 0.5, RULE_GRAY),
]))
story.append(pt)
story.append(Paragraph(
    "Total: $2,297/mo  |  Save $500/mo  |  0.23% of estimated revenue (well under the 35% cap)",
    S["savings"]))

doc.build(story, onFirstPage=add_page_elements, onLaterPages=add_page_elements)
print(f"PDF created: {OUTPUT_PATH}")

from pypdf import PdfReader
r = PdfReader(OUTPUT_PATH)
page_count = len(r.pages)
print(f"Page count: {page_count}")
if page_count != 2:
    print("WARNING: Sales Companion must be exactly 2 pages. Shorten bullet text to fit.")
