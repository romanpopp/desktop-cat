import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
import random

app = QApplication(sys.argv)
screen = app.primaryScreen()

# Constants
SW = screen.size().width() # Screen Width
SH = screen.size().height() # Screen Height
IW = int(SW * 0.12) # Image Width
IH = int(SH * 0.09) # Image Height
Y_MAX = int(SH * 0.1)
Y_MIN = 0
IMG = '/home/slippinjimmy/Projects/desktop-cat/catevido.png'
RISE_CHANCE = 60 # 1 in x chance of reappearing every minute

class MainWindow(QMainWindow):  

    # Cat position variables
    y_pos = Y_MAX
    x_pos = 0
    is_rising = True
    qlabel = 0

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.qlabel = QLabel(self)

        # Window attributes
        self.setAttribute(Qt.WA_TranslucentBackground, True) # HOLY SHIT
        self.setAttribute(Qt.WA_NoSystemBackground, True) # HOLY SHIT
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

        # Getting image
        pixmap = QPixmap(IMG)
        img = pixmap.scaled(IW, IH, Qt.KeepAspectRatio) # Resizes pixmap
        self.qlabel.setPixmap(img)
        self.qlabel.setGeometry(0, 0, IW, IH)
        self.label = self.qlabel
        self.setGeometry(0, 0, IW, IH)

        # Picking a spot for cat :3
        self.x_pos = random.randrange(0, int(SW * 0.98))

        # Position update methods / QT mainloop
        QTimer.singleShot(10, self.pos_update)
        QTimer.singleShot(10, self.try_to_reappear)
        self.show()


    # Method for updating position, called every 30ms
    def pos_update(self):
        if self.is_rising and self.y_pos > Y_MIN:
            self.y_pos -= 1
        if not self.is_rising and self.y_pos < Y_MAX:
            self.y_pos += 10
        
        self.qlabel.setGeometry(0, self.y_pos, IW, IH)

        # Shrinks window when cat is not visible so that you can click
        if not self.is_rising and self.y_pos >= Y_MAX:
            self.setGeometry(self.x_pos, SH, 1, 1)
        else:
            self.setGeometry(self.x_pos, SH, IW, IH)
        QTimer.singleShot(30, self.pos_update)

    # Method for attempting to reappear
    def try_to_reappear(self):
        if not self.is_rising:
            if random.randint(1, RISE_CHANCE) == 1:
                self.is_rising = True
                self.x_pos = random.randrange(0, int(SW * 0.98))
        QTimer.singleShot(60000, self.try_to_reappear)

    # Click event handler
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            global is_rising
            self.is_rising = False
        if QMouseEvent.button() == Qt.RightButton:
            self.close()
            sys.exit()

w = MainWindow()
sys.exit(app.exec_())
