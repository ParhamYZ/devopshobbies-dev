from django_filters import CharFilter, FilterSet
from django.contrib.postgres.search import SearchVector
from django.utils import timezone
from devopshobbies.blog.models import Post
from rest_framework.exceptions import APIException

class PostFilter(FilterSet):
    search = CharFilter(method="filter_search")
    author__in = CharFilter(method="filter_author__in")
    created_at__range = CharFilter(method="filter_created_at__range")

    def filter_author__in(self, queryset, value):
        limit = 10
        authors = value.split(",")
        if len(authors) > limit:
            raise APIException(f"You cannot add more than {len(authors)} usernames")
        return queryset.filter(author__username__in=authors)
    
    def filter_created_at__range(self, queryset, value):
        created_at__range = value.split(",")
        if len(created_at__range) > 2:
            raise APIException(f"Please just add two created_at with , in middle")
            
        if len(created_at__range) == 2:
            return queryset.filter(created_at__date__range=(created_at__range[0], created_at__range[1]))

        if len(created_at__range) == 1:
            return queryset.filter(created_at__date__lt=created_at__range[0])

        return queryset 

    def filter_search(self, queryset, value):
        return queryset.annotate(search=SearchVector("title")).filter(search=value)
    
    class Meta:
        model = Post
        fields = ["slug", "title"]