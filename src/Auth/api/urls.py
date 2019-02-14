from django.conf.urls import url

from .views import (
    check_email_exists_api_view, check_phone_exists_api_view,
    auth_phone_send_verification_code_api_view,
)

urlpatterns = [
    # Check Email and Phone
    url(r'api/v1/auth/email_exists/$', check_email_exists_api_view,
        name='email_exists_check_api'),
    url(r'api/v1/auth/phone_exists/$', check_phone_exists_api_view,
        name='phone_exists_check_api'),
    url(r'api/v1/auth/send_phone_verification_code/$', auth_phone_send_verification_code_api_view,
        name='send_phone_verification_code_api'),
]
