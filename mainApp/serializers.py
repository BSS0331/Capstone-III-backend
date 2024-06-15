from rest_framework import serializers
from mainApp.models import User, Post, Comment, Category, Ingredient
from .models import FoodExpiration
from .models import User
# 사용자 프로필 시리얼라이저
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']  # 프론트엔드에 전달할 필드 선택

# 사용자 등록 시리얼라이저
class UserRegistrationSerializer(serializers.ModelSerializer):
    # 비밀번호 필드는 쓰기 전용으로 설정합니다.
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')  # 사용자 등록 시 필요한 필드

    # 사용자 생성 메서드를 재정의합니다.
    def create(self, validated_data):
        # User 객체를 생성하고, 추가적으로 소셜 로그인 제공자를 'local'로 설정합니다.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            social_login_provider='local',  # 로컬 회원가입으로 설정
        )
        return user



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

# Comment 모델을 위한 시리얼라이저를 정의합니다.
class CommentSerializer(serializers.ModelSerializer):
    # 대댓글을 가져오기 위한 SerializerMethodField
    replies = serializers.SerializerMethodField()

    # 'replies' 필드의 값을 얻기 위한 메서드
    def get_replies(self, obj):
        # 현재 댓글 객체에 대댓글이 있는지 확인
        if obj.replies.exists():
            # 대댓글이 있으면, 대댓글들을 CommentSerializer를 사용하여 시리얼라이즈
            return CommentSerializer(obj.replies.all(), many=True).data
        return []  # 대댓글이 없으면 빈 리스트 반환

    class Meta:
        model = Comment  # 이 시리얼라이저가 사용할 모델 지정
        fields = (
            "id",  # 댓글 ID
            "content",  # 댓글 내용
            "creation_date",  # 댓글 생성 날짜
            "replies",  # 대댓글들
        )

# 게시글 모델을 위한 시리얼라이저
class PostSerializer(serializers.ModelSerializer):
    # 게시물에 대한 최상위 댓글을 가져오기 위한 SerializerMethodField
    comments = serializers.SerializerMethodField()

    # 'comments' 필드의 값을 설정하기 위한 메서드
    def get_comments(self, post):
        # post에 연결된 최상위 댓글(부모 댓글이 없는 댓글)을 가져옴
        comments = Comment.objects.filter(post=post, parent__isnull=True)
        # 가져온 댓글들을 CommentSerializer를 사용하여 시리얼라이즈
        return CommentSerializer(comments, many=True).data

    class Meta:
        model = Post  # 이 시리얼라이저가 사용할 모델 지정
        fields = (
            "id",  # 게시글 ID
            "title",  # 게시글 제목
            "content",  # 게시글 내용
            "comments",  # 최상위 댓글들
            "creation_date",  # 게시글 생성 날짜
        )

# 게시글 생성 및 업데이트 시리얼라이저
class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post  # 이 시리얼라이저가 사용할 모델 지정
        fields = ("title", "content")  # 시리얼라이징할 필드들

# 댓글 생성 및 업데이트 시리얼라이저
class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment  # 이 시리얼라이저가 사용할 모델 지정
        fields = ("content", "post", "parent")  # 시리얼라이징할 필드들

# 카테고리 모델을 위한 시리얼라이저
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category  # 이 시리얼라이저가 사용할 모델 지정
        fields = ['id', 'name']  # 시리얼라이징할 필드들

# 재료 모델을 위한 시리얼라이저
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient  # 이 시리얼라이저가 사용할 모델 지정
        fields = ['id', 'user', 'category', 'name', 'quantity', 'unit', 'expiration_date']  # 시리얼라이징할 필드들

# serializers.py
# FoodExpiration 모델 시리얼라이저
class FoodExpirationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodExpiration
        fields = '__all__'  # 모든 필드를 포함
        read_only_fields = ['user']  # 'user' 필드는 읽기 전용으로 설정

# 만료 임박 식품 조회를 위한 시리얼라이저
class FoodExpirationNearExpirySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodExpiration
        fields = ['food_name', 'expiration_date']  # 'food_name'과 'expiration_date' 필드만 포함
