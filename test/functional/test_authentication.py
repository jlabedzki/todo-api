def test_registration_route_with_fixture(test_client):
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

# def test_login_route_with_fixture(test_client):
