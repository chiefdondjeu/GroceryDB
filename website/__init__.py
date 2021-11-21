from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path, getenv
from dotenv import load_dotenv

load_dotenv()

SQL_LINK = getenv("SQL_LINK")
db = SQLAlchemy()

def create_app():
	app = Flask(__name__)
	app.config["SECRET_KEY"] = "secret"
	app.config["SQLALCHEMY_DATABASE_URI"] = SQL_LINK

	db.init_app(app)

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

# only run once
def create_database(app):
	db.create_all(app=app)
	print("Database created!")
