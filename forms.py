from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, URL, Email, EqualTo, Length, Regexp
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField(
        label="Blog Post Title",
        validators=[DataRequired(), Length(min=1, max=70)]
    )
    subtitle = StringField(
        label="Subtitle",
        validators=[DataRequired(), Length(min=1, max=50)]
    )
    img_url = StringField(
        label="Blog Image URL",
        validators=[DataRequired(), URL()]
    )
    body = CKEditorField(
        label="Blog Content",
        validators=[DataRequired()]
    )
    submit = SubmitField(label="Submit Post")


# TODO: Create a RegisterForm to register new users
class RegisterForm(FlaskForm):
    username = StringField(
        label="Username",
        validators=[DataRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": "Username"}
    )
    email = EmailField(
        label="Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"}
    )
    password = PasswordField(
        label="Password",
        validators=[
            DataRequired(),
            Length(min=8, max=20, message="Password must be at least 8 characters long"),
            EqualTo("password_confirmation", message="Passwords must match")
        ],
        render_kw={"placeholder": "Password"}
    )
    password_confirmation = PasswordField(
        label="Password Confirmation",
        validators=[DataRequired()],
        render_kw={"placeholder": "Password Confirmation"}
    )
    submit = SubmitField(label="Sign Up")


# TODO: Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    email = EmailField(
        label="Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"}
    )
    password = PasswordField(
        label="Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Password"}
    )
    remember = BooleanField(label="Remember Me")
    submit = SubmitField(label="Log In")


# TODO: Create a CommentForm so users can leave comments below posts
class CommentForm(FlaskForm):
    comment = TextAreaField(
        label="Comment",
        validators=[DataRequired(message="You can't send empty comments")]
    )
    submit = SubmitField(label="Submit Comment")


class ContactForm(FlaskForm):
    name = StringField(
        label="Name",
        validators=[DataRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": "Name"}
    )
    email = EmailField(
        label="Email",
        validators=[DataRequired(), Email(message="This is not a valid email address")],
        render_kw={"placeholder": "Email"}
    )
    phone = StringField(
        label="Phone",
        validators=[DataRequired(), Length(min=10, max=14)],
        render_kw={"placeholder": "Phone"}
    )  # Regexp(regex='^[+-]?[0-9]$')
    message = TextAreaField(
        label="Message",
        validators=[DataRequired(message="You can't send empty messages")],
        render_kw={"placeholder": "Message"}
    )
    submit = SubmitField(label="Contact Me")
