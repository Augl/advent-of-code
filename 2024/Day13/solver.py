class  Vec:
    def __init__(self, x: int, y: int) -> None:
        """
        Creates a new vector with x and y components.
        """
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """
        Returns a human readable representation.
        """
        return f"({self.x}, {self.y})"
    
    def __sub__(self, other):
        """
        Calculates the difference.
        """
        if not isinstance(other, Vec):
            raise TypeError("Vec can only be subtracted by Vec.")
        return Vec(self.x - other.x, self.y - other.y)
    
    def scale(self, s: int):
        """
        Returnes a new Vec representing a scaled Vec.
        """
        return Vec(self.x * s, self.y * s)
    
    def isDivisibleBy(self, other):
        """
        Checks if the other Vec can be scaled by an int to match the current Vec.
        """
        return self.x % other.x == 0 and self.y % other.y == 0
    
    def findScale(self, other):
        """
        Finds an integer scale to make other the same as self if it exists.
        """
        fX = self.x / other.x
        fY = self.y / other.y
        if not fX.is_integer() or not fY.is_integer() or fX != fY:
            return None
        return int(fX)


class ClawMachine:
    def __init__(self, lines: list[str]) -> None:
        """
        Creates a new instance by parsing the given lines of text.
        """
        if len(lines) != 3:
            raise ValueError("ClawMachine needs three lines of text to be created.")
        split = lines[0].strip()[9:].split(",")
        self.buttonA = Vec(int(split[0][3:]), int(split[1][3:]))
        split = lines[1].strip()[9:].split(",")
        self.buttonB = Vec(int(split[0][3:]), int(split[1][3:]))
        split = lines[2].strip()[6:].split(",")
        self.price = Vec(int(split[0][3:]), int(split[1][3:]))

def findStrategy(m: ClawMachine):
    """
    Finds a suitable strategy.
    First, ButtonA and ButtonB (or their direction) are treated as lines of the form y = ax + b.
    The line representing ButtonA has a b value of 0 because the claw machine starts at (0, 0).
    The b value of the line representing ButtonB can be calculated using b = y - m_b * x
    Then, the intersection point of the two lines can be calculated.
    The ratio intersection.x / buttonA.x is roughly the amount of ButtonA presses that are needed.
    """
    gradA = m.buttonA.y / m.buttonA.x
    gradB = m.buttonB.y / m.buttonB.x
    b = m.price.y - gradB * m.price.x
    x = b/(gradA - gradB)
    roughAmountA = int(x / m.buttonA.x)
    for i in range(roughAmountA-1, roughAmountA+2):
        remaining = m.price - m.buttonA.scale(i)
        if remaining.isDivisibleBy(m.buttonB):
            scale = remaining.findScale(m.buttonB)
            if scale != None:
                return (i, scale)

def readInput(filename: str):
    """
    Parses the input file.
    """
    data = open("2024/Day13/" + filename + ".txt", "r")
    lines = data.readlines()
    machines = []
    for i in range(0, len(lines), 4):
        machine = ClawMachine(lines[i:i+3])
        machines.append(machine)
    return machines

def solveTask1(machines: list[ClawMachine]):
    """
    Solves task 1.
    """
    tokens = 0
    for m in machines:
        strat = findStrategy(m)
        if strat != None:
            tokens += strat[0] * 3 + strat[1]
    print(tokens)

def solveTask2(machines: list[ClawMachine]):
    """
    Solves task 2 by moving the price position and finding a suitable strategy.
    """
    tokens = 0
    for m in machines:
        m.price.x += 10000000000000
        m.price.y += 10000000000000
        strat = findStrategy(m)
        if strat != None:
            tokens += strat[0] * 3 + strat[1]
    print(tokens)
    
machines = readInput("input")
solveTask2(machines)