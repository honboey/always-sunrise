from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("livestream-list", views.livestream_list, name="livestream_list"),
    path("livestream/<int:pk>/", views.single_livestream, name="single_livestream"),
]
