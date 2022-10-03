import imp
from flask_mail import Message
from flask import current_app
# import app
from api import mail

def send_conf_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_USERNAME']
    )
    mail.send(msg)