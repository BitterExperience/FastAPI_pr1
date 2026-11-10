

def test_create_book_without_token(client):
    response = client.post("/books",
                       json={"title": "Война и мир",
                             "author_id": 1,
                             "price": 1000.0
                             }
                       )
    assert response.status_code == 401


def test_create_book_with_token(auth_client, test_user, create_author):
    author_id = create_author.json()["id"]
    response = auth_client.post("/books",
                       json={"title": "Война и мир",
                             "author_id": author_id,
                             "price": 1000.0
                             }
                       )
    assert response.status_code == 201
    assert response.json()["created_by"] == test_user["id"]


def test_update_own_book(auth_client, create_author, create_book):
    assert create_author.status_code == 201
    author_id = create_author.json()["id"]

    assert create_book.status_code == 201
    book_id = create_book.json()["id"]
    print("create_book response:", create_book.json())

    upd_book = auth_client.put(f"/books/{book_id}",
                               json={"title": "Осень",
                                     "author_id": author_id,
                                     "price": 900.0
                                     }
                               )
    print("upd_book response:", upd_book.json())
    assert upd_book.status_code == 200


def test_delete_own_book(auth_client, create_author, create_book):
    assert create_author.status_code == 201
    author_id = create_author.json()["id"]
    assert create_book.status_code == 201
    book_id = create_book.json()["id"]
    assert create_book.json()["author_id"] == author_id
    response_delete = auth_client.delete(f"/books/{book_id}")
    assert response_delete.status_code == 204