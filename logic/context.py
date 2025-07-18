# logic/context.py
from flask import session
from logic.entity import User

def inject_user():
    user = None
    if "user_id" in session:
        user = User.query.get(session["user_id"])
    return {"user": user}
