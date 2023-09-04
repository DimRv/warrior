import pygame as pg


class Pistol:
    def __init__(self):
        self.start_shoot_time = 40
        self.shoot_time = 40
        self.shoot_timer = 40
        self.shoot_distance = 500
        self.sound = pg.mixer.Sound('sounds\\pistol.mp3')


class Shotgun:
    def __init__(self):
        self.start_shoot_time = 60
        self.shoot_time = 60
        self.shoot_timer = 60
        self.shoot_distance = 450
        self.sound = pg.mixer.Sound('sounds\\shotgun.mp3')


class MachineGun:
    def __init__(self):
        self.start_shoot_time = 10
        self.shoot_time = 13
        self.shoot_timer = 13
        self.shoot_distance = 800
        self.sound = pg.mixer.Sound('sounds\\machinegun.mp3')