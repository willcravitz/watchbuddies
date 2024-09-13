from django.urls import path

from . import views

urlpatterns = [
    path('movies/', views.MovieList.as_view(), name='api-movie-list'),
    path('tv/', views.TVSeriesList.as_view(), name='api-tv-list'),
    path('movies/<int:pk>/', views.MovieDetail.as_view(), name='api-movie-detail'),
    path('tv/<int:pk>/', views.TVSeriesDetail.as_view(), name='api-tv-detail'),
    path('tv/<int:pk>/create', views.TVEpisodeList.as_view(), name='api-episode-list'),
    path('tv/<int:series_pk>/<int:pk>/', views.TVEpisodeDetail.as_view(), name='api-episode-detail'),
    path('movies/<int:pk>/ratings', views.movie_ratings, name='api-movie-rating-list')
]