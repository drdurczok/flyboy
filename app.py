from ursina import *
from unittest.mock import Mock
import random, datetime

app = Ursina()
a = Audio('data/sfx/Flappy Bird Theme Song.mp3', loop=True, autoplay=True)

obstacleSpawnTimer = 0
obstacleCounter = 0
timestamp = datetime.datetime.now()
delay = 4

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
        self.color = color.white
        self.scale = 1
        self.position = (1, 1)
        self.horizontalSpeed = 6
        self.verticalSpeed = 10
        self.loSpeed = 6
        self.hiSpeed = 12

    def setSpeed(self, value):
        self.horizontalSpeed = value

    def getSpeed(self):
        return self.horizontalSpeed

    def input(self, key):
        if key == '1':
            quit()

    def update(self):
        self.y += held_keys['w'] * time.dt * self.verticalSpeed
        self.y -= held_keys['s'] * time.dt * self.verticalSpeed

        if held_keys['w'] and held_keys['s']:
            if self.horizontalSpeed != self.hiSpeed:
                self.setSpeed(self.hiSpeed)
                self.color = color.magenta
        else:
            if self.horizontalSpeed != self.loSpeed:
                self.setSpeed(self.loSpeed)

        self.x += time.dt * self.horizontalSpeed


# drawing entities and buttons to the screen
player1 = Entity(model='quad',
                 collider='box',
                 color=color.white,
                 scale=(1, 1),
                 position=(-.1, 0))

obstacleDefiner = Entity(position=(player1.x + 30, random.randint(-15, 15)))
obstacleDown = Entity(model='quad',
                      color=color.green,
                      scale=(8, 40),
                      y=-25,
                      collider='box',
                      parent=obstacleDefiner)
obstacleUp = Entity(model='quad',
                    color=color.green,
                    scale=(8, 40),
                    y=25,
                    collider='box',
                    parent=obstacleDefiner)

finish = Entity(model='quad',
                collider='box',
                color=color.black,
                scale=(1, 100),
                position=(player1.x + 30, 0),
                enabled=False)

Score = Text(position=(0, .4),
             scale=(2, 2))

Ending = Text(text="Congratulations, you've made it to the end",
              scale=(3, 3),
              enabled=False)

Collision = Text(text=f"You Crashed, restarting",
                 scale=(3, 3),
                 enabled=False,
                 position=(-.4, .2))


# responsible for drawing pipes
def drawObstacles():
    global player1, obstacleCounter, obstacleSpawnTimer

    obstacleDefiner.position = (player1.x + 30, random.randint(-15, 15))

    obstacleCounter += 1
    print(f"{obstacleCounter}")


# def drawFinish():
#     global finish
#
#     finish.enabled = True


# responsible for moving and changing player1's speed
# def Move():
#     global horizontalSpeed, verticalSpeed
#
#     player1.x += horizontalSpeed
#     camera.x = player1.x
#
#     if held_keys['w'] and held_keys['s']:
#         horizontalSpeed = 9 * time.dt
#     if not held_keys['w'] and held_keys['s']:
#         horizontalSpeed = 6 * time.dt
#         player1.y -= verticalSpeed * time.dt
#     if held_keys['w'] and not held_keys['s']:
#         horizontalSpeed = 6 * time.dt
#         player1.y += verticalSpeed * time.dt
#     if not held_keys['w'] and not held_keys['s']:
#         horizontalSpeed = 6 * time.dt

    # if held_keys['1']:
    #     quit()
    #
    # if horizontalSpeed == 6:
    #     player1.color = color.white
    # else:
    #     player1.color = color.magenta


drawObstacles()


# called every frame
def update():
    global currentState, states, obstacleSpawnTimer, obstacleCounter, timestamp, obstacleUp, obstacleDown, delay, finish

    # Move()
    Score.text = f"score: {int(player1.x)}"

    camera.x = flappy.x

    if player1.x >= obstacleDefiner.x:
        drawObstacles()

    if obstacleCounter == 10:
        finish.enabled = True

    if finish.enabled:
        print("Whats wrong with your code?!11?!?!1")

    # if player1.intersects(finish).hit:
    #     Ending.enabled = True

    if held_keys['m']:
        a.volume = 0
    if held_keys['n']:
        a.volume = 2

    if player1.intersects(obstacleUp).hit or player1.intersects(obstacleDown).hit:
        player1.enabled = False
        Collision.enabled = True

    if not player1.enabled:
        player1.position = (0, 0)
        player1.enabled = True
        drawObstacles()
        obstacleCounter = 0
        finish.enabled = False

flappy = Player()

app.run()
