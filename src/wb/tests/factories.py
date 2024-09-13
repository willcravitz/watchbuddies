import factory
from factory import Sequence, Faker, SubFactory
from factory.django import DjangoModelFactory
from wb.models import Media, Person, MediaCastCrew

class MediaFactory(DjangoModelFactory):
    class Meta:
        model = Media

    title = Faker('sentence', nb_words=4)
    cover_image = Faker('image_url')
    release_date = Faker('date_this_decade')

class MovieFactory(MediaFactory):
    media_type = Media.MOVIE
    series = None
    season = None
    episode_number = None

class TVSeriesFactory(MediaFactory):
    class Meta:
        skip_postgeneration_save = True
    
    media_type = Media.TV_SERIES
    series = None
    season = None
    episode_number = None
    
    @factory.post_generation
    def num_episodes(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        for episode_number in range(1, extracted + 1):
            self.episodes.add(TVEpisodeFactory(
                series=self,
                season=1,
                episode_number=episode_number,
            ))

class TVEpisodeFactory(MediaFactory):
    media_type = Media.TV_EPISODE
    series = SubFactory(TVSeriesFactory)
    season = Faker('random_int', min=1, max=10, step=1)
    episode_number = Faker('random_int', min=1, max=30, step=1)
    
class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person

    first_name = Faker('first_name')
    last_name = Faker('last_name')

class MediaCastCrewFactory(DjangoModelFactory):
    class Meta:
        model = MediaCastCrew

    media = SubFactory(MediaFactory)
    person = SubFactory(PersonFactory)
    role_type = Faker('random_element', 
                      elements=[MediaCastCrew.CREW, MediaCastCrew.CAST])
    role = Faker('word')
        
    