import datetime
from datetime import date
import flask
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm, ContactForm
import secrets
from dotenv import load_dotenv
import os
import smtplib

load_dotenv()

contact_email = os.getenv('contact_email')
contact_email_pwd = os.getenv('contact_email_pwd')
contact_mailbox = os.getenv('contact_mailbox')

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
ckeditor = CKEditor(app)
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(entity=User, ident=user_id)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    posts: Mapped[list["BlogPost"]] = relationship(back_populates="author")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    # Create reference to the User object. The "posts" refers to the posts property in the User class.
    author: Mapped["User"] = relationship(back_populates="posts")

    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comments: Mapped[list["Comment"]] = relationship(back_populates="parent_post")


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="comments")
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog_posts.id"))
    parent_post: Mapped["BlogPost"] = relationship(back_populates="comments")


# TODO: Add reply table to db for comment reply.
# class Reply(db.Model):
#     pass


with app.app_context():
    db.create_all()


# Gravatar config
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


def is_user_authenticated(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if current_user.is_authenticated:
            flash(f"You are already logged in! You can't access the {func.__name__} page", 'danger')
            return redirect(url_for('get_all_posts'))

        return func(*args, **kwargs)

    return wrapped


def is_user_admin(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if current_user.get_id() == "1":
            return func(*args, **kwargs)
        return abort(403)
    return wrapped


@app.route('/register', methods=['GET', 'POST'])
@is_user_authenticated
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = db.session.query(User).filter(User.username == form.username.data).first()
        email = db.session.query(User).filter(User.email == form.email.data).first()
        if username or email:
            if username:
                flash('Username already taken', 'danger')
                return redirect(url_for('register'))
            else:
                flash('Email already taken', 'danger')
                return redirect(url_for('register'))
        else:
            password_hash = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password=password_hash
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('get_all_posts'))
    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
@is_user_authenticated
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next = flask.request.args.get('next')
            return redirect(next or url_for('get_all_posts'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    else:
        return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    user = current_user
    form = CommentForm()
    comments = requested_post.comments
    if form.validate_on_submit():
        new_comment = Comment(
            comment=form.comment.data,
            author_id=user.get_id(),
            post_id=post_id,
            date=datetime.datetime.now().strftime("%B %d, %Y, %I:%M %p")
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('show_post', post_id=requested_post.id, form=form, comments=comments, avatar=gravatar))
    else:
        return render_template("post.html", post=requested_post, form=form, comments=comments, avatar=gravatar)


@app.route("/delete-comment/<int:comment_id>", methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    post_id = request.args.get('post_id')
    comment = db.get_or_404(entity=Comment, ident=comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('show_post', post_id=post_id))


# TODO: Add a edit comment feature.
# @app.route("/edit-comment/<int:comment_id>", methods=['GET', 'POST'])
@app.route("/edit-comment")
@login_required
def edit_comment():
    return render_template('coming-soon.html')


@app.route("/new-post", methods=["GET", "POST"])
@login_required
@is_user_admin
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
@is_user_admin
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:post_id>")
@login_required
@is_user_admin
def delete_post(post_id):
    post_to_delete = db.get_or_404(entity=BlogPost, ident=post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


# TODO: Add a user profile page
@app.route("/profile")
@login_required
def profile_page():
    return render_template("coming-soon.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as connection:
                connection.starttls()
                connection.ehlo()
                connection.login(user=contact_email, password=contact_email_pwd)
                message = (f"Subject: New message from {form.name.data}\n\n"
                           f"Name:{form.name.data},"
                           f"Phone:{form.phone.data},"
                           f"Email:{form.email.data}"
                           f"Message:{form.message.data}"
                           )
                connection.sendmail(from_addr=contact_email, to_addrs=contact_mailbox, msg=message)
        except Exception as e:
            print(e)
        return render_template("contact.html", form=form, msg_sent=True)
    else:
        return render_template("contact.html", form=form, msg_sent=False)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
