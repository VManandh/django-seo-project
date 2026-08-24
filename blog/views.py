from rest_framework import viewsets

from .models import Blog
from .serializers import BlogSerializer
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.http import HttpResponse


class BlogViewSet(viewsets.ModelViewSet):

    serializer_class = BlogSerializer

    def get_queryset(self):
        return Blog.objects.filter(
            is_published=True
        ).order_by("-created_at")
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

      
def robots_txt(request):

    content = """User-agent: *
Allow: /

Sitemap: http://127.0.0.1:8000/sitemap.xml
"""

    return HttpResponse(
        content,
        content_type="text/plain"
    )    