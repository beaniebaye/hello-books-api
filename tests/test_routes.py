

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
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }

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
    assert response_body == [{
        'id': 1,
        'title': 'Ocean Book',
        'description': 'watr 4evr'
    }, {
        'id': 2,
        'title': 'Mountain Book',
        'description': 'i luv 2 climb rocks'
    }]

#tests POST /books returns 201
def test_post_books_returns_correct_response(client):
    # Act
    response = client.post('/books', json={'title': 'Island Book', 'description': 'go play acnh'})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
