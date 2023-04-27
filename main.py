from hooman import Hooman
import pygame
from objects import *
from Data import Levels

WIDTH, HEIGHT = 600, 600
FPS = 60
UP_KEY = 1073741906
LEFT_KEY = 1073741904
RIGHT_KEY = 1073741903

clock = pygame.time.Clock()

hapi = Hooman(WIDTH, HEIGHT)
hapi.set_background(hapi.color['white'])
hapi.set_caption('FBoy and WGirl')

Fboy = Character(hapi, 'red', 'Images/FireBoy.png')
Wgirl = Character(hapi, 'blue', 'Images/WaterGirl.png')

obst = [
    Platform(hapi, 0, 580, 600, 20), 
    Platform(hapi, 0, 0, 20, 600), 
    Platform(hapi, 580, 20, 20, 600), 
    Platform(hapi, 0, 0, 600, 20),

    Platform(hapi, 150, 500, 200, 20),
    Platform(hapi, 500, 490, 100, 20),
    Platform(hapi, 20, 400, 450, 20)
    ]

liquids = [
    Liquid(hapi, "lava", 160, 500, 180),
    Liquid(hapi, 'water', 160, 580, 180)
]

diamonds = [
    Collectable(hapi, 'lava', 'Images/Red_diamond.png', 100, 360),
    Collectable(hapi, 'water', 'Images/Blue_diamond.png', 150, 360)

]

def event(event):
    if event.type == pygame.QUIT:
        hapi.is_running = False
    if event.type == pygame.KEYDOWN:
        key = event.unicode
        if key == " ":
            game.main_screen = game.win
        if key == "d":
            Fboy.vel[0] = 4
        elif key == "a":
            Fboy.vel[0] = -4
        elif key == "w":
            if Fboy.on_ground:
                Fboy.vel[1] = -7
        key = event.key
        if key == RIGHT_KEY:
            Wgirl.vel[0] = 4
        elif key == LEFT_KEY:
            Wgirl.vel[0] = -4
        elif key == 1073741906:
            if Wgirl.on_ground:
                Wgirl.vel[1] = -7
    if event.type == pygame.KEYUP:
        key = event.unicode
        if key == "d" and Fboy.vel[0] != -4:
            Fboy.slow_down = True
        elif key == "a" and Fboy.vel[0] != 4:
            Fboy.slow_down = True
        key = event.key
        if key == RIGHT_KEY and Wgirl.vel[0] != -4:
            Wgirl.slow_down = True
        elif key == LEFT_KEY and Wgirl.vel[0] != 4:
            Wgirl.slow_down = True

hapi.handle_events = event


class Game:
    def __init__(self) -> None:
        self.main_screen = self.start_screen
        self.show_fps = False
        self.restart_btn = hapi.button(250, 300, 100, 50, 'Restart', {
            'background_color': hapi.color['grey'],
            'hover_background_color': hapi.color['light_grey']
            })
        self.start_btn = hapi.button(250, 300, 100, 50, "Start", {
            'background_color': hapi.color['grey'],
            'hover_background_color': hapi.color['light_grey'],
            'curve': .5,
            'enlarge': True
        })

    def loop(self):
        while hapi.is_running:
            clock.tick(FPS)
            self.main_screen()
            if self.show_fps:
                hapi.fill(hapi.color["black"])
                hapi.font_size(10)
                hapi.text(str(clock.get_fps()), 50, 50)
            hapi.flip_display()
            hapi.event_loop()

    def win(self):
        hapi.font_size(40)
        hapi.text('You WIN', 200, 200)

    def start_screen(self):
        hapi.font_size(50)
        hapi.fill(hapi.color['black'])
        hapi.text('Fireboy and Watergirl', 50, 200)
        if self.start_btn.update():
            self.main_screen = self.play

    def dead(self):
        hapi.fill(hapi.color['black'])
        hapi.font_size(40)
        hapi.text('You Died', 200, 200)
        if self.restart_btn.update():
            global Fboy, Wgirl
            Fboy.restart()
            Wgirl.restart()
            self.main_screen = self.play

    def play(self):
        Fboy.draw()
        Wgirl.draw()
        if Fboy.check_for_death(liquids) or Wgirl.check_for_death(liquids):
            self.main_screen = self.dead
        Fboy.check_for_collisions(obst)
        Wgirl.check_for_collisions(obst)
        Fboy.check_for_collectables(diamonds)
        Wgirl.check_for_collectables(diamonds)
        for ob in obst:
            ob.draw()
        for liquid in liquids:
            liquid.draw()
        for diamond in diamonds:
            diamond.draw()

game = Game()
game.loop()