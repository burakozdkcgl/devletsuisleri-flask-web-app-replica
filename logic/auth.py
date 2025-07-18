from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from logic.entity import User, UserCredential
from logic.db import db
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if "user_id" in session:
        # Kullanıcı zaten giriş yaptıysa, login sayfasına değil, anasayfaya
        flash("Zaten giriş yaptınız.", "warning")
        return redirect(url_for("main.index"))
    

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.credentials and check_password_hash(user.credentials.password_hash, password):
            session["user_id"] = user.id
            flash(f"Hoş geldin, {user.full_name}!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Kullanıcı adı veya şifre yanlış.", "error")
            return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Başarıyla çıkış yaptınız.", "info")
    return redirect(url_for("main.index"))
