from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("info/<str:dnd_form_name>", views.info, name="info"),
    path("refresh", views.refresh, name="refresh"),
]