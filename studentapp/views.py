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

    empnos = request.session['empno'] #usrempno

    flst3 = zip(Dname3,Dprice3,Dabout3,Dimg3,Dcat3)
    datadict = {"data1": zip(Dname1, Dprice1, Dabout1, Dimg1, Dcat1),
                "data2": zip(Dname2, Dprice2, Dabout2, Dimg2, Dcat2),
                "data3": zip(Dname3, Dprice3, Dabout3, Dimg3, Dcat3),
                "usrempno":empnos}

    return render(request,'studentapp/home.html',datadict)

###########################################################################################################################################
#                                                   Collage Student Login and Register
###########################################################################################################################################
def studlogin(request):
    if request.method == 'POST':
        email = request.POST['rolempNO']
        password = request.POST['password'] 
        urole = "student"

        print(email,password)

        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM studenTachertbl WHERE employeerollno = %s AND upass = %s AND role=%s', (email, password, urole))
        result = cursor.fetchone()
        print("result")
        print(result)
        if result_count>0:
            print("len of result")
            request.session['uname'] = result[1]
            request.session ['userid'] = result[0]
            request.session ['uemail'] = result[2]
            request.session ['empno'] = result[5]

            # request.session.get('uname')
            return redirect('studindex')
        else:
            return render(request,'studentapp/studlogin.html')
    return render(request,'studentapp/studlogin.html')

def studregister(request):
    if request.method == 'POST':
        #Parse form data    
        # print("hii register")
        Uname = request.POST['Name']
        Uemails = request.POST['uemail']
        Upasswords = request.POST['Upass']
        Umobno = request.POST['mobileno']
        Uadd = request.POST['Uaddres']
        Urol = "student"

        print(Uname,Uemails,Upasswords,Umobno,Uadd,Urol)

        try: 
            con = dbConnection()
            cursor = con.cursor()
            sql1 = "INSERT INTO studenTachertbl (Uname, umail, mobileno, upass, employeerollno, role) VALUES (%s, %s, %s, %s, %s, %s)"
            val1 = (Uname,Uemails,Umobno,Upasswords,Uadd,Urol)
            cursor.execute(sql1, val1)
            print("query 1 submitted")
            con.commit()
            FinalMsg = "Congrats! Your account registerd successfully!"
        except:
            con.rollback()
            msg = "Database Error occured"
            print(msg)
            return render(request,'studentapp/studlogin.html')
        finally:
            dbClose()
        return render(request,'studentapp/studlogin.html')
    return render(request,'studentapp/studregister.html')

def logout(request):
    del request.session['uname']
    del request.session['userid']
    return redirect('home')


def studindex(request):
    if request.session.get('uname'):
        con = dbConnection()
        cursor = con.cursor()
        usrname = request.session['uname']
        empnos = request.session['empno']
        sql1 = "SELECT * FROM orderfoodtbl where Uname=%s and Statuss='ordering'"
        val1 = (usrname)
        cursor.execute(sql1,val1)
        res = cursor.fetchall()

        cartdict = {"cartcount":len(res),"usrempno":empnos}
        return render(request,'studentapp/studindex.html',cartdict)
    return render(request,'studentapp/studlogin.html')


def userprofile(request):
    if request.session.get('uname'):
        con = dbConnection()
        cursor = con.cursor()
        usrname = request.session['uname']
        empnos = request.session['empno']
        sql1 = "SELECT * FROM studentachertbl where Uname=%s and employeerollno=%s"
        val1 = (usrname,empnos)
        cursor.execute(sql1,val1)
        res = cursor.fetchall()
        results = list(res)

        usrnames = [i[1] for i in results]
        usrmail = [i[2] for i in results]
        usermobile = [i[3] for i in results]
        usrempId = [i[5] for i in results]
        empnos = request.session['empno'] #usrempno


        cartdict = {
            "cartcount":len(res),"usrempno":empnos,
            "usrnames":usrnames[0],
            "usrmail":usrmail[0],
            "usermobile":usermobile[0],
            "usrempId":usrempId[0]
            }
        
        if request.method == 'POST':
            UName = request.POST['usrname']
            Umobilno = request.POST['mobileno']
            Uemail = request.POST['emailid']
            Uempno = request.POST['empno']

            con = dbConnection()
            cursor = con.cursor()
            sql1 = "UPDATE studentachertbl SET umail=%s, mobileno=%s where Uname=%s and employeerollno=%s" 
            val1 = (Uemail,Umobilno,UName,Uempno)       
            cursor.execute(sql1,val1)
            con.commit()
            messages.success(request, 'Profile Updated Successfully!')

            return redirect("userprofile")
        
        return render(request,'studentapp/studprodile.html',cartdict)
    return render(request,'studentapp/studlogin.html')

###########################################################################################################################################
#                                                   Menu
###########################################################################################################################################

def menu(request):
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



        usrname = request.session['uname']
        sql1 = "SELECT * FROM orderfoodtbl where Uname=%s and Statuss='ordering'"
        val1 = (usrname)
        cursor.execute(sql1,val1)
        res = cursor.fetchall()

        empnos = request.session['empno'] #usrempno

        datadict = {"data1": zip(Dname1, Dprice1, Dabout1, Dimg1, Dcat1),
                    "data2": zip(Dname2, Dprice2, Dabout2, Dimg2, Dcat2),
                    "data3": zip(Dname3, Dprice3, Dabout3, Dimg3, Dcat3),
                    "data4": zip(Dname4, Dprice4, Dabout4, Dimg4, Dcat4),
                    "cartcount":len(res),
                    "usrempno":empnos}

        return render(request,'studentapp/menu.html',datadict)
    return render(request,'studentapp/studlogin.html')

###########################################################################################################################################
#                                                   Menu
###########################################################################################################################################

def addtocart(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            #Parse form data    
            # print("hii register")
            dishName = request.POST['addish']
            dishPrice = request.POST['pricedish']
            dishquantity = request.POST['Dquantity']
            dishinfo = request.POST['aboutdish']
            dishimg = request.POST['imgdish']

            usrname = request.session['uname']


            print(usrname,dishName,dishPrice,dishinfo,dishimg,dishquantity)

            con = dbConnection()
            cursor = con.cursor()
            sql1 = "INSERT INTO orderFoodtbl(Uname,dishName,dishPrice,dishinfo,dishimgs,dishQuantity,Statuss) VALUES (%s,%s,%s,%s,%s,%s,%s)" 
            val1 = (usrname,dishName,dishPrice,dishinfo,dishimg,dishquantity,"ordering")       
            cursor.execute(sql1,val1)
            con.commit()
            messages.success(request, 'Added to cart!')

            return redirect("menu")
        return render(request,'studentapp/menu.html')
    return render(request,'studentapp/studlogin.html')

###########################################################################################################################################
#                                                   Add and Remove from Cart
###########################################################################################################################################
def cartdata(request):
    if request.session.get('uname'):
        con = dbConnection()
        cursor = con.cursor()
        usrname = request.session['uname']
        sql1 = "SELECT * FROM orderfoodtbl where Uname=%s and Statuss='ordering'"
        val1 = (usrname)
        cursor.execute(sql1,val1)
        res = cursor.fetchall()
        result = list(res)

        unames = [i[1] for i in result]
        dishName = [i[2] for i in result]
        dishPrice = [i[3] for i in result]
        dishinfo = [i[4] for i in result]
        dishimgs = [i[5] for i in result]
        dishQuantity = [i[6] for i in result]
        totalPrice = [int(i)*int(j) for i,j in zip(dishQuantity,dishPrice)]
        for i,j in zip(dishQuantity,dishPrice):
            print(int(i),int(j))
            a = int(i)*int(j)
            print(a)
        
        empnos = request.session['empno'] #usrempno


        cartdict = {"cartcount":len(res),
                    "finalcost":sum(totalPrice),
                    "cartlst":zip(dishName,dishPrice,dishinfo,dishimgs,dishQuantity,totalPrice),
                    "usrempno":empnos}
        return render(request,'studentapp/cart.html',cartdict)
    return render(request,'studentapp/studlogin.html')

def removecartdata(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            removedish = request.POST['removedish']

            con = dbConnection()
            cursor = con.cursor()
            usrname = request.session['uname']
            sql1 = "DELETE FROM orderfoodtbl where Uname=%s and dishName=%s"
            val1 = (usrname,removedish)
            cursor.execute(sql1,val1)
            con.commit()

            return redirect('cartdata')
        return render(request,'studentapp/cart.html')
    return render(request,'studentapp/studlogin.html')
###########################################################################################################################################
#                                                   Checkout
###########################################################################################################################################

def checkout(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            #Parse form data    
            # print("hii register")
            pmodes = request.POST['pmode']
            dishPrice = request.POST['finalcost']

            con = dbConnection()
            cursor = con.cursor()
            usrname = request.session['uname']
            sql1 = "SELECT * FROM orderfoodtbl where Uname=%s and Statuss='ordering'"
            val1 = (usrname)
            cursor.execute(sql1,val1)
            res = cursor.fetchall()

            empnos = request.session['empno'] #usrempno

            if pmodes=="Card":
                cartdict = {"cartcount":len(res),
                            "dishPrice":dishPrice,
                            "usrempno":empnos}
                return render(request,'studentapp/checkout1.html',cartdict)
            else:
                cartdict = {"cartcount":len(res),
                                "dishPrice":dishPrice,
                                "usrempno":empnos}
                return render(request,'studentapp/checkout2.html',cartdict)
        return render(request,'studentapp/checkout.html')
    return render(request,'studentapp/studlogin.html')

###########################################################################################################################################
#                                                   Place Order
###########################################################################################################################################
import os
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
import random
import shutil
from datetime import date
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','wav','mp3'}
from django.core.files.storage import default_storage,FileSystemStorage
MEDIA_URL = '/media/Invoices/'
from django.conf import settings



import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def sendemailtouser(usermail,cmpimg):   
    fromaddr = "modern.project2023@gmail.com"
    toaddr = usermail
   
    #instance of MIMEMultipart 
    msg = MIMEMultipart() 
  
    # storing the senders email address   
    msg['From'] = fromaddr 
  
    # storing the receivers email address  
    msg['To'] = toaddr 
  
    # storing the subject  
    msg['Subject'] = "order invoice."
  
    # string to store the body of the mail 
    body = "Hello user! your oder has been placed successfully! Please find attached Invoice in mail. Thank You!"
  
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
  
    # open the file to be sent  
    filename = cmpimg
    attachment = open(cmpimg, "rb") 
  
    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 
  
    # To change the payload into encoded form 
    p.set_payload((attachment).read()) 
  
    # encode into base64 
    encoders.encode_base64(p) 
   
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
    # attach the instance 'p' to instance 'msg' 
    msg.attach(p) 
  
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

def placeorder(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            Fname = request.POST['Fname']
            Lname = request.POST['Lname']
            phoneno = request.POST['phoneno']
            Uemail = request.POST['Uemail']

            # con = dbConnection()
            # cursor = con.cursor()
            # usrname = request.session['uname']
            # sql1 = "SELECT * FROM orderfoodtbl where Uname=%s and Statuss='ordering'"
            # val1 = (usrname)
            # cursor.execute(sql1,val1)
            
            
            con = dbConnection()
            cursor = con.cursor()
            usrname = request.session['uname']
            sql1 = "SELECT * FROM orderfoodtbl where Uname=%s and Statuss='ordering'"
            val1 = (usrname)
            cursor.execute(sql1,val1)
            res = cursor.fetchall()
            result = list(res)

            dishname = [i[2] for i in result]       #dish name
            dishPrice = [i[3] for i in result]      #price per piece
            dishQuantity = [i[6] for i in result]   #units

            flst = zip(dishQuantity,dishPrice,dishname)

            os.environ["INVOICE_LANG"] = "en"

            client = Client(usrname)

            provider = Provider('Modern Canteen', bank_account='6454-6361-217273', bank_code='2023')

            creator = Creator('Modern Canteen')

            invoice = Invoice(client, provider, creator)
            #items(units,price per piece,dish name)

            for dishQuantity,dishPrice,dishname in flst:
                invoice.add_item(Item(int(dishQuantity), int(dishPrice), description=dishname))

            invoice.currency = "Rs."

            # invoice.number = "10393069"
            invoicenumber = str(random.randint(11111111,99999999))
            invoice.number = invoicenumber

            docu = SimpleInvoice(invoice)

            docname = str(usrname)+"_"+str(invoicenumber)
            

            docu.gen(os.path.join(settings.INVOICE_PATH, docname+"_invoice_.pdf"), generate_qr_code=False)
            print("file saved4")

            finaldocname = os.path.join(settings.INVOICE_PATH, docname+"_invoice_.pdf")
            print("file saved6")

            usremail = request.session['uemail']
            sendemailtouser(usremail,finaldocname)
            today = date.today()


            con = dbConnection()
            cursor = con.cursor()
            usrname = request.session['uname']
            finaldocname = "media/Invoices/"+docname+"_invoice_.pdf"
            sql2 = "insert into invoicetbl(Uname,invoicename,invoiceDate)values(%s,%s,%s)"
            val2 = (usrname,finaldocname,str(today))
            cursor.execute(sql2,val2)

            sql2 = "UPDATE orderfoodtbl SET Statuss='ordered' where Uname=%s"
            val2 = (usrname)
            cursor.execute(sql2,val2)
            con.commit()

            messages.success(request, 'Your order has been placed successfully!')
            return redirect("studindex")
        return render(request,'studentapp/checkout.html')
    return render(request,'studentapp/studlogin.html')

###########################################################################################################################################
#                                                   Add and Remove from Cart
###########################################################################################################################################
def invoicehistory(request):
    if request.session.get('uname'):
        con = dbConnection()
        cursor = con.cursor()
        usrname = request.session['uname']
        sql1 = "SELECT * FROM invoicetbl where Uname=%s"
        val1 = (usrname)
        cursor.execute(sql1,val1)
        res = cursor.fetchall()
        result = list(res)
        print()
        print("invoice result")
        print(result)
        print()

        pdfname = [i[2] for i in result]
        pdfdates = [i[3] for i in result]

        empnos = request.session['empno'] #usrempno

        invoicedate = {
            "invoicedata" : zip(pdfname,pdfdates),
            "usrempno":empnos
        }


        return render(request,"studentapp/invoice.html",invoicedate)
    return render(request,'studentapp/studlogin.html')
    
###########################################################################################################################################
#                                                   Add and Remove from Cart
###########################################################################################################################################
def userfeedback(request):
    if request.session.get('uname'):

        empnos = request.session['empno'] #usrempno
        usrdict = {
                "usrempno":empnos
            }
        
        if request.method == 'POST':
            usrfeedback = request.POST['feedback']

            con = dbConnection()
            cursor = con.cursor()
            usrname = request.session['uname']
            sql1 = "INSERT INTO userfeedback(Uname,feedbacks)VALUES(%s,%s)"
            val1 = (usrname,usrfeedback)
            cursor.execute(sql1,val1)
            con.commit()
            
            messages.success(request, 'The feedback has been submitted successfully!')


            empnos = request.session['empno'] #usrempno
            usrdict = {
                    "usrempno":empnos
                }
            return render(request,"studentapp/studfeedback.html",usrdict)
        return render(request,"studentapp/studfeedback.html",usrdict)
    return render(request,'studentapp/studlogin.html')
###########################################################################################################################################
#                                                   Send OTP
###########################################################################################################################################
def sendemailtouser2(usermail,otp):   
    fromaddr = "modern.project2023@gmail.com"
    toaddr = usermail
   
    #instance of MIMEMultipart 
    msg = MIMEMultipart() 
  
    # storing the senders email address   
    msg['From'] = fromaddr 
  
    # storing the receivers email address  
    msg['To'] = toaddr 
  
    # storing the subject  
    msg['Subject'] = "OTP Verification"
  
    # string to store the body of the mail 
    body = "Hello User! Your forget password OTP is: "+str(otp)
  
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


def sendotp(request):
    if request.method == 'POST':
        usrfeedback = request.POST['otpemail']

        print("usrfeedback")
        print(usrfeedback)

        randmotp = str(random.randint(111111,999999))
        sendemailtouser2(usrfeedback,randmotp)

        con = dbConnection()
        cursor = con.cursor()
        sql1 = "UPDATE studentachertbl SET otpval=%s where umail=%s"
        val1 = (randmotp,usrfeedback)
        cursor.execute(sql1,val1)
        con.commit()
        messages.success(request, 'OTP send Successfully!')

        otpdicts = {
            "usrmailid":usrfeedback
        }
        return render(request,"studentapp/setpassword.html",otpdicts)
    return render(request,"studentapp/studsendotp.html")

###########################################################################################################################################
#                                                   SET Password
###########################################################################################################################################
def setpassword(request):
    if request.method == 'POST':
        finalusrotp = request.POST['finalotp']
        passupdate = request.POST['finalpass']
        usremailscheck = request.POST['usremails']

        con = dbConnection()
        cursor = con.cursor()
        sql1 = "SELECT * from studentachertbl where umail=%s and otpval=%s"
        val1 = (usremailscheck,finalusrotp)
        curs_val = cursor.execute(sql1,val1)

        if curs_val>0:
            sql1 = "UPDATE studentachertbl SET upass=%s where umail=%s and otpval=%s"
            val1 = (passupdate, usremailscheck, finalusrotp)
            cursor.execute(sql1,val1)
            con.commit()
            messages.success(request, 'Your password has been updated successfully!!')
            redirect('studlogin')
        else:
            messages.error(request, 'Please enter correct OTP')
            redirect('setpassword')

    return render(request,"studentapp/setpassword.html")


    













