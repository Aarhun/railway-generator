"""
Module to test circuits
"""

import unittest
import circuit
import rail
import logging

LOGGER = logging.getLogger()
HANDLER = logging.StreamHandler()
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(HANDLER)


class TestValidity(unittest.TestCase):

    def setUp(self):
        self.test_circuit = None

    def nottest_simple_curved(self):
        rails = []
        rails.append(rail.LocalizedRail(rail.CommonCurved("curved_1")))

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        self.assertTrue(self.test_circuit.first_rail.localized_sides[0].direction == rail.Direction.S)
        self.assertTrue(self.test_circuit.first_rail.localized_sides[1].direction == rail.Direction.NE)
        self.test_circuit.export()

    def nottest_simple_straight(self):
        rails = []
        rails.append(rail.LocalizedRail(rail.CommonStraight("straight")))

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        self.test_circuit.export()

    def nottest_simple_curved_reverted(self):
        rails = []
        rails.append(rail.LocalizedRail(rail.CommonCurved("curved_1", reverted=True)))

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        self.test_circuit.export()

    def nottest_simple_loop(self):
        rails = []
        for i in range(8):
            rails.append(rail.LocalizedRail(rail.CommonCurved("curved_%d" % i)))
        for _rail in rails[:-1]:
            _next_index = (rails.index(_rail) + 1) % len(rails)
            _rail.localized_sides[1].connect(rails[_next_index].localized_sides[0])

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        self.assertTrue(self.test_circuit.complete)
        self.test_circuit.export()

    def nottest_simple_loop_reverted(self):
        rails = []
        for i in range(8):
            rails.append(rail.LocalizedRail(rail.CommonCurved("curved_%d" % i, reverted=True)))
        for _rail in rails:
            _next_index = (rails.index(_rail) + 1) % len(rails)
            _rail.localized_sides[1].connect(rails[_next_index].localized_sides[0])

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        self.assertTrue(self.test_circuit.complete)
        self.test_circuit.export()

    def nottest_too_much_curved(self):
        rails = []
        for i in range(10):
            rails.append(rail.LocalizedRail(rail.CommonCurved("curved_%d" % i)))
        for _rail in rails:
            _next_index = (rails.index(_rail) + 1) % len(rails)
            _rail.localized_sides[1].connect(rails[_next_index].localized_sides[0])

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertFalse(self.test_circuit.valid)
        self.test_circuit.export()

    def nottest_double_simple_loop(self):
        rails = []
        for i in range(16):
            rails.append(rail.LocalizedRail(rail.CommonCurved("curved_%d" % i)))
        for _rail in rails:
            _next_index = (rails.index(_rail) + 1) % len(rails)
            _rail.localized_sides[1].connect(rails[_next_index].localized_sides[0])

        self.test_circuit = circuit.Circuit(rails[0])

        self.test_circuit.export()
        self.assertTrue(not self.test_circuit.valid)


    def nottest_loop_with_two_straight(self):
        rails = []
        for i in range(4):
            rails.append(rail.LocalizedRail(rail.CommonCurved("curved_%d" % i)))


        rails.append(rail.LocalizedRail(rail.CommonStraight("straight_1")))
        for i in range(4):
            rails.append(rail.LocalizedRail(rail.CommonCurved("curved2_%d" % i)))

        rails.append(rail.LocalizedRail(rail.CommonStraight("straight_2")))

        for _rail in rails:
            _next_index = (rails.index(_rail) + 1) % len(rails)
            _rail.localized_sides[1].connect(rails[_next_index].localized_sides[0])

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        self.assertTrue(self.test_circuit.complete)
        self.test_circuit.export()
        


    def nottest_only_straight(self):
        rails = []
        for i in range(40):
            rails.append(rail.LocalizedRail(rail.CommonStraight("straight_%d" % i)))


        for _rail in rails[:-1]:
            _next_index = (rails.index(_rail) + 1) % len(rails)
            _rail.localized_sides[1].connect(rails[_next_index].localized_sides[0])

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        self.assertFalse(self.test_circuit.complete)
        self.test_circuit.export()


    def nottest_clover_circuit(self):
        rails = []
        for j in range(4):
            for i in range(4):
                rails.append(rail.LocalizedRail(rail.CommonCurved("curved%d_%d" % (j,i))))
            for i in range(2):
                rails.append(rail.LocalizedRail(rail.CommonStraight("straight%d_%d" % (j,i))))
            for i in range(2):
                rails.append(rail.LocalizedRail(rail.CommonCurved("curved%d_%d" % (j+1,i), reverted=True)))
            for i in range(2):
                rails.append(rail.LocalizedRail(rail.CommonStraight("straight%d_%d" % (j+1,i))))



        for _rail in rails:
            _next_index = (rails.index(_rail) + 1) % len(rails)
            _rail.localized_sides[1].connect(rails[_next_index].localized_sides[0])

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        self.assertTrue(self.test_circuit.complete)
        self.test_circuit.export()
        
    def nottest_cross_circuit(self):
        rails = []
        
        for k in range(2):
            for j in range(2):
                for i in range(6):
                    rails.append(rail.LocalizedRail(rail.LittleCurved("curved")))
                for i in range(2):
                    rails.append(rail.LocalizedRail(rail.CommonStraight("straight")))
                for i in range(2):
                    rails.append(rail.LocalizedRail(rail.CommonCurved("c")))
                for i in range(2):
                    rails.append(rail.LocalizedRail(rail.CommonStraight("straight")))

            for i in range(3):
                rails.append(rail.LocalizedRail(rail.CommonStraight("straight")))                   
            for i in range(6):
                rails.append(rail.LocalizedRail(rail.LittleCurved("curved", reverted=True)))
            for i in range(5):
                rails.append(rail.LocalizedRail(rail.CommonStraight("straight")))
            for i in range(2):
                rails.append(rail.LocalizedRail(rail.CommonCurved("c")))
            for i in range(2):
                rails.append(rail.LocalizedRail(rail.CommonStraight("straight")))   
            
                
        for _rail in rails:
            _next_index = (rails.index(_rail) + 1) % len(rails)
            _rail.localized_sides[1].connect(rails[_next_index].localized_sides[0])

        
        self.test_circuit = circuit.Circuit(rails[0])

        self.test_circuit.export()   
        self.assertTrue(not self.test_circuit.valid)
        self.assertTrue(self.test_circuit.complete)
             

    def nottest_O_O_circuit(self):
        rails = []

        for j in range(1):
            for i in range(1):
                rails.append(rail.LocalizedRail(rail.CommonCurved("curved")))

            for i in range(2):
                rails.append(rail.LocalizedRail(rail.LittleCurved("littlecurved", reverted=True)))

            # for i in range(2):
                # rails.append(rail.LocalizedRail(rail.CommonStraight("straight")))

            # for i in range(2):
                # rails.append(rail.LocalizedRail(rail.LittleStraight("straight")))

            #for i in range(6):
                #rails.append(rail.LocalizedRail(rail.CommonCurved("curved")))


            #for i in range(6):
                #rails.append(rail.LocalizedRail(rail.CommonCurved("curved", reverted=True)))

            #for i in range(5):
                #rails.append(rail.LocalizedRail(rail.CommonCurved("curved")))

            #for i in range(2):
                #rails.append(rail.LocalizedRail(rail.CommonCurved("curved", reverted=True)))



        for _rail in rails[:-1]:
            _next_index = (rails.index(_rail) + 1) % len(rails)
            _rail.localized_sides[1].connect(rails[_next_index].localized_sides[0])

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        #self.assertTrue(self.test_circuit.complete)
        self.test_circuit.export()
        LOGGER.debug(self.test_circuit)
        
    def test_search_circuit_simple_loop(self):
        rails = []
        for i in range(8):
            rails.append(rail.CommonCurved("curved%d" % i))
        for i in range(2):
            rails.append(rail.CommonStraight("straight%d" % i))            
        search_circuit = circuit.SearchCircuit(rails)
        search_circuit.search()

if __name__ == '__main__':
    unittest.main()
