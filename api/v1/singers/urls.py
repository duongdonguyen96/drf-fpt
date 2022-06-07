from django.urls import path
from api.v1.singers import views

urlpatterns = [
    path('list/', views.get_all, name='singer-list'),
    path('detail/<int:singer_id>/', views.detail, name='singer-detail'),
    path('create/', views.create, name='singer-create'),
    path('update/<int:singer_id>/', views.update, name='singer-update'),
    path('delete/<int:singer_id>/', views.delete, name='singer-delete'),

    path('detail/<int:singer_id>/songs/', views.get_list_songs, name='singer-list_songs'),
    path('detail/<int:singer_id>/albums/', views.get_list_albums, name='singer-list_albums'),
    path('search/', views.search_data, name='search-data'),

]
