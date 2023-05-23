from pygame import *
clock = time.Clock()
FPS = 60


win = display.set_mode((1000, 600))
display.set_caption('ping pong')
back_color = (70, 200, 250)
background = Surface((1000, 600))
background.fill(back_color)
class GameSprite(sprite.Sprite):
    def __init__(self, load_image, xpos, ypos, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(load_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
    def update(self):
        win.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def player_movement(self, Ydirection):
        if self.Ydirection == 'up':
            self.rect.y += self.speed
        if self.Ydirection == 'down':
            self.rect.y -= self.speed





game = True
while game:
    win.blit(background, (0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    


    clock.tick(FPS)
    display.update()