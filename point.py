from latitude import *
from longitude import *


class Point:
    """
    Class that represents the concept of point on the heart. It has a latitude and a longitude.
    """
    def __init__(self, latitude=Latitude(), longitude=Longitude()):
        #  TODO finish __init__ method
        if type(latitude) == Latitude and type(longitude) == Longitude:
            self.latitude, self.longitude = latitude, longitude
        elif type(latitude) == tuple and type(longitude) == Longitude:
            try:
                a, b, c, d = abs(float(latitude[0])), abs(float(latitude[1])), abs(float(latitude[2])), str(latitude[3])
            except (ValueError, IndexError) as e:
                raise ValueError('the tuple for latitude must be like (degrees, minutes, seconds, sign') from e
            else:
                latitude = Latitude(a, b, c, d)
                self.latitude, self.longitude = latitude, longitude
        elif type(latitude) == Latitude and type(longitude) == tuple:
            try:
                a, b, c = abs(float(longitude[0])), abs(float(longitude[1])), abs(float(longitude[2]))
                d = str(longitude[3])
            except (ValueError, IndexError) as e:
                raise ValueError('the tuple for longitude must be like (degrees, minutes, seconds, sign') from e
            else:
                longitude = Longitude(a, b, c, d)
                self.latitude, self.longitude = latitude, longitude
        elif type(latitude) == tuple and type(longitude) == tuple:
            try:
                a, b, c, d = abs(float(latitude[0])), abs(float(latitude[1])), abs(float(latitude[2])), str(latitude[3])
                e, f, g = abs(float(longitude[0])), abs(float(longitude[1])), abs(float(longitude[2]))
                h = str(longitude[3])
            except (ValueError, IndexError) as e:
                raise ValueError('the tuple for longitude must be like (degrees, minutes, seconds, sign') from e
            else:
                latitude, longitude = Latitude(a, b, c, d), Longitude(e, f, g, h)
                self.latitude, self.longitude = latitude, longitude
        else:
            raise TypeError('cannot make point with types: {} {}'.format(type(latitude), type(longitude)))

    def __str__(self):
        return 'LAT: {}\nLONG: {}'.format(str(self.latitude), str(self.longitude))
