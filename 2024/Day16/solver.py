from enum import Enum

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def isHorizontal(self):
        return self == Direction.RIGHT or self == Direction.LEFT
    
    def isCorner(self, other):
        return self.isHorizontal() != other.isHorizontal()

class Pos:
    def __init__(self, x: int, y: int) -> None:
        """
        Creates a new position.
        """
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        """
        Returns the hash.
        """
        return (self.x, self.y).__hash__()
    
    def __eq__(self, value: object) -> bool:
        """
        Checks if two positions are equal.
        """
        if not isinstance(value, Pos):
            return False
        return self.x == value.x and self.y == value.y
    
    def __repr__(self) -> str:
        """
        Returns a human readable form.
        """
        return f"({self.x}, {self.y})"
    
    def getNeighbors(self):
        """
        Returns all neighbors and the direction towards them.
        """
        return [
            (Pos(self.x, self.y - 1), Direction.UP),
            (Pos(self.x, self.y + 1), Direction.DOWN),
            (Pos(self.x - 1, self.y), Direction.LEFT),
            (Pos(self.x + 1, self.y), Direction.RIGHT),
        ]

class Node:
    def __init__(self, pos: Pos, dir: Direction, cost: int) -> None:
        """
        Creates a new node.
        """
        self.position = pos
        self.direction = dir
        self.cost = cost

    def __repr__(self) -> str:
        """
        Returns a human readable form.
        """
        return f"({self.position}, {self.direction}, {self.cost})"

class Map:
    def __init__(self, input: list[str]) -> None:
        """
        Creates a new map by parsing the input.
        """
        self.height = len(input)
        self.width = len(input[0]) - 1
        data: list[list[bool]] = []
        for y in range(self.height):
            data.append([])
            for x in range(self.width):
                char = input[y][x]
                data[y].append(char != "#")
                if char == "E":
                    self.exit = Pos(x, y)
                if char == "S":
                    self.start = Pos(x, y)
        self._data = data

    def isWalkable(self, pos: Pos):
        """
        Checks if the given position is walkable.
        """
        return self._data[pos.y][pos.x]
    
PredMap = dict[tuple[Pos, Direction], list[tuple[Pos, Direction]]]

def readInput(filename: str):
    """
    Parses the input file.
    """
    data = open("2024/Day16/" + filename + ".txt", "r")
    lines = data.readlines()
    return Map(lines)

def addToCostDictAndQueue(minCost: dict[Pos, dict[Direction, int]], node: Node, queue: list[Node], pred: PredMap, previous: Node | None):
    """
    Adds the specific node to the minCost map, the queue and the predecessor map.
    """
    if (node.position, node.direction) not in pred:
        pred[(node.position, node.direction)] = []
    if node.direction not in minCost[node.position] or minCost[node.position][node.direction] > node.cost:
        minCost[node.position][node.direction] = node.cost
        queue.append(node)
        pred[(node.position, node.direction)] = []
    if minCost[node.position][node.direction] == node.cost and previous != None:
        pred[(node.position, node.direction)].append((previous.position, previous.direction))

def addAllToCostDictAndQueue(minCost: dict[Pos, dict[Direction, int]], node: Node, queue: list[Node], pred: PredMap, previous: Node | None = None):
    """
    Adds the given node to the minCost map for all directions if it has a lower cost. 
    Also adds all new nodes to the queue and the predecessor map.
    """
    if node.position not in minCost:
        minCost[node.position] = {}
    addToCostDictAndQueue(minCost, node, queue, pred, previous)
    for d in [Direction.DOWN, Direction.UP, Direction.LEFT, Direction.RIGHT]:
        if not d.isCorner(node.direction):
            continue
        addToCostDictAndQueue(minCost, Node(node.position, d, node.cost + 1000), queue, pred, previous)

def findCostsToAll(map: Map, start: Pos, startDirection: Direction):
    """
    Finds the cost of moving to any position with any direction from the start position.
    """
    queue: list[Node] = []
    minCost: dict[Pos, dict[Direction, int]] = {}
    pred: PredMap = {}
    addAllToCostDictAndQueue(minCost, Node(start, startDirection, 0), queue, pred)
    while len(queue) > 0:
        current = queue.pop(0)
        neighbors = current.position.getNeighbors()
        for n, d in neighbors:
            if not map.isWalkable(n):
                continue
            if d == current.direction:
                addAllToCostDictAndQueue(minCost, Node(n, d, current.cost + 1), queue, pred, current)
    return (minCost, pred)

def findPositionsOnPaths(pred: PredMap, end: Pos, minCost: dict[Pos, dict[Direction, int]], pathLength: int):
    """
    Finds all positions on all shortest paths.
    """
    positions: set[Pos] = set()
    queue: list[tuple[Pos, Direction]] = []
    for d in [Direction.DOWN, Direction.UP, Direction.LEFT, Direction.RIGHT]:
        if minCost[end][d] == pathLength:
            queue.append((end, d))
    while len(queue) > 0:
        pos, dir = queue.pop(0)
        positions.add(pos)
        for option in pred[(pos, dir)]:
            queue.append(option)
    return positions

def solveTasks(map: Map):
    startCosts, pred = findCostsToAll(map, map.start, Direction.RIGHT)
    minLength = 100000
    for dir in startCosts[map.exit]:
        v = startCosts[map.exit][dir]
        if v < minLength:
            minLength = v
    print("shortest path length:", minLength)
    positions = findPositionsOnPaths(pred, map.exit, startCosts, minLength)
    print("number of positions on path:", len(positions))

map = readInput("input")
solveTasks(map)

    