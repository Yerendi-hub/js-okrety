from Utils import GameData, BoardMarkers
import pygame_widgets
from pygame_widgets.button import Button


class GameLogic:

    def __init__(self, window):
        self.shipsGrid = [[0 for x in range(GameData.gridSize)] for y in range(GameData.gridSize)]
        self.buttonsGrid = [[0 for x in range(GameData.gridSize)] for y in range(GameData.gridSize)]

        for row in range(0, GameData.gridSize-1):
            for col in range(0, GameData.gridSize-1):
                self.shipsGrid[row][col] = BoardMarkers.water

                button = Button(
                    window, row * 40, col * 40, 36, 36, text='Hello',
                    fontSize=50, margin=20,
                    inactiveColour=(255, 0, 0),
                    pressedColour=(0, 255, 0),
                    onClick=lambda: print('Click')
                )