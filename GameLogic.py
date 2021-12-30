import pygame
import Run
import Ship

from Utils import GameData, BoardMarkers, RectUtils, BoardMarkersUtils, GameState, GeneralData, Colors, TextDisplayer
from Utils import ShipOrientation


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
        self.playerShipsGrid = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]
        self.playerButtonsGrid = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]
        self.enemyShipsGrid = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]
        self.enemyButtonsGrid = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]
        self.currentShip = Ship.Ship(0, (0, 0))
        self.shipOrientation = ShipOrientation.vertical
        self.ships = list()

        self.fillGrid()

    def fillGrid(self):
        self.ships = list()

        for i in range(GameData.oneMast):
            self.ships.append(Ship.Ship(1, (0, 0)))
        for i in range(GameData.twoMast):
            self.ships.append(Ship.Ship(2, (0, 0)))
        for i in range(GameData.threeMast):
            self.ships.append(Ship.Ship(3, (0, 0)))
        for i in range(GameData.fourMast):
            self.ships.append(Ship.Ship(4, (0, 0)))

        for row in range(0, GameData.gridSize):
            for col in range(0, GameData.gridSize):
                self.playerShipsGrid[row][col] = BoardMarkers.water
                self.playerButtonsGrid[row][col] = pygame.Rect(GameData.mapMarginX + row * 40,
                                                               GameData.mapMarginY + col * 40, 36, 36)
                self.enemyShipsGrid[row][col] = BoardMarkers.water
                self.enemyButtonsGrid[row][col] = pygame.Rect(GameData.enemyMapOrigin + row * 40,
                                                              GameData.mapMarginY + col * 40, 36, 36)

    def drawGame(self, window):
        match self.gameState:
            case GameState.menu:
                self.__drawMenuButtons(window)
            case GameState.placeShips:
                self.__drawPlaceShips(window)
            case GameState.game:
                self.__drawBoards(window)

    def __drawBoards(self, window):
        self.__drawButton(window, "reset", self.resetButton)

        for row in range(0, GameData.gridSize):
            for col in range(0, GameData.gridSize):
                c = BoardMarkersUtils.getColorBaseOnBoardMarker(self.playerShipsGrid[row][col])
                pygame.draw.rect(window, c, self.playerButtonsGrid[row][col])

                c = BoardMarkersUtils.getColorBaseOnBoardMarker(self.enemyShipsGrid[row][col])
                pygame.draw.rect(window, c, self.enemyButtonsGrid[row][col])

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
        self.__drawButton(window, "start", self.startButton, color= Colors.blue if self.__anyShipLeftToPlace() else Colors.red)
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
        return sum(map(lambda x: x.numberOfMasts == mastCount and not x.isPlaced, self.ships))

    def __placeShip(self):
        if self.__canShipBePlaced(self.currentShip):
            for field in self.currentShip.gridFields:
                self.playerShipsGrid[field[0]][field[1]] = BoardMarkers.ship
                fieldsAround = self.__getFieldAround(field)

                for fa in fieldsAround:
                    if fa not in self.currentShip.gridFields and self.__isFieldInGrid(fa):
                        self.playerShipsGrid[fa[0]][fa[1]] = BoardMarkers.shipNeighborhood

            ship = next((x for x in self.ships if x.numberOfMasts == self.currentShip.numberOfMasts and not x.isPlaced),
                        None)
            ship.isPlaced = True

            self.currentShip.numberOfMasts = 0

    def __getFieldAround(self, field):
        return ((field[0] - 1, field[1] + 1), (field[0], field[1] + 1), (field[0] + 1, field[1] + 1),
                (field[0] - 1, field[1]), (field[0] + 1, field[1]),
                (field[0] - 1, field[1] - 1), (field[0], field[1] - 1), (field[0] + 1, field[1] - 1))

    def __canShipBePlaced(self, ship):
        if ship.numberOfMasts == 0:
            return False

        for field in ship.gridFields:
            if not self.__isFieldInGrid(field):
                return False

            if self.playerShipsGrid[field[0]][field[1]] != BoardMarkers.water:
                return False

        return True

    def __isFieldInGrid(self, field):
        if field[0] < 0 or field[0] > GameData.gridSize - 1 or field[1] < 0 or field[1] > GameData.gridSize - 1:
            return False
        return True

    def __anyShipLeftToPlace(self):
        return next((x for x in self.ships if not x.isPlaced), None) is None

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
            if self.startButton.collidepoint(mouse_pos) and self.__anyShipLeftToPlace():
                self.gameState = GameState.game
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
                        self.__placeShip()

        elif self.gameState == GameState.game:
            for row in range(0, GameData.gridSize):
                for col in range(0, GameData.gridSize):
                    button = self.playerButtonsGrid[row][col]

                    if button.collidepoint(mouse_pos):
                        coord = RectUtils.getPlayerBoardCoordinate(mouse_pos)
                        print('ship hit at {0}'.format(coord))
                        self.playerShipsGrid[coord[0]][coord[1]] = BoardMarkers.waterHit

                    button = self.enemyButtonsGrid[row][col]
                    mouse_pos = pygame.mouse.get_pos()

                    if button.collidepoint(mouse_pos):
                        coord = RectUtils.getEnemyBoardCoordinate(mouse_pos)
                        print('ship hit at {0}'.format(coord))
                        self.enemyShipsGrid[coord[0]][coord[1]] = BoardMarkers.waterHit
