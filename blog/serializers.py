from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog

        fields = [
            "id",
            "title",
            "slug",
            "content",
            "seo_title",
            "seo_description",
            "seo_keywords",
            "is_published",
            "created_at",
            "updated_at",
        ]