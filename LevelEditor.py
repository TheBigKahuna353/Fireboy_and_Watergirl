from hooman import Hooman
import pygame
from objects import System, btn, Object

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 10
SIZE = HEIGHT//GRID_SIZE

hapi = Hooman(WIDTH + 150, HEIGHT)
hapi.set_background(hapi.color['white'])
# hapi.background(hapi.color['white'])

level = [
    Object(0, 0, (100, 100, 100), hapi, "Wall", WIDTH, 2*GRID_SIZE),
    Object(0, 0, (100, 100, 100), hapi, "Wall", 2*GRID_SIZE, HEIGHT),
    Object(WIDTH-2*GRID_SIZE, 0, (100, 100, 100), hapi, "Wall", 2*GRID_SIZE, HEIGHT),
    Object(0, HEIGHT - 2*GRID_SIZE, (100, 100, 100), hapi, "Wall", WIDTH, 2*GRID_SIZE)
    ]

cols_dict = {
    'Wall': (100, 100, 100),
    '': (255, 255, 255),
    'FireBoy': (255, 100, 100),
    'WaterGirl': (100, 100, 255),
    'Lava': (255, 100, 100),
    'Water': (100, 100, 255)
    }

sys = System(level, None, hapi, GRID_SIZE, cols_dict)


btn_names = ["Wall", "Delete", "FireBoy","WaterGirl", "Lava", "Water", "Save"]

btns = [
    btn(675, 100 + 40*x, btn_names[x], sys, hapi) for x in range(len(btn_names))
]
sys.btns = btns


while hapi.is_running:

    for obj in level:
        obj.draw()

    for b in btns:
        b.update()

    sys.update()

    hapi.flip_display()
    hapi.event_loop()