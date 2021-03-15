from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail


# 异步发送邮件
def send_async_email(app, msg):
    # 必须在程序上下文中才能发送邮件，新建的线程没有，因此需要手动创建
    with app.app_context():
        # 发送邮件
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body,
               attachments=None, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email,
            args=(current_app._get_current_object(), msg)).start()

