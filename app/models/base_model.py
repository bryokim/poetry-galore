"""BaseModel class module.

All other classes in the models inherit form this class.
It contains methods and properties required by other classes.
"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime


class BaseModel:
    """BaseModel class"""

    id = Column(String(60), primary_key=True, nullable=False)
    updated_at = Column(DateTime(), default=datetime.utcnow(), nullable=False)
    created_at = Column(DateTime(), default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize a new instance"""

        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
        else:
            if "__class__" in kwargs:
                del kwargs["__class__"]

            self.__dict__.update(kwargs)

            if "created_at" in kwargs.keys():
                self.created_at = datetime.fromisoformat(kwargs["created_at"])
            else:
                self.created_at = datetime.utcnow()

            if "updated_at" in kwargs.keys():
                self.updated_at = datetime.fromisoformat(kwargs["updated_at"])
            else:
                self.updated_at = datetime.utcnow()

            if "id" not in kwargs.keys():
                self.id = str(uuid4())

    # def save(self):
    #     self.updated_at = datetime.utcnow()
    #     storage.save(self)

    def to_dict(self, password=True):
        """Get the dictionary representation of the object.

        Args:
            password (bool, optional): Whether to show password in resulting
                dictionary. Defaults to True.

        Returns:
            dict: Dictionary representation of the object.
        """
        new_dict = {}

        new_dict.update(self.__dict__)

        new_dict["created_at"] = datetime.isoformat(self.created_at)
        new_dict["updated_at"] = datetime.isoformat(self.updated_at)

        new_dict["__class__"] = self.__class__.__name__

        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        if not password and "password" in new_dict:
            del new_dict["password"]

        return new_dict
