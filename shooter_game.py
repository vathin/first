from pygame import *
from random import randint

clock = time.Clock()
FPS = 60
global points
points = 0
res = 0
global fl
fl = 0

class GameSprite(sprite.Sprite):
    def __init__(self,pl_image,x1,y1,speed,spriteW,spriteH):
        super().__init__()
        self.image = transform.scale(image.load(pl_image), (spriteW,spriteH))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x1
        self.rect.y = y1
        self.startx = x1
        self.starty = y1
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
    def player_movement(self):
        keyp = key.get_pressed()
        if keyp[K_LEFT]:
            if self.rect.x >=5:
                self.rect.x -= self.speed
        if keyp[K_RIGHT]:
            if self.rect.x <= 640:
                self.rect.x += self.speed
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            global fl
            fl += 1
            self.rect.x = (randint(1,128)*5)


        
    def change_speed(self, new_speed):
        self.speed = new_speed
    def Kill_toStart(self):
        global points
        self.rect.y = 0
        self.rect.x = (randint(1,128)*5)
        self.change_speed(randint(1,2))
        points +=1
    def restart(self):
        self.rect.y = self.starty
        self.rect.x = self.startx
    

class Bullet(GameSprite):
    '''def __init__(self, p_image, x, y, speed):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (10, 25))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y'''
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class Asteroid(GameSprite):
    def __init__(self,pl_image,x1,y1,speed,spriteW,spriteH,horisont_speed):
        super().__init__(pl_image,x1,y1,speed,spriteW,spriteH)
        self.image = transform.scale(image.load(pl_image), (spriteW,spriteH))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x1
        self.rect.y = y1
        self.horisont_speed = horisont_speed

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.horisont_speed
        if self.rect.y >= 500:
            self.kill()

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 40)

font2 = font.SysFont('Arial', 90)
youwin = font2.render('YOU WIN', True, (100,255,150))
youlose = font2.render('YOU LOSE', True, (255,100,100))
qtorestart = font1.render('press [q] to restart', True, (255,255,255))

win = display.set_mode((700,500))
display.set_caption('shooter_game')
enemygr = sprite.Group()
asteroidgr = sprite.Group()

background = transform.scale(image.load("galaxy.jpg"), (700,500))
player = GameSprite('spaceShip.png', 320, 380, 5, 85, 80)
for i in range(5):
    new_enemy = GameSprite('ufo.png', randint(1,128)*5, randint(0, 180), randint(1,2), 100, 50)
    enemygr.add(new_enemy)

new_asteroid = Asteroid('asteroid.png',randint(5, 650), 0, randint(1,3), randint(40, 70), randint(40,70), randint(-3,3))
asteroidgr.add(new_asteroid)
bulletgr = sprite.Group()




finish = False

game = True
while game:
    win.blit(background, (0,0))
    
    if not finish:
        
        player.player_movement()
        enemygr.update()
        bulletgr.update()
        asteroidgr.update()
        enemygr.draw(win)
        bulletgr.draw(win)
        player.reset()
        asteroidgr.draw(win)
            
            #bulletgr.bullet_movement()
        stat_fl = font1.render('Пропущено: ' + str(fl) + '/5', True, (255,255,255))
        stat_points = font1.render('Счёт: ' + str(points) + '/100', True, (255,255,255))

        win.blit(stat_fl, (2,50))
        win.blit(stat_points, (2, 10))

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                new_bullet = Bullet('bullet.png', player.rect.centerx, player.rect.top, 4, 10, 25)
                bulletgr.add(new_bullet)
                fire.play()
            elif e.key == K_q:
                for i in bulletgr:
                    i.kill()
                player.restart()
                for i in enemygr:
                    i.restart()
                for i in asteroidgr:
                    i.kill()
                points = 0
                fl = 0
                finish = False
    sprlist = sprite.groupcollide(
        enemygr, bulletgr, True, True
    )
    for i in sprlist:
        i.Kill_toStart()
        enemygr.add(i)
    sprlist2 = sprite.groupcollide(
        asteroidgr, bulletgr, True, True
    )
    sprlist3 = sprite.spritecollide(
        player, asteroidgr, False
    )
    if sprite.spritecollide(player, asteroidgr, False):
        finish = True
        res = 2
    if finish:
        win.blit(qtorestart, (235, 250))
        if res == 1:
            win.blit(youwin, (200,150))
        
        if res == 2:
            win.blit(youlose, (200,150))

    if points >= 100:
        res = 1
        finish = True
        
    elif fl >= 5:
        res = 2
        finish = True
        
    asteroidChance = randint(1,100)
    if asteroidChance == 99:
        new_asteroid = Asteroid('asteroid.png',randint(5, 650), 0, randint(1,3), randint(50, 70), randint(50,70), randint(-2,2))
        asteroidgr.add(new_asteroid)

    
    clock.tick(FPS)
    display.update()
