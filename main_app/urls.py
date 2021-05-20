from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),

    path('collections/', views.CollectionList.as_view(), name='collections_index'),
    path('collections/mine/', views.CollectionListCurrentUser.as_view(), name='collections_index_current_user'),
    path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collections_detail'),
    path('collections/create', views.CollectionCreate.as_view(), name='collections_create'),
    path('collections/<int:pk>/update', views.CollectionUpdate.as_view(), name='collections_update'),
    path('collections/<int:pk>/delete', views.CollectionDelete.as_view(), name='collections_delete'),
    path('items/create/', views.ItemCreate.as_view(), name='items_create'),
    path('items/<int:pk>/', views.ItemDetail.as_view(), name='items_detail'),
    path('items/<int:pk>/update/', views.ItemUpdate.as_view(), name='items_update'),
    path('items/<int:pk>/delete/', views.ItemDelete.as_view(), name='items_delete'),
    path('items/<int:item_id>/comments/create/',
         views.CommentCreate.as_view(),
         name='comments_create'),
    path('items/<int:item_id>/pictures/create/', views.PictureCreate.as_view(), name='pictures_create'),
    path('pictures/<int:pk>/delete/', views.PictureDelete.as_view(), name='pictures_delete'),
    path('registration/signup', views.SignUp.as_view(), name='signup')
]
