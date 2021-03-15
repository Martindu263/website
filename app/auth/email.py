from flask import render_template, current_app
from flask_babel import _
from app.email import send_email


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('[Microblog] Reset Your Password'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

def send_confirm_email(user):
    token = user.generate_confirmation_token()
    send_email(_('[Microblog] 激活你的账号'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('auth/email/confirm.txt',
                                         user=user, token=token),
               html_body=render_template('auth/email/confirm.html',
                                         user=user, token=token))
