from flask_sqlalchemy import SQLAlchemy
import datetime 

db = SQLAlchemy()

def connect_db(app):
    """connect to the database"""

    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False)


    posts = db.relationship('Post', backref="user")

    def __repr__(self):

        u = self
        return f"<User {u.first_name} {u.last_name}>"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    

    # pst = db.relationship('User', backref="post")


class PostTag(db.Model):

    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary='post_tags', backref='tags')


