"""Branded PDF invoice for canteen orders, drawn with ReportLab.

Layout adapts to the order: column widths are fractions of the page width,
long dish names and descriptions wrap inside their cell, and long orders
flow onto further pages with the table header repeated and "Page x of y"
in the footer.
"""
import os
from datetime import datetime
from decimal import Decimal, InvalidOperation
from xml.sax.saxutils import escape

from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate, Frame, KeepTogether, PageTemplate, Paragraph, Spacer, Table, TableStyle,
)

# Site palette (see static/css/site.css)
NAVY_900 = colors.HexColor("#0b1f3a")
NAVY_800 = colors.HexColor("#122f53")
NAVY_200 = colors.HexColor("#b3c7e4")
NAVY_50 = colors.HexColor("#eef3fa")
GOLD_500 = colors.HexColor("#c9a227")
GOLD_400 = colors.HexColor("#d9b84a")
GOLD_50 = colors.HexColor("#fbf7e9")
SLATE_500 = colors.HexColor("#64748b")
SLATE_200 = colors.HexColor("#e2e8f0")

BRAND = "Modern Canteen"
COLLEGE = "Modern College of Arts, Science & Commerce"
ADDRESS = "Shivajinagar, Pune – 411005"
PHONE = "9858358823 / 9730133445"
LOGO_PATH = os.path.join(settings.BASE_DIR, "canteenapp", "static", "canteenapp", "images", "moderncollege.jpg")

MARGIN = 16 * mm
FIRST_BAND = 40 * mm   # header band height on page 1
LATER_BAND = 15 * mm   # slimmer band on continuation pages
FOOTER = 16 * mm


def _style(name, **kw):
    base = dict(fontName="Helvetica", fontSize=9, leading=12, textColor=NAVY_900)
    base.update(kw)
    return ParagraphStyle(name, **base)


LABEL = _style("label", fontName="Helvetica-Bold", fontSize=7.5, leading=10, textColor=GOLD_500)
BODY = _style("body")
BODY_BOLD = _style("bodybold", fontName="Helvetica-Bold", fontSize=10.5, leading=14)
MUTED = _style("muted", fontSize=8, leading=11, textColor=SLATE_500)
CELL = _style("cell", fontSize=9, leading=11.5)
CELL_RIGHT = _style("cellr", fontSize=9, leading=11.5, alignment=TA_RIGHT)
CELL_CENTER = _style("cellc", fontSize=9, leading=11.5, alignment=TA_CENTER)
HEAD = _style("head", fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=colors.white)
HEAD_RIGHT = ParagraphStyle("headr", parent=HEAD, alignment=TA_RIGHT)
HEAD_CENTER = ParagraphStyle("headc", parent=HEAD, alignment=TA_CENTER)


###########################################################################################################################################
#                                                   Formatting helpers
###########################################################################################################################################
def _money(value):
    return "Rs. {:,.2f}".format(value)


def _decimal(value):
    try:
        return Decimal(str(value).strip() or "0")
    except InvalidOperation:
        return Decimal("0")


_ONES = ("Zero One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve Thirteen "
         "Fourteen Fifteen Sixteen Seventeen Eighteen Nineteen").split()
_TENS = ("", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety")


def _words(n):
    """Integer to words in the Indian numbering system (lakh, crore)."""
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else " " + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " Hundred" + ("" if n % 100 == 0 else " " + _words(n % 100))
    div, name = next(unit for unit in ((10 ** 7, "Crore"), (10 ** 5, "Lakh"), (1000, "Thousand")) if n >= unit[0])
    return _words(n // div) + " " + name + ("" if n % div == 0 else " " + _words(n % div))


def amount_in_words(amount):
    rupees = int(amount)
    paise = int((amount - rupees) * 100)
    text = "Rupees " + _words(rupees)
    if paise:
        text += " and " + _words(paise) + " Paise"
    return text + " Only"


###########################################################################################################################################
#                                                   Page decoration
###########################################################################################################################################
class _NumberedCanvas(canvas.Canvas):
    """Canvas that knows the total page count, for "Page x of y"."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pages = []

    def showPage(self):
        self._pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._pages)
        for state in self._pages:
            self.__dict__.update(state)
            self.setFont("Helvetica", 7.5)
            self.setFillColor(SLATE_500)
            self.drawRightString(self._pagesize[0] - MARGIN, FOOTER - 9 * mm,
                                 "Page %d of %d" % (self._pageNumber, total))
            super().showPage()
        super().save()


def _draw_logo(c, cx, cy, r):
    """College crest clipped to a circle with a white ring; monogram if the image is missing."""
    c.setFillColor(colors.white)
    c.circle(cx, cy, r + 1.2 * mm, stroke=0, fill=1)
    if os.path.exists(LOGO_PATH):
        c.saveState()
        path = c.beginPath()
        path.circle(cx, cy, r)
        c.clipPath(path, stroke=0, fill=0)
        c.drawImage(LOGO_PATH, cx - r, cy - r, 2 * r, 2 * r)
        c.restoreState()
    else:
        c.setFillColor(NAVY_800)
        c.circle(cx, cy, r, stroke=0, fill=1)
        c.setFillColor(GOLD_400)
        c.setFont("Times-Bold", r * 0.9)
        c.drawCentredString(cx, cy - r * 0.3, "MC")


def _draw_footer(c, width):
    c.setStrokeColor(GOLD_500)
    c.setLineWidth(0.8)
    c.line(MARGIN, FOOTER, width - MARGIN, FOOTER)
    c.setFont("Helvetica", 7.5)
    c.setFillColor(SLATE_500)
    c.drawString(MARGIN, FOOTER - 4.5 * mm, "%s, %s  ·  %s" % (COLLEGE, ADDRESS, PHONE))
    c.drawString(MARGIN, FOOTER - 9 * mm, "This is a computer-generated invoice and does not require a signature.")


def _first_page(info):
    def draw(c, doc):
        width, height = doc.pagesize
        c.saveState()
        c.setFillColor(NAVY_800)
        c.rect(0, height - FIRST_BAND, width, FIRST_BAND, stroke=0, fill=1)
        c.setFillColor(GOLD_500)
        c.rect(0, height - FIRST_BAND - 1.6 * mm, width, 1.6 * mm, stroke=0, fill=1)

        r = 12 * mm
        cy = height - FIRST_BAND / 2
        _draw_logo(c, MARGIN + r, cy, r)

        x = MARGIN + 2 * r + 7 * mm
        c.setFillColor(colors.white)
        c.setFont("Times-Bold", 22)
        c.drawString(x, cy + 3 * mm, BRAND)
        c.setFillColor(NAVY_200)
        c.setFont("Helvetica", 8.5)
        c.drawString(x, cy - 2.5 * mm, COLLEGE)
        c.drawString(x, cy - 7 * mm, "%s  ·  %s" % (ADDRESS, PHONE))

        right = width - MARGIN
        c.setFillColor(GOLD_400)
        c.setFont("Helvetica-Bold", 22)
        c.drawRightString(right, cy + 3 * mm, "INVOICE")
        c.setFillColor(colors.white)
        c.setFont("Helvetica", 9)
        c.drawRightString(right, cy - 2.5 * mm, "No. " + info["number"])
        c.drawRightString(right, cy - 7 * mm, info["issued"].strftime("%d %b %Y"))

        _draw_footer(c, width)
        c.restoreState()
    return draw


def _later_pages(info):
    def draw(c, doc):
        width, height = doc.pagesize
        c.saveState()
        c.setFillColor(NAVY_800)
        c.rect(0, height - LATER_BAND, width, LATER_BAND, stroke=0, fill=1)
        c.setFillColor(GOLD_500)
        c.rect(0, height - LATER_BAND - 1 * mm, width, 1 * mm, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Times-Bold", 13)
        c.drawString(MARGIN, height - LATER_BAND / 2 - 1.5 * mm, BRAND)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(NAVY_200)
        c.drawRightString(width - MARGIN, height - LATER_BAND / 2 - 1.5 * mm,
                          "Invoice No. %s  (continued)" % info["number"])
        _draw_footer(c, width)
        c.restoreState()
    return draw


###########################################################################################################################################
#                                                   Content blocks
###########################################################################################################################################
def _details_block(info, width):
    customer = info["customer"]
    billed = [Paragraph("BILLED TO", LABEL), Spacer(1, 2 * mm),
              Paragraph(escape(customer.get("name") or "Customer"), BODY_BOLD)]
    for key in ("role", "phone", "email"):
        if customer.get(key):
            billed.append(Paragraph(escape(str(customer[key])), BODY))

    paid = info["payment"] == "Card"
    status = ('<font color="#15803d"><b>PAID</b></font>' if paid
              else '<font color="#b45309"><b>PAY AT COUNTER</b></font>')
    rows = [
        ("Invoice No.", info["number"]),
        ("Date", info["issued"].strftime("%d %b %Y, %I:%M %p")),
        ("Payment", "Debit card" if paid else "Cash on collection"),
        ("Status", status),
    ]
    details = [Paragraph("INVOICE DETAILS", LABEL), Spacer(1, 2 * mm)]
    details += [Paragraph('<font color="#64748b">%s:</font>&nbsp; %s' % (k, v), BODY) for k, v in rows]

    gap = 6 * mm
    half = (width - gap) / 2
    table = Table([[billed, "", details]], colWidths=[half, gap, half])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, 0), NAVY_50),
        ("BACKGROUND", (2, 0), (2, 0), NAVY_50),
        ("LINEBEFORE", (0, 0), (0, 0), 2.5, NAVY_800),
        ("LINEBEFORE", (2, 0), (2, 0), 2.5, GOLD_500),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (1, 0), (1, 0), 0),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),
    ]))
    return table


def _items_table(lines, width):
    data = [[Paragraph("#", HEAD), Paragraph("ITEM", HEAD), Paragraph("QTY", HEAD_CENTER),
             Paragraph("UNIT PRICE", HEAD_RIGHT), Paragraph("AMOUNT", HEAD_RIGHT)]]
    for n, line in enumerate(lines, 1):
        text = "<b>%s</b>" % escape(line["name"])
        about = (line["about"] or "").strip()
        if about:
            if len(about) > 110:
                about = about[:107].rstrip() + "..."
            text += '<br/><font size="7.5" color="#64748b">%s</font>' % escape(about)
        data.append([Paragraph(str(n), CELL), Paragraph(text, CELL), Paragraph(str(line["qty"]), CELL_CENTER),
                     Paragraph(_money(line["price"]), CELL_RIGHT), Paragraph(_money(line["amount"]), CELL_RIGHT)])

    fractions = (0.06, 0.50, 0.10, 0.17, 0.17)
    table = Table(data, colWidths=[width * f for f in fractions], repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_800),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 1), (-1, -1), 0.5, SLATE_200),
        ("LINEBELOW", (0, -1), (-1, -1), 1, NAVY_800),
    ]
    for row in range(2, len(data), 2):
        style.append(("BACKGROUND", (0, row), (-1, row), NAVY_50))
    table.setStyle(TableStyle(style))
    return table


def _totals_block(info, total, count, width):
    note = [
        Paragraph("THANK YOU!", LABEL),
        Spacer(1, 1.5 * mm),
        Paragraph("Thank you for ordering from %s. Please show this invoice at the counter "
                  "when you collect your order." % BRAND, MUTED),
    ]
    if info["payment"] != "Card":
        note.append(Spacer(1, 1.5 * mm))
        note.append(Paragraph("<b>Amount due at collection:</b> %s" % _money(total), MUTED))

    totals = Table(
        [["Subtotal (%d item%s)" % (count, "" if count == 1 else "s"), _money(total)],
         ["Total payable", _money(total)]],
        colWidths=[width * 0.26, width * 0.18],
    )
    totals.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (-1, 0), NAVY_900),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("BACKGROUND", (0, 1), (-1, 1), NAVY_800),
        ("TEXTCOLOR", (0, 1), (-1, 1), colors.white),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 1), (-1, 1), 11),
        ("LINEBELOW", (0, 1), (-1, 1), 2, GOLD_500),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))

    outer = Table([[note, totals]], colWidths=[width * 0.54, width * 0.46])
    outer.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, 0), GOLD_50),
        ("LEFTPADDING", (0, 0), (0, 0), 10),
        ("RIGHTPADDING", (0, 0), (0, 0), 10),
        ("TOPPADDING", (0, 0), (0, 0), 8),
        ("BOTTOMPADDING", (0, 0), (0, 0), 9),
        ("LEFTPADDING", (1, 0), (1, 0), width * 0.02),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),
        ("TOPPADDING", (1, 0), (1, 0), 0),
    ]))
    words = Paragraph('<font color="#64748b">Amount in words:</font> <b>%s</b>' % amount_in_words(total), BODY)
    return KeepTogether([outer, Spacer(1, 4 * mm), words])


###########################################################################################################################################
#                                                   Public entry point
###########################################################################################################################################
def build_invoice_pdf(path, number, items, customer=None, payment=None, pagesize=A4):
    """Write the invoice to `path`.

    items: cart rows (name, price, about, img, qty)
    customer: optional dict with name, role, phone, email
    payment: "Card" (paid online) or anything else (cash at the counter)
    """
    lines = []
    for name, price, about, _img, qty in items:
        price = _decimal(price)
        qty = int(_decimal(qty))
        lines.append({"name": str(name), "about": about, "qty": qty, "price": price, "amount": price * qty})
    total = sum((line["amount"] for line in lines), Decimal("0"))

    info = {"number": number, "issued": datetime.now(), "customer": customer or {}, "payment": payment}

    width, height = pagesize
    content_width = width - 2 * MARGIN
    first = Frame(MARGIN, FOOTER + 4 * mm, content_width, height - FIRST_BAND - 8 * mm - FOOTER - 4 * mm,
                  id="first", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    later = Frame(MARGIN, FOOTER + 4 * mm, content_width, height - LATER_BAND - 7 * mm - FOOTER - 4 * mm,
                  id="later", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    doc = BaseDocTemplate(path, pagesize=pagesize, leftMargin=MARGIN, rightMargin=MARGIN,
                          title="Invoice %s" % number, author=BRAND, subject="Canteen order invoice")
    doc.addPageTemplates([
        PageTemplate(id="first", frames=[first], onPage=_first_page(info), autoNextPageTemplate="later"),
        PageTemplate(id="later", frames=[later], onPage=_later_pages(info)),
    ])

    story = [
        _details_block(info, content_width),
        Spacer(1, 7 * mm),
        _items_table(lines, content_width),
        Spacer(1, 6 * mm),
        _totals_block(info, total, sum(line["qty"] for line in lines), content_width),
    ]
    doc.build(story, canvasmaker=_NumberedCanvas)
    return total
