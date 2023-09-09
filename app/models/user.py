from flask_login import UserMixin
from sqlalchemy import Column, String
from uuid import uuid4

from app import db, bcrypt
from app.models.base_model import BaseModel
from app.models.comment import Comment
from app.models.poem import Poem, poem_user


class User(BaseModel, db.Model, UserMixin):
    __tablename__ = "users"

    username = Column(String(20), nullable=False, unique=True)
    email = Column(String(60), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    alternative_id = Column(String(60), nullable=False, unique=True)

    def __init__(self, *args, **kwargs):
        self.alternative_id = str(uuid4())
        self.password = bcrypt.generate_password_hash(kwargs.get("password"))
        del kwargs["password"]
        super(User, self).__init__(*args, **kwargs)

    def get_id(self):
        return str(self.alternative_id)

    poems = db.relationship(
        "Poem",
        backref="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    comments = db.relationship(
        "Comment",
        backref="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    poem_likes = db.relationship(
        "Poem",
        secondary=poem_user,
        back_populates="likes",
    )
