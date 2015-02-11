from threading import Thread
from flask.ext.mail import Message
from flask import render_template
from app import mail
from app import app

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)

def story_notification(target):
    send_email("Iemand heeft je een verhaal verteld...",
               "ketting.vertelling@gmail.com",
               [target.email, "fbkarsdorp@gmail.com"],
               render_template("target_email.txt", user=target),
               render_template("target_email.html", user=target))