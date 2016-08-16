from point import *


class RhumbLine:
    """
    Represents the rhumb line navigation concept. It contains the distance between two points, the course that must
    take to arrive from point A to point B, the point A of departure and the point B of arrival.
    """
    def __init__(self, point_a: Point = Point(), point_b: Point = None, miles: float = None, cog: float = None):
        if point_b is not None and (miles is not None or cog is not None):
            raise AttributeError('Cannot make rhumb line with both arrival point, miles and cog')
        elif point_b is None and(miles is None or cog is None):
            raise AttributeError('cannot calculate the arrival point without miles or cog')
        elif point_b is not None:
            if type(point_a) != Point or type(point_b) != Point:
                raise TypeError('departure point and arrival point must be instance of Point class')
            else:
                self.point_a = point_a
                self.point_b = point_b
        elif miles is not None and cog is not None:
            self.point_a = point_a
            self.point_b = calc_arrival_point(self.point_a, miles, cog)

    def __str__(self):
        course = self.course()
        fractional, c_deg = math.modf(course)
        fractional, c_min = math.modf((fractional * 60))
        c_sec = round(fractional * 60, 2)
        course = ' {: >3d}° {: >2d}\' {: >5.2f}"'.format(int(c_deg), int(c_min), c_sec)

        distance = ' {: >8.2f}'.format(self.distance())

        # formatting latitudes and longitudes.
        lat_a = '{deg: >3d}° {min: >2d}\' {sec: >5.2f}" {sign}'.format(
            deg=int(self.point_a.latitude.degrees), min=int(self.point_a.latitude.minutes),
            sec=self.point_a.latitude.seconds, sign=self.point_a.latitude.sign)
        lat_b = '{deg: >3d}° {min: >2d}\' {sec: >5.2f}" {sign}'.format(
            deg=int(self.point_b.latitude.degrees), min=int(self.point_b.latitude.minutes),
            sec=self.point_b.latitude.seconds, sign=self.point_b.latitude.sign)
        long_a = '{deg: >3d}° {min: >2d}\' {sec: >5.2f}" {sign}'.format(
            deg=int(self.point_a.longitude.degrees), min=int(self.point_a.longitude.minutes),
            sec=self.point_a.longitude.seconds, sign=self.point_a.longitude.sign)
        long_b = '{deg: >3d}° {min: >2d}\' {sec: >5.2f}" {sign}'.format(
            deg=int(self.point_b.longitude.degrees), min=int(self.point_b.longitude.minutes),
            sec=self.point_b.longitude.seconds, sign=self.point_b.longitude.sign)

        # making separators
        c_spaces = ' ' * (max(len(str(lat_a)), len(str(lat_a))) + 1)
        c_separator = '-' * (max(len(course)+4, len(distance)+6)) + '-----> To:|'
        tot = len(c_spaces) + len(c_separator)
        t_spaces_1 = ' ' * ((len(c_spaces) + 2) - len(str(lat_a)))
        t_spaces_2 = ' ' * (tot - (len(t_spaces_1) + len(str(lat_a)) + len(course) + 4) - 2)
        b_spaces_1 = ' ' * ((len(c_spaces) + 2) - len(str(long_a)))
        b_spaces_2 = ' ' * (tot - (len(b_spaces_1) + len(str(long_a)) +
                                   len(distance) + 6) - 2)

        # making string
        string = '     | {lat_a}{t_spaces_1}COG:{cog}{t_spaces_2}| {lat_b}\n' \
                 'From:|{c_spaces}{c_sep}\n' \
                 '     | {long_a}{b_spaces_1}Miles:{miles}{b_spaces_2}| {long_b}'

        # formatting and returning string
        return string.format(lat_a=lat_a, lat_b=lat_b, long_a=long_a, long_b=long_b,
                             t_spaces_1=t_spaces_1, t_spaces_2=t_spaces_2,
                             cog=course, c_spaces=c_spaces, c_sep=c_separator,
                             b_spaces_1=b_spaces_1, miles=distance, b_spaces_2=b_spaces_2)

    def course(self) -> float:
        diff_long = self.point_b.longitude - self.point_a.longitude
        diff_lat = self.point_b.latitude - self.point_a.latitude
        diff_meridional_part = meridional_part(self.point_b.latitude) - meridional_part(self.point_a.latitude)
        course = abs(round(math.degrees(math.atan((float(diff_long) * 60) / diff_meridional_part)), 5))

        if 'N' == diff_lat.sign and 'E' == diff_long.sign:
            return course
        elif 'N' == diff_lat.sign and 'W' == diff_long.sign:
            return 360 - course
        elif 'S' == diff_lat.sign and 'E' == diff_long.sign:
            return 180 - course
        else:
            return 180 + course

    def distance(self) -> float:
        course = self.course()

        if (80 < course < 100) or (260 < course < 280):
            diff_long = float(self.point_b.longitude - self.point_a.longitude) * 60
            average_lat = (float(self.point_a.latitude) + float(self.point_b.latitude)) / 2
            return round((diff_long * math.cos(math.radians(average_lat))) / math.sin(math.radians(course)), 2)
        else:
            diff_lat = float(self.point_b.latitude - self.point_a.latitude) * 60
            return round(diff_lat / math.cos(math.radians(course)), 2)


class GreatCircle:
    pass


class Composite:
    pass


def calc_arrival_point(point_a: Point = Point(), miles: float = 0.0, cog: float = 0.0) -> Point:
    if type(point_a) != Point or type(miles) != float or type(cog) != float:
        raise TypeError('cannot make arrival point with: {}, {}, {}'.format(type(point_a), type(miles), type(cog)))
    else:
        diff_lat = float_to_latitude_distance((miles * math.cos(math.radians(cog))) / 60)
        lat_b = point_a.latitude + diff_lat

        diff_meridional_parts = meridional_part(lat_b) - meridional_part(point_a.latitude)

        diff_long = float_to_longitude_distance((diff_meridional_parts * math.tan(math.radians(cog))) / 60)

        long_b = point_a.longitude + diff_long

        return Point(lat_b, long_b)
