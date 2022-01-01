import pygame
import Ship

from Utils import GameState
from Utils import ShipOrientation, Tour

width = 1280
height = 720
name = "js-okrety"
fps = 60
gridSize = 10
menuButtonSize = (200, 75)
shipButtonSize = (300, 50)
buttonSize = 40
mapMarginX = 30
spaceY = 15
boardTopMargin = 100
enemyMapOrigin = width - mapMarginX - gridSize * buttonSize
oneMast = 4
twoMast = 3
threeMast = 2
fourMast = 1

__getNewShift = lambda enlargement, currentShift: currentShift + enlargement + 2 * spaceY
__createButton = lambda size, shift: pygame.Rect(width / 2. - size[0] / 2., shift, size[0], size[1])
__fillList = lambda size: [[0 for _ in range(size)] for _ in range(size)]

gameState = GameState.menu
menuButtonShift = boardTopMargin
startButton = __createButton(menuButtonSize, menuButtonShift)
menuButtonShift = __getNewShift(menuButtonSize[1], menuButtonShift)
quitButton = __createButton(menuButtonSize, menuButtonShift)
menuButtonShift = __getNewShift(menuButtonSize[1], menuButtonShift)
oneMastButton = __createButton(shipButtonSize, menuButtonShift)
menuButtonShift = __getNewShift(shipButtonSize[1], menuButtonShift)
twoMastButton = __createButton(shipButtonSize, menuButtonShift)
menuButtonShift = __getNewShift(shipButtonSize[1], menuButtonShift)
threeMastButton = __createButton(shipButtonSize, menuButtonShift)
menuButtonShift = __getNewShift(shipButtonSize[1], menuButtonShift)
fourMastButton = __createButton(shipButtonSize, menuButtonShift)
resetButton = quitButton
winnerText = startButton

playerShipsGrid = __fillList(gridSize)
playerButtonsGrid = __fillList(gridSize)
enemyShipsGrid = __fillList(gridSize)
enemyButtonsGrid = __fillList(gridSize)
enemyShoots = __fillList(gridSize)

currentShip = Ship.Ship(0)
shipOrientation = ShipOrientation.vertical
playerShips = list()
enemyShips = list()
tour = Tour.player
winner = Tour.player


def countUnplacedShips(mastCount):
    return sum(map(lambda x: x.numberOfMasts == mastCount and not x.isPlaced, playerShips))


def countAliveShips(mastCount, ships, grid):
    return sum(map(lambda x: x.numberOfMasts == mastCount and not x.isShipSank(grid), ships))


def anyShipLeftToPlace(ships):
    for ship in ships:
        if not ship.isPlaced:
            return True
    return False
