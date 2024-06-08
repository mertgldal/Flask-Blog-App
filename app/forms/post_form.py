from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, URL, Length


class CreatePostForm(FlaskForm):
    title = StringField(
        label="Blog Post Title", validators=[DataRequired(), Length(min=1, max=70)]
    )
    subtitle = StringField(
        label="Subtitle", validators=[DataRequired(), Length(min=1, max=50)]
    )
    img_url = StringField(label="Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField(label="Blog Content", validators=[DataRequired()])
    submit = SubmitField(label="Submit Post")
