from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    # /music/
    path('', views.IndexView.as_view(), name='index'),

    # /music/<album-id>/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # before Django 2: r'^(?P<album_id>[0-9]+)$'

    # /music/album/add/
    path('album/add/', views.AlbumCreate.as_view(), name='album-add')
]
