from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

from app.models.user import User


class PostPoemForm(FlaskForm):
    title = StringField(
        "Title", validators=[DataRequired(), Length(min=3, max=30)]
    )

    poem_body = TextAreaField(
        "Body", validators=[DataRequired(), Length(max=1024)]
    )
