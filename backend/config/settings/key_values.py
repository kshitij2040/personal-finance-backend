"""
Environment-based configuration values
"""
from decouple import config

# Secret key for Django
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-this-in-production')

# Debug mode
DEBUG = config('DEBUG', default=True, cast=bool)

# Google Gemini API Key (Optional)
GEMINI_API_KEY = config('GEMINI_API_KEY', default='')

# Database credentials (for Supabase migration)
DB_NAME = config('DB_NAME', default='')
DB_USER = config('DB_USER', default='')
DB_PASSWORD = config('DB_PASSWORD', default='')
DB_HOST = config('DB_HOST', default='')
DB_PORT = config('DB_PORT', default='5432')
