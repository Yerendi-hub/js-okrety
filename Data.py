"""Module responsible for handling shared game data"""

import pygame
import Ship

from Utils import GameState
from Utils import ShipOrientation, Tour

width = 1280  # window width
height = 720  # window height
name = "js-okrety"  # window title
fps = 60  # game frame rate
gridSize = 10  # grid (board) size
menuButtonSize = (200, 75)  # function buttons rect
shipButtonSize = (300, 50)  # placing ships buttons rect
buttonSize = 40  # amount of space used by the ship button
buttonWithMargin = 36  # true ship button size
mapMarginX = 30  # distance from board to window side edge
mapMarginY = 15  # distance from board to window top edge
boardTopMargin = 100  # distance from buttons to window top edge
enemyMapOrigin = width - mapMarginX - gridSize * buttonSize  # distance from left window border enemy map
oneMast = 4  # count of one mast ships
twoMast = 3  # count of two mast ships
threeMast = 2  # count of three mast ships
fourMast = 1  # count of four mast ships
gameState = GameState.menu  # variable that determines current game state (scene)

# function to calculate buttons shift
__getNewShift = lambda enlargement, currentShift: currentShift + enlargement + 2 * mapMarginY
# function to create menu and ships placing buttons
__createButton = lambda size, shift: pygame.Rect(width / 2. - size[0] / 2., shift, size[0], size[1])
# function to fill grid lists
__fillList = lambda size: [[0 for _ in range(size)] for _ in range(size)]

# creating buttons
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

# grid lists
# buttons are arrays of rects (filled in at game start)
# ships grids and enemyShoots are arrays of BoardMarkers (willed with water at start and then updated)
playerShipsGrid = __fillList(gridSize)  # player ships grid
playerButtonsGrid = __fillList(gridSize)  # player buttons grid
enemyShipsGrid = __fillList(gridSize)  # enemy ships grid
enemyButtonsGrid = __fillList(gridSize)  # enemy buttons grid
enemyShoots = __fillList(gridSize)  # enemy shoots grid

currentShip = Ship.Ship(0)  # fake ship that is used while placing to display "ghost" of the ship
shipOrientation = ShipOrientation.vertical  # used while placing to display "ghost" of the ship to determine orientation
playerShips = list()  # list of ships placed by player (containing Ship objects)
enemyShips = list()  # list of ships placed by enemy (containing Ship objects)
tour = Tour.player  # used during game to determine who plays - player or computer or if the game is over
winner = Tour.player  # when tour is set to gameEnd it shows who won game. Reuses Tour enum but can be only player/enemy


def countUnplacedShips(mastCount):
    return sum(map(lambda x: x.numberOfMasts == mastCount and not x.isPlaced, playerShips))


def countAliveShips(mastCount, ships, grid):
    return sum(map(lambda x: x.numberOfMasts == mastCount and not x.isShipSank(grid), ships))


def anyShipLeftToPlace(ships):
    for ship in ships:
        if not ship.isPlaced:
            return True
    return False
