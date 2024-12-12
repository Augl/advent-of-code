class Pos:
    def __init__(self, x, y):
        """
        Creates a new position with the given coordinates.
        """
        self.x = x
        self.y = y
    
    def __eq__(self, value):
        """
        Checks if two positions are equal.
        """
        if not isinstance(value, Pos):
            return False
        return self.x == value.x and self.y == value.y
    
    def __hash__(self):
        """
        Calculates a hash of the instance.
        """
        return (self.x, self.y).__hash__()

class Map:
    def __init__(self, lines: list[str]) -> None:
        """
        Parses the input text into an object.
        """
        self.height = len(lines)
        self.width = len(lines[0]) - 1
        self._data = lines
        self.heads: list[Pos] = []
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if (lines[y][x] == "0"):
                    self.heads.append(Pos(x, y))

    def get(self, pos: Pos) -> int:
        if pos.x < 0 or pos.x >= self.width:
            return -1
        if pos.y < 0 or pos.y >= self.height:
            return -1
        return int(self._data[pos.y][pos.x])

def readInput(filename: str):
    """
    Parses the input file.
    """
    data = open("2024/Day10/" + filename + ".txt", "r")
    lines = data.readlines()
    return Map(lines)

def getNeighborPositions(pos: Pos) -> list[Pos]:
    """
    Returns the four neighboring positions.
    """
    left = Pos(pos.x-1, pos.y)
    right = Pos(pos.x+1, pos.y)
    top = Pos(pos.x, pos.y-1)
    bottom = Pos(pos.x, pos.y+1)
    return [left, top, right, bottom]

def followPath(start: Pos, map: Map, doRate = False):
    """
    Follows all paths starting at the given position and returns the number of peaks that can be reached.
    If doRate is set, all distinct paths to the peak are counted.
    """
    ends = 0
    queue = [start]
    scheduled = set()
    while len(queue) > 0:
        currentPos = queue.pop(0)
        current = map.get(currentPos)
        if current == 9:
            ends += 1
            continue
        neighbors = getNeighborPositions(currentPos)
        for n in neighbors:
            if map.get(n) == current + 1:
                if not doRate and n in scheduled:
                    continue
                queue.append(n)
                scheduled.add(n)
    return ends

def solveTask1(map: Map):
    sum = 0
    for h in map.heads:
        sum += followPath(h, map)
    print(sum)

def solveTask2(map: Map):
    sum = 0
    for h in map.heads:
        sum += followPath(h, map, True)
    print(sum)

map = readInput("input")
solveTask2(map)