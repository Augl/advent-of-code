import time

class Pos:
    def __init__(self, x: int, y: int) -> None:
        """
        Creates a new position with x and y components.
        """
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        """
        Returns a human readable representation.
        """
        return f"({self.x}, {self.y})"

class Robot:
    def __init__(self, spec: str) -> None:
        """
        Parses the given string to create a new robot.
        """
        split = spec.strip().split(" ")
        posSplit = split[0][2:].split(",")
        vecSplit = split[1][2:].split(",")
        self.position = Pos(int(posSplit[0]), int(posSplit[1]))
        self.velocity = Pos(int(vecSplit[0]), int(vecSplit[1]))

def readInput(filename: str):
    """
    Parses the input file.
    """
    data = open("2024/Day14/" + filename + ".txt", "r")
    lines = data.readlines()
    robots = []
    for l in lines:
        robots.append(Robot(l))
    return robots

def getSafetyFactor(positions: list[Pos], width: int, height: int) -> int:
    """
    Counts the robots in each quadrant and returns the safety factor.
    """
    topLeft = 0
    topRight = 0
    bottomLeft = 0
    bottomRight = 0
    for p in positions:
        if p.x < width // 2 and p.y < height // 2:
            topLeft += 1
        if p.x > width // 2 and p.y < height // 2:
            topRight += 1
        if p.x < width // 2 and p.y > height // 2:
            bottomLeft += 1
        if p.x > width // 2 and p.y > height // 2:
            bottomRight += 1
    return topLeft * topRight * bottomLeft * bottomRight


def solveTask1(robots: list[Robot], width: int, height: int):
    """
    Solves the first task by directly calculating the robots end positions.
    """
    endPositions = []
    for r in robots:
        x = r.position.x + 100 * r.velocity.x
        y = r.position.y + 100 * r.velocity.y
        endPos = Pos(x % width, y % height)
        endPositions.append(endPos)
    print(getSafetyFactor(endPositions, width, height))

def countRobotsInAreas(positions: list[Pos], width: int, size: int):
    """
    Splits the map into squares of given size and counts the number of robots in each square.
    """
    nAreas = (width // size) + 1
    areas = []
    for _ in range(nAreas):
        areas.append([0] * nAreas)
    for p in positions:
        yArea = p.y // size
        xArea = p.x // size
        areas[yArea][xArea] += 1
    return areas

def printRobotPositions(robots: list[Pos], width: int, height: int):
    """
    Prints an ASCII-image of the robots positions.
    """
    image = []
    for _ in range(height):
        image.append([" "] * width)
    for r in robots:
        image[r.y % height][r.x % width] = "#"
    for r in image:
        print("".join(r))
    print("", flush=True)

def solveTask2(robots: list[Robot], width: int, height: int, fromIt = 5000, toIt = 7000):
    """
    Solves the second task by simulating the robots and keeping track of the number of robots in the
    square with the highest density. To draw a christmas tree a few squares will have a very high robot
    density. For visual confirmation the frames are drawn to terminal.
    """
    maxDensity = 0
    for i in range(fromIt, toIt + 1):
        endPositions = []
        for r in robots:
            x = r.position.x + i * r.velocity.x
            y = r.position.y + i * r.velocity.y
            endPos = Pos(x % width, y % height)
            endPositions.append(endPos)
        areas = countRobotsInAreas(endPositions, width, 10)
        for r in areas:
            for v in r:
                if v > maxDensity:
                    maxDensity = v
                if v > 50:
                    print("found valid option", i)
                    printRobotPositions(endPositions, width, height)

robots = readInput("input")
solveTask2(robots, 101, 103)