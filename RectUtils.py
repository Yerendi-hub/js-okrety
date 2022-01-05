"""module for utils related with positions on grid"""
import Data


def getPlayerBoardCoordinate(mousePos):
    """returns player grid cell on given mouse position"""
    return int((mousePos[0] - Data.mapMarginX) / Data.buttonSize), int(
        (mousePos[1] - Data.mapMarginY) / Data.buttonSize)


def getEnemyBoardCoordinate(mousePos):
    """returns enemy grid cell on given mouse position"""
    return int((mousePos[0] - Data.enemyMapOrigin) / Data.buttonSize), int(
        (mousePos[1] - Data.mapMarginY) / Data.buttonSize)
