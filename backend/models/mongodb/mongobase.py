from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict

@dataclass
class MongoBaseClass(ABC):
    
    def dict(self):
        """a method to convert the dataclass to a dictionary"""
        return {k: v for k, v in asdict(self).items()}

    @abstractmethod
    def save(self):
        NotImplementedError("Subclasses must implement save() method")

    @abstractmethod
    def delete(self):
        NotImplementedError("Subclasses must implement delete() method")