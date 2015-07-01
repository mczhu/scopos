from flask import Flask
# SECRET_KEY = 'development key mczhu'
# DEBUG = True

app = Flask(__name__)
app.config['DEBUG'] = False
# app.config.from_object(__name__)

from app import views
