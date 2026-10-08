from django.http import HttpResponse
from django.shortcuts import redirect,render
import pymysql



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
#                                                   Collage Student Login and Register
###########################################################################################################################################
def stafflogin(request):
    if request.method == 'POST':
        email = request.POST['Email']
        password = request.POST['password']

        print(email,password)

        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM stafftbl WHERE Smail = %s AND Spass = %s', (email, password))
        result = cursor.fetchone()
        print("result")
        print(result)
        if result_count>0:
            print("len of result")
            request.session['uname'] = result[1]
            request.session ['userid'] = result[0]
            request.session ['uemail'] = result[2]

            # request.session.get('uname')
            return redirect('staffindex')
        else:
            return render(request,'canteenStaff/stafflogin.html')
    return render(request,'canteenStaff/stafflogin.html')

def logout(request):
    del request.session['uname']
    del request.session['userid']
    return redirect('adlogin')


def staffindex(request):
    if request.session.get('uname'):
        return render(request,'canteenStaff/staffindex.html')
    return render(request,'canteenStaff/stafflogin.html')

###########################################################################################################################################
#                                                   View Oder
###########################################################################################################################################
def takeorder(request):
    if request.session.get('uname'):
        con = dbConnection()
        cursor = con.cursor()
        # -------------------------- STARTER ---------------------------------------------
        sql1 = "SELECT * from orderfoodtbl where Statuss='ordered'"        
        cursor.execute(sql1)
        res1 = cursor.fetchall()
        result1 = list(res1)

        username = [i[1] for i in result1]
        dishname = [i[2] for i in result1]
        dishprice = [i[3] for i in result1]
        dishinfo = [i[4] for i in result1]
        dishimage = [i[5] for i in result1]
        dishquantity = [i[6] for i in result1]

        flst1 = zip(username,dishname,dishprice,dishinfo,dishimage,dishquantity)

        datadict = {"data1": zip(username,dishname,dishprice,dishinfo,dishimage,dishquantity)}

        return render(request,'canteenStaff/orders.html',datadict)
    return render(request,'canteenStaff/stafflogin.html')

###########################################################################################################################################
#                                                   Order Accept
###########################################################################################################################################
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def sendemailtouser(usermail,ordertime):   
    fromaddr = "modern.project2023@gmail.com"
    toaddr = usermail
   
    #instance of MIMEMultipart 
    msg = MIMEMultipart() 
  
    # storing the senders email address   
    msg['From'] = fromaddr 
  
    # storing the receivers email address  
    msg['To'] = toaddr 
  
    # storing the subject  
    msg['Subject'] = "order Placed"
  
    # string to store the body of the mail 
    body = "Hello user! your oder has been placed successfully! We will deliver order within "+str(ordertime)
  
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
from django.contrib import messages

def orderaccept(request):
    if request.session.get('uname'):
        if request.method == 'POST':
            usrname = request.POST['usrname']
            dishname = request.POST['dishname']
            exptimes = request.POST['exptime']
            

            # usrname = request.session['uname']

            print(usrname,dishname,exptimes)

            con = dbConnection()
            cursor = con.cursor()
            sql1 = "DELETE from orderfoodtbl where Uname=%s" 
            val1 = (usrname)       
            cursor.execute(sql1,val1)
            con.commit()

            sql2 = "select umail from studentachertbl where Uname=%s"
            val2 = (usrname)
            cursor.execute(sql2,val2)
            res = cursor.fetchone()

            sendemailtouser(res[0],str(exptimes))

            messages.success(request, usrname+"'s Order accepted successfully!")

            return redirect("takeorder")
        return render(request,'canteenStaff/orders.html')
    return render(request,'canteenStaff/stafflogin.html')
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
#                                                   Add and Remove from Cart
###########################################################################################################################################
def cartdata(request):
    if request.session.get('uname'):
        con = dbConnection()
        cursor = con.cursor()
        usrname = request.session['uname']
        sql1 = "SELECT * FROM orderfoodtbl where Uname=%s"
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


        cartdict = {"cartcount":len(res),
                    "finalcost":sum(totalPrice),
                    "cartlst":zip(dishName,dishPrice,dishinfo,dishimgs,dishQuantity,totalPrice)}
        return render(request,'canteenStaff/cart.html',cartdict)
    return render(request,'canteenStaff/stafflogin.html')

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
        return render(request,'canteenStaff/cart.html')
    return render(request,'canteenStaff/stafflogin.html')
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
            sql1 = "SELECT * FROM orderfoodtbl where Uname=%s"
            val1 = (usrname)
            cursor.execute(sql1,val1)
            res = cursor.fetchall()

            if pmodes=="Card":
                cartdict = {"cartcount":len(res),
                            "dishPrice":dishPrice}
                return render(request,'canteenStaff/checkout1.html',cartdict)
            else:
                cartdict = {"cartcount":len(res),
                                "dishPrice":dishPrice}
                return render(request,'canteenStaff/checkout2.html',cartdict)
        return render(request,'canteenStaff/checkout.html')
    return render(request,'canteenStaff/stafflogin.html')




