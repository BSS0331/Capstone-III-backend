import os
import secrets
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework import status, generics, views, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone

from .models import Post, Comment, User, FoodExpiration, Category, Ingredient
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    PostSerializer, CommentSerializer, FoodExpirationSerializer, CommentCreateUpdateSerializer, CategorySerializer,
    IngredientSerializer, PostCreateUpdateSerializer
)

# Basic REST API test function
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def hello_rest_api(request):
    data = {'message': 'Hello, REST API!'}
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                user.last_login = timezone.now()
                user.save()
                login(request, user)
                return Response({'message': 'Login successful', 'email': email}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Google login and callback
@api_view(['GET'])
def google_login(request):
    client_id = settings.GOOGLE_CLIENT_ID
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    state = secrets.token_hex(16)
    request.session['oauth_state'] = state
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}"
        f"&response_type=code&scope=openid%20email%20profile&state={state}"
    )
    return redirect(auth_url)

@api_view(['GET'])
def google_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")

    if state != request.session.get('oauth_state'):
        return Response({'error': 'Invalid state parameter'}, status=status.HTTP_400_BAD_REQUEST)

    token_request = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.GOOGLE_REDIRECT_URI
        }
    )
    token_json = token_request.json()
    access_token = token_json.get("access_token")

    profile_request = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        params={'alt': 'json', 'access_token': access_token}
    )
    profile_json = profile_request.json()
    email = profile_json.get("email")
    name = profile_json.get("name")
    social_login_id = profile_json.get("id")

    user, created = User.objects.get_or_create(email=email)
    if created:
        user.username = name
        user.social_login_id = social_login_id
        user.social_login_provider = 'google'
    else:
        user.social_login_id = social_login_id
        user.social_login_provider = 'google'
    user.last_login = timezone.now()
    user.save()

    return Response({'id': user.id, 'email': email, 'name': name, 'token': access_token})

# Naver login and callback
@api_view(['GET'])
def naver_login(request):
    state = secrets.token_hex(16)
    request.session['oauth_state'] = state
    url = (
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={settings.NAVER_CLIENT_ID}"
        f"&redirect_uri={settings.NAVER_REDIRECT_URI}&state={state}"
    )
    print(url)
    return redirect(url)

@api_view(['GET'])
def naver_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    print(code)

    if state != request.session.get('oauth_state'):
        return Response({'error': 'Invalid state parameter'}, status=status.HTTP_400_BAD_REQUEST)

    if not code:
        return JsonResponse({'error': 'Code is missing'}, status=400)

    token_response = requests.post(
        "https://nid.naver.com/oauth2.0/token",
        data={
            'grant_type': 'authorization_code',
            'client_id': settings.NAVER_CLIENT_ID,
            'client_secret': settings.NAVER_SECRET_KEY,
            'code': code,
            'state': state
        }
    )
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    profile_response = requests.get(
        "https://openapi.naver.com/v1/nid/me",
        headers={'Authorization': f'Bearer {access_token}'}
    )
    profile_data = profile_response.json()
    response = profile_data.get('response', {})
    email = response.get('email')
    name = response.get('name')
    social_login_id = response.get('id')

    if not email:
        return Response({'error': 'Naver account does not have an email'}, status=status.HTTP_400_BAD_REQUEST)

    user, created = User.objects.get_or_create(email=email)
    if created:
        user.username = name
        user.social_login_id = social_login_id
        user.social_login_provider = 'naver'
    else:
        user.social_login_id = social_login_id
        user.social_login_provider = 'naver'
    user.last_login = timezone.now()
    user.save()


    return Response({'id': user.id, 'email': email, 'name': name, 'token': access_token})

# Kakao login and callback
@api_view(['GET'])
def kakao_login(request):
    auth_url = (
        f"https://kauth.kakao.com/oauth/authorize?client_id={settings.KAKAO_CLIENT_ID}"
        f"&redirect_uri={settings.KAKAO_REDIRECT_URI}&response_type=code"
    )
    return redirect(auth_url)

@api_view(['GET'])
def kakao_callback(request):
    code = request.GET.get("code")

    token_request = requests.post(
        "https://kauth.kakao.com/oauth/token",
        data={
            'grant_type': 'authorization_code',
            'client_id': settings.KAKAO_CLIENT_ID,
            'redirect_uri': settings.KAKAO_REDIRECT_URI,
            'code': code
        }
    )
    token_json = token_request.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return Response({'error': 'Failed to obtain access token from Kakao'}, status=status.HTTP_400_BAD_REQUEST)

    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    kakao_account = profile_json.get("kakao_account", {})
    email = kakao_account.get("email")
    profile = kakao_account.get("profile", {})
    name = profile.get("nickname")
    social_login_id = str(profile_json.get("id"))

    if not email:
        return Response({'error': 'Kakao account does not have an email'}, status=status.HTTP_400_BAD_REQUEST)

    user, created = User.objects.get_or_create(email=email)
    if created:
        user.username = name
        user.social_login_id = social_login_id
        user.social_login_provider = 'kakao'
    else:
        user.social_login_id = social_login_id
        user.social_login_provider = 'kakao'
    user.last_login = timezone.now()
    user.save()

    return Response({'id': user.id, 'email': email, 'name': name, 'token': access_token})
    return Response(data)

# User Signup API
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login API

# Post and Comment APIs
class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by("-creation_date")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)

# 게시물 상세 조회, 업데이트, 삭제 뷰
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateUpdateSerializer
        return PostSerializer

# 댓글 리스트 조회 및 생성 뷰
class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id, parent__isnull=True)

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)

# 댓글 상세 조회, 업데이트, 삭제 뷰
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CommentCreateUpdateSerializer
        return CommentSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Food Expiration APIs
class FoodExpirationListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodExpirationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FoodExpiration.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FoodExpirationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FoodExpirationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FoodExpiration.objects.filter(user=self.request.user)
