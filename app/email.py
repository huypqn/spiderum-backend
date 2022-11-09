from flask import render_template
from flask_mail import Message
from app import app, mail
from app.services import get_register_token

def send_email(subject, sender, recipients, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    mail.send(msg)

def send_register_email(email):
    token = get_register_token(email)
    send_email(
        'Xác nhận địa chỉ email cho tài khoản của bạn',
        sender=app.config['NOREPLY'][0],
        recipients=[email],
        html_body=render_template('email/register.html', token=token)
    )