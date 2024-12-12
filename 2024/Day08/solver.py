class Pos:
    def __init__(self, x, y):
        """
        Creates a new position with the given coordinates.
        """
        self.x = x
        self.y = y

    def diff(self, other):
        """
        Returns the difference of the two positions.
        """
        return Pos(self.x - other.x, self.y - other.y)
    
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


def readInput(filename: str):
    """
    Reads the input file. Returns a list of antennas per frequency and the board dimensions.
    """
    f = open("2024/Day08/" + filename + ".txt")
    lines = f.readlines()
    antennas: dict[str, list[Pos]] = {}
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            char = lines[y][x]
            if char == "." or char == "\n":
                continue
            if not char in antennas:
                antennas[char] = []
            antennas[char].append(Pos(x, y))
    return (antennas, Pos(len(lines[0])-1, len(lines)))

def isInBounds(pos: Pos, dim: Pos):
    """
    Checks if the given position is within the board bounds.
    """
    return pos.x >= 0 and pos.x < dim.x and pos.y >= 0 and pos.y < dim.y

def findAntinodes(antenna1: Pos, antenna2: Pos, antinodes: set[Pos], dim: Pos, wholeLine = False):
    """
    Finds the antinodes created by the two antennas. Antinodes are added to the given set.
    If wholeLine ist set, all antinodes on the line are found, otherwise only the closest two.
    """
    diff = antenna1.diff(antenna2)
    antinodes.add(antenna1)
    while True:
        antenna1 = Pos(antenna1.x + diff.x, antenna1.y + diff.y)
        if isInBounds(antenna1, dim):
            antinodes.add(antenna1)
        else:
            break
        if not wholeLine:
            break
    antinodes.add(antenna2)
    while True:
        antenna2 = Pos(antenna2.x - diff.x, antenna2.y - diff.y)
        if isInBounds(antenna2, dim):
            antinodes.add(antenna2)
        else:
            break
        if not wholeLine:
            break

def findAllAntinodes(antennas: list[Pos], antinodes: set[Pos], dim: Pos, wholeLine = False):
    """
    Finds all antinodes created by a list of antennas of the same frequency.
    """
    for i in range(len(antennas)):
        for j in range(len(antennas)):
            if i == j:
                continue
            findAntinodes(antennas[i], antennas[j], antinodes, dim, wholeLine)

def solveTask1(antennas: dict[str, list[Pos]], dim: Pos):
    """
    Solves task 1 by iterating over all antenna pairs and finding the two closest antinodes.
    """
    antinodes = set()
    for type in antennas:
        findAllAntinodes(antennas[type], antinodes, dim)
    print(len(antinodes))

def solveTask2(antennas, dim):
    """
    Solves task 2 by iterating over all antenna pairs and finding all antinodes on the line.
    """
    antinodes = set()
    for type in antennas:
        findAllAntinodes(antennas[type], antinodes, dim, True)
    print(len(antinodes))

antennas, dim = readInput("input")
solveTask2(antennas, dim)