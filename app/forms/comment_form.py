from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    comment = TextAreaField(
        label="Comment",
        validators=[DataRequired(message="You can't send empty comments")],
    )
    submit = SubmitField(label="Submit Comment")
