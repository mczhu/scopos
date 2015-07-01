from flask import Flask
from Jobs import Jobs

with open("flask_key") as f:
    lines = f.read().splitlines() 
    flask_key = lines[0]

# DEBUG = True

class MyServer(Flask):

    def __init__(self, *args, **kwargs):
            super(MyServer, self).__init__(*args, **kwargs)

            self.jobs = Jobs()

app = MyServer(__name__)
app.secret_key = flask_key

# app = Flask(__name__)
# app.config.from_object(__name__)

from app import views
