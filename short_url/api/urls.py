from django.urls import include, path, re_path

from api.views import get_full_url, post_full_url

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    re_path(r'^[\w_-]', get_full_url),
    path('', post_full_url),
]
