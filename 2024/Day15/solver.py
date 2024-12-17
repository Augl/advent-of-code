from enum import Enum

class Tile(Enum):
    FREE = "."
    CHEST_FULL = "O"
    WALL = "#"
    CHEST_RIGHT = "]"
    CHEST_LEFT = "["

    def __repr__(self) -> str:
        return self.value

class Command(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Pos:
    def __init__(self, x: int, y: int) -> None:
        """
        Creates a new position.
        """
        self.x = x
        self.y = y

    def neighbor(self, command: Command):
        """
        Returns the neighbor in the given direction.
        """
        if command == Command.UP:
            return Pos(self.x, self.y - 1)
        if command == Command.DOWN:
            return Pos(self.x, self.y + 1)
        if command == Command.LEFT:
            return Pos(self.x - 1, self.y)
        if command == Command.RIGHT:
            return Pos(self.x + 1, self.y)
        raise ValueError("Unexpected command")
    
    def __repr__(self) -> str:
        """
        Returns a human readable representation.
        """
        return f"({self.x}, {self.y})"

class Map:
    def __init__(self, strings: list[str]) -> None:
        """
        Creates a new map by parsing the strings.
        """
        self.height = len(strings)
        self.width = len(strings[0]) - 1
        data: list[list[Tile]] = []
        for y in range(len(strings)):
            row: list[Tile] = []
            for x in range(len(strings[y])):
                c = strings[y][x]
                if c == ".":
                    row.append(Tile.FREE)
                if c == "#":
                    row.append(Tile.WALL)
                if c == "O":
                    row.append(Tile.CHEST_FULL)
                if c == "@":
                    self.robot = Pos(x, y)   
                    row.append(Tile.FREE)
            data.append(row)
        self._data = data

    def convertToWideVersion(self):
        """
        Converts the map into the wide version of task 2.
        """
        data: list[list[Tile]] = []
        for y in range(self.height):
            row: list[Tile] = []
            for x in range(self.width):
                t = self._data[y][x]
                if t == Tile.WALL:
                    row.extend([Tile.WALL, Tile.WALL])
                if t == Tile.CHEST_FULL:
                    row.extend([Tile.CHEST_LEFT, Tile.CHEST_RIGHT])
                if t == Tile.FREE:
                    row.extend([Tile.FREE, Tile.FREE])
            data.append(row)
        self._data = data
        self.width *= 2
        self.robot.x *= 2

    def getTile(self, pos: Pos):
        """
        Returns the tile at the given position.
        """
        return self._data[pos.y][pos.x]
    
    def setTile(self, pos: Pos, tile: Tile):
        """
        Sets the given tile to the given position.
        """
        self._data[pos.y][pos.x] = tile

    def _getPositionOfOtherHalfChest(self, pos: Pos):
        """
        Returns the position of the other half of the chest at the given position.
        """
        tile = self.getTile(pos)
        if tile == Tile.CHEST_RIGHT:
            return pos.neighbor(Command.LEFT)
        if tile == Tile.CHEST_LEFT:
            return pos.neighbor(Command.RIGHT)
        raise ValueError(f"Half chest expected at given position, found {tile}.")
    
    def _checkMoveTo(self, pos: Pos, direction: Command):
        """
        Checks if the given move can be performed, i.e. if there is an empty tile in the desired direction.
        """
        n = pos.neighbor(direction)
        tile = self.getTile(pos)
        if tile == Tile.CHEST_FULL:
            return self._checkMoveTo(n, direction)
        if tile == Tile.CHEST_LEFT or tile == Tile.CHEST_RIGHT:
            if direction == Command.LEFT or direction == Command.RIGHT:
                return self._checkMoveTo(n, direction)
            if direction == Command.UP or direction == Command.DOWN:
                otherHalfN = self._getPositionOfOtherHalfChest(pos).neighbor(direction)
                return self._checkMoveTo(n, direction) and self._checkMoveTo(otherHalfN, direction)
        return tile == Tile.FREE

    def _performMoveTo(self, pos: Pos, direction: Command):
        """
        Tries to perform the given move. Returns True if the move was completed successfully.
        """
        n = pos.neighbor(direction)
        tile = self.getTile(pos)
        if tile == Tile.CHEST_FULL:
            self._performMoveTo(n, direction)
            self.setTile(pos, Tile.FREE)
            self.setTile(n, tile)
        if tile == Tile.CHEST_LEFT or tile == Tile.CHEST_RIGHT:
            if direction == Command.LEFT or direction == Command.RIGHT:
                self._performMoveTo(n, direction)
                self.setTile(pos, Tile.FREE)
                self.setTile(n, tile)
            if direction == Command.UP or direction == Command.DOWN:
                otherHalf = self._getPositionOfOtherHalfChest(pos)
                otherTile = Tile.CHEST_LEFT
                if tile == Tile.CHEST_LEFT:
                    otherTile = Tile.CHEST_RIGHT
                self._performMoveTo(n, direction)
                self.setTile(pos, Tile.FREE)
                self.setTile(n, tile)
                self._performMoveTo(otherHalf.neighbor(direction), direction)
                self.setTile(otherHalf, Tile.FREE)
                self.setTile(otherHalf.neighbor(direction), otherTile)

    def tryMove(self, command: Command):
        """
        Moves the robot in the given direction, if possible.
        """
        next = self.robot.neighbor(command)
        if self._checkMoveTo(next, command):
            self._performMoveTo(next, command)
            self.robot = next

    def getChestGpsSum(self):
        """
        Returns the sum of all chest GPSs.
        """
        sum = 0
        for y in range(self.height):
            for x in range(self.width):
                if self._data[y][x] == Tile.CHEST_FULL or self._data[y][x] == Tile.CHEST_LEFT:
                    sum += 100 * y + x
        return sum

def readInput(filename: str):
    """
    Parses the input file.
    """
    data = open("2024/Day15/" + filename + ".txt", "r")
    lines = data.readlines()
    mapStrings = []
    commandStrings = []
    for i in range(len(lines)):
        if lines[i] == "\n":
            mapStrings = lines[:i]
            commandStrings = lines[i:]
    map = Map(mapStrings)
    wideMap = Map(mapStrings)
    wideMap.convertToWideVersion()
    commands: list[Command] = []
    for r in commandStrings:
        for c in r:
            if c == "^":
                commands.append(Command.UP)
            if c == "v":
                commands.append(Command.DOWN)
            if c == "<":
                commands.append(Command.LEFT)
            if c == ">":
                commands.append(Command.RIGHT)
    return (map, wideMap, commands)

def solveTask(m: Map, commands: list[Command]):
    """
    Solves the task by simulating the robot and fetching all chest positions.
    """
    for c in commands:
        m.tryMove(c)
    print(m.getChestGpsSum())

m, wideMap, commands = readInput("input")
solveTask(m, commands)
solveTask(wideMap, commands)
