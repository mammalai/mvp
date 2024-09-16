from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from backend.extensions import db

class Query:
    def __init__(self, owner_class, owner=None):
        self.owner = owner  # Keep a reference to the child class instance
        self.owner_class = owner_class

    def filter_by(self, **kwargs):
        """kwargs will be a dictionary and the mongodb find expects a query dictionary"""
        self.pymongo_cursor = db.db[self.owner_class.__collectionname__].find(kwargs, {"_id": False})
        return self

    def first(self):
        record = next(self.pymongo_cursor, None)
        if record is None:
            return None
        else:
            return self.owner_class(**record)

    def all(self):
        return [self.owner_class(**r) for r in self.pymongo_cursor]


class MongoMeta(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        # Create a class-level query attribute for each subclass
        cls.query = Query(owner_class=cls)

    def __call__(cls, *args, **kwargs):
        # Create the instance
        instance = super().__call__(*args, **kwargs)
        
        # Inject the query attribute, passing the child instance to Query
        instance.query = Query(owner=instance, owner_class=cls)
        
        return instance

@dataclass
class MongoBaseClass(metaclass=MongoMeta):
    
    def dict(self):
        """a method to convert the dataclass to a dictionary"""
        return {k: v for k, v in asdict(self).items()}

    @abstractmethod
    def save(self):
        NotImplementedError("Subclasses must implement save() method")

    @abstractmethod
    def delete(self):
        NotImplementedError("Subclasses must implement delete() method")