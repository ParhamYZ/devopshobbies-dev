from factory.django import DjangoModelFactory
from faker import Faker

from ..models import BaseUser

faker = Faker()

class UserFactory(DjangoModelFactory):
    username = faker.name()
    password = faker.password()
    email = faker.email()
    is_admin = False
    class Meta:
        model = BaseUser