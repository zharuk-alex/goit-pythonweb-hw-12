from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.repository.users import UserRepository
from src.schemas import UserCreate


class UserService:
    """
    Service class to handle operations related to Users.

    Args:
        db (AsyncSession): Database session to perform operations.
    """

    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create_user(self, body: UserCreate):
        """
        Create a new user.

        Args:
            body (UserCreate): Data for creating a new user.
            avatar (Optional[str]): URL of the user's avatar.

        Returns:
            User: The created user object.
        """
        avatar = None
        try:
            g = Gravatar(body.email)
            avatar = g.get_image()
        except Exception as e:
            print(e)

        return await self.repository.create_user(body, avatar)

    async def get_user_by_id(self, user_id: int):
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): ID of the user to retrieve.

        Returns:
            Optional[User]: The user object if found, else None.
        """
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str):
        """
        Retrieve a user by their username.

        Args:
            username (str): Username of the user to retrieve.

        Returns:
            Optional[User]: The user object if found, else None.
        """
        return await self.repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str):
        """
        Retrieve a user by their email address.

        Args:
            email (str): Email of the user to retrieve.

        Returns:
            Optional[User]: The user object if found, else None.
        """
        return await self.repository.get_user_by_email(email)

    async def confirmed_email(self, email: str):
        return await self.repository.confirmed_email(email)

    async def update_avatar_url(self, email: str, url: str):
        return await self.repository.update_avatar_url(email, url)
