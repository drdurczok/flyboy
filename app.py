from ursina import *
import datetime

app = Ursina()

states = ['mainMenu', 'gamemodeSelection', 'playerSelection', 'race', 'infinite']
currentState = states[4]

a = Audio('data/sfx/Flappy Bird Theme Song.mp3', loop=True, autoplay=True)
obstacleCounter = 0
obstacleCap = 2
obstacleReset = obstacleCap + 3

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
            Ending.enabled = True

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
        print('player')

        Score.text = f"score: {int(self.x)}"

        self.y += held_keys['w'] * time.dt * self.verticalSpeed
        self.y -= held_keys['s'] * time.dt * self.verticalSpeed

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

        if Ending.enabled and self.x >= obstacleReset * 30:
            Ending.enabled = False
            self.flag = self.complete
            self.position = (0, 0)
            pipes.position = (flappy.x + 30, random.randint(-15, 15))

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
        print('pipes')

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
        self.enabled = False

    def update(self):
        print('finish')
        if self.intersects(flappy).hit:
            Ending.enabled = True


class GameManager(Entity):
    def __init__(self):
        super().__init__()
        self.infiniteS = "infinite"
        self.multiRaceS = "multi-race"
        self.singleRaceS = "single-race"
        self.menuS = "menuState"
        self.state = self.menuS

    def startSRace(self):
        self.state = self.singleRaceS
        flappy.flag = flappy.inRace

    def input(self, key):
        if key == '1':
            quit()

    def update(self):
        print(self.state)

        if self.state == self.menuS:
            b.enabled = True

        if self.state == self.singleRaceS:
            b.enabled = False
            flappy.enabled = True
            pipes.enabled = True


flappy = Player()
pipes = Pipes()
finish = Finish()

g = GameManager()

Score = Text(position=(0, .4),
             scale=(2, 2))

Ending = Text(text="Congratulations, you've made it to the end",
              scale=(2, 2),
              position=(-.4, 0),
              enabled=False)

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
    global obstacleCounter

    if obstacleCounter == obstacleCap:
        finish.enabled = True
        finish.x = flappy.x + 30


app.run()
