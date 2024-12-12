def readInput() -> list[str]:
    """
    Parses the input file. Returnes an array of lines.
    """
    data = open("2024/Day04/input.txt", "r")
    lines = data.readlines()
    return lines

def checkDirection(lines: list[str], word: str, l: int, c: int, dL: int, dC: int) -> int:
    """
    Checks if the given word appears at the given location in the given direction.
    Returns 1 if the word is found, 0 otherwise.
    """
    i = 0
    while l >= 0 and l < len(lines) and c >= 0 and c < len(lines[l]) and i < len(word) and word[i] == lines[l][c]:
        l += dL
        c += dC
        i += 1
    if i == len(word):
        return 1
    return 0

def solveTask1(lines: list[str]):
    """
    Solves the first task by going through the grid and checking for each X that is encountered if 
    that X is the start of XMAS in any possible direction.
    """
    word = "XMAS"
    found = 0
    for lIndex in range(len(lines)):
        l = lines[lIndex]
        for cIndex in range(len(l)):
            c = l[cIndex]
            if c != word[0]:
                continue
            found += checkDirection(lines, word, lIndex, cIndex, 0, 1)
            found += checkDirection(lines, word, lIndex, cIndex, 0, -1)
            found += checkDirection(lines, word, lIndex, cIndex, 1, 0)
            found += checkDirection(lines, word, lIndex, cIndex, -1, 0)
            found += checkDirection(lines, word, lIndex, cIndex, -1, -1)
            found += checkDirection(lines, word, lIndex, cIndex, -1, 1)
            found += checkDirection(lines, word, lIndex, cIndex, 1, -1)
            found += checkDirection(lines, word, lIndex, cIndex, 1, 1)
    print(found)

def solveTask2(lines: list[str]):
    """
    Solves the second task by going through the grid and checking for each A if it's the center
    of an X-MAS.
    """
    found = 0
    for lIndex in range(len(lines)):
        l = lines[lIndex]
        for cIndex in range(len(l)):
            c = l[cIndex]
            if c != "A":
                continue
            if checkDirection(lines, "MAS", lIndex-1, cIndex-1, 1, 1) == 0 and checkDirection(lines, "SAM", lIndex-1, cIndex-1, 1, 1) == 0:
                continue
            if checkDirection(lines, "MAS", lIndex-1, cIndex+1, 1, -1) == 1 or checkDirection(lines, "SAM", lIndex-1, cIndex+1, 1, -1) == 1:
                found += 1
    print(found)


data = readInput()
solveTask2(data)