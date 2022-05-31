from django.shortcuts import render

from podcast.search import PodcastSearcher
from .models import PodcastOrmCacher, Podcast

DEFAULT_FEED = "https://feeds.buzzsprout.com/1501156.rss"


def index(request):
    feed = request.POST.get("feed", DEFAULT_FEED)
    term = request.POST.get("term", "")

    ps = PodcastSearcher(feed, cacher=PodcastOrmCacher)
    entries = ps.search(term)

    podcasts = Podcast.objects.all()
    context = {
        "entries": entries,
        "feed": feed,
        "term": term,
        "podcasts": podcasts,
    }
    return render(request, "index.html", context)
