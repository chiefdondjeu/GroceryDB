from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

links = Blueprint("links", __name__)

@links.route("/")
def home():
	return render_template("home.html", user=current_user)

@links.route("/admin")
@login_required
def admin():
	return render_template("admin.html", user=current_user)

@links.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form.get("username")
		password = request.form.get("password")

		user = User.query.filter_by(username=username).first()
		if user:
			if check_password_hash(user.password, password):
				flash("Login successfull.", category="success")
				login_user(user, remember=True)
				return redirect(url_for('links.admin'))
			else:
				flash("Incorrect password or username.", category="error")
		else:
			flash(f"{username} does not exist!", category="error")
	return render_template("login.html", user=current_user)

@links.route('/logout')
@login_required
def logout():
	logout_user()
	flash("Logout successfull.", category="success")
	return redirect(url_for('links.login'))

@links.route("/create-admin")
def create_admin():
	admin = User(username='admin', password=generate_password_hash('admin', method="sha256"))
	db.session.add(admin)
	db.session.commit()
	return redirect(url('links.login'))
