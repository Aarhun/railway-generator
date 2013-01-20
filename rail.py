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
    

class LocalizedRail(object):
    """
    Localized rail part.
    """
    
    def __init__(self, rail):
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None
        self.name = rail.name
        self.rail = rail
        self.localized_sides = []
        
        for side in self.rail.sides:
            self.localized_sides.append(LocalizedSide(side, self))

        
        
    def is_overlapping(self, _rail):
        """
        Check if two rails part are overlapping.
        """

        if self.is_located() and _rail.is_located():
            if (self.min_x < _rail.max_x and self.max_x > _rail.min_x and self.min_y < _rail.max_y and self.max_y > _rail.min_y):
                for _side in self.localized_sides:
                    if _side.is_connected() and _side.connected_to.localized_rail == _rail:
                        # LOGGER.debug("Rail %s and rail %s are connected, assuming they are not overlapping." % (self.name, _rail.name))
                        return False
                else:
                    return True

        else:
            raise AssertionError("Rails must be located in order to check if they overlapps each other.")
        
        
    def is_located(self):
        """
        Simply check if rail location has been defined.
        """
        return not (self.min_x is None or self.max_x is None or self.min_y is None or self.max_y is None)
        
    def update_sides(self):
        """
        Update other sides position (x,y) and direction.
        """
        for side in self.localized_sides:

            if side.loc_x is None or side.loc_y is None or side.direction is None:
                continue

            _ret = self.rail.side_calc(side, self.localized_sides)
            self.min_x = _ret.get("min_x")
            self.max_x = _ret.get("max_x")
            self.min_y = _ret.get("min_y")
            self.max_y = _ret.get("max_y")
            break
        else:
            raise ValueError("At least on side should have a location and a direction to update the other.")




    def update_connected_sides(self):
        """
        Update location (x,y) and direction of connected sides.
        """
        for side in self.localized_sides:
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
                    LOGGER.warning("Rail are connected but sides involved are not in the right direction. %d <> %d" % (side.connected_to.direction, opposite_direction))
                side.connected_to.direction = opposite_direction
                
    

    
    


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

        

    def side_calc(self, localized_side, sides):
        """
        Calculate location and direction of other side of the rail part from a defined side.
        This function define the form of the rail part.
        """
        raise NotImplementedError("Should be implemented by derived class.")





class StraightType(Rail):
    """
    Straight rail template.
    """
    def side_calc(self, localized_side, sides):
        """
        Calculate localized side location from the other.
        Return the min_x/max and min_y/max of localized rail.
        """

        _next_index = (sides.index(localized_side) + 1) % len(sides)
        _side_to_assign = sides[_next_index]
        _square_side = int(round(math.cos(math.radians(45)) * self.length))
        _square_side_width = int(round(math.cos(math.radians(45)) * (self.width / 2)))
        # LOGGER.debug(_square_side)
        container_box = {}


        if localized_side.direction == Direction.N:
            side_assign(localized_side.loc_x, localized_side.loc_y - self.length, Direction.S, _side_to_assign)
            container_box.setdefault("min_x", localized_side.loc_x - (self.width / 2))
            container_box.setdefault("max_x", localized_side.loc_x + (self.width / 2))
            container_box.setdefault("min_y", localized_side.loc_y - self.length)
            container_box.setdefault("max_y", localized_side.loc_y)

        elif localized_side.direction == Direction.NE:
            side_assign(localized_side.loc_x - _square_side, localized_side.loc_y - _square_side, Direction.SO, _side_to_assign)
            container_box.setdefault("min_x", localized_side.loc_x - _square_side_width - _square_side)
            container_box.setdefault("max_x", localized_side.loc_x + _square_side_width)
            container_box.setdefault("min_y", localized_side.loc_y - _square_side_width - _square_side)
            container_box.setdefault("max_y", localized_side.loc_y + _square_side_width)

        elif localized_side.direction == Direction.E:
            side_assign(localized_side.loc_x - self.length, localized_side.loc_y, Direction.O, _side_to_assign)
            container_box.setdefault("min_x", localized_side.loc_x - self.length)
            container_box.setdefault("max_x", localized_side.loc_x)
            container_box.setdefault("min_y", localized_side.loc_y - (self.width / 2))
            container_box.setdefault("max_y", localized_side.loc_y + (self.width / 2)             )

        elif localized_side.direction == Direction.SE:
            side_assign(localized_side.loc_x - _square_side, localized_side.loc_y + _square_side, Direction.NO, _side_to_assign)
            container_box.setdefault("min_x", localized_side.loc_x - _square_side_width - _square_side)
            container_box.setdefault("max_x", localized_side.loc_x + _square_side_width)
            container_box.setdefault("min_y", localized_side.loc_y - _square_side_width)
            container_box.setdefault("max_y", localized_side.loc_y + _square_side_width + _square_side            )

        elif localized_side.direction == Direction.S:
            side_assign(localized_side.loc_x, localized_side.loc_y + self.length, Direction.N, _side_to_assign)
            container_box.setdefault("min_x", localized_side.loc_x - (self.width / 2))
            container_box.setdefault("max_x", localized_side.loc_x + (self.width / 2))
            container_box.setdefault("min_y", localized_side.loc_y)
            container_box.setdefault("max_y", localized_side.loc_y + self.length          )

        elif localized_side.direction == Direction.SO:
            side_assign(localized_side.loc_x + _square_side, localized_side.loc_y + _square_side, Direction.NE, _side_to_assign)
            container_box.setdefault("min_x", localized_side.loc_x - _square_side_width)
            container_box.setdefault("max_x", localized_side.loc_x + _square_side_width + _square_side)
            container_box.setdefault("min_y", localized_side.loc_y - _square_side_width)
            container_box.setdefault("max_y", localized_side.loc_y + _square_side_width + _square_side            )

        elif localized_side.direction == Direction.O:
            side_assign(localized_side.loc_x + self.length, localized_side.loc_y, Direction.E, _side_to_assign)
            container_box.setdefault("min_x", localized_side.loc_x)
            container_box.setdefault("max_x", localized_side.loc_x + self.length)
            container_box.setdefault("min_y", localized_side.loc_y - (self.width / 2))
            container_box.setdefault("max_y", localized_side.loc_y + (self.width / 2)               )

        elif localized_side.direction == Direction.NO:
            side_assign(localized_side.loc_x + _square_side, localized_side.loc_y - _square_side, Direction.SE, _side_to_assign)
            container_box.setdefault("min_x", localized_side.loc_x - _square_side_width)
            container_box.setdefault("max_x", localized_side.loc_x + _square_side_width + _square_side)
            container_box.setdefault("min_y", localized_side.loc_y - _square_side_width - _square_side)
            container_box.setdefault("max_y", localized_side.loc_y + _square_side_width   )

        return container_box

    

class CurvedType(Rail):
    """
    Curved rail template
    """

    def __init__(self, radius, angle=45, **other_args):
        self.radius = radius
        self.angle = angle
        self.length = int(round((math.pi * self.radius * 2 * self.angle) / 360))
        super(CurvedType, self).__init__(length=self.length, curved=True, **other_args)


    def side_calc(self, localized_side, sides):
        """
        Calculate side location from the other.
        """

        _next_index = (sides.index(localized_side) + 1) % len(sides)
        _side_to_assign = sides[_next_index]
        _reverted = self.reverted
        _big = int(round(math.cos(math.radians(self.angle)) * self.radius))
        _little = self.radius - _big
        _square_side_width = int(round(math.cos(math.radians(45)) * (self.width / 2)))
        # LOGGER.debug(_square_side)
        container_box = {}        
        # LOGGER.debug(_big)
        # LOGGER.debug(_little)

        # LOGGER.debug("Rail %s" % side.rail.name)
        # LOGGER.debug("Side %d defined to (%d,%d)/%s" % (side.rail.sides.index(side), side.loc_x, side.loc_y, side.direction))
        # LOGGER.debug("Calculate side %d location and direction." % (_next_index))
        if self.sides.index(localized_side.side) == 1:
            _reverted = not self.reverted

        if _reverted:
            if localized_side.direction == Direction.N:
                side_assign(localized_side.loc_x + _little, localized_side.loc_y - _big, Direction.SE, _side_to_assign)
                container_box.setdefault("min_x", localized_side.loc_x - (self.width / 2))
                container_box.setdefault("max_x", localized_side.loc_x + _little + _square_side_width)
                container_box.setdefault("min_y", localized_side.loc_y - _big - _square_side_width)
                container_box.setdefault("max_y", localized_side.loc_y)

            elif localized_side.direction == Direction.NE:
                side_assign(localized_side.loc_x - _little, localized_side.loc_y - _big, Direction.S, _side_to_assign)
                container_box.setdefault("min_x", localized_side.loc_x  - _little - (self.width / 2))
                container_box.setdefault("max_x", localized_side.loc_x + _square_side_width)
                container_box.setdefault("min_y", localized_side.loc_y - _big)
                container_box.setdefault("max_y", localized_side.loc_y + _square_side_width)

            elif localized_side.direction == Direction.E:
                side_assign(localized_side.loc_x - _big, localized_side.loc_y - _little, Direction.SO, _side_to_assign)
                container_box.setdefault("min_x", localized_side.loc_x - _big - _square_side_width)
                container_box.setdefault("max_x", localized_side.loc_x)
                container_box.setdefault("min_y", localized_side.loc_y - _little - _square_side_width)
                container_box.setdefault("max_y", localized_side.loc_y + (self.width / 2))

            elif localized_side.direction == Direction.SE:
                side_assign(localized_side.loc_x - _big, localized_side.loc_y + _little, Direction.O, _side_to_assign)
                container_box.setdefault("min_x", localized_side.loc_x  - _big)
                container_box.setdefault("max_x", localized_side.loc_x + _square_side_width)
                container_box.setdefault("min_y", localized_side.loc_y - _square_side_width)
                container_box.setdefault("max_y", localized_side.loc_y + _little + (self.width / 2))

            elif localized_side.direction == Direction.S:
                side_assign(localized_side.loc_x - _little, localized_side.loc_y + _big, Direction.NO, _side_to_assign)
                container_box.setdefault("min_x", localized_side.loc_x - _little - _square_side_width)
                container_box.setdefault("max_x", localized_side.loc_x + (self.width / 2))
                container_box.setdefault("min_y", localized_side.loc_y)
                container_box.setdefault("max_y", localized_side.loc_y + _big + _square_side_width                )

            elif localized_side.direction == Direction.SO:
                side_assign(localized_side.loc_x + _little, localized_side.loc_y + _big, Direction.N, _side_to_assign)
                container_box.setdefault("min_x", localized_side.loc_x - _square_side_width)
                container_box.setdefault("max_x", localized_side.loc_x + _little + (self.width / 2))
                container_box.setdefault("min_y", localized_side.loc_y - _square_side_width)
                container_box.setdefault("max_y", localized_side.loc_y + _big     )

            elif localized_side.direction == Direction.O:
                side_assign(localized_side.loc_x + _big, localized_side.loc_y + _little, Direction.NE, _side_to_assign)
                container_box.setdefault("min_x", localized_side.loc_x)
                container_box.setdefault("max_x", localized_side.loc_x + _big + _square_side_width)
                container_box.setdefault("min_y", localized_side.loc_y - (self.width / 2))
                container_box.setdefault("max_y", localized_side.loc_y + _little + _square_side_width)

            elif localized_side.direction == Direction.NO:
                side_assign(localized_side.loc_x + _big, localized_side.loc_y - _little, Direction.E, _side_to_assign)
                container_box.setdefault("min_x", localized_side.loc_x - _square_side_width)
                container_box.setdefault("max_x", localized_side.loc_x + _big)
                container_box.setdefault("min_y", localized_side.loc_y - _little - (self.width / 2))
                container_box.setdefault("max_y", localized_side.loc_y + _square_side_width)
        else:
            if localized_side.direction == Direction.N:
                side_assign(localized_side.loc_x - _little, localized_side.loc_y - _big, Direction.SO, _side_to_assign)
                container_box.setdefault("min_x", localized_side.loc_x - _little - _square_side_width)
                container_box.setdefault("max_x", localized_side.loc_x + (self.width / 2))
                container_box.setdefault("min_y", localized_side.loc_y - _big - _square_side_width)
                container_box.setdefault("max_y", localized_side.loc_y)

            elif localized_side.direction == Direction.NE:
                side_assign(localized_side.loc_x - _big, localized_side.loc_y - _little, Direction.O, _side_to_assign)
                container_box.setdefault("min_x", localized_side.loc_x  - _big)
                container_box.setdefault("max_x", localized_side.loc_x + _square_side_width)
                container_box.setdefault("min_y", localized_side.loc_y - _little - (self.width / 2))
                container_box.setdefault("max_y", localized_side.loc_y + _square_side_width)
                

            elif localized_side.direction == Direction.E:
                side_assign(localized_side.loc_x - _big, localized_side.loc_y + _little, Direction.NO, _side_to_assign)
                container_box.setdefault("min_x", localized_side.loc_x - _big - _square_side_width)
                container_box.setdefault("max_x", localized_side.loc_x)
                container_box.setdefault("min_y", localized_side.loc_y - (self.width / 2))
                container_box.setdefault("max_y", localized_side.loc_y + _little + _square_side_width)

            elif localized_side.direction == Direction.SE:
                side_assign(localized_side.loc_x - _little, localized_side.loc_y + _big, Direction.N, _side_to_assign)
                container_box.setdefault("min_x", localized_side.loc_x - _little - (self.width / 2))
                container_box.setdefault("max_x", localized_side.loc_x + _square_side_width)
                container_box.setdefault("min_y", localized_side.loc_y - _square_side_width)
                container_box.setdefault("max_y", localized_side.loc_y + _big  )

            elif localized_side.direction == Direction.S:
                side_assign(localized_side.loc_x + _little, localized_side.loc_y + _big, Direction.NE, _side_to_assign)
                container_box.setdefault("min_x", localized_side.loc_x - (self.width / 2))
                container_box.setdefault("max_x", localized_side.loc_x + _little + _square_side_width)
                container_box.setdefault("min_y", localized_side.loc_y)
                container_box.setdefault("max_y", localized_side.loc_y + _big + _square_side_width         )

            elif localized_side.direction == Direction.SO:
                side_assign(localized_side.loc_x + _big, localized_side.loc_y + _little, Direction.E, _side_to_assign)
                container_box.setdefault("min_x", localized_side.loc_x - _square_side_width)
                container_box.setdefault("max_x", localized_side.loc_x + _big)
                container_box.setdefault("min_y", localized_side.loc_y - _square_side_width)
                container_box.setdefault("max_y", localized_side.loc_y + _little + (self.width / 2))

            elif localized_side.direction == Direction.O:
                side_assign(localized_side.loc_x + _big, localized_side.loc_y - _little, Direction.SE, _side_to_assign)
                container_box.setdefault("min_x", localized_side.loc_x)
                container_box.setdefault("max_x", localized_side.loc_x + _big + _square_side_width)
                container_box.setdefault("min_y", localized_side.loc_y - _little - _square_side_width)
                container_box.setdefault("max_y", localized_side.loc_y + (self.width / 2))

            elif localized_side.direction == Direction.NO:
                side_assign(localized_side.loc_x + _little, localized_side.loc_y - _big, Direction.S, _side_to_assign)
                container_box.setdefault("min_x", localized_side.loc_x - _square_side_width)
                container_box.setdefault("max_x", localized_side.loc_x + _little + (self.width / 2))
                container_box.setdefault("min_y", localized_side.loc_y - _big)
                container_box.setdefault("max_y", localized_side.loc_y + _square_side_width)
                
        return container_box

class LocalizedSide(object):
    """
    Localized side of rail.
    """

    def __init__(self, side, localized_rail):
                
        self.side = side
        self.localized_rail = localized_rail
        self.connected_to = None
        self.loc_x = None
        self.loc_y = None
        self.direction = None
        
    def connect(self, localized_side):
        """
        Connect two sides.
        """
        if self.side.rail != localized_side.side.rail:
            if self.side.connector_type != localized_side.side.connector_type:
                if localized_side.connected_to is None:
                    # LOGGER.debug("Connected side %d of rail %s to side %d of rail %s" % (self.rail.sides.index(self), self.rail.name, side.rail.sides.index(side), side.rail.name))
                    self.connected_to = localized_side
                    localized_side.connected_to = self
                    localized_side.loc_x = self.loc_x
                    localized_side.loc_y = self.loc_y
                    localized_side.direction = self.direction
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


class Side(object):
    """
    Side of rail
    """

    FEMALE = 0
    MALE = 1

    def __init__(self, rail, connector_type=FEMALE):
        self.rail = rail
        self.connector_type = connector_type



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

