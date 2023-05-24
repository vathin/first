from pygame import *
clock = time.Clock()
FPS = 60
global goal1
global goal2
goal1 = 0
goal2 = 0

win = display.set_mode((1000, 600))
display.set_caption('ping pong')
back_color = (70, 200, 250)
background = Surface((1000, 600))
background.fill(back_color)
class GameSprite(sprite.Sprite):
    def __init__(self, load_image:str, xpos:int, ypos:int, width:int, height:int, speed:int ):
        super().__init__()
        self.image = transform.scale(image.load(load_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
        self.xspeed = speed
        self.yspeed = speed
        self.startx = xpos
        self.starty = ypos
    def update(self):
        win.blit(self.image,(self.rect.x, self.rect.y))
    def ToStart(self):
        self.rect.x = self.startx
        self.rect.y = self.starty
        self.xspeed = self.speed
        self.yspeed = self.speed
class Player(GameSprite):
    def player_movement(self, Ydirection):
        if Ydirection == 'up' and self.rect.y >= 0:
            self.rect.y -= self.speed
        if Ydirection == 'down' and self.rect.y <= 490:
            self.rect.y += self.speed

class Ball(GameSprite):
    def ball_movement(self):
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed
        if self.rect.x >= 1000:
            global goal1
            self.rect.x = self.startx
            self.rect.y = self.starty
            self.xspeed = self.speed
            self.yspeed = self.speed
            goal1 += 1
        if self.rect.x <= 0:
            global goal2
            self.rect.x = self.startx
            self.rect.y = self.starty
            self.xspeed = self.speed
            self.yspeed = self.speed
            goal2 += 1
    def wall_bounce(self):
        if self.rect.y >= 560:
            self.rect.y -= 2
            self.yspeed = -self.yspeed
            self.ydir = 'down'
        if self.rect.y <= 0:
            self.rect.y += 2
            self.yspeed = -self.yspeed
            self.ydir = 'up'
    def player_bounce(self):
        self.xspeed = -self.xspeed
        self.rect.x += self.xspeed
        if self.xspeed >0:
            self.xspeed +=1
        elif self.xspeed <0:
            self.xspeed -=1
        if self.yspeed >0:
            self.yspeed +=1
        elif self.yspeed <0:
            self.yspeed -=1
        
font.init()
font1 = font.SysFont('Arial', 60)
font2 = font.SysFont('Arial', 70)
font3 = font.SysFont('Arial', 40)
pl1win = font2.render('Игрок 1 победил!', True, (250, 250, 100))
pl2win = font2.render('Игрок 2 победил!', True, (250, 250, 100))
points = font1.render(str(goal1) + ':' + str(goal2), True, (250, 250, 250))
spaceToRestart = font3.render('Нажмите [ПРОБЕЛ] чтобы начать заново', True, (250, 250, 250))
ball = Ball('ballspr.png', 475, 250, 40, 40, -3,)
player1 = Player('player_new.png', 30, 250, 16, 105, 5)
player2 = Player('player_new.png', 950, 250, 16, 105, 5)
mixer.init()
#bounce = mixer.Sound('pong.ogg')

plgroup = sprite.Group()
plgroup.add(player1)
plgroup.add(player2)

Finish = False
game = True
while game:
    win.blit(background, (0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    kpr = key.get_pressed()
    if not Finish:
    
        ball.ball_movement()
        ball.wall_bounce()
        if kpr[K_w]:
            player1.player_movement('up')
        if kpr[K_s]:
            player1.player_movement('down')
        if kpr[K_UP]:
            player2.player_movement('up')
        if kpr[K_DOWN]:
            player2.player_movement('down')
        if sprite.spritecollide(ball, plgroup, False):
            ball.player_bounce()
        if goal1 >= 7:
            winner = pl1win
            Finish = True
        elif goal2 >= 7:
            winner = pl2win
            Finish = True
        ball.update()
    if kpr[K_SPACE]:
        for i in plgroup:
            i.ToStart()
        ball.ToStart()
        goal1 = 0
        goal2 = 0
        Finish = False
    points = font1.render(str(goal1) + ':' + str(goal2), True, (250, 250, 250))
    plgroup.draw(win)
    
    
    
    
    points = font1.render(str(goal1) + ':' + str(goal2), True, (250, 250, 250))
    if Finish:
        win.blit(spaceToRestart, (200, 300))
        win.blit(winner, (270, 200))
        
    win.blit(points, (450, 10))
    clock.tick(FPS)
    display.update()