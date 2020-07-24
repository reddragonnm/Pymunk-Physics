from protonPhysics import Engine
import pymunk.pygame_util

engine = Engine()

body = pymunk.Body(mass=1, moment=10)
body.position = 100, 200

circle = pymunk.Circle(body, radius=40, offset=(20, 0))
circle.elasticity = 1

circle2 = pymunk.Circle(body, radius=40, offset=(-30, 0))
circle2.elasticity = 1
circle2.color = (255, 0, 0)

engine.space.add(body, circle, circle2)
engine.run()
