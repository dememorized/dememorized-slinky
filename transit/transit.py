from datetime import datetime
from enum import Enum
from typing import Generator

Mode = Enum("Mode", ["BUS", "METRO", "TRAIN", "TRAM", "SHIP"])


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
            timeFormat = "%Y-%m-%dT%H:%M:%S"
            t1 = datetime.strptime(departure, timeFormat)
            self.departure = t1

    def __str__(self) -> str:
        return f"{self.mode} {self.line} {self.direction} {self.human()}"

    def human(self) -> str:
        t = self.seconds() - 30
        mins = t // 60
        if mins < 0:
            return "0 mins"
        if mins == 1:
            return "1 min"
        return f"{mins} mins"

    def seconds(self) -> int:
        dt = self.departure - datetime.now()
        return int(dt.total_seconds())

    def filter(self, other) -> bool:
        m = self.mode is None or self.mode == other.mode
        li = self.line is None or self.line == other.line
        d = self.direction is None or self.direction == other.direction
        return m and li and d


class Transit:
    def next(self, tmpl: Departure) -> Generator[Departure, None, None]:
        yield Departure("0", "0", "SHIP", datetime.now())
