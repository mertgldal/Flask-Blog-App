import datetime
from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, BlogPost, Comment
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm, ContactForm
from functools import wraps
from flask_gravatar import Gravatar
import smtplib
import os

routes = Blueprint('routes', __name__)
contact_email = os.getenv('contact_email')
contact_email_pwd = os.getenv('contact_email_pwd')
contact_mailbox = os.getenv('contact_mailbox')
gravatar = Gravatar()


def is_user_authenticated(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if current_user.is_authenticated:
            flash(f"You are already logged in! You can't access the {func.__name__} page", 'danger')
            return redirect(url_for('routes.get_all_posts'))

        return func(*args, **kwargs)

    return wrapped


def is_user_admin(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if current_user.get_id() == "1":
            return func(*args, **kwargs)
        return abort(403)
    return wrapped


@routes.route('/register', methods=['GET', 'POST'])
@is_user_authenticated
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = db.session.query(User).filter(User.username == form.username.data).first()
        email = db.session.query(User).filter(User.email == form.email.data).first()
        if username or email:
            if username:
                flash('Username already taken', 'danger')
                return redirect(url_for('routes.register'))
            else:
                flash('Email already taken', 'danger')
                return redirect(url_for('routes.register'))
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
            return redirect(url_for('routes.get_all_posts'))
    else:
        return render_template("register.html", form=form)


@routes.route('/login', methods=['GET', 'POST'])
@is_user_authenticated
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('routes.get_all_posts'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('routes.login'))
    else:
        return render_template("login.html", form=form)


@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.get_all_posts'))


@routes.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@routes.route("/post/<int:post_id>", methods=['GET', 'POST'])
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
        return redirect(url_for('routes.show_post', post_id=requested_post.id, form=form, comments=comments, avatar=gravatar))
    else:
        return render_template("post.html", post=requested_post, form=form, comments=comments, avatar=gravatar)


@routes.route("/delete-comment/<int:comment_id>", methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    post_id = request.args.get('post_id')
    comment = db.get_or_404(entity=Comment, ident=comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('routes.show_post', post_id=post_id))


# TODO: Add a edit comment feature.
# @routes.route("/edit-comment/<int:comment_id>", methods=['GET', 'POST'])
@routes.route("/edit-comment")
@login_required
def edit_comment():
    return render_template('coming-soon.html')


@routes.route("/new-post", methods=["GET", "POST"])
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
        return redirect(url_for('routes.get_all_posts'))
    return render_template("make-post.html", form=form)


@routes.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
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
        return redirect(url_for('routes.show_post', post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@routes.route("/delete/<int:post_id>")
@login_required
@is_user_admin
def delete_post(post_id):
    post_to_delete = db.get_or_404(entity=BlogPost, ident=post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('routes.get_all_posts'))


@routes.route("/about")
def about():
    return render_template("about.html")


# TODO: Add a user profile page
@routes.route("/profile")
@login_required
def profile_page():
    return render_template("coming-soon.html")


@routes.route("/contact", methods=["GET", "POST"])
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

