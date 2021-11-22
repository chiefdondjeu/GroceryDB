from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db = SQLAlchemy(app)

def create_app():
	app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
	app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

	# db.init_app(app)

	from .links import links
	app.register_blueprint(links, url_prefix="/")

	from .models import User
	# create_database(app)

	login_manager = LoginManager()
	# redirect to url if user not logged in
	login_manager.login_view = 'links.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	return app
