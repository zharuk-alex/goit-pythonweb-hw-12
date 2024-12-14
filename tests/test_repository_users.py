import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import UserCreate
from src.repository.users import UserRepository


@pytest.mark.asyncio
async def test_get_user_by_email(async_session: AsyncSession):
    """
    Тест для перевірки отримання користувача за email.

    Args:
        async_session: Асинхронна сесія бази даних для тестування.

    Returns:
        None
    """
    test_email = "testuser@example.com"
    user_data = UserCreate(
        username="testuser", email=test_email, password="hashed_password", role="user"
    )
    user_repo = UserRepository(async_session)
    created_user = await user_repo.create_user(user_data)

    fetched_user = await user_repo.get_user_by_email(test_email)

    assert fetched_user is not None, "Користувач не знайдений"
    assert fetched_user.email == created_user.email, "Email користувача не збігається"
    assert (
        fetched_user.username == created_user.username
    ), "Ім'я користувача не збігається"
