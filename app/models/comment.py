from sqlalchemy import Column, ForeignKey, Integer, String

from app import db
from app.models.base_model import BaseModel


class Comment(BaseModel, db.Model):
    __tablename__ = "comments"

    text = Column(String(1000), nullable=False)
    user_id = Column(
        String(60), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    poem_id = Column(
        String(60), ForeignKey("poems.id", ondelete="CASCADE"), nullable=False
    )
