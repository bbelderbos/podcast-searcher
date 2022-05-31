from rich.console import Console
from rich.table import Table

from .cache import PodcastCacher

console = Console()


class PodcastSearcher:

    def __init__(self, feed, cacher=PodcastCacher):
        self.feed = feed
        self.cacher = cacher

    @property
    def entries(self):
        try:
            return self._entries
        except AttributeError:
            pass
        self._entries = self.cacher(self.feed).entries
        return self.entries

    def search(self, term):
        term = term.lower()
        results = []
        for entry in self.entries:
            if term in (entry.title + entry.description).lower():
                results.append(entry)
        return results

    def show_results(self, results):
        table = Table(title="Matching podcast episodes")
        table.add_column("Title", style="#ff6e4a")
        table.add_column("Published", style="magenta")
        table.add_column("Link", style="#00bfff")

        for episode in results:
            table.add_row(episode.title, episode.published, episode.link)

        console.print(table)


if __name__ == "__main__":
    feed = "https://feeds.buzzsprout.com/1501156.rss"
    ps = PodcastSearcher(feed)
    while True:
        term = input("Enter search term: ")
        if term.lower() == "q":
            print("Bye")
            break
        results = ps.search(term)
        ps.show_results(results)
