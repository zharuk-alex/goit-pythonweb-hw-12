def test_create_contact(client, get_token):

    new_contact = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+123456789",
        "birthday": "1990-01-01",
        "additional_info": "Friend from work",
    }

    response = client.post(
        "/api/contacts/",
        json=new_contact,
        headers={"Authorization": f"Bearer {get_token}"},
    )

    assert response.status_code == 201, f"Контакт не був створений, {response.json()}"

    data = response.json()
    assert data["first_name"] == new_contact["first_name"], "Невірне ім'я"
    assert data["last_name"] == new_contact["last_name"], "Невірне прізвище"
    assert data["email"] == new_contact["email"], "Невірна email"


def test_get_contacts(client, get_token):
    response = client.get(
        "/api/contacts/", headers={"Authorization": f"Bearer {get_token}"}
    )

    assert (
        response.status_code == 200
    ), f"Не вдалося отримати контакти, {response.json()}"

    data = response.json()
    assert isinstance(data, list), "Очікувався список контактів"
    assert len(data) > 0, "Список контактів порожній"

    contact = data[0]
    assert "id" in contact, "У контакту відсутній ідентифікатор"
    assert "first_name" in contact, "У контакту відсутнє ім'я"
    assert "last_name" in contact, "У контакту відсутнє прізвище"
    assert "email" in contact, "У контакту відсутній email"


def test_get_contact(client, get_token):
    contact_id = 1
    response = client.get(
        f"/api/contacts/{contact_id}",
        headers={"Authorization": f"Bearer {get_token}"},
    )

    assert response.status_code == 200, f"Контакт не був отриманий, {response.json()}"

    data = response.json()
    assert data["id"] == contact_id, "Невірний ID контакту"
    assert data["first_name"] == "John", "Невірне ім'я контакту"
    assert data["last_name"] == "Doe", "Невірне прізвище контакту"
    assert data["email"] == "john.doe@example.com", "Невірний email контакту"
    assert data["phone"] == "+123456789", "Невірний телефон контакту"
    assert data["birthday"] == "1990-01-01", "Невірна дата народження контакту"
    assert data["additional_info"] == "Friend from work", "Невірна додаткова інформація"


def test_get_contact_not_found(client, get_token):
    contact_id = 999

    response = client.get(
        f"/api/contacts/{contact_id}",
        headers={"Authorization": f"Bearer {get_token}"},
    )

    assert response.status_code == 404, response.text
    data = response.json()
    assert (
        data["detail"] == "Contact not found"
    ), f"Невірне повідомлення про помилку: {data['detail']}"


def test_update_contact(client, get_token):
    contact_id = 1

    new_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "phone": "+987654321",
        "birthday": "1985-05-15",
        "additional_info": "Updated contact information",
    }

    response = client.put(
        f"/api/contacts/{contact_id}",
        json=new_data,
        headers={"Authorization": f"Bearer {get_token}"},
    )

    assert response.status_code == 200, f"Контакт не був оновлений, {response.json()}"

    data = response.json()
    assert data["first_name"] == new_data["first_name"], "Невірне оновлене ім'я"
    assert data["last_name"] == new_data["last_name"], "Невірне оновлене прізвище"
    assert data["email"] == new_data["email"], "Невірний оновлений email"
    assert data["phone"] == new_data["phone"], "Невірний оновлений телефон"
    assert data["birthday"] == new_data["birthday"], "Невірна оновлена дата народження"
    assert (
        data["additional_info"] == new_data["additional_info"]
    ), "Невірна додаткова інформація"


def test_update_phone(client, get_token):
    contact_id = 1
    new_phone = "+987654321"

    response = client.patch(
        f"/api/contacts/{contact_id}/phone",
        json={"phone": new_phone},
        headers={"Authorization": f"Bearer {get_token}"},
    )

    assert response.status_code == 200, f"Телефон не був оновлений, {response.json()}"

    data = response.json()
    assert data["id"] == contact_id, "Невірний ID контакту"
    assert data["phone"] == new_phone, "Номер телефону не було оновлено"


def test_update_email(client, get_token):
    contact_id = 1
    new_email = "new.email@example.com"

    response = client.patch(
        f"/api/contacts/{contact_id}/email",
        json={"email": new_email},
        headers={"Authorization": f"Bearer {get_token}"},
    )

    assert response.status_code == 200, f"Email не був оновлений, {response.json()}"

    data = response.json()
    assert data["id"] == contact_id, "Невірний ID контакту"
    assert data["email"] == new_email, "Email не було оновлено"


def test_remove_contact(client, get_token):
    contact_id = 1
    response = client.delete(
        f"/api/contacts/{contact_id}", headers={"Authorization": f"Bearer {get_token}"}
    )

    assert response.status_code == 200, f"Контакт не був видалений, {response.json()}"

    data = response.json()
    assert data["id"] == contact_id, "Невірний ID видаленого контакту"
