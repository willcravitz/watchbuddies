from rest_framework import serializers
from wb.models import *

class MediaSerializer(serializers.ModelSerializer):
    avg_rating = serializers.ReadOnlyField()
    
    class Meta:
        model = Media
        fields = ['id', 'title', 'release_date', 'avg_rating']

class MovieSerializer(MediaSerializer):
    def create(self, validated_data):
        validated_data['media_type'] = Media.MOVIE
        return Media.objects.create(**validated_data)

class TVSeriesSerializer(MediaSerializer):
    episodes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    episode_names = serializers.SerializerMethodField(read_only=True)
    
    def get_episode_names(self, obj):
        return [episode.title for episode in obj.episodes.all()]
    
    def create(self, validated_data):
        validated_data['media_type'] = Media.TV_SERIES
        return Media.objects.create(**validated_data)
    
    class Meta(MediaSerializer.Meta):
        other_fields = ['episodes', 'episode_names']
        fields = MediaSerializer.Meta.fields + other_fields

class TVEpisodeSerializer(MediaSerializer):
    series_title = serializers.StringRelatedField(source='series', read_only=True)
    series = serializers.PrimaryKeyRelatedField(
        queryset=Media.objects.filter(media_type=Media.TV_SERIES))
    
    class Meta(MediaSerializer.Meta):
        other_fields = ['series', 'series_title', 'season', 'episode_number']
        fields = MediaSerializer.Meta.fields + other_fields
        
class GetRatingSerializer(serializers.ModelSerializer):
    ratings = serializers.ReadOnlyField()
    
    class Meta:
        model = Media
        fields = ['ratings']
        
class PostRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchedList
        fields = ['user', 'media', 'rating']