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
from Enemy      import Enemy
from Player     import Player
from EXP        import EXP
from LifeInfo   import PlayerIcon, XIcon, Life
from Stage      import Stage

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



# 메인 클래스
class Scene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)

        # hold the set of keys we're pressing
        self.keys_pressed = set()

        # use a timer to get 60Hz refresh (hopefully)  1000 / 16 == 62.5
        self.timer = QBasicTimer()
        self.timer.start(FRAME_TIME_MS, self)

        # bg = QGraphicsRectItem()
        # bg.setRect(-1,-1,SCREEN_WIDTH+2,SCREEN_HEIGHT+2)
        # bg.setBrush(QBrush(Qt.black))

        # BackGround
        self.bg = BackGround()
        self.addItem(self.bg)

        # Stage
        self.stage = Stage()
        self.addItem(self.stage)


        # Player
        self.player = Player()
        self.player.setPos((SCREEN_WIDTH-self.player.pixmap().width())/2,
                           (SCREEN_HEIGHT-self.player.pixmap().height())/2)
        self.addItem(self.player)


        # Player Life
        self.playerIcon = PlayerIcon()
        self.xIcon = XIcon()
        self.life = Life()
        self.playerIcon.setPos(20, 20)
        self.xIcon.setPos(60, 25)
        self.life.setPos(83, 24)
        self.addItem(self.playerIcon)
        self.addItem(self.xIcon)
        self.addItem(self.life)

        # Bullets
        self.bullets = [Bullet(PLAYER_BULLET_X_OFFSETS[0],PLAYER_BULLET_Y),
                        Bullet(PLAYER_BULLET_X_OFFSETS[1],PLAYER_BULLET_Y - 30),
                        Bullet(PLAYER_BULLET_X_OFFSETS[2],PLAYER_BULLET_Y)]
        for b in self.bullets:
            b.setPos(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.addItem(b)


        # Enemies
        self.enemies = [Enemy()]
        self.enemies[0].setPos(SCREEN_WIDTH, 0)
        self.addItem(self.enemies[0])
        self.idx = [0]


        # Execution Point
        self.EXP = EXP()
        self.EXP.score = 8
        self.EXP.setPos(SCREEN_WIDTH-40, 20)
        self.addItem(self.EXP)

        self.EXP1 = EXP()
        self.EXP1.score = 1
        self.EXP1.setPos(SCREEN_WIDTH-60, 20)
        self.addItem(self.EXP1)

        self.view = QGraphicsView(self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.show()
        self.view.setFixedSize(SCREEN_WIDTH,SCREEN_HEIGHT)
        self.setSceneRect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)

        self.ask = AskClose(self)

    def keyPressEvent(self, event):
        self.keys_pressed.add(event.key())
        if event.key() == Qt.Key_Escape:
            self.ask.show()
            

    def keyReleaseEvent(self, event):
        self.keys_pressed.remove(event.key())

    def timerEvent(self, event):
        self.game_update()
        self.update()

    def game_update(self):
        self.stage.game_update(self.EXP1.score*10 + self.EXP.score)
        self.player.game_update(self.keys_pressed, self.enemies[self.idx[0]], self.life)
        if not self.player.IS_DEAD:
            for b in self.bullets:
                b.game_update(self.keys_pressed, self.player)
        self.enemies[self.idx[0]].game_update(self.enemies, self.idx, self.bullets, self.EXP)
        self.EXP.game_update(self.EXP1)
        self.EXP1.game_update(self.EXP1)
        self.life.game_update()

        if self.enemies[-1] == 1:
            self.enemies[-1] = Enemy()
            self.enemies[-1].setPos(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.addItem(self.enemies[-1])




if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = Scene()
    sys.exit(app.exec_())