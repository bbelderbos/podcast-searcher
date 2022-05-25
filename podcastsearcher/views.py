from django.shortcuts import render

from podcast.search import PodcastSearcher

DEFAULT_FEED = "https://feeds.buzzsprout.com/1501156.rss"


def index(request):
    feed = request.POST.get("feed", DEFAULT_FEED)
    term = request.POST.get("term", "")

    ps = PodcastSearcher(feed)
    entries = ps.search(term)

    context = {
        "entries": entries,
        "feed": feed,
        "term": term,
    }
    return render(request, "index.html", context)
