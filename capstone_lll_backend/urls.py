from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from capstone_lll_backend import settings
from mainApp.views import hello_rest_api, naver_login, naver_callback, kakao_login, kakao_callback, PostDetailView, \
    CategoryListCreateView, IngredientDetailView, IngredientListCreateView, CommentDetailView, csrf_token, \
    UserProfileView, upload_image
from mainApp.views import LoginView
from mainApp.views import SignupView
from django.contrib import admin
from django.urls import path,include
from mainApp.views import google_login,google_callback
from mainApp.views import (
    PostListView,  # 모든 포스트를 리스트하는 뷰
    CommentListView,  # 특정 포스트에 대한 댓글을 리스트하는 뷰
    FoodExpirationListCreateView,
    FoodExpirationRetrieveUpdateDestroyView,
    FoodExpirationNearExpiryView,
    # api_posts,
)


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/hello/', hello_rest_api, name='hello_rest_api'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('accounts/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    #로그인
    # path('accounts/', include('allauth.urls')),
    # path('api/csrf_token/', csrf_token, name='csrf_token'),
    path('accounts/signup/', SignupView.as_view(), name='signup'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/google/login/', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    path('accounts/naver/login/', naver_login, name='naver_login'),
    path('accounts/naver/callback/', naver_callback, name='naver_callback'),
    path("kakao/callback/",kakao_callback,name="kakao_callback"),
    path("accounts/kakao/login/", kakao_login, name='kakao_login'),
    #food
    path('food/', FoodExpirationListCreateView.as_view(), name='food-list-create'),
    path('food/<int:pk>/', FoodExpirationRetrieveUpdateDestroyView.as_view(), name='food-detail'),

    path("food/nearfood/", FoodExpirationNearExpiryView.as_view(), name='food-near'),
    #post
    path("posts/", PostListView.as_view(), name="list_posts"),  # 게시물 리스트 조회 및 생성 URL
    path("posts/<int:pk>/", PostDetailView.as_view(), name="detail_post"),  # 게시물 상세 조회, 업데이트, 삭제 URL
    path("posts/<int:post_id>/comments/", CommentListView.as_view(), name="list_comments"),  # 특정 게시물의 댓글 조회 및 생성 URL
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="detail_comment"),  # 댓글 상세 조회, 업데이트, 삭제 URL
    path('categories/', CategoryListCreateView.as_view(), name='category_list_create'),
    path('ingredients/', IngredientListCreateView.as_view(), name='ingredient_list_create'),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name='ingredient_detail'),
    path('upload/', upload_image, name='upload_image'),  # 이미지 업로드 URL

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

