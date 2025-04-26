import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, session
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, gravatar
from app.models.user import User
from app.models.blogpost import BlogPost
from app.models.comment import Comment
from app.forms.post_form import CreatePostForm
from app.forms.user_form import RegisterForm, LoginForm, ChangePasswordForm
from app.forms.comment_form import CommentForm
from app.forms.contact_form import ContactForm
from functools import wraps
import smtplib
import os
from transformers import pipeline
from collections import Counter
from datetime import datetime, timedelta



routes = Blueprint("routes", __name__)
contact_email = os.getenv("contact_email")
contact_email_pwd = os.getenv("contact_email_pwd")
contact_mailbox = os.getenv("contact_mailbox")

summarizer = pipeline("summarization")


def is_user_authenticated(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if current_user.is_authenticated:
            flash(
                f"You are already logged in! You can't access the {func.__name__} page",
                "danger",
            )
            return redirect(url_for("routes.get_all_posts"))
        return func(*args, **kwargs)

    return wrapped


def admin_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if current_user.role == "admin":
            return func(*args, **kwargs)
        return abort(403)

    return wrapped


@routes.route("/register", methods=["GET", "POST"])
@is_user_authenticated
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = (
            db.session.query(User).filter(User.username == form.username.data).first()
        )
        email = db.session.query(User).filter(User.email == form.email.data).first()
        if username or email:
            if username:
                flash("Username already taken", "danger")
                return redirect(url_for("routes.register"))
            else:
                flash("Email already taken", "danger")
                return redirect(url_for("routes.register"))
        else:
            password_hash = generate_password_hash(
                form.password.data, method="pbkdf2:sha256", salt_length=8
            )
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password=password_hash,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("routes.get_all_posts"))
    return render_template("register.html", form=form)


@routes.route("/login", methods=["GET", "POST"])
@is_user_authenticated
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next = request.args.get("next")
            return redirect(next or url_for("routes.get_all_posts"))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("routes.login"))
    return render_template("login.html", form=form)


@routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("routes.get_all_posts"))


@routes.route("/")
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@routes.route("/generate-summary/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_required
def generate_summary(post_id):
    post = db.get_or_404(BlogPost, post_id)

    if len(post.body) < 50:
        flash("Post content is too short for summarization.", "warning")
        return redirect(url_for(endpoint="routes.get_all_posts"))

    try:
        summary_result = summarizer(post.body, max_length=80, min_length=30, do_sample=False)
        summary_text = summary_result[0]['summary_text']
        post.summary = summary_text
        db.session.commit()
        flash("Summary generated and saved!", "success")
    except Exception as e:
        flash(f"Failed to generate summary: {e}", "danger")

    return redirect(url_for(endpoint="routes.get_all_posts"))


@routes.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def view_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    user = current_user
    form = CommentForm()
    comments = post.comments

    # Only count unique views per session
    viewed_post = session.get('viewed_post', [])
    if post_id not in viewed_post:
        post.views += 1
        db.session.commit()
        viewed_post.append(post_id)
        session["viewed_post"] = viewed_post
    if form.validate_on_submit():
        new_comment = Comment(
            comment=form.comment.data,
            author_id=user.get_id(),
            post_id=post_id,
            date=datetime.datetime.now().strftime("%B %d, %Y, %I:%M %p"),
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(
            url_for(
                "routes.view_post",
                post_id=post.id,
                form=form,
                comments=comments,
                avatar=gravatar,
            )
        )
    return render_template(
        "post.html", post=post, form=form, comments=comments, avatar=gravatar
    )


@routes.route("/delete-comment/<int:comment_id>", methods=["GET", "POST"])
@login_required
def delete_comment(comment_id):
    post_id = request.args.get("post_id")
    comment = db.get_or_404(Comment, comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("routes.view_post", post_id=post_id))


@routes.route("/edit-comment")
@login_required
def edit_comment():
    return render_template("coming-soon.html")


@routes.route("/new-post", methods=["GET", "POST"])
@login_required
@admin_required
def add_new_post():
    form = CreatePostForm()

    if form.validate_on_submit():
        word_count = len(form.body.data.split())
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=datetime.date.today().strftime("%B %d, %Y"),
            avg_read_time=round(word_count / 100, 2),
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("routes.get_all_posts"))
    return render_template("make-post.html", form=form)


@routes.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(obj=post)
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("routes.view_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form)


@routes.route("/delete-post/<int:post_id>")
@login_required
@admin_required
def delete_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("routes.get_all_posts"))


@routes.route("/about")
def about():
    return render_template("about.html")


@routes.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        with smtplib.SMTP("smtp.mail.yahoo.com", 587, timeout=120) as connection:
            connection.starttls()
            connection.login(contact_email, contact_email_pwd)
            connection.sendmail(
                from_addr=contact_email,
                to_addrs=contact_mailbox,
                msg=f"Subject:Message from {form.name.data}\n\n{form.message.data}\n{form.email.data}",
            )
        flash("Message sent", "success")
    return render_template("contact.html", form=form)


@routes.route("/profile/<int:user_id>", methods=["GET", "POST"])
@login_required
def profile_page(user_id):
    user = db.get_or_404(User, user_id)
    change_password_form = ChangePasswordForm()
    if change_password_form.validate_on_submit():
        if check_password_hash(user.password, change_password_form.password.data):
            user.password = generate_password_hash(
                change_password_form.new_password.data,
                method="pbkdf2:sha256",
                salt_length=8,
            )
            db.session.commit()
            flash("Password updated", "success")
        else:
            flash("Invalid current password", "danger")
    return render_template("profile-page.html", user=user, form=change_password_form)


# Route to update user role
@routes.route('/admin/update-role/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def update_user_role(user_id):
    new_role = request.form.get('new_role')
    user = User.query.get(user_id)
    if user:
        if new_role in ['user', 'admin']:
            user.role = new_role
            db.session.commit()
            flash(f"Role updated for {user.username} to {new_role}.")
        else:
            flash(f"Invalid role value sent: {new_role}", "warning")
    else:
        flash(f"User not found (ID: {user_id}).", "error")
    return redirect(url_for('routes.admin_dashboard'))


@routes.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    users = User.query.all()
    posts = BlogPost.query.all()

    top_posts = sorted(posts, key=lambda p: p.views, reverse=True)[:5]
    top_titles = [post.title for post in top_posts]
    top_views = [post.views for post in top_posts]

    stats = {
        'total_users': len(users),
        'total_posts': len(posts),
        'avg_read_time': round(sum(p.avg_read_time for p in posts) / len(posts), 2) if posts else 0
    }

    return render_template(
        "admin_dashboard.html",
        users=users,
        posts=posts,
        stats=stats,
        top_titles=top_titles,
        top_views=top_views
    )


# Route to delete a user
@routes.route('/admin/delete-user', methods=['POST'])
@login_required
@admin_required
def delete_user():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(f"Deleted user {user.name}.")
    return redirect(url_for('admin_dashboard'))
