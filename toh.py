import sys
from math import sqrt
from multiprocessing import Process
from PySide6 import QtGui, QtCore, QtWidgets

class TowerOfHanoi(QtWidgets.QWidget):
    def __init__(self, num_disks, moves, source, target):
        super().__init__()
        self.num_disks = num_disks
        self.moves = moves
        self.towers = [[], [], []]
        self.towers[source] = [i for i in range(num_disks, 0, -1)]
        self.current_move = 0
        self.source = source
        self.target = target
        self.appWidth = 400*num_disks/5
        self.appHeight = 200*num_disks/5
        if self.appWidth > 1280:
            self.appWidth = 1270
        if self.appHeight > 680:
            self.appHeight = 680
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, self.appWidth, self.appHeight)
        self.setWindowTitle('Tower of Hanoi')
        self.show()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawTowers(qp)
        qp.end()

    def drawTowers(self, qp):
        for i in range(3):
            qp.setPen(QtCore.Qt.black)
            qp.setBrush(QtCore.Qt.black)
            pole_width = self.appWidth/(self.num_disks*16)
            qp.drawRect((self.appWidth/6)*(i*2+1)-pole_width/2, self.appHeight/5, pole_width, self.appHeight-self.appHeight/5)
            for j in range(len(self.towers[i])):
                disk = self.towers[i][j]
                #color = QtGui.QColor.fromHsl(0, 255 - disk * (255 // self.num_disks), 128)
                color = QtGui.QColor.fromHsl(disk*(255//self.num_disks), 255, 120)
                qp.setBrush(color)
                diskh = self.appWidth/(3*self.num_disks)
                diskw = disk*(self.appWidth/(3*self.num_disks))
                diskx = (i*2)*(self.appWidth/6)+((self.num_disks-disk)*(self.appWidth/(6*self.num_disks)))
                disky = self.appHeight-(j+1)*diskh
                qp.drawRect(diskx, disky, diskw, diskh)
                
    def nextMove(self):
        if self.current_move < len(self.moves):
            move = self.moves[self.current_move]
            disk = self.towers[move[0]].pop()
            self.towers[move[1]].append(disk)
            self.current_move += 1
            self.update()

def visualizer(num_disks, moves, source, target):
    app = QtWidgets.QApplication(sys.argv)
    toh = TowerOfHanoi(num_disks, moves, source, target)
    timer = QtCore.QTimer()
    timer.timeout.connect(toh.nextMove)
    timer.start(500)
    app.exec()
    app.shutdown()

def move(stacks, source, target):
    new_stacks = stacks
    disk = new_stacks[source].pop(0)
    new_stacks[target].insert(0,disk)
    return new_stacks

def solver(start, source, target, moves):
    if start[source] == 1:
        start[source] -= 1
        start[target] += 1
        moves.append((source, target))
        return (start, moves)
    else:
        start[source] -= 1
        target = 3 - (source+target)
        start, moves = solver(start, source, target, moves)
        start[source] += 1 
        target = 3 - (source+target)
        start, moves = solver(start, source, target, moves)
        start[target] -= 1
        source = 3 - (source+target)
        start, moves = solver(start, source, target, moves)
        start[target] += 1
        return (start, moves)

def islegal(stacks):
    all_disks = [i for i in range(num_disks)]
    order_correct = all(all(stacks[i][j] < stacks[i][j+1] for j in range(len(stacks[i])-1)) for i in range(len(stacks)))
    disks_in_state = sorted([disk for stack in stacks for disk in stack])
    disks_complete = (disks_in_state == all_disks)
    return (order_correct & disks_complete)

def iscomplete(stacks):
    all_disks = [i for i in range(num_disks)]
    return stacks[target] == all_disks

def run_solution(solver, start, source, target):
    moves = solver(start, source, target, [])[1]
    all_states = [[[],[],[]]]*(len(moves)+1)
    all_disks = [i for i in range(num_disks)]
    all_states[0][source] = all_disks
    for i, m in enumerate(moves):
        try:
            all_states[i+1] = move(all_states[i], m[0], m[1])
        except ValueError:
            all_states.append(None)
    return (all_states, moves)

def check_solution(solver, start, source, target):
    try:
        all_states, moves = run_solution(solver, start, source, target)
        all_legal = all(islegal(s) for s in all_states)
        complete = iscomplete(all_states[-1])
        return (all_legal and complete, moves)
    except ValueError:
        return False

if __name__ == '__main__':
    retry = True
    a, b, c, d = 1, 1, 1, 0

    num_disks = 0
    while(True):
        try:
            source = int(input("Source pole: "))
            target = int(input("Target pole: "))
            if ((source not in [0,1,2]) or (target not in [0,1,2])):
                raise ValueError()
            break
        except:
            print("Valid inputs are only 0, 1 and 2. Try again")
            continue

    while(retry):
        all_disks = [i for i in range(num_disks)]
        if a:
            try:
                num_disks = int(input("Enter the number of disks to solve for (or 0 to exit): "))
                if num_disks < 0:
                    raise ValueError()
                if not(num_disks):
                    break
                all_disks = [i for i in range(num_disks)]
            except:
                a, b, c, d = 0, 0, 0, 1
        if b:
            starting_stacks = [0, 0, 0]
            starting_stacks[source] = num_disks
            correct, moves = check_solution(solver, starting_stacks, source, target)
            if correct:
                #print('Moves:', moves)
                p = Process(target=visualizer, args=(num_disks, moves, source, target))
                p.start()
                p.join()
                p.terminate()
                del p
                if num_disks >= 3:
                    print("Congratulations, your solution works!")
                else:
                    print("Your solution works for the {} disks. Input 8 or more to see if it works for those".format(num_disks))
            else:
                print("The 'solver' function doesn't work yet. Keep working on it!")
        if c:
            try:
                num_disks = int(input("You may enter a different number this time, or enter 0 to exit: "))
                if num_disks < 0:
                    raise ValueError()
                if not(num_disks):
                    break
                a, b, c, d = 0, 1, 1, 0
            except:
                a, b, c, d = 0, 0, 0, 1
        if d:
            try:
                num_disks = int(input("Valid inputs are WHOLE NUMBERS ONLY. Try again or input 0 to exit: "))
                if num_disks < 0:
                    raise ValueError()
                if not(num_disks):
                    break
                a, b, c, d = 0, 1, 1, 0
            except:
                a, b, c, d = 0, 0, 0, 1