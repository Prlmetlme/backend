from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    # def set_author(self, validated_data):
    #     user = models.User.objects.filter(static_user_id=validated_data.get(
    #         'static_user_id', None
    #     ))
    #     seralized_user = ReadUserSerializer(user)
    #     author = seralized_user.data.pop('username')
    #     return author
    likes = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()
    disliked_by = serializers.SerializerMethodField()

    def get_likes(self, instance):
        return len(instance.liked_by.all()) - len(instance.disliked_by.all())
    def get_liked_by(self, instance):
        users_that_liked = set(instance.liked_by.filter(privated=False).values_list('username', flat=True))
        return users_that_liked
    def get_disliked_by(self, instance):
        users_that_disliked = set(instance.disliked_by.filter(privated=False).values_list('username', flat=True))
        return users_that_disliked

    class Meta:
        model = Post
        fields = '__all__'


    # author = serializers.SerializerMethodField('get_author_username')

    # def get_author_username(self, obj):
        # return obj.author.username

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'