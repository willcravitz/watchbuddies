import pytest
from datetime import date
from django.urls import reverse

from wb.models import User, Media
from .factories import MovieFactory, TVSeriesFactory, TVEpisodeFactory

@pytest.mark.django_db
def test_movie_detail_view(client):
    movie = MovieFactory.create()
    response = client.get(reverse('movie-detail', args=[movie.pk]))

    assert response.context['object'] == movie
    assert response.status_code == 200

    html = response.content.decode()
    assert movie.title in html
    assert movie.release_date.strftime("%B %-d, %Y") in html
    
@pytest.mark.django_db
def test_tvseries_create_view(client):
    # authenticate user so that they can access create page
    user = User.objects.create_user(username='user', password='test')
    user.is_staff = True
    user.save()
    client.login(username='user', password='test')
    
    data = {
        'title': 'My New TV Series',
        'release_date': date.today(),
    }
    response = client.post(reverse('tv-create'), data)
    
    assert response.status_code == 302
    print(response)
    tv_series = Media.objects.latest('pk')
    assert tv_series.title == data['title']
    assert tv_series.release_date == data['release_date']
    
@pytest.mark.django_db
def test_tvseries_detail_view_episodes(client):
    tv_series = TVSeriesFactory.create(num_episodes=10)
    response = client.get(reverse('tv-detail', args=[tv_series.pk]))
    
    assert response.context['object'] == tv_series
    assert response.status_code == 200

    html = response.content.decode()
    for episode in tv_series.episodes.all():
        assert episode.title in html