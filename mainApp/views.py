import os
import secrets
from datetime import date, timedelta

import requests
from django.contrib.messages.storage import default_storage
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
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware.csrf import get_token
from .models import Post, Comment, User, FoodExpiration, Category, Ingredient
from .serializers import UserProfileSerializer, FoodExpirationNearExpirySerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    PostSerializer, CommentSerializer, FoodExpirationSerializer, CommentCreateUpdateSerializer, CategorySerializer,
    IngredientSerializer, PostCreateUpdateSerializer
)

# CSRF 토큰을 반환하는 뷰
def csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


# 사용자 프로필 조회 뷰
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer #사용자의 이름과 이메일정보를 가져옴
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# 회원가입 뷰
class SignupView(APIView):
    # 이 뷰는 누구나 접근할 수 있도록 설정합니다.
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # 요청 데이터로 UserRegistrationSerializer를 초기화합니다.
        serializer = UserRegistrationSerializer(data=request.data)

        # 유효성 검사를 통과하면 사용자 정보를 저장합니다.
        if serializer.is_valid():
            user = serializer.save()
            # 사용자에 대한 JWT 리프레시 토큰을 생성합니다.
            refresh = RefreshToken.for_user(user)
            # 환영 메시지를 반환합니다.
            return Response({
                "hello world": "로그인 환영합니다.",
            }, status=status.HTTP_201_CREATED)

        # 유효성 검사에 실패하면 에러 메시지를 반환합니다.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인 뷰
class LoginView(APIView):
    # 이 뷰는 누구나 접근할 수 있도록 설정합니다.
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # 요청 데이터로 UserLoginSerializer를 초기화합니다.
        serializer = UserLoginSerializer(data=request.data)

        # 유효성 검사를 통과하면 이메일과 비밀번호를 추출합니다.
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            # 사용자를 인증합니다.
            user = authenticate(request, email=email, password=password)

            # 인증에 성공하면 사용자를 로그인시키고 JWT 토큰을 반환합니다.
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)

            # 인증에 실패하면 에러 메시지를 반환합니다.
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # 유효성 검사에 실패하면 에러 메시지를 반환합니다.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 구글 로그인 뷰
@api_view(['GET'])
def google_login(request):
    # CSRF 공격 방지를 위해 고유한 상태 토큰을 생성하고 세션에 저장합니다.
    state = secrets.token_hex(16)
    request.session['oauth_state'] = state
    # 구글 OAuth2 인증 URL을 생성합니다.
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        f"&response_type=code&scope=openid%20email%20profile&state={state}"
    )
    # 생성된 인증 URL을 출력합니다 (디버깅용).
    print(auth_url)
    # 사용자를 구글 로그인 페이지로 리디렉션합니다.
    return redirect(auth_url)

# 구글 로그인 콜백 뷰
@api_view(['GET'])
def google_callback(request):
    # 구글에서 반환된 인증 코드와 상태 토큰을 가져옵니다.
    code = request.GET.get("code")
    state = request.GET.get("state")

    # 세션에 저장된 상태 토큰과 반환된 상태 토큰을 비교하여 CSRF 공격을 방지합니다.
    if state != request.session.get('oauth_state'):
        return Response({'error': 'Invalid state parameter'}, status=status.HTTP_400_BAD_REQUEST)

    # 구글에 토큰을 요청합니다.
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
    # 액세스 토큰을 추출합니다.
    access_token = token_json.get("access_token")

    # 구글 API를 사용하여 사용자 정보를 가져옵니다.
    profile_request = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        params={'alt': 'json', 'access_token': access_token}
    )
    profile_json = profile_request.json()
    email = profile_json.get("email")
    name = profile_json.get("name")
    social_login_id = profile_json.get("id")

    # 이메일을 기반으로 사용자를 찾거나 새 사용자로 생성합니다.
    user, created = User.objects.get_or_create(email=email)
    if created:
        # 새 사용자의 경우 추가 정보를 설정합니다.
        user.username = name
        user.social_login_id = social_login_id
        user.social_login_provider = 'google'
    else:
        # 기존 사용자의 경우 소셜 로그인 정보를 업데이트합니다.
        user.social_login_id = social_login_id
        user.social_login_provider = 'google'
    # 마지막 로그인 시간을 업데이트합니다.
    user.last_login = timezone.now()
    user.save()

    # JWT 리프레시 토큰을 생성합니다.
    refresh = RefreshToken.for_user(user)
    # 리프레시 토큰과 액세스 토큰을 반환합니다.
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

# 네이버 로그인 뷰
@api_view(['GET'])
def naver_login(request):
    # CSRF 공격 방지를 위해 고유한 상태 토큰을 생성하고 세션에 저장합니다.
    state = secrets.token_hex(16)
    request.session['oauth_state'] = state
    # 네이버 OAuth2 인증 URL을 생성합니다.
    url = (
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={settings.NAVER_CLIENT_ID}"
        f"&redirect_uri={settings.NAVER_REDIRECT_URI}&state={state}"
    )
    # 사용자를 네이버 로그인 페이지로 리디렉션합니다.
    return redirect(url)

# 네이버 로그인 콜백 뷰
@api_view(['GET'])
def naver_callback(request):
    # 네이버에서 반환된 인증 코드와 상태 토큰을 가져옵니다.
    code = request.GET.get('code')
    state = request.GET.get('state')

    # 세션에 저장된 상태 토큰과 반환된 상태 토큰을 비교하여 CSRF 공격을 방지합니다.
    if state != request.session.get('oauth_state'):
        return Response({'error': 'Invalid state parameter'}, status=status.HTTP_400_BAD_REQUEST)

    # 인증 코드가 없는 경우 에러를 반환합니다.
    if not code:
        return JsonResponse({'error': 'Code is missing'}, status=400)

    # 네이버에 토큰을 요청합니다.
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
    # 액세스 토큰을 추출합니다.
    access_token = token_json.get('access_token')

    # 네이버 API를 사용하여 사용자 정보를 가져옵니다.
    profile_response = requests.get(
        "https://openapi.naver.com/v1/nid/me",
        headers={'Authorization': f'Bearer {access_token}'}
    )
    profile_data = profile_response.json()
    response = profile_data.get('response', {})
    email = response.get('email')
    name = response.get('name')
    social_login_id = response.get('id')

    # 네이버 계정에 이메일이 없는 경우 에러를 반환합니다.
    if not email:
        return Response({'error': 'Naver account does not have an email'}, status=status.HTTP_400_BAD_REQUEST)

    # 이메일을 기반으로 사용자를 찾거나 새 사용자로 생성합니다.
    user, created = User.objects.get_or_create(email=email)
    if created:
        # 새 사용자의 경우 추가 정보를 설정합니다.
        user.username = name
        user.social_login_id = social_login_id
        user.social_login_provider = 'naver'
    else:
        # 기존 사용자의 경우 소셜 로그인 정보를 업데이트합니다.
        user.social_login_id = social_login_id
        user.social_login_provider = 'naver'
    # 마지막 로그인 시간을 업데이트합니다.
    user.last_login = timezone.now()
    user.save()

    # JWT 리프레시 토큰을 생성합니다.
    refresh = RefreshToken.for_user(user)
    # 리프레시 토큰과 액세스 토큰을 반환합니다.
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

# 카카오 로그인 뷰
@api_view(['GET'])
def kakao_login(request):
    # 카카오 OAuth2 인증 URL을 생성합니다.
    auth_url = (
        f"https://kauth.kakao.com/oauth/authorize?client_id={settings.KAKAO_CLIENT_ID}"
        f"&redirect_uri={settings.KAKAO_REDIRECT_URI}&response_type=code"
    )
    # 사용자를 카카오 로그인 페이지로 리디렉션합니다.
    return redirect(auth_url)

# 카카오 로그인 콜백 뷰
@api_view(['GET'])
def kakao_callback(request):
    # 카카오에서 반환된 인증 코드를 가져옵니다.
    code = request.GET.get("code")

    # 카카오에 토큰을 요청합니다.
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
    # 액세스 토큰을 추출합니다.
    access_token = token_json.get("access_token")

    # 액세스 토큰을 얻지 못한 경우 에러를 반환합니다.
    if not access_token:
        return Response({'error': 'Failed to obtain access token from Kakao'}, status=status.HTTP_400_BAD_REQUEST)

    # 카카오 API를 사용하여 사용자 정보를 가져옵니다.
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

    # 카카오 계정에 이메일이 없는 경우 에러를 반환합니다.
    if not email:
        return Response({'error': 'Kakao account does not have an email'}, status=status.HTTP_400_BAD_REQUEST)

    # 이메일을 기반으로 사용자를 찾거나 새 사용자로 생성합니다.
    user, created = User.objects.get_or_create(email=email)
    if created:
        # 새 사용자의 경우 추가 정보를 설정합니다.
        user.username = name
        user.social_login_id = social_login_id
        user.social_login_provider = 'kakao'
    else:
        # 기존 사용자의 경우 소셜 로그인 정보를 업데이트합니다.
        user.social_login_id = social_login_id
        user.social_login_provider = 'kakao'
    # 마지막 로그인 시간을 업데이트합니다.
    user.last_login = timezone.now()
    user.save()

    # JWT 리프레시 토큰을 생성합니다.
    refresh = RefreshToken.for_user(user)
    # 리프레시 토큰과 액세스 토큰을 반환합니다.
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

# 게시글 목록 및 생성 뷰
class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by("-creation_date")  # 게시글을 생성 날짜 기준으로 정렬
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 인증된 사용자 또는 읽기 전용

    def perform_create(self, serializer):
        content = self.request.data.get('content', '')  # 요청 데이터에서 내용을 가져옴
        serializer.save(member=self.request.user, content=content)  # 게시글 생성 시 유저와 내용을 저장

# 게시글 상세, 수정 및 삭제 뷰
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()  # 모든 게시글 쿼리셋
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 인증된 사용자 또는 읽기 전용

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:  # 수정 요청일 경우
            return PostCreateUpdateSerializer
        return PostSerializer  # 조회 요청일 경우

# 댓글 목록 및 생성 뷰
class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 인증된 사용자 또는 읽기 전용

    def get_queryset(self):
        post_id = self.kwargs['post_id']  # URL에서 post_id를 가져옴
        return Comment.objects.filter(post_id=post_id, parent__isnull=True)  # 해당 게시글의 최상위 댓글만 가져옴

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)  # 댓글 생성 시 유저를 저장

# 댓글 상세, 수정 및 삭제 뷰
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()  # 모든 댓글 쿼리셋
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 인증된 사용자 또는 읽기 전용

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:  # 수정 요청일 경우
            return CommentCreateUpdateSerializer
        return CommentSerializer  # 조회 요청일 경우

# 카테고리 목록 및 생성 뷰
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()  # 모든 카테고리 쿼리셋
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 인증된 사용자 또는 읽기 전용

# 재료 목록 및 생성 뷰
class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()  # 모든 재료 쿼리셋
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 인증된 사용자 또는 읽기 전용

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # 재료 생성 시 유저를 저장

# 재료 상세, 수정 및 삭제 뷰
class IngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()  # 모든 재료 쿼리셋
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # 인증된 사용자 또는 읽기 전용

# 이미지 업로드 API 뷰
@api_view(['POST'])
def upload_image(request):
    file = request.FILES['file']  # 업로드된 파일 가져오기
    file_name = default_storage.save(file.name, file)  # 파일 저장
    file_url = default_storage.url(file_name)  # 파일 URL 가져오기
    return Response({'file_url': file_url}, status=201)  # 파일 URL 반환

# FoodExpiration 리스트 및 생성 뷰
class FoodExpirationListCreateView(generics.ListCreateAPIView):
    serializer_class = FoodExpirationSerializer
    # 인증된 사용자만 접근할 수 있도록 설정합니다.
    permission_classes = [IsAuthenticated]

    # 현재 인증된 사용자의 FoodExpiration 객체만 반환합니다.
    def get_queryset(self):
        return FoodExpiration.objects.filter(user=self.request.user)

    # 새로운 FoodExpiration 객체를 생성할 때, 현재 인증된 사용자를 설정합니다.
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# FoodExpiration 조회, 수정 및 삭제 뷰
class FoodExpirationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FoodExpirationSerializer
    # 인증된 사용자만 접근할 수 있도록 설정합니다.
    permission_classes = [IsAuthenticated]

    # 현재 인증된 사용자의 FoodExpiration 객체만 반환합니다.
    def get_queryset(self):
        return FoodExpiration.objects.filter(user=self.request.user)

    # FoodExpiration 객체를 삭제합니다.
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # FoodExpiration 객체를 삭제하는 로직을 수행합니다.
    def perform_destroy(self, instance):
        instance.delete()

# 만료 임박 식품 조회 뷰
class FoodExpirationNearExpiryView(generics.ListAPIView):
    serializer_class = FoodExpirationNearExpirySerializer
    # 인증된 사용자만 접근할 수 있도록 설정합니다.
    permission_classes = [IsAuthenticated]

    # 현재 인증된 사용자의 만료일이 7일 이내인 FoodExpiration 객체만 반환합니다.
    def get_queryset(self):
        user = self.request.user
        near_expiry_date = date.today() + timedelta(days=7)  # 7일 이내에 만료되는 식품 조회
        return FoodExpiration.objects.filter(user=user, expiration_date__lte=near_expiry_date)
