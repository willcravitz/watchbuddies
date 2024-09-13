import pytest
from datetime import datetime
from django.urls import reverse
from rest_framework.test import APIClient

from wb.models import Media
from .factories import MovieFactory, TVSeriesFactory, TVEpisodeFactory

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_movie_get(api_client):
    movie = MovieFactory.create()

    response = api_client.get(reverse('api-movie-detail', args=[movie.pk]))

    assert response.status_code == 200
    assert response.data['title'] == movie.title
    date_str = response.data['release_date']
    assert datetime.strptime(date_str, '%Y-%m-%d').date() == movie.release_date
    
@pytest.mark.django_db
def test_tvseries_post(api_client):
    data = {
        "title": "My New TV Series",
        "release_date": "2023-11-01"
    }
    response = api_client.post(reverse('api-tv-list'), data)
    assert response.status_code == 201

    tv_series = Media.objects.get(pk=response.data['id'])
    assert tv_series.title == data['title']
    date_str = data['release_date']
    assert tv_series.release_date == datetime.strptime(date_str, '%Y-%m-%d').date()
    
@pytest.mark.django_db
def test_tvseries_patch(api_client):
    tv_series = TVSeriesFactory.create(title='Old Title')
    data = {
        'title': 'New Title'
    }
    response = api_client.patch(reverse('api-tv-detail', args=[tv_series.pk]), data)
    assert response.status_code == 200

    tv_series.refresh_from_db()
    assert tv_series.title == data['title']