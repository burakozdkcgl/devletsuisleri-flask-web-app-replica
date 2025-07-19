from flask import Blueprint, render_template, session, flash, redirect, request

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    user_info = {
        "full_name": session.get("full_name"),
        "role": session.get("role"),
    }
    return render_template("index.html")

@main_bp.route("/cafeteria", methods=["POST"])
def cafeteria():
    flash("Bu sayfa henüz aktif değil.", "warning")
    return redirect(request.referrer or "/")

@main_bp.route("/directory")
def directory():
    from logic.entity import User, Branch
    users = User.query.all()
    branches = Branch.query.order_by(Branch.name).all()
    return render_template("directory.html", users=users, branches=branches)
