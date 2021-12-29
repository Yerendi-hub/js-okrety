import pygame
import Run

from Utils import GameData, BoardMarkers, RectUtils, BoardMarkersUtils, GameState, GeneralData, Colors, TextDisplayer


class GameLogic:

    def __init__(self):
        self.gameState = GameState.menu

        self.startButton = pygame.Rect(GeneralData.width / 2. - GameData.menuButtonSize[0] / 2.,
                                       GameData.mapMarginY, GameData.menuButtonSize[0], GameData.menuButtonSize[1])
        menuButtonShift = GameData.menuButtonSize[1] + 2 * GameData.mapMarginY
        self.quitButton = pygame.Rect(GeneralData.width / 2. - GameData.menuButtonSize[0] / 2., menuButtonShift,
                                      GameData.menuButtonSize[0], GameData.menuButtonSize[1])
        self.resetButton = self.startButton
        self.playerShipsGrid = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]
        self.playerButtonsGrid = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]
        self.enemyShipsGrid = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]
        self.enemyButtonsGrid = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]

        self.fillGrid()


    def fillGrid(self):
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
        self.__drawResetButton(window)

        for row in range(0, GameData.gridSize):
            for col in range(0, GameData.gridSize):
                c = BoardMarkersUtils.getColorBaseOnBoardMarker(self.playerShipsGrid[row][col])
                pygame.draw.rect(window, c, self.playerButtonsGrid[row][col])

                c = BoardMarkersUtils.getColorBaseOnBoardMarker(self.enemyShipsGrid[row][col])
                pygame.draw.rect(window, c, self.enemyButtonsGrid[row][col])

    def __drawMenuButtons(self, window):
        pygame.draw.rect(window, Colors.blue, self.startButton)
        textRect = self.__getTextPosition(self.startButton, "start")
        TextDisplayer.text_to_screen(window, "start", textRect[0], textRect[1])
        pygame.draw.rect(window, Colors.blue, self.quitButton)
        textRect2 = self.__getTextPosition(self.quitButton, "wyjdz")
        TextDisplayer.text_to_screen(window, "wyjdz", textRect2[0], textRect2[1])

    def __getTextPosition(self, originRect, text):
        textSize = TextDisplayer.get_text_size(text)
        textRect = originRect[0] + originRect[2] / 2. - textSize[0] / 2., originRect[1] + originRect[3] / 2. - textSize[1] / 2.
        return textRect

    def __drawResetButton(self, window):
        pygame.draw.rect(window, Colors.blue, self.resetButton)
        textRect = self.__getTextPosition(self.resetButton, "reset")
        TextDisplayer.text_to_screen(window, "reset", textRect[0], textRect[1])

    def __drawPlaceShips(self, window):
        self.__drawResetButton(window)

        for row in range(0, GameData.gridSize):
            for col in range(0, GameData.gridSize):
                c = BoardMarkersUtils.getColorBaseOnBoardMarker(self.playerShipsGrid[row][col])
                pygame.draw.rect(window, c, self.playerButtonsGrid[row][col])

    def handleMouseDown(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.gameState != GameState.menu:
            if self.resetButton.collidepoint(mouse_pos):
                self.gameState = GameState.game
                self.fillGrid()

        if self.gameState == GameState.menu:
            if self.startButton.collidepoint(mouse_pos):
                self.gameState = GameState.game
            if self.quitButton.collidepoint(mouse_pos):
                Run.quitGame()
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
