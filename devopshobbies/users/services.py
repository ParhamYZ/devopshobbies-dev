from django.db import transaction 
from .models import BaseUser, Profile
from django.core.cache import cache

def create_profile(*, user:BaseUser, bio:str | None) -> Profile:
    return Profile.objects.create(user=user, bio=bio)

def create_user(*, email:str, password:str, username:str) -> BaseUser:
    return BaseUser.objects.create_user(email=email, password=password, username=username)


@transaction.atomic
def register(*, bio:str|None, email:str, password:str, username:str) -> BaseUser:

    user = create_user(email=email, password=password, username=username)
    create_profile(user=user, bio=bio)

    return user

def profile_count_update():
    profiles = cache.keys("profile_*")
    
    for profile_key in profiles:
        username = profile_key.replace("profile_", "")
        data = cache.get(profile_key)

        try:
            profile = Profile.objects.get(user__username=username)
            profile.posts_count = data.get("posts_count")
            profile.subscribers_count = data.get("subscribers_count")
            profile.subscribings_count = data.get("subscribings_count")
            profile.save()

        except Exception as e:
            print(e)