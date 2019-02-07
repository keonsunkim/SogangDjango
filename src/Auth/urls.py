from django.conf.urls import url

from .views import (
    registration_view, AuthLoginView, AuthLogoutView,
    AuthPasswordChangeView, AuthPasswordChangeDoneView,
    AuthPasswordEmailResetView, AuthPasswordResetConfirmView,
    AuthPasswordEmailSentView, auth_phone_verify_code_view,
    auth_phone_send_verification_code_view, auth_form_successful_view,
)

urlpatterns = [
    url(r'login$', AuthLoginView.as_view(),
        name='login'),
    url(r'logout$', AuthLogoutView.as_view(),
        name='logout'),
    url(r'register$', registration_view,
        name='register'),
    url(r'passwordchange$', AuthPasswordChangeView.as_view(),
        name='password_change'),
    url(r'reset_password_email$', AuthPasswordEmailResetView.as_view(),
        name='password_email_reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        AuthPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^verify_code', auth_phone_verify_code_view,
        name='auth_phone_verify_code_view'),
    url(r'^send_verification_code', auth_phone_send_verification_code_view,
        name='auth_phone_send_verification_code_view'),
    url(r'^(?P<label>[A-Za-z_]+)/success', auth_form_successful_view,
        name='form_successful'),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    # AuthAccountActivateView.as_view(), name='account_activation_confirm'),
]
