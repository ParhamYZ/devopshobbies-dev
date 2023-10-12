import pytest
from devopshobbies.users.models import BaseUser

@pytest.fixture
def new_user(db):
    return BaseUser.objects.create(username="MyName", password="1234", email="a@a.com")