from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from devopshobbies.api.pagination import LimitOffsetPagination
from devopshobbies.blog.models import Post, Subscription 
# from devopshobbies.blog.services import un
from devopshobbies.api.mixins import ApiAuthMixin

class PostApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit=10

    class FilterSerializer(serializers.Serializer):
        title = serializers.CharField(required=False, max_length=100)
        search = serializers.CharField(required=False, max_length=100)
        created_at__range = serializers.CharField(required=False, max_length=100)
        author__in = serializers.CharField(required=False, max_length=100)
        slug = serializers.CharField(required=False, max_length=100)
        content = serializers.CharField(required=False, max_length=1000)

    class InputSerializer(serializers.Serializer):
        content = serializers.CharField(max_length=1000)
        title = serializers.CharField(max_length=100)

    class OutputSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")
        url = serializers.SerializerMethodField("get_url")
        class Meta:
            model=Post
            fields= ['url', 'title', 'author']

        def get_author(self, post):
            return post.author.email
        
        def get_url(self, post):
            request = self.context.get("request")
            path = reverse("api:blog:post_detail", args=(post.slug))
            return request.build_absolute_uri(path)
        
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try: 
            query = create_post(user=request.user, content=serializer.validated_data.get("content"), title=serializer.validated_data.get("title"))
        except Exception as e:
            