from enum import Enum

class Tile(Enum):
    OBSTACLE = 0
    FREE = 1
    OUT = -1

class Direction:
    def __init__(self, dX: int, dY: int) -> None:
        """
        Creates a new Direction with an x and y component.
        """
        self.dX = dX
        self.dY = dY

    def rotate(self):
        """
        Rotates the direction by 90 degrees clockwise.
        """
        self.dX, self.dY = -self.dY, self.dX

class Pos:
    def __init__(self, x: int, y: int) -> None:
        """
        Creates a new Position with an x and y component.
        """
        self.x = x
        self.y = y

    def next(self, dir: Direction):
        """
        Returns a new position representing one step from the current position in the given direction.
        """
        return Pos(self.x + dir.dX, self.y + dir.dY)
    
    def __hash__(self) -> int:
        """
        Returns a hash by constructing a tuple and using it's hash method.
        """
        return (self.x, self.y).__hash__()
    
    def __eq__(self, value: object) -> bool:
        """
        Checks equality.
        """
        if not isinstance(value, self.__class__):
            return False
        return self.x == value.x and self.y == value.y

class Map:
    def __init__(self, lines: list[str]):
        """
        Creates a new Map by parsing the given lines of strings.
        """
        map = []
        for i in range(len(lines)):
            row = []
            for j in range(len(lines[i])):
                if lines[i][j] == "^":
                    self.pos = Pos(j, i)
                if lines[i][j] == "#":
                    row.append(Tile.OBSTACLE)
                else:
                    row.append(Tile.FREE)
            map.append(row)
        self._data = map

    def get(self, x, y) -> Tile:
        """
        Returns the tile at the given position.
        """
        if y < 0 or y >= len(self._data):
            return Tile.OUT
        if x < 0 or x >= len(self._data[y]):
            return Tile.OUT
        return self._data[y][x]
    
    def set(self, x, y, tile):
        """
        Sets the tile at the given position.
        """
        self._data[y][x] = tile

def readInput(filename: str) -> Map:
    """
    Parses the input file.
    """
    data = open("2024/Day06/" + filename + ".txt", "r")
    lines = data.readlines()
    map = Map(lines)
    if map.pos == None:
        raise ValueError("Start position not found.")
    return map

def getUniqueKey(pos: Pos, dir: Direction) -> str:
    """
    Creates a key for the given position and direction combination.
    """
    return str(pos.x) + "," + str(pos.y) + "," + str(dir.dX) + "," + str(dir.dY)

def findPath(map: Map) -> set[Pos] | None:
    """
    Finds a path in the given map. Returns a set of all points on the path or None, if there is no path out of the map.
    """
    direction = Direction(0, -1)
    visited = set()
    path = set()
    start = map.pos
    path.add(start)
    visited.add(getUniqueKey(start, direction))
    while True:
        next = start.next(direction)
        if getUniqueKey(next, direction) in visited:
            return None
        tile = map.get(next.x, next.y)
        if tile == Tile.OBSTACLE:
            direction.rotate()
        elif tile == Tile.FREE:
            path.add(next)
            visited.add(getUniqueKey(next, direction))
            start = next
        else:
            break
    return path

def solveTask1(map: Map):
    """
    Solves the first task by finding the path out of the map.
    """
    path = findPath(map)
    if path != None:
        print(len(path))
    else:
        print("Path includes loop")

def solveTask2(map: Map):
    """
    Solves the second task by placing objects along the path from the first task and checking
    if the resulting map contains a looping path.
    """
    path = findPath(map)
    if path == None:
        print("Loop found in initial path")
        return
    result = 0
    for pos in path:
        map.set(pos.x, pos.y, Tile.OBSTACLE)
        path = findPath(map)
        if path == None:
            result += 1
        map.set(pos.x, pos.y, Tile.FREE)
    print(result)

map = readInput("input")
solveTask2(map)