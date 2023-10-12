from fixtures import new_user
import factories
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse


def test_by_fixtures(new_user):
    assert new_user.username == "MyName"

def test_by_factories(db):
    post = factories.PostFactory(title="First Post")
    assert post.title == "First Post"

class PostDetailApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = factories.UserFactory(username="AmirBahador", email="a@a.com")
        cls.subscriber = factories.UserFactory()
        cls.subscription = factories.SubscriptionFactory(subscriber=cls.subscriber, target=cls.user)
        cls.post1 = factories.PostFactory(author=cls.user)
        cls.post2 = factories.PostFactory(author=cls.user)

    def setUp(self) -> None:
        self.client.force_authenticate(self.user)
    
    def test_urls(self):
        self.assertEqual("/api/blog/post/post_slug", reverse("api:blog:post_detail", ["post_slug"]))

    def test_retrieve(self):
        res = self.client.get(reverse("api:blog:post_detail", [self.post1.slug]))
        self.assertEqual(status.HTTP_200_OK, res.status_code)

        self.assertEqual(res.data["slug"], self.post1.slug)
        self.assertEqual(res.data["author"], self.post1.author.username)
        self.assertEqual(res.data["content"], self.post1.content)
        self.assertEqual(res.data["title"], self.post1.title)

