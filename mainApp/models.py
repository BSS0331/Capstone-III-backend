from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    objects = CustomUserManager()
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)  # 이미 해시된 비밀번호라고 가정
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    # Django가 사용자 모델에 대해 필요로 하는 필드
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    social_login_id = models.CharField(max_length=100, null=True, blank=True)
    social_login_provider = models.CharField(max_length=20, null=True, blank=True)
    # 사용자의 'username' 필드를 'email' 필드로 사용하도록 설정
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # 여기에 사용자 모델 관리를 위한 매니저 클래스를 추가할 수 있습니다.
    # objects = CustomUserManager()
    def __str__(self):
        return self.email

    # 여기에 필요한 메소드를 추가합니다.
    # 예를 들어, 'is_staff'나 'has_perm' 같은 메소드를 추가해야 할 수도 있습니다.


# 게시물을 나타내는 모델입니다.
class Post(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=255)  # 게시물의 제목
    content = models.TextField()  # 게시물의 내용 (이미지 URL 포함)
    creation_date = models.DateTimeField(auto_now_add=True)  # 게시물의 생성 날짜

    def __str__(self):
        return self.title

# 댓글을 나타내는 모델입니다.
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)  # 댓글이 달린 게시물
    member = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)  # 댓글을 작성한 회원
    parent = models.ForeignKey("self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE)  # 대댓글 기능
    content = models.TextField()  # 댓글의 내용
    creation_date = models.DateTimeField(auto_now_add=True)  # 댓글의 생성 날짜

    def __str__(self):
        return f"Comment by {self.member.email} on {self.post.title}"

# 카테고리를 나타내는 모델입니다.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# 식자재를 나타내는 모델입니다.
class Ingredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20)
    expiration_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

# 사용자 생성 시 토큰을 생성하는 신호 수신기
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)





#유통기한
class FoodExpiration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 기본값으로 사용자 ID 1을 설정
    food_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField()
    purchase_date = models.DateField()
    expiration_date = models.DateField()
    storage_condition = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.food_name
