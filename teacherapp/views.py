from django.shortcuts import redirect, render
from django.contrib import messages

from firstproject.db import dbConnection
from firstproject.common import (
    fetch_menu, cart_count, cart_context, place_order, order_customer, invoice_rows, paginate,
    send_otp, reset_password, send_mail, logout_session,
)

LOGIN_TEMPLATE = 'teacherapp/studlogin.html'
ROLE = "teacher"

###########################################################################################################################################
#                                                   Home page
###########################################################################################################################################
def home(request):
    cursor = dbConnection().cursor()
    datadict = fetch_menu(cursor)
    datadict["usrempno"] = request.session.get('empno')
    return render(request, 'teacherapp/home.html', datadict)

###########################################################################################################################################
#                                                   Teacher Login and Register
###########################################################################################################################################
def teacherlogin(request):
    if request.method == 'POST':
        empno = request.POST['rolempNO']
        password = request.POST['password']

        cursor = dbConnection().cursor()
        cursor.execute(
            'SELECT * FROM studenTachertbl WHERE employeeempno = %s AND upass = %s AND role=%s',
            (empno, password, ROLE),
        )
        result = cursor.fetchone()
        if result:
            request.session['uname'] = result[1]
            request.session['userid'] = result[0]
            request.session['uemail'] = result[2]
            request.session['empno'] = result[5]
            return redirect('teaherindex')
    return render(request, LOGIN_TEMPLATE)

def teacherregister(request):
    if request.method == 'POST':
        con = dbConnection()
        try:
            con.cursor().execute(
                "INSERT INTO studenTachertbl (Uname, umail, mobileno, upass, employeerollno, role) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (request.POST['Name'], request.POST['uemail'], request.POST['mobileno'],
                 request.POST['Upass'], request.POST['Uaddres'], ROLE),
            )
            con.commit()
        except Exception as e:
            con.rollback()
            print("Database Error occured:", e)
        return render(request, LOGIN_TEMPLATE)
    return render(request, 'teacherapp/studregister.html')

def logout(request):
    logout_session(request)
    return redirect('home')


def teaherindex(request):
    if request.session.get('uname'):
        cursor = dbConnection().cursor()
        cartdict = {"cartcount": cart_count(cursor, request.session['uname']),
                    "usrempno": request.session['empno']}
        return render(request, 'teacherapp/studindex.html', cartdict)
    return render(request, LOGIN_TEMPLATE)


def teacherprofile(request):
    if request.session.get('uname'):
        con = dbConnection()
        cursor = con.cursor()
        usrname = request.session['uname']
        empnos = request.session['empno']

        if request.method == 'POST':
            # Name and roll number are read-only: take them from the session, not the form.
            cursor.execute(
                "UPDATE studentachertbl SET umail=%s, mobileno=%s WHERE Uname=%s AND employeerollno=%s",
                (request.POST['emailid'], request.POST['mobileno'], usrname, empnos),
            )
            con.commit()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect("teacherprofile")

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
        return render(request, 'teacherapp/teacherprodile.html', cartdict)
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Menu
###########################################################################################################################################

def teachermenu(request):
    if request.session.get('uname'):
        cursor = dbConnection().cursor()
        datadict = fetch_menu(cursor)
        datadict["cartcount"] = cart_count(cursor, request.session['uname'])
        datadict["usrempno"] = request.session['empno']
        return render(request, 'teacherapp/menu.html', datadict)
    return render(request, LOGIN_TEMPLATE)

def teacheraddtocart(request):
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
        return redirect("teachermenu")
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Add and Remove from Cart
###########################################################################################################################################
def teachercartdata(request):
    if request.session.get('uname'):
        cartdict = cart_context(dbConnection().cursor(), request.session['uname'])
        cartdict["usrempno"] = request.session['empno']
        return render(request, 'teacherapp/cart.html', cartdict)
    return render(request, LOGIN_TEMPLATE)

def teacherremovecartdata(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            con = dbConnection()
            con.cursor().execute(
                "DELETE FROM orderfoodtbl WHERE Uname=%s AND dishName=%s AND Statuss='ordering'",
                (request.session['uname'], request.POST['removedish']),
            )
            con.commit()
        return redirect('teachercartdata')
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Checkout
###########################################################################################################################################

def teachercheckout(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            cartdict = {"cartcount": cart_count(dbConnection().cursor(), request.session['uname']),
                        "dishPrice": request.POST['finalcost'],
                        "usrempno": request.session['empno']}
            template = 'teacherapp/checkout1.html' if request.POST['pmode'] == "Card" else 'teacherapp/checkout2.html'
            return render(request, template, cartdict)
        return redirect('teachercartdata')
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Place Order
###########################################################################################################################################
def teacherplaceorder(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            items, invoice_path = place_order(dbConnection(), request.session['uname'],
                                              order_customer(request, "Teacher"), request.POST.get('pmode'))
            if not items:
                messages.error(request, 'Your cart is empty.')
                return redirect('teachercartdata')
            send_mail(request.session['uemail'], "order invoice.",
                      "Hello user! your oder has been placed successfully! "
                      "Please find attached Invoice in mail. Thank You!",
                      invoice_path)
            messages.success(request, 'Your order has been placed successfully!')
            return redirect("teaherindex")
        return redirect('teachercartdata')
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Invoice history
###########################################################################################################################################
def teacherinvoicehistory(request):
    if request.session.get('uname'):
        invoicedate = {
            "invoicedata": paginate(request, invoice_rows(dbConnection().cursor(), request.session['uname'])),
            "usrempno": request.session['empno'],
        }
        return render(request, "teacherapp/invoice.html", invoicedate)
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Feedback
###########################################################################################################################################
def teacherfeedback(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            con = dbConnection()
            con.cursor().execute(
                "INSERT INTO userfeedback(Uname, feedbacks) VALUES (%s, %s)",
                (request.session['uname'], request.POST['feedback']),
            )
            con.commit()
            messages.success(request, 'The feedback has been submitted successfully!')
            return redirect('teacherfeedback')
        return render(request, "teacherapp/studfeedback.html", {"usrempno": request.session['empno']})
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
        return render(request, "teacherapp/setpassword.html", {"usrmailid": email})
    return render(request, "teacherapp/studsendotp.html")

def setpassword(request):
    if request.method == 'POST':
        email = request.POST['usremails']
        con = dbConnection()
        if reset_password(con.cursor(), con, email, request.POST['finalotp'], request.POST['finalpass']):
            messages.success(request, 'Your password has been updated successfully!!')
            return redirect('teacherlogin')
        messages.error(request, 'Please enter correct OTP')
        return render(request, "teacherapp/setpassword.html", {"usrmailid": email})
    return render(request, "teacherapp/setpassword.html")
