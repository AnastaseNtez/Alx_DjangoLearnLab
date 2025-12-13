# posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment
from accounts.serializers import UserProfileSerializer # Reuse the profile serializer

# Comment Serializer (Must come first as it's used by the Post serializer)
class CommentSerializer(serializers.ModelSerializer):
    # Use a read-only field to show the author's username instead of ID
    author_username = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Comment
        # Exclude 'post' in creation, but include it in list/retrieve
        fields = ('id', 'post', 'author', 'author_username', 'content', 'created_at', 'updated_at')
        read_only_fields = ('author', 'post') # Author and post are set automatically

class PostSerializer(serializers.ModelSerializer):
    # Nested field to show the author's username
    author_username = serializers.ReadOnlyField(source='author.username')
    # Nested representation of comments (read-only for list/detail views)
    comments = CommentSerializer(many=True, read_only=True)
    # Count of comments
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = (
            'id', 'author', 'author_username', 'title', 'content', 
            'comments', 'comments_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('author',) # Author is set automatically

    def get_comments_count(self, obj):
        return obj.comments.count()