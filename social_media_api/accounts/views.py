# accounts/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from .models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

# Registration View (using generics.CreateAPIView for simplicity)
class RegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    # Allow anyone to access the registration endpoint
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Manually get the created user instance
        user = serializer.instance
        # Create or get the token for the new user
        token, created = Token.objects.get_or_create(user=user)

        # Return the user data and the token
        return Response({
            "user": serializer.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

# Login View (using APIView for custom login logic)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Get or create the token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        }, status=status.HTTP_200_OK)

# User Profile View (using generics.RetrieveUpdateAPIView for GET/PUT/PATCH)
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    # Only authenticated users can access and modify their profile
    permission_classes = [permissions.IsAuthenticated]

    # Override get_object to ensure a user can only view/edit their own profile
    def get_object(self):
        # Use the currently authenticated user
        return self.request.user
    
User = get_user_model()

class FollowToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user == user_to_follow:
            return Response(
                {"detail": "You cannot follow yourself."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if already following
        is_following = request.user.following.filter(pk=user_id).exists()

        if is_following:
            # Unfollow (remove the user from the current user's 'following' set)
            request.user.following.remove(user_to_follow)
            action = "unfollowed"
        else:
            # Follow (add the user to the current user's 'following' set)
            request.user.following.add(user_to_follow)
            action = "followed"

        return Response(
            {"detail": f"Successfully {action} {user_to_follow.username}.", "action": action},
            status=status.HTTP_200_OK
        )