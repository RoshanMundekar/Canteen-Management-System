import random

from django.shortcuts import redirect, render
from django.contrib import messages

from firstproject.db import dbConnection
from firstproject.common import (
    fetch_menu, cart_count, cart_context, place_order, order_customer, invoice_rows, paginate,
    send_otp, reset_password, logout_session,
)

LOGIN_TEMPLATE = 'visitorsapp/studlogin.html'
ROLE = "visitor"

###########################################################################################################################################
#                                               Food Recommendation Function
###########################################################################################################################################
def recommend(cursor, dish_id):
    """Return up to 5 dish ids bought together with `dish_id`, or [] if there is too little data."""
    # Imported here, not at module level: these libraries take several seconds
    # to load and would otherwise slow down every server start and reload.
    import numpy as np
    import pandas as pd
    from sklearn.decomposition import TruncatedSVD

    cursor.execute("SELECT uid, dishId, dishquantity FROM foodrecommend")
    df = pd.DataFrame(list(cursor.fetchall()), columns=['uid', 'dishId', 'dishquantity'])
    if df.empty:
        return []
    df = df.astype({"uid": int, "dishId": int, "dishquantity": int})
    X = df.pivot_table(values='dishquantity', index='uid', columns='dishId', fill_value=0).T
    if dish_id not in X.index:
        return []
    try:
        decomposed_matrix = TruncatedSVD(n_components=2).fit_transform(X)
    except ValueError:
        # Not enough users/dishes yet for a 2-component decomposition.
        return []
    correlation_product = np.corrcoef(decomposed_matrix)[list(X.index).index(dish_id)]
    recommended = [int(d) for d in X.index[correlation_product > 0.70] if d != dish_id]
    return recommended[:5]


_recommend_table_ready = False


def ensure_recommend_table(cursor):
    """Create foodrecommend if the database was set up from a dump that lacks it."""
    global _recommend_table_ready
    if not _recommend_table_ready:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS foodrecommend ("
            " frId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
            " uid INT NOT NULL,"
            " dishId INT NOT NULL,"
            " dishquantity INT NOT NULL DEFAULT 1,"
            " KEY uid (uid)"
            ")"
        )
        _recommend_table_ready = True


def recommended_dishes(cursor, userid):
    """Menu rows recommended from the user's most recent purchase.

    Recommendations are optional: any failure leaves the list empty instead of
    breaking the cart page.
    """
    try:
        ensure_recommend_table(cursor)
        cursor.execute("SELECT dishId FROM foodrecommend WHERE uid=%s ORDER BY frId DESC LIMIT 1", (userid,))
        row = cursor.fetchone()
        if not row:
            return []
        dish_ids = recommend(cursor, int(row[0]))
        if not dish_ids:
            return []
        cursor.execute(
            "SELECT Mid, dishName, dishPrice, dishAbout, dishImg, dishCategory FROM menutbl WHERE Mid IN %s",
            (tuple(dish_ids),),
        )
        by_id = {r[0]: r[1:] for r in cursor.fetchall()}
        return [by_id[d] for d in dish_ids if d in by_id]
    except Exception as e:
        print("Recommendation failed:", e)
        return []

###########################################################################################################################################
#                                                   Home page
###########################################################################################################################################
def home(request):
    datadict = fetch_menu(dbConnection().cursor())
    datadict["usrempno"] = request.session.get('empno')
    return render(request, 'visitorsapp/home.html', datadict)

###########################################################################################################################################
#                                                   Visitor Login and Register
###########################################################################################################################################
def vistlogin(request):
    if request.method == 'POST':
        email = request.POST['visitemail']
        password = request.POST['password']

        cursor = dbConnection().cursor()
        cursor.execute(
            'SELECT * FROM studenTachertbl WHERE umail = %s AND upass = %s AND role=%s',
            (email, password, ROLE),
        )
        result = cursor.fetchone()
        if result:
            request.session['uname'] = result[1]
            request.session['userid'] = result[0]
            request.session['uemail'] = result[2]
            request.session['empno'] = result[5]
            return redirect('visitorindex')
    return render(request, LOGIN_TEMPLATE)

def visitregister(request):
    if request.method == 'POST':
        con = dbConnection()
        try:
            con.cursor().execute(
                "INSERT INTO studenTachertbl (Uname, umail, mobileno, upass, employeerollno, role) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (request.POST['Name'], request.POST['uemail'], request.POST['mobileno'],
                 request.POST['Upass'], str(random.randint(111, 999)), ROLE),
            )
            con.commit()
        except Exception as e:
            con.rollback()
            print("Database Error occured:", e)
        return render(request, LOGIN_TEMPLATE)
    return render(request, 'visitorsapp/studregister.html')

def logout(request):
    logout_session(request)
    return redirect('home')


def visitorindex(request):
    if request.session.get('uname'):
        cursor = dbConnection().cursor()
        cartdict = {"cartcount": cart_count(cursor, request.session['uname']),
                    "usrempno": request.session['empno']}
        return render(request, 'visitorsapp/studindex.html', cartdict)
    return render(request, LOGIN_TEMPLATE)


def visitorprofile(request):
    if request.session.get('uname'):
        con = dbConnection()
        cursor = con.cursor()
        usrname = request.session['uname']
        empnos = request.session['empno']

        if request.method == 'POST':
            # Name and visitor id are read-only: take them from the session, not the form.
            cursor.execute(
                "UPDATE studentachertbl SET umail=%s, mobileno=%s WHERE Uname=%s AND employeerollno=%s",
                (request.POST['emailid'], request.POST['mobileno'], usrname, empnos),
            )
            con.commit()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect("visitorprofile")

        cursor.execute(
            "SELECT Uname, umail, mobileno, employeerollno FROM studentachertbl "
            "WHERE Uname=%s AND employeerollno=%s",
            (usrname, empnos),
        )
        row = cursor.fetchone() or ("", "", "", "")
        cartdict = {
            "cartcount": cart_count(cursor, usrname),
            "usrempno": empnos,
            "usrnames": row[0],
            "usrmail": row[1],
            "usermobile": row[2],
            "usrempId": row[3],
        }
        return render(request, 'visitorsapp/studprodile.html', cartdict)
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Menu
###########################################################################################################################################

def visitormenu(request):
    if request.session.get('uname'):
        cursor = dbConnection().cursor()
        datadict = fetch_menu(cursor)
        datadict["cartcount"] = cart_count(cursor, request.session['uname'])
        datadict["usrempno"] = request.session['empno']
        return render(request, 'visitorsapp/menu.html', datadict)
    return render(request, LOGIN_TEMPLATE)

def visitoraddtocart(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            con = dbConnection()
            con.cursor().execute(
                "INSERT INTO orderFoodtbl(Uname, dishName, dishPrice, dishinfo, dishimgs, dishQuantity, Statuss) "
                "VALUES (%s, %s, %s, %s, %s, %s, 'ordering')",
                (request.session['uname'], request.POST['addish'], request.POST['pricedish'],
                 request.POST['aboutdish'], request.POST['imgdish'], request.POST['Dquantity']),
            )
            con.commit()
            messages.success(request, 'Added to cart!')
        return redirect("visitormenu")
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Add and Remove from Cart
###########################################################################################################################################
def visitorcartdata(request):
    if request.session.get('uname'):
        cursor = dbConnection().cursor()
        cartdict = cart_context(cursor, request.session['uname'])
        cartdict["Recommend_list"] = recommended_dishes(cursor, request.session['userid'])
        cartdict["usrempno"] = request.session['empno']
        return render(request, 'visitorsapp/cart.html', cartdict)
    return render(request, LOGIN_TEMPLATE)

def visitorremovecartdata(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            con = dbConnection()
            con.cursor().execute(
                "DELETE FROM orderfoodtbl WHERE Uname=%s AND dishName=%s AND Statuss='ordering'",
                (request.session['uname'], request.POST['removedish']),
            )
            con.commit()
        return redirect('visitorcartdata')
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Checkout
###########################################################################################################################################

def visitorcheckout(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            cartdict = {"cartcount": cart_count(dbConnection().cursor(), request.session['uname']),
                        "dishPrice": request.POST['finalcost'],
                        "usrempno": request.session['empno']}
            template = 'visitorsapp/checkout1.html' if request.POST['pmode'] == "Card" else 'visitorsapp/checkout2.html'
            return render(request, template, cartdict)
        return redirect('visitorcartdata')
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Place Order
###########################################################################################################################################
def record_purchases(con, userid, items):
    """Store what was bought in foodrecommend so recommend() can learn from it."""
    cursor = con.cursor()
    ensure_recommend_table(cursor)
    names = tuple({row[0] for row in items})
    cursor.execute("SELECT dishName, Mid FROM menutbl WHERE dishName IN %s", (names,))
    mid_by_name = {}
    for name, mid in cursor.fetchall():
        mid_by_name.setdefault(name, mid)
    rows = [(userid, mid_by_name[name], qty)
            for name, _price, _info, _img, qty in items if name in mid_by_name]
    if rows:
        cursor.executemany("INSERT INTO foodrecommend(uid, dishId, dishquantity) VALUES (%s, %s, %s)", rows)
        con.commit()


def visitorplaceorder(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            con = dbConnection()
            items, _invoice_path = place_order(con, request.session['uname'],
                                              order_customer(request, "Visitor"), request.POST.get('pmode'))
            if not items:
                messages.error(request, 'Your cart is empty.')
                return redirect('visitorcartdata')
            try:
                record_purchases(con, request.session['userid'], items)
            except Exception as e:
                con.rollback()
                print("Could not record purchases for recommendations:", e)
            messages.success(request, 'Your order has been placed successfully!')
            return redirect("visitorindex")
        return redirect('visitorcartdata')
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Invoice history
###########################################################################################################################################
def visitorinvoicehistory(request):
    if request.session.get('uname'):
        invoicedate = {
            "invoicedata": paginate(request, invoice_rows(dbConnection().cursor(), request.session['uname'])),
            "usrempno": request.session['empno'],
        }
        return render(request, "visitorsapp/invoice.html", invoicedate)
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Feedback
###########################################################################################################################################
def visitorfeedback(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            con = dbConnection()
            con.cursor().execute(
                "INSERT INTO userfeedback(Uname, feedbacks) VALUES (%s, %s)",
                (request.session['uname'], request.POST['feedback']),
            )
            con.commit()
            messages.success(request, 'The feedback has been submitted successfully!')
            return redirect('visitorfeedback')
        return render(request, "visitorsapp/studfeedback.html", {"usrempno": request.session['empno']})
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Send OTP and Set Password
###########################################################################################################################################
def sendotp(request):
    if request.method == 'POST':
        email = request.POST['otpemail']
        con = dbConnection()
        send_otp(con.cursor(), con, email)
        messages.success(request, 'OTP send Successfully!')
        return render(request, "visitorsapp/setpassword.html", {"usrmailid": email})
    return render(request, "visitorsapp/studsendotp.html")

def setpassword(request):
    if request.method == 'POST':
        email = request.POST['usremails']
        con = dbConnection()
        if reset_password(con.cursor(), con, email, request.POST['finalotp'], request.POST['finalpass']):
            messages.success(request, 'Your password has been updated successfully!!')
            return redirect('vistlogin')
        messages.error(request, 'Please enter correct OTP')
        return render(request, "visitorsapp/setpassword.html", {"usrmailid": email})
    return render(request, "visitorsapp/setpassword.html")
