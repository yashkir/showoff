from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('collections/', views.collections_index, name='collections_index'),
    path('collections/user/<int:user_id>/', views.collections_index_by_user, name='collections_index_by_user'),
    path('collections/<int:collection_id>/', views.collections_detail, name='collections_detail'),
    path('collections/create', views.CollectionCreate.as_view(), name='collections_create'),
    path('collections/<int:pk>/update', views.CollectionUpdate.as_view(), name='collections_update'),
    path('collections/<int:pk>/delete', views.CollectionDelete.as_view(), name='collections_delete'),
    path('items/create/', views.ItemCreate.as_view(), name='items_create'),
    path('items/<int:pk>/', views.ItemDetail.as_view(), name='items_detail'),
    path('items/<int:pk>/update/', views.ItemUpdate.as_view(), name='items_update'),
    path('items/<int:pk>/delete/', views.ItemDelete.as_view(), name='items_delete'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
