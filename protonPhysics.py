import pymunk.pygame_util
import pygame as pg
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import *
from pygame.locals import *

pymunk.pygame_util.positive_y_is_up = False
pg.init()


class Engine:
    def __init__(self, color=(0, 0, 0), size=(600, 400)):
        self.size = size
        self.screen = pg.display.set_mode(self.size)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.running = True
        self.color = color

        self.space = pymunk.Space()
        self.set_gravity()

    def give_static_body(self):
        '''
        Used to return a static body
        '''

        return self.space.static_body

    def set_gravity(self, gravity=(0, 9.8)):
        '''
        Used to set the gravity of the environment
        '''

        self.space.gravity = gravity

    def run(self, event_func=None, step=0.01):
        '''
        Main function to run the physics simulation
        '''

        while self.running:

            self.screen.fill(self.color)
            self.space.debug_draw(self.draw_options)
            self.space.step(step)
            pg.display.update()

            for event in pg.event.get():
                if event.type == QUIT:
                    self.running = False

                event_func(None)
                if event.type == KEYDOWN:
                    if event_func is not None:
                        event_func(event.key)

                    if event.key == K_q or event.key == K_ESCAPE:
                        self.running = False
                    elif event.key == K_g:
                        if self.space.gravity == (0, 0):
                            self.set_gravity((0, 9.8))
                        else:
                            self.set_gravity((0, 0))

    def make_segment_from_string(self, string, thickness=0.4, size=30, recognizer_char="x", smoothen_contours=False):
        img_list = string.split()
        segments = []

        height = len(img_list)
        width = len(img_list[0])

        def segment_func(point1, point2):
            segments.append((point1, point2))

        def sample_func(point):
            x = int(point.x)
            y = (height - 1) - int(point.y)

            return 1 if img_list[y][x] == recognizer_char else 0

        bb = pymunk.BB(0, 0, height-1, width-1)

        if smoothen_contours:
            march_soft(bb, height, width, thickness, segment_func, sample_func)
        else:
            march_hard(bb, height, width, thickness, segment_func, sample_func)

        for (a, b) in segments:
            segment = pymunk.Segment(self.space.static_body, size*a, size*b, 1)
            self.space.add(segment)

    def new_circle(self, pos, radius=20, elasticity=0.5, friction=0.5, mass=1, moment=10, impulse=(0, 0)):
        body = pymunk.Body(mass=1, moment=10)
        body.position = pos
        body.apply_impulse_at_local_point(impulse)

        circle = pymunk.Circle(body, radius=radius)
        circle.elasticity = 1
        circle.friction = friction

        self.space.add(body, circle)
        return circle

    def new_segment(self, start_pos=None, end_pos=None, thickness=2, elasticity=0.2, friction=0.5,
                    surface_velocity=(0, 0), dynamic=False, mass=1, moment=10):

        '''
        Used to make a wall or ground or ceiling
        '''

        if end_pos is None:
            end_pos = self.size

        if start_pos is None:
            start_pos = 0, self.size[1]

        if not dynamic:
            segment = pymunk.Segment(self.space.static_body, start_pos, end_pos, thickness)
        else:
            body = pymunk.Body(mass, moment)
            segment = pymunk.Segment(body, start_pos, end_pos, thickness)

            self.space.add(body)

        segment.elasticity = elasticity
        segment.friction = friction
        segment.surface_velocity = surface_velocity
        self.space.add(segment)
        return segment

    def new_polygon(self, pos, vertices, elasticity=0.8, friction=0.2, mass=10, moment=10, impulse=(0, 0)):
        '''
        Used to make a polygon of any number of sides taking position of all vertices
        '''

        body = pymunk.Body(mass, moment)
        body.position = pos
        body.apply_impulse_at_local_point(impulse)

        poly = pymunk.Poly(body, vertices)
        poly.elasticity = elasticity
        poly.friction = friction
        self.space.add(body, poly)
        return poly

    def new_box(self, pos, size, elasticity=0.1, friction=0.5, mass=10, moment=10, impulse=(0, 0), give_vertices=False):
        '''
        Makes a rectangle box with position and size
        '''

        width, height = size

        vs = [(-width // 2, -height // 2), (width // 2, -height // 2), (width // 2, height // 2),
              (-width // 2, height // 2)]

        box = self.new_polygon(pos, vs, elasticity=elasticity, friction=friction, mass=mass, moment=moment,
                               impulse=impulse)

        if give_vertices:
            return box, vs
        return box

    def make_boundary_box(self, distance=0, thickness=3, elasticity=0, friction=0.8, surface_velocity=(0, 0)):
        '''
        Makes a boundary containing box around the space
        '''

        pts = [
            (distance, distance),
            (self.size[0] - distance, distance),
            (self.size[0] - distance, self.size[1] - distance),
            (distance, self.size[1] - distance)
        ]

        for i in range(4):
            this_pos = pts[i]
            next_pos = pts[(i + 1) % 4]
            segment = pymunk.Segment(self.space.static_body, this_pos, next_pos, thickness)

            segment.surface_velocity = surface_velocity
            segment.elasticity = elasticity
            segment.friction = friction

            self.space.add(segment)

    def pin_joint(self, body1, body2, body1_increment=(0, 0), body2_increment=(0, 0)):
        '''
        The most simplest type of joint connecting 2 bodies. Eg: a pendulum
        '''

        joint = pymunk.constraint.PinJoint(body1, body2, body1_increment, body2_increment)
        self.space.add(joint)

        return joint

    def pivot_joint(self, body1, body2, body1_increment=(0, 0), body2_increment=(0, 0), collide=True):
        joint = pymunk.constraint.PivotJoint(body1, body2, body1_increment, body2_increment)
        joint.collide_bodies = collide
        self.space.add(joint)

        return joint

    def damped_string(self, body1, body2, body1_increment=(0, 0), body2_increment=(0, 0), rest_length=100,
                      stiffness=100, damping=0):
        '''
        A joint with a spring between 2 bodies
        '''

        joint = pymunk.constraint.DampedSpring(body1, body2, body1_increment, body2_increment, rest_length, stiffness,
                                               damping)
        self.space.add(joint)

        return joint

    def simple_motor(self, body1, body2, rate=100):
        '''
        The most simple type of motor with 2 bodies and rate of rotation
        '''

        joint = pymunk.constraint.SimpleMotor(body1, body2, rate)
        self.space.add(joint)

        return joint

    def slide_joint(self, body1, body2, body1_increment=(0, 0), body2_increment=(0, 0), min_dist=50, max_dist=100, collide=True):
        '''
        This joint is used when you need variable distance with a minimum and maximum value like a folding pin joint
        '''

        joint = pymunk.constraint.SlideJoint(body1, body2, body1_increment, body2_increment, min_dist, max_dist)
        joint.collide_bodies = collide
        self.space.add(joint)

        return joint

    def groove_joint(self, body1, body2, groove1=(0, 0), groove2=(60, 0), anchor2=(60, 0), collide=True):
        '''
        This joint is used when you need variable distance in one direction with a minimum and maximum value
        '''

        joint = pymunk.constraint.GrooveJoint(body1, body2, groove1, groove2, anchor2)
        joint.collide_bodies = collide
        self.space.add(joint)

        return joint

    def damped_rotary_spring(self, body1, body2, angle, stiffness, damping):
        '''
        Used to make spring that can rotate
        '''

        joint = pymunk.constraint.DampedRotarySpring(body1, body2, angle, stiffness, damping)
        self.space.add(joint)

        return joint

    def rotatory_limit_joint(self, body1, body2, min_rotate=-1, max_rotate=1, collide=True):
        '''
        It is used to limit the pivot or pin joints
        '''

        joint = pymunk.constraint.RotaryLimitJoint(body1, body2, min_rotate, max_rotate)
        joint.collide_bodies = collide
        self.space.add(joint)

        return joint

    def gear_joint(self, body1, body2, phase=0, ratio=-2):
        '''
        A gear joint keeps the angular velocity ratio of a pair of bodies constant
        '''

        joint = pymunk.constraint.GearJoint(body1, body2, phase, ratio)
        self.space.add(joint)

        return joint

pg.quit()
