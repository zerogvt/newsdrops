from django.contrib import admin
from .models import Post, Vote


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'crdate',)


class VoteAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'crdate',)


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Vote, VoteAdmin)
