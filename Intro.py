import pymunk.pygame_util
import pygame as pg
pymunk.pygame_util.positive_y_is_up = False

pg.init()
size = 600, 400
screen = pg.display.set_mode(size)
draw_options = pymunk.pygame_util.DrawOptions(screen)

space = pymunk.Space()  # defining new space
space.gravity = 0, 9.8  # space.gravity = gravity to right or left, gravity to up or down

# defining the ground
b0 = space.static_body  # making static body that doesn't move
ground = pymunk.Segment(b0, (0, size[1]), (640, size[1]), 10)  # starting pos, end pos, thickness
ground.elasticity = 1  # allowing bounciness

body = pymunk.Body(mass=1, moment=10)

circle = pymunk.Circle(body, radius=20)
circle.elasticity = 1  # default 0
body.position = 100, 200  # x, y

'''
Pymunk shapes:
1. Circle
2. Poly
3. Segment
'''

space.add(
    body,
    circle,
    ground
)

while True:
    screen.fill((0, 0, 0))
    space.debug_draw(draw_options)
    
    space.step(0.01)  # speed through which simulation should run
    pg.display.update()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()


