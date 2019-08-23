"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post, Tag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "thesecretestofallkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()


@app.route('/')
def home():

    return redirect('/users')


@app.route("/users")
def show_users():

    users1 = User.query.all()

    return render_template("index.html", users=users1)


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

#################################################################

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):

    user = User.query.get(user_id)
    return render_template('/posts/new.html', user=user)



@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def post_content(user_id):

    user = User.query.get(user_id)
    new_post = Post(
        title=request.form["title"],
        content=request.form["content"],
        user=user 
    )

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")  

@app.route('/posts/<int:post_id>')
def show_post(post_id):

    post = Post.query.get(post_id)
    
    return render_template("posts/post.html", post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit(post_id):
    post = Post.query.get(post_id)

    return render_template("posts/edit_post.html", post=post)
    

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):

    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']


    db.session.add(post)
    db.session.commit()
    
    return redirect("/users")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):

    post = Post.query.get(post_id)
    postId = post.user.id
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{postId}")



##########################################################################################

@app.route('/tags')
def show_tags():

    tags = Tag.query.all()
    return render_template('/tag/show_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_detail(tag_id):

    tag = Tag.query.get(tag_id)

    return render_template('/tag/tag.html', tag=tag)

@app.route('/tags/new')
def new_tag():

    posts = Post.query.all()
    return render_template('/tag/new_tag.html', posts=posts)

@app.route('/tags/new', methods=['POST'])
def submit_new_tag():

    new_tag = Tag(
        name=request.form["name"]
    )

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):

    tag = Tag.query.get(tag_id)
    post = Post.query.all()

    return render_template('/tag/edit_tag.html', tag=tag, post=post)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def update_tag(tag_id):

    tag = Tag.query.get(tag_id)
    tagId = tag.id
    tag.name = request.form('name')
    tag.post = Post.query.all()

    db.session.add(tag)
    db.session.commit()



    return redirect(f'/tags/{tagId}')


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(iag_id):

    tag = Tag.query.get(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')

