from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ping/', views.ping),
    url(r'^secured/ping/', views.secured),
    url(r'^private/secured/ping/', views.private),
]
