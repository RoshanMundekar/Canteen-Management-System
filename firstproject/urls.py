"""
URL configuration for firstproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
# from . import views
from django.conf.urls.static import static
from django.conf import settings

from studentapp import views as student_views
from canteenapp import views as canteen_views
from canteenStaff import views as staff_views
from visitorsapp import views as visitor_views
from teacherapp import views as teacher_views


urlpatterns = [
    path("studlogin", student_views.studlogin, name='studlogin'),
    path("studregister", student_views.studregister, name='studregister'),
    path("logout", canteen_views.logout, name='logout'),
    path("studindex", student_views.studindex, name='studindex'),
    path("menu", student_views.menu, name='menu'),
    path("addtocart", student_views.addtocart, name='addtocart'),
    path("removecartdata", student_views.removecartdata, name='removecartdata'),
    path("cartdata", student_views.cartdata, name='cartdata'),
    path("checkout", student_views.checkout, name='checkout'),
    path("placeorder", student_views.placeorder, name='placeorder'),
    path("invoicehistory", student_views.invoicehistory, name='invoicehistory'),
    path("userfeedback", student_views.userfeedback, name='userfeedback'),
    path("userprofile", student_views.userprofile, name='userprofile'),
    path("sendotp", student_views.sendotp, name='sendotp'),
    path("setpassword", student_views.setpassword, name='setpassword'),

    path("", canteen_views.home, name='home'),
    path("adlogin", canteen_views.adlogin, name='adlogin'),
    path("adregister", canteen_views.adregister, name='adregister'),
    path("adindex", canteen_views.adindex, name='adindex'),
    path("admenu", canteen_views.admenu, name='admenu'),
    path("admenu2", canteen_views.admenu2, name='admenu2'),
    path("combomenu", canteen_views.combomenu, name='combomenu'),
    path("addstaff", canteen_views.addstaff, name='addstaff'),
    path("addstaff2", canteen_views.addstaff2, name='addstaff2'),
    path("deletestaff", canteen_views.deletestaff, name='deletestaff'),
    path("viewfeedback", canteen_views.viewfeedback, name='viewfeedback'),
    path("userinfo", canteen_views.userinfo, name='userinfo'),
    path("userpament", canteen_views.userpament, name='userpament'),
    path("logout", canteen_views.logout, name='logout'),

    path("stafflogin", staff_views.stafflogin, name='stafflogin'),
    path("logout", staff_views.logout, name='logout'),
    path("staffindex", staff_views.staffindex, name='staffindex'),
    path("takeorder", staff_views.takeorder, name='takeorder'),
    path("orderaccept", staff_views.orderaccept, name='orderaccept'),

    path("vistlogin", visitor_views.vistlogin, name='vistlogin'),
    path("visitregister", visitor_views.visitregister, name='visitregister'),
    path("logout", visitor_views.logout, name='logout'),
    path("visitorindex", visitor_views.visitorindex, name='visitorindex'),
    path("visitormenu", visitor_views.visitormenu, name='visitormenu'),
    path("visitoraddtocart", visitor_views.visitoraddtocart, name='visitoraddtocart'),
    path("visitorremovecartdata", visitor_views.visitorremovecartdata, name='visitorremovecartdata'),
    path("visitorcartdata", visitor_views.visitorcartdata, name='visitorcartdata'),
    path("visitorcheckout", visitor_views.visitorcheckout, name='visitorcheckout'),
    path("visitorplaceorder", visitor_views.visitorplaceorder, name='visitorplaceorder'),
    path("visitorinvoicehistory", visitor_views.visitorinvoicehistory, name='visitorinvoicehistory'),
    path("visitorfeedback", visitor_views.visitorfeedback, name='visitorfeedback'),
    path("sendotp", visitor_views.sendotp, name='sendotp'),
    path("setpassword", visitor_views.setpassword, name='setpassword'),
    path("visitorprofile", visitor_views.visitorprofile, name='visitorprofile'),

    path("teacherlogin", teacher_views.teacherlogin, name='teacherlogin'),
    path("teacherregister", teacher_views.teacherregister, name='teacherregister'),
    path("logout", teacher_views.logout, name='logout'),
    path("teaherindex", teacher_views.teaherindex, name='teaherindex'),
    path("teachermenu", teacher_views.teachermenu, name='teachermenu'),
    path("teacheraddtocart", teacher_views.teacheraddtocart, name='teacheraddtocart'),
    path("teacherremovecartdata", teacher_views.teacherremovecartdata, name='teacherremovecartdata'),
    path("teachercartdata", teacher_views.teachercartdata, name='teachercartdata'),
    path("teachercheckout", teacher_views.teachercheckout, name='teachercheckout'),
    path("teacherplaceorder", teacher_views.teacherplaceorder, name='teacherplaceorder'),
    path("teacherinvoicehistory", teacher_views.teacherinvoicehistory, name='teacherinvoicehistory'),
    path("teacherfeedback", teacher_views.teacherfeedback, name='teacherfeedback'),
    path("sendotp", teacher_views.sendotp, name='sendotp'),
    path("setpassword", teacher_views.setpassword, name='setpassword'),
    path("teacherprofile", teacher_views.teacherprofile, name='teacherprofile'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
