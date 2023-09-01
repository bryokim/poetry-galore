from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Length, InputRequired

from app.models.user import User


class PostPoemForm(FlaskForm):
    title = StringField(
        "Title", validators=[DataRequired(), Length(min=3, max=30)]
    )

    poem_body = TextAreaField(
        "Body", validators=[DataRequired(), Length(min=3, max=1024)]
    )
    # tag = SelectMultipleField(
    #     "Tag",
    #     validators=[DataRequired()],
    #     choices=["love", "sad", "death", "silly"],
    #     coerce=True,
    # )

    # category = RadioField(
    #     "Category",
    #     validators=[InputRequired()],
    #     choices=[("classical", "type"), "old-but"],
    #     coerce="unicode",
    # )
