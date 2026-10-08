from django.http import HttpResponse
from django.shortcuts import redirect,render
import pymysql
from django.contrib import messages



def dbConnection():
    try:
        connection = pymysql.connect(host="localhost", user="root", password="root", database="canteendb",charset='utf8')
        return connection
    except:
        print("Something went wrong in database Connection")

def dbClose():
    try:
        dbConnection().close()
    except:
        print("Something went wrong in Close DB Connection")

###########################################################################################################################################
#                                                   Admin Login, Register, Logout
###########################################################################################################################################
def adlogin(request):
    if request.method == 'POST':
        email = request.POST['Email']
        password = request.POST['password'] 

        print(email,password)

        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM user_register WHERE umail = %s AND upass = %s', (email, password))
        result = cursor.fetchone()
        print("result in canteen views")
        print(result)
        print(result_count)
        if result_count>0:
            print("len of result")
            request.session['uname'] = result[1]
            request.session ['userid'] = result[0]

            # request.session.get('uname')
            return redirect('adindex')
            # return render(request,'canteenapp/adindex.html')
        else:
            return render(request,'canteenapp/adlogin.html')
    return render(request,'canteenapp/adlogin.html')

def adregister(request):
    if request.method == 'POST':
        #Parse form data    
        # print("hii register")
        Uname = request.POST['Name']
        Uemails = request.POST['uemail']
        Upasswords = request.POST['Upass']
        Umobno = request.POST['mobileno']
        Uadd = request.POST['Uaddres']
        # Urol = request.POST['urole']

        print(Uname,Uemails,Upasswords,Umobno,Uadd)

        try: 
            con = dbConnection()
            cursor = con.cursor()
            sql1 = "INSERT INTO user_register (Uname, umail, mobileno, upass, uaddress) VALUES (%s, %s, %s, %s, %s)"
            val1 = (Uname,Uemails,Umobno,Upasswords,Uadd)
            cursor.execute(sql1, val1)
            print("query 1 submitted")
            con.commit()
            FinalMsg = "Congrats! Your account registerd successfully!"
        except:
            con.rollback()
            msg = "Database Error occured"
            print(msg)
            return render(request,'canteenapp/adlogin.html')
        finally:
            dbClose()
        return render(request,'canteenapp/adlogin.html')
    return render(request,'canteenapp/adregister.html')


def adindex(request):
    if request.session.get('uname'):
        return render(request,'canteenapp/adindex.html')
    return render(request,'canteenapp/adlogin.html')


def logout(request):
    del request.session['uname']
    del request.session['userid']
    return redirect('home')


###########################################################################################################################################
#                                                   Add Menu
###########################################################################################################################################

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','wav','mp3'}
from django.core.files.storage import default_storage,FileSystemStorage
MEDIA_URL = '/media/'


def admenu(request):
    if request.session.get('uname'):
        con = dbConnection()
        cursor = con.cursor()
        # -------------------------- STARTER ---------------------------------------------
        sql1 = "SELECT * from menutbl where dishCategory='VEG'"        
        cursor.execute(sql1)
        res1 = cursor.fetchall()
        result1 = list(res1)

        Dname1 = [i[1] for i in result1]
        Dprice1 = [i[2] for i in result1]
        Dabout1 = [i[3] for i in result1]
        Dimg1 = [i[4] for i in result1]
        Dcat1 = [i[5] for i in result1]

        flst1 = zip(Dname1,Dprice1,Dabout1,Dimg1,Dcat1)

        # -------------------------- main dish ---------------------------------------------
        sql2 = "SELECT * from menutbl where dishCategory='NON-VEG'"        
        cursor.execute(sql2)
        res2 = cursor.fetchall()
        result2 = list(res2)

        Dname2 = [i[1] for i in result2]
        Dprice2 = [i[2] for i in result2]
        Dabout2 = [i[3] for i in result2]
        Dimg2 = [i[4] for i in result2]
        Dcat2 = [i[5] for i in result2]

        flst2 = zip(Dname2,Dprice2,Dabout2,Dimg2,Dcat2)
        
        # -------------------------- STARTER ---------------------------------------------
        sql3 = "SELECT * from menutbl where dishCategory='BEVERAGES'"        
        cursor.execute(sql3)
        res3 = cursor.fetchall()
        result3 = list(res3)

        Dname3 = [i[1] for i in result3]
        Dprice3 = [i[2] for i in result3]
        Dabout3 = [i[3] for i in result3]
        Dimg3 = [i[4] for i in result3]
        Dcat3 = [i[5] for i in result3]

        flst3 = zip(Dname3,Dprice3,Dabout3,Dimg3,Dcat3)

        # -------------------------- CoMBO OFFERS ---------------------------------------------
        sql4 = "SELECT * from menutbl where dishCategory='comboffer'"        
        cursor.execute(sql4)
        res4 = cursor.fetchall()
        result4 = list(res4)

        Dname4 = [i[1] for i in result4]
        Dprice4 = [i[2] for i in result4]
        Dabout4 = [i[3] for i in result4]
        Dimg4 = [i[4] for i in result4]
        Dcat4 = [i[5] for i in result4]

        all_dishes = Dname1+Dname2+Dname3
        print()
        print("all_dishes")
        print(all_dishes)
        print()


        if request.method == 'POST':
            #Parse form data    
            # print("hii register")
            dishname = request.POST['dishname']
            dishprice = request.POST['dishprice']
            aboutdish = request.POST['aboutdish']
            dishimg = request.FILES['dishimg']
            dishcategory = request.POST['dishcategory']


            fs = FileSystemStorage()
            filepath = fs.save(dishimg.name, dishimg)
            # filepath = fs.url(filepath)
            # file_name = default_storage.save(filename.name, filename)
            upload_Path= fs.path(filepath)
            print("filename")
            print(filepath)
            print(upload_Path)

            print(dishname,dishprice,aboutdish,dishimg,dishcategory)

            try: 
                con = dbConnection()
                cursor = con.cursor()
                sql1 = "INSERT INTO menutbl (dishName, dishPrice, dishAbout, dishImg, dishCategory) VALUES (%s, %s, %s, %s, %s)"
                val1 = (dishname,dishprice,aboutdish,filepath,dishcategory)
                cursor.execute(sql1, val1)
                print("query 1 submitted")
                con.commit()
                messages.success(request, 'Dish added successfully!')
                return redirect('admenu')
            except:
                con.rollback()
                msg = "Database Error occured"
                print(msg)
                return redirect('admenu')
            finally:
                dbClose()

        datadict = {"data1": zip(Dname1, Dprice1, Dabout1, Dimg1, Dcat1),
                    "data2": zip(Dname2, Dprice2, Dabout2, Dimg2, Dcat2),
                    "data3": zip(Dname3, Dprice3, Dabout3, Dimg3, Dcat3),
                    "data4": zip(Dname4, Dprice4, Dabout4, Dimg4, Dcat4),
                    "all_menus":all_dishes}


        return render(request,'canteenapp/admenu.html',datadict)   
    return render(request,'canteenapp/adlogin.html')


def combomenu(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            #Parse form data    
            # print("hii register")
            dish1 = request.POST['dish1']
            dish2 = request.POST['dish2']
            dishname = dish1+"+"+dish2
            aboutdish = request.POST['aboutdish']
            dishprice = request.POST['comboprice2']
            dishcategory = "comboffer"
            filepath = "../../../media/comboofer.jpg"

            print(dishname,dishprice)

            try: 
                con = dbConnection()
                cursor = con.cursor()
                sql1 = "INSERT INTO menutbl (dishName, dishPrice, dishAbout, dishImg, dishCategory) VALUES (%s, %s, %s, %s, %s)"
                val1 = (dishname,dishprice,aboutdish,filepath,dishcategory)
                cursor.execute(sql1, val1)
                print("query 1 submitted")
                con.commit()
                messages.success(request, 'Dish added successfully!')
                return redirect('admenu')
            except:
                con.rollback()
                msg = "Database Error occured"
                print(msg)
                return redirect('admenu')
            finally:
                dbClose()

        return render(request,'canteenapp/combomenu.html')   
    return render(request,'canteenapp/adlogin.html')

###########################################################################################################################################
#                                                   Update Menu
###########################################################################################################################################
def admenu2(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            #Parse form data    
            # print("hii register")
            dishname = request.POST['dishname']
            dishname2 = request.POST['dishname2']
            dishprice = request.POST['dishprice2']
            aboutdish = request.POST['aboutdish2']
            dishimg = request.FILES['dishimg2']
            dishcategory = request.POST['dishcategory2']


            fs = FileSystemStorage()
            filepath = fs.save(dishimg.name, dishimg)
            # filepath = fs.url(filepath)
            # file_name = default_storage.save(filename.name, filename)
            upload_Path= fs.path(filepath)
            print("filename")
            print(filepath)
            print(upload_Path)

            print(dishname,dishname2,dishprice,aboutdish,dishimg,dishcategory)

            try: 
                con = dbConnection()
                cursor = con.cursor()
                sql1 = "UPDATE menutbl SET dishName=%s, dishPrice=%s, dishAbout=%s, dishImg=%s where dishName=%s"
                val1 = (dishname2,dishprice,aboutdish,filepath,dishname)
                cursor.execute(sql1, val1)
                print("Update query submitted")
                con.commit()
                messages.success(request, dishname+' updated successfully!')
                return redirect('admenu')
            except:
                con.rollback()
                msg = "Database Error occured"
                print(msg)
                return redirect('admenu')
            finally:
                dbClose()
        return redirect('admenu') 
    return render(request,'canteenapp/adlogin.html')

###########################################################################################################################################
#                                                   Add and Delete staff
###########################################################################################################################################
import random
import array
def randompassgenerate():
    MAX_LEN = 12
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                     'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                     'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                     'z']
    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                     'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                     'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                     'Z']
    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
            '*', '(', ')', '<']
    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)
    password = ""
    for x in temp_pass_list:
            password = password + x
    return password


import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def sendemailtouser(usermail,registeremail,registerpass):   
    fromaddr = "modern.project2023@gmail.com"
    toaddr = usermail
   
    #instance of MIMEMultipart 
    msg = MIMEMultipart() 
  
    # storing the senders email address   
    msg['From'] = fromaddr 
  
    # storing the receivers email address  
    msg['To'] = toaddr 
  
    # storing the subject  
    msg['Subject'] = "Registration Successful!!"
  
    # string to store the body of the mail 
    body = "Hello user! your Registration has been done successfully! your <b>Email id: "+registeremail+" and password: "+registerpass+"</b>"
  
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain'))    
  
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
  
    # start TLS for security 
    s.starttls() 
  
    # Authentication 
    s.login(fromaddr, "vxaaamxvcgkvfeie") 
  
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
  
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
  
    # terminating the session 
    s.quit() 
def addstaff(request):
    if request.session.get('uname'):
        randompassword = randompassgenerate()
        con = dbConnection()
        cursor = con.cursor()
        sql1 = "SELECT * FROM stafftbl"
        cursor.execute(sql1)
        res = cursor.fetchall()
        result = list(res)

        SFnames = [i[1] for i in result]
        SLnames = [i[2] for i in result]
        SMail = [i[3] for i in result]
        SPass = [i[4] for i in result]
        SMobile = [i[5] for i in result]
        SAddress = [i[6] for i in result]

        staffdict = {"data1": zip(SFnames, SLnames, SMail, SMobile, SAddress),
                     "usrpass":randompassword}

        if request.method == 'POST':
            #Parse form data    
            # print("hii register")
            SfName = request.POST['staffFname']
            SlName = request.POST['staffLname']
            sMail = request.POST['Smail']
            sPass = request.POST['Spass']
            sMobile = request.POST['Smobile']
            sAddress = request.POST['Saddress']
            staffcategory = request.POST['stafcategory']

            print(SfName,SlName,sMail,sPass,sMobile,sAddress)

            try: 
                con = dbConnection()
                cursor = con.cursor()
                sql1 = "INSERT INTO stafftbl (Sfname, Slname, Smail, Spass, Smobile, Saddress, staffcat) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val1 = (SfName,SlName,sMail,sPass,sMobile,sAddress,staffcategory)
                cursor.execute(sql1, val1)

                sendemailtouser(sMail,sMail,sPass)
                  
                print("Update query submitted")
                con.commit()
                messages.success(request, 'Staff added sucessfully!!')
                return redirect('addstaff')
            except:
                con.rollback()
                msg = "Database Error occured"
                print(msg)
                return redirect('addstaff')
        return render(request,'canteenapp/addstaff.html',staffdict)
    return render(request,'canteenapp/adlogin.html')

def addstaff2(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            #Parse form data    
            # print("hii register")
            SfName = request.POST['staffFname']
            SlName = request.POST['staffLname']
            sMail = request.POST['Smail']
            sPass = request.POST['Spass']
            sMobile = request.POST['Smobile']
            sAddress = request.POST['Saddress']
            staffcategory = request.POST['stafcategory']

            print(SfName,SlName,sMail,sPass,sMobile,sAddress,staffcategory)

            try: 
                con = dbConnection()
                cursor = con.cursor()
                sql1 = "INSERT INTO stafftbl (Sfname, Slname, Smail, Spass, Smobile, Saddress, staffcat) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val1 = (SfName,SlName,sMail,sPass,sMobile,sAddress,staffcategory)
                cursor.execute(sql1, val1)
                print("Update query submitted")
                sendemailtouser(sMail,sMail,sPass)
                print("mail sent successfully")
                con.commit()
                messages.success(request, 'Staff added sucessfully!!')
                return redirect('addstaff')
            except:
                con.rollback()
                msg = "Database Error occured"
                print(msg)
        return redirect('addstaff')
    return render(request,'canteenapp/adlogin.html')

def deletestaff(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            #Parse form data    
            # print("hii register")
            SfName = request.POST['SFName']
            SlName = request.POST['SLName']
            sMail = request.POST['SEmailid']
            sMobile = request.POST['SMobile']

            print(SfName,SlName,sMail,sMobile)

            try: 
                con = dbConnection()
                cursor = con.cursor()
                sql1 = "DELETE FROM stafftbl WHERE Sfname=%s and Slname=%s and Smail=%s and Smobile=%s;"
                val1 = (SfName,SlName,sMail,sMobile)
                cursor.execute(sql1, val1)
                print("delete query submitted")
                con.commit()
            except:
                con.rollback()
                msg = "Database Error occured in delete staff"
                print(msg)
                return redirect('addstaff')
            return redirect('addstaff')
        return render(request,'canteenapp/addstaff.html')
    return render(request,'canteenapp/adlogin.html')

###########################################################################################################################################
#                                                   View Feedback
###########################################################################################################################################
def viewfeedback(request):
    if request.session.get('uname'):
        con = dbConnection()
        cursor = con.cursor()
        sql1 = "SELECT * FROM userFeedBack"
        cursor.execute(sql1)
        res = cursor.fetchall()
        result = list(res)
        print()
        print("result")
        print(result)
        print()

        Unames = [i[1] for i in result]
        Ufeedbacks = [i[2] for i in result]

        print(Unames,Ufeedbacks)

        fedbackdict = {
            "feedata":zip(Unames,Ufeedbacks)
        }

        return render(request,'canteenapp/adfeedback.html',fedbackdict)
    return render(request,'canteenapp/adlogin.html')

###########################################################################################################################################
#                                                   Home page
###########################################################################################################################################
def home(request):
    con = dbConnection()
    cursor = con.cursor()
    # -------------------------- STARTER ---------------------------------------------
    sql1 = "SELECT * from menutbl where dishCategory='VEG'"        
    cursor.execute(sql1)
    res1 = cursor.fetchall()
    result1 = list(res1)

    Dname1 = [i[1] for i in result1]
    Dprice1 = [i[2] for i in result1]
    Dabout1 = [i[3] for i in result1]
    Dimg1 = [i[4] for i in result1]
    Dcat1 = [i[5] for i in result1]

    flst1 = zip(Dname1,Dprice1,Dabout1,Dimg1,Dcat1)

    # -------------------------- main dish ---------------------------------------------
    sql2 = "SELECT * from menutbl where dishCategory='NON-VEG'"        
    cursor.execute(sql2)
    res2 = cursor.fetchall()
    result2 = list(res2)

    Dname2 = [i[1] for i in result2]
    Dprice2 = [i[2] for i in result2]
    Dabout2 = [i[3] for i in result2]
    Dimg2 = [i[4] for i in result2]
    Dcat2 = [i[5] for i in result2]

    flst2 = zip(Dname2,Dprice2,Dabout2,Dimg2,Dcat2)
    
    # -------------------------- STARTER ---------------------------------------------
    sql3 = "SELECT * from menutbl where dishCategory='BEVERAGES'"        
    cursor.execute(sql3)
    res3 = cursor.fetchall()
    result3 = list(res3)

    Dname3 = [i[1] for i in result3]
    Dprice3 = [i[2] for i in result3]
    Dabout3 = [i[3] for i in result3]
    Dimg3 = [i[4] for i in result3]
    Dcat3 = [i[5] for i in result3]

    flst3 = zip(Dname3,Dprice3,Dabout3,Dimg3,Dcat3)
    datadict = {"data1": zip(Dname1, Dprice1, Dabout1, Dimg1, Dcat1),
                "data2": zip(Dname2, Dprice2, Dabout2, Dimg2, Dcat2),
                "data3": zip(Dname3, Dprice3, Dabout3, Dimg3, Dcat3)}

    return render(request,'studentapp/home.html',datadict)

###########################################################################################################################################
#                                                   User Information
###########################################################################################################################################
def userinfo(request):
    if request.session.get('uname'):
        con = dbConnection()
        cursor = con.cursor()
        
        sql1 = "SELECT * FROM studentachertbl where role='teacher'"
        cursor.execute(sql1)
        res1 = cursor.fetchall()
        result1 = list(res1)
        
        Unames1 = [i[1] for i in result1]
        Uemail1 = [i[2] for i in result1]
        Umobile1 = [i[3] for i in result1]
        Uemproll1 = [i[5] for i in result1]
        Urole1 = [i[6] for i in result1]


        sql2 = "SELECT * FROM studentachertbl where role='student'"
        cursor.execute(sql2)
        res2 = cursor.fetchall()
        result2 = list(res2)
        
        Unames2 = [i[1] for i in result2]
        Uemail2 = [i[2] for i in result2]
        Umobile2 = [i[3] for i in result2]
        Uemproll2 = [i[5] for i in result2]
        Urole2 = [i[6] for i in result2]


        sql3 = "SELECT * FROM studentachertbl where role='visitor'"
        cursor.execute(sql3)
        res3 = cursor.fetchall()
        result3 = list(res3)
        
        Unames3 = [i[1] for i in result3]
        Uemail3 = [i[2] for i in result3]
        Umobile3 = [i[3] for i in result3]
        Uemproll3 = [i[5] for i in result3]
        Urole3 = [i[6] for i in result3]


        sql2 = "SELECT * FROM stafftbl"
        cursor.execute(sql2)
        res2 = cursor.fetchall()
        result2 = list(res2)
        
        staffFnames = [i[1] for i in result2]
        staffLnames = [i[2] for i in result2]
        staffmail = [i[3] for i in result2]
        staffmobile = [i[5] for i in result2]
        staffaddress = [i[6] for i in result2]
        staffcat = [i[7] for i in result2]


        fedbackdict = {
            "teacherData":zip(Unames1,Uemail1,Umobile1,Uemproll1,Urole1),
            "studentData":zip(Unames2,Uemail2,Umobile2,Uemproll2,Urole2),
            "visitorData":zip(Unames3,Uemail3,Umobile3,Urole3),
            "staffData":zip(staffFnames,staffLnames,staffmail,staffmobile,staffaddress,staffcat)
        }

        return render(request,'canteenapp/userdata.html',fedbackdict)
    return render(request,'canteenapp/adlogin.html')

###########################################################################################################################################
#                                                   User Information
###########################################################################################################################################
def userpament(request):
    if request.session.get('uname'):
        con = dbConnection()
        cursor = con.cursor()
        
        sql1 = "SELECT * FROM invoicetbl"
        cursor.execute(sql1)
        res1 = cursor.fetchall()
        result1 = list(res1)
        
        Unames1 = [i[1] for i in result1]
        invoicepath = [i[2] for i in result1]
        invoiceDate = [i[3] for i in result1]


        fedbackdict = {
            "InvoiceData":zip(Unames1,invoicepath,invoiceDate)
        }

        return render(request,'canteenapp/userpayment.html',fedbackdict)
    return render(request,'canteenapp/adlogin.html')














