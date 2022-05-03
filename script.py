import feedparser
from rich.console import Console
from rich.table import Table

console = Console()
error_console = Console(stderr=True, style="bold red")


class PodcastSearcher:

    def __init__(self, podcast, feed):
        self.podcast = podcast
        self.feed = feed
        self.entries = self._load_feed()

    def _load_feed(self):
        return feedparser.parse(self.feed).entries

    def search(self, term):
        term = term.lower()
        matches = []
        for entry in self.entries:
            if term in (entry.title + entry.description).lower():
                matches.append(entry)
        return matches

    def show_results(self, matches):
        if not matches:
            error_console.print(f"No results for {term}")
            return

        table = Table(title=f"Matching {self.podcast} podcast episodes")

        table.add_column("Title", style="magenta")
        table.add_column("Published", style="#c23b22")
        table.add_column("Link", style="#00bfff")

        for row in matches:
            table.add_row(row.title, row.published, row.links[0].href)

        console.print(table)


if __name__ == "__main__":
    podcast = "Pybites"
    feed = "https://feeds.buzzsprout.com/1501156.rss"
    # podcast = "Tim Ferriss Show"
    # feed = "https://rss.art19.com/tim-ferriss-show"
    ps = PodcastSearcher(podcast, feed)

    while True:
        term = input("Enter search term: ")
        if term.lower() == "q":
            print("Bye")
            break
        matches = ps.search(term)
        ps.show_results(matches)
