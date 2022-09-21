from random import randint
import copy



class Side:

    def __init__(self, color, face, gears):
        self.color = color
        self.face = face
        self.topGear = gears[0]
        self.rightGear = gears[1]
        self.bottomGear = gears[2]
        self.leftGear = gears[3]

    def __eq__(self, other):
        equal = True
        for i in range(9):
            if self.face[i] != other.face[i]:
                equal = False
        return equal

    def isolatedRotateToLeft(self):
        temp = [None] * 9
        temp[0] = self.face[2]
        temp[1] = self.face[5]
        temp[2] = self.face[8]
        temp[3] = self.face[1]
        temp[4] = self.face[4]
        temp[5] = self.face[7]
        temp[6] = self.face[0]
        temp[7] = self.face[3]
        temp[8] = self.face[6]

        for i in range(9):
            self.face[i] = temp[i]

    def isolatedRotateToRight(self):
        temp = [None] * 9
        temp[0] = self.face[6]
        temp[1] = self.face[3]
        temp[2] = self.face[0]
        temp[3] = self.face[7]
        temp[4] = self.face[4]
        temp[5] = self.face[1]
        temp[6] = self.face[8]
        temp[7] = self.face[5]
        temp[8] = self.face[2]

        for i in range(9):
            self.face[i] = temp[i]


class Gear:
    def __init__(self, color1, color2):
        self.color1 = color1
        self.color2 = color2
        self.rotation = 0

    # counterclockwise rotation
    def rotateL(self):
        self.rotation -= 1

    # clockwise rotation
    def rotateR(self):
        self.rotation += 1

    def PrintHorizGear(self, end):
        rot = self.rotation % 6
        if end == True:
            if rot == 0:
                print(self.color1[0], "|", self.color2[0], end="")
            elif rot == 1:
                print(self.color1[0], "\\", self.color2[0], end="")
            elif rot == 2:
                print(self.color2[0], "/", self.color1[0], end="")
            elif rot == 3:
                print(self.color2[0], "|", self.color1[0], end="")
            elif rot == 4:
                print(self.color2[0], "\\", self.color1[0], end="")
            elif rot == 5:
                print(self.color1[0], "/", self.color2[0], end="")
        else:
            if rot == 0:
                print(self.color1[0], "|", self.color2[0])
            elif rot == 1:
                print(self.color1[0], "\\", self.color2[0])
            elif rot == 2:
                print(self.color2[0], "/", self.color1[0])
            elif rot == 3:
                print(self.color2[0], "|", self.color1[0])
            elif rot == 4:
                print(self.color2[0], "\\", self.color1[0])
            elif rot == 5:
                print(self.color1[0], "/", self.color2[0])

    def printVertGear(self, end):
        rot = self.rotation % 6
        if end == True:
            if rot == 0:
                print(self.color1[0], "|", self.color2[0], end="")
            elif rot == 1:
                print(self.color1[0], "/", self.color2[0], end="")
            elif rot == 2:
                print(self.color1[0], "\\", self.color2[0], end="")
            elif rot == 3:
                print(self.color2[0], "|", self.color1[0], end="")
            elif rot == 4:
                print(self.color2[0], "/", self.color1[0], end="")
            elif rot == 5:
                print(self.color2[0], "\\", self.color1[0], end="")
        else:
            if rot == 0:
                print(self.color1[0], "|", self.color2[0])
            elif rot == 1:
                print(self.color1[0], "/", self.color2[0])
            elif rot == 2:
                print(self.color1[0], "\\", self.color2[0])
            elif rot == 3:
                print(self.color2[0], "|", self.color1[0])
            elif rot == 4:
                print(self.color2[0], "/", self.color1[0])
            elif rot == 5:
                print(self.color2[0], "\\", self.color1[0])


class Gearball:

    def __init__(self):

        # to keep track of last moves to avoid loops
        self.lastMove = []

        #depth, parent for astar
        self.depth = 0
        self.parent = None

        # initialize gears
        # top/left color, bottom/right color
        bp = Gear('purple', 'blue')
        br = Gear('blue', 'red')
        ob = Gear('orange', 'blue')
        gr = Gear('red', 'green')
        og = Gear('orange', 'green')
        gy = Gear('green', 'yellow')
        gp = Gear('green', 'purple')
        ry = Gear('red', 'yellow')
        yp = Gear('yellow', 'purple')
        by = Gear('blue', 'yellow')
        ro = Gear('orange', 'red')
        po = Gear('orange', 'purple')

        # initialize sides
        self.top = Side('blue', ['b', 'b', 'b', 'b', 'b',
                                 'b', 'b', 'b', 'b'], [bp, by, br, ob])
        self.bottom = Side('green', ['g', 'g', 'g', 'g', 'g',
                                     'g', 'g', 'g', 'g'], [gr, gy, gp, og])
        self.front = Side('red', ['r', 'r', 'r', 'r', 'r',
                                  'r', 'r', 'r', 'r'], [br, ry, gr, ro])
        self.left = Side('orange', ['o', 'o', 'o', 'o', 'o',
                                    'o', 'o', 'o', 'o'], [ob, ro, og, po])
        self.right = Side('yellow', ['y', 'y', 'y', 'y', 'y',
                                     'y', 'y', 'y', 'y'], [by, yp, gy, ry])
        self.back = Side('purple', ['p', 'p', 'p', 'p', 'p',
                                    'p', 'p', 'p', 'p'], [gp, yp, bp, po])

        self.sideList = [self.top, self.left, self.front,
                         self.right, self.bottom, self.back]

    def __eq__(self, other):
        equal = True
        if type(other) == type(None):
            equal = False
            return equal

        for i in range(6):
            if self.sideList[i] != other.sideList[i]:
                equal = False
        return equal

    def __lt__(self, other):
        h_val1 = self.eval() + self.depth
        h_val2 = other.eval() + other.depth
        if h_val1 < h_val2:
            return True
        else:
            return False

    def copy(self):
        new = copy.deepcopy(self)
        return new

    # rotates the left and right clockwise
    def rotateLeftR(self):

        self.lastMove.append('LR')
        self.left.isolatedRotateToRight()
        self.right.isolatedRotateToRight()
        # left side
        # shift gears
        tempgear = self.left.topGear
        tempgear2 = self.left.bottomGear
        self.left.topGear = self.left.leftGear
        self.left.bottomGear = self.left.rightGear
        self.left.rightGear = tempgear
        self.left.leftGear = tempgear2
        # make bordering side gears match
        self.front.leftGear = self.left.rightGear
        self.top.leftGear = self.left.topGear
        self.bottom.leftGear = self.left.bottomGear
        self.back.leftGear = self.left.leftGear
        # rotate corners
        temp = self.top.face[0]
        temp2 = self.top.face[3]
        temp3 = self.top.face[6]
        self.top.face[0] = self.back.face[0]
        self.top.face[3] = self.back.face[3]
        self.top.face[6] = self.back.face[6]
        self.back.face[0] = self.bottom.face[0]
        self.back.face[3] = self.bottom.face[3]
        self.back.face[6] = self.bottom.face[6]
        self.bottom.face[0] = self.front.face[0]
        self.bottom.face[3] = self.front.face[3]
        self.bottom.face[6] = self.front.face[6]
        self.front.face[0] = temp
        self.front.face[3] = temp2
        self.front.face[6] = temp3

        # right side
        # shift gears
        tempgear = self.right.topGear
        tempgear2 = self.right.bottomGear
        self.right.topGear = self.right.leftGear
        self.right.bottomGear = self.right.rightGear
        self.right.rightGear = tempgear
        self.right.leftGear = tempgear2
        # make bordering side gears match
        self.front.rightGear = self.right.leftGear
        self.top.rightGear = self.right.topGear
        self.bottom.rightGear = self.right.bottomGear
        self.back.rightGear = self.right.rightGear
        # rotate corners
        temp = self.top.face[2]
        temp2 = self.top.face[5]
        temp3 = self.top.face[8]
        self.top.face[2] = self.front.face[2]
        self.top.face[5] = self.front.face[5]
        self.top.face[8] = self.front.face[8]
        self.front.face[2] = self.bottom.face[2]
        self.front.face[5] = self.bottom.face[5]
        self.front.face[8] = self.bottom.face[8]
        self.bottom.face[2] = self.back.face[2]
        self.bottom.face[5] = self.back.face[5]
        self.bottom.face[8] = self.back.face[8]
        self.back.face[2] = temp
        self.back.face[5] = temp2
        self.back.face[8] = temp3

        # rotate gears
        self.front.topGear.rotateL()
        self.front.bottomGear.rotateL()
        self.back.topGear.rotateL()
        self.back.bottomGear.rotateL()

        return self

    # rotates the top and bottom clockwise
    def rotateTopR(self):
        self.lastMove.append('TR')
        self.top.isolatedRotateToRight()
        self.bottom.isolatedRotateToRight()

        tempgear = self.top.topGear
        tempgear2 = self.top.rightGear
        self.top.topGear = self.top.leftGear
        self.top.leftGear = self.top.bottomGear
        self.top.bottomGear = tempgear2
        self.top.rightGear = tempgear

        self.left.topGear = self.top.leftGear
        self.back.bottomGear = self.top.topGear
        self.right.topGear = self.top.rightGear
        self.front.topGear = self.top.bottomGear

        temp = self.right.face[0]
        temp2 = self.right.face[1]
        temp3 = self.right.face[2]
        self.right.face[0] = self.back.face[8]
        self.right.face[1] = self.back.face[7]
        self.right.face[2] = self.back.face[6]
        self.back.face[6] = self.left.face[2]
        self.back.face[7] = self.left.face[1]
        self.back.face[8] = self.left.face[0]
        self.left.face[0] = self.front.face[0]
        self.left.face[1] = self.front.face[1]
        self.left.face[2] = self.front.face[2]
        self.front.face[0] = temp
        self.front.face[1] = temp2
        self.front.face[2] = temp3

        self.front.leftGear.rotateL()
        self.front.rightGear.rotateL()

        tempgear = self.bottom.topGear
        tempgear2 = self.bottom.rightGear
        self.bottom.topGear = self.bottom.leftGear
        self.bottom.leftGear = self.bottom.bottomGear
        self.bottom.bottomGear = tempgear2
        self.bottom.rightGear = tempgear

        self.left.bottomGear = self.bottom.leftGear
        self.right.bottomGear = self.bottom.rightGear
        self.back.topGear = self.bottom.bottomGear
        self.front.bottomGear = self.bottom.topGear

        temp = self.right.face[6]
        temp2 = self.right.face[7]
        temp3 = self.right.face[8]
        self.right.face[6] = self.front.face[6]
        self.right.face[7] = self.front.face[7]
        self.right.face[8] = self.front.face[8]
        self.front.face[6] = self.left.face[6]
        self.front.face[7] = self.left.face[7]
        self.front.face[8] = self.left.face[8]
        self.left.face[6] = self.back.face[2]
        self.left.face[7] = self.back.face[1]
        self.left.face[8] = self.back.face[0]
        self.back.face[0] = temp3
        self.back.face[1] = temp2
        self.back.face[2] = temp

        self.back.leftGear.rotateL()
        self.back.rightGear.rotateL()

        return self

    # rotates front and back clockwise
    def rotateFrontR(self):
        self.lastMove.append('FR')
        self.front.isolatedRotateToRight()
        self.back.isolatedRotateToRight()

        tempgear = self.front.topGear
        self.front.topGear = self.front.leftGear
        self.front.leftGear = self.front.bottomGear
        self.front.bottomGear = self.front.rightGear
        self.front.rightGear = tempgear

        self.right.leftGear = self.front.rightGear
        self.top.bottomGear = self.front.topGear
        self.left.rightGear = self.front.leftGear
        self.bottom.topGear = self.front.bottomGear

        # rotate slices of sides touching front
        temp = self.top.face[6]
        temp2 = self.top.face[7]
        temp3 = self.top.face[8]
        self.top.face[6] = self.left.face[8]
        self.top.face[7] = self.left.face[5]
        self.top.face[8] = self.left.face[2]
        self.left.face[2] = self.bottom.face[0]
        self.left.face[5] = self.bottom.face[1]
        self.left.face[8] = self.bottom.face[2]
        self.bottom.face[0] = self.right.face[6]
        self.bottom.face[1] = self.right.face[3]
        self.bottom.face[2] = self.right.face[0]
        self.right.face[0] = temp
        self.right.face[3] = temp2
        self.right.face[6] = temp3

        tempgear = self.back.topGear
        self.back.topGear = self.back.leftGear
        self.back.leftGear = self.back.bottomGear
        self.back.bottomGear = self.back.rightGear
        self.back.rightGear = tempgear

        self.left.leftGear = self.back.leftGear
        self.top.topGear = self.back.bottomGear
        self.right.rightGear = self.back.rightGear
        self.bottom.bottomGear = self.back.topGear

        # rotate slices of sides touching back face
        temp = self.top.face[0]
        temp2 = self.top.face[1]
        temp3 = self.top.face[2]
        self.top.face[0] = self.right.face[2]
        self.top.face[1] = self.right.face[5]
        self.top.face[2] = self.right.face[8]
        self.right.face[2] = self.bottom.face[8]
        self.right.face[5] = self.bottom.face[7]
        self.right.face[8] = self.bottom.face[6]
        self.bottom.face[6] = self.left.face[0]
        self.bottom.face[7] = self.left.face[3]
        self.bottom.face[8] = self.left.face[6]
        self.left.face[0] = temp3
        self.left.face[3] = temp2
        self.left.face[6] = temp

        self.top.leftGear.rotateL()
        self.top.rightGear.rotateL()
        self.bottom.leftGear.rotateL()
        self.bottom.rightGear.rotateL()

        return self

    # rotates left and right counterclockwise
    def rotateLeftL(self):
        self.lastMove.append('LL')
        self.left.isolatedRotateToLeft()
        self.right.isolatedRotateToLeft()
        # left side
        # shift gears
        tempgear = self.left.topGear
        tempgear2 = self.left.bottomGear
        self.left.topGear = self.left.rightGear
        self.left.bottomGear = self.left.leftGear
        self.left.rightGear = tempgear2
        self.left.leftGear = tempgear
        # make bordering side gears match
        self.front.leftGear = self.left.rightGear
        self.top.leftGear = self.left.topGear
        self.bottom.leftGear = self.left.bottomGear
        self.back.leftGear = self.left.leftGear
        # rotate corners
        temp = self.bottom.face[0]
        temp2 = self.bottom.face[3]
        temp3 = self.bottom.face[6]
        self.bottom.face[0] = self.back.face[0]
        self.bottom.face[3] = self.back.face[3]
        self.bottom.face[6] = self.back.face[6]
        self.back.face[0] = self.top.face[0]
        self.back.face[3] = self.top.face[3]
        self.back.face[6] = self.top.face[6]
        self.top.face[0] = self.front.face[0]
        self.top.face[3] = self.front.face[3]
        self.top.face[6] = self.front.face[6]
        self.front.face[0] = temp
        self.front.face[3] = temp2
        self.front.face[6] = temp3

        # right side
        # shift gears
        tempgear = self.right.topGear
        tempgear2 = self.right.bottomGear
        self.right.topGear = self.right.rightGear
        self.right.bottomGear = self.right.leftGear
        self.right.rightGear = tempgear2
        self.right.leftGear = tempgear
        # make bordering side gears match
        self.front.rightGear = self.right.leftGear
        self.top.rightGear = self.right.topGear
        self.bottom.rightGear = self.right.bottomGear
        self.back.rightGear = self.right.rightGear
        # rotate corners
        temp = self.top.face[2]
        temp2 = self.top.face[5]
        temp3 = self.top.face[8]
        self.top.face[2] = self.back.face[2]
        self.top.face[5] = self.back.face[5]
        self.top.face[8] = self.back.face[8]
        self.back.face[2] = self.bottom.face[2]
        self.back.face[5] = self.bottom.face[5]
        self.back.face[8] = self.bottom.face[8]
        self.bottom.face[2] = self.front.face[2]
        self.bottom.face[5] = self.front.face[5]
        self.bottom.face[8] = self.front.face[8]
        self.front.face[2] = temp
        self.front.face[5] = temp2
        self.front.face[8] = temp3

        # rotate gears
        self.front.topGear.rotateR()
        self.front.bottomGear.rotateR()
        self.back.topGear.rotateR()
        self.back.bottomGear.rotateR()

        return self

    # rotates top and bottom counterclockwise
    def rotateTopL(self):
        self.lastMove.append('TL')
        self.top.isolatedRotateToLeft()
        self.bottom.isolatedRotateToLeft()

        tempgear = self.top.leftGear
        tempgear2 = self.top.rightGear
        self.top.leftGear = self.top.topGear
        self.top.topGear = self.top.rightGear
        self.top.rightGear = self.top.bottomGear
        self.top.bottomGear = tempgear

        self.left.topGear = self.top.leftGear
        self.back.bottomGear = self.top.topGear
        self.right.topGear = self.top.rightGear
        self.front.topGear = self.top.bottomGear

        temp = self.front.face[0]
        temp2 = self.front.face[1]
        temp3 = self.front.face[2]
        self.front.face[0] = self.left.face[0]
        self.front.face[1] = self.left.face[1]
        self.front.face[2] = self.left.face[2]
        self.left.face[0] = self.back.face[8]
        self.left.face[1] = self.back.face[7]
        self.left.face[2] = self.back.face[6]
        self.back.face[6] = self.right.face[2]
        self.back.face[7] = self.right.face[1]
        self.back.face[8] = self.right.face[0]
        self.right.face[0] = temp
        self.right.face[1] = temp2
        self.right.face[2] = temp3

        self.front.leftGear.rotateR()
        self.front.rightGear.rotateR()

        tempgear = self.bottom.topGear
        tempgear2 = self.bottom.rightGear
        self.bottom.rightGear = self.bottom.bottomGear
        self.bottom.bottomGear = self.bottom.leftGear
        self.bottom.topGear = tempgear2
        self.bottom.leftGear = tempgear

        self.left.bottomGear = self.bottom.leftGear
        self.right.bottomGear = self.bottom.rightGear
        self.back.topGear = self.bottom.bottomGear
        self.front.bottomGear = self.bottom.topGear

        temp = self.front.face[6]
        temp2 = self.front.face[7]
        temp3 = self.front.face[8]
        self.front.face[6] = self.right.face[6]
        self.front.face[7] = self.right.face[7]
        self.front.face[8] = self.right.face[8]
        self.right.face[6] = self.back.face[2]
        self.right.face[7] = self.back.face[1]
        self.right.face[8] = self.back.face[0]
        self.back.face[0] = self.left.face[8]
        self.back.face[1] = self.left.face[7]
        self.back.face[2] = self.left.face[6]
        self.left.face[6] = temp
        self.left.face[7] = temp2
        self.left.face[8] = temp3

        self.back.leftGear.rotateR()
        self.back.rightGear.rotateR()

        return self

    # rotates front and back counterclockwise
    def rotateFrontL(self):
        self.lastMove.append('FL')
        self.front.isolatedRotateToLeft()
        self.back.isolatedRotateToLeft()

        tempgear = self.front.topGear
        self.front.topGear = self.front.rightGear
        self.front.rightGear = self.front.bottomGear
        self.front.bottomGear = self.front.leftGear
        self.front.leftGear = tempgear

        self.right.leftGear = self.front.rightGear
        self.top.bottomGear = self.front.topGear
        self.left.rightGear = self.front.leftGear
        self.bottom.topGear = self.front.bottomGear

        temp = self.top.face[6]
        temp2 = self.top.face[7]
        temp3 = self.top.face[8]
        self.top.face[6] = self.right.face[0]
        self.top.face[7] = self.right.face[3]
        self.top.face[8] = self.right.face[6]
        self.right.face[0] = self.bottom.face[2]
        self.right.face[3] = self.bottom.face[1]
        self.right.face[6] = self.bottom.face[0]
        self.bottom.face[0] = self.left.face[2]
        self.bottom.face[1] = self.left.face[5]
        self.bottom.face[2] = self.left.face[8]
        self.left.face[2] = temp3
        self.left.face[5] = temp2
        self.left.face[8] = temp

        tempgear = self.back.topGear
        self.back.topGear = self.back.rightGear
        self.back.rightGear = self.back.bottomGear
        self.back.bottomGear = self.back.leftGear
        self.back.leftGear = tempgear

        self.left.leftGear = self.back.leftGear
        self.top.topGear = self.back.bottomGear
        self.right.rightGear = self.back.rightGear
        self.bottom.bottomGear = self.back.topGear

        temp = self.top.face[0]
        temp2 = self.top.face[1]
        temp3 = self.top.face[2]
        self.top.face[0] = self.left.face[6]
        self.top.face[1] = self.left.face[3]
        self.top.face[2] = self.left.face[0]
        self.left.face[0] = self.bottom.face[6]
        self.left.face[3] = self.bottom.face[7]
        self.left.face[6] = self.bottom.face[8]
        self.bottom.face[6] = self.right.face[8]
        self.bottom.face[7] = self.right.face[5]
        self.bottom.face[8] = self.right.face[2]
        self.right.face[2] = temp
        self.right.face[5] = temp2
        self.right.face[8] = temp3

        self.top.leftGear.rotateR()
        self.top.rightGear.rotateR()
        self.bottom.leftGear.rotateR()
        self.bottom.rightGear.rotateR()

        return self

    # randomizer
    def randomMoves(self, number):
        movesList = ["LR", "LL", "TR", "TL", "FR", "FL"]
        for i in range(number):
            option = randint(0, 5)
            # check that the next move doesn't undo the last one
            moveCheck(self, movesList, option)

            if (option == 0):
                self.rotateLeftR()
            elif (option == 1):
                self.rotateLeftL()
            elif (option == 2):
                self.rotateTopR()
            elif option == 3:
                self.rotateTopL()
            elif option == 4:
                self.rotateFrontR()
            elif option == 5:
                self.rotateFrontL()
        return self

    # print rep of ball
    def printBall(self):
        # top
        print("\t\t\t", end="")
        self.top.topGear.printVertGear(False)
        print("\t\t\t", self.top.face[0], self.top.face[1], self.top.face[2])
        print("\t\t  ", end="")
        self.top.leftGear.PrintHorizGear(True)
        print(" ", self.top.face[3], self.top.face[4],
              self.top.face[5], " ", end="")
        self.top.rightGear.PrintHorizGear(False)
        print("\t\t\t", self.top.face[6], self.top.face[7], self.top.face[8])
        print("\t\t\t", end="")
        self.top.bottomGear.printVertGear(False)

        # left, front, right
        print("\t", self.left.face[0],
              self.left.face[1], self.left.face[2], end="")
        print("\t\t", self.front.face[0],
              self.front.face[1], self.front.face[2], end="")
        print("\t\t", self.right.face[0],
              self.right.face[1], self.right.face[2])
        print("\t", self.left.face[3], self.left.face[4],
              self.left.face[5], " ", end="")
        self.left.rightGear.PrintHorizGear(True)
        print("\t", self.front.face[3], self.front.face[4],
              self.front.face[5], " ", end="")
        self.front.rightGear.PrintHorizGear(True)
        print("\t", self.right.face[3],
              self.right.face[4], self.right.face[5], " ")
        print("\t", self.left.face[6],
              self.left.face[7], self.left.face[8], end="")
        print("\t\t", self.front.face[6],
              self.front.face[7], self.front.face[8], end="")
        print("\t\t", self.right.face[6],
              self.right.face[7], self.right.face[8])

        # bottom
        print("\t\t\t", end="")
        self.bottom.topGear.printVertGear(False)
        print("\t\t\t", self.bottom.face[0],
              self.bottom.face[1], self.bottom.face[2])
        print("\t\t  ", end="")
        self.bottom.leftGear.PrintHorizGear(True)
        print(" ", self.bottom.face[3], self.bottom.face[4],
              self.bottom.face[5], " ", end="")
        self.bottom.rightGear.PrintHorizGear(False)
        print("\t\t\t", self.bottom.face[6],
              self.bottom.face[7], self.bottom.face[8])
        print("\t\t\t", end="")
        self.bottom.bottomGear.printVertGear(False)

        # back
        print("\t\t\t", self.back.face[0],
              self.back.face[1], self.back.face[2])
        print("\t\t  ", end="")
        self.back.leftGear.PrintHorizGear(True)
        print(" ", self.back.face[3], self.back.face[4],
              self.back.face[5], " ", end="")
        self.back.rightGear.PrintHorizGear(False)
        print("\t\t\t", self.back.face[6],
              self.back.face[7], self.back.face[8])
        print("\t\t\t")

    def eval(self):
        solvedBall = Gearball()
        if self == solvedBall:
            return 0
        else:
            return 1


def moveCheck(ball, movesList, currentOption):
    if ball.lastMove != []:
        if movesList[currentOption][0] == "L":
            if ball.lastMove[-1][1] != movesList[currentOption][1]:
                currentOption = randint(0, 5)
            elif movesList[currentOption + 1][0] == "T":
                if ball.lastMove[-1][1] != movesList[currentOption][1]:
                    currentOption = randint(0, 5)
            elif movesList[currentOption + 1][0] == "F":
                if ball.lastMove[-1][1] != movesList[currentOption][1]:
                    currentOption = randint(0, 5)
    return currentOption
