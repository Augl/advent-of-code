import math

def parseRule(rule: str) -> tuple[int, int]:
    """
    Parses a rule. Converts 'X|Y' to a tuple of ints (X, Y).
    """
    rule = rule.strip()
    split = rule.split("|")
    return (int(split[0]), int(split[1]))

def parseUpdate(update: str) -> list[int]:
    """
    Parses an update. Converts a string of numbers into a list of ints.
    """
    update = update.strip()
    split = update.split(",")
    return list(map(int, split))

def readInput(filename: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    """
    Parses the input file. Returnes the rules and the update sequences.
    """
    data = open("2024/Day05/" + filename + ".txt", "r")
    lines = data.readlines()
    rules = []
    updates = []
    for i in range(len(lines)):
        l = lines[i]
        if l == "\n":
            rules = lines[:i]
            updates = lines[i+1:]
    rules = list(map(parseRule, rules))
    updates = list(map(parseUpdate, updates))
    return (rules, updates)

def compileRules(rules: list[tuple[int, int]]) -> dict[int, set[int]]:
    """
    Compiles the given list of rules into a more efficient format.
    Returns a dictionary. For each number it contains a set of values that must be after the value.
    """
    result: dict[int, set[int]] = {}
    for r in rules:
        first = r[0]
        after = r[1]
        if not first in result:
            result[first] = set()
        result[first].add(after)
    return result

def checkUpdate(compiled: dict[int, set[int]], update: list[int]) -> tuple[int, int] | None:
    """
    Checks the given update against the rules. Returns a tuple of indices of conflicting numbers or None,
    if no such conflicts exist.
    """
    for i in range(len(update)):
        n = update[i]
        if not n in compiled:
            continue
        rule = compiled[n]
        for j in range(i):
            b = update[j]
            if b in rule:
                return (i, j)
    return None

def solveTask1(rules: list[tuple[int, int]], updates: list[list[int]]):
    """
    Solves the first task by compiling the rules and checking each update against them.
    """
    compiled = compileRules(rules)
    sum = 0
    for u in updates:
        if not checkUpdate(compiled, u):
            continue
        sum += u[math.floor(len(u)/2)]
    print(sum)

def solveTask2(rules: list[tuple[int, int]], updates: list[list[int]]):
    """
    Solves task 2 by checking all updates against the ruleset. On invalid updates the problematic numbers
    are switched until all confilcts are resolved.
    """
    compiled = compileRules(rules)
    sum = 0
    for u in updates:
        problem = checkUpdate(compiled, u)
        if problem == None:
            continue
        while problem != None:
            temp = u[problem[0]]
            u[problem[0]] = u[problem[1]]
            u[problem[1]] = temp
            problem = checkUpdate(compiled, u)
        sum += u[math.floor(len(u)/2)]
    print(sum)

    
rules, updates = readInput("input")
solveTask2(rules, updates)
