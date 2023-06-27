from django.db.models import QuerySet
from devopshobbies.blog.models import Post, Subscription
from devopshobbies.blog.filters import PostFilter
from devopshobbies.users.models import BaseUser


def get_subscribings(*, user:BaseUser) -> QuerySet[Subscription]:
    return Subscription.objects.filter(subscriber=user)

def post_detail(*, slug:str, user:BaseUser, self_include:bool = True) -> QuerySet[Post]:
    subscriptions = list(Subscription.objects.filter(subscriber=user).values_list('target', flat=True))
    if self_include:
        subscriptions.append(user.id)
    return Post.objects.get(slug=slug, author__in=subscriptions)

def post_list(*, filters=None, user:BaseUser, self_include:bool = True) -> QuerySet[Post]:
    filters = filters or {}
    subscriptions = list(Subscription.objects.filter(subscriber=user).values_list('target', flat=True))
    if self_include:
        subscriptions.append(user.id)
    qs = Post.objects.filter(author__in=subscriptions)
    return PostFilter(filters, qs).qs

