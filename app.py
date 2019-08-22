"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "thesecretestofallkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()


@app.route('/')
def home():

    return redirect('/users')


@app.route("/users")
def show_users():

    users = User.query.all()

    return render_template("index.html", users=users)


@app.route("/users/new", methods=["GET"])
def show_new_user():

    return render_template("new.html")


@app.route("/users", methods=["POST"])
def create_new_user():

    new_user = User(

        first_name=request.form["first_name"],
        last_name=request.form["last_name"],
        image_url=request.form["url_image"]
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def user_page(user_id):
    
    user = User.query.get(user_id)
    return render_template("profile.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_page(user_id):

    user = User.query.get(user_id)
    return render_template("edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):

    user = User.query.get(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['url_image']

    db.session.add(user)
    db.session.commit()
    
    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
