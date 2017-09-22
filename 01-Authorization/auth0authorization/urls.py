from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^api/public/', views.public),
    url(r'^api/private/', views.private),
    url(r'^api/private-scoped/', views.private_scoped),
]
