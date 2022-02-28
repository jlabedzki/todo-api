from src.db.models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username and password fields are defined correctly
    """

    user = User(username='Test', password='Test')
    assert user.username == 'Test'
    # The password should be hashed hence the != operator
    assert user.password != 'Test'
