from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('movies/', views.MovieListView.as_view(), name='movie-list'),
    path('tv/', views.TVSeriesListView.as_view(), name='tv-list'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('tv/<int:pk>/', views.TVSeriesDetailView.as_view(), name='tv-detail'),
    path('tv/<int:series_pk>/<int:pk>/', views.TVEpisodeDetailView.as_view(), name='episode-detail'),
    path('movies/create/', views.MovieCreateView.as_view(), name='movie-create'),
    path('tv/create/', views.TVSeriesCreateView.as_view(), name='tv-create'),
    path('tv/<int:series_pk>/create/', views.TVEpisodeCreateView.as_view(), name='episode-create'),
    path('movies/<int:pk>/edit/', views.MovieUpdateView.as_view(), name='movie-edit'),
    path('tv/<int:pk>/edit/', views.TVSeriesUpdateView.as_view(), name='tv-edit'),
    path('tv/<int:series_pk>/<int:pk>/edit/', views.TVEpisodeUpdateView.as_view(), name='episode-edit'),
    path('movies/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie-delete'),
    path('tv/<int:pk>/delete/', views.TVSeriesDeleteView.as_view(), name='tv-delete'),
    path('tv/<int:series_pk>/<int:pk>/delete/', views.TVEpisodeDeleteView.as_view(), name='episode-delete'),
]