import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Add this to serve HTML files from frontend folder
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, '..'),  # Root directory for index.html
            os.path.join(BASE_DIR, '../frontend'),  # Frontend folder for other HTML files
        ],
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

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '../frontend'),  # Serve frontend static files
    os.path.join(BASE_DIR, '../frontend/css'),  # CSS files
    os.path.join(BASE_DIR, '../frontend/js'),   # JS files
]

# Make sure this is set
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')