from flask_sqlalchemy import SQLAlchemy
from config import AUTO_CREATE_SCHEMA, RESET_SCHEMA_ON_EACH_LAUNCH, FILL_MOCK_DATA

db = SQLAlchemy()

def handle_schema(app):
    with app.app_context():
        if RESET_SCHEMA_ON_EACH_LAUNCH:
            db.drop_all()
            db.create_all()
        elif AUTO_CREATE_SCHEMA:
            db.create_all()
        else:
            pass  # No action taken if schema management is disabled

        if FILL_MOCK_DATA:
            from logic.mock_data import insert_mock_data
            insert_mock_data(db)