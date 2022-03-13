# Since a single user is created during testing, we can use that
# user_id when testing the todos and todo routes

def test_todos_post_route(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/todos/<user_id>' route is requested (POST)
    THEN check that the response is valid:
        statuscode = 201 for user created or 409 if user exists
    """

    response = test_client.post('/todos/1', json={
        'title': 'Walk the dog',
        'date': '2022-03-13'
    })

    assert response.status_code == 201
    assert response.get_json() == {
        'id': 1,
        'user_id': 1,
        'title': 'Walk the dog',
        'date': '2022-03-13',
        'priority': 1,
        'completed': False,
    }


def test_todos_get_route(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/todos/<user_id>' route is requested (GET)
    THEN check that the response is valid:
        statuscode = 200 for user created or 409 if user exists
    """

    response = test_client.get('/todos/1')

    # Try to make a request with a user_id that has no todos
    expect_no_data = test_client.get('/todos/2')

    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0] == {
        'id': 1,
        'user_id': 1,
        'title': 'Walk the dog',
        'date': '2022-03-13',
        'priority': 1,
        'completed': False,
    }
    assert len(expect_no_data.get_json()) == 0


def test_todo_put_route(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/todo/<todo_id>' route is requested (PUT)
    THEN check that the response is valid:
        statuscode = 201 for user created or 409 if user exists
    """

    response = test_client.put('/todo/1', json={
        'title': 'do the dishes',
        'date': '2022-03-13',
        'priority': 2,
        'completed': True
    })

    # Send a request for a todo that doesn't exist (id = 2)
    expect_404 = test_client.put('/todo/2', json={
        'title': 'do the dishes',
        'date': '2022-03-13',
        'priority': 2,
        'completed': True
    })

    assert response.status_code == 200
    assert response.get_json() == {
        'id': 1,
        'user_id': 1,
        'title': 'do the dishes',
        'date': '2022-03-13',
        'priority': 2,
        'completed': True,
    }
    assert expect_404.status_code == 404


def test_todos_delete_route(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/todos/<user_id>' route is requested (POST)
    THEN check that the response is valid:
        statuscode = 201 for user created or 409 if user exists
    """

    response = test_client.delete('/todo/1')

    # Make a get request for todos to ensure that the todo was deleted
    expect_no_data = test_client.get('/todos/1')

    # Send a request for a todo that doesn't exist (id = 2)
    expect_404 = test_client.delete('/todo/2')

    assert response.status_code == 200
    assert len(expect_no_data.get_json()) == 0
    assert expect_404.status_code == 404
