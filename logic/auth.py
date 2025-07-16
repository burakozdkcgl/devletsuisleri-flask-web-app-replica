from flask import Blueprint, render_template, request, redirect, url_for, flash
from logic.entity import User, UserCredential
from logic.db import db
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.credentials and check_password_hash(user.credentials.password_hash, password):
            # Giriş başarılı
            return f"Giriş başarılı! Hoş geldin {user.full_name}"
        else:
            flash("Kullanıcı adı veya şifre yanlış.")
            return redirect(url_for("auth.login"))

    return render_template("login.html")
