import sys
import time
from math import sqrt
from random import randint
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QPainter, QColor

class PiwithSim(QWidget):
    def __init__(self):
        super().__init__()
        self.pi_estimate = 1
        self.inside_circle = 1
        self.rand_drop_positions = [(300,300)]
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 660, 690)
        self.setWindowTitle("Estimating Pi with the Monte-Carlo Technique")
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        qp.setPen(Qt.black)

        qp.setBrush(QColor.fromRgb(210, 140, 110, a=255))
        qp.drawRect(30, 30, 600, 600)

        qp.setBrush(QColor.fromRgb(120, 170, 220, a=255))
        qp.drawEllipse(30, 30, 600, 600)

        qp.setBrush(QColor.fromRgb(120, 240, 100, a=100))
        for drop in self.rand_drop_positions:
            qp.drawEllipse(drop[0], drop[1], 15, 15)

        qp.drawText(30, 670, "\u03C0 estimate: " + str(self.pi_estimate))
        
        qp.end()

    def next_drop(self):
        drop = (randint(30, 630), randint(30, 630))
        self.rand_drop_positions.append(drop)
        if sqrt((330-drop[0])**2 + (330-drop[1])**2) < 300:
            self.inside_circle += 1
        self.pi_estimate = 4*(self.inside_circle/len(self.rand_drop_positions))
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer = QTimer()
    pi_estimator = PiwithSim()

    timer.timeout.connect(pi_estimator.next_drop)
    timer.start(20)
    app.exec()
    app.quit()