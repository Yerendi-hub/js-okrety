import pygame

from Utils import GameData, BoardMarkers, RectUtils, BoardMarkersUtils, GameState
import pygame_widgets
from pygame_widgets.button import Button


class GameLogic:

    def __init__(self):
        self.gameState = GameState.game

        self.playerShipsGrid = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]
        self.playerButtonsGrid = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]
        self.enemyShipsGrid = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]
        self.enemyButtonsGrid = [[0 for _ in range(GameData.gridSize)] for _ in range(GameData.gridSize)]

        for row in range(0, GameData.gridSize):
            for col in range(0, GameData.gridSize):
                self.playerShipsGrid[row][col] = BoardMarkers.water
                self.playerButtonsGrid[row][col] = pygame.Rect(GameData.mapMarginX + row * 40, GameData.mapMarginY + col * 40, 36, 36)
                self.enemyShipsGrid[row][col] = BoardMarkers.water
                self.enemyButtonsGrid[row][col] = pygame.Rect(GameData.enemyMapOrigin + row * 40, GameData.mapMarginY + col * 40, 36, 36)


    def drawGame(self, window):
        match self.gameState:
            case GameState.menu:
                return self.drawMenuButtons(window)
            case GameState.placeShips:
                return self.drawPlaceShips(window)
            case GameState.game:
                return self.drawButtons(window)


    def drawButtons(self, window):
        for row in range(0, GameData.gridSize):
            for col in range(0, GameData.gridSize):
                c = BoardMarkersUtils.getColorBaseOnBoardMarker(self.playerShipsGrid[row][col])
                pygame.draw.rect(window, c, self.playerButtonsGrid[row][col])

                c = BoardMarkersUtils.getColorBaseOnBoardMarker(self.enemyShipsGrid[row][col])
                pygame.draw.rect(window, c, self.enemyButtonsGrid[row][col])

    def drawMenuButtons(self, window):
            Button(window, 0, 0, 200, 100, text='start',
            fontSize=50, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0),
            onClick=lambda: print('Click'))

    def drawPlaceShips(self, window):
        for row in range(0, GameData.gridSize):
            for col in range(0, GameData.gridSize):
                c = BoardMarkersUtils.getColorBaseOnBoardMarker(self.playerShipsGrid[row][col])
                pygame.draw.rect(window, c, self.playerButtonsGrid[row][col])

    def handleMouseDown(self):
        if self.gameState == GameState.game:
            for row in range(0, GameData.gridSize):
                for col in range(0, GameData.gridSize):
                    button = self.playerButtonsGrid[row][col]
                    mouse_pos = pygame.mouse.get_pos()

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
