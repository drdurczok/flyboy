from ursina import *
from serial import Serial
import datetime, pyautogui

ser = Serial('/dev/ttyUSB0', 115200)

app = Ursina()

audio = Audio('data/sfx/Flappy Bird Theme Song.mp3', loop=True, autoplay=True)
obstacleCounter = 0
obstacleCap = 332

finishSpawned = False

camera.orthographic = True
window.fullscreen = True
window.cog_button.enabled = False
window.fps_counter.enabled = False

window.exit_button.position = (.2, -.2)
window.exit_button.scale = (.4, .1)
window.exit_button.color = color.red
window.exit_button.enabled = False


class Player(Entity):
    def __init__(self):
        super().__init__()
        self.enabled = False
        self.model = "quad"
        self.normalTxt = "data/gfx/FlappyBirdSkinClassic"
        self.texture = self.normalTxt
        self.collider = "box"
        self.color = color.white
        self.loSpeed = 6
        self.hiSpeed = 12
        self.scale = (2.12, 1.5)
        self.position = (1, 1)
        self.horizontalSpeed = self.loSpeed
        self.verticalSpeed = 10
        self.loVol = 0
        self.hiVol = 2
        self.muted = False
        self.always_on_top = True
        self.inRace = "racing"
        self.complete = "finished"
        self.inMenu = "menu"
        self.flag = self.inMenu
        self.currTime = datetime.datetime.now()
        self.prevTime = self.currTime
        self.rate = 160000
        self.ID = '0'
        self.UP = '0'
        self.DOWN = '0'
        self.rTrigger = '0'
        self.lTrigger = '0'
        self.inAnimation = False

    def setSpeed(self, value):
        self.horizontalSpeed = value

    def getSpeed(self):
        return self.horizontalSpeed

    def mute(self, value):
        self.muted = value

    def getVolState(self):
        return self.muted

    def resetPlayer(self, reason):
        global obstacleCounter

        if reason == "dead":
            Collision.enabled = True
            obstacleCounter = 0
            self.position = (0, 0)
            pipes.position = (self.x + 30, random.randint(-15, 15))
        if reason == "end":
            pass

    def input(self, key):
        pass

        if key == 'm':
            if not self.muted:
                self.mute(self.hiVol)
            if self.muted:
                self.mute(self.loVol)

    def update(self):
        background.x = camera.x

        buf = ser.inWaiting()
        if buf >= 8:
            rt = ser.read(size=8)
            rt_decoded = rt.decode("utf-8")

            self.ID = rt_decoded[0:1]
            self.UP = rt_decoded[5]
            self.DOWN = rt_decoded[3]
            self.rTrigger = rt_decoded[2]
            self.lTrigger = rt_decoded[4]

        self.currTime = datetime.datetime.now()

        if (self.currTime - self.prevTime).microseconds >= self.delay:
            if self.UP == '1':
                self.y += self.verticalSpeed * time.dt
            if self.DOWN == '1':
                self.y -= self.verticalSpeed * time.dt
            if self.lTrigger == '1':
                self.horizontalSpeed = self.hiSpeed
                self.color = color.red
            if self.lTrigger == '0':
                self.horizontalSpeed = self.loSpeed
                self.color = color.white
            if self.rTrigger == '0':
                pass
            if self.rTrigger == '1':
                menu.enabled = True
            self.prevTime = self.currTime

        Score.text = f"score: {int(self.x)}"

        if not self.inAnimation:
            self.y += held_keys['w'] * time.dt * self.verticalSpeed
            self.y -= held_keys['s'] * time.dt * self.verticalSpeed

            self.x += time.dt * self.horizontalSpeed
            camera.x = self.x

        if held_keys['w'] and held_keys['s']:
            if self.horizontalSpeed != self.hiSpeed:
                self.setSpeed(self.hiSpeed)
                self.color = color.red
                self.texture = self.normalTxt
        else:
            if self.horizontalSpeed != self.loSpeed:
                self.setSpeed(self.loSpeed)
                self.color = color.white
                self.texture = self.normalTxt

        if self.intersects(pipes.obstacleUp).hit or self.intersects(pipes.obstacleDown).hit:
            self.resetPlayer("dead")

        if Collision.enabled:
            if self.x >= 30:
                Collision.enabled = False

        if self.flag == self.complete:
            self.resetPlayer("end")
            self.flag = self.inRace

        if obstacleCounter == 334:
            self.flag = self.complete
            g.state = g.menuS

        if not self.muted:
            audio.volume = 2
        if self.muted:
            audio.volume = 0


class Pipes(Entity):
    def __init__(self):
        super().__init__()
        self.position = (flappy.x + 30, random.randint(-15, 15))
        self.enabled = False
        self.always_on_top = True
        self.obstacleDown = Entity(model='quad', color=color.green, scale=(8, 40), y=-25, collider='box',
                                   texture='data/gfx/pipe-green', parent=self)
        self.obstacleUp = Entity(model='quad', color=color.green, scale=(8, 40), y=25, collider='box',
                                 texture='data/gfx/pipe-green-up', parent=self)

    def input(self, key):
        pass

    def update(self):
        global obstacleCounter

        if flappy.x >= self.x:
            obstacleCounter += 1
            print(obstacleCounter)
            self.position = (flappy.x + 30, random.randint(-15, 15))


class Finish(Entity):
    def __init__(self):
        super().__init__()
        self.model = 'quad'
        self.collider = 'box'
        self.color = color.black
        self.scale = (3, 100)
        self.position = (flappy.x + 30, 0)
        self.enabled = True

    def update(self):
        global obstacleCounter

        if self.intersects(flappy).hit and g.spawnOnce == 0:
            Ending = Text(text="Congratulations, you've made it to the end",
                          scale=(2, 2),
                          position=(-.4, 0))
            self.enabled = False
            g.spawnOnce = 1

            if Ending:
                destroy(Ending, 2)

        if obstacleCounter != 332:
            self.position = (flappy.x + 30, 0)


class Menu(Entity):
    def __init__(self):
        super().__init__()
        self.enabled = False
        self.spawnOnce = 0
        self.bChoose = 0
        self.currTime = datetime.datetime.now()
        self.prevTime = self.currTime
        self.rate = 160000
        self.ID = '0'
        self.UP = '0'
        self.DOWN = '0'
        self.rTrigger = '0'
        self.lTrigger = '0'

    def input(self, key):
        if key == 'y':
            self.bChoose -= 1
        if key == 'h':
            self.bChoose += 1

    def update(self):
        camera.position = (0, 0)
        background.x, background.y = camera.x, camera.y
        bPlay.enabled = True
        window.exit_button.enabled = True
        flappy.enabled = False
        pipes.enabled = False
        finish.enabled = False
        Score.enabled = False

        if self.enabled and self.spawnOnce == 0:
            Title = Entity(model='quad', scale=(30, 8), position=(0, 10), texture=r"data/gfx/title.png", enabled=True)
            self.spawnOnce = 1

        buf = ser.inWaiting()
        if buf >= 8:
            rt = ser.read(size=8)
            rt_decoded = rt.decode("utf-8")

            self.ID = rt_decoded[0:1]
            self.UP = rt_decoded[5]
            self.DOWN = rt_decoded[3]
            self.rTrigger = rt_decoded[2]
            self.lTrigger = rt_decoded[4]

            self.currTime = datetime.datetime.now()

            if (self.currTime - self.prevTime).microseconds >= self.delay:
                if self.UP == '1':
                    self.bChoose -= '1'
                if self.DOWN == '1':
                    self.bChoose += '1'
                if self.rTrigger == '1':
                    pyautogui.click()

                self.prevTime = self.currTime

        if self.bChoose == 0:
            mouse.x, mouse.y = .005, bPlay.position.y
        if self.bChoose == 1:
            mouse.x, mouse.y = .005, -.25

        print(self.bChoose)

        if self.bChoose <= 0:
            self.bChoose = 0
        if self.bChoose >= 1:
            self.bChoose = 1


class SingleRace(Entity):
    def __init__(self):
        super().__init__()
        self.enabled = False

    def update(self):
        bPlay.enabled = False
        window.exit_button.enabled = False
        flappy.enabled = True
        pipes.enabled = True
        finish.enabled = True
        Score.enabled = True
        menu.spawnOnce = 0


def JustQuit():
    quit()
    return


class GameManager(Entity):
    def __init__(self):
        super().__init__()
        self.infiniteS = "infinite"
        self.multiRaceS = "multi-race"
        self.singleRaceS = "single-race"
        self.menuS = "menuState"
        self.state = self.menuS
        self.runOnce, self.spawnOnce, self.flappyOnce, self.pipesOnce = 0, 0, 0, 0

    def startSRace(self):
        global obstacleCounter

        self.state = self.singleRaceS
        flappy.position = (0, 0)
        pipes.position = (flappy.x + 30, random.randint(-15, 15))
        obstacleCounter = 0
        finish.enabled = True
        self.spawnOnce = 0
        Score.enabled = True
        flappy.flag = flappy.inRace

    def Quit(self):
        i = 0
        i += 1
        quit()
        return i

    def input(self, key):
        if key == '1':
            quit()

    def update(self):

        if self.state == self.menuS:
            menu.enabled = True
            sRace.enabled = False

        if self.state == self.singleRaceS:
            sRace.enabled = True
            menu.enabled = False


flappy = Player()
pipes = Pipes()
sRace = SingleRace()
menu = Menu()
finish = Finish()

g = GameManager()

Score = Text(position=(0, .4),
             scale=(2, 2),
             enabled=False)

Collision = Text(text=f"You Crashed, restarting",
                 scale=(3, 3),
                 enabled=False,
                 position=(-.4, .2))

background = Entity(model="quad",
                    texture="data/gfx/FlappyBirdBG",
                    scale=(100, 50),
                    position=Vec2(0, 0))

bPlay = Button(scale=(.4, .1),
               position=(0, -.1),
               color=color.blue,
               enabled=False,
               on_click=g.startSRace)


def update():
    global obstacleCounter, finishSpawned

    finishSpawned = False


app.run()
