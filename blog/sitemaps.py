from django.contrib.sitemaps import Sitemap
from .models import Blog


class BlogSitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Blog.objects.filter(
            is_published=True
        ).order_by("-updated_at")

    def lastmod(self, obj):
        return obj.updated_at