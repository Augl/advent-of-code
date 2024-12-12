def readInput(filename: str):
    """
    Parses the input file.
    """
    data = open("2024/Day11/" + filename + ".txt", "r")
    lines = data.readlines()
    if len(lines) != 1:
        raise ValueError("Input expected to be one line only.")
    strings = lines[0].strip().split(" ")
    return list(map(int, strings))

def getStonesAfterBlink(stone: int):
    """
    Returns a list of stones that appear from the given stone after one blink.
    """
    next: list[int] = []
    if stone == 0:
        next.append(1)
    elif len(str(stone)) % 2 == 0:
        string = str(stone)
        half = int(len(string)/2)
        next.append(int(string[:half]))
        next.append(int(string[half:]))
    else:
        next.append(stone * 2024)
    return next

def solveTask1(stones: list[int]):
    """
    Solves the first task using brute force.
    """
    next: list[int] = []
    for i in range(25):
        for s in stones:
            after = getStonesAfterBlink(s)
            next.extend(after)
        stones = next
        next = []
    print(len(stones))

def getOccurences(stones: list[int]) -> dict[int, int]:
    """
    Returns a dictionary indicating for each engraving how many stones there are.
    """
    occs = {}
    for s in stones:
        n = occs.get(s, 0)
        occs[s] = n + 1
    return occs

def sumValues(dict: dict[int, int]):
    """
    Sums up all values in the dictionary.
    """
    sum = 0
    for k in dict:
        sum += dict[k]
    return sum

def solveTask2(stones: list[int]):
    """
    Solves the second task by keeping track of how many stones have which engraving.
    """
    occs = getOccurences(stones)
    for i in range(75):
        newOccs = {}
        for value in occs:
            after = getStonesAfterBlink(value)
            amount = occs[value]
            for v in after:
                before = newOccs.get(v, 0)
                newOccs[v] = before + amount
        occs = newOccs
        newOccs = {}
    print(sumValues(occs))

stones = readInput("input")
solveTask2(stones)