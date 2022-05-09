from ursina import *
# from gpiozero import Button
from serial import Serial
import datetime

ser = Serial('/dev/ttyUSB0', 115200)

app = Ursina()

states = ['mainMenu', 'gamemodeSelection', 'playerSelection', 'race', 'infinite']
currentState = states[4]

a = Audio('data/sfx/Flappy Bird Theme Song.mp3', loop=True, autoplay=True)
obstacleCounter = 0
obstacleCap = 2
obstacleReset = obstacleCap + 3

finishSpawned = False

textDelDelay = 6
camera.orthographic = True
# window.fullscreen = True
window.cog_button.enabled = False
window.exit_button.enabled = False
window.fps_counter.enabled = False


class Player(Entity):
    def __init__(self):
        super().__init__()
        self.enabled = False
        self.model = "quad"
        self.normalTxt = "data/gfx/FlappyBirdSkinClassic"
        self.texture = self.normalTxt
        self.collider = "box"
        self.color = color.white
        self.scale = (2.12, 1.5)
        self.position = (1, 1)
        self.horizontalSpeed = 6
        self.verticalSpeed = 10
        self.loSpeed = 6
        self.hiSpeed = 12
        self.loVol = 0
        self.hiVol = 2
        self.muted = False
        self.always_on_top = True
        self.inRace = "racing"
        self.complete = "finished"
        self.inMenu = "menu"
        self.flag = self.inMenu
        self.timestamp = datetime.datetime.now()
        #self.bUp = Button(2) # gpio pin 3
        #self.bDown = Button(3) # gpio pin 5

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
        camera.x = self.x
        background.x = self.x
        
        buf = ser.inWaiting()
        print(buf)
        if buf >= 2:
            rt = ser.read(size=2)
            if rt == b'Up':
                self.y += self.verticalSpeed * time.dt
        # rt_decoded = rt.decode("utf-8")

        Score.text = f"score: {int(self.x)}"

        self.y += held_keys['w'] * time.dt * self.verticalSpeed
        self.y -= held_keys['s'] * time.dt * self.verticalSpeed

        #if self.bUp.is_pressed or comm.rt_decoded == 'Up'
        #if self.bDown.is_pressed:
            #self.y -= self.verticalSpeed * time.dt

        if held_keys['w'] and held_keys['s']: #or self.bUp.is_pressed and self.bDown.is_pressed:
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

        if 149 < self.x < obstacleReset * 30:
            self.flag = self.complete
            g.state = g.menuS

        if not self.muted:
            a.volume = 2
        if self.muted:
            a.volume = 0

        self.x += time.dt * self.horizontalSpeed


class Pipes(Entity):
    def __init__(self):
        super().__init__()
        self.position = (flappy.x + 30, random.randint(-15, 15))
        self.enabled = False
        self.obstacleDown = Entity(model='quad', color=color.green, scale=(8, 40), y=-25, collider='box',
                                   texture='data/gfx/pipe-green', parent=self)
        self.obstacleUp = Entity(model='quad', color=color.green, scale=(8, 40), y=25, collider='box',
                                 texture='data/gfx/pipe-green-up', parent=self)

    def input(self, key):
        pass

    def update(self):
        global obstacleCounter

        self.always_on_top = True

        if flappy.x >= self.x:
            self.position = (flappy.x + 30, random.randint(-15, 15))
            obstacleCounter += 1


class Finish(Entity):
    def __init__(self):
        super().__init__()
        self.model = 'quad'
        self.collider = 'box'
        self.color = color.black
        self.scale = (3, 100)
        self.position = (flappy.x + 30, 0)

    def update(self):
        global obstacleCounter

        if self.intersects(flappy).hit and g.spawnOnce == 0:
            Ending = Text(text="Congratulations, you've made it to the end",
                          scale=(2, 2),
                          position=(-.4, 0))
            obstacleCounter = 0
            g.spawnOnce = 1

            if Ending:
                destroy(Ending, 2)
                destroy(self, 3)


class Menu(Entity):
    def __init__(self):
        super().__init__()
        self.enabled = False

    def update(self):
        b.enabled = True
        flappy.enabled = False
        pipes.enabled = False


class SingleRace(Entity):
    def __init__(self):
        super().__init__()
        self.enabled = False

    def update(self):
        b.enabled = False
        flappy.enabled = True
        pipes.enabled = True


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
        self.state = self.singleRaceS
        flappy.flag = flappy.inRace

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

g = GameManager()

Score = Text(position=(0, .4),
             scale=(2, 2))

Collision = Text(text=f"You Crashed, restarting",
                 scale=(3, 3),
                 enabled=False,
                 position=(-.4, .2))

background = Entity(model="quad",
                    texture="data/gfx/FlappyBirdBG",
                    scale=(100, 50))

b = Button(scale=1,
           color=color.blue,
           enabled=False,
           on_click=g.startSRace)


# called every frame
def update():
    global obstacleCounter, finishSpawned

    finishSpawned = False

    if obstacleCounter == obstacleCap and g.runOnce == 0:
        print('spawning finish')
        finish = Finish()
        g.runOnce = 1


app.run()
