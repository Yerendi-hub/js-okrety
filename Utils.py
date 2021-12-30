from enum import Enum
import pygame


class Colors:
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    lightBlue = (0, 191, 255)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    orange = (255, 165, 0)
    darkOrange = (255, 99, 71)
    lightGreen = (0, 255, 127)
    gray = (119,136,153)


class GeneralData:
    width = 1280
    height = 720
    name = "js-okrety"
    fps = 60


class GameData:
    gridSize = 10
    menuButtonSize = (200, 75)
    shipButtonSize = (300, 50)
    buttonSize = 40
    mapMarginX = 30
    mapMarginY = 30
    boardTopMargin = 100
    enemyMapOrigin = GeneralData.width - mapMarginX - gridSize * buttonSize
    oneMast = 4
    twoMast = 3
    threeMast = 2
    fourMast = 1


class ShipOrientation(Enum):
    horizontal = 1
    vertical = 2


class BoardMarkers(Enum):
    ship = 1
    shipDamaged = 2
    wreck = 3
    shipNeighborhood = 4
    water = 5
    waterHit = 6
    error = 7
    placeShip = 8


class GameState(Enum):
    menu = 1
    placeShips = 2
    game = 3


class BoardMarkersUtils:
    @staticmethod
    def getColorBaseOnBoardMarker(marker):
        match marker:
            case BoardMarkers.ship:
                return Colors.green
            case BoardMarkers.shipDamaged:
                return Colors.orange
            case BoardMarkers.wreck:
                return Colors.darkOrange
            case BoardMarkers.shipNeighborhood:
                return Colors.lightBlue
            case BoardMarkers.water:
                return Colors.lightBlue
            case BoardMarkers.waterHit:
                return Colors.blue
            case BoardMarkers.error:
                return Colors.red
            case BoardMarkers.placeShip:
                return Colors.lightGreen
            case _:
                return Colors.black


class RectUtils:
    @staticmethod
    def getPlayerBoardCoordinate(mousePos):
        return int((mousePos[0] - GameData.mapMarginX) / GameData.buttonSize), int(
            (mousePos[1] - GameData.mapMarginY) / GameData.buttonSize)

    @staticmethod
    def getEnemyBoardCoordinate(mousePos):
        return int((mousePos[0] - GameData.enemyMapOrigin) / GameData.buttonSize), int(
            (mousePos[1] - GameData.mapMarginY) / GameData.buttonSize)


class TextDisplayer:
    @staticmethod
    def text_to_screen(window, text, x, y, size=50, color=Colors.black):
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        text = font.render(text, False, color)
        window.blit(text, (x, y))

    @staticmethod
    def get_text_size(text, size=50):
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        text = font.render(text, False, Colors.red)
        return text.get_width(), text.get_height()

