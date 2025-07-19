# logic/context.py
from flask import session, redirect, url_for, flash, request
from functools import wraps
from logic.entity import User

ALLOWED_ENDPOINTS_WHEN_NO_PASSWORD = {"account.account", "account.change_password"}

def inject_user():
    user = None
    if "user_id" in session:
        user = User.query.get(session["user_id"])
    return {"user": user}

def require_login(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        user = User.query.get(user_id) if user_id else None

        # Şifresiz kullanıcıyı sadece /account'a izin vererek yönlendir
        if user and not user.credentials and request.endpoint not in ALLOWED_ENDPOINTS_WHEN_NO_PASSWORD:
            flash("Lütfen hesabınıza bir şifre oluşturun.", "warning")
            return redirect(url_for("account.account"))

        if not user_id:
            flash("Bu sayfayı görüntülemek için giriş yapmalısınız.", "warning")
            return redirect(url_for("auth.login"))

        if not user:
            flash("Kullanıcı bulunamadı.", "error")
            return redirect(url_for("auth.login"))

        return view_func(*args, **kwargs)
    return wrapper

def require_admin(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        user = User.query.get(user_id) if user_id else None

        # Şifresiz kullanıcıyı sadece /account'a izin vererek yönlendir
        if user and not user.credentials and request.endpoint not in ALLOWED_ENDPOINTS_WHEN_NO_PASSWORD:
            flash("Lütfen hesabınıza bir şifre oluşturun.", "warning")
            return redirect(url_for("account.account"))

        if not user_id:
            flash("Giriş yapmanız gerekiyor.", "warning")
            return redirect(url_for("auth.login"))

        if not user or not user.role or user.role.name.lower() != "admin":
            flash("Bu sayfaya erişim yetkiniz yok.", "error")
            return redirect(url_for("main.index"))

        return view_func(*args, **kwargs)
    return wrapper
