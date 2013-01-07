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
        rails.append(rail.Curved("curved_1"))

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        self.assertTrue(self.test_circuit.first_rail.sides[0].direction == rail.Direction.S)
        self.assertTrue(self.test_circuit.first_rail.sides[1].direction == rail.Direction.NE)
        self.test_circuit.export()
        
    def nottest_simple_straight(self):
        rails = []
        rails.append(rail.Straight("straight"))

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        self.test_circuit.export()        

    def nottest_simple_curved_reverted(self):
        rails = []
        rails.append(rail.Curved("curved_1", reverted=True))

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        self.test_circuit.export()

    def nottest_simple_loop(self):
        rails = []
        for i in range(8):
            rails.append(rail.Curved("curved_%d" % i))
        for _rail in rails:
            _next_index = (rails.index(_rail) + 1) % len(rails)
            _rail.sides[1].connect(rails[_next_index].sides[0])

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        self.assertTrue(self.test_circuit.complete)
        self.test_circuit.export()

    def nottest_simple_loop_reverted(self):
        rails = []
        for i in range(8):
            rails.append(rail.Curved("curved_%d" % i, reverted=True))
        for _rail in rails:
            _next_index = (rails.index(_rail) + 1) % len(rails)
            _rail.sides[1].connect(rails[_next_index].sides[0])

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        self.assertTrue(self.test_circuit.complete)
        self.test_circuit.export()

    def nottest_too_much_curved(self):
        rails = []
        for i in range(10):
            rails.append(rail.Curved("curved_%d" % i))
        for _rail in rails:
            _next_index = (rails.index(_rail) + 1) % len(rails)
            _rail.sides[1].connect(rails[_next_index].sides[0])

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertFalse(self.test_circuit.valid)

    def nottest_double_simple_loop(self):
        # Should fail if space management is implemented.
        rails = []
        for i in range(16):
            rails.append(rail.Curved("curved_%d" % i))
        for _rail in rails:
            _next_index = (rails.index(_rail) + 1) % len(rails)
            _rail.sides[1].connect(rails[_next_index].sides[0])

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)


    def nottest_loop_with_two_straight(self):
        rails = []
        for i in range(4):
            rails.append(rail.Curved("curved_%d" % i))


        rails.append(rail.Straight("straight_1"))
        for i in range(4):
            rails.append(rail.Curved("curved2_%d" % i))

        rails.append(rail.Straight("straight_2"))

        for _rail in rails:
            _next_index = (rails.index(_rail) + 1) % len(rails)
            _rail.sides[1].connect(rails[_next_index].sides[0])

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        self.assertTrue(self.test_circuit.complete)
        self.test_circuit.export()


    def nottest_only_straight(self):
        rails = []
        for i in range(40):
            rails.append(rail.Straight("straight_%d" % i))


        for _rail in rails[:-1]:
            _next_index = (rails.index(_rail) + 1) % len(rails)
            _rail.sides[1].connect(rails[_next_index].sides[0])

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        self.assertFalse(self.test_circuit.complete)
        self.test_circuit.export()


    def test_clover_circuit(self):
        rails = []
        for j in range(4):
            for i in range(4):
                rails.append(rail.Curved("curved%d_%d" % (j,i)))
            for i in range(2):
                rails.append(rail.Straight("straight%d_%d" % (j,i)))
            for i in range(2):
                rails.append(rail.Curved("curved%d_%d" % (j+1,i), reverted=True))
            for i in range(2):
                rails.append(rail.Straight("straight%d_%d" % (j+1,i)))



        for _rail in rails[:-1]:
            _next_index = (rails.index(_rail) + 1) % len(rails)
            _rail.sides[1].connect(rails[_next_index].sides[0])

        self.test_circuit = circuit.Circuit(rails[0])

        self.assertTrue(self.test_circuit.valid)
        # self.assertTrue(self.test_circuit.complete)
        self.test_circuit.export()

if __name__ == '__main__':
    unittest.main()
