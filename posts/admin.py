from django.contrib import admin

from .models import Group, Post


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Страница административной панели сообщества"""
    list_display = ("pk", "title", "slug", "description")
    search_fields = ("title", 'slug')
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = "-пусто-"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Страница административной панели постов"""
    list_display = ("pk", "text", "pub_date", "author")
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"
