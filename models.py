from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False)

    def __repr__(self):

        u = self
        return f"<User {u.first_name} {u.last_name}>"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


def connect_db(app):
    """connect to the database"""

    db.app = app
    db.init_app(app)

