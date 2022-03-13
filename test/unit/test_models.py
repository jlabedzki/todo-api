def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username and password fields are defined correctly
    """

    assert new_user.username == 'Test'
    # The password should be hashed hence the != operator
    assert new_user.password != 'Test'


def test_new_todo_with_fixture(new_todo):
    """
    GIVEN a Todo model
    WHEN a new Todo is created
    THEN check the that the title and date fields are defined properly
    and that the priority and completed fields are automatically set correctly
    """

    assert new_todo.user_id == 1
    assert new_todo.title == "Walk the dog"
    assert new_todo.date == "2022-03-12"
    assert new_todo.priority == 1
    assert new_todo.completed == False
