def readInput():
    data = open("2024/Day01/input.txt", "r")
    lines = data.readlines()

    left = []
    right = []
    for l in lines:
        split = l.split("   ")
        left.append(int(split[0]))
        right.append(int(split[1]))
    
    return (left, right)



def solveTask1(left, right):
    left.sort()
    right.sort()
    sum = 0
    for i in range(len(left)):
        sum += abs(left[i] - right[i])
    print(sum)



def solveTask2(left, right):
    appearances = {}
    for el in right:
        appearances[el] = appearances.get(el, 0) + 1
    
    score = 0
    for el in left:
        score += el * appearances.get(el, 0)
    print(score)

(left, right) = readInput()
solveTask1(left, right)
solveTask2(left, right)