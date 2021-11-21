from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db
from .models import User

links = Blueprint("links", __name__)

@links.route("/")
def home():
	return render_template("home.html", current_user=current_user)

@links.route("/dashboard")
@login_required
def dashboard():
	return render_template("dashboard.html", current_user=current_user)

@links.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form.get("username")
		password = request.form.get("password")

		user = User.query.filter_by(username=username).first()
		if user:
			if check_password_hash(user.password, password):
				flash(f"Login successfull. Last login {user.last_login.strftime('%a %b %d, %I:%M:%S %p')}", category="success")
				current_time = datetime.now()
				user.last_login = current_time
				db.session.commit()
				login_user(user, remember=True)
				return redirect(url_for('links.dashboard'))
			else:
				flash("Incorrect password or username.", category="error")
		else:
			flash(f"{username} does not exist!", category="error")
	return render_template("login.html", current_user=current_user)

@links.route('/logout')
@login_required
def logout():
	logout_user()
	flash("Logout successfull.", category="success")
	return redirect(url_for('links.login'))

@links.route("/createadmin")
def create_admin():
	admin = User(username='admin', password=generate_password_hash('admin', method="sha256"))
	db.session.add(admin)
	db.session.commit()
	return redirect(url_for('links.login'))
