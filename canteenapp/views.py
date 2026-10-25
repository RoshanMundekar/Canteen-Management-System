import secrets
import string

from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from firstproject.db import dbConnection
from firstproject.common import fetch_menu, paginate, send_mail, logout_session

LOGIN_TEMPLATE = 'canteenapp/adlogin.html'
MENU_PAGE_PARAMS = {"data1": "veg", "data2": "nonveg", "data3": "bev", "data4": "combo"}

###########################################################################################################################################
#                                                   Admin Login, Register, Logout
###########################################################################################################################################
def adlogin(request):
    if request.method == 'POST':
        cursor = dbConnection().cursor()
        cursor.execute('SELECT * FROM user_register WHERE umail = %s AND upass = %s',
                       (request.POST['Email'], request.POST['password']))
        result = cursor.fetchone()
        if result:
            request.session['uname'] = result[1]
            request.session['userid'] = result[0]
            return redirect('adindex')
    return render(request, LOGIN_TEMPLATE)

def adregister(request):
    if request.method == 'POST':
        con = dbConnection()
        try:
            con.cursor().execute(
                "INSERT INTO user_register (Uname, umail, mobileno, upass, uaddress) VALUES (%s, %s, %s, %s, %s)",
                (request.POST['Name'], request.POST['uemail'], request.POST['mobileno'],
                 request.POST['Upass'], request.POST['Uaddres']),
            )
            con.commit()
        except Exception as e:
            con.rollback()
            print("Database Error occured:", e)
        return render(request, LOGIN_TEMPLATE)
    return render(request, 'canteenapp/adregister.html')


def adindex(request):
    if request.session.get('uname'):
        return render(request, 'canteenapp/adindex.html')
    return render(request, LOGIN_TEMPLATE)


def logout(request):
    logout_session(request)
    return redirect('home')


###########################################################################################################################################
#                                                   Add Menu
###########################################################################################################################################
def add_dish(request, dishname, dishprice, aboutdish, dishimg, dishcategory):
    con = dbConnection()
    try:
        con.cursor().execute(
            "INSERT INTO menutbl (dishName, dishPrice, dishAbout, dishImg, dishCategory) VALUES (%s, %s, %s, %s, %s)",
            (dishname, dishprice, aboutdish, dishimg, dishcategory),
        )
        con.commit()
        messages.success(request, 'Dish added successfully!')
    except Exception as e:
        con.rollback()
        print("Database Error occured:", e)


def admenu(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            dishimg = request.FILES['dishimg']
            filepath = FileSystemStorage().save(dishimg.name, dishimg)
            add_dish(request, request.POST['dishname'], request.POST['dishprice'],
                     request.POST['aboutdish'], filepath, request.POST['dishcategory'])
            return redirect('admenu')

        menu = fetch_menu(dbConnection().cursor(), include_combos=True)
        # The combo dropdowns need every dish, not just the page on screen.
        datadict = {"all_menus": [row[0] for key in ("data1", "data2", "data3") for row in menu[key]]}
        # Each category pages on its own (?veg=2&bev=3 ...); 12 cards fill 2, 3 or 4 grid columns evenly.
        for key, param in MENU_PAGE_PARAMS.items():
            datadict[key] = paginate(request, menu[key], param, per_page=12)
        return render(request, 'canteenapp/admenu.html', datadict)
    return render(request, LOGIN_TEMPLATE)


def combomenu(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            add_dish(request, request.POST['dish1'] + "+" + request.POST['dish2'],
                     request.POST['comboprice2'], request.POST['aboutdish'],
                     "../../../media/comboofer.jpg", "comboffer")
        return redirect('admenu')
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Update Menu
###########################################################################################################################################
def admenu2(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            dishname = request.POST['dishname']
            dishimg = request.FILES['dishimg2']
            filepath = FileSystemStorage().save(dishimg.name, dishimg)

            con = dbConnection()
            try:
                con.cursor().execute(
                    "UPDATE menutbl SET dishName=%s, dishPrice=%s, dishAbout=%s, dishImg=%s WHERE dishName=%s",
                    (request.POST['dishname2'], request.POST['dishprice2'],
                     request.POST['aboutdish2'], filepath, dishname),
                )
                con.commit()
                messages.success(request, dishname + ' updated successfully!')
            except Exception as e:
                con.rollback()
                print("Database Error occured:", e)
        return redirect('admenu')
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Add and Delete staff
###########################################################################################################################################
def randompassgenerate(length=12):
    """Random password with at least one digit, upper, lower and symbol."""
    symbols = '@#$%=:?./|~>*()<'
    pools = [string.digits, string.ascii_uppercase, string.ascii_lowercase, symbols]
    chars = [secrets.choice(pool) for pool in pools]
    combined = ''.join(pools)
    chars += [secrets.choice(combined) for _ in range(length - len(chars))]
    secrets.SystemRandom().shuffle(chars)
    return ''.join(chars)


def save_staff(request):
    """Insert the staff member from the posted form and email them their login."""
    sMail = request.POST['Smail']
    sPass = request.POST['Spass']
    con = dbConnection()
    try:
        con.cursor().execute(
            "INSERT INTO stafftbl (Sfname, Slname, Smail, Spass, Smobile, Saddress, staffcat) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (request.POST['staffFname'], request.POST['staffLname'], sMail, sPass,
             request.POST['Smobile'], request.POST['Saddress'], request.POST['stafcategory']),
        )
        con.commit()
    except Exception as e:
        con.rollback()
        print("Database Error occured:", e)
        return
    send_mail(sMail, "Registration Successful!!",
              "Hello user! your Registration has been done successfully! "
              "your Email id: " + sMail + " and password: " + sPass)
    messages.success(request, 'Staff added sucessfully!!')


def addstaff(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            save_staff(request)
            return redirect('addstaff')

        cursor = dbConnection().cursor()
        cursor.execute("SELECT Sfname, Slname, Smail, Smobile, Saddress FROM stafftbl")
        staffdict = {"data1": paginate(request, list(cursor.fetchall())),
                     "usrpass": randompassgenerate()}
        return render(request, 'canteenapp/addstaff.html', staffdict)
    return render(request, LOGIN_TEMPLATE)

def addstaff2(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            save_staff(request)
        return redirect('addstaff')
    return render(request, LOGIN_TEMPLATE)

def deletestaff(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            con = dbConnection()
            try:
                con.cursor().execute(
                    "DELETE FROM stafftbl WHERE Sfname=%s AND Slname=%s AND Smail=%s AND Smobile=%s",
                    (request.POST['SFName'], request.POST['SLName'],
                     request.POST['SEmailid'], request.POST['SMobile']),
                )
                con.commit()
            except Exception as e:
                con.rollback()
                print("Database Error occured in delete staff:", e)
        return redirect('addstaff')
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   View Feedback
###########################################################################################################################################
def viewfeedback(request):
    if request.session.get('uname'):
        cursor = dbConnection().cursor()
        cursor.execute("SELECT Uname, feedbacks FROM userFeedBack")
        return render(request, 'canteenapp/adfeedback.html', {"feedata": list(cursor.fetchall())})
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   Home page
###########################################################################################################################################
def home(request):
    return render(request, 'studentapp/home.html', fetch_menu(dbConnection().cursor()))

###########################################################################################################################################
#                                                   User Information
###########################################################################################################################################
def userinfo(request):
    if request.session.get('uname'):
        cursor = dbConnection().cursor()

        cursor.execute(
            "SELECT Uname, umail, mobileno, employeerollno, role FROM studentachertbl "
            "WHERE role IN ('teacher', 'student', 'visitor')"
        )
        by_role = {"TEACHER": [], "STUDENT": [], "VISITOR": []}
        for row in cursor.fetchall():
            role = (row[4] or "").strip().upper()
            if role in by_role:
                by_role[role].append(row)

        cursor.execute("SELECT Sfname, Slname, Smail, Smobile, Saddress, staffcat FROM stafftbl")

        userdict = {
            "teacherData": paginate(request, by_role["TEACHER"], "faculty"),
            "studentData": paginate(request, by_role["STUDENT"], "students"),
            # Visitors have no meaningful roll number; the template expects (name, email, mobile, role).
            "visitorData": paginate(request, [(r[0], r[1], r[2], r[4]) for r in by_role["VISITOR"]], "visitors"),
            "staffData": paginate(request, list(cursor.fetchall()), "staff"),
        }
        return render(request, 'canteenapp/userdata.html', userdict)
    return render(request, LOGIN_TEMPLATE)

###########################################################################################################################################
#                                                   User Payments
###########################################################################################################################################
def userpament(request):
    if request.session.get('uname'):
        cursor = dbConnection().cursor()
        cursor.execute("SELECT Uname, invoicename, invoiceDate FROM invoicetbl ORDER BY invoiceId DESC")
        return render(request, 'canteenapp/userpayment.html', {"InvoiceData": paginate(request, list(cursor.fetchall()))})
    return render(request, LOGIN_TEMPLATE)
