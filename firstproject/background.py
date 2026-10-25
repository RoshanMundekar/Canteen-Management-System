"""Run slow side effects (sending email over SMTP) off the request thread."""
import functools
import threading
import traceback


def in_background(func):
    """Make calls to `func` return immediately; it runs on a daemon thread.

    Errors are printed to the server console instead of reaching the view,
    so a slow or failing mail server no longer delays or breaks the page.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        def run():
            try:
                func(*args, **kwargs)
            except Exception:
                print("Background task %s failed:" % func.__name__)
                traceback.print_exc()
        threading.Thread(target=run, daemon=True).start()
    return wrapper
