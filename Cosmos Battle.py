import pygame
import pygame_gui
import random
from moviepy.editor import *
import sys
import os



pygame.init()
os.chdir('maps')
map = random.choice(os.listdir())
os.chdir('..')
with open(f'maps/{map}', 'r') as mapFile:
    Level_map = [list(line.strip()) for line in mapFile]
with open('info.txt', 'r') as infofile:
    data = infofile.read()
Cell_size = 60
pygame.display.set_caption('Pygame_project')
size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
print(size)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

pygame.mixer.music.load('music/background_music_menu.mp3')
sound_step = pygame.mixer.Sound('music/Foot.wav')
background = pygame.image.load('images/background/BingWallpaper_2.jpg')
menu_background = pygame.image.load('images/background/BingWallpaper_5.jpg')
unites_background = pygame.image.load('images/background/unites_background.jpg')
LEFT = width // 8
TOP = height // 8
Coords_for_players = []
Walls_tile = []
floor = []
end_game = 0

for x in range(len(Level_map)):
    for y in range(len(Level_map[x])):
        if Level_map[x][y] == '#':
            Walls_tile.append((x, y))
        elif Level_map[x][y] == '@' or Level_map[x][y] == '!' or Level_map[x][y] == '?' or Level_map[x][y] == '$'\
                or Level_map[x][y] == '%' or Level_map[x][y] == '&':
            Coords_for_players.append((x, y))
        else:
            floor.append((x, y))
Save_walls = Walls_tile.copy()


manager = pygame_gui.UIManager((width, height))
btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((LEFT, (Cell_size * len(Level_map[0]) + 120)), (120, 30)),
                                             text='Exit',
                                             manager=manager)

healthbar = pygame_gui.elements.UIScreenSpaceHealthBar(relative_rect=pygame.Rect((len(Level_map)
                                                       * 60 + 60, (Cell_size * len(Level_map[0]) + 120)), (120, 30)),
                                                       manager=manager)
label_goals = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((len(Level_map)
                                                       * 60 + 60, (Cell_size * len(Level_map[0]) + 180)), (120, 30)),
                                                       manager=manager, text='')


manager_2 = pygame_gui.UIManager((width, height))
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width // 2 - 110, 320), (220, 50)),
                                             text='Начать игру',
                                             manager=manager_2)
info_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width // 2 - 110, 400), (220, 50)),
                                             text='Как играть?',
                                             manager=manager_2)
units_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width // 2 - 110, 480), (220, 50)),
                                             text='Игровые юниты',
                                             manager=manager_2)
exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width // 2 - 110, 560), (220, 50)),
                                             text='Выход',
                                             manager=manager_2)

unites_manager = pygame_gui.UIManager((width, height))
unites_exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width // 2 - 110, height - (height // 8)),
                                                                            (220, 50)),
                                             text='Выход',
                                             manager=unites_manager)
unites_easy_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(width // 2 - 180, 120, 360, 60),
                                          manager=unites_manager, text='Легкий боец')
unites_middle_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(width // 2 - 180, 360, 360, 60),
                                          manager=unites_manager, text='Средний боец')
unites_hard_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(width // 2 - 180, 600, 360, 60),
                                          manager=unites_manager, text='Тяжелый боец')

manager_3 = pygame_gui.UIManager((width, height))
end_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((width // 2 - 260, 260), (520, 50)),
                                             text='',
                                             manager=manager_3)

end_exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width // 2 - 100, 400), (220, 50)),
                                             text='Выход',
                                             manager=manager_3)


class Label:
    def __init__(self):
        self.left = LEFT
        self.top = TOP
        self.count = 0

    def set_view(self, left, top):
        self.left = left
        self.top = top

    def render(self):
        font = pygame.font.Font('20354.otf', 100)
        text = font.render('Cosmos battle', True, pygame.Color('white'))
        screen.blit(text, (width // 2 - text.get_size()[0] // 2, 170))
        font2 = pygame.font.Font('20354.otf', 28)
        text2 = font2.render('Author:PYPROJECTGAMES', True, pygame.Color('black'))
        screen.blit(text2, (width // 2 - text2.get_size()[0] // 2, height - height // 8))


class Tile(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            filename)
        self.mask = pygame.mask.from_surface(self.image)
        for coords in Walls_tile:
            self.rect = self.image.get_rect(topleft=((coords[0] * 60) + LEFT, (coords[1] * 60) + TOP))
            break
        del Walls_tile[0]


class Go(pygame.sprite.Sprite):
    def __init__(self, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            filename)
        self.mask = pygame.mask.from_surface(self.image)
        for coords in floor:
            self.rect = self.image.get_rect(topleft=((coords[0] * 60) + LEFT, (coords[1] * 60) + TOP))
            break
        del floor[0]


class Player(pygame.sprite.Sprite):
    def __init__(self, filename, command, current_health, check, damage, health_capacity, moves, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            filename).convert_alpha()
        self.image.set_colorkey('white')
        self.mask = pygame.mask.from_surface(self.image)
        self.health_capacity = health_capacity
        self.current_health = current_health
        self.command = command
        self.save_moves = moves
        self.moves = moves
        self.damage = damage
        self.name = name
        for coords in Coords_for_players:
            Level_map[coords[0]][coords[1]] = '.'
            self.rect = self.image.get_rect(topleft=((coords[0] * 60) + LEFT, (coords[1] * 60) + TOP))
            break
        del Coords_for_players[0]
        self.count = False
        self.check_for_chess_move = check

    def move_down(self):
        if self.check_for_chess_move != 1:
            if self.moves > 0:
                sound_step.play()
                x = (self.rect.left - LEFT) // Cell_size
                y = (self.rect.top - TOP) // Cell_size
                if self.rect.top == (len(Level_map[x]) - 1) * Cell_size + TOP and Level_map[x][0] != '#':
                    self.rect[1] = TOP
                    self.moves -= 1

                elif self.rect.top == (len(Level_map[x]) - 1) * Cell_size + TOP and Level_map[x][0] == '#':
                    pass
                else:
                    if Level_map[x][y + 1] == '#':
                        pass
                    else:
                        self.rect[1] += 60
                        self.moves -= 1
            else:
                for sprt in all_sprites.sprites():
                    if sprt.command == self.command:
                        sprt.check_for_chess_move = 1
                    else:
                        sprt.check_for_chess_move = 0

    def move_up(self):
        if self.check_for_chess_move != 1:
            if self.moves > 0:
                sound_step.play()
                x = (self.rect.left - LEFT) // Cell_size
                y = (self.rect.top - TOP) // Cell_size
                if self.rect.top == TOP and Level_map[x][len(Level_map[x]) - 1] != '#':
                    self.rect[1] = (len(Level_map[x]) - 1) * Cell_size + TOP
                    self.moves -= 1
                elif self.rect.top == TOP and Level_map[x][len(Level_map[x]) - 1] == '#':
                    pass
                else:
                    if Level_map[x][y - 1] == '#':
                        pass
                    else:
                        self.rect[1] -= 60
                        self.moves -= 1
            else:
                for sprt in all_sprites.sprites():
                    if sprt.command == self.command:
                        sprt.check_for_chess_move = 1
                    else:
                        sprt.check_for_chess_move = 0

    def move_right(self):
        if self.check_for_chess_move != 1:
            if self.moves > 0:
                sound_step.play()
                x = (self.rect.left - LEFT) // Cell_size
                y = (self.rect.top - TOP) // Cell_size
                if self.rect.left == (len(Level_map) - 1) * Cell_size + LEFT and Level_map[0][y] != '#':
                    self.rect[0] = LEFT
                    self.moves -= 1
                elif self.rect.left == (len(Level_map) - 1) * Cell_size + LEFT and Level_map[0][y] == '#':
                    pass
                else:
                    if Level_map[x + 1][y] == '#':
                        pass
                    else:
                        self.rect[0] += 60
                        self.moves -= 1
            else:
                for sprt in all_sprites.sprites():
                    if sprt.command == self.command:
                        sprt.check_for_chess_move = 1
                    else:
                        sprt.check_for_chess_move = 0

    def move_left(self):
        if self.check_for_chess_move != 1:
            if self.moves > 0:
                sound_step.play()
                x = (self.rect.left - LEFT) // Cell_size
                y = (self.rect.top - TOP) // Cell_size
                if self.rect.left == LEFT and Level_map[len(Level_map) - 1][y] != '#':
                    self.rect[0] = (len(Level_map) - 1) * Cell_size + LEFT
                    self.moves -= 1
                elif self.rect.left == LEFT and Level_map[len(Level_map) - 1][y] == '#':
                    pass
                else:
                    if Level_map[x - 1][y] == '#':
                        pass
                    else:
                        self.rect[0] -= 60
                        self.moves -= 1
            else:
                for sprt in all_sprites.sprites():
                    if sprt.command == self.command:
                        sprt.check_for_chess_move = 1
                    else:
                        sprt.check_for_chess_move = 0

    def check(self, mouse):
        if self.rect.left <= mouse[0] <= self.rect.left + self.rect.size[0] and self.rect.top <= mouse[1]\
                <= self.rect.top + self.rect.size[0] and self.check_for_chess_move != 1:
            self.count = True
            self.moves = self.save_moves
            healthbar.set_sprite_to_monitor(sprite_to_monitor=sprt)
        else:
            self.count = False

    def attack(self, sprites, go):
        if self.check_for_chess_move != 1:
            if self.moves > 0:
                for sprt in sprites:
                    if go == 'down':
                        if self.rect.top == (len(Level_map[x]) - 1) * Cell_size + TOP and self.rect.left ==\
                                sprt.rect.left and sprt.command != self.command:
                            if sprt.current_health - self.damage <= 0:
                                sprt.current_health -= self.damage
                                sprt.kill()
                                self.moves -= 1
                                label_goals.set_text(f'Шагов: {self.moves}')
                            else:
                                sprt.current_health -= self.damage
                                self.moves -= 1
                                label_goals.set_text(f'Шагов: {self.moves}')
                            return True
                        elif self.rect.top + 60 == sprt.rect.top and self.rect.left == sprt.rect.left and sprt.command\
                                != self.command:
                            if sprt.current_health - self.damage <= 0:
                                sprt.current_health -= self.damage
                                sprt.kill()
                                self.moves -= 1
                            else:
                                sprt.current_health -= self.damage
                                self.moves -= 1
                                label_goals.set_text(f'Шагов: {self.moves}')
                            return True
                        elif self.rect.top + 60 == sprt.rect.top and self.rect.left == sprt.rect.left and\
                                sprt.command == self.command:
                            return True
                    elif go == 'up':
                        if self.rect.top == TOP and self.rect.left == sprt.rect.left and sprt.command != self.command:
                            if sprt.current_health - self.damage <= 0:
                                sprt.current_health -= self.damage
                                sprt.kill()
                                self.moves -= 1
                                label_goals.set_text(f'Шагов: {self.moves}')
                            else:
                                sprt.current_health -= self.damage
                                self.moves -= 1
                                label_goals.set_text(f'Шагов: {self.moves}')
                            return True
                        elif self.rect.top - 60 == sprt.rect.top and self.rect.left == sprt.rect.left and sprt.command\
                                != self.command:
                            if sprt.current_health - self.damage <= 0:
                                sprt.current_health -= self.damage
                                sprt.kill()
                                self.moves -= 1
                                label_goals.set_text(f'Шагов: {self.moves}')
                            else:
                                sprt.current_health -= self.damage
                                self.moves -= 1
                                label_goals.set_text(f'Шагов: {self.moves}')
                            return True
                        elif self.rect.top - 60 == sprt.rect.top and self.rect.left == sprt.rect.left and sprt.command\
                                == self.command:
                            return True
                    elif go == 'right':
                        if self.rect.left == (len(Level_map) - 1) * Cell_size + LEFT and self.rect.top == sprt.rect.top\
                                and sprt.command != self.command:
                            if sprt.current_health - self.damage <= 0:
                                sprt.current_health -= self.damage
                                sprt.kill()
                                self.moves -= 1
                                label_goals.set_text(f'Шагов: {self.moves}')
                            else:
                                sprt.current_health -= self.damage
                                self.moves -= 1
                                label_goals.set_text(f'Шагов: {self.moves}')
                            return True
                        elif self.rect.top == sprt.rect.top and self.rect.left + 60 == sprt.rect.left and\
                                sprt.command != self.command:
                            if sprt.current_health - self.damage <= 0:
                                sprt.current_health -= self.damage
                                sprt.kill()
                                self.moves -= 1
                                label_goals.set_text(f'Шагов: {self.moves}')
                            else:
                                sprt.current_health -= self.damage
                                self.moves -= 1
                                label_goals.set_text(f'Шагов: {self.moves}')
                            return True
                        elif self.rect.top == sprt.rect.top and self.rect.left + 60 == sprt.rect.left and sprt.command\
                                == self.command:
                            return True
                    elif go == 'left':
                        if self.rect.left == LEFT and self.rect.top == sprt.rect.top and sprt.command != self.command:
                            if sprt.current_health - self.damage <= 0:
                                sprt.current_health -= self.damage
                                sprt.kill()
                                self.moves -= 1
                                label_goals.set_text(f'Шагов: {self.moves}')
                            else:
                                sprt.current_health -= self.damage
                                self.moves -= 1
                                label_goals.set_text(f'Шагов: {self.moves}')

                            return True
                        elif self.rect.top == sprt.rect.top and self.rect.left - 60 == sprt.rect.left and sprt.command\
                                != self.command:
                            if sprt.current_health - self.damage <= 0:
                                sprt.current_health -= self.damage
                                sprt.kill()
                                self.moves -= 1
                                label_goals.set_text(f'Шагов: {self.moves}')
                            else:
                                sprt.current_health -= self.damage
                                self.moves -= 1
                                label_goals.set_text(f'Шагов: {self.moves}')
                            return True
                        elif self.rect.top == sprt.rect.top and self.rect.left - 60 == sprt.rect.left and \
                                sprt.command == self.command:
                            return True
            else:
                for sprt in all_sprites.sprites():
                    if sprt.command == self.command:
                        sprt.check_for_chess_move = 1
                    else:
                        sprt.check_for_chess_move = 0


class Point(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            filename).convert()
        self.image.set_colorkey('white')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=((x * Cell_size) + LEFT, (y * Cell_size) + TOP))
        self.count = 0

    def update(self, player):
        if not pygame.sprite.collide_rect(self, player) and self.count == 0:
            return True
        elif pygame.sprite.collide_rect(self, player):
            self.count += 1
            if player.current_health + 20 <= player.health_capacity:
                player.current_health += 20
            elif player.current_health + 20 > player.health_capacity:
                player.current_health = player.health_capacity
            return False
        else:
            return False


def randomiser():
    x = random.randint(0, len(Level_map) - 1)
    y = random.randint(0, len(Level_map[0]) - 1)
    if Level_map[x][y] == '#' or Level_map[x][y] == '@':
        return (4, 0)
    else:
        return (int(x), int(y))


first_command = pygame.sprite.Group()
second_command = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
cords1 = Coords_for_players.copy()
for i in cords1:                                                           #@, $, & - 1 команда ! % ? - 2 команда
    if Level_map[i[0]][i[1]] == '@':
        j = Player('images/unites/m_kontsepty1.png', 1, 50, 1, 10, 50, 10, 'easy')
        first_command.add(j)
        all_sprites.add(j)
    elif Level_map[i[0]][i[1]] == '!':
        k = Player('images/unites/m_kontsepty4.png', 2, 50, 0, 10, 50, 10, 'easy')
        second_command.add(k)
        all_sprites.add(k)
    elif Level_map[i[0]][i[1]] == '&':
        k = Player('images/unites/m_kontsepty3.png', 1, 200, 1, 40, 200, 3, 'hard')
        first_command.add(k)
        all_sprites.add(k)
    elif Level_map[i[0]][i[1]] == '?':
        k = Player('images/unites/m_kontsepty6.png', 2, 200, 0, 40, 200, 3, 'hard')
        second_command.add(k)
        all_sprites.add(k)
    elif Level_map[i[0]][i[1]] == '%':
        k = Player('images/unites/m_kontsepty5.png', 2, 100, 0, 25, 100, 5, 'medium')
        second_command.add(k)
        all_sprites.add(k)
    elif Level_map[i[0]][i[1]] == '$':
        k = Player('images/unites/m_kontsepty2.png', 1, 100, 1, 25, 100, 5, 'medium')
        first_command.add(k)
        all_sprites.add(k)


for x in range(len(Level_map)):
    for y in range(len(Level_map[x])):
        if Level_map[x][y] == '.':
            floor.append((x, y))

tiles = pygame.sprite.Group()
for _ in range(len(Walls_tile)):
    tiles.add(Tile('images/tiles/wall.png'))
for _ in range(len(floor)):
    tiles.add(Go('images/tiles/tile.png'))

win_command = ''
x, y = randomiser()
point = Point('images/tiles/bonus.png', x, y)
label = Label()
game_page = False
start_page = True
end_page = True
present = True
clock = pygame.time.Clock()
fps = 30
apple = True
game = True
units_page = False
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1)
while game:
    while start_page:
        clock.tick(fps)
        time_delta = clock.tick(fps) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        game_page = True
                        start_page = False
                    if event.ui_element == info_button:
                        window = pygame_gui.windows.UIMessageWindow(
                            rect=pygame.Rect((width // 2 - 260, 240), (520, 520)),
                            manager=manager_2,
                            html_message=f'{data}')
                    if event.ui_element == units_button:
                        start_page = False
                        units_page = True
                    if event.ui_element == exit_button:
                        game_page = False
                        start_page = False
                        end_page = False
                        sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            manager_2.process_events(event)
        manager_2.draw_ui(screen)
        manager_2.update(time_delta)
        pygame.display.flip()
        screen.blit(menu_background, (0, 0))
        label.render()
    pygame.mixer.music.stop()
    pygame.mixer.music.load('music/background_music_game.mp3')
    pygame.mixer.music.play(-1)
    while units_page:
        clock.tick(fps)
        time_delta = clock.tick(fps) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    units_page = False
                    game_page = False
                    end_page = False
                    start_page = True
        unites_manager.process_events(event)
        x = 0
        for i in range(1, 6 + 1):
            if i <= 3:
                u_img = pygame.image.load(f'images/unites/big_kon_{i}.png')
                screen.blit(u_img, (width - 240, 60 + x))
            if i == 3:
                x = 0
            elif i > 3:
                u_img = pygame.image.load(f'images/unites/big_kon_{i}.png')
                screen.blit(u_img, (0, -160 + x))
            x += 240
        pygame.display.flip()
        screen.blit(unites_background, (0, 0))
        unites_manager.draw_ui(screen)
        unites_manager.update(time_delta)
    while game_page:
        clock.tick(fps)
        time_delta = clock.tick(fps) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    game_page = False
                    end_page = False
                    start_page = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprt in all_sprites:
                    sprt.check(event.pos)
                    label_goals.set_text(f'Шагов: {sprt.moves}')
            if event.type == pygame.KEYDOWN:
                for sprt in all_sprites:
                    if sprt.count:
                        if event.key == pygame.K_s:
                            if not sprt.attack(all_sprites, 'down'):
                                label_goals.set_text(f'Шагов: {sprt.moves}')
                                sprt.move_down()
                                healthbar.set_sprite_to_monitor(sprite_to_monitor=sprt)
                                label_goals.set_text(f'Шагов: {sprt.moves}')
                        if event.key == pygame.K_w:
                            if not sprt.attack(all_sprites, 'up'):
                                label_goals.set_text(f'Шагов: {sprt.moves}')
                                sprt.move_up()
                                healthbar.set_sprite_to_monitor(sprite_to_monitor=sprt)
                                label_goals.set_text(f'Шагов: {sprt.moves}')
                        if event.key == pygame.K_d:
                            if not sprt.attack(all_sprites, 'right'):
                                label_goals.set_text(f'Шагов: {sprt.moves}')
                                sprt.move_right()
                                healthbar.set_sprite_to_monitor(sprite_to_monitor=sprt)
                                label_goals.set_text(f'Шагов: {sprt.moves}')
                        if event.key == pygame.K_a:
                            if not sprt.attack(all_sprites, 'left'):
                                label_goals.set_text(f'Шагов: {sprt.moves}')
                                sprt.move_left()
                                healthbar.set_sprite_to_monitor(sprite_to_monitor=sprt)
                                label_goals.set_text(f'Шагов: {sprt.moves}')
        manager.draw_ui(screen)
        for player in all_sprites:
            if point.update(player):
                screen.blit(point.image, point.rect)
            else:
                x, y = randomiser()
                point = Point('images/bonus.png', x, y)
        pygame.display.flip()
        manager.process_events(event)
        screen.blit(background, (0, 0))
        for sprite in tiles:
            screen.blit(sprite.image, sprite.rect)
        for sprt in all_sprites:
            screen.blit(sprt.image, sprt.rect)
            if len(all_sprites.sprites()) == 2:
                if all_sprites.sprites()[0].command == all_sprites.sprites()[1].command:
                    win_command = f'Люди одержали победу над роботами-захватчиками!'
                    running = False
                    end_running = True
            elif len(all_sprites.sprites()) == 1:
                win_command = f'Роботы разгромили отряд людей-космонавтов!'
                running = False
                end_running = True
        manager.update(time_delta)
    pygame.mixer.music.stop()
    pygame.mixer.music.load('music/background_music_menu.mp3')
    pygame.mixer.music.play(-1)
    while end_page:
        clock.tick(fps)
        time_delta = clock.tick(fps) / 1000.0
        if len(win_command) == 0:
            end_label.set_text('Роботы и люди пришли к мирному решению конфликта!')
        else:
            end_label.set_text(win_command)
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == end_exit_button:
                        end_page = False
        manager_3.process_events(event)
        pygame.display.flip()
        screen.blit(menu_background, (0, 0))
        manager_3.draw_ui(screen)
        manager_3.update(time_delta)
        label.render()
pygame.quit()
