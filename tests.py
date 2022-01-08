import unittest

import Data
import Logic
import Ship
from Utils import ShipOrientation


class TestStringMethods(unittest.TestCase):

    def test_adjacent(self):
        logic = Logic.Logic()
        ship = Ship.Ship(1)
        ship.setCoords((0, 0), ShipOrientation.vertical)
        self.assertTrue(logic._Logic__placeShip(ship, Data.playerShipsGrid))
        # parallel adjacent
        ship.setCoords((1, 0), ShipOrientation.vertical)
        self.assertFalse(logic._Logic__placeShip(ship, Data.playerShipsGrid))

    def test_shoot_empty(self):
        logic = Logic.Logic()
        self.assertTrue(logic._Logic__makeAPlayerShoot((0, 0)))

    def test_ship_shoot(self):
        logic = Logic.Logic()
        ship = Ship.Ship(1)
        ship.setCoords((0, 0), ShipOrientation.vertical)
        self.assertTrue(logic._Logic__makeAPlayerShoot((0, 0)))

    def test_own_ship_shoot(self):
        logic = Logic.Logic()
        # trying to shoot player ship will be shooting outside map
        self.assertFalse(logic._Logic__makeAPlayerShoot((-1, -1)))

    def test_shoot_twice_same_field(self):
        logic = Logic.Logic()
        self.assertTrue(logic._Logic__makeAPlayerShoot((0, 0)))
        self.assertFalse(logic._Logic__makeAPlayerShoot((0, 0)))

    def test_twice_ship_shoot(self):
        logic = Logic.Logic()
        ship = Ship.Ship(1)
        ship.setCoords((0, 0), ShipOrientation.vertical)
        self.assertTrue(logic._Logic__makeAPlayerShoot((0, 0)))
        self.assertFalse(logic._Logic__makeAPlayerShoot((0, 0)))


if __name__ == '__main__':
    unittest.main()
