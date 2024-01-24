from typing import Generator

from PIL import Image, ImageDraw, ImageFont

import transit.transit

_fontSm = 14
_fontMd = 18
_fontLg = 24


class DepartureSign:
    _image: Image.Image
    _draw: ImageDraw.ImageDraw
    _width: int
    _height: int

    y: int
    lineDistance: int = 4

    def __init__(self, station: str, width: int, height: int):
        self._image = Image.new("P", (width, height), color=0)
        self._image.putpalette([255, 255, 255, 0, 0, 0])
        self._draw = ImageDraw.Draw(self._image)
        self._width = width
        self._height = height
        self.y = 5

        self._drawText(_fontLg, station)
        self.y += 10

    def addDeparture(
        self, line: str, departures: Generator[transit.transit.Departure, None, None]
    ):
        self._drawText(_fontSm, line)

        i = 0
        for departure in departures:
            self._drawText(_fontMd, departure.human())
            i += 1
            if i == 2:
                break

        self.y += 10

    def _drawText(self, sz: int, line: str):
        font = ImageFont.truetype("Verdana", size=sz)
        self._draw.text((5, self.y), line, fill=1, font=font)
        self.y += sz + self.lineDistance
