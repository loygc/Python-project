__author__ = "susmote"

import pygame
import time
import random
from pygame.locals import *


enemy_list = pygame.sprite.Group()


class Base(pygame.sprite.Sprite):
    def __init__(self, screen_temp, x, y, image_name):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = pygame.image.load(image_name)
        self.bullet_list = []


class BasePlane(Base):
    # 飞机基类
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if bullet.judge():
                self.bullet_list.remove(bullet)


class HeroPlane(BasePlane):
    # 玩家飞机类
    def __init__(self, screen_temp):
        BasePlane.__init__(self, screen_temp, 120, 420, "./img/hero1.png")
        self.stop = True
        self.direction = None
        self.image = pygame.transform.scale(self.image, (int(100 * 0.6), int(124 * 0.6)))

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if bullet.judge():
                self.bullet_list.remove(bullet)
            for enemy in enemy_list:
                bullet.hit_plane(enemy)

    def move(self):
        if not self.stop:
            if self.direction == "left":
                self.x -= 3
            if self.direction == "right":
                self.x += 3
            if self.direction == "up":
                self.y -= 3
            if self.direction == "down":
                self.y += 3

    def fire(self):
        self.bullet_list.append(Bullet(self.screen, self.x, self.y))


class EnemyPlane(BasePlane):
    # 敌机类
    def __init__(self, screen_temp):
        BasePlane.__init__(self, screen_temp, 0, 0, "./img/enemy0.png")
        self.live = True
        self.image = pygame.transform.scale(self.image, (int(51*0.6), int(39*0.6)))
        self.direction = "right"

        self.images = [pygame.image.load("./img/enemy0_down1.png"),
                       pygame.image.load("./img/enemy0_down2.png"),
                       pygame.image.load("./img/enemy0_down3.png"),
                       pygame.image.load("./img/enemy0_down4.png")]
        self.step = 0
        self.rect = self.image.get_rect()

    def move(self):

        if self.direction == "right":
            self.x += 3
        elif self.direction == "left":
            self.x -= 3

        if self.x > int(0.6*480 - 0.6*51):
            self.direction = "left"
        elif self.x < 0:
            self.direction = "right"

    def fire(self):

        random_num = random.randint(1, 100)
        if random_num == 25 or random_num == 50 or random_num == 75:
            self.bullet_list.append(EnemyBullet(self.screen, self.x, self.y))

    def explode(self):
        while self.live:
            if self.step == len(self.images):
                self.live = False
            else:
                self.image = self.images[self.step]
                self.image = pygame.transform.scale(self.image, (int(51 * 0.6), int(39 * 0.6)))
                time.sleep(0.03)
                pygame.display.update()
                self.screen.blit(self.image, (self.x, self.y))
                self.step += 1


class BaseBullet(Base):
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))


class Bullet(BaseBullet):
    # 子弹类
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x+24, y-11, "./img/bullet.png")
        self.image = pygame.transform.scale(self.image, (int(22 * 0.6), int(22 * 0.6)))
        self.rect = self.image.get_rect()

    def move(self):
        self.y -= 5

    def judge(self):
        if self.y < 0:
            return True
        else:
            return False

    def hit_plane(self, enemy):
        if self.judge():
            # 获取敌机的坐标
            print("敌机的坐标 ：",enemy.x, enemy.y)
            # 获取子弹的坐标
            print("子弹的坐标 ：", self.x, self.y)
            # 获取敌机的实时区域
            startX = enemy.x
            endX = enemy.x+(enemy.rect.width)
            print(startX)
            print(endX)
            if self.x > startX and self.x < endX:
                print(enemy)
                enemy.explode()





class EnemyBullet(BaseBullet):
    # 敌机子弹类
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x+12, y+17, "./img/bullet1.png")
        self.image = pygame.transform.scale(self.image, (int(9 * 0.6), int(21 * 0.6)))

    def move(self):
        self.y += 3

    def judge(self):
        if self.y > int(0.6*852):
            return True
        else:
            return False


def main():

    screen = pygame.display.set_mode((int(0.6*480), int(0.6*852)), 0, 32)

    pygame.display.set_caption("打飞机游戏  by susmote")

    background = pygame.image.load("./img/background.png")
    background = pygame.transform.scale(background, (int(0.6*480), int(0.6*852)))

    hero = HeroPlane(screen)

    enemy_list.add(EnemyPlane(screen))


    while True:

        screen.blit(background, (0, 0))

        hero.display()

        hero.move()

        for enemy in enemy_list:
            if enemy.live:
                enemy.display()
                enemy.move()
                enemy.fire()
        if len(enemy_list) < 1:
            enemy_list.add(EnemyPlane(screen))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == QUIT:
                print("exit")
                exit()

            elif event.type == KEYDOWN:
                if event.key == K_a or event.key == K_LEFT:
                    print('left')
                    hero.stop = False
                    hero.direction = "left"
                elif event.key == K_d or event.key == K_RIGHT:
                    print('right')
                    hero.stop = False
                    hero.direction = "right"
                elif event.key == K_w or event.key == K_UP:
                    print('up')
                    hero.stop = False
                    hero.direction = "up"
                elif event.key == K_s or event.key == K_DOWN:
                    print('down')
                    hero.stop = False
                    hero.direction = "down"
                elif event.key == K_SPACE:
                    print('space')
                    hero.fire()
                elif event.key == K_ESCAPE:
                    print("exit")
                    exit()
            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_a:
                    hero.stop = True
                if event.key == K_RIGHT or event.key == K_d:
                    hero.stop = True
                if event.key == K_UP or event.key == K_w:
                    hero.stop = True
                if event.key == K_DOWN or event.key == K_s:
                    hero.stop = True

        time.sleep(0.01)


if __name__ == "__main__":
    main()
