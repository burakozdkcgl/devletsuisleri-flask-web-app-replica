from flask import Flask
from config import SQLALCHEMY_DATABASE_URI, RESET_COOKIE_ON_EACH_LAUNCH, SQLALCHEMY_TRACK_MODIFICATIONS
from logic.context import inject_user
from logic.db import db, handle_schema


import secrets

if RESET_COOKIE_ON_EACH_LAUNCH:
    SECRET_KEY = secrets.token_hex(32)
else:
    from config import SECRET_KEY as STATIC_SECRET_KEY
    SECRET_KEY = STATIC_SECRET_KEY

app = Flask(__name__,
            static_folder="static",
            template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = SECRET_KEY


app.context_processor(inject_user)

db.init_app(app)


from logic.main import main_bp
from logic.auth import auth_bp
from logic.admin import admin_bp
from logic.account import account_bp
from logic.inventory import inventory_bp
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(account_bp)
app.register_blueprint(inventory_bp)

if __name__ == "__main__":
    with app.app_context():
        handle_schema(app)
    app.run(debug=True)
