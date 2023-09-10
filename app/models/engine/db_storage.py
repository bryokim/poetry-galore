from app import db
from app.models.category import Category
from app.models.comment import Comment
from app.models.poem import Poem
from app.models.theme import Theme
from app.models.user import User


class DBStorage(object):
    """Database Storage class containing methods
    for interacting with the database.
    """

    classes = {
        "Category": Category,
        "Comment": Comment,
        "Poem": Poem,
        "Theme": Theme,
        "User": User,
    }

    def __init__(self, _db=None):
        """Initialize a DBStorage instance.
        If _db is None, the default database created during Flask app
        creation will be used. You can specify _db to use a specific database
        for example in testing.

        Args:
            _db (object, optional): Database to use. Defaults to None.
        """
        if _db is not None:
            self.__session = _db.session
        else:
            self.__session = db.session

    def all(self, cls=None):
        """Return all objects on current database session of class cls.
        If cls is None return all objects.

        Args:
            cls (class): Class of the objects to return. Defaults to None.
        """
        if cls:
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for value in self.classes.values():
                objs.extend(self.__session.query(value).all())

        return {f"{obj.__class__.__name__}.{obj.id}": obj for obj in objs}

    def new(self, obj):
        """Add obj to the current database session

        Args:
            obj (object): Object to add to the session
        """

        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""

        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session if not none.

        Args:
            obj (object): Object to delete. Defaults to None.
        """

        if obj:
            self.__session.delete(obj)

    def get(self, cls, id):
        """Retrieve one object.

        Args:
            cls (class): Class of the object.
            id (str) : Object ID.

        Returns:
            obj : Object based on cls and id,
                or None if not found.
        """
        retrieved_obj = None
        new_dict = self.all(cls)
        for obj in new_dict.values():
            if obj.id == id:
                retrieved_obj = obj

        return retrieved_obj

    def count(self, cls=None):
        """count the number of object in storage

        Args:
            cls (class, optional): Class. Defaults to None.

        Returns:
            int : number of objects in storage matching the given class.
                If no class is passed, returns the count of all objects in
                storage.
        """
        if cls:
            count = len(self.all(cls).values())
        else:
            count = len(self.all().values())

        return count

    def get_by_attribute(self, cls, **kwargs):
        """Retrieve one object if it matches the given attribute.

        Args:
            cls (class): Class of the object.
            kwargs (dict) : Dictionary containing the attribute name
                and value.

        Returns:
            obj : Object based on cls and attribute given,
                or None if not found.
        """
        retrieved_obj = None
        new_dict = self.all(cls)

        for obj in new_dict.values():
            if not retrieved_obj:
                for attr, value in kwargs.items():
                    if getattr(obj, attr) != value:
                        retrieved_obj = None
                        break
                    else:
                        retrieved_obj = obj
            else:
                break

        return retrieved_obj
