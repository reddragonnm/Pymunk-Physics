from protonPhysics import Engine

size = 700, 500
engine = Engine(size=size)

engine.new_circle((60, 200), 0.5, 0.5, impulse=(-50, -50))
engine.new_box((60, 270), (50, 50), 0.95, 0.5)
engine.new_segment((0, int(size[1]/2)), (size[0], size[1]), 1, 0.5, 0.5)

engine.make_boundary_box(1, 5)

engine.run()
