from sqlalchemy import Column, ForeignKey, Integer, String, Table

from app import db
from app.models.base_model import BaseModel
from app.models.comment import Comment

poem_category = Table(
    "poem_category",
    db.metadata,
    Column(
        "poem_id",
        String(60),
        ForeignKey("poems.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "category_id",
        String(60),
        ForeignKey("categories.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)


poem_theme = Table(
    "poem_theme",
    db.metadata,
    Column(
        "poem_id",
        String(60),
        ForeignKey("poems.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "theme_id",
        String(60),
        ForeignKey("themes.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)

poem_user = Table(
    "likes",
    db.metadata,
    Column(
        "poem_id",
        String(60),
        ForeignKey("poems.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "user_id",
        String(60),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)


class Poem(BaseModel, db.Model):
    __tablename__ = "poems"

    title = Column(String(100), nullable=False)
    body = Column(String(1024), nullable=False)
    language = Column(String(4), nullable=False, default="en")
    user_id = Column(
        String(60), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    comments = db.relationship(
        "Comment",
        backref="poem",
        cascade="all,delete-orphan",
        passive_deletes=True,
    )

    from app.models.category import Category

    category = db.relationship(
        "Category",
        secondary=poem_category,
        viewonly=False,
        back_populates="poems",
    )

    from app.models.theme import Theme

    themes = db.relationship(
        "Theme",
        secondary=poem_theme,
        viewonly=False,
        back_populates="poems",
    )

    likes = db.relationship(
        "User",
        secondary=poem_user,
        viewonly=False,
        back_populates="user_likes",
    )
