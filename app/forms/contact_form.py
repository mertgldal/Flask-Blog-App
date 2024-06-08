from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.simple import EmailField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField(
        label="Name",
        validators=[DataRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": "Name"},
    )
    email = EmailField(
        label="Email",
        validators=[DataRequired(), Email(message="This is not a valid email address")],
        render_kw={"placeholder": "Email"},
    )
    phone = StringField(
        label="Phone",
        validators=[DataRequired(), Length(min=10, max=14)],
        render_kw={"placeholder": "Phone"},
    )  # Regexp(regex='^[+-]?[0-9]$')
    message = TextAreaField(
        label="Message",
        validators=[DataRequired(message="You can't send empty messages")],
        render_kw={"placeholder": "Message"},
    )
    submit = SubmitField(label="Contact Me")
