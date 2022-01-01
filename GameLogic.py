import pygame
import Run
import Ship
import random

from Utils import GameData, BoardMarkers, RectUtils, BoardMarkersUtils, GameState, GeneralData, Colors, TextDisplayer
from Utils import ShipOrientation, Tour


class GameLogic:

    def __init__(self):
        self.gameState = GameState.menu
        menuButtonShift = GameData.boardTopMargin

        self.startButton = pygame.Rect(GeneralData.width / 2. - GameData.menuButtonSize[0] / 2., menuButtonShift,
                                       GameData.menuButtonSize[0], GameData.menuButtonSize[1])
        menuButtonShift += GameData.shipButtonSize[1] + 2 * GameData.mapMarginY
        self.quitButton = pygame.Rect(GeneralData.width / 2. - GameData.menuButtonSize[0] / 2., menuButtonShift,
                                      GameData.menuButtonSize[0], GameData.menuButtonSize[1])

        menuButtonShift += GameData.menuButtonSize[1] + GameData.mapMarginY
        self.oneMastButton = pygame.Rect(GeneralData.width / 2. - GameData.shipButtonSize[0] / 2., menuButtonShift,
                                         GameData.shipButtonSize[0], GameData.shipButtonSize[1])
        menuButtonShift += GameData.shipButtonSize[1] + GameData.mapMarginY
        self.twoMastButton = pygame.Rect(GeneralData.width / 2. - GameData.shipButtonSize[0] / 2., menuButtonShift,
                                         GameData.shipButtonSize[0], GameData.shipButtonSize[1])
        menuButtonShift += GameData.shipButtonSize[1] + GameData.mapMarginY
        self.threeMastButton = pygame.Rect(GeneralData.width / 2. - GameData.shipButtonSize[0] / 2., menuButtonShift,
                                           GameData.shipButtonSize[0], GameData.shipButtonSize[1])
        menuButtonShift += GameData.shipButtonSize[1] + GameData.mapMarginY
        self.fourMastButton = pygame.Rect(GeneralData.width / 2. - GameData.shipButtonSize[0] / 2., menuButtonShift,
                                          GameData.shipButtonSize[0], GameData.shipButtonSize[1])

        self.resetButton = self.quitButton

        menuButtonShift += GameData.shipButtonSize[1] + GameData.mapMarginY

        self.winnerText = pygame.Rect(GeneralData.width / 2. - GameData.shipButtonSize[0] / 2., menuButtonShift,
                                      GameData.shipButtonSize[0], GameData.shipButtonSize[1])

        self.playerShipsGrid = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]
        self.playerButtonsGrid = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]
        self.enemyShipsGrid = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]
        self.enemyButtonsGrid = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]
        self.enemyShoots = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]
        self.currentShip = Ship.Ship(0)
        self.shipOrientation = ShipOrientation.vertical
        self.playerShips = list()
        self.enemyShips = list()
        self.tour = Tour.player
        self.winner = Tour.player

        self.fillGrid()

    def fillGrid(self):
        self.__fillListWithShips(self.playerShips)

        for row in range(0, GameData.gridSize):
            for col in range(0, GameData.gridSize):
                self.playerShipsGrid[row][col] = BoardMarkers.water
                self.playerButtonsGrid[row][col] = pygame.Rect(GameData.mapMarginX + row * 40,
                                                               GameData.mapMarginY + col * 40, 36, 36)
                self.enemyShipsGrid[row][col] = BoardMarkers.water
                self.enemyButtonsGrid[row][col] = pygame.Rect(GameData.enemyMapOrigin + row * 40,
                                                              GameData.mapMarginY + col * 40, 36, 36)

    def __fillListWithShips(self, shipsList):
        shipsList.clear()

        for i in range(GameData.fourMast):
            shipsList.append(Ship.Ship(4))
        for i in range(GameData.threeMast):
            shipsList.append(Ship.Ship(3))
        for i in range(GameData.twoMast):
            shipsList.append(Ship.Ship(2))
        for i in range(GameData.oneMast):
            shipsList.append(Ship.Ship(1))

    def drawGame(self, window):
        match self.gameState:
            case GameState.menu:
                self.__drawMenuButtons(window)
            case GameState.placeShips:
                self.__drawPlaceShips(window)
            case GameState.game:
                self.__drawBoards(window)

    def gameLogic(self):
        if self.tour == Tour.enemy:
            field = self.__getDamagedShip()

            if field is not None:
                self.__guessNextField(field)
            else:
                self.__shootRandomField()

            field = self.__getDamagedShip()

            if field is not None:
                ship = self.__getShipWithGivenCoordinates(field)
                if ship.isShipSank(self.playerShipsGrid):
                    for field in ship.gridFields:
                        self.playerShipsGrid[field[0]][field[1]] = BoardMarkers.wreck
                        self.enemyShoots[field[0]][field[1]] = BoardMarkers.wreck
                        fieldsAround = self.__getFieldAround(field)
                        for fa in fieldsAround:
                            if fa not in ship.gridFields and self.__isFieldInGrid(fa):
                                self.enemyShoots[fa[0]][fa[1]] = BoardMarkers.shipNeighborhood

            if not self.__andShipsLeft(self.playerShipsGrid):
                self.tour = Tour.gameEnd
                self.winner = Tour.enemy
            else:
                self.tour = Tour.player

    def __getDamagedShip(self):
        for row in range(0, GameData.gridSize):
            for col in range(0, GameData.gridSize):
                if self.playerShipsGrid[row][col] == BoardMarkers.shipDamaged:
                    return row, col
        return None

    def __andShipsLeft(self, grid):
        for row in range(0, GameData.gridSize):
            for col in range(0, GameData.gridSize):
                if grid[row][col] == BoardMarkers.shipDamaged or grid[row][col] == BoardMarkers.ship:
                    return True
        return False

    def __getShipWithGivenCoordinates(self, field):
        for ship in self.playerShips:
            if field in ship.gridFields:
                return ship
        return None

    def __drawBoards(self, window):
        self.__drawButton(window, "reset", self.resetButton)

        for row in range(0, GameData.gridSize):
            for col in range(0, GameData.gridSize):
                c = BoardMarkersUtils.getColorBaseOnBoardMarker(self.playerShipsGrid[row][col])
                pygame.draw.rect(window, c, self.playerButtonsGrid[row][col])

                c = BoardMarkersUtils.getColorBaseOnBoardMarker(self.enemyShipsGrid[row][col])
                pygame.draw.rect(window, c, self.enemyButtonsGrid[row][col])

        if self.tour == Tour.gameEnd:
            winner = "Wygrana!" if self.winner == Tour.player else "Przegrana!"
            TextDisplayer.text_to_screen(window, winner, self.winnerText[0], self.winnerText[1], size=30)

    def __drawMenuButtons(self, window):
        self.__drawButton(window, "start", self.startButton)
        self.__drawButton(window, "wyjdz", self.quitButton)

    def __getTextPosition(self, originRect, text, size=50):
        textSize = TextDisplayer.get_text_size(text, size=size)
        textRect = originRect[0] + originRect[2] / 2. - textSize[0] / 2., originRect[1] + originRect[3] / 2. - textSize[
            1] / 2.
        return textRect

    def __drawButton(self, window, name, rect, textSize=50, color=Colors.blue):
        pygame.draw.rect(window, color, rect)
        textRect = self.__getTextPosition(rect, name, size=textSize)
        TextDisplayer.text_to_screen(window, name, textRect[0], textRect[1], size=textSize)

    def __drawPlaceShips(self, window):
        self.__drawButton(window, "start", self.startButton,
                          color=Colors.red if self.__anyShipLeftToPlace(self.playerShips) else Colors.blue)
        self.__drawButton(window, "reset", self.resetButton)
        count = (self.__countShips(1), self.__countShips(2), self.__countShips(3), self.__countShips(4))
        self.__drawButton(window, f"one mast ({count[0]})", self.oneMastButton, textSize=35,
                          color=Colors.green if count[0] > 0 else Colors.red)
        self.__drawButton(window, f"two mast ({count[1]})", self.twoMastButton, textSize=35,
                          color=Colors.green if count[1] > 0 else Colors.red)
        self.__drawButton(window, f"three mast ({count[2]})", self.threeMastButton, textSize=35,
                          color=Colors.green if count[2] > 0 else Colors.red)
        self.__drawButton(window, f"four mast ({count[3]})", self.fourMastButton, textSize=35,
                          color=Colors.green if count[3] > 0 else Colors.red)

        mouse_pos = pygame.mouse.get_pos()
        coord = RectUtils.getPlayerBoardCoordinate(mouse_pos)
        self.currentShip.setCoords(coord, self.shipOrientation)

        for row in range(0, GameData.gridSize):
            for col in range(0, GameData.gridSize):
                c = BoardMarkersUtils.getColorBaseOnBoardMarker(self.playerShipsGrid[row][col])

                if self.playerShipsGrid[row][col] == BoardMarkers.shipNeighborhood:
                    c = Colors.gray

                if self.currentShip.numberOfMasts > 0 and (row, col) in self.currentShip.gridFields:
                    c = BoardMarkersUtils.getColorBaseOnBoardMarker(BoardMarkers.placeShip)

                pygame.draw.rect(window, c, self.playerButtonsGrid[row][col])

    def __countShips(self, mastCount):
        return sum(map(lambda x: x.numberOfMasts == mastCount and not x.isPlaced, self.playerShips))

    def __guessNextField(self, field):
        ship = self.__getShipWithGivenCoordinates(field)
        fields = list()

        for f in ship.gridFields:
            if self.enemyShoots[f[0]][f[1]] == BoardMarkers.shipDamaged:
                fields.clear()
                if ship.enemyOrientation == ShipOrientation.notKnown or ship.enemyOrientation == ShipOrientation.vertical:
                    fields.append((f[0], f[1] + 1))
                    fields.append((f[0], f[1] - 1))
                if ship.enemyOrientation == ShipOrientation.notKnown or ship.enemyOrientation == ShipOrientation.horizontal:
                    fields.append((f[0] + 1, f[1]))
                    fields.append((f[0] - 1, f[1]))
                found = False
                for fl in fields:
                    if self.__isFieldInGrid(fl) and self.enemyShoots[fl[0]][fl[1]] == BoardMarkers.water:
                        found = True
                if found:
                    break

        newField = random.choice(fields)

        while not self.__isFieldInGrid(newField) or self.enemyShoots[newField[0]][newField[1]] != BoardMarkers.water:
            newField = random.choice(fields)
            fields.remove(newField)

        if ship.enemyOrientation == ShipOrientation.notKnown and self.playerShipsGrid[newField[0]][
            newField[1]] == BoardMarkers.ship:
            ship.enemyOrientation = ShipOrientation.vertical if newField[1] != field[1] else ShipOrientation.horizontal

        self.__shotGivenField(newField)

    def __shootRandomField(self):
        field = random.choice(self.enemyShootsLeft)

        while self.enemyShoots[field[0]][field[1]] != BoardMarkers.water:
            self.enemyShootsLeft.remove(field)

            if len(self.enemyShootsLeft) > 0:
                field = random.choice(self.enemyShootsLeft)

        self.__shotGivenField(field)

    def __shotGivenField(self, field):
        self.enemyShootsLeft.remove(field)
        marker = BoardMarkers.waterHit
        if self.playerShipsGrid[field[0]][field[1]] == BoardMarkers.ship:
            marker = BoardMarkers.shipDamaged
        self.enemyShoots[field[0]][field[1]] = marker
        self.playerShipsGrid[field[0]][field[1]] = marker

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
        for row in range(0, GameData.gridSize):
            for col in range(0, GameData.gridSize):
                tempShips.append((row, col))

        for ship in self.enemyShips:
            while len(tempShips) > 0 and not ship.isPlaced:
                gridField = random.choice(tempShips)
                self.shipOrientation = ShipOrientation.vertical if random.getrandbits(
                    1) == 1 else ShipOrientation.horizontal
                ship.setCoords(gridField, self.shipOrientation)

                if not self.__placeShip(ship, self.enemyShipsGrid):
                    self.shipOrientation = ShipOrientation.vertical if self.shipOrientation == ShipOrientation.horizontal else ShipOrientation.horizontal
                    ship.setCoords(gridField, self.shipOrientation)
                    ship.isPlaced = self.__placeShip(ship, self.enemyShipsGrid)
                else:
                    ship.isPlaced = True

                tempShips.remove(gridField)

        if self.__anyShipLeftToPlace(self.enemyShips):
            if fuse < 5:
                self.__placeEnemyShips(fuse + 1)
            else:
                print("Cant place enemy ships")

    def __isFieldInGrid(self, field):
        if field[0] < 0 or field[0] > GameData.gridSize - 1 or field[1] < 0 or field[1] > GameData.gridSize - 1:
            return False
        return True

    def __anyShipLeftToPlace(self, ships):
        for ship in ships:
            if not ship.isPlaced:
                return True
        return False

    def __startGame(self):
        self.__fillListWithShips(self.enemyShips)
        self.__placeEnemyShips()
        self.tour = Tour.player if random.getrandbits(1) == 1 else Tour.enemy

        self.enemyShootsLeft = list()
        for row in range(0, GameData.gridSize):
            for col in range(0, GameData.gridSize):
                self.enemyShoots[row][col] = BoardMarkers.water
                self.enemyShootsLeft.append((row, col))

        self.gameState = GameState.game

    def prepareToPlaceShip(self, mastCount, orientation):
        self.currentShip.numberOfMasts = mastCount
        self.shipOrientation = orientation

    def handleKeyPress(self, key):
        if key == pygame.K_r:
            self.shipOrientation = ShipOrientation.vertical if self.shipOrientation == ShipOrientation.horizontal else ShipOrientation.horizontal

    def handleRightMouseDown(self):
        self.currentShip.numberOfMasts = 0

    def handleLeftMouseDown(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.gameState != GameState.menu:
            if self.resetButton.collidepoint(mouse_pos):
                self.gameState = GameState.placeShips
                self.fillGrid()

        if self.gameState == GameState.menu:
            if self.startButton.collidepoint(mouse_pos):
                self.gameState = GameState.placeShips
            if self.quitButton.collidepoint(mouse_pos):
                Run.quitGame()
        elif self.gameState == GameState.placeShips:
            if self.startButton.collidepoint(mouse_pos) and not self.__anyShipLeftToPlace(self.playerShips):
                self.__startGame()
            if self.oneMastButton.collidepoint(mouse_pos) and self.__countShips(1) > 0:
                self.currentShip.numberOfMasts = 1
            if self.twoMastButton.collidepoint(mouse_pos) and self.__countShips(2) > 0:
                self.currentShip.numberOfMasts = 2
            if self.threeMastButton.collidepoint(mouse_pos) and self.__countShips(3) > 0:
                self.currentShip.numberOfMasts = 3
            if self.fourMastButton.collidepoint(mouse_pos) and self.__countShips(4) > 0:
                self.currentShip.numberOfMasts = 4

            for row in range(0, GameData.gridSize):
                for col in range(0, GameData.gridSize):
                    button = self.playerButtonsGrid[row][col]

                    if button.collidepoint(mouse_pos):
                        if self.__placeShip(self.currentShip, self.playerShipsGrid):
                            ship = next((x for x in self.playerShips if
                                         x.numberOfMasts == self.currentShip.numberOfMasts and not x.isPlaced),
                                        None)
                            ship.isPlaced = True
                            ship.gridFields.clear()
                            for field in self.currentShip.gridFields:
                                ship.gridFields.append((field[0], field[1]))
                            self.currentShip.numberOfMasts = 0

        elif self.gameState == GameState.game:
            if self.tour == Tour.player:
                for row in range(0, GameData.gridSize):
                    for col in range(0, GameData.gridSize):
                        button = self.enemyButtonsGrid[row][col]
                        mouse_pos = pygame.mouse.get_pos()

                        if button.collidepoint(mouse_pos):
                            coord = RectUtils.getEnemyBoardCoordinate(mouse_pos)
                            marker = BoardMarkers.waterHit if self.enemyShipsGrid[coord[0]][coord[
                                1]] != BoardMarkers.ship else BoardMarkers.shipDamaged
                            self.enemyShipsGrid[coord[0]][coord[1]] = marker

                            if not self.__andShipsLeft(self.enemyShipsGrid):
                                self.tour = Tour.gameEnd
                                self.winner = Tour.player
                            else:
                                self.tour = Tour.enemy
