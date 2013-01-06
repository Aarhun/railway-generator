"""
Module to define a circuit.
"""

import rail
import logging
import json
import os

LOGGER = logging.getLogger()
HANDLER = logging.NullHandler()
LOGGER.addHandler(HANDLER)



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
        self.first_rail = first_rail
        self.complete = True
        self.valid = True
        self.length = 0
        self.max_x = 0
        self.min_x = 0
        self.max_y = 0
        self.min_y = 0
        self.rails_number = 0
        self.first_rail.sides[0].loc_x = 0
        self.first_rail.sides[0].loc_y = 0
        self.first_rail.sides[0].direction = rail.Direction.S
        self.json_repr = {}
        self._walk_circuit(self.first_rail, 
                           funcs=[self._init_length, self._init_sides, self._init_json])
                  
        self.json_repr.setdefault("max_x", self.max_x)
        self.json_repr.setdefault("max_y", self.max_y)
        self.json_repr.setdefault("min_x", self.min_x)
        self.json_repr.setdefault("min_y", self.min_y)
        LOGGER.debug("Created a circuit of %d rails for a length of %dmm." % (self.rails_number, self.length))

       
    def export(self):
        _file = open(os.path.join(os.path.dirname(__file__), "railway.json"), "w")
        _file.write("var railway = ")
        _file.write(json.dumps(self.json_repr))
        _file.close()
        
    def _init_json(self, _rail):
        """
        Init dictionnary containing rails.
        """
        self.json_repr.setdefault(_rail.name, {})
        self.json_repr[_rail.name].setdefault("sides", {})
        self.json_repr[_rail.name].setdefault("curved", _rail.curved)
        self.json_repr[_rail.name].setdefault("reverted", _rail.reverted)
        for side in _rail.sides:
            self.json_repr[_rail.name]["sides"].setdefault(_rail.sides.index(side), (side.loc_x, side.loc_y, side.direction))
            if side.loc_x < self.min_x:
                self.min_x = side.loc_x
            if side.loc_y < self.min_y:
                self.min_y = side.loc_y
            if side.loc_x > self.max_x:
                self.max_x = side.loc_x
            if side.loc_y > self.max_y:
                self.max_y = side.loc_y   

    
    def _init_sides(self, _rail):
        """
        Update sides and connected sides location and direction.
        If an error occured it means that the circuit is not valid.
        """
        try:
            _rail.update_sides()
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
        
    def _is_overlaping(self, _rail):
        """
        TODO: to implement
        """
        pass
        
    def _init_length(self, _rail):
        """
        Calculate the length of the circuit by additionnate all length of rail part found.
        Can be not accurate in case of multiples loops.
        """
        self.length = self.length + _rail.length
        
        
        
    def _walk_circuit(self, _rail, already_walked=None, funcs=None):
        """
        Walk through all the circuit.
        """
        if already_walked and _rail in already_walked:
            return
            
        LOGGER.info("Walk through rail %s" % _rail.name)
        
        self.rails_number = self.rails_number + 1
    
            
        if not already_walked:
            already_walked = []
        already_walked.append(_rail)
        
        if funcs:
            for func in funcs:
                func(_rail)
                

            
        for side in _rail.sides:
            if not side.is_connected():
                self.complete = False
            else:
                self._walk_circuit(side.connected_to.rail, 
                                   already_walked, funcs)
                
                
                
                
                
                
                
                
                
                
                
                