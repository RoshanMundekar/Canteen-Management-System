"""Helpers shared by the admin, staff, student, teacher and visitor views.

The three customer portals (student, teacher, visitor) used to carry their
own copy of every query and of the SMTP code; they now call these instead.
"""
import os
import random
import smtplib
from datetime import date
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from django.core.paginator import Paginator

from firstproject.background import in_background

# Override with environment variables instead of editing the code.
SMTP_USER = os.environ.get("CANTEEN_SMTP_USER", "modern.project2023@gmail.com")
SMTP_PASSWORD = os.environ.get("CANTEEN_SMTP_PASSWORD", "vxaaamxvcgkvfeie")

MENU_CATEGORIES = ("VEG", "NON-VEG", "BEVERAGES", "comboffer")


###########################################################################################################################################
#                                                   Menu and cart queries
###########################################################################################################################################
def fetch_menu(cursor, include_combos=False):
    """Load the menu with one query and split it by category.

    Returns {"data1": veg, "data2": non-veg, "data3": beverages} (plus
    "data4": combos when asked). Each entry is a list of
    (name, price, about, img, category) rows, the shape the templates unpack.
    """
    categories = MENU_CATEGORIES if include_combos else MENU_CATEGORIES[:3]
    cursor.execute(
        "SELECT dishName, dishPrice, dishAbout, dishImg, dishCategory FROM menutbl "
        "WHERE dishCategory IN %s ORDER BY Mid",
        (categories,),
    )
    # MySQL matched the old per-category WHERE case-insensitively, so group the same way.
    groups = {c.upper(): [] for c in categories}
    for row in cursor.fetchall():
        key = (row[4] or "").strip().upper()
        if key in groups:
            groups[key].append(row)
    return {"data%d" % n: groups[c.upper()] for n, c in enumerate(categories, 1)}


def paginate(request, rows, param="page", per_page=10):
    """One page of `rows` for the page number in ?param= (bad or out-of-range numbers fall back safely)."""
    return Paginator(rows, per_page).get_page(request.GET.get(param))


def cart_count(cursor, uname):
    cursor.execute(
        "SELECT COUNT(*) FROM orderfoodtbl WHERE Uname=%s AND Statuss='ordering'", (uname,)
    )
    return cursor.fetchone()[0]


def cart_items(cursor, uname):
    """Return the user's open cart as (name, price, info, img, qty) rows."""
    cursor.execute(
        "SELECT dishName, dishPrice, dishinfo, dishimgs, dishQuantity FROM orderfoodtbl "
        "WHERE Uname=%s AND Statuss='ordering'",
        (uname,),
    )
    return list(cursor.fetchall())


def cart_context(cursor, uname):
    """Template context for a cart page: rows with line totals, count and grand total."""
    items = cart_items(cursor, uname)
    rows = [row + (int(row[4]) * int(row[1]),) for row in items]
    return {
        "cartcount": len(rows),
        "finalcost": sum(row[5] for row in rows),
        "cartlst": rows,
    }


###########################################################################################################################################
#                                                   Orders and invoices
###########################################################################################################################################
def generate_invoice(uname, items, customer=None, payment=None):
    """Write a PDF invoice for the cart rows; return (absolute path, media-relative path)."""
    # Imported lazily: reportlab is slow to load and only needed when an order is placed.
    from firstproject.invoice_pdf import build_invoice_pdf

    number = "MC-%d" % random.randint(10000000, 99999999)
    filename = "%s_%s_invoice_.pdf" % (uname, number)
    os.makedirs(settings.INVOICE_PATH, exist_ok=True)
    abs_path = os.path.join(settings.INVOICE_PATH, filename)
    build_invoice_pdf(abs_path, number, items, customer=customer, payment=payment)
    return abs_path, "media/Invoices/" + filename


def order_customer(request, role):
    """'Billed to' details for the invoice, from the checkout form with session fallbacks."""
    post = request.POST
    name = " ".join(p for p in (post.get('Fname', '').strip(), post.get('Lname', '').strip()) if p)
    empno = request.session.get('empno')
    return {
        "name": name or request.session.get('uname'),
        "role": "%s  ·  ID %s" % (role, empno) if empno else role,
        "phone": post.get('phoneno', '').strip(),
        "email": post.get('Uemail', '').strip() or request.session.get('uemail'),
    }


def place_order(con, uname, customer=None, payment=None):
    """Turn the user's cart into an order: invoice PDF, invoicetbl row, status 'ordered'.

    customer / payment are printed on the invoice (see invoice_pdf.build_invoice_pdf).

    Returns (cart rows, absolute invoice path), or (None, None) if the cart is empty.
    """
    cursor = con.cursor()
    items = cart_items(cursor, uname)
    if not items:
        return None, None
    abs_path, media_path = generate_invoice(uname, items, customer, payment)
    cursor.execute(
        "INSERT INTO invoicetbl(Uname, invoicename, invoiceDate) VALUES (%s, %s, %s)",
        (uname, media_path, str(date.today())),
    )
    cursor.execute(
        "UPDATE orderfoodtbl SET Statuss='ordered' WHERE Uname=%s AND Statuss='ordering'", (uname,)
    )
    con.commit()
    return items, abs_path


def invoice_rows(cursor, uname):
    """(invoice path, date) rows for the invoice history page."""
    cursor.execute("SELECT invoicename, invoiceDate FROM invoicetbl WHERE Uname=%s ORDER BY invoiceId DESC", (uname,))
    return list(cursor.fetchall())


###########################################################################################################################################
#                                                   Password reset
###########################################################################################################################################
def send_otp(cursor, con, email):
    otp = str(random.randint(111111, 999999))
    cursor.execute("UPDATE studentachertbl SET otpval=%s WHERE umail=%s", (otp, email))
    con.commit()
    send_mail(email, "OTP Verification", "Hello User! Your forget password OTP is: " + otp)


def reset_password(cursor, con, email, otp, new_password):
    """Set the new password if the OTP matches; return True on success."""
    # Check first: UPDATE's row count is 0 when the new password equals the old one.
    if not cursor.execute("SELECT 1 FROM studentachertbl WHERE umail=%s AND otpval=%s", (email, otp)):
        return False
    cursor.execute(
        "UPDATE studentachertbl SET upass=%s WHERE umail=%s AND otpval=%s",
        (new_password, email, otp),
    )
    con.commit()
    return True


###########################################################################################################################################
#                                                   Email
###########################################################################################################################################
@in_background
def send_mail(to_addr, subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        part = MIMEBase('application', 'octet-stream')
        with open(attachment_path, "rb") as f:
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % os.path.basename(attachment_path))
        msg.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_addr, msg.as_string())


def logout_session(request):
    request.session.pop('uname', None)
    request.session.pop('userid', None)
