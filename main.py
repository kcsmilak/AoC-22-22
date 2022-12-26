inputFilename = "example.txt"


def parseInput():
    instructions = []
    map = []
    with open(inputFilename, "r") as inputFile:
        mapStrings = []
        maxX = 0
        maxY = 0
        mode = 0
        for line in inputFile:

            if len(line.strip()) == 0:
                mode = 1

                maxY = len(mapStrings)

                for y in range(maxY):
                    row = []
                    for x in range(maxX):
                        value = 0
                        mapString = mapStrings[y]
                        if x < len(mapString):
                            c = mapString[x]
                            if c == " ": value = 0
                            if c == ".": value = 1
                            if c == "#": value = 2
                        row.append(value)
                    map.append(row)

                continue

            if 0 == mode:
                mapStrings.append(line)
                if len(line) > maxX: maxX = len(line)
                pass

            if 1 == mode:
                charBuffer = ""
                for char in line:

                    if char == "R" or char == "L":
                        instructions.append(int(charBuffer))
                        charBuffer = ""
                        instructions.append(char)
                        pass
                    else:
                        charBuffer += char
                instructions.append(int(charBuffer))
    return map, instructions


class Map:

    rowRanges = []
    colRanges = []
    
    def __init__(self, map):
        self.map = map
    
        #for i in range(len(map)):
         #   start = min(map[i].index(1), map[i].index(2))
          #  end = max(map[i].index(1,start+1), map[i].index(2,start+1))
           # self.rowRanges.append((start, end))
            
    def print(self, player=None):
        print()
        print(" ", end="")
        for i in range(len(self.map[0])):
            print(i%10, end="")
        print()
        for y in range(len(self.map)):
            print(y%10, end="")
            for x in range(len(self.map[y])):
                cell = self.map[y][x]
                char = " .#"[cell]
                if None != player and player.x == x and player.y == y:
                    char = ">v<^"[player.direction]
    
                print(char, end="")
            print()
        print()

    def getCell(self, x, y):
        return self.map[y][x]

    def start(self):
        return self.map[0].index(1)
        
    def width(self):
        return len(self.map[0])

    def height(self):
        return len(self.map)

    def startRow(self, row):
        return self.map[row][0].index
        
    def endRow(self, row):
        return self.map
        

class Player:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction


def delta(direction):
    if 0 == direction: return 1, 0
    if 1 == direction: return 0, 1
    if 2 == direction: return -1, 0
    return 0, -1


map, instructions = parseInput()
map = Map(map)

player = Player(map.start(),0,0)

map.print(player)

for instruction in instructions:
    print(instruction)

    if "R" == instruction:
        player.direction = (player.direction + 1) % 4
    elif "L" == instruction:
        player.direction = (player.direction - 1) % 4
    else:
        # move the player until they hit a block
        dx, dy = delta(player.direction)

        steps = abs((dx if dx!= 0 else dy) * instruction)
        print("--> d:{0} DX:{1} DY:{2} s:{3}".format(player.direction, dx, dy, steps))
        foundSpace = False

        minX = 0
        minY = 0
        maxX = map.width()
        maxY = map.height()
        targetx, targety = player.x, player.y
        scanx, scany = 0,0
        while (steps > 0):

            nextx = targetx + dx + scanx
            nexty = targety + dy + scany

            # wrap around map edges
            if nextx < minX: nextx = maxX - 1
            if nextx >= maxX: nextx = minX
            if nexty < minY: nexty = maxY - 1
            if nexty >= maxY: nexty = minY

            # get the next cell
            print(maxX, maxY, nextx, nexty)
            nextCell = map.getCell(nextx, nexty)

            if nextCell == 0:
                # keep going, void space in map, doesn't take a step!
                scanx += dx
                scany += dy
                pass
            if nextCell == 1:
                # keep going, empty space in map
                targetx, targety = nextx, nexty
                scanx, scany = 0,0
                steps -= 1
                foundSpace = True
            if nextCell == 2:
                # hit a wall! need to stop
                break
                        
        if foundSpace:
            player.x = targetx
            player.y = targety

            print(steps)
            map.print(player)
            
        
    map.print(player)