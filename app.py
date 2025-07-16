from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logic.config import SQLALCHEMY_DATABASE_URI, SECRET_KEY

from logic.db import db


app = Flask(__name__,
            static_folder="static",
            template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY



db.init_app(app)


from logic.entity import User, Role, Branch, UserCredential

from logic.main import main_bp
app.register_blueprint(main_bp)

from logic.auth import auth_bp
app.register_blueprint(auth_bp)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        from werkzeug.security import generate_password_hash

        admin_role = Role.query.filter_by(name="Admin").first()
        if not admin_role:
            admin_role = Role(name="Admin")
            db.session.add(admin_role)
            db.session.commit()

        user = User.query.filter_by(username="deneme").first()
        if not user:
            user = User(
                username="deneme",
                full_name="Test Kullanıcı",
                role_id=admin_role.id,
                branch_id=None
            )
            db.session.add(user)
            db.session.commit()

            password = generate_password_hash("1234")
            credential = UserCredential(user_id=user.id, password_hash=password)
            db.session.add(credential)
            db.session.commit()
            
    app.run(debug=True)
