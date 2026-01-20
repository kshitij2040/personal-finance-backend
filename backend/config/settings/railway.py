"""
Production settings for Railway deployment.
"""
import os
import dj_database_url
from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Allow Railway and your frontend domains
ALLOWED_HOSTS = [
    '.railway.app',
    'localhost',
    '127.0.0.1',
    os.environ.get('RAILWAY_STATIC_URL', ''),
]

# If you have a custom domain, add it to environment variables
if 'ALLOWED_HOST' in os.environ:
    ALLOWED_HOSTS.append(os.environ['ALLOWED_HOST'])

# Database configuration for Railway PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Security settings for production
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files with WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS settings - update with your frontend URL
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://personal-finance-xi-lake.vercel.app",
]

# Add your frontend domain from environment variable
if 'FRONTEND_URL' in os.environ:
    CORS_ALLOWED_ORIGINS.append(os.environ['FRONTEND_URL'])

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False

# Google Gemini API Key from environment
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', GEMINI_API_KEY)
