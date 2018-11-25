from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

from .models import Post, Like
from .serializers import PostSerializer

class PostViewSet(viewsets.ViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        #serialize data from request
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        #define user as author of post
        serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_post(self, request, pk=None):
        """Get a certain post"""
        #get post from queryset
        data = get_object_or_404(self.queryset, pk=pk)

        #serialize post and respond to client
        serializer = self.serializer_class(data=model_to_dict(data))
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_post_list(self, request):
        """Get all posts"""
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def like_post(self, request, pk=None):
        """An endpoint that provides like and unlike certain post"""
        #at first check whether a post exist
        try:
            Post.objects.get(id=pk)
        except Post.DoesNotExist:
            #if it doesn't, send status 404
            return Response(status=status.HTTP_404_NOT_FOUND)

        #then check whether like already set
        try:
            #if it set, remove the like
            Like.objects.get(user=request.user, post=pk).delete()
            data = {'response': 'Post №%s has been unliked.' % pk}
        except Like.DoesNotExist:
            #otherwise set the like
            like = Like.objects.create(user=request.user, post=Post.objects.get(id=pk))
            like.save()
            data = {'response': 'Post №%s has been liked.' % pk}

        #respond to client about done action
        return Response(data, status=status.HTTP_200_OK)