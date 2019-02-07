from django.http import JsonResponse

from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
# django basic tools

from django.contrib.auth import views as auth_views
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
# for auth

from datetime import timedelta
# for cryptosigning

from django.contrib.auth.forms import (
    AuthenticationForm, UsernameField, UserCreationForm,
)

from .models import PasswordResetData
from .forms import (
    UserRegistrationForm, AuthResetPhoneVerificationForm,
    AuthResetPhoneOnlyForm
)

from django.contrib.auth import (
    get_user_model, logout as auth_logout,
)
User = get_user_model()


@method_decorator(never_cache)
def auth_form_successful_view(request, label):
    if label == 'register_user':
        auth_logout(request)
        success_msg = (
            'You have sucessfully registered your account! ',
            'Activate your account with the link we provided to your email!'
        )
    elif label == 'email_password_reset':
        auth_logout(request)
        success_msg = (
            'We have sent your password reset link to your email!',
            'Reset with the link provided from our email!'
        )
    elif label == 'register_phonenumber' or label == 'change_phonenumber':
        auth_logout(request)
        success_msg = (
            'You have sucessfully registered your phone number! ',
            'Please log in again'
        )
    elif label == 'change_email':
        auth_logout(request)
        success_msg = (
            'You have sucessfully registered your email! ',
            'Activate your account with the link we provided to your email!'
        )
    elif label == 'password_change_complete':
        auth_logout(request)
        success_msg = (
            'You have successfully changed your password!',
            'Please log in again')
    else:
        return HttpResponse(status=404)

    context = dict(success_msg=success_msg)
    return render(request, 'auth/form_success.html', context)


@sensitive_post_parameters()
def registration_view(request):
    if request.user.is_authenticated():
        return HttpResponse("must logout before registering!",
                            status=403)
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(email=form.cleaned_data['email'],
                                     password=form.cleaned_data['password2'])
            return redirect('auth:form_successful', kwargs={'label': 'register_user'})
        return render(request, 'auth/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
        return render(request, 'auth/register.html', {'form': form})


class AuthLoginView(auth_views.LoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True


class AuthLogoutView(auth_views.LogoutView):
    template_name = "auth/logout.html"


class AuthPasswordChangeView(auth_views.PasswordChangeView):
    template_name = "auth/changepassword.html"
    success_url = reverse_lazy('auth:form_successful', kwargs={
                               'label': 'password_change_complete'})


class AuthPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'auth/password_change_done.html'


class AuthPasswordEmailResetView(auth_views.PasswordResetView):
    template_name = 'auth/password_reset_email.html'
    email_template_name = 'auth/email/email_content_password_reset.html'
    subject_template_name = 'auth/email/password_reset_subject.txt'
    success_url = reverse_lazy('auth:form_successful', kwargs={
                               'label': 'email_password_reset'})


class AuthPasswordEmailSentView(auth_views.PasswordResetDoneView):
    template_name = 'auth/password_reset_email_sent.html'


class AuthPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'auth/password_reset_confirm.html'
    success_url = reverse_lazy('auth:form_successful', kwargs={
                               'label': 'password_change_complete'})


@method_decorator(never_cache)
@method_decorator(sensitive_post_parameters())
def auth_phone_verify_code_view(request):
    if request.user.is_authenticated():
        return HttpResponse("must logout before registering!",
                            status=403)
    if request.method == "POST":
        auth_phone_verification_form = AuthResetPhoneVerificationForm(
            request.POST)
        if auth_phone_verification_form.is_valid():
            user_phone = auth_phone_verification_form.cleaned_data[
                'user_phone']
            verification_code = auth_phone_verification_form.cleaned_data[
                'verification_code']
            latest_of_user = PasswordResetData.objects.filter(
                user_phone=user_phone).latest('created')
            if latest_of_user:
                print(latest_of_user.user_phone,
                      latest_of_user.verification_code, latest_of_user.created)
                print('*' * 10)
                print(verification_code)
                if not latest_of_user.is_not_expired:
                    auth_phone_verification_form.add_error(
                        None, "Your key has expired")
                    return render(request,
                                  'auth/password_reset_phone_verification.html',
                                  {'auth_phone_verification_form': auth_phone_verification_form}
                                  )
                if not latest_of_user.verification_code_matches(verification_code):
                    auth_phone_verification_form.add_error(None, "Wrong Key!")
                    return render(request,
                                  'auth/password_reset_phone_verification.html',
                                  {'auth_phone_verification_form': auth_phone_verification_form}
                                  )
                user_object = get_object_or_404(
                    User, user_phone=user_phone, is_active=True)
                # user.has_usable() add for later!
                if "Reset" in request.POST:
                    uid = urlsafe_base64_encode(force_bytes(user_object.pk))
                    token = default_token_generator.make_token(user_object)
                    return redirect(reverse_lazy('auth:password_reset_confirm',
                                                 kwargs={'uidb64': uid, 'token': token}))
                elif "Register" in request.POST:
                    if User.objects.filter(user_phone=user_phone).exists():
                        auth_phone_verification_form.add_error(
                            user_phone, "The phone number is already being used")
                        return render(request,
                                      'auth/password_reset_phone_verification.html',
                                      {'auth_phone_verification_form': auth_phone_verification_form}
                                      )
                    else:
                        user_object.user_phone = user_phone
                        user_object.save()
                        return redirect(reverse_lazy())

        else:
            return render(request,
                          'auth/password_reset_phone_verification.html',
                          {'auth_phone_verification_form': auth_phone_verification_form}
                          )
    else:
        auth_phone_verification_form = AuthResetPhoneVerificationForm()
        context = dict(
            auth_phone_verification_form=auth_phone_verification_form)
        return render(request, 'auth/password_reset_phone_verification.html', context)


@method_decorator(never_cache)
@method_decorator(sensitive_post_parameters())
def auth_phone_send_verification_code_view(request):
    if request.user.is_authenticated():
        return HttpResponse(status=403)
    if request.method == "POST":
        auth_phone_only_form = AuthResetPhoneOnlyForm(request.POST)
        if auth_phone_only_form.is_valid():
            user_phone = auth_phone_only_form.cleaned_data['user_phone']
            verification_code = PasswordResetData()._generate_phone_verification_number()
            reset_data = PasswordResetData(
                user_phone=user_phone,
                verification_code=verification_code)
            reset_data.full_clean()
            reset_data.save()
            print(verification_code)
            return redirect(reverse_lazy('auth:auth_phone_send_verification_code_view'))
        else:
            # return JsonResponse({'error':
            # auth_phone_only_form.errors.as_json()}, status=404)
            return render(request, 'auth/password_reset_phone_send.html',
                          {'auth_phone_only_form': auth_phone_only_form})
    else:
        auth_phone_only_form = AuthResetPhoneOnlyForm()
        return render(request,
                      'auth/password_reset_phone_send.html',
                      {'auth_phone_only_form': auth_phone_only_form}
                      )
