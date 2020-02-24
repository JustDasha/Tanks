import pygame
import os
import sys
import pygame_textinput
import pyganim

import random

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Танки')

clock = pygame.time.Clock()
FPS = 50
shoot_right = False
shoot_left = False
shoot_up = False
shoot_down = False



def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('IMAGE', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    intro_text = ["ТАНКИ",
                  "Добро пожаловать в игру!",
                  "Введите имя игрока"]

    fon = pygame.transform.scale(load_image('fon1.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def end_screen():
    intro_text = ["Поздравляем",
                  "Вы победили"]

    fon = pygame.transform.scale(load_image('fon1.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def load_level(filename):
    filename = "TEXT/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


bricks = [load_image('brick1.png'), load_image('brick2.png'), load_image('brick3.png'),
          load_image('brick4.png'), load_image('brick5.png'), load_image('brick6.png'),
          load_image('brick7.png'), load_image('brick8.png'), load_image('brick9.png')]
brick = random.choice(bricks)
tile_images = {'wall': brick, 'empty': load_image('empty.png'), 'water': load_image('water.png'),
               'flagok': load_image('flagok.png', -1)}
player_image = load_image('blue_tank.png', -1)
enemy_image = load_image('en_tank.png', -1)
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bricks_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                a = Tile('wall', x, y)
                bricks_group.add(a)
            elif level[y][x] == '?':
                Tile('water', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                player_group.add(new_player)
            elif level[y][x] == 'e':
                Tile('empty', x, y)
                enem = Enemy(x, y)
                enemy_group.add(enem)
            elif level[y][x] == 'f':
                Tile('flagok', x, y)
                flag_x = x
                flag_y = y
    return [new_player, x, y], flag_x, flag_y


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            running = False
    start_screen()
    pygame.display.flip()
    clock.tick(FPS)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = player_image
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def get_coord(self):
        return self.x, self.y

    def move_player_down(self, x, y):
        COLOR = "#888888"
        ANIMATION_DOWN = [('%s/IMAGE/tank/down1.png' % ICON_DIR),
                    ('%s/IMAGE/tank/down3.png' % ICON_DIR)]
        boltAnim = []
        for anim in ANIMATION_DOWN:
            boltAnim.append((anim, 0.1))
        self.boltAnimDown = pyganim.PygAnimation(boltAnim)
        self.boltAnimDown.play()
        self.image.fill(pygame.Color(COLOR))
        self.boltAnimDown.blit(self.image, (0, 0))
        new = Player(self.x + x, self.y + y)
        collide = pygame.sprite.spritecollide(new, bricks_group, False)
        collide_with_en = pygame.sprite.spritecollide(new, enemy_group, False)
        if collide or collide_with_en:
            y = 0        
        self.x += x
        self.y += y
        self.rect = self.image.get_rect().move(tile_width * self.x, tile_height * self.y)

    def move_player_up(self, x, y):
        COLOR = "#888888"
        ANIMATION_UP = [('%s/IMAGE/tank/up1.png' % ICON_DIR),
                    ('%s/IMAGE/tank/up3.png' % ICON_DIR)]
        boltAnim = []
        for anim in ANIMATION_UP:
            boltAnim.append((anim, 0.1))
        self.boltAnimUp = pyganim.PygAnimation(boltAnim)
        self.boltAnimUp.play()
        self.image.fill(pygame.Color(COLOR))
        self.boltAnimUp.blit(self.image, (0, 0))
        new = Player(self.x + x, self.y + y)
        collide = pygame.sprite.spritecollide(new, bricks_group, False)
        collide_with_en = pygame.sprite.spritecollide(new, enemy_group, False)
        if collide or collide_with_en:
            y = 0        
        self.x += x
        self.y += y
        self.rect = self.image.get_rect().move(tile_width * self.x, tile_height * self.y)

    def move_player_left(self, x, y):
        COLOR = "#888888"
        ANIMATION_LEFT = [('%s/IMAGE/tank/l1.png' % ICON_DIR),
                    ('%s/IMAGE/tank/l3.png' % ICON_DIR)]
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, 0.1))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.image.fill(pygame.Color(COLOR))
        self.boltAnimLeft.blit(self.image, (0, 0))
        new = Player(self.x + x, self.y + y)
        collide = pygame.sprite.spritecollide(new, bricks_group, False)
        collide_with_en = pygame.sprite.spritecollide(new, enemy_group, False)
        if collide or collide_with_en:
            x = 0
        self.x += x
        self.y += y
        self.rect = self.image.get_rect().move(tile_width * self.x, tile_height * self.y)

    def move_player_right(self, x, y):
        COLOR = "#888888"
        ANIMATION_RIGHT = [('%s/IMAGE/tank/r1.png' % ICON_DIR),
                    ('%s/IMAGE/tank/r3.png' % ICON_DIR)]
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, 0.1))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.image.fill(pygame.Color(COLOR))
        self.boltAnimRight.blit(self.image, (0, 0))
        if self.rect.right > WIDTH:
            x = 0
        new = Player(self.x + x, self.y + y)
        collide = pygame.sprite.spritecollide(new, bricks_group, False)
        collide_with_en = pygame.sprite.spritecollide(new, enemy_group, False)
        if collide or collide_with_en:
            x = 0
        self.x += x
        self.y += y
        self.rect = self.image.get_rect().move(tile_width * self.x, tile_height * self.y)

    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = enemy_image
        self.x = pos_x
        self.y = pos_y
        self.kill = False
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def get_coord(self):
        return (self.x, self.y)

    def move_player_down(self, x, y):
        COLOR = "#888888"
        ANIMATION_DOWN = [('%s/IMAGE/tank/end1.png' % ICON_DIR),
                          ('%s/IMAGE/tank/end3.png' % ICON_DIR)]
        boltAnim = []
        for anim in ANIMATION_DOWN:
            boltAnim.append((anim, 0.1))
        self.boltAnimDown = pyganim.PygAnimation(boltAnim)
        self.boltAnimDown.play()
        self.image.fill(pygame.Color(COLOR))
        self.boltAnimDown.blit(self.image, (0, 0))
        self.x += x
        self.y += y
        self.rect = self.image.get_rect().move(tile_width * self.x, tile_height * self.y)

    def move_player_up(self, x, y):
        COLOR = "#888888"
        ANIMATION_UP = [('%s/IMAGE/tank/enu1.png' % ICON_DIR),
                        ('%s/IMAGE/tank/enu3.png' % ICON_DIR)]
        boltAnim = []
        for anim in ANIMATION_UP:
            boltAnim.append((anim, 0.1))
        self.boltAnimUp = pyganim.PygAnimation(boltAnim)
        self.boltAnimUp.play()
        self.image.fill(pygame.Color(COLOR))
        self.boltAnimUp.blit(self.image, (0, 0))
        self.x += x
        self.y += y
        self.rect = self.image.get_rect().move(tile_width * self.x, tile_height * self.y)

    def move_player_left(self, x, y):
        COLOR = "#888888"
        ANIMATION_LEFT = [('%s/IMAGE/tank/enl1.png' % ICON_DIR),
                          ('%s/IMAGE/tank/enl3.png' % ICON_DIR)]
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, 0.1))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.image.fill(pygame.Color(COLOR))
        self.boltAnimLeft.blit(self.image, (0, 0))
        self.x += x
        self.y += y
        self.rect = self.image.get_rect().move(tile_width * self.x, tile_height * self.y)

    def move_player_right(self, x, y):
        COLOR = "#888888"
        ANIMATION_RIGHT = [('%s/IMAGE/tank/enr1.png' % ICON_DIR),
                           ('%s/IMAGE/tank/enr3.png' % ICON_DIR)]
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, 0.1))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        self.image.fill(pygame.Color(COLOR))
        self.boltAnimRight.blit(self.image, (0, 0))
        self.x += x
        self.y += y
        self.rect = self.image.get_rect().move(tile_width * self.x, tile_height * self.y)

    def move(self, x, y):
        new = Enemy(self.x + x, self.y + y)
        collide = pygame.sprite.spritecollide(new, bricks_group, False)
        collide_with_en = pygame.sprite.spritecollide(new, player_group, False)
        if not(collide or collide_with_en):
            self.x += x
            self.y += y
        self.rect = self.image.get_rect().move(tile_width * self.x, tile_height * self.y)

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        BLUE = (255, 255, 0)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2, 2))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        if shoot_up:
            self.rect.bottom = y
            self.rect.centerx = x
        if shoot_down:
            self.rect.bottom = y + 40
            self.rect.centerx = x
        if shoot_left:
            self.rect.bottom = y + 20
            self.rect.centerx = x - 20
        if shoot_right:
            self.rect.bottom = y + 20
            self.rect.centerx = x + 20

    def update(self):
        if shoot_up:
            self.rect.y -= 10
            if self.rect.bottom < 0:
                self.kill()
            hit = pygame.sprite.groupcollide(bullets, bricks_group, False,  False)
            if hit:
                self.kill()
        elif shoot_down:
            self.rect.y += 10
            if self.rect.bottom > 600:
                self.kill()
            hit = pygame.sprite.groupcollide(bullets, bricks_group, False, False)
            if hit:
                self.kill()
        elif shoot_left:
            self.rect.x -= 10
            if self.rect.right < 0:
                self.kill()
            hit = pygame.sprite.groupcollide(bullets, bricks_group, False, False)
            if hit:
                self.kill()
        elif shoot_right:
            self.rect.x += 10
            if self.rect.left > 800:
                self.kill()
            hit = pygame.sprite.groupcollide(bullets, bricks_group, False, False)
            if hit:
                self.kill()


ICON_DIR = os.path.dirname(__file__) # путь к каталогу с файлами
ANIMATION_RIGHT = [('%s/IMAGE/tank/down1.png' % ICON_DIR),
            ('%s/IMAGE/tank/down3.png' % ICON_DIR)]


def move(st, x, y):
    x1, y1 = player.get_coord()
    for i in range(len(level)):
        level[i] = level[i].replace('@', '.')

    if st.lower() == 'down':
        player.move_player_down(x, y)
    if st.lower() == 'up':
        player.move_player_up(x, y)
    if st.lower() == 'left':
        player.move_player_left(x, y)
    if st.lower() == 'right':
        player.move_player_right(x, y)


levels = [load_level('map1.txt'), load_level('map2.txt'), load_level('map3.txt'), load_level('map4.txt'),
          load_level('map5.txt'), load_level('map6.txt')]
levels_for_game = random.sample(levels, 3)


def do_level():
    if levels_for_game:
        all_sprites.empty()
        tiles_group.empty()
        player_group.empty()
        bricks_group.empty()
        enemy_group.empty()
        player = None
        l = levels_for_game[0]
        s, flag1, flag2 = generate_level(l)
        levels_for_game.remove(l)
        return l, s, flag1, flag2


def random_move():
    napr = ['up', 'down', 'left', 'right']
    for enem in enemy_group:
        random_napr = random.choice(napr)
        if random_napr == 'up':
            enem.move(0, 0.5)
        elif random_napr == 'down':
            enem.move(0, -0.5)
        elif random_napr == 'left':
            enem.move(-0.5, 0)
        else:
            enem.move(0.5, 0)
        enem.shoot()


while levels_for_game:
    level, s, flag_x, flag_y = do_level()
    player, level_x, level_y = s[0], s[1], s[2]
    screen.fill((0, 0, 0))
    bullets = pygame.sprite.Group()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                random_move()
                if event.key == pygame.K_DOWN:
                    move("down", 0, 0.5)
                    shoot_right = False
                    shoot_left = False
                    shoot_up = False
                    shoot_down = True
                if event.key == pygame.K_UP:
                    move("up", 0, -0.5)
                    shoot_right = False
                    shoot_left = False
                    shoot_up = True
                    shoot_down = False
                if event.key == pygame.K_LEFT:
                    move("left", -0.5, 0)
                    shoot_right = False
                    shoot_left = True
                    shoot_up = False
                    shoot_down = False
                if event.key == pygame.K_RIGHT:
                    move("right", 0.5, 0)
                    shoot_right = True
                    shoot_left = False
                    shoot_up = False
                    shoot_down = False
                if event.key == pygame.K_SPACE:
                    player.shoot()
            if player.get_coord()[0] == flag_x and player.get_coord()[1] == flag_y:
                running = False
                break
        collide = pygame.sprite.spritecollide(player, bullets, False)
        if collide:
            running = False
        bullets.update()
        tiles_group.draw(screen)
        enemy_group.draw(screen)
        player_group.draw(screen)
        bullets.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if not(levels_for_game):
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run = False
        end_screen()
        pygame.display.flip()
        clock.tick(FPS)
pygame.quit()
sys.exit()
