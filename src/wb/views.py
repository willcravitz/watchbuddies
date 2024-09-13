from django.shortcuts import render
from django.db import IntegrityError 
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django_tables2 import SingleTableView, SingleTableMixin
from .models import Media
from .tables import MediaTable, MovieTable, TVSeriesTable, TVEpisodeTable, RatingTable

def index(request):
    context = {"welcome": "Hello, world!"}
    return render(request, "wb/index.html", context)

def profile(request):
    return render(request, "wb/profile.html")

class MediaListView(SingleTableView):
    model = Media
    table_class = MediaTable
    template_name = 'wb/media_list.html'
    
class MovieListView(MediaListView):
    queryset = Media.objects.filter(media_type=Media.MOVIE)
    table_class = MovieTable
    extra_context = {
        'media_type': 'Movies',
        'detail_url': 'movie-detail',
        'create_url': 'movie-create'}

class TVSeriesListView(MediaListView):
    queryset = Media.objects.filter(media_type=Media.TV_SERIES)
    table_class = TVSeriesTable
    extra_context = {
        'media_type': 'TV Series', 
        'detail_url': 'tv-detail',
        'create_url': 'tv-create'}

class MediaDetailView(SingleTableMixin, DetailView):
    model = Media
    table_class = RatingTable
    template_name = 'wb/media_detail.html'
    
    def get_table_data(self):
        return self.object.watches.filter(rating__isnull=False)

class MovieDetailView(MediaDetailView):
    queryset = Media.objects.filter(media_type=Media.MOVIE)
    template_name = 'wb/movie_detail.html'

class TVSeriesDetailView(MediaDetailView):
    queryset = Media.objects.filter(media_type=Media.TV_SERIES)
    table_class = TVEpisodeTable
    template_name = 'wb/tv_detail.html'
    
    def get_table_data(self):
        return self.object.episodes.all()
        
class TVEpisodeDetailView(MediaDetailView):
    queryset = Media.objects.filter(media_type=Media.TV_EPISODE)
    template_name = 'wb/episode_detail.html'

class IsStaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff
  
class MediaCreateView(IsStaffRequiredMixin, CreateView):
    model = Media
    template_name = 'wb/media_form.html'
    fields = ['title', 'release_date']
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

class MovieCreateView(MediaCreateView):
    def form_valid(self, form):
        form.instance.media_type = Media.MOVIE
        form.instance.cover_image = 'cover.png'
        return super().form_valid(form)
    success_url = reverse_lazy('movie-list')

class TVSeriesCreateView(MediaCreateView):
    def form_valid(self, form):
        form.instance.media_type = Media.TV_SERIES
        form.instance.cover_image = 'cover.png'
        return super().form_valid(form)
    success_url = reverse_lazy('tv-list')

class TVEpisodeCreateView(MediaCreateView):
    fields = ['season', 'episode_number', 'title', 'release_date']
    
    def form_valid(self, form):
        form.instance.media_type = Media.TV_EPISODE
        series_pk = self.kwargs['series_pk']
        form.instance.series = Media.objects.get(pk=series_pk)
        form.instance.cover_image = 'cover.png'
        return super().form_valid(form)

    def get_success_url(self):
        series_pk = self.kwargs['series_pk']
        success_url = reverse_lazy('tv-detail', kwargs={'pk': series_pk})
        return success_url

class MediaUpdateView(IsStaffRequiredMixin, UpdateView):
    model = Media
    template_name = 'wb/media_form.html'
    fields = ['title', 'release_date']
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            form.add_error(None, e)
            return self.form_invalid(form)
    
class MovieUpdateView(MediaUpdateView):
    def form_valid(self, form):
        form.instance.media_type = Media.MOVIE
        form.instance.cover_image = 'cover.png'
        return super().form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        success_url = reverse_lazy('movie-detail', kwargs={'pk': pk})
        return success_url

class TVSeriesUpdateView(MediaUpdateView):
    def form_valid(self, form):
        form.instance.media_type = Media.TV_SERIES
        form.instance.cover_image = 'cover.png'
        return super().form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        success_url = reverse_lazy('tv-detail', kwargs={'pk': pk})
        return success_url

class TVEpisodeUpdateView(MediaUpdateView):
    fields = ['season', 'episode_number', 'title', 'release_date']
    
    def form_valid(self, form):
        form.instance.media_type = Media.TV_EPISODE
        series_pk = self.kwargs['series_pk']
        form.instance.series = Media.objects.get(pk=series_pk)
        form.instance.cover_image = 'cover.png'
        return super().form_valid(form)

    def get_success_url(self):
        series_pk = self.kwargs['series_pk']
        pk = self.kwargs['pk']
        success_url = reverse_lazy('episode-detail', kwargs={
            'series_pk': series_pk, 'pk': pk})
        return success_url

class MediaDeleteView(IsStaffRequiredMixin, DeleteView):
    model = Media
    template_name = 'wb/media_confirm_delete.html'

class MovieDeleteView(MediaDeleteView):
    queryset = Media.objects.filter(media_type=Media.MOVIE)
    success_url = reverse_lazy('movie-list')
    extra_context = {'return_url': 'movie-detail'}

class TVSeriesDeleteView(MediaDeleteView):
    queryset = Media.objects.filter(media_type=Media.TV_SERIES)
    success_url = reverse_lazy('tv-list')
    extra_context = {'return_url': 'tv-detail'}

class TVEpisodeDeleteView(MediaDeleteView):
    queryset = Media.objects.filter(media_type=Media.TV_EPISODE)
    template_name = 'wb/episode_confirm_delete.html'
    
    def get_success_url(self):
        series_pk = self.kwargs['series_pk']
        success_url = reverse_lazy('tv-detail', kwargs={'pk': series_pk})
        return success_url