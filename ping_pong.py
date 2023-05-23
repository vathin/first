from pygame import *
clock = time.Clock()
FPS = 60


win = display.set_mode((1000, 600))
display.set_caption('ping pong')
back_color = (70, 200, 250)
background = Surface((1000, 600))
background.fill(back_color)










game = True
while game:
    win.blit(background, (0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    


    clock.tick(FPS)
    display.update()