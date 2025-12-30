from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


def test_base_view(request):
    return render(request, "base.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("billing/", include("billing.urls")),
    path("test-base/", test_base_view),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)