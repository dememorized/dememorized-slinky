from PIL import Image, ImageDraw, ImageFont, ImagePalette
import sl

_fontSm = 14
_fontMd = 18
_fontLg = 24

class DepartureSign:
    _image: Image
    _draw: ImageDraw
    _width: int
    _height: int

    y: int
    lineDistance: int = 4

    def __init__(self, station: str, width: int, height: int):
        self._image = Image.new('P', (width, height), color=0)
        self._image.putpalette([255, 255, 255, 0, 0, 0])
        self._draw = ImageDraw.Draw(self._image)
        self._width = width
        self._height = height
        self.y = 5

        self._drawText(_fontLg, station)
        self.y += 10

    def addDeparture(self, line: str, departures: [sl.Departure]):
        self._drawText(_fontSm, line)

        if len(departures) == 0:
            self._drawText(_fontMd, "...")
        elif len(departures) == 1:
            self._drawText(_fontMd, departures[0].human())
        else:
            self._drawText(_fontMd, departures[0].human())
            self._drawText(_fontMd, departures[1].human())

        self.y += 10

    def _drawText(self, sz: int, line: str):
        font = ImageFont.truetype("Verdana", size=sz)
        self._draw.text((5, self.y), line, fill=1, font=font)
        self.y += sz + self.lineDistance

