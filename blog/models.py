from django.db import models
from django.urls import reverse

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    content = models.TextField()

    seo_title = models.CharField(
        max_length=60,
        blank=True
    )

    seo_description = models.CharField(
        max_length=160,
        blank=True
    )

    seo_keywords = models.CharField(
        max_length=255,
        blank=True
    )

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse(
            "blog-detail",
            kwargs={
                "slug": self.slug
            }
        )

    def __str__(self):
        return self.title