import sys
import random
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import (
    Qt,
    QBasicTimer
)
from PyQt5.QtGui import (
    QBrush,
    QPixmap
)
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QGridLayout,
    QLabel,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView
)

from AskClose   import AskClose
from BackGround import BackGround
from Bullet     import Bullet
from FoodInfo      import FoodInfo
from Player     import Player

SCREEN_WIDTH            = 800
SCREEN_HEIGHT           = 600
PLAYER_SPEED            = 3   # pix/frame
PLAYER_BULLET_X_OFFSETS = [0, 45, 90]
PLAYER_BULLET_Y         = 15
BULLET_SPEED            = 10  # pix/frame
BULLET_FRAMES           = 50
FRAME_TIME_MS           = 16  # ms/frame
# frame * ms/frame = ms  =>  frame(y) = whole_ms(x) / frame_ms(16)
ENEMY_SPONE_X           = 800
ENEMY_SPONE_Y           = 600
ENEMY_FRAMES            = 500

path = '/home/user/PycharmProjects/AD_Project/Hyewon/'

class Select(QGraphicsPixmapItem):

    def __init__(self, imagePath, parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap(path + imagePath))
        self.select = ""
    
    def game_update(self, bullets):
        for i in range(len(bullets)):
            if (self.x() <= bullets[i].x() <= self.x() + self.pixmap().width() and self.y() <= bullets[i].y() <= self.y() + self.pixmap().width()):
                bullets[0].setPos(SCREEN_WIDTH, SCREEN_HEIGHT)
                bullets[1].setPos(SCREEN_WIDTH, SCREEN_HEIGHT)
                bullets[2].setPos(SCREEN_WIDTH, SCREEN_HEIGHT)
                return True