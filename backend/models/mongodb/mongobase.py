from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from backend.extensions import db

class Query:
    def __init__(self, owner_class, owner=None):
        self.owner = owner  # Keep a reference to the child class instance
        self.owner_class = owner_class

    async def filter_by(self, **kwargs):
        """kwargs will be a dictionary and the mongodb find expects a query dictionary"""
        self.cursor = db[self.owner_class.__collectionname__].find(kwargs, {"_id": False})
        return self

    async def first(self):
        """Get the first record asynchronously"""
        if not hasattr(self, 'cursor'):
            return None
            
        # For AsyncIOMotorCursor
        doc = await self.cursor.to_list(length=1)
        if doc:
            return self.owner_class(**doc[0])
        return None

    async def all(self):
        """Get all records asynchronously"""
        if not hasattr(self, 'cursor'):
            return []
            
        docs = await self.cursor.to_list(length=None)  # Get all documents
        return [self.owner_class(**doc) for doc in docs]


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
    async def save(self):
        NotImplementedError("Subclasses must implement save() method")

    @abstractmethod
    async def delete(self):
        NotImplementedError("Subclasses must implement delete() method")