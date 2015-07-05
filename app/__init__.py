from flask import Flask
from Jobs import Jobs

with open("flask_key") as f:
    lines = f.read().splitlines() 
    flask_key = lines[0]

class MyServer(Flask):

    def __init__(self, *args, **kwargs):
            super(MyServer, self).__init__(*args, **kwargs)
            self.jobs = Jobs()

app = MyServer(__name__)
app.secret_key = flask_key

with open("gmail_usr") as f:
    gmail_name = f.read()

ADMINS = [gmail_name + '@gmail.com']

with open("yahoo_usr") as f:
    usr_name = f.read()

with open("yahoo_psw") as f:
    psw = f.read()

fromAddr = usr_name + '@yahoo.com'

smtpServer = 'smtp.mail.yahoo.com'
smtpPort = 587

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler((smtpServer, smtpPort),
                               fromAddr,
                               ADMINS, 'YourApplication Failed',
                               credentials=(usr_name, psw),
                               secure=())
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


# app = Flask(__name__)
# app.config.from_object(__name__)

from app import views
