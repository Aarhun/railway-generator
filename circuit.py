"""
Module to define a circuit.
"""

import rail
import logging
import json
import os
import random

LOGGER = logging.getLogger()
HANDLER = logging.NullHandler()
LOGGER.addHandler(HANDLER)

class SearchCircuit(object):
    """
    Search for circuits
    """
    def __init__(self, rails):
        self.rails = rails[:]
        self.uncomplete_circuit = []
        self.good_circuit = []
        self.not_valid_circuit = []
        
    def _recursive_add(self, test_circuit):

        _test_circuit = test_circuit[:]
        _not_used_rails = list(set(self.rails) - set(_test_circuit))
        
        if len(_not_used_rails):
            random.shuffle(_not_used_rails)
            # _next_rail = _not_used_rails[random.randrange(0, len(_not_used_rails))]
            for _next_rail in _not_used_rails:
                _next_rail = rail.LocalizedRail(_next_rail)   
                LOGGER.debug("Following %s" % _next_rail.name)
                _test_circuit[-1].localized_sides[1].connect(_next_rail.localized_sides[0])
                _test_circuit.append(_next_rail)

                if _test_circuit in self.not_valid_circuit:
                    return False
                    
                if _test_circuit in self.uncomplete_circuit:
                    return False                
                    
                if _test_circuit in self.good_circuit:
                    return True
                
                _circuit = Circuit(_test_circuit[0])
                
                if not _circuit.valid:
                    self.not_valid_circuit.append(_test_circuit)
                    LOGGER.info("Circuit is not valid.")
                    return False
                    
                if not _circuit.complete:
                    self.uncomplete_circuit.append(_test_circuit)
                    LOGGER.info("Circuit is not complete.")
                    return self._recursive_add(_test_circuit)
                else:
                    self.good_circuit.append(_test_circuit)
                    return True
                break
                
        else:
            LOGGER.info("No more rails to add.")
            return False
        
        
        
        
    def search(self):
        _already_first = []
        _not_already_first = list(set(self.rails) - set(_already_first))
        
        while len(_not_already_first):
            _rail = _not_already_first[random.randrange(0, len(_not_already_first))]
            _already_first.append(_rail)
        
        
            LOGGER.debug("Start with rail %s" % _rail.name)
            _test_circuit = []
            _test_circuit.append(_rail)
                
            _test = self._recursive_add(_test_circuit)
                
            
           
            if len(self.good_circuit):
                break
                
            _not_already_first = list(set(self.rails) - set(_already_first))
            
        else:
            LOGGER.debug("END without found one :(")
            for elt in self.not_valid_circuit:
                LOGGER.debug(str(elt))
                
                
class Circuit(object):
    """
    Define a circuit.
    """

    def __init__(self, first_rail):
        """
        Initialize a circuit.
        It just need to specify the first rail, as the rail's sides have memory of which rail is connected to.
        To construct the circuit we just need to follow the chain.
        """
        self.rails = []
        self.first_rail = first_rail
        self.first_rail.localized_sides[0].loc_x = 0
        self.first_rail.localized_sides[0].loc_y = 0
        self.first_rail.localized_sides[0].direction = rail.Direction.S
        self.complete = True
        self.valid = True
        self.length = 0
        self.max_x = None
        self.min_x = None
        self.max_y = None
        self.min_y = None
        self.sides_not_connected = []
        self.rails_number = 0

        self.json_repr = {}
        self.json_repr.setdefault("rails", {})
        self._walk_circuit(self.first_rail,
                           funcs=[self._init_length, self._init_sides, self._is_overlapping, self._init_json, self._init_min_max])

        self._try_to_complete_circuit()
        self._convert_location()

        self.json_repr.setdefault("max_x", self.max_x)
        self.json_repr.setdefault("max_y", self.max_y)
        self.json_repr.setdefault("min_x", self.min_x)
        self.json_repr.setdefault("min_y", self.min_y)
        self.rails_number = len(self.rails)
        
        
        LOGGER.debug("Created a circuit of %d rails for a length of %dmm." % (self.rails_number, self.length))
        
    def __str__(self):
        return "<->".join([elt.name for elt in self.rails])
        
        
        
    def _try_to_complete_circuit(self):
        """
        Try to complete the circuit by connecting two rails sides if they are at the same location.
        """
        while len(self.sides_not_connected):
            _side = self.sides_not_connected.pop(0)
            for _side_bis in self.sides_not_connected:
                if _side.loc_x == _side_bis.loc_x and _side.loc_y == _side_bis.loc_y:
                    _side.connect(_side_bis)
                    self.sides_not_connected.remove(_side_bis)
                    LOGGER.debug("Found sides in the same place, not connected, connected them. (rails %s and %s)" % (_side.rail.name, _side_bis.rail.name))
                    break
            else:
                break
        # If there is no more sides 'alone', circuit is complete:
        if not len(self.sides_not_connected):
            self.complete = True
    
    def _is_overlapping(self, _rail):
        for elt in self.rails:
            if elt.is_overlapping(_rail):
                self.valid = False
                LOGGER.error("Two rails (%s and %s) are overlapping !" % (_rail.name, elt.name))
                LOGGER.error("Circuit is not valid.")
                

    def _convert_location(self):
        """
        We need positive location to draw canvas easily.
        """
        delta_x = 0
        delta_y = 0
        if self.min_x < 0:
            delta_x = abs(self.min_x)
            self.min_x += delta_x
            self.max_x += delta_x
        if self.min_y < 0:
            delta_y = abs(self.min_y)
            self.min_y += delta_y
            self.max_y += delta_y

        if delta_x or delta_y:
            for key, value in self.json_repr["rails"].items():
                self.json_repr["rails"][key]["min_x"] += delta_x
                self.json_repr["rails"][key]["max_x"] += delta_x
                self.json_repr["rails"][key]["min_y"] += delta_y
                self.json_repr["rails"][key]["max_y"] += delta_y
                for key_2, value_2 in value["sides"].items():
                    value_2["x"] += delta_x
                    value_2["y"] += delta_y

    def export(self):
        _file = open(os.path.join(os.path.dirname(__file__), "railway.json"), "w")
        _file.write("var railway = ")
        _file.write(json.dumps(self.json_repr))
        _file.close()
        
    def _init_min_max(self, _rail):
        if self.min_x is None or _rail.min_x < self.min_x:
            self.min_x = _rail.min_x
        if self.min_y is None or _rail.min_y < self.min_y:
            self.min_y = _rail.min_y
        if self.max_x is None or _rail.max_x > self.max_x:
            self.max_x = _rail.max_x
        if self.max_y is None or _rail.max_y > self.max_y:
            self.max_y = _rail.max_y   
            
    def _init_json(self, _rail):
        """
        Init dictionnary containing rails.
        """
        # LOGGER.debug("_init_json:%s" % _rail.name)

        self.json_repr["rails"].setdefault(_rail.name, {})
        self.json_repr["rails"][_rail.name].setdefault("sides", {})
        self.json_repr["rails"][_rail.name].setdefault("curved", _rail.rail.curved)
        self.json_repr["rails"][_rail.name].setdefault("reverted", _rail.rail.reverted)
        self.json_repr["rails"][_rail.name].setdefault("color", _rail.rail.color)
        self.json_repr["rails"][_rail.name].setdefault("width", _rail.rail.width)
        self.json_repr["rails"][_rail.name].setdefault("min_x", _rail.min_x)
        self.json_repr["rails"][_rail.name].setdefault("min_y", _rail.min_y)
        self.json_repr["rails"][_rail.name].setdefault("max_x", _rail.max_x)
        self.json_repr["rails"][_rail.name].setdefault("max_y", _rail.max_y)
        if _rail.rail.curved:
            self.json_repr["rails"][_rail.name].setdefault("radius", _rail.rail.radius)
            
        for side in _rail.localized_sides:
            self.json_repr["rails"][_rail.name]["sides"].setdefault(_rail.localized_sides.index(side), {})
            self.json_repr["rails"][_rail.name]["sides"][_rail.localized_sides.index(side)].setdefault("x", side.loc_x)
            self.json_repr["rails"][_rail.name]["sides"][_rail.localized_sides.index(side)].setdefault("y", side.loc_y)
            self.json_repr["rails"][_rail.name]["sides"][_rail.localized_sides.index(side)].setdefault("direction", side.direction)
                



    def _init_sides(self, _rail):
        """
        Update sides and connected sides location and direction.
        If an error occured it means that the circuit is not valid.
        """
        try:
            _rail.update_sides()
        except AssertionError, error:
            self.valid = False
            LOGGER.error(error)
            LOGGER.error("Circuit is not valid.")
            
        try:
            _rail.update_connected_sides()
        except AssertionError, error:
            self.valid = False
            LOGGER.error(error)
            LOGGER.error("Circuit is not valid.")

    def is_valid(self):
        """
        Core of the project, how to determine if a circuit is valid ?

        Should verify if:

        * pieces are not overlapping in a 2d space.
        * pieces chain is a loop, i.e. all pieces are connected to another.

        Three state possible:

        * Circuit is valid.
        * Circuit is valid but not complete.
        * Circuit is not valid.

        :: Note:

        We assume that connection are corrects (male <---> female) as the :py:func:`Side.connect` function check it before connecting two rails.
        (It's not an homophobic assumption however, just that circuit would not possibly work otherwise ;))
        """
        return self.valid


    def _init_length(self, _rail):
        """
        Calculate the length of the circuit by additionnate all length of rail part found.
        Can be not accurate in case of multiples loops.
        """
        self.length = self.length + _rail.rail.length



    def _walk_circuit(self, _rail, funcs=None):
        """
        Walk through all the circuit.
        """
        if _rail in self.rails:
            return

        # LOGGER.info("Walk through rail %s" % _rail.name)

        if _rail.name in [elt.rail.name for elt in self.rails]:
            _rail.name = "%s%s" % (_rail.name, str(random.randrange(0, 10000)))
        
        if funcs:
            for func in funcs:
                try:
                    func(_rail)
                except Exception, error:
                    LOGGER.error(error)
                    break
        

        
        self.rails.append(_rail)
        
            

        for side in _rail.localized_sides:
            if not side.is_connected():
                self.complete = False
                self.sides_not_connected.append(side)
            else:
                self._walk_circuit(side.connected_to.localized_rail, funcs)
        
        










