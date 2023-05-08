from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor
import sys

class TowerofHanoi(QWidget):
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
        qp = QPainter()
        qp.begin(self)
        self.drawTowers(qp)
        qp.end()

    def drawTowers(self, qp):
        for i in range(3):
            qp.setPen(Qt.black)
            qp.setBrush(Qt.black)
            pole_width = self.appWidth/(self.num_disks*16)
            qp.drawRect((self.appWidth/6)*(i*2+1)-pole_width/2, self.appHeight/5, pole_width, self.appHeight-self.appHeight/5)
            for j in range(len(self.towers[i])):
                disk = self.towers[i][j]
                #color = QtGui.QColor.fromHsl(0, 255 - disk * (255 // self.num_disks), 128)
                color = QColor.fromHsl(disk*(255//self.num_disks), 255, 120)
                qp.setBrush(color)
                diskh = self.appWidth/(3*self.num_disks)
                diskw = disk*(self.appWidth/(3*self.num_disks))
                diskx = (i*2)*(self.appWidth/6)+((self.num_disks-disk)*(self.appWidth/(6*self.num_disks)))
                disky = self.appHeight-(j+1)*diskh
                qp.drawRect(diskx, disky, diskw, diskh)
    
    def show_initial_state(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer = QTimer()
    toh = TowerofHanoi(num_disks = 30, moves = [], source = 1, target = 0)
    
    timer.timeout.connect(toh.show_initial_state)
    timer.start(60000)
    app.exec()
    app.shutdown()