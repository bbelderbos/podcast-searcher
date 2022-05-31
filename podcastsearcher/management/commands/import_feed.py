from django.core.management.base import BaseCommand, CommandError

from podcastsearcher.models import Podcast, PodcastOrmCacher
from podcast.search import PodcastSearcher


class Command(BaseCommand):
    help = 'Import a feed into the DB'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--feed', required=True)
        parser.add_argument(
            '-n', '--name', required=True)

    def handle(self, *args, **options):
        name = options["name"]
        feed = options["feed"]
        # could move this into the cacher possibly:
        podcast, created = Podcast.objects.get_or_create(name=name, url=feed)
        if not created:
            raise CommandError("Feed already imported")
        PodcastSearcher(feed, cacher=PodcastOrmCacher).entries
