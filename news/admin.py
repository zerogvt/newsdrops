from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('crdate',)


# Register your models here.
admin.site.register(Post, PostAdmin)
