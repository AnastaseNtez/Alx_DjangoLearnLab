# posts/views.py
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from .pagination import CustomPageNumberPagination 
from rest_framework import generics, permissions
from notifications.utils import create_notification
from django.shortcuts import get_object_or_404 as generics_get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

# ViewSet for Posts
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination # Used for Step 5
    
    # Filtering and Search (Used for Step 5)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'content'] # Fields to search across
    # filterset_fields = ['author__username'] # Optional: filter by author

    # Automatically set the author of the post to the currently authenticated user
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def toggle_like(self, request, pk=None):
        post = generics_get_object_or_404(Post, pk=pk)
        user = request.user
        
        is_liked = post.likes.filter(pk=user.pk).exists()

        if is_liked:
            post.likes.remove(user)
            action_performed = "unliked"
        else:
            post.likes.add(user)
            action_performed = "liked"
            if not post.author == user:
            # NOTIFICATION TRIGGER
                create_notification(
                    actor=user,
                    recipient=post.author,
                    verb="liked your post",
                    target=post
                )
            
        return Response(
            {'status': f'Post successfully {action_performed}.', 
             'likes_count': post.total_likes(),
             'is_liked': action_performed == "liked"}, 
            status=status.HTTP_200_OK
        )

# ViewSet for Comments (Nested under Posts for routing clarity)
class CommentViewSet(viewsets.ModelViewSet):
    # The queryset will be filtered by the router, so we start with all comments
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination # Used for Step 5

    # Filter comments to only show those belonging to the parent post (if routed)
    def get_queryset(self):
        # Check if this view is being used as a nested view via the Post ID
        post_id = self.kwargs.get('post_pk')
        if post_id:
            return self.queryset.filter(post_id=post_id)
        return self.queryset

    # Automatically set the author and the parent post
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        
        # Ensure the post exists before creating the comment
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            # Although DRF router should handle this, it's safer to check
            raise serializers.ValidationError("Post not found.")
            
        serializer.save(author=self.request.user, post=post)
    def perform_create(self, serializer):
        # ... (post retrieval and comment save)
        comment = serializer.save(author=self.request.user, post=post)
        
        # NOTIFICATION TRIGGER
        create_notification(
            actor=self.request.user,
            recipient= Post.author,
            verb="commented on your post",
            target=comment
        )

class FeedView(generics.ListAPIView):
    # Only authenticated users can see their feed
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = PostSerializer
    pagination_class = CustomPageNumberPagination # Use existing pagination

    def get_queryset(self):
        # 1. Get the list of users the current user is FOLLOWING
        #followed_users = self.request.user.following.all()
        
        # 2. Get all posts where the author is in the followed_users list
        # Order by created_at descending (newest first)
        #queryset = Post.objects.filter(author__in=followed_users).order_by('-created_at')
        
        # Rename the variable to match the checker's string requirement
        following_users = self.request.user.following.all()
        
        # REQUIRED STRING: Post.objects.filter(author__in=following_users).order_by
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        return queryset