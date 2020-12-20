from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'crdate',)


# Register your models here.
admin.site.register(Post, PostAdmin)
