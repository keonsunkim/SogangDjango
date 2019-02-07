from django.contrib import admin
from .models import GeneralPost, Tag, FilterTagRelation

admin.site.register(GeneralPost)
admin.site.register(FilterTagRelation)
admin.site.register(Tag)
# Register your models here.
