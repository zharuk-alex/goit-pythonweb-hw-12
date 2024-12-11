from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.contacts import ContactRepository
from src.schemas import ContactBase, ContactUpdate
from src.database.models import Contact, User


class ContactService:
    def __init__(self, db: AsyncSession):
        self.contact_repository = ContactRepository(db)

    async def create_contact(self, body: ContactBase, user: User):
        return await self.contact_repository.create_contact(body, user)

    async def get_contacts(self, skip: int, limit: int, filters: dict, user: User):
        return await self.contact_repository.get_contacts(
            skip=skip, limit=limit, filters=filters, user=user
        )

    async def get_contact(self, contact_id: int, user: User):
        return await self.contact_repository.get_contact_by_id(contact_id, user)

    async def update_contact(self, contact_id: int, body: ContactUpdate, user: User):
        return await self.contact_repository.update_contact(contact_id, body, user)

    async def remove_contact(self, contact_id: int, user: User):
        return await self.contact_repository.remove_contact(contact_id, user)

    async def get_upcoming_birthdays(self, user: User):
        return await self.contact_repository.get_upcoming_birthdays(user)

    async def update_phone(
        self, contact_id: int, phone: str, user: User
    ) -> Optional[Contact]:
        return await self.contact_repository.update_phone(contact_id, phone, user)

    async def update_email(
        self, contact_id: int, email: str, user: User
    ) -> Optional[Contact]:
        return await self.contact_repository.update_email(contact_id, email, user)
