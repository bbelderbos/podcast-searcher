import typer

from .search import PodcastSearcher

app = typer.Typer()


@app.command()
def search(feed: str, term: str):
    ps = PodcastSearcher(feed)
    results = ps.search(term)
    ps.show_results(results)


if __name__ == "__main__":
    app()
