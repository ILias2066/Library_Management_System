from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Тест на создание автора
def test_create_author():
    # Отправляем POST-запрос для создания нового автора
    response = client.post("/authors", json={"first_name": "John", "last_name": "Doe", "birth_date": "1980-01-01"})

    # Проверяем, что статус код 201, а не 200
    assert response.status_code == 201
    # Проверяем, что в ответе есть id
    author_data = response.json()
    assert "id" in author_data
    assert author_data["first_name"] == "John"
    assert author_data["last_name"] == "Doe"
    assert author_data["birth_date"] == "1980-01-01"


# Тест на создание книги
def test_create_book():
    # Для создания книги сначала создаем автора (предположим, что его id = 1)
    response = client.post("/authors", json={"first_name": "John", "last_name": "Doe", "birth_date": "1980-01-01"})
    author_id = response.json()["id"]

    # Создаем книгу с использованием созданного id автора
    response = client.post("/books",
                           json={"title": "Book Title", "description": "Book Description", "author_id": author_id,
                                 "available_copies": 5})

    # Проверяем, что статус код 201, а не 200
    assert response.status_code == 201
    # Проверяем, что в ответе есть id книги
    book_data = response.json()
    assert "id" in book_data
    assert book_data["title"] == "Book Title"
    assert book_data["description"] == "Book Description"
    assert book_data["author_id"] == author_id
    assert book_data["available_copies"] == 5
