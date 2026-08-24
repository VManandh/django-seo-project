import json

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse

from rest_framework import viewsets

from .models import Blog
from .serializers import BlogSerializer

# ----
from django.urls import reverse
# =========================================================
# API
# =========================================================

class BlogViewSet(viewsets.ModelViewSet):

    serializer_class = BlogSerializer

    def get_queryset(self):

        return Blog.objects.filter(
            is_published=True
        ).order_by("-created_at")


# =========================================================
# BLOG LIST PAGE
# =========================================================

class BlogListView(ListView):

    model = Blog

    template_name = "blog/list.html"

    context_object_name = "blogs"

    # Show 5 blogs per page
    paginate_by = 5

    def get_queryset(self):

        return Blog.objects.filter(
            is_published=True
        ).order_by("-created_at")


# =========================================================
# BLOG DETAIL PAGE
# =========================================================

class BlogDetailView(DetailView):

    model = Blog

    template_name = "blog/detail.html"

    context_object_name = "blog"

    def get_object(self):

        return get_object_or_404(
            Blog,
            slug=self.kwargs["slug"],
            is_published=True
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        blog = self.object

        # -------------------------------------------------
        # Current Blog URL
        # -------------------------------------------------

        blog_url = self.request.build_absolute_uri()

        # -------------------------------------------------
        # Article JSON-LD Structured Data
        # -------------------------------------------------

        structured_data = {

            "@context": "https://schema.org",

            "@type": "Article",

            # Blog title
            "headline": blog.title,

            # SEO description
            "description": (
                blog.seo_description
                or blog.title
            ),

            # Current page URL
            "url": blog_url,

            # Main page
            "mainEntityOfPage": {

                "@type": "WebPage",

                "@id": blog_url
            },

            # Published date
            "datePublished": (
                blog.created_at.isoformat()
            ),

            # Updated date
            "dateModified": (
                blog.updated_at.isoformat()
            ),

            # Author
            "author": {

                "@type": "Person",

                "name": "My Django Blog"
            },

            # Publisher
            "publisher": {

                "@type": "Organization",

                "name": "My Django Blogss"
            }
        }

        # -------------------------------------------------
        # Featured Image
        # -------------------------------------------------

        if blog.featured_image:

            image_url = (
                self.request.scheme
                + "://"
                + self.request.get_host()
                + blog.featured_image.url
            )

            structured_data["image"] = image_url

        # -------------------------------------------------
        # Convert Python dictionary to JSON
        # -------------------------------------------------

        context["structured_data"] = (

            json.dumps(structured_data)

            # Prevent unsafe HTML characters
            .replace("<", "\\u003c")
            .replace(">", "\\u003e")
            .replace("&", "\\u0026")
        )

        return context


# =========================================================
# ROBOTS.TXT
# =========================================================
def robots_txt(request):

    sitemap_url = request.build_absolute_uri(
        reverse("django-sitemap")
    )

    content = f"""User-agent: *
Allow: /

Sitemap: {sitemap_url}
"""

    return HttpResponse(
        content,
        content_type="text/plain"
    )