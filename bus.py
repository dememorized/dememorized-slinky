import time
import image
import transit.transit
from transit import sl
import os


def main():
    d = sl.Departures(9142, os.getenv("SL_API_KEY"))
    inky = False

    while True:
        sign = image.DepartureSign("Kärrtorp", 104, 212)
        sign.addDeparture(
            "Buss 163", d.next(transit.transit.Departure(1, "163", None, None))
        )
        sign.addDeparture(
            "Linje 17", d.next(transit.transit.Departure(1, "17", None, None))
        )

        if inky:
            from inky import InkyPHAT # type: ignore

            display = InkyPHAT("black")
            display.set_image(sign._image.rotate(-90, expand=True))
            display.show()
        else:
            sign._image.convert("RGB").show()

        time.sleep(30)


if __name__ == "__main__":
    main()
