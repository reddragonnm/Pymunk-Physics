from protonPhysics import Engine

engine = Engine()
engine.make_boundary_box()
# engine.new_polygon(((100, 100), (200, 200), (100, 300)))

'''
segment can also be defined if body is not static or if body is dynamic and is moving
'''

engine.new_box((200, 350), (50, 50), friction=0.1)
engine.new_circle(20, (100, 200), mass=10)

# L - shaped segment
# body = pymunk.Body(mass=1, moment=1000)
# body.position = (100, 200)
# body.apply_impulse_at_local_point((0, 0))

# s1 = pymunk.Segment(body, (0, 0), (50, 0), radius=10)
# s1.density = 1

# s2 = pymunk.Segment(body, (0, 0), (0, 50), radius=10)
# s2.density = 1

# s1.elasticity = 0.999
# s2.elasticity = 0.999
# engine.space.add(body, s1, s2)

engine.run()

