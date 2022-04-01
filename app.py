from ursina import *
import random

app = Ursina()
a = Audio('data/sfx/Flappy Bird Theme Song.mp3', loop=True, autoplay=True)

obstacleCounter = 0

states = ['mainMenu', 'gamemodeSelection', 'playerSelection', 'race', 'infinite']
currentState = states[4]

camera.orthographic = True
# window.fullscreen = True
window.cog_button.enabled = False
window.exit_button.enabled = False
window.fps_counter.enabled = False


class Player(Entity):
    def __init__(self):
        super().__init__()
        self.model = "quad"
        self.collider = "box"
        self.color = color.white
        self.scale = 1
        self.position = (1, 1)
        self.horizontalSpeed = 6
        self.verticalSpeed = 10
        self.loSpeed = 6
        self.hiSpeed = 12
        self.loVol = 0
        self.hiVol = 2
        self.muted = False

    def setSpeed(self, value):
        self.horizontalSpeed = value

    def getSpeed(self):
        return self.horizontalSpeed

    def mute(self, value):
        self.muted = value

    def getVolState(self):
        return self.muted

    def input(self, key):
        if key == '1':
            quit()

        if key == 'm':
            if not self.muted:
                self.mute(self.hiVol)
            if self.muted:
                self.mute(self.loVol)

    def update(self):
        camera.x = self.x

        self.y += held_keys['w'] * time.dt * self.verticalSpeed
        self.y -= held_keys['s'] * time.dt * self.verticalSpeed

        if held_keys['w'] and held_keys['s']:
            if self.horizontalSpeed != self.hiSpeed:
                self.setSpeed(self.hiSpeed)
                self.color = color.magenta
        else:
            if self.horizontalSpeed != self.loSpeed:
                self.setSpeed(self.loSpeed)
                self.color = color.white

        if self.intersects(pipes.obstacleUp).hit or self.intersects(pipes.obstacleDown).hit:
            self.position = (0, 0)
            pipes.position = (self.x + 30, random.randint(-15, 15))

        if not self.muted:
            a.volume = 2
        if self.muted:
            a.volume = 0

        self.x += time.dt * self.horizontalSpeed


class Pipes(Entity):
    def __init__(self):
        super().__init__()
        self.position = (flappy.x + 30, random.randint(-15, 15))
        self.obstacleDown = Entity(model='quad', color=color.green, scale=(8, 40), y=-25, collider='box', parent=self)
        self.obstacleUp = Entity(model='quad', color=color.green, scale=(8, 40), y=25, collider='box', parent=self)

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
        self.enabled = False

    def update(self):
        if self.intersects(flappy).hit:
            Ending.enabled = True


flappy = Player()
pipes = Pipes()
finish = Finish()

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


# called every frame
def update():
    global currentState, states, obstacleCounter

    Score.text = f"score: {int(flappy.x)}"

    if obstacleCounter == 2:
        finish.enabled = True
        finish.x = flappy.x + 30


app.run()
