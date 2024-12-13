from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.contacts import ContactRepository
from src.schemas import ContactBase, ContactUpdate
from src.database.models import Contact, User


class ContactService:
    """
    Service class to handle operations related to Contacts.

    Attributes:
        contact_repository (ContactRepository): Repository to perform contact operations.
    """

    def __init__(self, db: AsyncSession):
        self.contact_repository = ContactRepository(db)

    async def create_contact(self, body: ContactBase, user: User):
        """
        Create a new contact for the given user.

        Args:
            body (ContactBase): Data for creating a contact.
            user: The user to whom the contact will belong.

        Returns:
            Contact: The created contact object.
        """
        return await self.contact_repository.create_contact(body, user)

    async def get_contacts(self, skip: int, limit: int, filters: dict, user: User):
        """
        Retrieve a list of contacts for the given user with filters applied.

        Args:
            skip (int): Number of records to skip for pagination.
            limit (int): Number of records to fetch.
            filters (dict): Filters to apply to the query.
            user: The user to whom the contacts belong.

        Returns:
            List[Contact]: List of retrieved contacts.
        """
        return await self.contact_repository.get_contacts(
            skip=skip, limit=limit, filters=filters, user=user
        )

    async def get_contact(self, contact_id: int, user: User):
        """
        Retrieve a single contact by its ID for the given user.

        Args:
            contact_id (int): ID of the contact.
            user: The user to whom the contact belongs.

        Returns:
            Optional[Contact]: The contact object if found, else None.
        """
        return await self.contact_repository.get_contact_by_id(contact_id, user)

    async def update_contact(self, contact_id: int, body: ContactUpdate, user: User):
        """
        Update a contact by its ID for the given user.

        Args:
            contact_id (int): ID of the contact to update.
            body (ContactUpdate): Data to update the contact.
            user: The user to whom the contact belongs.

        Returns:
            Optional[Contact]: The updated contact object if found, else None.
        """
        return await self.contact_repository.update_contact(contact_id, body, user)

    async def remove_contact(self, contact_id: int, user: User):
        """
        Remove a contact by its ID for the given user.

        Args:
            contact_id (int): ID of the contact to remove.
            user: The user to whom the contact belongs.

        Returns:
            Optional[Contact]: The removed contact object if found, else None.
        """
        return await self.contact_repository.remove_contact(contact_id, user)

    async def get_upcoming_birthdays(self, user: User):
        """
        Retrieve contacts with upcoming birthdays within the next 7 days for the given user.

        Args:
            user: The user to whom the contacts belong.

        Returns:
            List[Contact]: List of contacts with upcoming birthdays.
        """
        return await self.contact_repository.get_upcoming_birthdays(user)

    async def update_phone(
        self, contact_id: int, phone: str, user: User
    ) -> Optional[Contact]:
        """
        Update the phone number of a contact for the given user.

        Args:
            contact_id (int): ID of the contact to update.
            phone (str): New phone number.
            user: The user to whom the contact belongs.

        Returns:
            Optional[Contact]: The updated contact object if found, else None.
        """
        return await self.contact_repository.update_phone(contact_id, phone, user)

    async def update_email(
        self, contact_id: int, email: str, user: User
    ) -> Optional[Contact]:
        """
        Update the email of a contact for the given user.

        Args:
            contact_id (int): ID of the contact to update.
            email (str): New email address.
            user: The user to whom the contact belongs.

        Returns:
            Optional[Contact]: The updated contact object if found, else None.
        """
        return await self.contact_repository.update_email(contact_id, email, user)
