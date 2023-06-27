from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from devopshobbies.api.pagination import LimitOffsetPagination
from devopshobbies.blog.models import Post, Subscription 
# from devopshobbies.blog.services import un
from devopshobbies.api.mixins import ApiAuthMixin

from drf_spectacular.utils import extend_schema


class SubscribeDetailApi(ApiAuthMixin, APIView):
    def delete(self, request, username):
        try:
            unsubscribe(user=request.user, username=username)
        except Exception as e:
            return Response(
                {"detail": "Database Error - " + str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class SubscribeApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit=10

    class InputSubSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=150)

    class OutputSubSerializer(serializers.ModelSerializer):
        username = serializers.SerializerMethodField("get_username")

        class Meta:
            model = Subscription
            fields = ['username']

        def get_username(self, subscription):
            return subscription.target.username
        
    @extend_schema(responses=OutputSubSerializer)
    def get(self, request):
        user=request.user
        query=get_subscribers(user=user)
        return get_paginated_response(
            request=request,
            pagination_class=self.Pagination,
            queryset=query,
            serializer_class=self.OutputSubSerializer,
            view=self,
        )
    
    @extend_schema(request=InputSubSerializer, responses=OutputSubSerializer)
    def post(self, request):
        serializer = self.InputSubSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            query = subscribe()
        except Exception as e:
            return Response(
                    f"Database Error {e}",
                    status=status.HTTP_400_REQUEST
                    )
        return Response(self.OutputSubSerializer(query).data)