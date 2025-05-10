from domain.repositories.contact_repository import ContactRepository
from domain.entities.contact import Contact
from typing import List


class ListContactsUseCase:
    def __init__(self, repository:ContactRepository):
        self.repository = repository

    def execute(self):
        return self.repository.get_all()