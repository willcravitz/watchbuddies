from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Inherits username, first_name, last_name, email from AbstractUser
    watched = models.ManyToManyField('Media', through='WatchedList', 
                                     related_name='watched_by')
    buddies = models.ManyToManyField('self', through='BuddiesList')
    buddy_groups = models.ManyToManyField('BuddyGroup', 
                        through='BuddyGroupMembership', related_name='members')
    watch_parties = models.ManyToManyField('WatchParty', 
                        through='WatchPartyAttendance', related_name='attendees')
    
class BuddiesList(models.Model):
    DECLINED = 1
    PENDING = 2
    ACCEPTED = 3
    
    STATUSES = (
        (DECLINED, 'Declined'),
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name='user_buddies')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, 
                               related_name='friend_buddies')
    status = models.SmallIntegerField(choices=STATUSES)
    
    class Meta:
        unique_together = ['user', 'friend']

class Media(models.Model):
    MOVIE = 1
    TV_SERIES = 2
    TV_EPISODE = 3
    
    MEDIA_TYPES = (
        (MOVIE, 'Movie'),
        (TV_SERIES, 'TV Series'),
        (TV_EPISODE, 'TV Episode')
    )
    
    media_type = models.SmallIntegerField(choices=MEDIA_TYPES)
    series = models.ForeignKey('self', on_delete=models.CASCADE, 
                               related_name='episodes', null=True)
    title = models.TextField()
    cover_image = models.URLField()
    season = models.SmallIntegerField(null=True)
    episode_number = models.SmallIntegerField(null=True)
    release_date = models.DateField()
    
    cast_crew = models.ManyToManyField('Person', through='MediaCastCrew', 
                                       related_name='credits')
    
    class Meta:
        unique_together = ['series', 'season', 'episode_number']
        
    def __str__(self):
        return self.title
    
    @property
    def ratings(self):
        rated_watches = self.watches.filter(rating__isnull=False)
        return [watch.rating for watch in rated_watches]
    
    @property
    def avg_rating(self):
        if self.ratings:
            return sum(self.ratings)/len(self.ratings)
        return 'Not yet rated'
    
class WatchedList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='watches')
    rating = models.SmallIntegerField(null=True)
    
    class Meta:
        unique_together = ['user', 'media']
        
class Person(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    
class MediaCastCrew(models.Model):
    CAST = 1
    CREW = 2
    
    ROLE_TYPES = (
        (CAST, 'Cast'),
        (CREW, 'Crew')
    )
    
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role_type = models.SmallIntegerField(choices=ROLE_TYPES)
    role = models.TextField()

class Comment(models.Model):
    YOURSELF = 1
    BUDDIES = 2
    BUDDY_GROUP = 3

    VISIBILITIES = (
        (YOURSELF, 'Only Yourself'),
        (BUDDIES, 'Your Buddies'),
        (BUDDY_GROUP, 'A Buddy Group')
    )
    
    media = models.ForeignKey(Media, on_delete=models.CASCADE, 
                              related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name='comments')
    buddy_group = models.ForeignKey('BuddyGroup', on_delete=models.CASCADE, 
                                    related_name='comments', null=True)
    text = models.TextField()
    time = models.DateTimeField()
    visibility = models.SmallIntegerField(choices=VISIBILITIES)
    
    viewers = models.ManyToManyField(User, related_name="visible_comments")

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    watch_party = models.ForeignKey('WatchParty', on_delete=models.CASCADE, 
                                    related_name='chats')
    text = models.TextField()
    time = models.DateTimeField()

class BuddyGroup(models.Model):
    name = models.TextField()

class BuddyGroupMembership(models.Model):
    DECLINED = 1
    PENDING = 2
    ACCEPTED = 3
    
    STATUSES = (
        (DECLINED, 'Declined'),
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buddy_group = models.ForeignKey(BuddyGroup, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=STATUSES)
    
    class Meta:
        unique_together = ['user', 'buddy_group']

class WatchParty(models.Model):
    buddy_group = models.ForeignKey(BuddyGroup, on_delete=models.CASCADE, 
                                    related_name='watch_parties')
    media = models.ForeignKey(Media, on_delete=models.CASCADE, 
                              related_name='watch_parties')
    start_time = models.DateTimeField()
    
    
class WatchPartyAttendance(models.Model):
    DECLINED = 1
    PENDING = 2
    ATTENDING = 3
    
    STATUSES = (
        (DECLINED, 'Declined'),
        (PENDING, 'Pending'),
        (ATTENDING, 'Attending')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watch_party = models.ForeignKey(WatchParty, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=STATUSES)
    
    class Meta:
        unique_together = ['user', 'watch_party']