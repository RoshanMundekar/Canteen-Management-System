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
    path("vistlogin", views.vistlogin, name='vistlogin'),
    path("visitregister", views.visitregister, name='visitregister'),
    path("logout", views.logout, name='logout'),
    path("visitorindex", views.visitorindex, name='visitorindex'),
    path("visitormenu", views.visitormenu, name='visitormenu'),
    path("visitoraddtocart", views.visitoraddtocart, name='visitoraddtocart'),
    path("visitorremovecartdata", views.visitorremovecartdata, name='visitorremovecartdata'),
    path("visitorcartdata", views.visitorcartdata, name='visitorcartdata'),
    path("visitorcheckout", views.visitorcheckout, name='visitorcheckout'),
    path("visitorplaceorder", views.visitorplaceorder, name='visitorplaceorder'),
    path("visitorinvoicehistory", views.visitorinvoicehistory, name='visitorinvoicehistory'),
    path("visitorfeedback", views.visitorfeedback, name='visitorfeedback'),
    path("sendotp", views.sendotp, name='sendotp'),
    path("setpassword", views.setpassword, name='setpassword'),
    path("visitorprofile", views.visitorprofile, name='visitorprofile'),







] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
