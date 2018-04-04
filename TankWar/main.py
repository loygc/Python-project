__author__ = "susmote"

import pygame
import sys
import time
from random import randint
from pygame.locals import *


#主窗口
class TankMain(object):

    width = 800
    heigh = 600
    wall = None
    my_tank = None
    my_tank_missile_list = []
    enemy_list = pygame.sprite.Group()
    explode_list = []
    enemy_missile_list = pygame.sprite.Group()
    # 开始游戏
    def startGame(self):

        # 模块初始化
        pygame.init()

        # 创建一个屏幕
        screen = pygame.display.set_mode((TankMain.width, TankMain.heigh), 0, 32)

        # 设置屏幕标题
        pygame.display.set_caption("坦克大战")

        TankMain.wall = Wall(screen, 80, 200, 30, 120)
        # 创建一个坦克
        TankMain.my_tank = My_Tank(screen)
        if len(TankMain.enemy_list) == 0:
            for i in range(1,6):
                TankMain.enemy_list.add(Enemy_Tank(screen))
        while True:
            if len(TankMain.enemy_list) < 5:
                TankMain.enemy_list.add(Enemy_Tank(screen))
            # 设置屏幕背景色
            screen.fill((0, 0, 0))
            # 显示左上角的文字
            for i,text in enumerate(self.write_text(),0):
                screen.blit(text, (0,5+(15*i)))
            TankMain.wall.display()
            TankMain.wall.hit_other()

            for enemy in TankMain.enemy_list:
                enemy.display()
                enemy.random_move()
                enemy.random_fire()
            for m in TankMain.my_tank_missile_list:
                if m.live:
                    m.display()
                    m.hit_tank()
                    m.move()
                else:
                    TankMain.my_tank_missile_list.remove(m)
            for m in TankMain.enemy_missile_list:
                if m.live:
                    m.display()
                    m.move()
                else:
                    TankMain.enemy_missile_list.remove(m)
            self.get_event(TankMain.my_tank,screen)
            if TankMain.my_tank:
                TankMain.my_tank.hit_enemy_missile()
            if TankMain.my_tank and TankMain.my_tank.live:
                TankMain.my_tank.display()
                TankMain.my_tank.move()
            else:
                TankMain.my_tank = None

            for explode in TankMain.explode_list:
                explode.display()
            #屏幕重置
            time.sleep(0.05)
            pygame.display.update()


    #获取事件
    def get_event(self,my_tank,screen):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.stopGame()
            if event.type == KEYDOWN and not my_tank and event.key == K_n:
                TankMain.my_tank = My_Tank(screen)
            if event.type == KEYDOWN and my_tank:
                if event.key == K_LEFT or event.key == K_a:
                    my_tank.direction = "L"
                    my_tank.stop = False
                if event.key == K_RIGHT or event.key == K_d:
                    my_tank.direction = "R"
                    my_tank.stop = False
                if event.key == K_UP or event.key == K_w:
                    my_tank.direction = "U"
                    my_tank.stop = False
                if event.key == K_DOWN or event.key == K_s:
                    my_tank.direction = "D"
                    my_tank.stop = False
                if event.key == K_ESCAPE:
                    self.stopGame()
                if event.key == K_SPACE:
                    m = my_tank.fire()
                    m.own = True
                    TankMain.my_tank_missile_list.append(m)
            if event.type == KEYUP and my_tank:
                if event.key == K_LEFT or event.key == K_a:
                    my_tank.stop = True
                if event.key == K_RIGHT or event.key == K_d:
                    my_tank.stop = True
                if event.key == K_UP or event.key == K_w:
                    my_tank.stop = True
                if event.key == K_DOWN or event.key == K_s:
                    my_tank.stop = True


    #结束游戏
    def stopGame(self):
        sys.exit()

    #显示文字
    def write_text(self):

        #定义字体
        font = pygame.font.SysFont(("华文中宋"), 15)

        #根据字体创建图像
        text_sf1 = font.render("敌方坦克数量为：%s"%len(TankMain.enemy_list), True, (255, 0, 0))
        text_sf2 = font.render("我方坦克炮弹的数量：%s" % len(TankMain.my_tank_missile_list), True, (255, 0, 0))
        return text_sf1,text_sf2

# 坦克大战游戏所有对象的所有父类
class BaseItem(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen

    # 显示坦克
    def display(self):
        self.image = self.images[self.direction]
        self.screen.blit(self.image, self.rect)


class Tank(BaseItem):
    width = 50
    height = 50

    def __init__(self,screen,left,top):
        super().__init__(screen)
        self.direction = "D"
        self.speed = 3 #移动速度
        self.images = {}   #所有图片
        self.images["L"] = pygame.image.load("images/p1tankL.gif")
        self.images["R"] = pygame.image.load("images/p1tankR.gif")
        self.images["U"] = pygame.image.load("images/p1tankU.gif")
        self.images["D"] = pygame.image.load("images/p1tankD.gif")
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True  #决定坦克的状态
        self.stop = False
        self.oldtop = self.rect.top
        self.oldleft = self.rect.left

    def stay(self):
        self.rect.top = self.oldtop
        self.rect.left = self.oldleft

    #坦克移动
    def move(self):
        if not self.stop:
            self.oldleft = self.rect.left
            self.oldtop = self.rect.top
            if self.direction == "L":
                if self.rect.left > 0:
                    self.rect.left -= self.speed
                else:
                    self.rect.left = 0
            elif self.direction == "R":
                if self.rect.left < TankMain.width:
                    self.rect.left += self.speed
                else:
                    self.rect.left = self.width

            if self.direction == "D":
                if self.rect.bottom < TankMain.width :
                    self.rect.top += self.speed
                else:
                    self.rect.top = TankMain.width
            elif self.direction == "U":
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.rect.top = 0


    def fire(self):
        m = Missile(self.screen, self)
        return m

class My_Tank(Tank):
    def __init__(self, screen):
        super().__init__(screen, 275, 400)
        self.speed = 5
        self.stop = True
        self.live = True
    def hit_enemy_missile(self):
        hit_list = pygame.sprite.spritecollide(self,TankMain.enemy_missile_list,False)
        for m in hit_list:
            m.live = False
            TankMain.enemy_missile_list.remove(m)
            self.live = False
            explode = Explode(self.screen, self.rect)
            TankMain.explode_list.append(explode)



class Enemy_Tank(Tank):
    def __init__(self,screen):
        self.speed = 3
        super().__init__(screen,randint(2,7)*100, 200)
        self.images = {}  # 所有图片
        self.images["L"] = pygame.image.load("images/p2tankL.gif")
        self.images["R"] = pygame.image.load("images/p2tankR.gif")
        self.images["U"] = pygame.image.load("images/p2tankF.gif")
        self.images["D"] = pygame.image.load("images/p2tankD.gif")
        self.step = 8
        self.get_random_direction()

    def get_random_direction(self):
        r = randint(0, 4)
        if r == 4:
            self.stop = True
        elif r == 1:
            self.direction = "L"
            self.stop = False
        elif r == 2:
            self.direction = "R"
            self.stop = False
        elif r == 0:
            self.direction = "D"
            self.stop = False
        elif r == 3:
            self.direction = "U"
            self.stop = False
    #按照一个确定的随机方向，连续移动8步，然后才能改变方向
    def random_move(self):
        if self.live:
            if self.step == 0:
                self.get_random_direction()
                self.step = 6
            else:
                self.move()
                self.step -= 1



    def random_fire(self):
        r = randint(0, 50)
        if r == 10 :
            m = self.fire()
            TankMain.enemy_missile_list.add(m)
        else:
            return


class Missile(BaseItem):
    width = 15
    height = 15
    def __init__(self,screen, tank):
        super().__init__(screen)
        self.tank = tank
        self.direction = tank.direction
        self.speed = 12  # 移动速度
        self.images = {}  # 所有图片
        self.images["L"] = pygame.image.load("images/22.gif")
        self.images["R"] = pygame.image.load("images/22.gif")
        self.images["U"] = pygame.image.load("images/22.gif")
        self.images["D"] = pygame.image.load("images/22.gif")
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = tank.rect.left + (tank.width - self.width) / 2
        self.rect.top = tank.rect.top + (tank.height - self.height) / 2
        self.live = True
        self.own = False

    def move(self):
        if self.live:
            if self.direction == "L":
                if self.rect.left > 0:
                    self.rect.left -= self.speed
                else:
                    self.live = False
            elif self.direction == "R":
                if self.rect.left < TankMain.width:
                    self.rect.left += self.speed
                else:
                    self.live = False

            if self.direction == "D":
                if self.rect.bottom < TankMain.width :
                    self.rect.top += self.speed
                else:
                    self.live = False
            elif self.direction == "U":
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.live = False

    def display(self):
        if self.live:
            self.image = self.images[self.direction]
            self.screen.blit(self.image,self.rect)

    def hit_tank(self):
        if self.own:
            hit_list = pygame.sprite.spritecollide(self, TankMain.enemy_list, False)
            for e in hit_list:
                e.live = False
                TankMain.enemy_list.remove(e)
                self.live = False
                explode = Explode(self.screen, e.rect)
                TankMain.explode_list.append(explode)

class Explode(BaseItem):
    def __init__(self, screen, rect):
        super().__init__(screen)
        self.live = True
        self.images = [pygame.image.load("images/blast1.gif"),
                       pygame.image.load("images/blast2.gif"),
                       pygame.image.load("images/blast3.gif"),
                       pygame.image.load("images/blast4.gif"),
                       pygame.image.load("images/blast5.gif"),
                       pygame.image.load("images/blast6.gif"),
                       pygame.image.load("images/blast7.gif"),
                       pygame.image.load("images/blast8.gif")]
        self.step = 0
        self.rect = rect

    def display(self):
        if self.live:
            if self.step == len(self.images):
                self.live = False
            else:
                self.image = self.images[self.step]
                self.screen.blit(self.image, self.rect)
                self.step += 1
        else:
            pass

class Wall(BaseItem):
    def __init__(self, screen, left, top, width, height):
        super().__init__(screen)
        self.rect = Rect(left, top, width, height)
        self.color = (255, 0, 0)
    def display(self):
        self.screen.fill(self.color, self.rect)


    def hit_other(self):
        if TankMain.my_tank:
            is_hit = pygame.sprite.collide_rect(self,TankMain.my_tank)
            if is_hit:
                TankMain.my_tank.stop = True
                TankMain.my_tank.stay()

        if len(TankMain.enemy_list) != 0:
            hit_list = pygame.sprite.spritecollide(self, TankMain.enemy_list, False)
            for e in hit_list:
                e.stop = True
                e.stay()

        if len(TankMain.enemy_missile_list) != 0:
            hit_list = pygame.sprite.spritecollide(self, TankMain.enemy_missile_list, False)
            for e in hit_list:
                e.live = False
        if len(TankMain.my_tank_missile_list) != 0:
            hit_list = pygame.sprite.spritecollide(self, TankMain.my_tank_missile_list, False)
            for e in hit_list:
                e.live = False
game = TankMain()
game.startGame()