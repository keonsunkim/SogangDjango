from .base import *

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static-root')
STATICFILES_DIRS = [
	os.path.join(BASE_DIR, 'static'),
]
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"



STATICFILES_DIRS = [
	os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media-root')
MEDIA_URL = '/media-root/'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True