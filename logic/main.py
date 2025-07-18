from flask import Blueprint, render_template, session

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    user_info = {
        "full_name": session.get("full_name"),
        "role": session.get("role"),
    }
    return render_template("index.html")
