class Equation:
    def __init__(self, line: str) -> None:
        """
        Creates a new Equation from a string representation.
        """
        line = line.strip()
        split = line.split(":")
        self.result = int(split[0])
        self.numbers = list(map(int, split[1].split(" ")[1:]))

def readInput(filename: str) -> list[Equation]:
    """
    Parses the input file. Returns a list of equations.
    """
    file = open("2024/Day07/" + filename + ".txt", "r")
    lines = file.readlines()
    equations = []
    for l in lines:
        eq = Equation(l)
        equations.append(eq)
    return equations

def solveEquation(equation: Equation, allowConcat = False) -> bool:
    """
    Tries to solve the given equation using addition and multiplication. If the allowConcat flag is set,
    concationation is allowed as a third operator.
    """
    bases = [equation.numbers[0]]
    for current in range(1, len(equation.numbers)):
        nextBases = []
        for b in bases:
            if b > equation.result:
                continue
            currentN = equation.numbers[current]
            added = b + currentN
            multed = b * currentN
            nextBases.append(added)
            nextBases.append(multed)
            concat = 0
            if allowConcat:
                concat = int(str(b) + str(currentN))
            nextBases.append(concat)
            if current == len(equation.numbers)-1 and (added == equation.result or multed == equation.result or concat == equation.result):
                return True
        bases = nextBases
    return False


def solveTask1(equations: list[Equation]):
    """
    Solves task one by solving all equations with only addition and multiplication.
    """
    sum = 0
    for eq in equations:
        if solveEquation(eq):
            sum += eq.result
    print(sum)

def solveTask2(equations: list[Equation]):
    """
    Solves task two by solving all equations with all three operators.
    """
    sum = 0
    for eq in equations:
        if solveEquation(eq, True):
            sum += eq.result
    print(sum)

equations = readInput("input")
solveTask2(equations)
