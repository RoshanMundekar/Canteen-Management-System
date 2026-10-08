from django.http import HttpResponse
from django.shortcuts import redirect,render
import pymysql



def dbConnection():
    try:
        connection = pymysql.connect(host="localhost", user="root", password="root", database="object_detect",charset='utf8')
        return connection
    except:
        print("Something went wrong in database Connection")

def dbClose():
    try:
        dbConnection().close()
    except:
        print("Something went wrong in Close DB Connection")

