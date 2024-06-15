from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from capstone_lll_backend import settings
from mainApp.views import (
    naver_login, naver_callback,
    kakao_login, kakao_callback,
    PostDetailView, CategoryListCreateView,
    IngredientDetailView, IngredientListCreateView,
    CommentDetailView, csrf_token, UserProfileView,
    upload_image, LoginView, SignupView,
    google_login, google_callback,
    PostListView, CommentListView,
    FoodExpirationListCreateView,
    FoodExpirationRetrieveUpdateDestroyView,
    FoodExpirationNearExpiryView,
)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  # JWT 토큰 발급 및 갱신 엔드포인트
                  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('accounts/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

                  # 사용자 프로필 엔드포인트
                  path('user/profile/', UserProfileView.as_view(), name='user-profile'),

                  # 회원가입 및 로그인 엔드포인트
                  path('accounts/signup/', SignupView.as_view(), name='signup'),
                  path('accounts/login/', LoginView.as_view(), name='login'),

                  # 구글 로그인 엔드포인트
                  path('accounts/google/login/', google_login, name='google_login'),
                  path('google/callback/', google_callback, name='google_callback'),

                  # 네이버 로그인 엔드포인트
                  path('accounts/naver/login/', naver_login, name='naver_login'),
                  path('accounts/naver/callback/', naver_callback, name='naver_callback'),

                  # 카카오 로그인 엔드포인트
                  path("accounts/kakao/login/", kakao_login, name='kakao_login'),
                  path("kakao/callback/", kakao_callback, name="kakao_callback"),

                  # 식품 유통기한 관리 엔드포인트
                  path('food/', FoodExpirationListCreateView.as_view(), name='food-list-create'),
                  path('food/<int:pk>/', FoodExpirationRetrieveUpdateDestroyView.as_view(), name='food-detail'),
                  path("food/nearfood/", FoodExpirationNearExpiryView.as_view(), name='food-near'),

                  # 게시물 관리 엔드포인트
                  path("posts/", PostListView.as_view(), name="list_posts"),  # 게시물 리스트 조회 및 생성
                  path("posts/<int:pk>/", PostDetailView.as_view(), name="detail_post"),  # 게시물 상세 조회, 업데이트, 삭제
                  path("posts/<int:post_id>/comments/", CommentListView.as_view(), name="list_comments"),  # 특정 게시물의 댓글 조회 및 생성
                  path("comments/<int:pk>/", CommentDetailView.as_view(), name="detail_comment"),  # 댓글 상세 조회, 업데이트, 삭제
                  path('categories/', CategoryListCreateView.as_view(), name='category_list_create'),
                  path('ingredients/', IngredientListCreateView.as_view(), name='ingredient_list_create'),
                  path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name='ingredient_detail'),

                  # 이미지 업로드 엔드포인트
                  path('upload/', upload_image, name='upload_image'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
