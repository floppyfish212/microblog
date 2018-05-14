from flask import Flask
# from flask library import Flask object
from config import Config
# from config.py import Config object
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#...
login = LoginManager(app)
login.login_view = 'login'    # Assign login.html to login.login_view
                              # force users to login before they can view parts of the app
#...

from app import routes, models
# from app directory import routes.py

