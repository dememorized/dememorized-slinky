from datetime import datetime, timedelta
from typing import List, Generator

import requests

from transit.transit import Departure


class Departures:
    _lastUpdated: datetime = datetime(1900, 1, 1, 0, 0)
    _departures: List[Departure]
    _key: str
    _site: int

    def __init__(self, site: int, key: str):
        self._key = key
        self._site = site

    def _update(self):
        now = datetime.now()
        print(f"downloading departure time: {now}", flush=True)
        r = requests.get(
            f"https://api.sl.se/api2/realtimedeparturesV4.json?key={self._key}&siteid={self._site}&timewindow=3600"
        )
        data = r.json()
        r.close()

        ds = []
        print(data)
        for key in data["ResponseData"]:
            departures = data["ResponseData"][key]
            if not isinstance(departures, list):
                continue

            for d in departures:
                if "LineNumber" not in d:
                    continue
                dept = Departure(
                    d["JourneyDirection"],
                    d["LineNumber"],
                    d["TransportMode"],
                    d["ExpectedDateTime"],
                )
                ds.append(dept)

        self._departures = ds
        self._lastUpdated = datetime.now()

    def next(self, tmpl: Departure) -> Generator[Departure, None, None]:
        nextUpdate = self._lastUpdated + timedelta(minutes=5)
        print(f"updating image, next update: {nextUpdate}", flush=True)
        if nextUpdate < datetime.now():
            self._update()

        rv = filter(lambda d: d.seconds() > 0, filter(tmpl.filter, self._departures))

        for departure in rv:
            yield departure
