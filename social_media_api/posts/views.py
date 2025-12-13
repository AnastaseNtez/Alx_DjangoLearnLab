# posts/views.py
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from .pagination import CustomPageNumberPagination 
from rest_framework import generics, permissions

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

class FeedView(generics.ListAPIView):
    # Only authenticated users can see their feed
    permission_classes = [permissions.IsAuthenticated] 
    serializer_class = PostSerializer
    pagination_class = CustomPageNumberPagination # Use existing pagination

    def get_queryset(self):
        # 1. Get the list of users the current user is FOLLOWING
        followed_users = self.request.user.following.all()
        
        # 2. Get all posts where the author is in the followed_users list
        # Order by created_at descending (newest first)
        queryset = Post.objects.filter(author__in=followed_users).order_by('-created_at')
        
        return queryset