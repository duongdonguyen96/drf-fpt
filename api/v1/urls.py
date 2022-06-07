from django.conf.urls import include
from django.urls import path
import debug_toolbar

urlpatterns = [
    path('singers/', include('api.v1.singers.urls')),
    path('albums/', include('api.v1.albums.urls')),
    path('songs/', include('api.v1.songs.urls')),
    path('example/', include('api.v1.example.urls')),
    path('__debug__/', include(debug_toolbar.urls)),

]
