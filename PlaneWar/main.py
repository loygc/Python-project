__author__ = "susmote"

import pygame
import time
import random
from pygame.locals import *


class Base(object):
    def __init__(self, screen_temp, x, y, image_name):
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
        self.image = pygame.transform.scale(self.image, (int(100 * 0.6), int(124 * 0.6)))

    def move_left(self):
        self.x -= 3

    def move_right(self):
        self.x += 3

    def move_up(self):
        self.y -= 3

    def move_down(self):
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
        if self.step == len(self.images):
            self.live = False
        else:
            self.image = self.images[self.step]
            self.image = pygame.transform.scale(self.image, (int(51 * 0.6), int(39 * 0.6)))
            time.sleep(0.05)
            self.screen.blit(self.image, (self.x, self.y))
            self.step += 1
            print(self.step)


class BaseBullet(Base):
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))


class Bullet(BaseBullet):
    # 子弹类
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x+24, y-11, "./img/bullet.png")
        self.image = pygame.transform.scale(self.image, (int(22 * 0.6), int(22 * 0.6)))

    def move(self):
        self.y -= 5

    def judge(self):
        if self.y < 0:
            return True
        else:
            return False


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

    enemy = EnemyPlane(screen)

    while True:

        screen.blit(background, (0, 0))

        hero.display()

        if enemy.live:
            enemy.display()
            enemy.move()
            enemy.fire()

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == QUIT:
                print("exit")
                exit()

            elif event.type == KEYDOWN:
                if event.key == K_a or event.key == K_LEFT:
                    print('left')
                    hero.move_left()
                elif event.key == K_d or event.key == K_RIGHT:
                    print('right')
                    hero.move_right()
                elif event.key == K_w or event.key == K_UP:
                    print('up')
                    hero.move_up()
                elif event.key == K_s or event.key == K_DOWN:
                    print('down')
                    hero.move_down()
                elif event.key == K_SPACE:
                    print('space')
                    hero.fire()
                elif event.key == K_ESCAPE:
                    print("exit")
                    exit()
                elif event.key == K_b:
                    while enemy.live:
                        enemy.explode()
                        pygame.display.update()

        time.sleep(0.01)


if __name__ == "__main__":
    main()
