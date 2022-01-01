import pygame

import RectUtils
import Data
from Utils import GameState, Colors, TextDisplayer, BoardMarkersUtils, BoardMarkers, Tour


class Drawing:
    def drawGame(self, window):
        window.fill(Colors.white)

        match Data.gameState:
            case GameState.menu:
                self.__drawMenuButtons(window)
            case GameState.placeShips:
                self.__drawPlaceShips(window)
            case GameState.game:
                self.__drawBoards(window)

    def __drawMenuButtons(self, window):
        self.__drawButton(window, "start", Data.startButton)
        self.__drawButton(window, "wyjdz", Data.quitButton)

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
        self.__drawButton(window, "start", Data.startButton,
                          color=Colors.red if Data.anyShipLeftToPlace(Data.playerShips) else Colors.blue)
        self.__drawButton(window, "reset", Data.resetButton)
        count = (Data.countUnplacedShips(1), Data.countUnplacedShips(2),
                 Data.countUnplacedShips(3), Data.countUnplacedShips(4))
        self.__drawButton(window, f"one mast ({count[0]})", Data.oneMastButton, textSize=35,
                          color=Colors.green if count[0] > 0 else Colors.red)
        self.__drawButton(window, f"two mast ({count[1]})", Data.twoMastButton, textSize=35,
                          color=Colors.green if count[1] > 0 else Colors.red)
        self.__drawButton(window, f"three mast ({count[2]})", Data.threeMastButton, textSize=35,
                          color=Colors.green if count[2] > 0 else Colors.red)
        self.__drawButton(window, f"four mast ({count[3]})", Data.fourMastButton, textSize=35,
                          color=Colors.green if count[3] > 0 else Colors.red)

        mouse_pos = pygame.mouse.get_pos()
        coord = RectUtils.getPlayerBoardCoordinate(mouse_pos)
        Data.currentShip.setCoords(coord, Data.shipOrientation)

        for row in range(0, Data.gridSize):
            for col in range(0, Data.gridSize):
                c = BoardMarkersUtils.getColorBaseOnBoardMarker(Data.playerShipsGrid[row][col])

                if Data.playerShipsGrid[row][col] == BoardMarkers.shipNeighborhood:
                    c = Colors.gray

                if Data.currentShip.numberOfMasts > 0 and (row, col) in Data.currentShip.gridFields:
                    c = BoardMarkersUtils.getColorBaseOnBoardMarker(BoardMarkers.placeShip)

                pygame.draw.rect(window, c, Data.playerButtonsGrid[row][col])

    def __drawBoards(self, window):
        self.__drawButton(window, "reset", Data.resetButton)

        for row in range(0, Data.gridSize):
            for col in range(0, Data.gridSize):
                c = BoardMarkersUtils.getColorBaseOnBoardMarker(Data.playerShipsGrid[row][col])
                pygame.draw.rect(window, c, Data.playerButtonsGrid[row][col])

                c = BoardMarkersUtils.getColorBaseOnBoardMarker(Data.enemyShipsGrid[row][col])
                if Data.enemyShipsGrid[row][col] == BoardMarkers.ship:
                    c = BoardMarkersUtils.getColorBaseOnBoardMarker(BoardMarkers.water)
                pygame.draw.rect(window, c, Data.enemyButtonsGrid[row][col])

        if Data.tour == Tour.gameEnd:
            winner = "Wygrana!" if Data.winner == Tour.player else "Przegrana!"
            TextDisplayer.text_to_screen(window, winner, Data.winnerText[0], Data.winnerText[1], size=30)
        else:
            TextDisplayer.text_to_screen(window,
                                         f"1-maszt przeciwnika: {Data.countAliveShips(1, Data.enemyShips, Data.enemyShipsGrid)}",
                                         Data.oneMastButton[0], Data.oneMastButton[1], size=30)
            TextDisplayer.text_to_screen(window,
                                         f"2-maszt przeciwnika: {Data.countAliveShips(2, Data.enemyShips, Data.enemyShipsGrid)}",
                                         Data.twoMastButton[0], Data.twoMastButton[1], size=30)
            TextDisplayer.text_to_screen(window,
                                         f"3-maszt przeciwnika: {Data.countAliveShips(3, Data.enemyShips, Data.enemyShipsGrid)}",
                                         Data.threeMastButton[0], Data.threeMastButton[1], size=30)
            TextDisplayer.text_to_screen(window,
                                         f"4-maszt przeciwnika: {Data.countAliveShips(4, Data.enemyShips, Data.enemyShipsGrid)}",
                                         Data.fourMastButton[0], Data.fourMastButton[1], size=30)
