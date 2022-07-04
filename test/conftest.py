from flask_jwt_extended.utils import create_access_token
import pytest
from src.db.models import *
from src import create_app


@pytest.fixture(scope='module')
def new_user():
    user = User(username='Test', password='Test')
    return user


@pytest.fixture(scope='module')
def new_todo():
    todo = Todo(user_id=1, title='Walk the dog', date='2022-03-12')
    return todo


@pytest.fixture(scope='session')
def test_client():
    flask_app = create_app('flask_test.cfg')

    testing_client = flask_app.test_client()
    with flask_app.app_context():
        db.create_all()

        yield testing_client

        db.session.close()
        db.drop_all()
