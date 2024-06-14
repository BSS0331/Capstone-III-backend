from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key

# 기본 디렉토리 설정
BASE_DIR = Path(__file__).resolve().parent.parent
# .env 파일의 경로를 설정합니다.
load_dotenv()

# 보안 설정
# SECRET_KEY = os.getenv('SECRET_KEY')

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', get_random_secret_key())
DEBUG = True

# 호스트 및 프론트엔드 URL 설정
ALLOWED_HOSTS = ['*']
FRONTEND_URL = 'http://localhost:19006'

# 설치된 애플리케이션
INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'corsheaders',
    'mainApp',  # 프로젝트의 메인 애플리케이션
]

# 미들웨어 설정
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # 추가
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# URL 설정
ROOT_URLCONF = 'capstone_lll_backend.urls'

# 템플릿 설정
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI 애플리케이션 설정
WSGI_APPLICATION = 'capstone_lll_backend.wsgi.application'

# 데이터베이스 설정
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# 비밀번호 검증기
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# settings.py

AUTH_USER_MODEL = 'mainApp.User'  # 'your_app_name'은 User 모델이 정의된 앱의 이름입니다.

# 인증 및 권한 부여 설정
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
# 소셜 계정 제공자 설정
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online'
        },
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'key': ''
        }
    },
    'naver': {
        'APP': {
            'client_id': os.getenv('NAVER_CLIENT_ID'),
            'secret': os.getenv('NAVER_SECRET_KEY'),
            'key': ''
        }
    },
}

# 리디렉션 URL 설정
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# 사이트 ID 설정
SITE_ID = 1

# 국제화 설정
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# CORS 설정
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:19000',
]

# 정적 파일 URL
STATIC_URL = 'static/'

# 기본 자동 필드 설정
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST 프레임워크 설정
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',

    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'ROTATE_REFRESH_TOKENS': True,
}

# OAuth 리디렉션 URI 설정
load_dotenv()

# 환경 변수 사용


GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
NAVER_REDIRECT_URI = os.getenv('NAVER_REDIRECT_URI')
NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_SECRET_KEY = os.getenv('NAVER_SECRET_KEY')
KAKAO_API = os.getenv('KAKAO_API')
KAKAO_REDIRECT_URI = os.getenv('KAKAO_REDIRECT_URI')
KAKAO_CLIENT_ID = os.getenv('KAKAO_CLIENT_ID')

