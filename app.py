from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY, SQLALCHEMY_TRACK_MODIFICATIONS


from logic.db import db, handle_schema


app = Flask(__name__,
            static_folder="static",
            template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = SECRET_KEY



db.init_app(app)


from logic.entity import User, Role, Branch, UserCredential

from logic.main import main_bp
app.register_blueprint(main_bp)

from logic.auth import auth_bp
app.register_blueprint(auth_bp)


if __name__ == "__main__":
    with app.app_context():
        handle_schema(app)
    app.run(debug=True)
