from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from logic.context import require_login
from logic.entity import User, UserCredential
from logic.db import db

account_bp = Blueprint("account", __name__)

@account_bp.route("/account", methods=["GET"])
@require_login
def account():
    user = User.query.get(session["user_id"])
    return render_template("account.html", user=user)


@account_bp.route("/account/update_info", methods=["POST"])
@require_login
def update_info():
    user = User.query.get(session["user_id"])

    full_name = request.form.get("full_name", "").strip()
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()

    # Kullanıcı adı başka biri tarafından kullanılıyor mu?
    if username != user.username:
        existing_user = User.query.filter(User.username == username, User.id != user.id).first()
        if existing_user:
            flash("Bu kullanıcı adı zaten kullanılıyor.", "error")
            return redirect(url_for("account.account"))
        user.username = username
        flash("Kullanıcı adınız güncellendi.", "success")

    if full_name != user.full_name:
        user.full_name = full_name
        flash("Ad soyad güncellendi.", "success")

    if email != user.email:
        user.email = email
        flash("E-posta güncellendi.", "success")

    db.session.commit()
    return redirect(url_for("account.account"))


@account_bp.route("/account/change_password", methods=["POST"])
@require_login
def change_password():
    user = User.query.get(session["user_id"])
    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not user.credentials or not check_password_hash(user.credentials.password_hash, current_password):
        flash("Mevcut şifreniz yanlış.", "error")
        return redirect(url_for("account.account"))

    if new_password != confirm_password:
        flash("Yeni şifreler uyuşmuyor.", "error")
        return redirect(url_for("account.account"))

    if check_password_hash(user.credentials.password_hash, new_password):
        flash("Yeni şifre, mevcut şifreyle aynı olamaz.", "error")
        return redirect(url_for("account.account"))

    user.credentials.password_hash = generate_password_hash(new_password)
    db.session.commit()

    flash("Şifreniz başarıyla güncellendi.", "success")
    return redirect(url_for("account.account"))
