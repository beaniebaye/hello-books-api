from app.models.book import Book
from app import db

# tests for an empty list if there are no records in the database
def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

# tests GET /books/1 where book id 1 exists
def test_get_one_book(client, two_saved_books):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["id"] == 1
    assert response_body["title"] == "Ocean Book"
    assert response_body["description"] == "watr 4evr"

#tests GET /books/1 returns 404 code when book id 1 does not exist
def test_get_one_book_that_does_not_exist(client):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == None

# tests GET /books returns all books in db
def test_get_all_books_with_records(client, two_saved_books):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body[0]["id"] == 1
    assert response_body[0]["title"] == "Ocean Book"
    assert response_body[0]["description"] == "watr 4evr"
    assert response_body[1]["id"] == 2
    assert response_body[1]["title"] == "Mountain Book"
    assert response_body[1]["description"] == "i luv 2 climb rocks"

#tests POST /books returns 201
def test_post_books_returns_correct_response(client):
    # Act
    response = client.post('/books', json={'title': 'Island Book', 'description': 'go play acnh'})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["id"] == 1
    assert response_body["title"] == "Island Book"
    assert response_body["description"] == "go play acnh"

    new_book = Book.query.get(1)
    assert new_book
    assert new_book.id == 1
    assert new_book.title == "Island Book"
    assert new_book.description == "go play acnh"
