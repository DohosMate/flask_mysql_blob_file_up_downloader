from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Function that initializes the db and creates tables
def db_init(app):
    db.init_app(app)

    # Creates the tables if the db doesn't already exist
    with app.app_context():
        db.create_all()