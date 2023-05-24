from pygame import *
clock = time.Clock()
FPS = 60


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
    def update(self):
        win.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def player_movement(self, Ydirection):
        if Ydirection == 'up' and self.rect.y >= 0:
            self.rect.y -= self.speed
        if Ydirection == 'down' and self.rect.y <= 495:
            self.rect.y += self.speed

class Ball(GameSprite):
    def ball_movement(self):
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed
        if self.rect.x >= 1000:
            self.rect.x = 450
            self.xspeed = self.speed
            self.yspeed = self.speed
        if self.rect.x <= 0:
            self.rect.x = 450
            self.xspeed = self.speed
            self.yspeed = self.speed
    def wall_bounce(self):
        if self.rect.y >= 568:
            self.rect.y -= 2
            self.yspeed = -self.yspeed
            self.ydir = 'down'
        if self.rect.y <= 0:
            self.rect.y += 2
            self.yspeed = -self.yspeed
            self.ydir = 'up'
    def player_bounce(self):
        self.xspeed = -self.xspeed
        if self.xspeed >0:
            self.xspeed +=1
        elif self.xspeed <0:
            self.xspeed -=1
        if self.yspeed >0:
            self.yspeed +=1
        elif self.yspeed <0:
            self.yspeed -=1
        
    
        
    
ball = Ball('ballspr.png', 500, 270, 32, 32, -3,)
player1 = Player('player.png', 30, 250, 32, 105, 4)
player2 = Player('player.png', 940, 250, 32, 105, 4)



plgroup = sprite.Group()
plgroup.add(player1)
plgroup.add(player2)

game = True
while game:
    win.blit(background, (0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    ball.update()
    ball.ball_movement()
    ball.wall_bounce()
    plgroup.update()
    kpr = key.get_pressed()
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
        

    clock.tick(FPS)
    display.update()