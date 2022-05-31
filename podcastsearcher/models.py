from django.db import models
import feedparser
from dateutil.parser import parse

from podcast.cache import PodcastCacherInterface


class Podcast(models.Model):
    name = models.CharField(max_length=50, unique=True)
    url = models.URLField()

    def __str__(self):
        return self.name


class Episode(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    published = models.DateTimeField()
    url = models.URLField()
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class PodcastOrmCacher(PodcastCacherInterface):

    def __init__(self, feed):
        self.feed = feed

    @property
    def entries(self):
        entries = self._retrieve_entries()
        if not entries:
            self._cache_entries()
            entries = self._retrieve_entries()
        return entries

    def _retrieve_entries(self):
        return Episode.objects.filter(podcast__url=self.feed)

    def _cache_entries(self):
        entries = feedparser.parse(self.feed).entries
        podcast = Podcast.objects.get(url=self.feed)
        for entry in entries:
            Episode.objects.get_or_create(
                title=entry.title,
                description=entry.description,
                published=parse(entry.published),
                url=entry.links[0].href,
                podcast=podcast
            )

