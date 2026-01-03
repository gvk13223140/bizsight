from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

def home_view(request):
    return render(request, "home.html")

def test_base_view(request):
    return render(request, "base.html")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("billing/", include("billing.urls")),
    path("test-base/", test_base_view),
    path("accounts/", include("accounts.urls")),   # your app’s URLs
    # path("auth/", include("allauth.urls")),
    path("", home_view, name="home"),
    path("bizmitra/", include("bizmitra.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

