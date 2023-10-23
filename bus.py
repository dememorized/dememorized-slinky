from inky import InkyPHAT
import time
import image
import sl
import os

def main():
    d = sl.Departures(9142, os.getenv('SL_API_KEY'))
    
    while True:
        sign = image.DepartureSign('Kärrtorp', 104, 212)
        sign.addDeparture('Buss 163', d.next(sl.Departure(1, "163", None, None)))
        sign.addDeparture('Linje 17', d.next(sl.Departure(1, "17", None, None)))

        #sign._image.convert('RGB').show()
        
        display = InkyPHAT('black')
        display.set_image(image.rotate(-90, expand=True))
        display.show()
        time.sleep(30)

if __name__ == '__main__':
    main()
