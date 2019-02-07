from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from .models import GeneralPost,Tag,FilterTagRelation

# admin.site.register(GeneralPost)
admin.site.register(Tag)
admin.site.register(FilterTagRelation)

class GeneralPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = GeneralPost
        fields = '__all__'

class GeneralPostAdmin(admin.ModelAdmin):
    form = GeneralPostAdminForm

admin.site.register(GeneralPost, GeneralPostAdmin)
# Register your models here.
