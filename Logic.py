import random

import pygame

import RectUtils
import Run
import Data
from Ship import Ship
from Utils import Tour, BoardMarkers, ShipOrientation, GameState


class Logic:
    def __init__(self):
        self.__fillGrid()
        self.__enemyShootsLeft = list()

    def __startGame(self):
        self.__fillListWithShips(Data.enemyShips)
        self.__placeEnemyShips()
        Data.tour = Tour.player if random.getrandbits(1) == 1 else Tour.enemy

        self.__enemyShootsLeft.clear()
        for row in range(0, Data.gridSize):
            for col in range(0, Data.gridSize):
                Data.enemyShoots[row][col] = BoardMarkers.water
                self.__enemyShootsLeft.append((row, col))

        Data.gameState = GameState.game

    def __fillGrid(self):
        self.__fillListWithShips(Data.playerShips)

        for row in range(0, Data.gridSize):
            for col in range(0, Data.gridSize):
                Data.playerShipsGrid[row][col] = BoardMarkers.water
                Data.playerButtonsGrid[row][col] = pygame.Rect(Data.mapMarginX + row * 40,
                                                               Data.spaceY + col * 40, 36, 36)
                Data.enemyShipsGrid[row][col] = BoardMarkers.water
                Data.enemyButtonsGrid[row][col] = pygame.Rect(Data.enemyMapOrigin + row * 40,
                                                              Data.spaceY + col * 40, 36, 36)

    def gameLogic(self):
        if Data.tour == Tour.enemy:
            field = self.__getDamagedShip()

            if field is not None:
                self.__guessNextField(field)
            else:
                self.__shootRandomField()

            field = self.__getDamagedShip()

            if field is not None:
                ship = self.__getShipWithGivenCoordinates(field, Data.playerShips)
                if ship.isShipSank(Data.playerShipsGrid):
                    for field in ship.gridFields:
                        Data.playerShipsGrid[field[0]][field[1]] = BoardMarkers.wreck
                        Data.enemyShoots[field[0]][field[1]] = BoardMarkers.wreck
                        fieldsAround = self.__getFieldAround(field)
                        for fa in fieldsAround:
                            if fa not in ship.gridFields and self.__isFieldInGrid(fa):
                                Data.enemyShoots[fa[0]][fa[1]] = BoardMarkers.shipNeighborhood

            if not self.__andShipsLeft(Data.playerShipsGrid):
                Data.tour = Tour.gameEnd
                Data.winner = Tour.enemy
            else:
                Data.tour = Tour.player

    def __fillListWithShips(self, shipsList):
        shipsList.clear()

        for i in range(Data.fourMast):
            shipsList.append(Ship(4))
        for i in range(Data.threeMast):
            shipsList.append(Ship(3))
        for i in range(Data.twoMast):
            shipsList.append(Ship(2))
        for i in range(Data.oneMast):
            shipsList.append(Ship(1))

    def __getDamagedShip(self):
        for row in range(0, Data.gridSize):
            for col in range(0, Data.gridSize):
                if Data.playerShipsGrid[row][col] == BoardMarkers.shipDamaged:
                    return row, col
        return None

    def __andShipsLeft(self, grid):
        for row in range(0, Data.gridSize):
            for col in range(0, Data.gridSize):
                if grid[row][col] == BoardMarkers.shipDamaged or grid[row][col] == BoardMarkers.ship:
                    return True
        return False

    def __getShipWithGivenCoordinates(self, field, ships):
        for ship in ships:
            if field in ship.gridFields:
                return ship
        return None



    def __guessNextField(self, field):
        ship = self.__getShipWithGivenCoordinates(field, Data.playerShips)
        fields = list()

        for f in ship.gridFields:
            if Data.enemyShoots[f[0]][f[1]] == BoardMarkers.shipDamaged:
                fields.clear()
                if ship.enemyOrientation == ShipOrientation.notKnown or ship.enemyOrientation == ShipOrientation.vertical:
                    fields.append((f[0], f[1] + 1))
                    fields.append((f[0], f[1] - 1))
                if ship.enemyOrientation == ShipOrientation.notKnown or ship.enemyOrientation == ShipOrientation.horizontal:
                    fields.append((f[0] + 1, f[1]))
                    fields.append((f[0] - 1, f[1]))
                found = False
                for fl in fields:
                    if self.__isFieldInGrid(fl) and Data.enemyShoots[fl[0]][fl[1]] == BoardMarkers.water:
                        found = True
                if found:
                    break

        newField = random.choice(fields)

        while not self.__isFieldInGrid(newField) or Data.enemyShoots[newField[0]][newField[1]] != BoardMarkers.water:
            newField = random.choice(fields)
            fields.remove(newField)

        if ship.enemyOrientation == ShipOrientation.notKnown and Data.playerShipsGrid[newField[0]][newField[1]] == BoardMarkers.ship:
            ship.enemyOrientation = ShipOrientation.vertical if newField[1] != field[1] else ShipOrientation.horizontal

        self.__shotGivenField(newField)

    def __shootRandomField(self):
        field = random.choice(self.__enemyShootsLeft)

        while Data.enemyShoots[field[0]][field[1]] != BoardMarkers.water:
            self.__enemyShootsLeft.remove(field)

            if len(self.__enemyShootsLeft) > 0:
                field = random.choice(self.__enemyShootsLeft)

        self.__shotGivenField(field)

    def __shotGivenField(self, field):
        self.__enemyShootsLeft.remove(field)
        marker = BoardMarkers.waterHit
        if Data.playerShipsGrid[field[0]][field[1]] == BoardMarkers.ship:
            marker = BoardMarkers.shipDamaged
        Data.enemyShoots[field[0]][field[1]] = marker
        Data.playerShipsGrid[field[0]][field[1]] = marker

    def __placeShip(self, ship, grid):
        if self.__canShipBePlaced(ship, grid):
            for field in ship.gridFields:
                grid[field[0]][field[1]] = BoardMarkers.ship
                fieldsAround = self.__getFieldAround(field)

                for fa in fieldsAround:
                    if fa not in ship.gridFields and self.__isFieldInGrid(fa):
                        grid[fa[0]][fa[1]] = BoardMarkers.shipNeighborhood
            return True
        return False

    def __getFieldAround(self, field):
        return ((field[0] - 1, field[1] + 1), (field[0], field[1] + 1), (field[0] + 1, field[1] + 1),
                (field[0] - 1, field[1]), (field[0] + 1, field[1]),
                (field[0] - 1, field[1] - 1), (field[0], field[1] - 1), (field[0] + 1, field[1] - 1))

    def __canShipBePlaced(self, ship, grid):
        if ship.numberOfMasts == 0:
            return False

        for field in ship.gridFields:
            if not self.__isFieldInGrid(field):
                return False

            if grid[field[0]][field[1]] != BoardMarkers.water:
                return False

        return True

    def __placeEnemyShips(self, fuse=0):
        tempShips = list()
        for row in range(0, Data.gridSize):
            for col in range(0, Data.gridSize):
                tempShips.append((row, col))

        for ship in Data.enemyShips:
            while len(tempShips) > 0 and not ship.isPlaced:
                gridField = random.choice(tempShips)
                Data.shipOrientation = ShipOrientation.vertical if random.getrandbits(
                    1) == 1 else ShipOrientation.horizontal
                ship.setCoords(gridField, Data.shipOrientation)

                if not self.__placeShip(ship, Data.enemyShipsGrid):
                    Data.shipOrientation = ShipOrientation.vertical if Data.shipOrientation == ShipOrientation.horizontal else ShipOrientation.horizontal
                    ship.setCoords(gridField, Data.shipOrientation)
                    ship.isPlaced = self.__placeShip(ship, Data.enemyShipsGrid)
                else:
                    ship.isPlaced = True

                tempShips.remove(gridField)

        if Data.anyShipLeftToPlace(Data.enemyShips):
            if fuse < 5:
                self.__placeEnemyShips(fuse + 1)
            else:
                print("Cant place enemy ships")

    def __isFieldInGrid(self, field):
        if field[0] < 0 or field[0] > Data.gridSize - 1 or field[1] < 0 or field[1] > Data.gridSize - 1:
            return False
        return True

    def prepareToPlaceShip(self, mastCount, orientation):
        Data.currentShip.numberOfMasts = mastCount
        Data.shipOrientation = orientation

    def handleKeyPress(self, key):
        if key == pygame.K_r:
            Data.shipOrientation = ShipOrientation.vertical if Data.shipOrientation == ShipOrientation.horizontal else ShipOrientation.horizontal

    def handleRightMouseDown(self):
        Data.currentShip.numberOfMasts = 0

    def handleLeftMouseDown(self):
        mouse_pos = pygame.mouse.get_pos()

        if Data.gameState != GameState.menu:
            if Data.resetButton.collidepoint(mouse_pos):
                Data.gameState = GameState.placeShips
                self.__fillGrid()

        if Data.gameState == GameState.menu:
            if Data.startButton.collidepoint(mouse_pos):
                Data.gameState = GameState.placeShips
            if Data.quitButton.collidepoint(mouse_pos):
                Run.quitGame()
        elif Data.gameState == GameState.placeShips:
            if Data.startButton.collidepoint(mouse_pos) and not Data.anyShipLeftToPlace(Data.playerShips):
                self.__startGame()
            if Data.oneMastButton.collidepoint(mouse_pos) and Data.countUnplacedShips(1) > 0:
                Data.currentShip.numberOfMasts = 1
            if Data.twoMastButton.collidepoint(mouse_pos) and Data.countUnplacedShips(2) > 0:
                Data.currentShip.numberOfMasts = 2
            if Data.threeMastButton.collidepoint(mouse_pos) and Data.countUnplacedShips(3) > 0:
                Data.currentShip.numberOfMasts = 3
            if Data.fourMastButton.collidepoint(mouse_pos) and Data.countUnplacedShips(4) > 0:
                Data.currentShip.numberOfMasts = 4

            for row in range(0, Data.gridSize):
                for col in range(0, Data.gridSize):
                    button = Data.playerButtonsGrid[row][col]

                    if button.collidepoint(mouse_pos):
                        if self.__placeShip(Data.currentShip, Data.playerShipsGrid):
                            ship = next((x for x in Data.playerShips if
                                         x.numberOfMasts == Data.currentShip.numberOfMasts and not x.isPlaced),
                                        None)
                            ship.isPlaced = True
                            ship.gridFields.clear()
                            for field in Data.currentShip.gridFields:
                                ship.gridFields.append((field[0], field[1]))
                            Data.currentShip.numberOfMasts = 0

        elif Data.gameState == GameState.game:
            if Data.tour == Tour.player:
                for row in range(0, Data.gridSize):
                    for col in range(0, Data.gridSize):
                        button = Data.enemyButtonsGrid[row][col]
                        mouse_pos = pygame.mouse.get_pos()

                        if button.collidepoint(mouse_pos):
                            coord = RectUtils.getEnemyBoardCoordinate(mouse_pos)
                            cm = Data.enemyShipsGrid[coord[0]][coord[1]]
                            if cm != BoardMarkers.waterHit and cm != BoardMarkers.shipDamaged and cm != BoardMarkers.wreck:
                                marker = BoardMarkers.waterHit if Data.enemyShipsGrid[coord[0]][coord[
                                    1]] != BoardMarkers.ship else BoardMarkers.shipDamaged
                                Data.enemyShipsGrid[coord[0]][coord[1]] = marker

                                if marker == BoardMarkers.shipDamaged:
                                    ship = self.__getShipWithGivenCoordinates(coord, Data.enemyShips)
                                    if ship.isShipSank(Data.enemyShipsGrid):
                                        for field in ship.gridFields:
                                            Data.enemyShipsGrid[field[0]][field[1]] = BoardMarkers.wreck

                                if not self.__andShipsLeft(Data.enemyShipsGrid):
                                    Data.tour = Tour.gameEnd
                                    Data.winner = Tour.player
                                else:
                                    Data.tour = Tour.enemy
