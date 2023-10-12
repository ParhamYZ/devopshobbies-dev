from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from devopshobbies.users.tests.factories import UserFactory
from devopshobbies.blog import models

faker = Faker()

class PostFactory(DjangoModelFactory):
    author = SubFactory(UserFactory)
    content = faker.text()
    title = faker.word()
    class Meta:
        model = models.Post

class SubscriptionFactory(DjangoModelFactory):
    subscriber = SubFactory(UserFactory)
    target = SubFactory(UserFactory)
    class Meta:
        model = models.Subscription
