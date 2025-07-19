# logic/context.py
from flask import session, redirect, url_for, flash
from functools import wraps
from logic.entity import User

def inject_user():
    user = None
    if "user_id" in session:
        user = User.query.get(session["user_id"])
    return {"user": user}

def require_admin(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            flash("Giriş yapmanız gerekiyor.", "warning")
            return redirect(url_for("auth.login"))

        user = User.query.get(user_id)
        if not user or user.role.name != "Admin":
            flash("Bu sayfaya erişim yetkiniz yok.", "error")
            return redirect(url_for("main.index"))

        return view_func(*args, **kwargs)
    return wrapper


def require_login(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            flash("Bu sayfayı görüntülemek için giriş yapmalısınız.", "warning")
            return redirect(url_for("auth.login"))

        user = User.query.get(user_id)
        if not user:
            flash("Kullanıcı bulunamadı.", "error")
            return redirect(url_for("auth.login"))

        return view_func(*args, **kwargs)
    return wrapper