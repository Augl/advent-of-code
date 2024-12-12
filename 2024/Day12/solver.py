class Pos:
    def __init__(self, x, y) -> None:
        """
        Creates a new position at the given coordinates.
        """
        self.x = x
        self.y = y

    def getNeighbors(self):
        """
        Returns all four neighboring positions.
        """
        return [
            Pos(self.x+1, self.y),
            Pos(self.x-1, self.y),
            Pos(self.x, self.y+1),
            Pos(self.x, self.y-1),
        ]
    
    def __repr__(self) -> str:
        """
        Returns a human readable representation.
        """
        return f"Pos({self.x}, {self.y})"
    
    def __hash__(self) -> int:
        """
        Returns the hash.
        """
        return (self.x, self.y).__hash__()
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Pos):
            return False
        return self.x == value.x and self.y == value.y
    
class BorderSegment:
    def __init__(self, p1: Pos, p2: Pos) -> None:
        """
        Creates a new border segment between two positions.
        The first position must be inside, the second outside.
        """
        if p1.x == p2.x and p1.y - p2.y == 1:
            self.startPos = p1
            self.endPos = Pos(p1.x + 1, p1.y)
            self.direction = "R"
        elif p1.x == p2.x and p1.y - p2.y == -1:
            self.startPos = Pos(p1.x + 1, p1.y + 1)
            self.endPos = Pos(p1.x, p1.y + 1)
            self.direction = "L"
        elif p1.y == p2.y and p1.x - p2.x == 1:
            self.startPos = Pos(p1.x, p1.y + 1)
            self.endPos = Pos(p1.x, p1.y)
            self.direction = "U"
        elif p1.y == p2.y and p1.x - p2.x == -1:
            self.startPos = p2
            self.endPos = Pos(p2.x, p2.y + 1)
            self.direction = "D"
        else:
            raise ValueError("BorderSegment can only be created between adjacent positions.")

class Map:
    def __init__(self, data: list[str]) -> None:
        """
        Creates a new map from the input data.
        """
        self._data = data
        self.height = len(data)
        self.width = len(data[0]) - 1
        self.visited = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(False)
            self.visited.append(row)

    def get(self, pos: Pos):
        """
        Returns the value at the given position.
        """
        if pos.x < 0 or pos.x >= self.width:
            return ""
        if pos.y < 0 or pos.y >= self.height:
            return ""
        return self._data[pos.y][pos.x]

    def wasVisited(self, pos: Pos):
        """
        Returns true if the given position was already visited.
        """
        if pos.x < 0 or pos.x >= self.width:
            return True
        if pos.y < 0 or pos.y >= self.height:
            return True
        return self.visited[pos.y][pos.x]
    
    def markVisited(self, pos: Pos):
        """
        Marks the given position as visited.
        """
        if pos.x < 0 or pos.x >= self.width:
            return
        if pos.y < 0 or pos.y >= self.height:
            return
        self.visited[pos.y][pos.x] = True

def readInput(filename: str):
    """
    Parses the input file.
    """
    data = open("2024/Day12/" + filename + ".txt", "r")
    lines = data.readlines()    
    return Map(lines)

def analyzeArea(map: Map, start: Pos):
    """
    Finds the size of a planting area and all border segments using BFS.
    """
    value = map.get(start)
    map.markVisited(start)
    queue = [start]
    area = 0
    border = 0
    segments: dict[Pos, list[BorderSegment]] = {}
    while len(queue) > 0:
        current = queue.pop(0)
        area += 1
        neighbors = current.getNeighbors()
        for n in neighbors:
            if map.get(n) != value:
                border += 1
                segment = BorderSegment(current, n)
                if (not segment.startPos in segments):
                    segments[segment.startPos] = []
                segments[segment.startPos].append(segment)
                continue
            if map.wasVisited(n):
                continue
            map.markVisited(n)
            queue.append(n)
    return (area, border, segments)

def getAnyBorderSegment(segments: dict[Pos, list[BorderSegment]]):
    """
    Returns any border segment from the given segment collection.
    """
    key, current = segments.popitem()
    if len(current) == 1:
        return current[0]
    element = current.pop()
    segments[key] = current
    return element

def countSides(segments: dict[Pos, list[BorderSegment]]):
    """
    Reconstructs the border and counts the number of sides.
    """
    sum = 0
    while len(segments) > 0:
        current = getAnyBorderSegment(segments)
        direction = current.direction
        start = current.startPos
        startDir = direction
        changes = 0
        while True:
            nextList = segments[current.endPos]
            next = nextList.pop()
            if len(nextList) == 0:
                del segments[current.endPos]
            if next.direction != direction:
                changes += 1
            if next.endPos == start:
                if next.direction != startDir:
                    changes += 1
                sum += changes
                break
            direction = next.direction
            current = next
    return sum

def solveTask1(map: Map):
    """
    Solves the first task by analyzing all planting areas.
    """
    sum = 0
    for y in range(map.height):
        for x in range(map.width):
            if not map.wasVisited(Pos(x, y)):
                area, border, _ = analyzeArea(map, Pos(x, y))
                sum += area * border
    print(sum)

def solveTask2(map: Map):
    """
    Solves the second task by analyzing all planting areas, constructing the border and counting the
    consecutive border segments (number of sides).
    """
    sum = 0
    for y in range(map.height):
        for x in range(map.width):
            if not map.wasVisited(Pos(x, y)):
                area, _, segments = analyzeArea(map, Pos(x, y))
                sides = countSides(segments)
                sum += area * sides
    print(sum)


map = readInput("input")
solveTask2(map)