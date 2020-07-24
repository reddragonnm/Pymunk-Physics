from Physics import *
import random

mass = 3
rotation = 1.5
elasticity = 0.1
friction = 1

engine = Engine()
engine.set_gravity((0, 0))

engine.make_boundary_box(friction=1, elasticity=elasticity)
engine.set_gravity((0, 0))

p = Vec2d(100, 400)
height = 60
width = 100

vs = [(-width//2, -height//2), (width//2, -height//2), (width//2, height//2), (-width//2, height//2)]
v0, v1, v2, v3 = vs

head = engine.new_circle(p-(0, height//2), radius=15, elasticity=elasticity, friction=friction, mass=mass//5)
chassis = engine.new_polygon(p, vs, elasticity=elasticity, friction=friction, mass=mass)
wheel1 = engine.new_circle(p+v0, elasticity=elasticity, friction=friction, radius=20, mass=mass)
wheel2 = engine.new_circle(p+v1, elasticity=elasticity, friction=friction, radius=20, mass=mass)

engine.damped_string(chassis.body, head.body, rest_length=40)
engine.pivot_joint(chassis.body, wheel1.body, v3, (0, 0), False)
engine.pivot_joint(chassis.body, wheel2.body, v2, (0, 0), False)
joint = engine.simple_motor(chassis.body, wheel1.body, 0)
joint2 = engine.simple_motor(chassis.body, wheel2.body, 0)

print(type(chassis))


def event_func(event_key):
    joint.rate = 0
    joint2.rate = 0

    if event_key is None:
        return

    if event_key == K_RIGHT:
        joint.rate = -rotation
        joint2.rate = -rotation

    elif event_key == K_LEFT:
        joint.rate = rotation
        joint2.rate = rotation

engine.run(event_func=event_func)
