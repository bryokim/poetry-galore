"""Tests for the BaseModel class"""

from datetime import datetime
from uuid import uuid4

from app.models.base_model import BaseModel


def test_base_model_no_args():
    """
    GIVEN a BaseModel model
    WHEN a new BaseModel is created without arguments
    THEN check id, created_at and updated_at are defined correctly
    """

    base_model = BaseModel()
    assert base_model.id is not None
    assert type(base_model.id) is str

    assert base_model.created_at is not None
    assert type(base_model.created_at) is datetime

    assert base_model.updated_at is not None
    assert type(base_model.updated_at) is datetime


def test_base_model_with_args():
    """
    GIVEN a BaseModel model
    WHEN a new BaseModel is created with positional arguments
    THEN check id, created_at and updated_at are defined correctly
    """

    base_model = BaseModel("one", "two", "three")
    assert base_model.id != "one"
    assert type(base_model.id) is str

    assert base_model.created_at != "two"
    assert type(base_model.created_at) is datetime

    assert base_model.updated_at != "three"
    assert type(base_model.updated_at) is datetime


def test_base_model_with_kwargs():
    """
    GIVEN a BaseModel model
    WHEN a new BaseModel is created with keyword arguments
    THEN check id, created_at and updated_at are defined correctly
    """

    base_model = BaseModel(
        id="one",
        created_at=(datetime.now()).isoformat(),
        updated_at=(datetime.now()).isoformat(),
    )
    assert base_model.id == "one"
    assert type(base_model.id) is str

    assert base_model.created_at is not None
    assert type(base_model.created_at) is datetime

    assert base_model.updated_at is not None
    assert type(base_model.updated_at) is datetime


def test_base_model_without_id_kwarg():
    """
    GIVEN a BaseModel model
    WHEN a new BaseModel is created without the id keyword arguments
        but with both the created_at and updated_at kwargs
    THEN check created_at and updated_at are defined correctly from the
        kwargs and new id is created.
    """

    created_at = (datetime.now()).isoformat()
    updated_at = (datetime.now()).isoformat()

    base_model = BaseModel(
        created_at=created_at,
        updated_at=updated_at,
    )
    assert base_model.id is not None
    assert type(base_model.id) is str

    assert base_model.created_at == datetime.fromisoformat(created_at)
    assert type(base_model.created_at) is datetime

    assert base_model.updated_at == datetime.fromisoformat(updated_at)
    assert type(base_model.updated_at) is datetime


def test_base_model_without_created_at_kwarg():
    """
    GIVEN a BaseModel model
    WHEN a new BaseModel is created without the created_at keyword arguments
        but with both the id and updated_at kwargs
    THEN check id and updated_at are defined correctly from the
        kwargs and new created_at is created.
    """

    id = str(uuid4())
    updated_at = (datetime.now()).isoformat()

    base_model = BaseModel(
        id=id,
        updated_at=updated_at,
    )
    assert base_model.id == id
    assert type(base_model.id) is str

    assert base_model.created_at is not None
    assert type(base_model.created_at) is datetime

    assert base_model.updated_at == datetime.fromisoformat(updated_at)
    assert type(base_model.updated_at) is datetime


def test_base_model_without_updated_at_kwarg():
    """
    GIVEN a BaseModel model
    WHEN a new BaseModel is created without the updated_at keyword arguments
        but with both the id and created_at kwargs
    THEN check id and created_at are defined correctly from the
        kwargs and new updated_at is created.
    """

    id = str(uuid4())
    created_at = (datetime.now()).isoformat()

    base_model = BaseModel(
        id=id,
        created_at=created_at,
    )
    assert base_model.id == id
    assert type(base_model.id) is str

    assert base_model.created_at == datetime.fromisoformat(created_at)
    assert type(base_model.created_at) is datetime

    assert base_model.updated_at is not None
    assert type(base_model.updated_at) is datetime


def test_to_dict():
    """
    GIVEN a BaseModel model
    WHEN to_dict method is called
    THEN a dictionary of the model with a __class__ key with a value of
        BaseModel is returned. Check that both created_at and updated_at
        have been converted to isoformat.
    """
    base_model = BaseModel()
    base_model_dict = base_model.to_dict()

    assert type(base_model_dict) is dict

    assert base_model_dict["__class__"] == "BaseModel"

    assert base_model_dict["id"] is not None
    assert type(base_model_dict["id"]) is str

    assert base_model_dict["created_at"] is not None
    assert type(base_model_dict["created_at"]) is str

    assert base_model_dict["updated_at"] is not None
    assert type(base_model_dict["updated_at"]) is str
