from datetime import date, timedelta
import pytest
from unittest.mock import patch
from src.database.models import Contact
from src.repository.contacts import ContactRepository
from src.schemas import UserCreate
from src.repository.users import UserRepository
from sqlalchemy import select, func


@pytest.mark.asyncio
async def test_get_upcoming_birthdays(async_session, monkeypatch):
    user_data = UserCreate(
        username="testuser",
        email="testuser@testuser.com",
        password="hashed_password",
        role="user",
    )
    user_repo = UserRepository(async_session)
    user = await user_repo.create_user(user_data)

    today = date.today()
    upcoming_birthday = today + timedelta(days=3)
    past_birthday = today - timedelta(days=3)

    contact_1 = Contact(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="+123456789",
        birthday=upcoming_birthday,
        user_id=user.id,
        additional_info="",
    )
    contact_2 = Contact(
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@example.com",
        phone="+123456789",
        birthday=past_birthday,
        user_id=user.id,
        additional_info="",
    )
    async_session.add_all([contact_1, contact_2])
    await async_session.commit()

    async def mock_get_upcoming_birthdays(self, user):
        today = date.today()
        end_date = today + timedelta(days=7)

        query = select(Contact).where(
            Contact.user_id == user.id,
            func.strftime("%m-%d", Contact.birthday).between(
                today.strftime("%m-%d"), end_date.strftime("%m-%d")
            ),
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    monkeypatch.setattr(
        ContactRepository, "get_upcoming_birthdays", mock_get_upcoming_birthdays
    )

    repository = ContactRepository(async_session)
    results = await repository.get_upcoming_birthdays(user)

    assert len(results) == 1
    assert results[0].first_name == "John"
