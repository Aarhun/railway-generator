"""
Module to describe a rail.
"""

class Rail(object):
    """
    General rail part.
    """

    def __init__(self, length, height, width, angle=0, start_sides=None, end_sides=None, reversable=False):
        self.length = length
        self.height = height
        self.width = width
        self.angle = angle
        self.reversable = reversable
        self.start_sides = [Side()]
        self.end_sides = [Side(Side.MALE)]
        if start_sides:
            self.start_sides = start_sides[:]
        if end_sides:
            self.end_sides = end_sides[:]



class Side(Object):
    """
    Side of rail
    """

    FEMALE=0
    MALE=1

    def __init__(self, connector=Side.FEMALE):
        self.connector = connector


class Straight(Rail):
    """
    Common straight rail.
    """

    def __init__(self):
        super(Straight, self).__init__(10, 10, 10)