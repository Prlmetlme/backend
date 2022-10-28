from django.shortcuts import render, get_object_or_404
from request_utils import user_from_access_token, get_engagement_data_or_400
from rest_framework.response import Response
from rest_framework.views import APIView
from Accounts.models import User
from .models import Post, Comment
from .serializer import PostSerializer
from Accounts.serializer import UserSerializer, ReadUserSerializer
from rest_framework.pagination import PageNumberPagination


class LikesHandler(APIView):
    def post(self, request):
        user:User = user_from_access_token(request)
        error = Response({"error": "Incorrect input. Please specify the 'type' 'id' and 'vote' in the body of the POST request and ensure the data is formatted correctly"}, status=400)
        type, id, vote = get_engagement_data_or_400(request)
        if type.lower() == 'post':
            match vote:
                case 'like':
                    if id in set(user.disliked_posts.all().values_list('post_ID', flat=True)):
                        user.disliked_posts.remove(
                            Post.objects.get(post_ID=id)
                        )
                    if id not in set(user.liked_posts.all().values_list('post_ID', flat=True)):
                        user.liked_posts.add(
                            get_object_or_404(Post, post_ID=id)
                        )
                        
                        return Response({}, status=201)
                    else:
                        user.liked_posts.remove(
                            # Post.objects.get(post_ID=id)
                            get_object_or_404(Post, post_ID=id)

                        )
                        return Response({}, status=201)
                case 'dislike':
                    if id in set(user.liked_posts.all().values_list('post_ID', flat=True)):
                        user.liked_posts.remove(
                            Post.objects.get(post_ID=id)
                        )
                    if id not in set(user.disliked_posts.all().values_list('post_ID', flat=True)):
                        user.disliked_posts.add(
                            # Post.objects.get(post_ID=id)
                            get_object_or_404(Post, post_ID=id)

                        )
                        return Response({}, status=201)
                    else:
                        user.disliked_posts.remove(
                            # Post.objects.get(post_ID=id)
                            get_object_or_404(Post, post_ID=id)

                        )
                        return Response({}, status=201)
                case _:
                    return error
        elif type.lower() == 'comment':
            match vote:
                case 'like':
                    if id in set(user.liked_comments.all()):
                        return Response({'yay': 'you did it right'})
                    else:
                        return Response({'yay': 'you did it wrong'})
                case 'dislike':
                    if id in set(user.disliked_comments.all()):
                        pass
                    else:
                        pass
                case _:
                    return error
        else:
            return Response({'error': 'All fields are here, but fields are invalid'}, status=400)

class UserPostHandler(APIView):
    def post(self, request):
        user:User = user_from_access_token(request)
        full_request = request.data
        # full_request['author'] = user
        serialized_post = PostSerializer(data=request.data)
        if serialized_post.is_valid(raise_exception=True):
            serialized_post.save(author=user)
            return Response(serialized_post.data, status=201)
        return Response({'post': {'serialized_post.data': 'invalid form'}}, status=400)

    def get(self, request, **kwargs):
        if kwargs.get('id'):            
            if kwargs.get('id') == 'all':
                user:User = user_from_access_token(request)
                user_serialized = UserSerializer(user)
                user_posts = Post.objects.filter(author=user)
                serialized = PostSerializer(user_posts, many=True)
                return Response(serialized.data)
            else:
                return Response({})
        else:
            paginator = PageNumberPagination()
            paginator.page_size = 5
            user:User = user_from_access_token(request)
            # user_serialized = UserSerializer(user)
            user_posts = Post.objects.filter(author=user)
            result_page = paginator.paginate_queryset(user_posts, request)
            serialized = PostSerializer(result_page, many=True)
            return paginator.get_paginated_response(serialized.data)

class CommentsHandler(APIView):
    def get(self, request):
        pass
