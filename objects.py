import pygame
from Data import Levels

GRAVITY = 0.3
PLAYER_W = 30
PLAYER_H = 40
LIQUID_H = 5

class Liquid:
    def __init__(self, hapi, element, x, y, w) -> None:
        self.element = element
        self.rect = pygame.Rect(x, y, w, LIQUID_H)
        self.col = 'red' if self.element == 'lava' else 'blue'
        self.hapi = hapi
    
    def draw(self):
        self.hapi.fill(self.hapi.color[self.col])
        self.hapi.rect(*self.rect)
    
    def Save(self):
        return ["Liquid", *self.rect, self.element]

class Character:

    def __init__(self, hapi, col, image, sx = 50, sy = 500) -> None:
        self.rect = pygame.Rect(sx, sy, PLAYER_W, PLAYER_H)
        self.vel = [0, 0]
        self.on_ground = False
        self.touch_count = 0
        self.col = col
        self.element = 'lava' if col == 'red' else 'water'
        self.hapi = hapi
        self.image = pygame.image.load(image).convert_alpha()
        self.slow_down = False
        self.score = 0
    
    def restart(self):
        self.rect.topleft = (50, 500)

    def draw(self):
        # self.hapi.fill(self.hapi.color[self.col])
        # self.hapi.rect(*self.rect)
        self.hapi.screen.blit(self.image, self.rect)
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
        self.vel[1] += GRAVITY
        if self.slow_down:
            self.vel[0] += 1 if self.vel[0] < 0 else -1
            if self.vel[0] == 0:
                self.slow_down = False
    
    def check_for_death(self, liquids):
        for liquid in liquids:
            if liquid.element != self.element:
                if self.rect.colliderect(liquid.rect):
                    return True
    
    def Save(self) -> list:
        return ["Character", *self.rect, self.element]

    def check_for_collectables(self, collects):
        for cll in collects:
            if cll.active:
                if cll.element == self.element:
                    if self.rect.colliderect(cll.rect):
                        self.score += 1
                        cll.active = False

    def check_for_collisions(self, obstacles):
        self.touch_count += 1
        if self.touch_count > 10:
            self.on_ground = False
        for obst in obstacles:
            if self.rect.colliderect(obst.rect):
                if self.rect.centerx < obst.rect.left:
                    self.rect.right = obst.rect.left
                elif self.rect.centerx > obst.rect.right:
                    self.rect.left = obst.rect.right
                if self.rect.centery < obst.rect.top:
                    self.rect.bottom = obst.rect.top
                    self.vel[1] = 0
                    self.on_ground = True
                    self.touch_count = 0
                elif self.rect.centery > obst.rect.bottom:
                    self.rect.top = obst.rect.bottom
                    self.vel[1] = 0

class Platform:

    def __init__(self, hapi, x, y, w, h) -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.hapi = hapi
        
    def draw(self):
        self.hapi.fill(self.hapi.color['grey'])
        self.hapi.rect(*self.rect)
    
    def Save(self) -> list:
        return ["Platform", *self.rect, self.element]

class Collectable:
    def __init__(self, hapi, element, image, x, y) -> None:
        self.hapi = hapi
        self.element = element
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(topleft = (x, y))
        self.active = True
    
    def draw(self):
        if self.active:
            self.hapi.screen.blit(self.image, self.rect)
    
    def Save(self) -> list:
        return ["Collectable", *self.rect, self.element]


# ===================================================================================================
#----------------------------------------- Level Editor ---------------------------------------------
# ===================================================================================================

class Object:
    def __init__(self, x, y, col, hapi, t, w=0, h=0) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.col = col
        self.hapi = hapi
        # self.make_positive()
        self.t = t
    
    def draw(self):
        self.hapi.fill(self.col)
        self.hapi.rect(self.x, self.y, self.w, self.h)
    
    def negative_draw(self):
        self.hapi.fill(self.col)
        x = self.x + self.w if self.w < 0 else self.x
        y = self.y + self.h if self.h < 0 else self.y
        self.hapi.rect(x, y, abs(self.w), abs(self.h))
    
    def rect(self) ->pygame.Rect:
        return pygame.Rect(self.x, self.y, self.w, self.h)
    
    def make_positive(self):
        if self.w < 0:
            self.x += self.w
            self.w *= -1
        if self.h < 0:
            self.y += self.h
            self.h *= -1
    
    def __repr__(self) -> str:
        return "Object: (%d, %d, %d, %d) " %(self.x, self.y, self.w, self.h) + str(self.col) 

class System:
    def __init__(self, level, btns, hapi, size, cols) -> None:
        self.selected = ""
        self.level = level
        self.wgirl_pos = None
        self.fboy_pos = None
        self.btns = btns
        self.hapi = hapi
        self.size = size
        self.new_obj = None
        self.cols_dict = cols
        self.deleted = False
    
    def update(self):
        if self.selected == "Wall":
            self.wall()
        elif self.selected in ["FireBoy", "WaterGirl"]:
            self.char()
        elif self.selected == "Delete":
            self.delete()
        elif self.selected in ["Lava", "Water"]:
            self.liquid()
    
    def char(self):
        x = self.hapi.mouseX()
        y = self.hapi.mouseY()
        if x < 600:
            obj = self.fboy_pos if self.selected == "FireBoy" else self.wgirl_pos
            if obj is None:
                if pygame.mouse.get_pressed()[0]:
                        self.new_obj = Object(
                            int(x), int(y), self.cols_dict[self.selected], self.hapi,
                            self.selected, PLAYER_W, PLAYER_H)
                        if self.selected == "FireBoy":
                            self.fboy_pos = self.new_obj
                        else:
                            self.wgirl_pos = self.new_obj
                        self.level.append(self.new_obj)
            elif pygame.mouse.get_pressed()[0]:
                obj.x = x
                obj.y = y

    def wall(self):
        if self.new_obj is None:
            if pygame.mouse.get_pressed()[0]:
                x = self.hapi.mouseX()
                y = self.hapi.mouseY()
                if x < 600:
                    self.new_obj = Object(int(x), int(y), self.cols_dict[self.selected],
                        self.hapi, self.selected)
        elif not pygame.mouse.get_pressed()[0]:
            self.new_obj.make_positive()
            self.level.append(self.new_obj)
            self.new_obj = None
        else:
            dx = self.hapi.mouseX() - self.new_obj.x
            dy = self.hapi.mouseY() - self.new_obj.y
            self.new_obj.negative_draw()
            if abs(dx) > abs(dy):
                self.new_obj.w = dx
                self.new_obj.h = 2*self.size
            else:
                self.new_obj.h = dy
                self.new_obj.w = 2*self.size
    
    def liquid(self):
        if self.new_obj is None:
            if pygame.mouse.get_pressed()[0]:
                x = self.hapi.mouseX()
                y = self.hapi.mouseY()
                for obj in self.level:
                    if obj.rect().collidepoint((x, y)):
                        self.new_obj = Object(
                            int(x), obj.y, self.cols_dict[self.selected], self.hapi, 
                            self.selected, 0, LIQUID_H)
        elif not pygame.mouse.get_pressed()[0]:
            self.new_obj.make_positive()
            self.level.append(self.new_obj)
            self.new_obj = None
        else:
            dx = self.hapi.mouseX() - self.new_obj.x
            self.new_obj.negative_draw()
            self.new_obj.w = dx

    def delete(self):
        if self.hapi.mouseX() < 600:
            if pygame.mouse.get_pressed()[0]:
                if not self.deleted:
                    for obj in reversed(self.level):
                        if obj.rect().collidepoint((self.hapi.mouseX(), self.hapi.mouseY())):
                            self.level.remove(obj)
                            if self.wgirl_pos == obj:
                                self.wgirl_pos = None
                            if self.fboy_pos == obj:
                                self.fboy_pos = None
                            self.deleted = True
                            break
            else:
                self.deleted = False
    
    def save(self):
        l = Levels()
        l.new_level("Test", self.level)

    def btn_select(self, btn):
        self.selected = btn.txt
        btn.select()
        for b in self.btns:
            if b != btn:
                b.unselect()
    
    def btn_unselect(self, btn):
        self.selected = None
        btn.unselect()

class btn:
    def __init__(self, x, y, txt, sys, hapi) -> None:
        self.btn = hapi.button(x, y, 0, 0, txt, {
            'calculate_size': True,
            'background_color': (200, 200, 200),
            'hover_background_color': (220, 220, 220),
            'padding_x': 2,
            'padding_y': 2,
            'centered': True
            })
        self.selected = False
        self.txt = txt
        self.hapi = hapi
        self.sys = sys
    
    def select(self):
        self.btn.outline = True
        self.selected = True
        self.btn.create_button()
        self.btn.image = self.btn.hover_image

    def unselect(self):
        self.btn.outline = False
        self.btn.create_button()
        self.selected = False

    def update(self):
        """This updates the Button"""
        if self.btn.update():
            if self.selected: self.sys.btn_unselect(self)
            else: self.sys.btn_select(self)
        if self.selected:
            self.btn.hover = True