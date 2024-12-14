from unittest.mock import AsyncMock, patch
import pytest
from src.services.email import send_email
from fastapi_mail.errors import ConnectionErrors


@pytest.mark.asyncio
async def test_send_email_success():
    # Мокаємо залежності
    with patch(
        "src.services.email.create_email_token", return_value="mocked_token"
    ) as mock_token, patch("src.services.email.FastMail") as MockFastMail:
        mock_send_message = AsyncMock()
        MockFastMail.return_value.send_message = mock_send_message

        # Викликаємо функцію
        await send_email("test@example.com", "TestUser", "http://localhost")

        # Перевіряємо виклики
        mock_token.assert_called_once_with({"sub": "test@example.com"})
        mock_send_message.assert_awaited_once()


@pytest.mark.asyncio
async def test_send_email_token_generation_error():
    with patch(
        "src.services.email.create_email_token", side_effect=Exception("Token error")
    ):
        with pytest.raises(Exception, match="Token error"):
            await send_email("test@example.com", "TestUser", "http://localhost")


@pytest.mark.asyncio
async def test_send_email_connection_error():
    with patch("src.services.email.FastMail") as MockFastMail, patch(
        "builtins.print"
    ) as mock_print:

        mock_send_message = AsyncMock(
            side_effect=ConnectionErrors("Simulated connection error")
        )
        MockFastMail.return_value.send_message = mock_send_message

        await send_email("test@example.com", "TestUser", "http://localhost")

        mock_print.assert_called_once()
        printed_message = mock_print.call_args[0][0]

        assert "Simulated connection error" in str(printed_message)
