from enum import Enum
import pygame


class Colors:
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (50, 205, 50)
    lightBlue = (0, 191, 255)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    orange = (255, 165, 0)
    darkOrange = (255, 99, 71)
    lightGreen = (107, 142, 35)
    gray = (192, 192, 192)


class ShipOrientation(Enum):
    horizontal = 1
    vertical = 2
    notKnown = 3


class Tour(Enum):
    player = 1
    enemy = 2
    gameEnd = 3


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


class TextUtility:

    @staticmethod
    def getTextSize(text, size=50):
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        text = font.render(text, False, Colors.red)
        return text.get_width(), text.get_height()

    @staticmethod
    def getTextPosition(originRect, text, size=50):
        textSize = TextUtility.getTextSize(text, size=size)
        textRect = originRect[0] + originRect[2] / 2. - textSize[0] / 2., originRect[1] + originRect[3] / 2. - textSize[
            1] / 2.
        return textRect


class Drawer:

    @staticmethod
    def textToScreen(window, text, x, y, size=50, color=Colors.black):
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        text = font.render(text, False, color)
        window.blit(text, (x, y))

    @staticmethod
    def drawButton(window, name, rect, textSize=50, color=Colors.blue):
        pygame.draw.rect(window, color, rect)
        textRect = TextUtility.getTextPosition(rect, name, size=textSize)
        Drawer.textToScreen(window, name, textRect[0], textRect[1], size=textSize)
