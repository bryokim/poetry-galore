from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.models.user import User


class UpdateUserForm(FlaskForm):
    username = StringField(
        "New username", validators=[DataRequired(), Length(min=1, max=30)]
    )

    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Email(message=None),
            Length(min=6, max=40),
        ],
    )

    def validate(self, extra_validators=None):
        initial_validation = super(UpdateUserForm, self).validate()

        if not initial_validation:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already taken")
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False

        return True
