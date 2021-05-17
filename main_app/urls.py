from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('collections/', views.collections_index, name='collections_index'),
]
