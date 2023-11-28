from django.urls import path
from . import views

urlpatterns = [
  	path('livestream-list', views.livestream_list, name='livestream_list'),
]

