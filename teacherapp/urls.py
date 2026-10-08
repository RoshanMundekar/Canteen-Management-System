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
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("teacherlogin", views.teacherlogin, name='teacherlogin'),
    path("teacherregister", views.teacherregister, name='teacherregister'),
    path("logout", views.logout, name='logout'),
    path("teaherindex", views.teaherindex, name='teaherindex'),
    path("teachermenu", views.teachermenu, name='teachermenu'),
    path("teacheraddtocart", views.teacheraddtocart, name='teacheraddtocart'),
    path("teacherremovecartdata", views.teacherremovecartdata, name='teacherremovecartdata'),
    path("teachercartdata", views.teachercartdata, name='teachercartdata'),
    path("teachercheckout", views.teachercheckout, name='teachercheckout'),
    path("teacherplaceorder", views.teacherplaceorder, name='teacherplaceorder'),
    path("teacherinvoicehistory", views.teacherinvoicehistory, name='teacherinvoicehistory'),
    path("teacherfeedback", views.teacherfeedback, name='teacherfeedback'),
    path("sendotp", views.sendotp, name='sendotp'),
    path("setpassword", views.setpassword, name='setpassword'),
    path("teacherprofile", views.teacherprofile, name='teacherprofile'),







] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
