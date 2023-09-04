import pygame as pg
from objects import VisibleObject


class BonusObject(VisibleObject):
    def __init__(self, size, pos, button):
        VisibleObject.__init__(self, size, pos)
        self.is_activated = False
        #self.is_active = False
        self.timer = 0
        self.time = 300
        self.radius = 20
        self.radius_timer = 0
        self.radius_time = 3
        self.decrease = True
        self.button = button
        self.sound = pg.mixer.Sound('sounds\\bonus.mp3')

    def get_surface(self):
        surf = pg.Surface(self.size)
        pg.Surface.set_colorkey(surf, 'black')
        pg.draw.circle(surf, 'gold', (20, 20), self.radius)
        pg.draw.circle(surf, (50, 50, 50), (20, 20), self.radius, 1)
        font = pg.sysfont.SysFont('arial', 18)
        text = font.render(self.button, False, (50, 50, 50))
        surf.blit(text, (20 - text.get_width()/2, 20 - text.get_height()/2))
        """if self.is_activated:
            self.screen_pos = (-60, -60)"""
        return surf


class AttackBonus(BonusObject):
    def __init__(self, size, pos):
        BonusObject.__init__(self, size, pos, "A")
        self.surface = self.get_surface()

    def __repr__(self):
        return "A"


class SpeedBonus(BonusObject):
    def __init__(self, size, pos):
        BonusObject.__init__(self, size, pos, "S")
        self.surface = self.get_surface()

    def __repr__(self):
        return "S"


class HealthBonus(BonusObject):
    def __init__(self, size, pos):
        BonusObject.__init__(self, size, pos, "H")
        self.surface = self.get_surface()

    def __repr__(self):
        return "H"


class DefenceBonus(BonusObject):
    def __init__(self, size, pos):
        BonusObject.__init__(self, size, pos, "D")
        self.surface = self.get_surface()

    def __repr__(self):
        return "D"


class TerminateBonus(BonusObject):
    def __init__(self, size, pos):
        BonusObject.__init__(self, size, pos, "T")
        self.time = 50
        self.angle = 0
        self.sound = pg.mixer.Sound('sounds\\terminate.mp3')
        self.start_surface = self.create_surface()
        self.surface = self.get_surface()

    def create_surface(self):
        surf = pg.Surface(self.size)
        pg.Surface.set_colorkey(surf, "black")
        pg.draw.circle(surf, (100, 200, 200), (20, 20), 15)
        pg.draw.circle(surf, (50, 50, 50), (20, 20), 15, 1)
        pg.draw.line(surf, (50, 50, 50), (20, 19), (40, 19), 3)
        return surf

    def get_new_surface(self):
        surf = pg.transform.rotate(self.start_surface, self.angle)
        self.size = surf.get_size()
        self.screen_pos = self.center[0] - self.size[0] / 2, self.center[1] - self.size[1] / 2
        return surf

    def __repr__(self):
        return "T"


class ShotgunBonus(BonusObject):
    def __init__(self, size, pos):
        BonusObject.__init__(self, size, pos, "SG")
        self.surface = self.get_surface()

    def __repr__(self):
        return "SG"


class MachineGunBonus(BonusObject):
    def __init__(self, size, pos):
        BonusObject.__init__(self, size, pos, "MG")
        self.surface = self.get_surface()

    def __repr__(self):
        return "MG"


