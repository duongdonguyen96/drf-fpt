from django.urls import path
from api.v1.songs import views

urlpatterns = [
    path('list/', views.get_all, name='song-list'),
    path('detail/<int:song_id>/', views.detail, name='song-detail'),
    path('create/', views.create, name='song-create'),
    path('update/<int:song_id>/', views.update, name='song-update'),
    path('delete/<int:song_id>/', views.delete, name='song-delete'),

    path('top5-newest/', views.get_top_5_songs_newest, name='top_5_newest'),
    path('album/top5/', views.get_top_5_songs, name='top_5_newest'),



]
