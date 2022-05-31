from django.contrib import admin

from .models import Podcast, Episode


class PodcastAdmin(admin.ModelAdmin):
    list_display = ("name", "url")
    search_fields = ("name", "url")
admin.site.register(Podcast, PodcastAdmin)


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "published", "url")
    search_fields = ("title", "description", "url")
admin.site.register(Episode, EpisodeAdmin)
