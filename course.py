from point import *
from enum import Enum
import math


class WpMode(Enum):
    """
    enumeration that is necessary to represents the various different ways to make a way point: equal difference of
    longitude compared to vertex of the GreatCircle, or equal difference of longitude compared to starting point
    """
    equal_distance = 0
    equal_difference_of_longitude = 1


class CourseType(Enum):
    """
    enumeration that represents the type of course: quadrantal, or circular
    """
    circular = 0
    quadrantal = 1

class RhumbLine:
    """
    Represents the rhumb line navigation concept. It contains the distance between two points, the course that must
    take to arrive from point A to point B, the point A of departure and the point B of arrival.
    """

    def __init__(self, point_a: Point = Point(), point_b: Point = None, miles: float = None, cog: float = None):
        """
        simple constructor of RhumbLine class, you can make a rhumb line with starting and arrival point or with
        starting point, routes to follow and distance to tread
        :param point_a: starting point
        :param point_b: arrival point
        :param miles: distance to tread
        :param cog: route to follow
        """
        if point_b is not None and (miles is not None or cog is not None):
            raise AttributeError('Cannot make rhumb line with both arrival point, miles and cog')
        elif point_b is None and (miles is None or cog is None):
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
        """
        method that permits to print on screen a simple representation of the Rhumb line route.
        :return:
        """
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
        c_separator = '-' * (max(len(course) + 4, len(distance) + 6)) + '-----> To:|'
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

    def course(self, course_type: CourseType = CourseType.circular) -> float:
        """
        method that returns the route to follow for arrive from point_a to point_b.
        :return : float value representing the route.
        """
        diff_long = self.point_b.longitude - self.point_a.longitude
        diff_lat = self.point_b.latitude - self.point_a.latitude
        if float(diff_long) == 0 and float(diff_lat) == 0:
            return 0
        elif float(diff_lat) == 0:
            if diff_long.sign == 'E':
                return 90
            else:
                return 270
        elif float(diff_long) == 0:
            if diff_lat.sign == 'N':
                return 0
            else:
                return 180
        else:
            diff_meridional_part = meridional_part(self.point_b.latitude) - meridional_part(self.point_a.latitude)
            course = abs(round(math.degrees(math.atan((float(diff_long) * 60) / diff_meridional_part)), 5))

            if course_type == CourseType.quadrantal:
                return course;
            else:
                if 'N' == diff_lat.sign and 'E' == diff_long.sign:
                    return course
                elif 'N' == diff_lat.sign and 'W' == diff_long.sign:
                    return 360 - course
                elif 'S' == diff_lat.sign and 'E' == diff_long.sign:
                    return 180 - course
                else:
                    return 180 + course

    def distance(self) -> float:
        """
        method that returns the nautical miles that is necessary to tread to arrive from point_a to point_b.
        :return : nautical miles to tread from point_a to point_b following self.course() route
        """
        course = self.course()

        if 90 == course or 270 == course:
            diff_long = float(self.point_b.longitude - self.point_a.longitude) * 60
            return abs(round(diff_long * math.cos(math.radians(float(self.point_a.latitude))), 2))

        elif 0 == course or 180 == course:
            diff_lat = float(self.point_b.latitude - self.point_a.latitude) * 60
            return abs(round(diff_lat, 2))

        elif (80 < course < 100) or (260 < course < 280):
            diff_long = float(self.point_b.longitude - self.point_a.longitude) * 60
            average_lat = (float(self.point_a.latitude) + float(self.point_b.latitude)) / 2
            return abs(round((diff_long * math.cos(math.radians(average_lat))) / math.sin(math.radians(course)), 2))

        else:
            diff_lat = float(self.point_b.latitude - self.point_a.latitude) * 60
            return abs(round(diff_lat / math.cos(math.radians(course)), 2))


class GreatCircle:
    def __init__(self, point_a: Point, point_b: Point, wp_number: int = 10, wp_mode: WpMode = WpMode.equal_distance):
        # TODO finish this __init__
        self.point_a = point_a
        self.point_b = point_b
        self.wp_number = wp_number
        self.wp_mode = wp_mode

    def course(self, start_wp: int = None, course_type: CourseType = CourseType.circular ):
        if start_wp is None:
            diff_long = self.point_b.longitude - self.point_a.longitude
            diff_lat = self.point_b.latitude - self.point_a.latitude
            route = math.degrees(math.atan(round(math.sin(math.radians(float(diff_long))), 5) /
                                           (round(math.tan(math.radians(float(self.point_b.latitude))) *
                                                  math.cos(math.radians(float(self.point_a.latitude))), 5) -
                                            round((math.sin(math.radians(float(self.point_a.latitude))) *
                                                   math.cos(math.radians(float(diff_long)))), 5))))
            if course_type == CourseType.quadrantal:
                return round(route, 5)

            else:
                if 'N' == diff_lat.sign and 'E' == diff_long.sign:
                    return round(route, 5)
                elif 'S' == diff_lat.sign and 'E' == diff_long.sign:
                    return round(180 - route, 5)
                elif 'S' == diff_lat.sign and 'W' == diff_long.sign:
                    return round(180 + route, 5)
                else:
                    return round(360 - route, 5)

        else:
            pass  # return Rhumb Line object containing the route from start_wp to next one

    def wp(self, number: int = None):
        if number is None:
            pass  # TODO return list of all way points
        else:
            pass  # TODO return the number way point or in case of out of bound wp return index out of bound error

    def vertex(self) -> Point:
        # TODO debug longitude of this shit!!!!!
        lat_a, course = abs(float(self.point_a.latitude)), self.course(course_type=CourseType.quadrantal)
        long_a = self.point_a.longitude
        lat_v = float_to_latitude(round(math.degrees(math.acos(math.cos(math.radians(lat_a)) * math.sin(
            math.radians(course)))), 5))
        long_v = long_a + float_to_longitude_distance(round(math.degrees(math.atan((1/math.tan(course)) /
                                                                                   math.sin(math.radians(lat_a)))), 5))

        return Point(lat_v, long_v)

    def distance(self):
        diff_long = float(self.point_b.longitude - self.point_a.longitude)
        lat_a = float(self.point_a.latitude)
        lat_b = float(self.point_b.latitude)

        distance = round(math.sin(math.radians(lat_a)), 5) * round(math.sin(math.radians(lat_b)), 5) + \
            round(math.cos(math.radians(lat_a)), 5) * round(math.cos(math.radians(lat_b)), 5) * \
            round(math.cos(math.radians(diff_long)), 5)

        return round(math.degrees(math.acos(distance)) * 60, 5)


class Composite:
    pass


def calc_arrival_point(point_a: Point = Point(), miles: float = 0.0, cog: float = 0.0) -> Point:
    """
    Function that calculates the arrival point, starting from point_a following the route (cog) for 'miles' miles.
    :param point_a: starting point
    :param miles: distance to tread
    :param cog: route to follow
    :return: Point of arrival.
    """
    try:
        miles, cog = float(miles), float(cog)
    except ValueError as e:
        raise TypeError('miles and cog must be numerical value') from e
    if type(point_a) != Point:
        raise TypeError('starting point cannot be of type: {}'.format(type(point_a)))
    else:
        if 90 == cog or 270 == cog:
            diff_long = float_to_longitude_distance((miles / math.cos(math.radians(float(point_a.latitude)))) / 60)
            diff_long.sign = 'E' if 90 == cog else 'W'
            lat_b = point_a.latitude
            long_b = point_a.longitude + diff_long

        elif 0 == cog or 180 == cog:
            diff_lat = float_to_latitude_distance(miles / 60)
            diff_lat.sign = 'N' if 0 == cog else 'S'
            lat_b = point_a.latitude + diff_lat
            long_b = point_a.longitude

        else:
            diff_lat = float_to_latitude_distance((miles * math.cos(math.radians(cog))) / 60)
            lat_b = point_a.latitude + diff_lat

            diff_meridional_parts = meridional_part(lat_b) - meridional_part(point_a.latitude)

            diff_long = float_to_longitude_distance((diff_meridional_parts * math.tan(math.radians(cog))) / 60)

            long_b = point_a.longitude + diff_long

        return Point(lat_b, long_b)
