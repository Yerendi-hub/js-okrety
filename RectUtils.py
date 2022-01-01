import Data


def getPlayerBoardCoordinate(mousePos):
    return int((mousePos[0] - Data.mapMarginX) / Data.buttonSize), int(
        (mousePos[1] - Data.spaceY) / Data.buttonSize)


def getEnemyBoardCoordinate(mousePos):
    return int((mousePos[0] - Data.enemyMapOrigin) / Data.buttonSize), int(
        (mousePos[1] - Data.spaceY) / Data.buttonSize)