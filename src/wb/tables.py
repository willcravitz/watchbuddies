import django_tables2 as tables
from .models import Media, WatchedList

class MediaTable(tables.Table):
    title = tables.Column()
    release_date = tables.Column()
    
    class Meta:
        model = Media
        template_name = 'django_tables2/bootstrap.html'
        fields = ['title', 'release_date']
        
class MovieTable(MediaTable):
    title = tables.LinkColumn('movie-detail', args=[tables.A('pk')])
    class Meta:
        template_name = 'django_tables2/bootstrap.html'
    
class TVSeriesTable(MediaTable):
    title = tables.LinkColumn('tv-detail', args=[tables.A('pk')])
    class Meta:
        template_name = 'django_tables2/bootstrap.html'

class TVEpisodeTable(MediaTable):
    title = tables.LinkColumn('episode-detail', 
                              kwargs={'series_pk': tables.A('series__pk'), 
                                      'pk': tables.A('pk')})
    season = tables.Column()
    episode_number = tables.Column()
    class Meta:
        template_name = 'django_tables2/bootstrap.html'

class RatingTable(tables.Table):
    username = tables.Column(accessor='user__username')
    rating = tables.Column()
    
    class Meta:
        model = WatchedList
        template_name = 'django_tables2/bootstrap.html'
        fields = ['username', 'rating']