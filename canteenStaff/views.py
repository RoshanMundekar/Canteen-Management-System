from django.shortcuts import redirect, render
from django.contrib import messages

from firstproject.db import dbConnection
from firstproject.common import send_mail, logout_session

LOGIN_TEMPLATE = 'canteenStaff/stafflogin.html'

###########################################################################################################################################
#                                                   Staff Login
###########################################################################################################################################
def stafflogin(request):
    if request.method == 'POST':
        cursor = dbConnection().cursor()
        cursor.execute(
            'SELECT * FROM stafftbl WHERE Smail = %s AND Spass = %s',
            (request.POST['Email'], request.POST['password']),
        )
        result = cursor.fetchone()
        if result:
            request.session['uname'] = result[1]
            request.session['userid'] = result[0]
            request.session['uemail'] = result[3]
            return redirect('staffindex')
    return render(request, LOGIN_TEMPLATE)

def logout(request):
    logout_session(request)
    return redirect('adlogin')


def staffindex(request):
    if request.session.get('uname'):
        return render(request, 'canteenStaff/staffindex.html')
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   View Order
###########################################################################################################################################
def takeorder(request):
    if request.session.get('uname'):
        cursor = dbConnection().cursor()
        cursor.execute(
            "SELECT Uname, dishName, dishPrice, dishinfo, dishimgs, dishQuantity "
            "FROM orderfoodtbl WHERE Statuss='ordered'"
        )
        return render(request, 'canteenStaff/orders.html', {"data1": list(cursor.fetchall())})
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Order Accept
###########################################################################################################################################
def orderaccept(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            usrname = request.POST['usrname']
            exptimes = request.POST['exptime']

            con = dbConnection()
            cursor = con.cursor()
            # Only the placed order is cleared; items still in the user's cart stay.
            cursor.execute("DELETE FROM orderfoodtbl WHERE Uname=%s AND Statuss='ordered'", (usrname,))
            con.commit()

            cursor.execute("SELECT umail FROM studentachertbl WHERE Uname=%s", (usrname,))
            res = cursor.fetchone()
            if res:
                send_mail(res[0], "order Placed",
                          "Hello user! your oder has been placed successfully! "
                          "We will deliver order within " + str(exptimes))

            messages.success(request, usrname + "'s Order accepted successfully!")
        return redirect("takeorder")
    return render(request, LOGIN_TEMPLATE)
