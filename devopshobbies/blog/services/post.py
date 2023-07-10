from django.db.models import QuerySet
from django.db import transaction
from django.utils.text import slugify
from django.core.cache import cache

from devopshobbies.blog.models import Post, Subscription
from devopshobbies.users.models import BaseUser


def count_subscribers(*, user:BaseUser) -> int:
    return Subscription.objects.filter(target=user).count()

def count_subscribings(*, user:BaseUser) -> int:
    return Subscription.objects.filter(subscriber=user).count()

def count_posts(*, user:BaseUser) -> int:
    return Post.objects.filter(author=user).count()

def cache_profile(*, user: BaseUser) -> None:
    profile = {
        "posts_count": count_posts(user=user),
        "subscribers_count": count_subscribers(user=user),
        "subscribings_count": count_subscribings(user=user),
    }
    cache.set(f"profile_{user.username}", profile, timeout=None)

def subscribe(*, user:BaseUser, username:str) -> QuerySet[Subscription]:
    target = BaseUser.objects.get(username=username)
    sub = Subscription(subscriber=user, target=target)
    sub.full_clean()
    sub.save()
    cache_profile(user=user)
    return sub

def unsubscribe(*, user:BaseUser, username:str) -> bool:
    target = BaseUser.objects.get(username=username)
    res = Subscription.objects.get(subscriber=user, target=target).delete()
    cache_profile(user=user)
    return res
    
@transaction.atomic
def create_post(*, user:BaseUser, title:str, content:str) -> QuerySet[Post]:
    post = Post.objects.create(author=user, title=title, content=content, slug=slugify(title))
    cache_profile(user=user)
    return post

