"""
Module to define a rail.
"""
import logging
import math

LOGGER = logging.getLogger()
HANDLER = logging.NullHandler()
LOGGER.addHandler(HANDLER)


def side_assign(new_x, new_y, new_direction, side_to_assign):
    """
    Assign location (x,y) and direction to a side.
    Check firts is previous assignement is the same.
    """
    if side_to_assign.loc_x is not None and side_to_assign.loc_x != new_x:
        raise AssertionError("Side x (%s) already defined but not what it should be (%s)"
                            % (str(side_to_assign.loc_x), str(new_x)))
    if side_to_assign.loc_y is not None and side_to_assign.loc_y != new_y:
        raise AssertionError("Side y (%s) already defined but not what it should be (%s)"
                            % (str(side_to_assign.loc_y), str(new_y)))
    if side_to_assign.direction is not None and side_to_assign.direction != new_direction:
        raise AssertionError("Side direction (%s) already defined but not what it should be (%s)"
                            % (str(side_to_assign.direction), str(new_direction)))

    side_to_assign.loc_x = new_x
    side_to_assign.loc_y = new_y
    side_to_assign.direction = new_direction
    # LOGGER.debug("Assigned rail %s side %d location to (%d,%d) and direction to %s" % (side_to_assign.rail.name, side_to_assign.rail.sides.index(side_to_assign), new_x, new_y, new_direction))

class Direction(object):
    """
    Class to define constant to indicate which direction a side is facing.
    """
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SO = 5
    O = 6
    NO = 7

class Rail(object):
    """
    General rail part.
    """


    def __init__(self, name, length, width=40, heigth=12, sides=None, curved=False, reverted=False, color="#3cb371"):
        """
        Initialize a rail.

        :param length: The length of the part in millimeters.
        :type length: int

        Optional:

        :param width: The width of the part in millimeters.
        :type width: int
        :param heigth: The heigth of the part in millimeters.
        :type heigth: int
        :param angle: The angle of the part.
        :type angle: int
        :param sides: List of sides of the piece, by default two simple sides one with male connector, the other with female connector.
        :type sides: list of :py:class:`Side`
        :param reverted: To tell if piece is reverted. (for curved rail it change the direction of the opposite side)
        :type reverted: bool
        """
        self.length = length
        self.width = width
        self.heigth = heigth
        self.reverted = reverted
        self.sides = []
        self.name = name
        self.curved = curved
        self.color = color

        if sides:
            self.sides = sides[:]
        else:
            # By default, one side female, and one side male.
            self.sides.append(Side(self))
            self.sides.append(Side(self, Side.MALE))

        # LOGGER.debug("Created rail %s" % self.name)


    def update_sides(self):
        """
        Update other sides position (x,y) and direction.
        """
        for side in self.sides:

            if side.loc_x is None or side.loc_y is None or side.direction is None:
                continue

            self._side_calc(side)
            break
        else:
            raise ValueError("At least on side should have a location and a direction to update the other.")



    def _side_calc(self, side):
        """
        Calculate location and direction of other side of the rail part from a defined side.
        This function define the form of the rail part.
        """
        raise NotImplementedError("Should be implemented by derived class.")

    def update_connected_sides(self):
        """
        Update location (x,y) and direction of connected sides.
        """
        for side in self.sides:
            if side.connected_to is not None:
                if side.connected_to.loc_x is not None and side.connected_to.loc_x != side.loc_x:
                    raise AssertionError("Rail are connected but sides involved are not at the same x location.")
                else:
                    side.connected_to.loc_x = side.loc_x
                if side.connected_to.loc_y is not None and side.connected_to.loc_y != side.loc_y:
                    raise AssertionError("Rail are connected but sides involved are not at the same y location.")
                else:
                    side.connected_to.loc_y = side.loc_y

                opposite_direction = (side.direction + 4) % 8
                if side.connected_to.direction is not None and side.connected_to.direction != opposite_direction:
                    raise AssertionError("Rail are connected but sides involved are not in the right direction.")
                else:
                    side.connected_to.direction = opposite_direction




class StraightType(Rail):
    """
    Straight rail template.
    """
    def _side_calc(self, side):

        _next_index = (self.sides.index(side) + 1) % len(self.sides)
        _side_to_assign = self.sides[_next_index]
        _square_side = int(round(math.cos(math.radians(45)) * self.length))
        LOGGER.debug(_square_side)

        if side.direction == Direction.N:
            side_assign(side.loc_x, side.loc_y - self.length, Direction.S, _side_to_assign)

        elif side.direction == Direction.NE:
            side_assign(side.loc_x - _square_side, side.loc_y - _square_side, Direction.SO, _side_to_assign)

        elif side.direction == Direction.E:
            side_assign(side.loc_x - self.length, side.loc_y, Direction.O, _side_to_assign)

        elif side.direction == Direction.SE:
            side_assign(side.loc_x - _square_side, side.loc_y + _square_side, Direction.NO, _side_to_assign)

        elif side.direction == Direction.S:
            side_assign(side.loc_x, side.loc_y + self.length, Direction.N, _side_to_assign)

        elif side.direction == Direction.SO:
            side_assign(side.loc_x + _square_side, side.loc_y + _square_side, Direction.NE, _side_to_assign)

        elif side.direction == Direction.O:
            side_assign(side.loc_x + self.length, side.loc_y, Direction.E, _side_to_assign)

        elif side.direction == Direction.NO:
            side_assign(side.loc_x + _square_side, side.loc_y - _square_side, Direction.SE, _side_to_assign)



class CurvedType(Rail):
    """
    Curved rail template
    """

    def __init__(self, radius, angle=45, **other_args):
        self.radius = radius
        self.angle = angle
        self.length = int(round((math.pi * self.radius * 2 * self.angle) / 360))
        super(CurvedType, self).__init__(length=self.length, curved=True, **other_args)


    def _side_calc(self, side):

        _next_index = (self.sides.index(side) + 1) % len(self.sides)
        _side_to_assign = self.sides[_next_index]
        _reverted = self.reverted
        _big = int(round(math.cos(math.radians(self.angle)) * self.radius))
        _little = self.radius - _big
        LOGGER.debug(_big)
        LOGGER.debug(_little)

        # LOGGER.debug("Rail %s" % side.rail.name)
        # LOGGER.debug("Side %d defined to (%d,%d)/%s" % (side.rail.sides.index(side), side.loc_x, side.loc_y, side.direction))
        # LOGGER.debug("Calculate side %d location and direction." % (_next_index))
        if side.rail.sides.index(side) == 1:
            _reverted = not self.reverted

        if _reverted:
            if side.direction == Direction.N:
                side_assign(side.loc_x + _little, side.loc_y - _big, Direction.SE, _side_to_assign)

            elif side.direction == Direction.NE:
                side_assign(side.loc_x - _little, side.loc_y - _big, Direction.S, _side_to_assign)

            elif side.direction == Direction.E:
                side_assign(side.loc_x - _big, side.loc_y - _little, Direction.SO, _side_to_assign)

            elif side.direction == Direction.SE:
                side_assign(side.loc_x - _big, side.loc_y + _little, Direction.O, _side_to_assign)

            elif side.direction == Direction.S:
                side_assign(side.loc_x - _little, side.loc_y + _big, Direction.NO, _side_to_assign)

            elif side.direction == Direction.SO:
                side_assign(side.loc_x + _little, side.loc_y + _big, Direction.N, _side_to_assign)

            elif side.direction == Direction.O:
                side_assign(side.loc_x + _big, side.loc_y + _little, Direction.NE, _side_to_assign)

            elif side.direction == Direction.NO:
                side_assign(side.loc_x + _big, side.loc_y - _little, Direction.E, _side_to_assign)
        else:
            if side.direction == Direction.N:
                side_assign(side.loc_x - _little, side.loc_y - _big, Direction.SO, _side_to_assign)

            elif side.direction == Direction.NE:
                side_assign(side.loc_x - _big, side.loc_y - _little, Direction.O, _side_to_assign)

            elif side.direction == Direction.E:
                side_assign(side.loc_x - _big, side.loc_y + _little, Direction.NO, _side_to_assign)

            elif side.direction == Direction.SE:
                side_assign(side.loc_x - _little, side.loc_y + _big, Direction.N, _side_to_assign)

            elif side.direction == Direction.S:
                side_assign(side.loc_x + _little, side.loc_y + _big, Direction.NE, _side_to_assign)

            elif side.direction == Direction.SO:
                side_assign(side.loc_x + _big, side.loc_y + _little, Direction.E, _side_to_assign)

            elif side.direction == Direction.O:
                side_assign(side.loc_x + _big, side.loc_y - _little, Direction.SE, _side_to_assign)

            elif side.direction == Direction.NO:
                side_assign(side.loc_x + _little, side.loc_y - _big, Direction.S, _side_to_assign)





class Side(object):
    """
    Side of rail
    """

    FEMALE = 0
    MALE = 1

    def __init__(self, rail, connector_type=FEMALE):
        self.rail = rail
        self.connector_type = connector_type
        # Another side connected to it
        self.connected_to = None
        self.loc_x = None
        self.loc_y = None
        self.direction = None


    def connect(self, side):
        """
        Connect two sides.
        """
        if self.rail != side.rail:
            if side.connector_type != self.connector_type:
                if side.connected_to is None:
                    # LOGGER.debug("Connected side %d of rail %s to side %d of rail %s" % (self.rail.sides.index(self), self.rail.name, side.rail.sides.index(side), side.rail.name))
                    self.connected_to = side
                    side.connected_to = self
                    side.loc_x = self.loc_x
                    side.loc_y = self.loc_y
                    side.direction = self.direction
                else:
                    raise AssertionError("Other side is already connected.")
            else:
                raise AssertionError("Connector of same type cannot be connected.")
        else:
            raise AssertionError("Cannot connect a rail to itself.")

    def is_connected(self):
        """
        Check if a side is connected.
        """
        if self.connected_to:
            return True


class LittleCurved(CurvedType):
    def __init__(self, name, reverted=False):
        super(LittleCurved, self).__init__(radius=100, name=name, reverted=reverted, color="#daa520")

class CommonCurved(CurvedType):
    """
    Common curved rail.

    Circle formed by vario-sytem wooden rail has a diameter of about 45cm (external).
    With a width of 4cm, the internal circle diameter is about 37cm.
    In case of curved piece, the length is calculate like this:

    l = ((pi * external_diameter * angle / 360) + (pi * internal_diameter * angle / 360)) / 2

    Here:
    (17,7 + 14,5) / 2 = 16,1
    """
    def __init__(self, name, reverted=False):
        super(CommonCurved, self).__init__(radius=205, name=name, reverted=reverted)

class LittleStraight(StraightType):
    """
    Little straight rail.
    """
    def __init__(self, name):
        super(LittleStraight, self).__init__(name, length=75, color="#b22222")

class CommonStraight(StraightType):
    """
    Common straight rail.
    """
    def __init__(self, name):
        super(CommonStraight, self).__init__(name, length=150, color="#7b68ee")

