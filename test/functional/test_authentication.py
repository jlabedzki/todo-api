def test_registration_route(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' route is requested (POST)
    THEN check that the response is valid:
        statuscode = 201 for user created or 409 if user exists
    """

    # This user shouldn't exist yet so we should receive a 201 from the API
    good_response = test_client.post('/register', json={
        'username': 'test', 'password': 'asdf'
    })

    # Attempting to create the same user again should yield a 409 response
    bad_response = test_client.post('/register', json={
        'username': 'test', 'password': 'asdf'
    })

    assert good_response.status_code == 201
    assert bad_response.status_code == 409


def test_login_route(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' route is requested (POST)
    THEN check that the response is valid:
        if successful, user_id is returned as well as 200 status code
        if wrong password, 401 status returned
        if no user, 404 status returned
    """

    # Using user data generated from register test above
    good_response = test_client.post('/login', json={
        'username': 'test', 'password': 'asdf'
    })

    bad_response_forbidden = test_client.post('/login', json={
        'username': 'test', 'password': 'notasdf'
    })

    bad_response_not_found = test_client.post('/login', json={
        'username': 'notfound', 'password': 'asdf'
    })

    assert good_response.status_code == 200
    assert good_response.get_json()['user_id'] == 1
    assert good_response.get_json()['username'] == 'test'
    assert bad_response_forbidden.status_code == 401
    assert bad_response_not_found.status_code == 404


def test_logout_route(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' route is requested (GET)
    THEN check that the response is valid:
        200 response for valid logout
    """

    response = test_client.get('/logout')

    # Need to login again so todo routes don't fail
    test_client.post('/login', json={
        'username': 'test', 'password': 'asdf'
    })

    assert response.status_code == 200
