from django.contrib import admin
from Post.models import GeneralPost
from Post.models import Tag
from Post.models import FilterTagRelation
admin.site.register(GeneralPost)
admin.site.register(Tag)
admin.site.register(FilterTagRelation)
# Register your models here.
