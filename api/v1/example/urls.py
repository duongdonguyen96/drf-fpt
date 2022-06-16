from django.urls import path

from api.v1.example import views

urlpatterns = [
    path('greate_than/', views.greate_than, name='greate_than'),
    path('q_object/', views.q_object, name='q_object'),
    path('sub_query/', views.sub_query, name='sub_query'),
    path('sub_query_limit/', views.sub_query_limit, name='sub_query_limit'),
    path('count/', views.count, name='count'),
    path('aggregate/', views.aggregate, name='aggregate'),
    path('when_then/', views.when_then, name='when_then'),
    path('f/', views.f, name='f'),
    path('exact/', views.exact, name='exact'),
    path('contains/', views.contains, name='contains'),
    path('starts_with/', views.starts_with, name='starts_with'),
    path('range/', views.range, name='range'),
    path('year/', views.year, name='year'),
    path('exits/', views.exits, name='exits'),
    # path('callback/', views.callback, name='callback'),
    # path('publish/', views.publish, name='publish'),
]
