"""WARRIOR shoots enemies"""

import pygame as pg
from sys import exit
from objects import Player, Bug, Patron
from random import choice, randint, random
from bonus import AttackBonus, SpeedBonus, HealthBonus, TerminateBonus, ShotgunBonus, MachineGunBonus, DefenceBonus
from weapons import Shotgun, MachineGun


class Game:

    def __init__(self):
        self.version = "0.0.0"
        self._screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self._screen_size = self._screen.get_size()
        self.clock = pg.time.Clock()
        self.player = Player((40,40), (self._screen_size[0]/2, self._screen_size[1]/2))
        self.patrons = []
        self.enemies = [Bug((40, 40), (1000, 100), (self._screen_size[0]/2, self._screen_size[1]/2))]
        self.bonuses = []
        self.able_bonuses = [AttackBonus, SpeedBonus]
        self.activated_bonuses = []
        self.enemy_timer = 0
        self.enemy_time = 60
        self.is_running = True
        self.start_menu = True
        self.results_menu = False
        self.start = False
        self.game_menu = False
        self.menu_title_pos = (self._screen_size[0], 200)
        self.menu_buttons = ['Start Game', "Best Results", "Quit"]
        self.menu_buttons_pos = []
        self.menu_active_button = 0
        self.results_menu_buttons = ['To Menu']
        self.results_menu_buttons_pos = []
        self.results_menu_active_button = 0
        self.cursor_on_button = False
        self.cursor_on_resultbutton = False
        self.game_menu_buttons = ['Resume Game', "Quit"]
        self.game_menu_buttons_pos = []
        self.game_menu_active_button = 0
        self.start_menu_surface = self.get_start_menu()
        self.results_menu_surface = self.get_results_menu()
        self.game_menu_surface = self.get_game_menu()
        self.score_surface = self.get_score_surface()

    def start_game(self):
        pg.mixer.music.load('sounds\\menu.mp3')
        pg.mixer.music.play()
        while self.is_running:
            self.clock.tick(60)
            self.get_events()
            self.display_frame()
            self.update()

    def quit_game(self):
        self.is_running = False
        pg.quit()
        exit()

    def get_events(self):
        if self.start_menu or self.results_menu:
            for event in pg.event.get():
                if event.type == pg.MOUSEMOTION:
                    if self.start_menu:
                        for coordinate in self.menu_buttons_pos:
                            delta_x = range(int(coordinate[0]), int(coordinate[0]) + int(coordinate[2]))
                            delta_y = range(int(coordinate[1]), int(coordinate[1]) + int(coordinate[3]))
                            if event.pos[0] in delta_x and event.pos[1] in delta_y:
                                self.menu_active_button = self.menu_buttons_pos.index(coordinate)
                                self.cursor_on_button = True
                                break
                            else:
                                self.cursor_on_button = False
                                self.cursor_on_resultbutton = False
                    if self.results_menu:
                        for coordinate in self.results_menu_buttons_pos:
                            delta_x = range(int(coordinate[0]), int(coordinate[0]) + int(coordinate[2]))
                            delta_y = range(int(coordinate[1]), int(coordinate[1]) + int(coordinate[3]))
                            if event.pos[0] in delta_x and event.pos[1] in delta_y:
                                self.results_menu_active_button = self.results_menu_buttons_pos.index(coordinate)
                                self.cursor_on_resultbutton = True
                                break
                            else:
                                self.cursor_on_button = False
                                self.cursor_on_resultbutton = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.results_menu and event.button == 1:
                        if self.results_menu_buttons[self.results_menu_active_button] == 'To Menu' and self.cursor_on_resultbutton:
                            self.results_menu = False
                            self.start_menu = True
                    if self.start_menu and event.button == 1:
                        if self.menu_buttons[self.menu_active_button] == 'Start Game' and self.cursor_on_button:
                            self.start_menu = False
                            pg.mixer.music.load('sounds\\fon.mp3')
                            pg.mixer.music.play()
                            self.start = True
                        if self.menu_buttons[self.menu_active_button] == 'Best Results' and self.cursor_on_button:
                            self.start_menu = False
                            self.results_menu = True
                        if self.menu_buttons[self.menu_active_button] == 'Quit' and self.cursor_on_button:
                            self.quit_game()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        if self.start_menu:
                            self.quit_game()
                        if self.results_menu:
                            self.results_menu = False
                            self.start_menu = True
                    if event.key == pg.K_RETURN:
                        if self.start_menu:
                            if self.menu_buttons[self.menu_active_button] == 'Start Game':
                                self.start_menu = False
                                pg.mixer.music.load('sounds\\fon.mp3')
                                pg.mixer.music.play()
                                self.start = True
                            if self.menu_buttons[self.menu_active_button] == 'Best Results':
                                self.start_menu = False
                                self.results_menu = True
                            if self.menu_buttons[self.menu_active_button] == 'Quit':
                                self.quit_game()
                    if event.key in (pg.K_DOWN, pg.K_s):
                        self.menu_active_button += 1
                        if self.menu_active_button >= len(self.menu_buttons):
                            self.menu_active_button = 0
                        self.start_menu_surface = self.get_start_menu()
                    if event.key in (pg.K_UP, pg.K_w):
                        self.menu_active_button -= 1
                        if self.menu_active_button < 0:
                            self.menu_active_button = len(self.menu_buttons) - 1
                        self.start_menu_surface = self.get_start_menu()

        else:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        if self.game_menu:
                            self.game_menu = False
                            self.start = True
                            pg.mixer.music.load('sounds\\fon.mp3')
                            pg.mixer.music.play()
                        else:
                            self.game_menu = True
                            self.start = False
                            pg.mixer.music.load('sounds\\pause.mp3')
                            pg.mixer.music.play()
                    if event.key in (pg.K_w, pg.K_a, pg.K_s, pg.K_d):
                        self.player.set_move_direction(event.type, event.key)
                    if event.key == pg.K_UP:
                        self.game_menu_active_button += 1
                        if self.game_menu_active_button >= len(self.game_menu_buttons):
                            self.game_menu_active_button = 0
                        self.game_menu_surface = self.get_game_menu()
                    if event.key == pg.K_DOWN:
                        self.game_menu_active_button -= 1
                        if self.game_menu_active_button < 0:
                            self.game_menu_active_button = len(self.game_menu_buttons) - 1
                        self.game_menu_surface = self.get_game_menu()
                    if event.key == pg.K_RETURN and self.game_menu:
                        if self.game_menu_buttons[self.game_menu_active_button] == "Resume Game":
                            self.start = True
                            self.game_menu = False
                            pg.mixer.music.load('sounds\\fon.mp3')
                            pg.mixer.music.play()
                        if self.game_menu_buttons[self.game_menu_active_button] == "Quit":
                            self.game_menu = False
                            self.end_game()
                            self.results_menu = True
                if event.type == pg.KEYUP:
                    if event.key in (pg.K_w, pg.K_a, pg.K_s, pg.K_d):
                        self.player.set_move_direction(event.type, event.key)

                if event.type == pg.MOUSEMOTION:
                    self.player.set_angle(event.pos)
                    self.player.change_surface()
                    if self.game_menu:
                        for coordinate in self.game_menu_buttons_pos:
                            delta_x = range(int(coordinate[0]), int(coordinate[0]) + int(coordinate[2]))
                            delta_y = range(int(coordinate[1]), int(coordinate[1]) + int(coordinate[3]))
                            if event.pos[0] in delta_x and event.pos[1] in delta_y:
                                self.game_menu_active_button = self.game_menu_buttons_pos.index(coordinate)
                                self.cursor_on_button = True
                                self.game_menu_surface = self.get_game_menu()
                                break
                            else:
                                self.cursor_on_button = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.player.is_shooting = True
                        if self.game_menu:
                            if self.game_menu_buttons[self.game_menu_active_button] == 'Resume Game' and self.cursor_on_button:
                                self.start = True
                                self.game_menu = False
                                pg.mixer.music.load('sounds\\fon.mp3')
                                pg.mixer.music.play()
                            if self.game_menu_buttons[self.game_menu_active_button] == "Quit" and self.cursor_on_button:
                                self.game_menu = False
                                self.end_game()
                                self.results_menu = True
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.player.is_shooting = False

    def update(self):
        if self.start_menu:
            self.menu_title_pos = (self.menu_title_pos[0] - 1, self.menu_title_pos[1])
            if self.menu_title_pos[0] < -1600:
                self.menu_title_pos = (self._screen_size[0], 200)
            self.start_menu_surface = self.get_start_menu()
        if self.start:
            if self.enemy_timer == self.enemy_time:
                self.create_enemy()
                self.enemy_timer = 0
            else:
                self.enemy_timer += 1

            if self.player.move_direction != (0, 0):
                self.player.map_pos = (self.player.map_pos[0] + self.player.move_direction[0]*self.player.speed,
                                         self.player.map_pos[1] + self.player.move_direction[1]*self.player.speed)
                self.player.change_surface()

            if self.player.weapon.shoot_timer < self.player.weapon.shoot_time:
                self.player.weapon.shoot_timer += 1

            if self.player.is_shooting:
                if self.player.weapon.shoot_timer == self.player.weapon.shoot_time:
                    if self.player.weapon.__class__.__name__ == "Pistol":
                        self.patrons.append(Patron((6, 6), self.player.map_pos, self.player.angle))
                    if self.player.weapon.__class__.__name__ == "Shotgun":
                        delta = -10
                        for i in range(5):
                            self.patrons.append(Patron((6, 6), self.player.map_pos, self.player.angle + delta))
                            delta += 5
                    if self.player.weapon.__class__.__name__ == "MachineGun":
                        delta = randint(-10, 10)
                        self.patrons.append(Patron((6, 6), self.player.map_pos, self.player.angle + delta))
                    self.player.weapon.sound.play()
                    self.player.weapon.shoot_timer = 0

            if any(self.patrons):
                for patron in self.patrons:
                    patron.update()
                    if any(self.enemies):
                        for enemy in self.enemies:
                            range_x = range(int(enemy.screen_pos[0]), int(enemy.screen_pos[0]) + 40)
                            range_y = range(int(enemy.screen_pos[1]), int(enemy.screen_pos[1]) + 40)
                            if int(patron.screen_pos[0]) in range_x and int(patron.screen_pos[1]) in range_y:
                                enemy.sound.play()
                                if random() > .95:
                                    self.bonuses.append(choice(self.able_bonuses)((40, 40), enemy.center))
                                self.enemies.remove(enemy)
                                if patron in self.patrons:
                                    self.patrons.remove(patron)
                                self.player.points += 100
                                self.score_surface = self.get_score_surface()
                                if self.player.points % 1000 == 0:
                                    self.player.level += 1
                                    if self.player.level == 5:
                                        self.able_bonuses.append(ShotgunBonus)
                                    if self.player.level == 10:
                                        self.able_bonuses.append(TerminateBonus)
                                    if self.player.level == 15:
                                        self.able_bonuses.append(MachineGunBonus)
                                        self.able_bonuses.append(DefenceBonus)
                                    Bug.speed += .1
                                    if self.enemy_time > 2:
                                        self.enemy_time -= 2
                                    self.enemy_timer = self.enemy_time
                    if patron.distance > self.player.weapon.shoot_distance and patron in self.patrons:
                        self.patrons.remove(patron)

            if any(self.enemies):
                for enemy in self.enemies:
                    if self.player.move_direction != (0, 0):
                        if enemy.speed == 0:
                            enemy.speed = Bug.speed
                        enemy.angle = enemy.set_angle(self.player.map_pos)
                        enemy.surface = enemy.change_surface()
                    enemy.update()
                    if enemy.check_collision(self.player):
                        if not self.player.shield:
                            self.player.health -= 1
                            if HealthBonus not in self.able_bonuses:
                                self.able_bonuses.append(HealthBonus)
                            self.player.change_surface()
                        enemy.speed = 0
                        if self.player.health == 0:
                            self.player.death_sound.play()
                            self.end_game()
                            self.start = False
                            self.results_menu = True

                if any(self.bonuses):
                    for bonus in self.bonuses:
                        if bonus.radius_timer == bonus.radius_time:
                            if bonus.decrease:
                                bonus.radius -= 1
                                if bonus.radius == 15: bonus.decrease = False
                            else:
                                bonus.radius += 1
                                if bonus.radius == 20: bonus.decrease = True
                            bonus.surface = bonus.get_surface()
                            bonus.radius_timer = 0
                        else:
                            bonus.radius_timer += 1
                        if bonus.check_collision(self.player):
                            bonus.sound.play()
                            if any(self.activated_bonuses):
                                if repr(bonus) in [repr(i) for i in self.activated_bonuses]:
                                    if repr(bonus) in ("A", "S", "D"):
                                        index = [repr(i) for i in self.activated_bonuses].index(repr(bonus))
                                        self.activated_bonuses[index].timer = 0
                                else:
                                    self.activated_bonuses.append(bonus)
                            else:
                                self.activated_bonuses.append(bonus)
                            if repr(bonus) != "T":
                                self.bonuses.remove(bonus)

                if any(self.activated_bonuses):
                    for bonus in self.activated_bonuses:
                        if not bonus.is_activated:
                            bonus.is_activated = True
                            if repr(bonus) == "A":
                                self.player.weapon.shoot_time -= 30
                                if self.player.weapon.shoot_time < 2:
                                    self.player.weapon.shoot_time = 2
                                self.player.weapon.shoot_timer = self.player.weapon.shoot_time
                            if repr(bonus) == "S":
                                self.player.speed += 4
                            if repr(bonus) == "D":
                                self.player.shield = True
                            if repr(bonus) == "SG":
                                self.player.weapon = Shotgun()
                                if ShotgunBonus in self.able_bonuses:
                                    self.able_bonuses.remove(ShotgunBonus)
                                self.activated_bonuses.remove(bonus)
                            if repr(bonus) == "MG":
                                self.player.weapon = MachineGun()
                                if MachineGunBonus in self.able_bonuses:
                                    self.able_bonuses.remove(MachineGunBonus)
                                self.activated_bonuses.remove(bonus)

                        if bonus.is_activated:
                            if repr(bonus) == "H":
                                self.player.health += 2
                                if self.player.health >= 100:
                                    self.player.health = 100
                                    if HealthBonus in self.able_bonuses:
                                        self.able_bonuses.remove(HealthBonus)
                                    self.activated_bonuses.remove(bonus)

                            if repr(bonus) == "T":
                                bonus.angle += 25
                                bonus.surface = bonus.get_new_surface()
                                self.patrons.append(Patron((6, 6), bonus.center, bonus.angle))

                            if bonus.timer != bonus.time:
                                bonus.timer += 1
                            else:
                                if repr(bonus) == "A":
                                    self.player.weapon.shoot_time = self.player.weapon.start_shoot_time
                                    self.player.weapon.shoot_timer = self.player.weapon.shoot_time
                                if repr(bonus) == "S":
                                    self.player.speed -= 4
                                if repr(bonus) == "D":
                                    self.player.shield = False
                                if repr(bonus) == "T":
                                    self.player.weapon.shoot_timer = self.player.weapon.shoot_time
                                    self.bonuses.remove(bonus)
                                self.activated_bonuses.remove(bonus)

    def display_frame(self):
        if self.start_menu:
            self._screen.blit(self.start_menu_surface, (0, 0))
        if self.results_menu:
            self._screen.blit(self.results_menu_surface, (0, 0))
        if self.game_menu:
            self._screen.blit(self.game_menu_surface, (0, 0))
        if self.start:
            self._screen.fill("#3e753b")
            if any(self.patrons):
                for patron in self.patrons:
                    self._screen.blit(patron.surface, patron.screen_pos)
            if any(self.enemies):
                for enemy in self.enemies:
                    self._screen.blit(enemy.surface, enemy.screen_pos)
            if any(self.bonuses):
                for bonus in self.bonuses:
                    self._screen.blit(bonus.surface, bonus.screen_pos)
            if any(self.activated_bonuses):
                surf = self.get_activated_bonuses_surface()
                self._screen.blit(surf, (10, self._screen_size[1] - surf.get_height() - 10))
            self._screen.blit(self.player.surface, self.player.screen_pos)
            self._screen.blit(self.score_surface, (0, 0))
        pg.display.flip()

    def create_enemy(self):
        pos = (0, 0)
        side = choice(['left', "top", "right", 'bottom'])
        if side == 'left': pos = (-40, randint(-40, self._screen_size[1] + 40))
        if side == 'right': pos = (self._screen_size[0] + 40, randint(-40, self._screen_size[1] + 40))
        if side == 'top': pos = (randint(-40, self._screen_size[0] + 40), -40)
        if side == 'bottom': pos = (randint(-40, self._screen_size[0] + 40), self._screen_size[1] + 40)
        self.enemies.append(Bug((40, 40), pos, self.player.screen_pos))

    def get_score_surface(self):
        points = self.player.points
        font = pg.font.SysFont('Arial', 36)
        text = font.render("SCORE: "+str(points), False, (50, 50, 50))
        return text

    def get_activated_bonuses_surface(self):
        bonus = [i for i in self.activated_bonuses if repr(i) in ("A", "S", "D") ]
        surf = pg.Surface((340, len(bonus) * 40))
        surf.set_colorkey("black")
        step = 0
        for bonus in self.activated_bonuses:
            if repr(bonus) == "T":
                continue
            surf.blit(bonus.surface, (0, step))
            pg.draw.rect(surf, (50, 150, 50), (40, step + 5, bonus.time - bonus.timer, 30))
            pg.draw.rect(surf, (50, 50, 50), (40, step + 5, bonus.time, 30), 1)
            step += 40

        return surf

    def get_start_menu(self):
        font = pg.font.SysFont('Arial', 36)
        surf = pg.Surface(self._screen_size)
        title_font = pg.font.SysFont('Arial', 400)
        title = title_font.render("WARRIOR", False, (150, 150, 150))
        surf.blit(title, self.menu_title_pos)
        vertical = 0
        for button_text in self.menu_buttons:
            if self.menu_buttons.index(button_text) == self.menu_active_button:
                color = (150, 150, 250)
            else:
                color = (150, 150, 150)
            text = font.render(button_text, False, color)
            surf.blit(text, (self._screen_size[0] / 2 - text.get_width() / 2, self._screen_size[1] - 200 + vertical))
            if len(self.menu_buttons_pos) < len(self.menu_buttons):
                self.menu_buttons_pos.append((self._screen_size[0] / 2 - text.get_width() / 2,
                                         self._screen_size[1] - 200 + vertical, text.get_width(), text.get_height()))
            vertical += 50
        version_font = pg.font.SysFont('Arial', 20)
        version = version_font.render("ver: " + self.version, False, (150, 150, 150))
        surf.blit(version, (self._screen_size[0] / 2 - version.get_width() / 2, self._screen_size[1] - 30))
        return surf

    def get_results_menu(self, current=False):
        font = pg.font.SysFont('Arial', 36)
        surf = pg.Surface(self._screen_size)
        with open('results\\results.txt') as results_file:
            values = results_file.read().split("\n")
            vertical = 0
            for i in range(len(values)):
                if current == int(values[i]):
                    color = (150, 250, 150)
                else:
                    color = (150, 150, 150)
                text = font.render(str(i+1) + ": " + values[i].rstrip(), False, color)
                surf.blit(text, (self._screen_size[0] / 2 - text.get_width() / 2, 100 + vertical))
                vertical += 50
        if current:
            text = font.render("Your Score: " + str(current), False, color)
            surf.blit(text, (self._screen_size[0] / 2 - text.get_width() / 2, self._screen_size[1] - 300))

        vertical = 0
        for button_text in self.results_menu_buttons:
            if self.results_menu_buttons.index(button_text) == self.results_menu_active_button:
                color = (150, 150, 250)
            else:
                color = (150, 150, 150)
            text = font.render(button_text, False, color)
            surf.blit(text, (self._screen_size[0] / 2 - text.get_width() / 2, self._screen_size[1] - 100 + vertical))
            if len(self.results_menu_buttons_pos) < len(self.results_menu_buttons):
                self.results_menu_buttons_pos.append((self._screen_size[0] / 2 - text.get_width() / 2,
                                              self._screen_size[1] - 100 + vertical, text.get_width(),
                                              text.get_height()))
            vertical += 50

        return surf

    def get_game_menu(self, current=False):
        font = pg.font.SysFont('Arial', 36)
        surf = pg.Surface(self._screen_size)
        surf.set_colorkey("black")
        text = font.render("GAME PAUSED", False, (200, 200, 200))
        surf.blit(text, (self._screen_size[0] / 2 - text.get_width() / 2, self._screen_size[1] / 2))
        vertical = 0
        for button_text in self.game_menu_buttons:
            if self.game_menu_buttons.index(button_text) == self.game_menu_active_button:
                color = (150, 150, 250)
            else:
                color = (150, 150, 150)
            text = font.render(button_text, False, color)
            surf.blit(text, (self._screen_size[0] / 2 - text.get_width() / 2, self._screen_size[1] - 100 + vertical))
            if len(self.game_menu_buttons_pos) < len(self.game_menu_buttons):
                self.game_menu_buttons_pos.append((self._screen_size[0] / 2 - text.get_width() / 2,
                                                   self._screen_size[1] - 100 + vertical,
                                                   text.get_width(),
                                                   text.get_height()))
            vertical += 50
        return surf

    def end_game(self):
        points = self.player.points
        if points > 0:
            with open('results\\results.txt', 'r') as results_file:
                values = [int(i) for i in results_file.read().split("\n")]
            if min(values) < points:
                values.append(int(points))
                values.sort(reverse=True)
                values = values[:10]
                values = [str(i) for i in values]
                values = "\n".join(values)
                with open('results\\results.txt', 'w') as results_file:
                    results_file.write(values)
            self.results_menu_surface = self.get_results_menu(points)

        self.player = Player((40, 40), (self._screen_size[0] / 2, self._screen_size[1] / 2))
        self.patrons = []
        self.enemies = [Bug((40, 40), (1000, 100), (self._screen_size[0] / 2, self._screen_size[1] / 2))]
        self.bonuses = []
        self.able_bonuses = [AttackBonus, SpeedBonus]
        self.enemy_timer = 0
        self.enemy_time = 60
        self.score_surface = self.get_score_surface()
        Bug.speed = 1
        pg.mixer.music.load('sounds\\menu.mp3')
        pg.mixer.music.play()





pg.init()
game = Game()
game.start_game()
