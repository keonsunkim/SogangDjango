from django.shortcuts import render
from django.views.generic import TemplateView

from Auth.forms import (
    UserRegistrationForm, AuthPhoneVerificationForm,
    AuthPhoneOnlyVerificationForm, UserAuthenticationForm
)


def homepage_view(request):
    registration_form = UserRegistrationForm()
    login_form = UserAuthenticationForm()
    context = dict(
        registration_form=registration_form,
        login_form=login_form
    )
    return render(request, 'home/home.html', context)

class about_view(TemplateView):
    template_name = "home/about.html"