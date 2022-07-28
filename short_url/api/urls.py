from django.urls import path, re_path

from api.views import get_full_url, post_full_url

urlpatterns = [
    re_path(r'^[\w_-]', get_full_url),
    path('', post_full_url),
]
