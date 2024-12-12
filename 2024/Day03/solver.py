import re

def readInput() -> list[str]:
    """
    Parses the input file using regex, extracts all commands.
    """
    data = open("2024/Day03/input.txt", "r")
    mulPat = "mul\\(\\d{1,3},\\d{1,3}\\)" # finds all mul(xxx, yyy)
    dontPat = "don't\\(\\)"
    doPat = "do\\(\\)"
    return re.findall("(" + mulPat + "|" + dontPat + "|" + doPat + ")", data.read())

def runProgram(p: list[str], allowControlFlow = False) -> int:
    """
    Executes the given program by interpreting the commands.
    If the allowControlFlow flag is set, do() and don't() commands are exeuted, otherwise they are ignored.
    """
    sum = 0
    enabled = True
    for instr in p:
        if instr[0:3] == "mul" and enabled:
            substr = instr[4:-1]
            split = substr.split(",")
            sum += int(split[0]) * int(split[1])
        if instr[0:5] == "don't" and allowControlFlow:
            enabled = False
        if instr[0:4] == "do()":
            enabled = True
    return sum

def solveTask1(p: list[str]):
    """
    Solves the first task by running the program and ignoring the do() and don't() commands.
    """
    print(runProgram(p))

def solveTask2(p: list[str]):
    """
    Solves the second task by running the program and executing all commands.
    """
    print(runProgram(p, True))

prog = readInput()
solveTask2(prog)