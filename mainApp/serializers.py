from rest_framework import serializers
from mainApp.models import User, Post, Comment, Category, Ingredient
from .models import FoodExpiration

from rest_framework import serializers
from .models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # 프론트엔드에 전달할 필드 선택
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            social_login_provider = 'local'
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

# Comment 모델을 위한 시리얼라이저를 정의합니다.
class CommentSerializer(serializers.ModelSerializer):
    # SerializerMethodField는 get_<field_name> 메서드의 결과를 필드의 값으로 사용합니다.
    replies = serializers.SerializerMethodField()

    # 'replies' 필드의 값을 얻기 위한 메서드입니다.
    def get_replies(self, obj):
        # 현재 댓글 객체(obj)에 대댓글이 존재하는지 확인합니다.
        if obj.replies.exists():
            # 대댓글이 있다면, 대댓글들을 CommentSerializer를 사용하여 시리얼라이즈하고,
            return CommentSerializer(obj.replies.all(), many=True).data
        return []  # 대댓글이 없다면 빈 리스트를 반환합니다.

    class Meta:
        model = Comment  # 이 시리얼라이저가 사용할 모델을 지정합니다.
        fields = (
            "id",
            "content",
            "creation_date",
            "replies",
        )  # 시리얼라이징할 필드를 명시합니다.


# Post 모델을 위한 시리얼라이저를 정의합니다.
class PostSerializer(serializers.ModelSerializer):
    # 게시물에 대한 최상위 댓글만을 가져오기 위한 SerializerMethodField를 정의합니다.
    comments = serializers.SerializerMethodField()

    # 'comments' 필드의 값을 설정하기 위한 메서드입니다.
    def get_comments(self, post):
        # post에 연결된 최상위 댓글(부모 댓글이 없는 댓글)을 가져옵니다.
        comments = Comment.objects.filter(post=post, parent__isnull=True)
        # 가져온 댓글들을 CommentSerializer를 사용하여 시리얼라이즈합니다.
        return CommentSerializer(comments, many=True).data

    class Meta:
        model = Post  # 이 시리얼라이저가 사용할 모델을 지정합니다.
        fields = (
            "id",
            "title",
            "content",
            "comments",
        )

# Post 생성 및 업데이트 시리얼라이저
class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content")

# Comment 생성 및 업데이트 시리얼라이저
class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content", "post", "parent")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'user', 'category', 'name', 'quantity', 'unit', 'expiration_date']
# serializers.py
class FoodExpirationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodExpiration
        fields = '__all__'
        read_only_fields = ['user']  # 'user' 필드는 읽기 전용으로 설정

