from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from wb.models import *

class MediaList(generics.ListCreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    
class MovieList(MediaList):
    queryset = Media.objects.filter(media_type=Media.MOVIE)
    serializer_class = MovieSerializer
    
class TVSeriesList(MediaList):
    queryset = Media.objects.filter(media_type=Media.TV_SERIES)
    serializer_class = TVSeriesSerializer
    
class TVEpisodeList(MediaList):
    serializer_class = TVEpisodeSerializer
    def get_queryset(self):
        series_pk = self.kwargs['pk']
        queryset = Media.objects.filter(series=series_pk, 
                                        media_type=Media.TV_EPISODE)
        return queryset

class MediaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    
class MovieDetail(MediaDetail):
    queryset = Media.objects.filter(media_type=Media.MOVIE)
    serializer_class = MovieSerializer
    
class TVSeriesDetail(MediaDetail):
    queryset = Media.objects.filter(media_type=Media.TV_SERIES)
    serializer_class = TVSeriesSerializer
    
class TVEpisodeDetail(MediaDetail):
    serializer_class = TVEpisodeSerializer
    def get_queryset(self):
        series_pk = self.kwargs['series_pk']
        queryset = Media.objects.filter(series=series_pk, 
                                        media_type=Media.TV_EPISODE)
        return queryset
    
@api_view(['GET', 'POST'])
def movie_ratings(request, pk):
    try:
        movie = Media.objects.get(media_type=Media.MOVIE, pk=pk)
    except Media.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GetRatingSerializer(movie)
        return Response(serializer.data)

    elif request.method == 'POST':
        try:
            user = User.objects.get(username=request.data.get('user'))
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        watch_data = {
            'user': user.id,
            'media': movie.id,
            'rating': request.data.get('rating')
        }
        if movie in user.watched.all():
            update = True       
            watched_listing = WatchedList.objects.get(user=user, media=movie)
            serializer = PostRatingSerializer(watched_listing, data=watch_data)
        else:
            update = False
            serializer = PostRatingSerializer(data=watch_data)
        if serializer.is_valid():
            serializer.save()
            if update:
                return Response(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)