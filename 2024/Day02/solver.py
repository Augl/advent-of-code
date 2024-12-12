def readInput():
    """
    Parses the input file.
    """
    data = open("2024/Day02/input.txt", "r")
    lines = data.readlines()
    reports = []
    for l in lines:
        split = l.split(" ")
        reports.append(list(map(int, split)))
    
    return reports

def checkReport(r: list) -> int:
    """
    Checks if a given report is valid.
    Returns the index of the first failing number or -1 if the report is valid.
    """
    changePrev = r[1] > r[0]
    for i in range(1, len(r)):
        change = r[i] > r[i-1]
        if changePrev != change:
            return i
        changePrev = change
        diff = abs(r[i] - r[i-1])
        if diff < 1 or diff > 3:
            return i
    return -1

def solveTask1(reports):
    """
    Solves task 1 by checking all reports.s
    """
    sum = 0
    for r in reports:
        if checkReport(r) == -1:
            sum += 1
    print(sum)

def checkReportModified(r: list[int], remove: int) -> bool:
    """
    Checks the validity of a report after removing the element with the given index.
    """
    copy = r.copy()
    copy.pop(remove)
    return checkReport(copy) == -1

def solveTask2(reports: list[list[int]]): 
    """
    Checks each record and, if a record is invalid, tries again with the first element or any element in the collision removed.
    """   
    sum = 0
    for r in reports:
        result = checkReport(r)
        if result == -1:
            sum += 1
        elif checkReportModified(r, 0) or checkReportModified(r, result-1) or checkReportModified(r, result):
            sum += 1
    print(sum)        

reports = readInput()
solveTask2(reports)