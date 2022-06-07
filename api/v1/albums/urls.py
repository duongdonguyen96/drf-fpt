from django.urls import path
from api.v1.albums import views

urlpatterns = [
    path('list/', views.get_all, name='album-list'),
    path('detail/<int:album_id>/', views.detail, name='album-detail'),
    path('create/', views.create, name='album-create'),
    path('update/<int:album_id>/', views.update, name='album-update'),
    path('delete/<int:album_id>/', views.delete, name='album-delete'),

    path('top10/', views.get_top_10_albums, name='top-10-albums'),
    path('get_albums_of_singer/', views.get_albums_of_singer, name='get_albums_of_singer'),

]
