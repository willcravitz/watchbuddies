from django.contrib import admin

# Register your models here.
from .models import (
    User, 
    BuddiesList, 
    Media, 
    WatchedList, 
    Person, 
    MediaCastCrew,
    Comment,
    Chat,
    BuddyGroup,
    BuddyGroupMembership,
    WatchParty,
    WatchPartyAttendance
)

admin.site.register(User)
admin.site.register(BuddiesList)
admin.site.register(Media)
admin.site.register(WatchedList)
admin.site.register(Person)
admin.site.register(MediaCastCrew)
admin.site.register(Comment)
admin.site.register(Chat)
admin.site.register(BuddyGroup)
admin.site.register(BuddyGroupMembership)
admin.site.register(WatchParty)
admin.site.register(WatchPartyAttendance)