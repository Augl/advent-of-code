class Machine:
    def __init__(self, a: int, b: int, c: int, program: list[int]) -> None:
        """
        Creates a new machine with the given register values.
        """
        self.reset(a, b, c)
        self.program = program

    def reset(self, a: int, b: int, c: int):
        self.programCounter = 0
        self.regA = a
        self.regB = b
        self.regC = c
        self.output: list[int] = []

    def resolveComboOperand(self, op: int) -> int:
        """
        Resolves the given operand.
        """
        if op >= 0 and op <= 3:
            return op
        if op == 4:
            return self.regA
        if op == 5:
            return self.regB
        if op == 6:
            return self.regC
        raise ValueError("Unexpected operand in combo operand resolver.")

    def runADV(self, operand: int):
        """
        Executes a-division instruction.
        """
        numerator = self.regA
        denumerator = 2 ** self.resolveComboOperand(operand)
        self.regA = int(numerator / denumerator)

    def runBDV(self, operand: int):
        """
        Executes b-division instruction.
        """
        numerator = self.regA
        denumerator = 2 ** self.resolveComboOperand(operand)
        self.regB = int(numerator / denumerator)

    def runCDV(self, operand: int):
        """
        Executes c-division instruction.
        """
        numerator = self.regA
        denumerator = 2 ** self.resolveComboOperand(operand)
        self.regC = int(numerator / denumerator)

    def runBXL(self, operand: int):
        """
        Executes the first bitwise xor instruction.
        """
        self.regB = self.regB ^ operand

    def runJNZ(self, operand: int):
        """
        Executes the jump instruction. Jumps to 2 less than specified so that the program counter
        can still be increases by 2 after the instruction has been executed.
        """
        if self.regA == 0:
            return
        self.programCounter = operand - 2

    def runBXC(self, _: int):
        """
        Executes the second bitwise xor instruction.
        """
        self.regB = self.regB ^ self.regC

    def runOUT(self, operand: int):
        """
        Executes the out instruction.
        """
        value = self.resolveComboOperand(operand) % 8
        self.output.append(value)

    def runBST(self, operand: int):
        """
        Executes the bst instruction.
        """
        self.regB = self.resolveComboOperand(operand) % 8

    def run(self):
        while True:
            if self.programCounter >= len(self.program):
                break
            instr = self.program[self.programCounter]
            operand = self.program[self.programCounter + 1]
            if instr == 0:
                self.runADV(operand)
            if instr == 1:
                self.runBXL(operand)
            if instr == 2:
                self.runBST(operand)
            if instr == 3:
                self.runJNZ(operand)
            if instr == 4:
                self.runBXC(operand)
            if instr == 5:
                self.runOUT(operand)
            if instr == 6:
                self.runBDV(operand)
            if instr == 7:
                self.runCDV(operand)
            self.programCounter += 2
        return self.output

def readInput(filename: str):
    """
    Parses the input file.
    """
    data = open("2024/Day17/" + filename + ".txt", "r")
    lines = data.readlines()
    a = int(lines[0].strip().split(":")[1])
    b = int(lines[1].strip().split(":")[1])
    c = int(lines[2].strip().split(":")[1])
    prog = lines[4].strip().split(":")[1]
    prog = list(map(int, prog.split(",")))
    return Machine(a, b, c, prog)

def solveTask1(machine: Machine):
    """
    Solves the first task by running the program on the small virtual computer.
    """
    output = machine.run()    
    outStr = list(map(str, output))
    print(",".join(outStr))

def solveTask2(machine: Machine, aVal: int, offset: int):
    """
    Solves the second task.
    The program consumes the number in register a in groups of 3 bits (so octal numbers).
    Therefore, we first find the three bits necessary to create the last number in the program (desired output).
    When a matching number is found, the number is shifted left by 3 bits (by multiplying with 8) and the 
    process is repeated with the second to last number in the program.
    """
    machine.reset(aVal, 0, 0)
    output = machine.run()
    if output == machine.program:
        return aVal
    if output == machine.program[-offset:] or offset == 0:
        minResult = 999999999999999
        for n in range(8):
            result = solveTask2(machine, 8 * aVal + n, offset + 1)
            if result != None:
                minResult = min(result, minResult)
        if offset == 0:
            print(minResult)
        return minResult

machine = readInput("input")
solveTask1(machine)
solveTask2(machine, 0, 0)

