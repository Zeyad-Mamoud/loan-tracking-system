from abc import ABC, abstractmethod
from typing import List
from domain.entities.contact import Contact

class ContactRepository(ABC):
    @abstractmethod
    def add(self, contact: Contact) -> Contact:
        pass

    @abstractmethod
    def get_by_id(self, contact_id: int) -> Contact:
        pass

    @abstractmethod
    def get_all(self) -> List[Contact]:
        pass