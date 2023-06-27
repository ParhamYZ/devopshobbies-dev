from django.db.models import QuerySet
from django.db import transaction
from django.utils.text import slugify

from devopshobbies.blog.models import Post, Subscription
from devopshobbies.users.models import BaseUser


def count_subscribers(*, user:BaseUser) -> int:
    return Subscription.objects.filter(target=user).count()

def count_subscribings(*, user:BaseUser) -> int:
    return Subscription.objects.filter(subscriber=user).count()

def count_posts(*, user:BaseUser) -> int:
    return Post.objects.filter(author=user).count()

def subscribe(*, user:BaseUser, username:str) -> QuerySet[Subscription]:
    target = BaseUser.objects.get(username=username)
    sub = Subscription(subscriber=user, target=target)
    sub.full_clean()
    sub.save()
    return sub

def unsubscribe(*, user:BaseUser, username:str) -> bool:
    target = BaseUser.objects.get(username=username)
    return Subscription.objects.get(subscriber=user, target=target).delete()
    
@transaction.atomic
def create_post(*, user:BaseUser, title:str, content:str) -> QuerySet[Post]:
    return Post.objects.create(author=user, title=title, content=content, slug=slugify(title))

