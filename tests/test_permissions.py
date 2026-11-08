

def test_create_book_without_token(client):
    response = client.post("/books",
                       json={"title": "Война и мир",
                             "author_id": 1,
                             "price": 1000.0
                             }
                       )
    assert response.status_code == 401


def test_create_book_with_token(auth_client, test_user):
    response = auth_client.post("/books",
                       json={"title": "Война и мир",
                             "author_id": 1,
                             "price": 1000.0
                             }
                       )
    assert response.status_code == 201
    assert response.json()["created_by"] == test_user["id"]


def test_update_own_book(auth_client):
    author_response = auth_client.post("/authors",
                                       json={"name": "Лев Толстой",
                                             "bio":" Русский классик"}
                                       )
    assert author_response.status_code == 201
    author_id = author_response.json()["id"]



    create_book = auth_client.post("/books",
                                   json={"title": "Война и мир",
                                         "author_id": author_id,
                                         "price": 1000.0
                                         }
                                   )
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