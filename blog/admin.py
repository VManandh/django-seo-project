from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "slug",
        "is_published",
        "created_at",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    search_fields = (
        "title",
        "content",
        "seo_keywords",
    )