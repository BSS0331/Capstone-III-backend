from pathlib import Path

# 기본 디렉토리 설정
BASE_DIR = Path(__file__).resolve().parent.parent

# 보안 설정
SECRET_KEY = 'django-insecure-7@m8fafl@j#gv_h9hc9@ei&0qx7-x$_(ui9&ctz(z42__(x=f='
DEBUG = True

# 호스트 및 프론트엔드 URL 설정
ALLOWED_HOSTS = ['*']
FRONTEND_URL = 'http://localhost:19006'

# 설치된 애플리케이션
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.naver',
    'corsheaders',
    'mainApp',  # 프로젝트의 메인 애플리케이션
]

# 미들웨어 설정
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
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
        'NAME': 'caps3',
        'USER': 'kim11',
        'PASSWORD': 'qwer1234@',
        'HOST': '180.66.65.21',
        'PORT': '3306',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'caps3',
#         'USER': 'root',
#         'PASSWORD': 'wt505033@#',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

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
    'allauth.account.auth_backends.AuthenticationBackend',
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
            'client_id': '32157736725-r5nop4snh9gf76a6unu1touq9hfhj2ep.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    },
    'naver': {
        'APP': {
            'client_id': 'DjGy6lYaL3QrYEe5jA8v',
            'secret': '3cm1u9Dye9',
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
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# OAuth 리디렉션 URI 설정
GOOGLE_REDIRECT_URI = 'http://localhost:8000/google/callback/'
GOOGLE_CLIENT_ID = "32157736725-r5nop4snh9gf76a6unu1touq9hfhj2ep.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
NAVER_REDIRECT_URI = 'http://localhost:8000/accounts/naver/login/callback/'
NAVER_CLIENT_ID = 'DjGy6lYaL3QrYEe5jA8v'
NAVER_SECRET_KEY = '3cm1u9Dye9'