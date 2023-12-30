from rest_framework import serializers
from .models import *
from accounts.serializers import UserSerializer 

class TopicsSerializer(serializers.ModelSerializer):
    num_blogs = serializers.SerializerMethodField()
    class Meta:
        model=Topics
        fields='__all__'
    def get_num_blogs(self, topic):
        return topic.blogs.count() 


class Blogserializer(serializers.ModelSerializer):
    user_id = UserSerializer(required = False)
    topic = TopicsSerializer(required = False, read_only=True)
    class Meta:
        model=Blogs
        fields = '__all__'


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = '__all__'


class CommunityCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model=Community
        fields='__all__'

class CommunitySerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)

    class Meta:
        model=Community
        fields='__all__'






class CommentSerializer(serializers.ModelSerializer):
    user=UserSerializer(required=False)
    class Meta:
        model=Comments
        fields='__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=Comments
        fields='__all__'


class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields='__all__'


class ReportBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model=Report_blog
        fields='__all__'

class ReportListSerializer(serializers.ModelSerializer):
    user=UserSerializer(required=False)
    blog=Blogserializer(required=False)
    class Meta:
        model=Report_blog
        fields='__all__'
        


class SavedCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model=SavedBlogs
        fields='__all__'


class SavedListSerializer(serializers.ModelSerializer):
    blog=Blogserializer(read_only=True)
    class Meta:
        model=SavedBlogs
        fields='__all__'
