from sqlalchemy import Column, ForeignKey, Integer, String

from app import db
from app.models.base_model import BaseModel
from app.models.poem import poem_category


class Category(BaseModel, db.Model):
    __tablename__ = "categories"

    name = Column(String(100), nullable=False)

    poems = db.relationship("Poem", secondary=poem_category)
