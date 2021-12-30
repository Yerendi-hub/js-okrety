from Utils import BoardMarkers, ShipOrientation


class Ship:

    def __init__(self, numberOfMasts, gridFields):
        self.numberOfMasts = numberOfMasts
        self.gridFields = gridFields
        self.isPlaced = False

    def isFieldPartOfTheShip(self, filed):
        return filed in self.gridFields

    def isShipSank(self, grid):
        for field in self.gridFields:
            if grid[field] == BoardMarkers.wreck:
                return True
            if grid[field] != BoardMarkers.shipDamaged:
                return False
        return True

    def setCoords(self, coords, orientation):
        self.gridFields = list()

        if orientation == ShipOrientation.vertical:
            for i in range(self.numberOfMasts):
                self.gridFields.append((coords[0] - i, coords[1]))

        if orientation == ShipOrientation.horizontal:
            for i in range(self.numberOfMasts):
                self.gridFields.append((coords[0], coords[1]+i))