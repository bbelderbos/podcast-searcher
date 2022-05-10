from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from podcast.cache import PodcastCacher
from podcast.search import PodcastSearcher

app = FastAPI()


class Entry(BaseModel):
    title: str
    description: str
    published: str
    link: str


def _get_entries(entries):
    return [
        Entry(
            title=entry.title,
            description=entry.description,
            published=entry.published,
            link=entry.link
        )
        for entry in entries
    ]


@app.get("/", response_model=list[Entry])
def search(feed: str, term: str):
    ps = PodcastSearcher(feed)
    results = ps.search(term)
    entries = _get_entries(results)
    return entries


@app.post("/refresh", response_model=list[Entry])
def search(feed: str):
    pc = PodcastCacher(feed, refresh=True)
    entries = _get_entries(pc.entries)
    return entries
