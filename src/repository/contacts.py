from typing import List, Optional

from datetime import date, timedelta

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.schemas import ContactBase, ContactUpdate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        """
        Initialize the ContactRepository with a database session.

        Args:
            session: An instance of AsyncSession for database interactions.
        """
        self.db = session

    async def get_contacts(
        self, skip: int, limit: int, filters: dict, user: User
    ) -> List[Contact]:
        """
        Retrieve a list of contacts with optional filters, pagination, and user ownership.

        Args:
            skip: The number of contacts to skip.
            limit: The maximum number of contacts to retrieve.
            filters: A dictionary of field-value pairs to filter contacts.
            user: The User who owns the contacts.

        Returns:
            A list of Contact instances matching the criteria.
        """
        filter_cond = [
            getattr(Contact, field).ilike(f"%{value}%")
            for field, value in filters.items()
            if hasattr(Contact, field) and value
        ]

        filter_cond.append(Contact.user_id == user.id)

        query = select(Contact).filter(and_(*filter_cond)).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_contact_by_id(self, contact_id: int, user: User) -> Optional[Contact]:
        """
        Retrieve a contact by its ID and ensure it belongs to the specified user.

        Args:
            contact_id: The ID of the contact to retrieve.
            user: The User who owns the contact.

        Returns:
            The Contact instance if found, or None otherwise.
        """
        query = select(Contact).where(
            Contact.id == contact_id, Contact.user_id == user.id
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_contact(self, body: ContactBase, user: User) -> Contact:
        """
        Create a new contact for the specified user.

        Args:
            body: A ContactBase instance with the contact details.
            user: The User who will own the new contact.

        Returns:
            The created Contact instance.
        """
        new_contact = Contact(**body.dict(), user=user)
        self.db.add(new_contact)
        await self.db.commit()
        await self.db.refresh(new_contact)
        return new_contact

    async def remove_contact(self, contact_id: int, user: User) -> Optional[Contact]:
        """
        Remove a contact by its ID if it belongs to the specified user.

        Args:
            contact_id: The ID of the contact to remove.
            user: The User who owns the contact.

        Returns:
            The removed Contact instance if found, or None otherwise.
        """
        query = select(Contact).where(
            Contact.id == contact_id, Contact.user_id == user.id
        )
        result = await self.db.execute(query)
        contact = result.scalars().first()
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactUpdate, user: User
    ) -> Optional[Contact]:
        """
        Update a contact's details by its ID if it belongs to the specified user.

        Args:
            contact_id: The ID of the contact to update.
            body: A ContactUpdate instance with the updated contact details.
            user: The User who owns the contact.

        Returns:
            The updated Contact instance if found, or None otherwise.
        """
        query = select(Contact).where(
            Contact.id == contact_id, Contact.user_id == user.id
        )
        result = await self.db.execute(query)
        contact = result.scalars().first()
        if contact:
            for field, value in body.dict(exclude_unset=True).items():
                setattr(contact, field, value)
            self.db.add(contact)
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def get_upcoming_birthdays(self, user: User) -> List[Contact]:
        """
        Retrieve a list of contacts with birthdays within the next 7 days for the specified user.

        Args:
            user: The User who owns the contacts.

        Returns:
            A list of Contact instances with upcoming birthdays.
        """
        today = date.today()
        end_date = today + timedelta(days=7)

        query = select(Contact).where(
            Contact.user_id == user.id,
            func.to_char(Contact.birthday, "MM-DD").between(
                today.strftime("%m-%d"), end_date.strftime("%m-%d")
            ),
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_phone(
        self, contact_id: int, phone: str, user: User
    ) -> Optional[Contact]:
        """
        Update a contact's phone number by its ID if it belongs to the specified user.

        Args:
            contact_id: The ID of the contact to update.
            phone: The new phone number.
            user: The User who owns the contact.

        Returns:
            The updated Contact instance if found, or None otherwise.
        """
        query = select(Contact).where(
            Contact.id == contact_id, Contact.user_id == user.id
        )
        result = await self.db.execute(query)
        contact = result.scalars().first()

        if contact:
            contact.phone = phone
            self.db.add(contact)
            await self.db.commit()
            await self.db.refresh(contact)

        return contact

    async def update_email(
        self, contact_id: int, email: str, user: User
    ) -> Optional[Contact]:
        """
        Update a contact's email address by its ID if it belongs to the specified user.

        Args:
            contact_id: The ID of the contact to update.
            email: The new email address.
            user: The User who owns the contact.

        Returns:
            The updated Contact instance if found, or None otherwise.
        """
        query = select(Contact).where(
            Contact.id == contact_id, Contact.user_id == user.id
        )
        result = await self.db.execute(query)
        contact = result.scalars().first()

        if contact:
            contact.email = email
            self.db.add(contact)
            await self.db.commit()
            await self.db.refresh(contact)

        return contact
