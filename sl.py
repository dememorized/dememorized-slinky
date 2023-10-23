from datetime import datetime, timedelta
from enum import Enum
import requests

Mode = Enum('Mode', ['BUS', 'METRO', 'TRAIN', 'TRAM', 'SHIP'])

class Departure:
    direction: str
    line: str
    mode: Mode
    departure: datetime

    def __init__(self, direction, line, mode, departure):
        self.direction = direction
        self.line = line
        self.mode = mode
        if departure:
            timeFormat = '%Y-%m-%dT%H:%M:%S'
            t1 = datetime.strptime(departure, timeFormat)
            self.departure = t1

    def __str__(self) -> str:
        return f'{self.mode} {self.line} {self.direction} {self.human()}'

    def human(self) -> str:
        t = self.seconds() - 30
        mins = t//60
        if mins < 0:
            return '0 mins'
        if mins == 1:
            return '1 min'
        return f'{mins} mins'

    def seconds(self) -> int:
        dt = self.departure - datetime.now()
        return int(dt.total_seconds())

    def filter(self, other) -> bool:
        m = self.mode == None or self.mode == other.mode
        l = self.line == None or self.line == other.line
        d = self.direction == None or self.direction == other.direction
        return m and l and d


class Departures:
    _lastUpdated: datetime = datetime(1900, 1, 1, 0, 0)
    _departures: [Departure]
    _key: str
    _site: int

    def __init__(self, site: int, key: str):
        self._key = key
        self._site = site

    def _update(self):
        now = datetime.now()
        print(f'downloading departure time: {now}', flush=True)
        r = requests.get(f'https://api.sl.se/api2/realtimedeparturesV4.json?key={self._key}&siteid={self._site}&timewindow=3600')
        data = r.json()
        r.close()

        ds = []
        for key in data['ResponseData']:
            departures = data['ResponseData'][key]
            if type(departures) != list:
                continue

            for d in departures:
                if 'LineNumber' not in d:
                    continue
                dept = Departure(d['JourneyDirection'], d['LineNumber'], d['TransportMode'], d['ExpectedDateTime'])
                ds.append(dept)

        self._departures = ds
        self._lastUpdated = datetime.now()

    def next(self, tmpl: Departure) -> [Departure]:
        nextUpdate = self._lastUpdated+timedelta(minutes=5)
        print(f'updating image, next update: {nextUpdate}', flush=True)
        if nextUpdate < datetime.now():
            self._update()

        rv = filter(lambda d: d.seconds() > 0, filter(tmpl.filter, self._departures))
        return list(rv)

