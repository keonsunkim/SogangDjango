from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class FollowForm(forms.Form):
	empty_field = forms.CharField(empty_value='empty')