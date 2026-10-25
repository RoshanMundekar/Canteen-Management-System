"""Shared MySQL connection helpers used by every app's views.

One connection is opened per request thread and reused by every
dbConnection() call in that request, then closed when the request
finishes. Previously each call opened a brand-new connection (and
dbClose() opened yet another one just to close it), so a single page
could open several connections and none were ever closed.
"""
import threading

import pymysql
from django.core.signals import request_finished

DB_SETTINGS = {
    # 127.0.0.1 rather than "localhost": on Windows "localhost" resolves to
    # IPv6 ::1 first, and when MySQL only listens on IPv4 each connect stalls
    # for ~1-2 seconds before falling back.
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "canteendb",
    "charset": "utf8",
    "connect_timeout": 5,
}

_local = threading.local()


def dbConnection():
    con = getattr(_local, "connection", None)
    if con is not None:
        try:
            con.ping(reconnect=True)
            return con
        except Exception:
            _local.connection = None
    # Let a failed connect raise: returning None only moved the crash to the
    # caller's next line with a less helpful "NoneType has no attribute" error.
    con = pymysql.connect(**DB_SETTINGS)
    _local.connection = con
    return con


def dbClose(**kwargs):
    con = getattr(_local, "connection", None)
    _local.connection = None
    if con is not None:
        try:
            con.close()
        except Exception:
            pass


# Close the request's connection once the response has been sent.
request_finished.connect(dbClose, dispatch_uid="canteen_db_close")
