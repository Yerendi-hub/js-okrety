import random
import pygame
import RectUtils
import Run
import Data
from Ship import Ship
from Utils import Tour, BoardMarkers, ShipOrientation, GameState


class Logic:
    """Class responsible for logic part of the game"""

    def __init__(self):
        self.__fillGrid()
        self.__enemyShootsLeft = list()  # shots that can be done by enemy

    def handleEvent(self, event):
        """handling pygame events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left mouse button
                self.__handleLeftMouseDown()
            elif event.button == 3:  # right mouse button
                self.__handleRightMouseDown()
        if event.type == pygame.KEYDOWN:
            self.__handleKeyPress(event.key)  # event.key represents keyboard keycode

    def __startGame(self):
        """start game logic, reinitialize enemy ships and randomly select starting player"""
        self.__fillListWithShips(Data.enemyShips)
        self.__placeEnemyShips()
        Data.tour = Tour.player if random.getrandbits(1) == 1 else Tour.enemy  # draw starting player

        self.__enemyShootsLeft.clear()
        for row in range(0, Data.gridSize):
            for col in range(0, Data.gridSize):
                Data.enemyShoots[row][col] = BoardMarkers.water
                self.__enemyShootsLeft.append((row, col))  # filling enemy available shoots with all board fields

        Data.gameState = GameState.game

    def __fillGrid(self):
        """initialize grids and player ships. Can be used to restart the game"""
        self.__fillListWithShips(Data.playerShips)
        margin = Data.buttonWithMargin

        for row in range(0, Data.gridSize):
            for col in range(0, Data.gridSize):
                # we fill both lists with water so there are no ships placed
                Data.playerShipsGrid[row][col] = BoardMarkers.water
                Data.playerButtonsGrid[row][col] = pygame.Rect(Data.mapMarginX + row * Data.buttonSize,
                                                               Data.mapMarginY + col * Data.buttonSize, margin, margin)
                Data.enemyShipsGrid[row][col] = BoardMarkers.water
                Data.enemyButtonsGrid[row][col] = pygame.Rect(Data.enemyMapOrigin + row * Data.buttonSize,
                                                              Data.mapMarginY + col * Data.buttonSize, margin, margin)

    def AI(self):
        """enemy player AI, invoked only on enemy turn"""

        if Data.tour == Tour.enemy:
            # we need to know if there are damaged but not destroyed ships
            field = self.__getDamagedShip()

            if field is not None:
                # if there are damaged ships we try to find next ship fields
                self.__guessNextField(field)
            else:
                # else we fire random
                self.__shootRandomField()

            # we check if ship there are damaged ships after shoot, so we can set wreck coordinates
            field = self.__getDamagedShip()

            if field is not None:
                ship = self.__getShipWithGivenCoordinates(field, Data.playerShips)
                if ship.isShipSank(Data.playerShipsGrid):
                    # if it is sunk we mark it as wreck
                    for field in ship.gridFields:
                        Data.playerShipsGrid[field[0]][field[1]] = BoardMarkers.wreck
                        Data.enemyShoots[field[0]][field[1]] = BoardMarkers.wreck
                        fieldsAround = self.__getFieldAround(field)
                        for fa in fieldsAround:
                            # we mark all surrounding fields as neighborhood to prevent AI from shooting there
                            if fa not in ship.gridFields and self.__isFieldInGrid(fa):
                                Data.enemyShoots[fa[0]][fa[1]] = BoardMarkers.shipNeighborhood

            if not self.__anyShipsLeft(Data.playerShipsGrid):
                # if enemy destroyed last ship we mark it as winner and finish game
                self.__endGame(Tour.enemy)
            else:
                # otherwise, we switch to player' turn
                Data.tour = Tour.player

    def __endGame(self, whoWon):
        """finish game"""
        Data.winner = whoWon
        Data.tour = Tour.gameEnd

    def __fillListWithShips(self, shipsList):
        """fill given list with Ships objects according to given ships count in Data"""
        # we clear list (without creating new list())
        shipsList.clear()

        for i in range(Data.fourMast):
            shipsList.append(Ship(4))
        for i in range(Data.threeMast):
            shipsList.append(Ship(3))
        for i in range(Data.twoMast):
            shipsList.append(Ship(2))
        for i in range(Data.oneMast):
            shipsList.append(Ship(1))

    def __getDamagedShip(self):
        """returns damaged player ship (not destroyed, just damaged),
        There can be only one or non because AI always tries to finish destroying ship"""
        for row in range(0, Data.gridSize):
            for col in range(0, Data.gridSize):
                if Data.playerShipsGrid[row][col] == BoardMarkers.shipDamaged:
                    return row, col
        return None

    def __anyShipsLeft(self, grid):
        """returns true if there is any ship left in given grid"""
        for row in range(0, Data.gridSize):
            for col in range(0, Data.gridSize):
                if grid[row][col] == BoardMarkers.shipDamaged or grid[row][col] == BoardMarkers.ship:
                    return True
        return False

    def __getShipWithGivenCoordinates(self, field, ships):
        """returns Ship object from given ships list that has 'field' coordinates"""
        for ship in ships:
            if field in ship.gridFields:
                return ship
        return None

    def __guessNextField(self, field):
        """finding rest of the ship algorithm"""
        ship = self.__getShipWithGivenCoordinates(field, Data.playerShips)
        fields = list()

        # we iterate over ship fields to find damaged ones
        for f in ship.gridFields:
            if Data.enemyShoots[f[0]][f[1]] == BoardMarkers.shipDamaged:
                fields.clear()

                # if we know orientation of damaged ship (we shoot at least two of its fields) then we add only fields
                # that are matching this orientation
                if ship.enemyOrientation == ShipOrientation.notKnown or ship.enemyOrientation == ShipOrientation.vertical:
                    fields.append((f[0], f[1] + 1))
                    fields.append((f[0], f[1] - 1))
                if ship.enemyOrientation == ShipOrientation.notKnown or ship.enemyOrientation == ShipOrientation.horizontal:
                    fields.append((f[0] + 1, f[1]))
                    fields.append((f[0] - 1, f[1]))
                found = False
                # we look for any water, so we can shoot there (we can find damaged ship/other ship neighborhood/water)
                # if there is any then we know that some of these fields will be appropriate to shoot
                for fl in fields:
                    if self.__isFieldInGrid(fl) and Data.enemyShoots[fl[0]][fl[1]] == BoardMarkers.water:
                        found = True
                if found:
                    break

        # selecting random field from given
        newField = random.choice(fields)

        # if it is not on grid or if it is not water we skip it and draw another random one
        while not self.__isFieldInGrid(newField) or Data.enemyShoots[newField[0]][newField[1]] != BoardMarkers.water:
            newField = random.choice(fields)
            fields.remove(newField)

        # if we don't know orientation then we can decide if ship is vertical or horizontal when we hit ship
        # (there is part that can look like AI is using player hidden information, but we already decided that we are shooing
        # this field, so we can check if there is a ship)
        if ship.enemyOrientation == ShipOrientation.notKnown and Data.playerShipsGrid[newField[0]][
            newField[1]] == BoardMarkers.ship:
            ship.enemyOrientation = ShipOrientation.vertical if newField[1] != field[1] else ShipOrientation.horizontal

        self.__shotGivenField(newField)

    def __shootRandomField(self):
        """shoot random water field from remaining player fields"""

        # randomly choose field from remaining
        field = random.choice(self.__enemyShootsLeft)

        # if this field isn't water (it can be water/damaged ship/wreck/ship neighborhood) we remove it from remaining
        # ships list and choose next field
        while Data.enemyShoots[field[0]][field[1]] != BoardMarkers.water:
            self.__enemyShootsLeft.remove(field)

            if len(self.__enemyShootsLeft) > 0:
                field = random.choice(self.__enemyShootsLeft)

        self.__shotGivenField(field)

    def __shotGivenField(self, field):
        """mark given field as hit"""

        # remove this field from remaining fields list
        self.__enemyShootsLeft.remove(field)

        # mark is as waterHit
        marker = BoardMarkers.waterHit
        # if we hit ship then mark it as shipDamaged instead
        if Data.playerShipsGrid[field[0]][field[1]] == BoardMarkers.ship:
            marker = BoardMarkers.shipDamaged

        # fill marker information in enemy shoots and player ships
        Data.enemyShoots[field[0]][field[1]] = marker
        Data.playerShipsGrid[field[0]][field[1]] = marker

    def __placeShip(self, ship, grid):
        """place Ship object in the given grid. Returns true if ship is successfully placed"""

        if self.__canShipBePlaced(ship, grid):
            for field in ship.gridFields:
                # mark ships coordinates in grid as BoardMarker.ship
                grid[field[0]][field[1]] = BoardMarkers.ship
                fieldsAround = self.__getFieldAround(field)

                # mark fields around as BoardMarkers.shipNeighborhood
                for fa in fieldsAround:
                    if fa not in ship.gridFields and self.__isFieldInGrid(fa):
                        grid[fa[0]][fa[1]] = BoardMarkers.shipNeighborhood
            return True
        return False

    def __getFieldAround(self, field):
        """returns tuple with fields around given field. It will also return fields outside grid (like -1,-1 or over grid size)"""
        return ((field[0] - 1, field[1] + 1), (field[0], field[1] + 1), (field[0] + 1, field[1] + 1),
                (field[0] - 1, field[1]), (field[0] + 1, field[1]),
                (field[0] - 1, field[1] - 1), (field[0], field[1] - 1), (field[0] + 1, field[1] - 1))

    def __canShipBePlaced(self, ship, grid):
        """returns true if given Ship can be placed at ships coordinates on given grid"""

        # this prevents from placing ship without selecting what ship we want to place
        if ship.numberOfMasts == 0:
            return False

        for field in ship.gridFields:
            # this preventing from placing ship that has parts outside grid
            if not self.__isFieldInGrid(field):
                return False

            # this preventing from placing ship that has parts not on water (on other ship or in ships neighborhood)
            if grid[field[0]][field[1]] != BoardMarkers.water:
                return False

        return True

    def __placeEnemyShips(self):
        """implementation of randomly placed ships"""

        # we start by creating temp list with all fields from the grid
        tempShips = list()
        for row in range(0, Data.gridSize):
            for col in range(0, Data.gridSize):
                tempShips.append((row, col))

        # we iterate over enemy ships and place it randomly. Very important thing is that ships are placed from
        # four-masted ship to one-masted ship, so we can't have situation that there is no space to place remaining ships
        # there can be full board filled, but there is no possibility to have no space to place ship
        # https://gyazo.com/9695280f2a2b5d1ef92d62be0952dc4e

        for ship in Data.enemyShips:
            while len(tempShips) > 0 and not ship.isPlaced:
                # select random fields and orientation and set it to ship
                gridField = random.choice(tempShips)
                Data.shipOrientation = ShipOrientation.vertical if random.getrandbits(
                    1) == 1 else ShipOrientation.horizontal
                ship.setCoords(gridField, Data.shipOrientation)

                # try to place ship at given field, if failed change orientation
                if not self.__placeShip(ship, Data.enemyShipsGrid):
                    Data.shipOrientation = ShipOrientation.vertical if Data.shipOrientation == ShipOrientation.horizontal else ShipOrientation.horizontal
                    ship.setCoords(gridField, Data.shipOrientation)
                    ship.isPlaced = self.__placeShip(ship, Data.enemyShipsGrid)
                else:
                    ship.isPlaced = True

                # remove used gridField
                tempShips.remove(gridField)

    def __isFieldInGrid(self, field):
        """checks if field is in grid"""
        if field[0] < 0 or field[0] > Data.gridSize - 1 or field[1] < 0 or field[1] > Data.gridSize - 1:
            return False
        return True

    def __handleKeyPress(self, key):
        """handle keyboard key press"""
        if key == pygame.K_r:
            # ship rotation
            Data.shipOrientation = ShipOrientation.vertical if Data.shipOrientation == ShipOrientation.horizontal else ShipOrientation.horizontal

    def __handleRightMouseDown(self):
        """handle right mouse button down"""
        # removes ship ghost while placing ships
        Data.currentShip.numberOfMasts = 0

    def __handleLeftMouseDown(self):
        """handle left mouse button down"""

        # cache mouse position for shorter use
        mouse_pos = pygame.mouse.get_pos()

        if Data.gameState != GameState.menu:
            # reset button logic - it sets game on the beginning of ships placing
            if Data.resetButton.collidepoint(mouse_pos):
                Data.gameState = GameState.placeShips
                self.__fillGrid()

        # menu logic
        if Data.gameState == GameState.menu:
            if Data.startButton.collidepoint(mouse_pos):
                # if start game then go to ship placing
                Data.gameState = GameState.placeShips
            if Data.quitButton.collidepoint(mouse_pos):
                # if quit then quit application
                Run.quitGame()
        # placing ships logic
        elif Data.gameState == GameState.placeShips:
            # if all ships are placed, and we press start then game begins
            if Data.startButton.collidepoint(mouse_pos) and not Data.anyShipLeftToPlace(Data.playerShips):
                self.__startGame()

            # selecting given ship type logic
            if Data.oneMastButton.collidepoint(mouse_pos) and Data.countUnplacedShips(1) > 0:
                Data.currentShip.numberOfMasts = 1
            if Data.twoMastButton.collidepoint(mouse_pos) and Data.countUnplacedShips(2) > 0:
                Data.currentShip.numberOfMasts = 2
            if Data.threeMastButton.collidepoint(mouse_pos) and Data.countUnplacedShips(3) > 0:
                Data.currentShip.numberOfMasts = 3
            if Data.fourMastButton.collidepoint(mouse_pos) and Data.countUnplacedShips(4) > 0:
                Data.currentShip.numberOfMasts = 4

            # checking if we press any button on grid
            for row in range(0, Data.gridSize):
                for col in range(0, Data.gridSize):
                    button = Data.playerButtonsGrid[row][col]

                    if button.collidepoint(mouse_pos):
                        # if we press grid field, and we can place ship there then place ship
                        if self.__placeShip(Data.currentShip, Data.playerShipsGrid):
                            # select ship with given masts count that is not already placed
                            ship = next((x for x in Data.playerShips if
                                         x.numberOfMasts == Data.currentShip.numberOfMasts and not x.isPlaced),
                                        None)

                            # make ship placed and fill its data
                            ship.isPlaced = True
                            ship.gridFields.clear()
                            for field in Data.currentShip.gridFields:
                                ship.gridFields.append((field[0], field[1]))

                            # reset ghost
                            Data.currentShip.numberOfMasts = 0
        # main game logic
        elif Data.gameState == GameState.game:
            # if its players turn then we check if he pressed enemy grid
            if Data.tour == Tour.player:
                for row in range(0, Data.gridSize):
                    for col in range(0, Data.gridSize):
                        button = Data.enemyButtonsGrid[row][col]

                        if button.collidepoint(mouse_pos):
                            # if player pressed grid button we get coordinates and current marker
                            coord = RectUtils.getEnemyBoardCoordinate(mouse_pos)
                            cm = Data.enemyShipsGrid[coord[0]][coord[1]]

                            # if player shoot intact field and hit water/ship we set according marker
                            if cm != BoardMarkers.waterHit and cm != BoardMarkers.shipDamaged and cm != BoardMarkers.wreck:
                                marker = BoardMarkers.waterHit if Data.enemyShipsGrid[coord[0]][coord[
                                    1]] != BoardMarkers.ship else BoardMarkers.shipDamaged
                                Data.enemyShipsGrid[coord[0]][coord[1]] = marker

                                # if player damage ship we check if he did not destroy it, if so we set it to wreck
                                if marker == BoardMarkers.shipDamaged:
                                    ship = self.__getShipWithGivenCoordinates(coord, Data.enemyShips)
                                    if ship.isShipSank(Data.enemyShipsGrid):
                                        for field in ship.gridFields:
                                            Data.enemyShipsGrid[field[0]][field[1]] = BoardMarkers.wreck

                                # if there is no enemies ships left we endGame with player as winner
                                if not self.__anyShipsLeft(Data.enemyShipsGrid):
                                    self.__endGame(Tour.player)
                                # otherwise, its AI turn
                                else:
                                    Data.tour = Tour.enemy
