"""Visible on display objects"""
import pygame as pg
from random import choice
from math import atan2, pi, radians, sin, cos
from weapons import Pistol, Shotgun, MachineGun


class VisibleObject:

    def __init__(self, size, pos):
        self.start_size = size
        self.size = self.start_size
        self.center = pos
        self.screen_pos = pos[0] - self.size[0] / 2, pos[1] - self.size[1] / 2

    def get_center(self):
        return self.size[0]/2, self.size[1]/2

    def check_collision(self, obj):
        delta_x = (self.size[0] - self.start_size[0]) / 2
        delta_y = (self.size[1] - self.start_size[1]) / 2
        points = ((self.screen_pos[0] + delta_x, self.screen_pos[1] + delta_y),
                  (self.screen_pos[0] + self.start_size[0] + delta_x, self.screen_pos[1] + delta_y),
                  (self.screen_pos[0] + self.start_size[0] + delta_x, self.screen_pos[1] + delta_y +self.start_size[0]),
                  (self.screen_pos[0] + delta_x, self.screen_pos[1] + delta_y + self.start_size[0]))
        obj_delta_x = (obj.size[0] - obj.start_size[0]) / 2
        obj_delta_y = (obj.size[1] - obj.start_size[1]) / 2
        for x, y in points:
            if int(x) in range(int(obj.screen_pos[0] + obj_delta_x),
                               int(obj.screen_pos[0] + obj_delta_x + obj.start_size[0])):
                if int(y) in range(int(obj.screen_pos[1] + obj_delta_y),
                                   int(obj.screen_pos[1] + obj_delta_y + obj.start_size[1])):
                    return True


class Player(VisibleObject):
    def __init__(self, size, pos):
        VisibleObject.__init__(self, size, pos)
        self.map_pos = pos
        self.screen_pos = self.map_pos[0] - self.get_center()[0], self.map_pos[1] - self.get_center()[1]
        self.angle = 0
        self.points = 0
        self.speed = 1
        self.level = 1
        self.health = 100
        self.is_shooting = False
        self.move_direction = (0, 0)
        self.weapon = Pistol()
        self.shield = False
        self.death_sound = pg.mixer.Sound("./sounds/death.mp3")
        self.start_surface = self.create_surface()
        self.surface = self.start_surface

    def set_angle(self, point):
        start = self.map_pos
        x = point[0] - start[0]
        y = point[1] - start[1]
        self.angle = -atan2(y, x) * 180 / pi

    def create_surface(self):
        surf = pg.Surface(self.size)
        pg.Surface.set_colorkey(surf, 'black')
        pg.draw.circle(surf, (100, 100, 100), (self.size[0]/2, self.size[1]/2), 15)
        pg.draw.circle(surf, (50, 50, 50), (self.size[0] / 2, self.size[1] / 2), 15, 1)
        pg.draw.line(surf, (50, 50, 50), (self.size[0] / 2, self.size[1] / 2 - 1), (self.size[0], self.size[1] / 2-1), 3)
        return surf

    def change_surface(self):
        self.surface = pg.transform.rotate(self.start_surface, self.angle)
        self.size = self.surface.get_size()
        self.screen_pos = (self.map_pos[0] - int(self.size[0] / 2), self.map_pos[1] - int(self.size[1] / 2))
        if self.health < 100:
            surf = pg.Surface((40,5))
            width = self.health * 40 / 100
            pg.draw.rect(surf, (250, 50, 50), (0, 0, width, 5))
            pg.draw.rect(surf, (50, 50, 50), (0,0, 40, 5), 1)
            pos = ((self.surface.get_width() - 40) / 2, (self.surface.get_height() - 40) / 2)
            self.surface.blit(surf, pos)
        if self.shield:
            pg.draw.circle(self.surface, (50, 50, 250), (self.size[0]/2, self.size[1]/2), 20, 1)

    def set_move_direction(self, event, key):
        if event == pg.KEYDOWN:
            if key == pg.K_w: self.move_direction = (self.move_direction[0], self.move_direction[1] - 1)
            if key == pg.K_s: self.move_direction = (self.move_direction[0], self.move_direction[1] + 1)
            if key == pg.K_a: self.move_direction = (self.move_direction[0] - 1, self.move_direction[1])
            if key == pg.K_d: self.move_direction = (self.move_direction[0] + 1, self.move_direction[1])
        if event == pg.KEYUP:
            if key == pg.K_w: self.move_direction = (self.move_direction[0], self.move_direction[1] + 1)
            if key == pg.K_s: self.move_direction = (self.move_direction[0], self.move_direction[1] - 1)
            if key == pg.K_a: self.move_direction = (self.move_direction[0] + 1, self.move_direction[1])
            if key == pg.K_d: self.move_direction = (self.move_direction[0] - 1, self.move_direction[1])


class Patron(VisibleObject):
    def __init__(self, size, pos, angle):
        VisibleObject.__init__(self, size, pos)
        self.start_pos = pos
        self.speed = 10
        self.angle = angle
        self.surface = self.create_surface()
        self.distance = 0

    def create_surface(self):
        surf = pg.Surface(self.size)
        pg.Surface.set_colorkey(surf, 'black')
        pg.draw.circle(surf, (255, 100, 100), (self.size[0] / 2, self.size[1] / 2), 3)
        pg.draw.circle(surf, (50, 50, 50), (self.size[0] / 2, self.size[1] / 2), 3, 1)
        return surf

    def update(self):
        self.screen_pos = (self.screen_pos[0] + self.speed*cos(radians(-self.angle)),
                           self.screen_pos[1] + self.speed*sin(radians(-self.angle)))
        self.distance = ((self.screen_pos[0] - self.start_pos[0]) ** 2 + (self.screen_pos[1] - self.start_pos[1]) ** 2) ** 0.5


class Bug(VisibleObject):
    speed = 1

    def __init__(self, size, pos, screen_center):
        VisibleObject.__init__(self, size, pos)
        self.center = pos
        self.angle = self.set_angle(screen_center)
        self.start_surface = self.create_surface()
        self.sound = pg.mixer.Sound(choice(['./sounds/bug_die.mp3', './sounds/bug_die2.mp3', './sounds/bug_die3.mp3']))
        self.surface = self.change_surface()

    def create_surface(self):
        surf = pg.Surface(self.size)
        pg.Surface.set_colorkey(surf, 'black')
        pg.draw.ellipse(surf, (150, 150, 150), (0, 0, 35, 40))
        pg.draw.ellipse(surf, (50, 50, 50), (0, 0, 35, 40), 1)
        pg.draw.ellipse(surf, (200, 100, 100), (30, 10, 10, 20))
        pg.draw.ellipse(surf, (50, 50, 50), (30, 10, 10, 20), 1)
        pg.draw.line(surf, (50, 50, 50), (0,20), (30, 20), 1)
        pg.draw.ellipse(surf, (50, 50, 50), (35, 17, 4, 3))
        pg.draw.ellipse(surf, (50, 50, 50), (35, 22, 4, 3))
        pg.draw.circle(surf, (250, 100, 100), (10, 12), 2)
        pg.draw.circle(surf, (50, 50, 50), (10, 12), 2, 1)
        pg.draw.circle(surf, (250, 100, 100), (25, 12), 2)
        pg.draw.circle(surf, (50, 50, 50), (25, 12), 2, 1)
        pg.draw.circle(surf, (250, 100, 100), (10, 28), 2)
        pg.draw.circle(surf, (50, 50, 50), (10, 28), 2, 1)
        pg.draw.circle(surf, (250, 100, 100), (25, 28), 2)
        pg.draw.circle(surf, (50, 50, 50), (25, 28), 2, 1)
        #pg.draw.circle(surf, (50, 50, 50), (self.size[0] / 2, self.size[1] / 2), 15, 1)
        #pg.draw.line(surf, (50, 50, 50), (self.size[0] / 2, self.size[1] / 2 - 1), (self.size[0], self.size[1] / 2 - 1), 3)
        return surf

    def change_surface(self):
        surf = pg.transform.rotate(self.start_surface, self.angle)
        self.size = surf.get_size()
        self.screen_pos = (self.center[0] - int(self.size[0] / 2), self.center[1] - int(self.size[1] / 2))
        return surf

    def set_angle(self, warrior_pos):
        x = warrior_pos[0] - self.center[0]
        y = warrior_pos[1] - self.center[1]
        angle = -atan2(y, x) * 180 / pi
        if -int(angle) in range(-45, 45): self.direction = 'right'
        if -int(angle) in range(45, 135):self.direction = 'bottom'
        if -int(angle) in range(-135, -45): self.direction = 'top'
        if -int(angle) in range(-180, -135) or -int(angle) in range(135, 180): self.direction = "left"
        return angle

    def update(self):
        self.center = (self.center[0] + self.speed*cos(radians(-self.angle)),
                       self.center[1] + self.speed*sin(radians(-self.angle)))
        self.screen_pos = (self.center[0] - int(self.size[0] / 2), self.center[1] - int(self.size[1] / 2))









