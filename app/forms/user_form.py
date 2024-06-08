from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    username = StringField(
        label="Username",
        validators=[DataRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": "Username"},
    )
    email = EmailField(
        label="Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        label="Password",
        validators=[
            DataRequired(),
            Length(
                min=8, max=20, message="Password must be at least 8 characters long"
            ),
            EqualTo("password_confirmation", message="Passwords must match"),
        ],
        render_kw={"placeholder": "Password"},
    )
    password_confirmation = PasswordField(
        label="Password Confirmation",
        validators=[DataRequired()],
        render_kw={"placeholder": "Password Confirmation"},
    )
    submit = SubmitField(label="Sign Up")


# TODO: Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    email = EmailField(
        label="Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        label="Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Password"},
    )
    remember = BooleanField(label="Stay logged in")
    submit = SubmitField(label="Log In")


# TODO: Update the ChangePasswordForm to change a user's password'
class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        label="Current Password",
        validators=[
            DataRequired(),
            Length(
                min=8, max=20, message="Password must be at least 8 characters long"
            ),
            EqualTo("password_confirmation", message="Passwords must match"),
        ],
        render_kw={"placeholder": "Current Password"},
    )
    new_password = PasswordField(
        label="Password",
        validators=[
            DataRequired(),
            Length(
                min=8, max=20, message="Password must be at least 8 characters long"
            ),
            EqualTo("password_confirmation", message="Passwords must match"),
        ],
        render_kw={"placeholder": "New Password"},
    )
    new_password_confirmation = PasswordField(
        label="Password Confirmation",
        validators=[DataRequired()],
        render_kw={"placeholder": "Password Confirmation"},
    )
    submit = SubmitField("Change Password")
