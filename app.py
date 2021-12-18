from ursina import *
from unittest.mock import Mock
import random, time

app = Ursina()
a = Audio('data/sfx/Flappy Bird Theme Song.mp3', loop=True, autoplay=True)

pipeSpawnTimer = 0
pipeCounter = 0

states = ['mainMenu', 'gamemodeSelection', 'playerSelection', 'race', 'infinite']
currentState = states[4]

horizontalSpeed = .3
verticalSpeed = .3
camera.orthographic = True
window.fullscreen = True
window.cog_button.enabled = False
window.exit_button.enabled = False
window.fps_counter.enabled = True

# drawing entities and buttons to the screen
player1 = Entity(model='quad',
                 collider='box',
                 color=color.white,
                 scale=(1, 1),
                 position=(-.1, 0))

finish = Entity(model='quad',
                collider='box',
                color=color.black,
                scale=(1, 10),
                position=(player1.x + 30, 0))
finish.enabled = False


# responsible for drawing pipes
def drawPipes():
    global player1, pipeCounter, pipeSpawnTimer

    # checkFinMock = Mock(side_effect=drawPipes)

    pipeDefiner = Entity(position=(player1.x + 30, random.randint(-15, 15)))
    pipeDown = Entity(model='quad',
                      color=color.green,
                      scale=(8, 40),
                      y=-25,
                      collider='box',
                      parent=pipeDefiner)
    pipeUp = Entity(model='quad',
                    color=color.green,
                    scale=(8, 40),
                    y=25,
                    collider='box',
                    parent=pipeDefiner)
    pipeDefiner.enabled = False

    if pipeSpawnTimer == 100:
        print("Drawn a pipe")
        pipeDefiner.enabled = True

        pipeSpawnTimer = 0
    pipeSpawnTimer += 1

    # if pipeCounter == 10:
    #     checkFinMock()

    # if checkFinMock.called:
    #     drawFinish()

    # if player1.intersects(pipeDown or pipeUp).hit:
    #     player1.enabled = False


def drawFinish():
    global finish

    finish.enabled = True


# responsible for moving and changing player1's speed
def Move():
    global horizontalSpeed, verticalSpeed

    player1.x += horizontalSpeed
    camera.x = player1.x

    if held_keys['w'] and held_keys['s']:
        horizontalSpeed = .6
    if not held_keys['w'] and held_keys['s']:
        horizontalSpeed = .3
        player1.y -= verticalSpeed
    if held_keys['w'] and not held_keys['s']:
        horizontalSpeed = .3
        player1.y += verticalSpeed
    if not held_keys['w'] and not held_keys['s']:
        horizontalSpeed = .3

    if held_keys['1']:
        quit()

    if horizontalSpeed == .3:
        player1.color = color.white
    else:
        player1.color = color.magenta


def Play():
    global currentState, states

    currentState = states[4]

    return currentState


def MainMenu():
    global currentState, states

    playBTN = Button(text='Play',
                     color=color.blue,
                     scale=(.2, .1))

    playBTN.on_click = Play()


drawPipes()


# called every frame
def update():
    global currentState, states, pipeSpawnTimer

    if currentState == states[4]:
        Move()
        drawPipes()

        if player1.intersects(finish).hit:
            quit()

    if held_keys['m']:
        a.volume = 0
    if held_keys['n']:
        a.volume = 2

    if player1.intersects().hit:
        player1.enabled = False

    if not player1.enabled:
        player1.position = (0, 0)
        player1.enabled = True

    time.sleep(0.008333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333)


app.run()
