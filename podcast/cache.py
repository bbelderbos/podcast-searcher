import os
import sqlite3
from pathlib import Path
from typing import NamedTuple
from urllib.parse import urlparse

import feedparser


class Entry(NamedTuple):
    id: int
    title: str
    description: str
    published: str
    link: str


class PodcastCacher:

    def __init__(self, feed, refresh=False):
        self.feed = feed
        self.dbname = urlparse(self.feed).netloc + ".db"
        if refresh:
            print("Updating cache")
            try:
                os.remove(self.dbname)
            except OSError:
                pass
        if not Path(self.dbname).exists():
            print("Creating cache")
            self._cache_entries()
        self.entries = self._retrieve_entries()

    def _cache_entries(self):
        con = sqlite3.connect(self.dbname)
        con.execute(
            "create table episodes "
            "(id integer primary key, "
            "title varchar unique, "
            "description varchar, "
            "published varchar, "
            "link varchar"
            ")")
        entries = feedparser.parse(self.feed).entries
        with con:
            for entry in entries:
                con.execute(
                    "insert into episodes("
                    "title, description, published, link"
                    ") values (?, ?, ?, ?)",
                    (entry.title, entry.description,
                     entry.published,
                     entry.links[0].href)
                )

    def _retrieve_entries(self):
        con = sqlite3.connect(self.dbname)
        rows = con.execute(
            "select * from episodes").fetchall()
        results = []
        for row in rows:
            results.append(Entry(*row))
        return results
