from flask import Flask
# SECRET_KEY = 'development key mczhu'
# DEBUG = True

# class MyServer(Flask):

#     def __init__(self, *args, **kwargs):
#             super(MyServer, self).__init__(*args, **kwargs)

#             #instanciate your variables here
#             self.messages = []

# app = MyServer(__name__)
app = Flask(__name__)
# app.config.from_object(__name__)

from app import views
