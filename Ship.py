from Utils import BoardMarkers, ShipOrientation


class Ship:
    """ represents ship object with its:
        position,
        number of masts
        information about being placed
        orientation for enemy ship
     """

    def __init__(self, numberOfMasts):
        self.numberOfMasts = numberOfMasts
        self.gridFields = list()
        self.isPlaced = False
        self.enemyOrientation = ShipOrientation.notKnown

    def isFieldPartOfTheShip(self, filed):
        """check if given field is part of ship"""
        return filed in self.gridFields

    def isShipSank(self, grid):
        """check if ship is sank by checking all of its fields"""
        for field in self.gridFields:
            if grid[field[0]][field[1]] == BoardMarkers.wreck:
                return True
            if grid[field[0]][field[1]] != BoardMarkers.shipDamaged:
                return False
        return True

    def setCoords(self, coords, orientation):
        """set ships coords by giving filed and orientation"""
        self.gridFields = list()

        if orientation == ShipOrientation.vertical:
            for i in range(self.numberOfMasts):
                self.gridFields.append((coords[0] - i, coords[1]))

        if orientation == ShipOrientation.horizontal:
            for i in range(self.numberOfMasts):
                self.gridFields.append((coords[0], coords[1]+i))