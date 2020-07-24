from protonPhysics import Engine

engine = Engine()
engine.make_boundary_box()

b0 = engine.give_static_body()

# engine.new_circle(radius, pos, elasticity, friction, mass, moment)
circle_body = engine.new_circle(pos=(200, 300), elasticity=1, impulse=(0, 0))
circle_body2 = engine.new_circle((240, 300), elasticity=1)
circle_body3 = engine.new_circle((280, 300), elasticity=1)
circle_body4 = engine.new_circle((320, 300), elasticity=1)
circle_body5 = engine.new_circle((360, 300), elasticity=1)

engine.damped_string(b0, circle_body.body, (200, 200))
engine.pin_joint(b0, circle_body2.body, (240, 200))
engine.damped_string(b0, circle_body3.body, (280, 200))
engine.pin_joint(b0, circle_body4.body, (320, 200))
engine.damped_string(b0, circle_body5.body, (360, 200))

circle_body6 = engine.new_circle((100, 200), elasticity=1)
circle_body7 = engine.new_circle((100, 300), elasticity=1, impulse=(50, 0))
engine.pin_joint(b0, circle_body6.body, (100, 100))
engine.slide_joint(circle_body6.body, circle_body7.body)

img = """
.......
.xxx...
.xxx...
..xx...
..xxx..
..xxx..
.......
"""

# engine.make_segment_from_string(img)
engine.run()

