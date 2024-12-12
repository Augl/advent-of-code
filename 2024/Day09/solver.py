from typing import cast

class File:
    def __init__(self, id: int, size: int) -> None:
        """
        Creates a new File with an id and size.
        """
        self.id = id
        self.size = size

class Space:
    def __init__(self, size: int) -> None:
        """
        Creates a new Space with given size.
        """
        self.size = size

def readInput(filename: str) -> list[File | Space]:
    """
    Parses the input file.
    """
    data = open("2024/Day09/" + filename + ".txt", "r")
    lines = data.readlines()
    if len(lines) != 1:
        raise ValueError("Input should only be one line.")
    disk = []
    for i in range(len(lines[0])):
        if i % 2 == 0:
            disk.append(File(int(i / 2), int(lines[0][i])))
        else:
            disk.append(Space(int(lines[0][i])))
    return disk

def getNextNonEmptyFileFromBack(disk: list[File | Space], right: int) -> int:
    """
    Returns the index of a non empty file to the left of the given index from left to right.
    """
    while isinstance(disk[right], Space) or disk[right].size == 0:
        right -= 1
    return right

def createFileToFillSpace(space: Space, right: int) -> tuple[File, int]:
    """
    Creates a new file to fill the given space. The data is taken from the next non-empty file to the left of 
    the given index. The file size is updated.
    The new right index is returned with the created file.
    """
    right = getNextNonEmptyFileFromBack(disk, right)
    currentRight = cast(File, disk[right])
    amount = min(space.size, currentRight.size)
    currentRight.size -= amount
    space.size -= amount
    return (File(currentRight.id, amount), right)

def calculateChecksum(disk: list[File | Space]) -> int:
    """
    Calculates the checksum of the given disk.
    """
    sum = 0
    offset = 0
    for f in disk:
        if isinstance(f, Space):
            offset += f.size
            continue
        for i in range(f.size):
            sum += f.id * (offset + i)
        offset += f.size
    return sum

def findFirstSpace(disk: list[File | Space], size: int, limit: int):
    """
    Finds the left-most space with at least the given size.
    """
    for i in range(limit):
        candidate = disk[i]
        if isinstance(candidate, Space) and candidate.size >= size:
            return i

def solveTask1(disk: list[File | Space]):
    """
    Solves task one by filling all empty spaces from left to right with files from right to left.
    """
    sorted: list[File | Space ] = []
    left = 0
    right = len(disk) - 1
    while left < right:
        currentLeft = disk[left]
        if isinstance(currentLeft, File):
            sorted.append(currentLeft)
        else:
            while currentLeft.size > 0:
                newFile, right = createFileToFillSpace(currentLeft, right)
                sorted.append(newFile)            
        left += 1
    remaining = disk[left].size
    if remaining > 0:
        sorted[-1].size += remaining
    print(calculateChecksum(sorted))

def solveTask2(disk: list[File | Space]):
    """
    Solves the second task by iterating the files from right to left. For each file a suitable free space is found,
    if such a space exists. The file is then moved to that space or left in place.
    """
    right = len(disk) - 1
    moved: set[int] = set()
    while right > 0:
        toMove = disk[right]
        if isinstance(toMove, File):
            i = findFirstSpace(disk, toMove.size, right)
            if i != None and not toMove.id in moved:
                disk[i].size -= toMove.size
                disk[right] = Space(toMove.size)
                disk.insert(i, toMove)
                moved.add(toMove.id)
        right -= 1
    print(calculateChecksum(disk))


disk = readInput("input")
solveTask2(disk)
